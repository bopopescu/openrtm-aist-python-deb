#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file OpenHRPExecutionContext.py
# @brief OpenHRPExecutionContext class
# @date $Date: 2007/08/29$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import threading
import time

import OpenRTM_aist
import OpenRTM, OpenRTM__POA, RTC, RTC__POA


class OpenHRPExecutionContext(OpenRTM_aist.ExecutionContextBase,
                              OpenRTM__POA.ExtTrigExecutionContextService):
  """
  """

  def __init__(self):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.exttrig_sync_ec")
    self._rtcout.RTC_TRACE("OpenHRPExecutionContext.__init__()")
    OpenRTM_aist.ExecutionContextBase.__init__(self, "exttrig_sync_ec")

    self.setObjRef(self._this())
    self.setKind(RTC.PERIODIC)
    self.setRate(OpenRTM_aist.DEFAULT_EXECUTION_RATE)
    self._rtcout.RTC_DEBUG("Actual rate: %d [sec], %d [usec]",
                           (self._profile.getPeriod().sec(), self._profile.getPeriod().usec()))    
    self._tickmutex = threading.RLock()
    self._count = 0
    return


  def __del__(self):
    self._rtcout.RTC_TRACE("OpenHRPExecutionContext().__del__()")
    return


  #============================================================
  # OpenHRPExecutionContextService
  #============================================================
  ##
  # @if jp
  # @brief ������1���ƥå׿ʤ��
  # @else
  # @brief Move forward one step of ExecutionContext
  # @endif
  def tick(self):
    self._rtcout.RTC_TRACE("tick()")
    if not self.isRunning():
      return

    guard = OpenRTM_aist.ScopedLock(self._tickmutex)

    OpenRTM_aist.ExecutionContextBase.invokeWorkerPreDo(self) # update state
    t0 = OpenRTM_aist.Time()
    OpenRTM_aist.ExecutionContextBase.invokeWorkerDo(self)
    t1 = OpenRTM_aist.Time()
    OpenRTM_aist.ExecutionContextBase.invokeWorkerPostDo(self)
    t2 = OpenRTM_aist.Time()

    period = self.getPeriod()

    if self._count > 1000:
      excdotm = (t1 - t0).getTime().toDouble()
      excpdotm = (t2 - t1).getTime().toDouble()
      slptm = period.toDouble() - (t2 - t0).getTime().toDouble()
      self._rtcout.RTC_PARANOID("Period:      %f [s]", period.toDouble())
      self._rtcout.RTC_PARANOID("Exec-Do:     %f [s]", excdotm)
      self._rtcout.RTC_PARANOID("Exec-PostDo: %f [s]", excpdotm)
      self._rtcout.RTC_PARANOID("Sleep:       %f [s]", slptm)

    t3 = OpenRTM_aist.Time()
    if period.toDouble() > (t2 - t0).getTime().toDouble():
      if self._count > 1000:
        self._rtcout.RTC_PARANOID("sleeping...")
        slptm = period.toDouble() - (t2 - t0).getTime().toDouble()
        time.sleep(slptm)

    if self._count > 1000:
      t4 = OpenRTM_aist.Time()
      self._rtcout.RTC_PARANOID("Slept:       %f [s]", (t4 - t3).getTime().toDouble())
      self._count = 0

    self._count += 1
    return


  #============================================================
  # ExecutionContextService
  #============================================================
  ##
  # @if jp
  # @brief ExecutionContext �¹Ծ��ֳ�ǧ�ؿ�
  # @else
  # @brief Check for ExecutionContext running state
  # @endif
  # CORBA::Boolean OpenHRPExecutionContext::is_running()
  #   throw (CORBA::SystemException)
  def is_running(self):
    return OpenRTM_aist.ExecutionContextBase.isRunning(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ򳫻�
  # @else
  # @brief Start the ExecutionContext
  # @endif
  # RTC::ReturnCode_t OpenHRPExecutionContext::start()
  #   throw (CORBA::SystemException)
  def start(self):
    return OpenRTM_aist.ExecutionContextBase.start(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ����
  # @else
  # @brief Stop the ExecutionContext
  # @endif
  # RTC::ReturnCode_t OpenHRPExecutionContext::stop()
  #   throw (CORBA::SystemException)
  def stop(self):
    return OpenRTM_aist.ExecutionContextBase.stop(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)���������
  # @else
  # @brief Get execution rate(Hz) of ExecutionContext
  # @endif
  # CORBA::Double OpenHRPExecutionContext::get_rate()
  #   throw (CORBA::SystemException)
  def get_rate(self):
    return OpenRTM_aist.ExecutionContextBase.getRate(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)�����ꤹ��
  # @else
  # @brief Set execution rate(Hz) of ExecutionContext
  # @endif
  # RTC::ReturnCode_t OpenHRPExecutionContext::set_rate(CORBA::Double rate)
  #   throw (CORBA::SystemException)
  def set_rate(self, rate):
    return OpenRTM_aist.ExecutionContextBase.setRate(self, rate)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��ɲä���
  # @else
  # @brief Add an RT-Component
  # @endif
  # RTC::ReturnCode_t
  # OpenHRPExecutionContext::add_component(RTC::LightweightRTObject_ptr comp)
  #   throw (CORBA::SystemException)
  def add_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.addComponent(self, comp)


  ##
  # @if jp
  # @brief ����ݡ��ͥ�Ȥ򥳥�ݡ��ͥ�ȥꥹ�Ȥ���������
  # @else
  # @brief Remove the RT-Component from participant list
  # @endif
  # RTC::ReturnCode_t OpenHRPExecutionContext::
  # remove_component(RTC::LightweightRTObject_ptr comp)
  #   throw (CORBA::SystemException)
  def remove_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.removeComponent(self, comp)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ򥢥��ƥ��ֲ�����
  # @else
  # @brief Activate an RT-Component
  # @endif
  # RTC::ReturnCode_t OpenHRPExecutionContext::
  # activate_component(RTC::LightweightRTObject_ptr comp)
  #   throw (CORBA::SystemException)
  def activate_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.activateComponent(self, comp)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ�����
  # @else
  # @brief Deactivate an RT-Component
  # @endif
  # RTC::ReturnCode_t OpenHRPExecutionContext::
  # deactivate_component(RTC::LightweightRTObject_ptr comp)
  #   throw (CORBA::SystemException)
  def deactivate_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.deactivateComponent(self, comp)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ�ꥻ�åȤ���
  # @else
  # @brief Reset the RT-Component
  # @endif
  # RTC::ReturnCode_t OpenHRPExecutionContext::
  # reset_component(RTC::LightweightRTObject_ptr comp)
  #   throw (CORBA::SystemException)
  def reset_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.resetComponent(self, comp)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥξ��֤��������
  # @else
  # @brief Get RT-Component's state
  # @endif
  # RTC::LifeCycleState OpenHRPExecutionContext::
  # get_component_state(RTC::LightweightRTObject_ptr comp)
  #   throw (CORBA::SystemException)
  # get_component_state(RTC::LightweightRTObject_ptr comp)
  #   throw (CORBA::SystemException)
  def get_component_state(self, comp):
    return OpenRTM_aist.ExecutionContextBase.getComponentState(self, comp)


  ##
  # @if jp
  # @brief ExecutionKind ���������
  # @else
  # @brief Get the ExecutionKind
  # @endif
  # RTC::ExecutionKind OpenHRPExecutionContext::get_kind()
  #   throw (CORBA::SystemException)
  def get_kind(self):
    return OpenRTM_aist.ExecutionContextBase.getKind(self)


  #------------------------------------------------------------
  # ExecutionContextService interfaces
  #------------------------------------------------------------
  ##
  # @if jp
  # @brief ExecutionContextProfile ���������
  # @else
  # @brief Get the ExecutionContextProfile
  # @endif
  # RTC::ExecutionContextProfile* OpenHRPExecutionContext::get_profile()
  #   throw (CORBA::SystemException)
  def get_profile(self):
    return OpenRTM_aist.ExecutionContextBase.getProfile(self)


def OpenHRPExecutionContextInit(manager):
  OpenRTM_aist.ExecutionContextFactory.instance().addFactory("OpenHRPExecutionContext",
                                                             OpenRTM_aist.OpenHRPExecutionContext,
                                                             OpenRTM_aist.ECDelete)
  return
