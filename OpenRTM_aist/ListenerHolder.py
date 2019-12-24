#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ListnerHolder.py
# @brief Listener holder class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2011
#     Noriaki Ando
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.
#
# $Id$
#

import threading
import OpenRTM_aist


##
# @if jp
# @class Listener �ۥ�������饹
#
# ���Υ��饹�ϡ��ꥹ�ʥ��饹��ñ����ݻ���������Ԥ��ꥹ�ʥۥ������
# ���Ǥ��롣���Υ��饹�����Ѥ��뤿��ˤϡ��ƥ�ץ졼�Ȥ��裱��������
# ����ꥹ�ʥ��饹 (Listener���饹) ����ӡ�����ListenerHolder���饹
# �ƥ�ץ졼�Ȥ�Ѿ����ơ��ºݤ˥ꥹ�ʤθƤӽФ���Ԥ�
# ListenerHolder�������饹���������ɬ�פ����롣
#
# ���Υ��饹�ϡ�����åɥ����֤�¸����뤿�ᡢ�ꥹ�ʤ��ɲäȺ���ˤ�
# ���Ƥϥߥ塼�ƥå����ˤ���å���ԤäƤ��롣�����˥���åɥ�����
# �ʥꥹ�ʴ�����¸����뤿��ˤϥꥹ�ʤΥ�����Хå��򥳡��뤹��ݤ�
# ��ߥ塼�ƥå��ˤ���å���Ԥ�ɬ�פ����롣
#
# @section Listener���饹�����
#
# ���٥��ȯ�����˥�����Хå��������дؿ�����Ĵ��쥯�饹�����
# ���롣������Хå��Τ���Υ��дؿ��ϡ�Ǥ�դ�����͡���������Ĥ�
# �Τ�����Ǥ����̾�δؿ��Ǥ��äƤ�褤����operator()�ʤɤΥե���
# ���Ȥ���������Ƥ�褤���ºݤˤϴ��쥯�饹�ˤƤ����δؿ����貾
# �۴ؿ��Ȥ�������������Υ��饹��Ѿ����ơ��ºݤΥꥹ�ʥ��饹�����
# ���뤳�Ȥˤʤ롣�ޤ����ҤȤĤΥꥹ�ʥ��饹��ʣ���Υ�����Хå��ؿ�
# ��������Ƥ�褤���ºݤˤϡ������Υ�����Хå��ؿ���ºݤ˸Ƥӽ�
# ����ˡ�˴ؤ��Ƥϡ�����ListenerHolder�������饹�ˤƾܤ���������뤳
# �Ȥˤʤ롣
# <pre>
# class MyListenerBase
# {
# public:
#   // ������Хå��ؿ�1: �ؿ��ƤӽФ��黻�Ҥˤ�륳����Хå��ؿ�
#   // ������ե��󥯥��Τ褦�˥�����Хå��ؿ�����������㡣
#   virtual void operator()(std::string strarg) = 0; // ��貾�۴ؿ�
#   
#   // ������Хå��δؿ������˥��㤬¿�ͤǤ����硢���Τ褦��ñ��
#   // ����дؿ��Ȥ���������뤳�Ȥ��ǽ��
#   virtual void onEvent0(const char* arg0) = 0;
#   virtual void onEvent1(int arg0) = 0;
#   virtual void onEvent2(double arg0) = 0;
#   virtual void onEvent3(HogeProfile& arg0) = 0;
# };
# </pre>
#
# @section ListenerHolder�������饹
#
# ListenerHolder�������饹�Ϥ���LsitenerHolder���饹�ƥ�ץ졼�Ȥ��
# �����ơ����������� MyListenerBase ���饹���ɲäȺ���ʤɴ������
# �������ļºݤ˥�����Хå��ؿ���ƤӽФ���ʬ��������뤳�Ȥˤʤ롣
# �ºݤ˥�����Хå���ƤӽФ���ʬ�Ǥϡ��ؿ������˥��㤬¿��¿�ͤǤ���
# ���ꡢ�ҤȤĤΥꥹ�ʥ��饹��ʣ���Υ�����Хå��ؿ�����ľ�礬����
# ���ᡢ���̤Υꥹ�ʥ��饹���б����뤿�ᡢ���θƤӽФ���ʬ��ɬ�פȤ�
# �롣ListenerHolder�������饹�ϡ�MyListenerBase���饹��Ʊ�������˥���
# ����ĥ��дؿ��������ؿ������Ǥϡ�ListenerHolder���饹�����ġ�
# m_listeners, m_mutex �Τ������ĤΥ����ѿ������Ѥ��ơ���Ͽ����
# ���ꥹ�ʥ��֥������ȤΥ����ѿ���ƤӽФ���
#
# <pre>
# class MyListenerHolderImpl
#  : public ::RTM::util::ListenerHolder<MyListenerBase>
# {
# public:
#   // �ؿ��ƤӽФ��黻�ҤΥ�����Хå��ؿ��ξ��
#   virtual void operator()(std::string strarg)
#   {
#     Gurad gurad(m_mutex);
#     for (int i(0), len(m_listeners.size()); i < len; ++i)
#     {
#       m_listeners[i].first->operator()(strarg);
#     }
#   }
#
#   virtual void onEvent0(const char* arg0)
#   {
#     Gurad gurad(m_mutex);
#     for (int i(0), len(m_listeners.size()); i < len; ++i)
#     {
#       m_listeners[i].first->onEvent(arg0);
#     }
#   }
# };
# </pre>
#
# �ꥹ�ʥ��֥������ȤؤΥݥ��󥿤��Ǽ���Ƥ���Entry���֥������Ȥ�
# std::pair<ListenerClass, bool> �Ȥ����������Ƥ��ꡢfirst��
# Listener���֥������ȤؤΥݥ��󥿡�second����ư����ե饰�Ǥ��롣��
# �����äơ��ꥹ�ʥ��֥������Ȥإ�������������ˤ�first����Ѥ��롣
# �ޥ������åɴĶ������Ѥ��뤳�Ȥ����ꤵ�����ϡ�Guard
# guard(m_mutex) �ˤ���å���˺�줺�˹Ԥ����ȡ�
# 
# @section ListenerHolder�������饹������
# �������줿MyListenerHolderImpl�ϰ���Ȥ��ưʲ��Τ褦�����Ѥ��롣
#
# <pre>
# // ���Ȥ��Х��饹���ФȤ������
# MyListenerHolderImpl m_holder;
#
# // ��Ͽ����ư���꡼��⡼�ɤ���Ͽ��
# // ���֥������Ȥκ����Holder���饹��Ǥ����
# m_holder.addListener(new MyListener0(), true); // MyListener0��
# 
# // ������Хå���ƤӽФ�
# m_holder.operator()(strarg);
# m_holder.onEvent0("HogeHoge);
# </pre>
#
# @else
#
# @class Listener holder class
#
# @endif
#
class ListenerHolder:
  """
  """

  ##
  # @if jp
  # @brief ListenerHolder���饹���󥹥ȥ饯��
  # @else
  # @brief ListenerHolder class ctor 
  # @endif
  def __init__(self):
    self.listener_mutex = threading.RLock()
    self.listeners = []
    return


  ##
  # @if jp
  # @brief ListenerHolder�ǥ��ȥ饯��
  # @else
  # @brief ListenerHolder class dtor 
  # @endif
  def __del__(self):
    guard = OpenRTM_aist.ScopedLock(self.listener_mutex)
    
    for listener_ in self.listeners:
      for (l,f) in listener_.iteritems():
        if f:
          del l
    del guard
    return
  
  ##
  # @if jp
  # @brief �ꥹ�ʤ��ɲä���
  # @else
  # @brief add listener object
  # @endif
  # virtual void addListener(ListenerClass* listener,
  #                          bool autoclean)
  def addListener(self, listener, autoclean):
    guard = OpenRTM_aist.ScopedLock(self.listener_mutex)
    self.listeners.append({listener:autoclean})
    del guard
    return
    
  ##
  # @if jp
  # @brief �ꥹ�ʤ�������
  # @else
  # @brief remove listener object
  # @endif
  # virtual void removeListener(ListenerClass* listener)
  def removeListener(self, listener):
    guard = OpenRTM_aist.ScopedLock(self.listener_mutex)
    for (i, listener_) in enumerate(self.listeners):
      if listener == listener:
        del self.listeners[i]
        return
    return

  def LISTENERHOLDER_CALLBACK(self, func, *args):
    guard = OpenRTM_aist.ScopedLock(self.listener_mutex)
    for listener in self.listeners:
      for (l,f) in listener.iteritems():
        func_ = getattr(l,func,None)
        func_(*args)
    return
