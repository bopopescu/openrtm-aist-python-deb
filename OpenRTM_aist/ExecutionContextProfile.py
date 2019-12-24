#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ExecutionContextProfile.py
# @brief ExecutionContextProfile class
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
from omniORB import CORBA, PortableServer

import OpenRTM_aist
import RTC

DEFAULT_PERIOD = 0.000001

##
# @if jp
# @class ExecutionContextProfile
# @brief ExecutionContextProfile ���饹
#
# @since 1.2.0
#
# @else
# @class ExecutionContextProfile
# @brief ExecutionContextProfile class
#
# @since 1.2.0
#
# @endif
class ExecutionContextProfile:
  """
  """

  ##
  # @if jp
  # @brief �ǥե���ȥ��󥹥ȥ饯��
  #
  # �ǥե���ȥ��󥹥ȥ饯��
  # �ץ�ե�����˰ʲ��ι��ܤ����ꤹ�롣
  #  - kind : PERIODIC
  #  - rate : 0.0
  #
  # @else
  # @brief Default Constructor
  #
  # Default Constructor
  # Set the following items to profile.
  #  - kind : PERIODIC
  #  - rate : 0.0
  #
  # @endif
  # ExecutionContextProfile(RTC::ExecutionKind kind = RTC::PERIODIC);
  def __init__(self, kind = RTC.PERIODIC):
    global DEFAULT_PERIOD
    self._rtcout  = OpenRTM_aist.Manager.instance().getLogbuf("periodic_ecprofile")
    self._period = OpenRTM_aist.TimeValue(DEFAULT_PERIOD)
    self._rtcout.RTC_TRACE("ExecutionContextProfile.__init__()")
    self._rtcout.RTC_DEBUG("Actual rate: %d [sec], %d [usec]",
                           (self._period.sec(), self._period.usec()))
    self._profileMutex = threading.RLock()
    self._ref = None
    self._profile = RTC.ExecutionContextProfile(RTC.PERIODIC,
                                                (1.0/self._period.toDouble()),
                                                None, [], [])
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  #
  # �ǥ��ȥ饯��
  #
  # @else
  # @brief Destructor
  #
  # Destructor
  #
  # @endif
  def __del__(self):
    self._rtcout.RTC_TRACE("ExecutionContextProfile.__del__()")

    # cleanup EC's profile
    self._profile.owner = None
    self._profile.participants = []
    self._profile.properties = []
    self._ref = None
    return


  ##
  # @if jp
  # @brief CORBA ���֥������Ȼ��Ȥ򥻥å�
  #
  # ExecutioncontextService �Ȥ��Ƥ� CORBA ���֥���
  # ���Ȼ��Ȥ򥻥åȤ��롣
  #
  # @param ec_ptr CORBA ���֥������Ȼ���
  #
  # @else
  # @brief Set the reference to the CORBA object
  #
  # Set the reference to the CORBA object as
  # ExecutioncontextService of this object.
  #
  # @param ec_ptr The reference to CORBA object
  #
  # @endif
  # void setObjRef(RTC::ExecutionContextService_ptr ec_ptr);
  def setObjRef(self, ec_ptr):
    self._rtcout.RTC_TRACE("setObjRef()")
    assert(not CORBA.is_nil(ec_ptr))
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    self._ref = ec_ptr
    del guard
    return


  ##
  # @if jp
  # @brief CORBA ���֥������Ȼ��Ȥμ���
  #
  # �ܥ��֥������Ȥ� ExecutioncontextService �Ȥ��Ƥ� CORBA ���֥���
  # ���Ȼ��Ȥ�������롣
  #
  # @return CORBA ���֥������Ȼ���
  #
  # @else
  # @brief Get the reference to the CORBA object
  #
  # Get the reference to the CORBA object as
  # ExecutioncontextService of this object.
  #
  # @return The reference to CORBA object
  #
  # @endif
  # RTC::ExecutionContextService_ptr getObjRef(void) const;
  def getObjRef(self):
    self._rtcout.RTC_TRACE("getObjRef()")
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    return self._ref


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)�����ꤹ��
  #
  # Active ���֤ˤ�RT����ݡ��ͥ�Ȥ��¹Ԥ�������(ñ��:Hz)�����ꤹ
  # �롣�¹Լ������ѹ��ϡ�DataFlowComponentAction ��
  # on_rate_changed �ˤ�äƳ�RT����ݡ��ͥ�Ȥ���ã����롣
  #
  # @param rate ��������(ñ��:Hz)
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #         RTC_OK: ���ｪλ
  #         BAD_PARAMETER: �����ͤ������
  #
  # @else
  #
  # @brief Set execution rate(Hz) of ExecutionContext
  #
  # This operation shall set the rate (in hertz) at which this
  # context��s Active participating RTCs are being called.  If the
  # execution kind of the context is PERIODIC, a rate change shall
  # result in the invocation of on_rate_changed on any RTCs
  # realizing DataFlowComponentAction that are registered with any
  # RTCs participating in the context.
  #
  # @param rate Execution cycle(Unit:Hz)
  #
  # @return The return code of ReturnCode_t type
  #         RTC_OK: Succeed
  #         BAD_PARAMETER: Invalid value. The value might be negative.
  #
  # @endif
  # RTC::ReturnCode_t setRate(double rate);
  def setRate(self, rate):
    self._rtcout.RTC_TRACE("setRate(%f)", rate)
    if rate < 0.0:
      return RTC.BAD_PARAMETER

    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    self._profile.rate = rate
    self._period = OpenRTM_aist.TimeValue(1.0 / rate)
    return RTC.RTC_OK


  # RTC::ReturnCode_t setPeriod(double sec, coil::TimeValue tv);
  def setPeriod(self, sec=None, tv=None):
    if sec:
      self._rtcout.RTC_TRACE("setPeriod(%f [sec])", sec)
      if sec < 0.0:
        return RTC.BAD_PARAMETER

      guard = OpenRTM_aist.ScopedLock(self._profileMutex)
      self._profile.rate = 1.0 / sec
      self._period = OpenRTM_aist.TimeValue(sec)
      del guard
      return RTC.RTC_OK;
    elif tv:
      self._rtcout.RTC_TRACE("setPeriod(%f [sec])", tv.toDouble())
      if tv.toDouble() < 0.0:
        return RTC.BAD_PARAMETER

      guard = OpenRTM_aist.ScopedLock(self._profileMutex)
      self._profile.rate = 1.0 / tv.toDouble()
      self._period = tv
      del guard
      return RTC.RTC_OK
    return RTC.BAD_PARAMETER


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)���������
  #
  # Active ���֤ˤ�RT����ݡ��ͥ�Ȥ��¹Ԥ�������(ñ��:Hz)�������
  # �롣
  #
  # @return ��������(ñ��:Hz)
  #
  # @else
  #
  # @brief Get execution rate(Hz) of ExecutionContext
  #
  # This operation shall return the rate (in hertz) at which its
  # Active participating RTCs are being invoked.
  #
  # @return Execution cycle(Unit:Hz)
  #
  # @endif
  # double getRate(void) const;
  def getRate(self):
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    return self._profile.rate


  # coil::TimeValue getPeriod(void) const;
  def getPeriod(self):
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    return self._period


  ##
  # @if jp
  # @brief ExecutionKind ��ʸ���󲽤���
  #
  # RTC::ExecutionKind ���������Ƥ��� PERIODIC, EVENT_DRIVEN,
  # OTHER ��ʸ���󲽤��롣
  #
  # @param kind ExecutionKind
  # @return ʸ���󲽤��줿ExecutionKind
  #
  # @else
  #
  # @brief Converting ExecutionKind enum to string 
  #
  # This function converts enumeration (PERIODIC, EVENT_DRIVEN,
  # OTHER) defined in RTC::ExecutionKind to string.
  #
  # @param kind ExecutionKind
  # @return String of ExecutionKind
  #
  # @endif
  # const char* getKindString(RTC::ExecutionKind kind) const;
  def getKindString(self, kind=None):
    kinds_ = ["PERIODIC", "EVENT_DRIVEN", "OTHER"]
    if not kind:
      kind_ = self._profile.kind
    else:
      kind_ = kind

    if kind_ < RTC.PERIODIC or kind_ > RTC.OTHER:
      return ""

    return kinds_[kind_._v]


  ##
  # @if jp
  # @brief ExecutionKind �����ꤹ��
  #
  # ���� ExecutionContext �� ExecutionKind �����ꤹ��
  #
  # @param kind ExecutionKind
  #
  # @else
  #
  # @brief Set the ExecutionKind
  #
  # This operation sets the kind of the execution context.
  #
  # @param kind ExecutionKind
  #
  # @endif
  # RTC::ReturnCode_t setKind(RTC::ExecutionKind kind);
  def setKind(self, kind):
    if kind < RTC.PERIODIC or kind > RTC.OTHER:
      self._rtcout.RTC_ERROR("Invalid kind is given. %d", kind._v)
      return RTC.BAD_PARAMETER

    self._rtcout.RTC_TRACE("setKind(%s)", self.getKindString(kind))
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    self._profile.kind = kind
    del guard
    return RTC.RTC_OK


  ##
  # @if jp
  # @brief ExecutionKind ���������
  #
  # �� ExecutionContext �� ExecutionKind ���������
  #
  # @return ExecutionKind
  #
  # @else
  #
  # @brief Get the ExecutionKind
  #
  # This operation shall report the execution kind of the execution
  # context.
  #
  # @return ExecutionKind
  #
  # @endif
  # RTC::ExecutionKind getKind(void) const;
  def getKind(self):
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    self._rtcout.RTC_TRACE("%s = getKind()", self.getKindString(self._profile.kind))
    return self._profile.kind


  ##
  # @if jp
  # @brief Owner����ݡ��ͥ�Ȥ򥻥åȤ��롣
  #
  # ����EC��Owner�Ȥʤ�RTC�򥻥åȤ��롣
  #
  # @param comp Owner�Ȥʤ�RT����ݡ��ͥ��
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # @else
  # @brief Setting owner component of the execution context
  #
  # This function sets an RT-Component to be owner of the execution context.
  #
  # @param comp an owner RT-Component of this execution context
  # @return The return code of ReturnCode_t type
  # @endif
  # RTC::ReturnCode_t setOwner(RTC::LightweightRTObject_ptr comp);
  def setOwner(self, comp):
    self._rtcout.RTC_TRACE("setOwner()")
    assert(not CORBA.is_nil(comp))
    rtobj_ = comp._narrow(RTC.RTObject)
    if CORBA.is_nil(rtobj_):
      self._rtcout.RTC_ERROR("Narrowing failed.")
      return RTC.BAD_PARAMETER

    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    self._profile.owner = rtobj_
    del guard
    return RTC.RTC_OK


  ##
  # @if jp
  # @brief Owner����ݡ��ͥ�Ȥλ��Ȥ��������
  #
  # ����EC��Owner�Ǥ���RTC�λ��Ȥ�������롣
  #
  # @return OwnerRT����ݡ��ͥ�Ȥλ���
  # @else
  # @brief Getting a reference of the owner component
  #
  # This function returns a reference of the owner RT-Component of
  # this execution context
  #
  # @return a reference of the owner RT-Component
  # @endif
  # const RTC::RTObject_ptr getOwner() const;
  def getOwner(self):
    self._rtcout.RTC_TRACE("getOwner()")
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    return self._profile.owner


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��ɲä���
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ��ɲä��롣�ɲä��줿RT��
  # ��ݡ��ͥ�Ȥ� attach_context ���ƤФ졢Inactive ���֤����ܤ��롣
  # ���ꤵ�줿RT����ݡ��ͥ�Ȥ�null�ξ��ϡ�BAD_PARAMETER ���֤���
  # �롣���ꤵ�줿RT����ݡ��ͥ�Ȥ� DataFlowComponent �ʳ��ξ��ϡ�
  # BAD_PARAMETER ���֤���롣
  #
  # @param comp �ɲ��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Add an RT-component
  #
  # The operation causes the given RTC to begin participating in
  # the execution context.  The newly added RTC will receive a call
  # to LightweightRTComponent::attach_context and then enter the
  # Inactive state.  BAD_PARAMETER will be invoked, if the given
  # RT-Component is null or if the given RT-Component is other than
  # DataFlowComponent.
  #
  # @param comp The target RT-Component for add
  #
  # @return The return code of ReturnCode_t type
  #
  # @endif
  # RTC::ReturnCode_t addComponent(RTC::LightweightRTObject_ptr comp);
  def addComponent(self, comp):
    self._rtcout.RTC_TRACE("addComponent()")
    if CORBA.is_nil(comp):
      self._rtcout.RTC_ERROR("A nil reference was given.")
      return RTC.BAD_PARAMETER

    rtobj_ = comp._narrow(RTC.RTObject)
    if CORBA.is_nil(rtobj_):
      self._rtcout.RTC_ERROR("Narrowing was failed.")
      return RTC.RTC_ERROR

    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    OpenRTM_aist.CORBA_SeqUtil.push_back(self._profile.participants,
                                         rtobj_)
    del guard
    return RTC.RTC_OK


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ���������
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ��������롣������줿
  # RT����ݡ��ͥ�Ȥ� detach_context ���ƤФ�롣���ꤵ�줿RT����ݡ�
  # �ͥ�Ȥ����üԥꥹ�Ȥ���Ͽ����Ƥ��ʤ����ϡ�BAD_PARAMETER ����
  # ����롣
  #
  # @param comp ����о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Remove the RT-Component from participant list
  #
  # This operation causes a participant RTC to stop participating in the
  # execution context.
  # The removed RTC will receive a call to
  # LightweightRTComponent::detach_context.
  # BAD_PARAMETER will be returned, if the given RT-Component is not
  # participating in the participant list.
  #
  # @param comp The target RT-Component for delete
  #
  # @return The return code of ReturnCode_t type
  #
  # @endif
  # RTC::ReturnCode_t removeComponent(RTC::LightweightRTObject_ptr comp);
  def removeComponent(self, comp):
    self._rtcout.RTC_TRACE("removeComponent()")
    if CORBA.is_nil(comp):
      self._rtcout.RTC_ERROR("A nil reference was given.")
      return RTC.BAD_PARAMETER

    rtobj_ = comp._narrow(RTC.RTObject)
    if CORBA.is_nil(rtobj_):
      self._rtcout.RTC_ERROR("Narrowing was failed.")
      return RTC.RTC_ERROR

    guard = OpenRTM_aist.ScopedLock(self._profileMutex)

    index_ = OpenRTM_aist.CORBA_SeqUtil.find(self._profile.participants,
                                             self.find_participant(rtobj_))
    if index_ < 0:
      self._rtcout.RTC_ERROR("The given RTObject does not exist in the EC.")
      return RTC.BAD_PARAMETER
    OpenRTM_aist.CORBA_SeqUtil.erase(self._profile.participants, index_)
    return RTC.RTC_OK


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥλ��üԥꥹ�Ȥ��������
  #
  # ������Ͽ����Ƥ��뻲�ü�RTC�Υꥹ�Ȥ�������롣
  #
  # @return ���ü�RTC�Υꥹ��
  #
  # @else
  #
  # @brief Getting participant RTC list
  #
  # This function returns a list of participant RTC of the execution context.
  #
  # @return Participants RTC list
  #
  # @endif
  # const RTC::RTCList& getComponentList() const;
  def getComponentList(self):
    self._rtcout.RTC_TRACE("getComponentList(%d)", len(self._profile.participants))
    return self._profile.participants


  ##
  # @if jp
  # @brief Properties�򥻥åȤ���
  #
  # ExecutionContextProfile::properties �򥻥åȤ��롣
  #
  # @param props ExecutionContextProfile::properties �˥��åȤ����
  #              ��ѥƥ���
  #
  # @else
  # @brief Setting Properties
  #
  # This function sets ExecutionContextProfile::properties by
  # coil::Properties.
  #
  # @param props Properties to be set to
  #              ExecutionContextProfile::properties.
  #
  # @endif
  # void setProperties(coil::Properties& props);
  def setProperties(self, props):
    self._rtcout.RTC_TRACE("setProperties()")
    self._rtcout.RTC_DEBUG(props)
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    OpenRTM_aist.NVUtil.copyFromProperties(self._profile.properties, props)
    del guard
    return

  
  ##
  # @if jp
  # @brief Properties���������
  #
  # ExecutionContextProfile::properties ��������롣
  #
  # @return coil::Properties���Ѵ����줿
  #              ExecutionContextProfile::properties
  #
  # @else
  # @brief Setting Properties
  #
  # This function sets ExecutionContextProfile::properties by
  # coil::Properties.
  #
  # @param props Properties to be set to ExecutionContextProfile::properties.
  #
  # @endif
  # const coil::Properties getProperties() const;
  def getProperties(self):
    self._rtcout.RTC_TRACE("getProperties()")
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    props_ = OpenRTM_aist.Properties()
    OpenRTM_aist.NVUtil.copyToProperties(props_, self._profile.properties)
    del guard
    self._rtcout.RTC_DEBUG(props_)
    return props_


  ##
  # @if jp
  # @brief Profile���������
  #
  # RTC::ExecutionContextProfile ��������롣��������
  # ExecutionContextProfile �ν�ͭ���ϸƤӽФ�¦�ˤ��롣�������줿��
  # �֥������Ȥ����פˤʤä���硢�ƤӽФ�¦������������Ǥ���餦��
  #
  # @return RTC::ExecutionContextProfile
  #
  # @else
  # @brief Getting Profile
  #
  # This function gets RTC::ExecutionContextProfile.  The ownership
  # of the obtained ExecutionContextProfile is given to caller. The
  # caller should release obtained object when it is unneccessary
  # anymore.
  #
  # @return RTC::ExecutionContextProfile
  #
  # @endif
  # RTC::ExecutionContextProfile* getProfile(void);
  def getProfile(self):
    self._rtcout.RTC_TRACE("getProfile()")
    guard = OpenRTM_aist.ScopedLock(self._profileMutex)
    return self._profile


  ##
  # @if jp
  # @brief ExecutionContextProfile���å�����
  #
  # ���Υ��֥������Ȥ��������� RTC::ExecutionContextProfile ���å����롣
  # ��å������פˤʤä��ݤˤ�unlock()�ǥ�å��������ʤ���Фʤ�ʤ���
  #
  # @else
  # @brief Getting a lock of RTC::ExecutionContextProfile
  #
  # This function locks  RTC::ExecutionContextProfile in the object.
  # The lock should be released when the lock is unneccessary.
  #
  # @endif
  # void lock() const;
  def lock(self):
    self._profileMutex.acquire()
    return


  ##
  # @if jp
  # @brief ExecutionContextProfile�򥢥��å�����
  #
  # ���Υ��֥������Ȥ��������� RTC::ExecutionContextProfile �򥢥���
  # �����롣
  #
  # @else
  # @brief Release a lock of the RTC::ExecutionContextProfile
  #
  # This function release the lock of RTC::ExecutionContextProfile
  # in the object.
  #
  # @endif
  # void unlock() const;
  def unlock(self):
    self._profileMutex.release()
    return

  class find_participant:
    def __init__(self, comp):
      self._comp = comp
      return

    def __call__(self, comp):
      return self._comp._is_equivalent(comp)
