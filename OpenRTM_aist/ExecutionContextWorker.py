#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ExecutionContextWorker.py
# @brief ExecutionContext's state machine worker class
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


##
# @if jp
# @class PeriodicExecutionContext
# @brief PeriodicExecutionContext ���饹
#
# Periodic Sampled Data Processing(�����¹���)ExecutionContext���饹��
#
# @since 0.4.0
#
# @else
# @class PeriodicExecutionContext
# @brief PeriodicExecutionContext class
#
# Periodic Sampled Data Processing (for the execution cycles)
# ExecutionContext class
#
# @since 0.4.0
#
# @endif
class ExecutionContextWorker:
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
  def __init__(self):
    self._rtcout  = OpenRTM_aist.Manager.instance().getLogbuf("ec_worker")
    self._running = False
    self._rtcout.RTC_TRACE("ExecutionContextWorker.__init__")
    self._ref = None
    self._comps = []
    self._addedComps = []
    self._removedComps = []
    self._mutex = threading.RLock()
    self._addedMutex = threading.RLock()
    self._removedMutex = threading.RLock()
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
    self._rtcout.RTC_TRACE("~ExecutionContextWorker.__del__")
    return


  #============================================================
  # Object reference to EC
  #============================================================
  # void setECRef(RTC::ExecutionContextService_ptr ref);
  def setECRef(self, ref):
    self._ref = ref
    return


  #RTC::ExecutionContextService_ptr getECRef();
  def getECRef(self):
    return self._ref


  #============================================================
  # ExecutionContext
  #============================================================
  ##
  # @if jp
  # @brief ExecutionContext �¹Ծ��ֳ�ǧ�ؿ�
  #
  # �������� ExecutionContext �� Runnning ���֤ξ��� true ���֤���
  # Executioncontext �� Running �δ֡����� Executioncontext �˻��ä�
  # �Ƥ������ƤΥ����ƥ���RT����ݡ��ͥ�Ȥ���ExecutionContext �μ�
  # �Լ���˱����Ƽ¹Ԥ���롣
  #
  # @return ���ֳ�ǧ�ؿ�(ư����:true�������:false)
  #
  # @else
  #
  # @brief Check for ExecutionContext running state
  #
  # This operation shall return true if the context is in the
  # Running state.  While the context is Running, all Active RTCs
  # participating in the context shall be executed according to the
  # context��s execution kind.
  #
  # @return Check state function (Running:true��Stopping:false)
  #
  # @endif
  # bool isRunning(void);
  def isRunning(self):
    self._rtcout.RTC_TRACE("isRunning()")
    return self._running


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ򳫻�
  #
  # ExecutionContext �μ¹Ծ��֤� Runnning �Ȥ��뤿��Υꥯ�����Ȥ�
  # ȯ�Ԥ��롣ExecutionContext �ξ��֤����ܤ����
  # ComponentAction::on_startup ���ƤӽФ���롣���ä��Ƥ���RT����ݡ�
  # �ͥ�Ȥ�������������ޤ� ExecutionContext �򳫻Ϥ��뤳�ȤϤǤ�
  # �ʤ���ExecutionContext ��ʣ���󳫻�/��ߤ򷫤��֤����Ȥ��Ǥ��롣
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Start the ExecutionContext
  #
  # Request that the context enter the Running state.  Once the
  # state transition occurs, the ComponentAction::on_startup
  # operation will be invoked.  An execution context may not be
  # started until the RT-Components that participate in it have
  # been initialized.  An execution context may be started and
  # stopped multiple times.
  #
  # @return The return code of ReturnCode_t type
  #
  # @endif
  # RTC::ReturnCode_t start(void);
  def start(self):
    self._rtcout.RTC_TRACE("start()")
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    if self._running:
      del guard
      self._rtcout.RTC_WARN("ExecutionContext is already running.")
      return RTC.PRECONDITION_NOT_MET

    # invoke ComponentAction::on_startup for each comps.
    for comp in self._comps:
      comp.onStartup()

    self._rtcout.RTC_DEBUG("%d components started.", len(self._comps))
    # change EC thread state
    self._running = True
    del guard
    return RTC.RTC_OK


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ����
  #
  # ExecutionContext �ξ��֤� Stopped �Ȥ��뤿��Υꥯ�����Ȥ�ȯ�Ԥ�
  # �롣���ܤ�ȯ���������ϡ�ComponentAction::on_shutdown ���Ƥӽ�
  # ����롣���ä��Ƥ���RT����ݡ��ͥ�Ȥ���λ��������
  # ExecutionContext ����ߤ���ɬ�פ����롣ExecutionContext ��ʣ����
  # ����/��ߤ򷫤��֤����Ȥ��Ǥ��롣
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Stop the ExecutionContext
  #
  # Request that the context enter the Stopped state.  Once the
  # transition occurs, the ComponentAction::on_shutdown operation
  # will be invoked.  An execution context must be stopped before
  # the RT components that participate in it are finalized.  An
  # execution context may be started and stopped multiple times.
  #
  # @return The return code of ReturnCode_t type
  #
  # @endif
  # RTC::ReturnCode_t stop(void);
  def stop(self):
    self._rtcout.RTC_TRACE("stop()")
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    if not self._running:
      del guard
      self._rtcout.RTC_WARN("ExecutionContext is already stopped.")
      return RTC.PRECONDITION_NOT_MET

    # stop thread
    self._running = False

    # invoke on_shutdown for each comps.
    for comp in self._comps:
      comp.onShutdown()
      
    del guard
    return RTC.RTC_OK


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ򥢥��ƥ��ֲ�����
  #
  # Inactive ���֤ˤ���RT����ݡ��ͥ�Ȥ�Active �����ܤ����������ƥ�
  # �ֲ����롣�������ƤФ줿��̡�on_activate ���ƤӽФ���롣��
  # �ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ�
  # BAD_PARAMETER ���֤���롣���ꤷ��RT����ݡ��ͥ�Ȥξ��֤�
  # Inactive �ʳ��ξ��ϡ�PRECONDITION_NOT_MET ���֤���롣
  #
  # @param comp �����ƥ��ֲ��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Activate an RT-component
  #
  # The given participant RTC is Inactive and is therefore not
  # being invoked according to the execution context��s execution
  # kind. This operation shall cause the RTC to transition to the
  # Active state such that it may subsequently be invoked in this
  # execution context.  The callback on_activate shall be called as
  # a result of calling this operation. This operation shall not
  # return until the callback has returned, and shall result in an
  # error if the callback does.
  #
  # @param comp The target RT-Component for activation
  #
  # @return The return code of ReturnCode_t type
  #
  # @endif
  # RTC::ReturnCode_t activateComponent(RTC::LightweightRTObject_ptr comp,
  #                                     RTObjectStateMachine*& rtobj);
  def activateComponent(self, comp, rtobj):
    self._rtcout.RTC_TRACE("activateComponent()")
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    obj_ = self.findComponent(comp)
    if not obj_:
      del guard
      self._rtcout.RTC_ERROR("Given RTC is not participant of this EC.")
      return RTC.BAD_PARAMETER

    self._rtcout.RTC_DEBUG("Component found in the EC.")
    if not obj_.isCurrentState(RTC.INACTIVE_STATE):
      del guard
      self._rtcout.RTC_ERROR("State of the RTC is not INACTIVE_STATE.")
      return RTC.PRECONDITION_NOT_MET

    self._rtcout.RTC_DEBUG("Component is in INACTIVE state. Going to ACTIVE state.")
    obj_.goTo(RTC.ACTIVE_STATE)
    rtobj[0] = obj_
    del guard
    self._rtcout.RTC_DEBUG("activateComponent() done.")
    return RTC.RTC_OK


  # RTC::ReturnCode_t waitActivateComplete(RTObjectStateMachine*& rtobj,
  #                                        coil::TimeValue timeout = 1.0,
  #                                        long int cycle = 1000);
  def waitActivateComplete(self, rtobj, timeout = 1.0, cycle = 1000):
    pass

  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ�����
  #
  # Inactive ���֤ˤ���RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ�����Inactive
  # �����ܤ����롣�������ƤФ줿��̡�on_deactivate ���ƤӽФ���
  # �롣���ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ�
  # BAD_PARAMETER ���֤���롣���ꤷ��RT����ݡ��ͥ�Ȥξ��֤�
  # Active �ʳ��ξ��ϡ�PRECONDITION_NOT_MET ���֤���롣
  #
  # @param comp �󥢥��ƥ��ֲ��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Deactivate an RT-component
  #
  # The given RTC is Active in the execution context. Cause it to
  # transition to the Inactive state such that it will not be
  # subsequently invoked from the context unless and until it is
  # activated again.  The callback on_deactivate shall be called as
  # a result of calling this operation. This operation shall not
  # return until the callback has returned, and shall result in an
  # error if the callback does.
  #
  # @param comp The target RT-Component for deactivate
  #
  # @return The return code of ReturnCode_t type
  #
  # @endif
  # RTC::ReturnCode_t deactivateComponent(RTC::LightweightRTObject_ptr comp,
  #                                       RTObjectStateMachine*& rtobj);
  def deactivateComponent(self, comp, rtobj):
    self._rtcout.RTC_TRACE("deactivateComponent()")
    guard = OpenRTM_aist.ScopedLock(self._mutex)

    rtobj[0] = self.findComponent(comp)
    if not rtobj[0]: 
      del guard
      self._rtcout.RTC_ERROR("Given RTC is not participant of this EC.")
      return RTC.BAD_PARAMETER

    if not rtobj[0].isCurrentState(RTC.ACTIVE_STATE):
      del guard
      self._rtcout.RTC_ERROR("State of the RTC is not ACTIVE_STATE.")
      return RTC.PRECONDITION_NOT_MET

    rtobj[0].goTo(RTC.INACTIVE_STATE)
    del guard
    return RTC.RTC_OK


  # RTC::ReturnCode_t waitDeactivateComplete(RTObjectStateMachine*& rtobj,
  #                                            coil::TimeValue timeout = 1.0,
  #                                            long int cycle = 1000);
  def waitDeactivateComplete(self, rtobj, timeout = 1.0, cycle = 1000):
    pass


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ�ꥻ�åȤ���
  #
  # Error ���֤�RT����ݡ��ͥ�Ȥ��������ߤ롣�������ƤФ줿��
  # �̡�on_reset ���ƤӽФ���롣���ꤷ��RT����ݡ��ͥ�Ȥ����üԥ�
  # ���Ȥ˴ޤޤ�ʤ����ϡ�BAD_PARAMETER ���֤���롣���ꤷ��RT����
  # �ݡ��ͥ�Ȥξ��֤� Error �ʳ��ξ��ϡ�PRECONDITION_NOT_MET ����
  # ����롣
  #
  # @param comp �ꥻ�å��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Reset the RT-component
  #
  # Attempt to recover the RTC when it is in Error.  The
  # ComponentAction::on_reset callback shall be invoked. This
  # operation shall not return until the callback has returned, and
  # shall result in an error if the callback does. If possible, the
  # RTC developer should implement that callback such that the RTC
  # may be returned to a valid state.
  #
  # @param comp The target RT-Component for reset
  #
  # @return The return code of ReturnCode_t type
  #
  # @endif
  # RTC::ReturnCode_t resetComponent(RTC::LightweightRTObject_ptr com,
  #                                  RTObjectStateMachine*& rtobj);
  def resetComponent(self, comp, rtobj):
    self._rtcout.RTC_TRACE("resetComponent()")
    guard = OpenRTM_aist.ScopedLock(self._mutex)

    rtobj[0] = self.findComponent(comp)
    if not rtobj[0]:
      del guard
      self._rtcout.RTC_ERROR("Given RTC is not participant of this EC.")
      return RTC.BAD_PARAMETER

    if not rtobj[0].isCurrentState(RTC.ERROR_STATE):
      del guard
      self._rtcout.RTC_ERROR("State of the RTC is not ERROR_STATE.")
      return RTC.PRECONDITION_NOT_MET

    rtobj[0].goTo(RTC.INACTIVE_STATE)
    del guard
    return RTC.RTC_OK


  # RTC::ReturnCode_t waitResetComplete(RTObjectStateMachine*& rtobj,
  #                                     coil::TimeValue timeout = 1.0,
  #                                     long int cycle = 1000);
  def waitResetComplete(self, rtobj, timeout = 1.0, cycle = 1000):
    pass


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥξ��֤��������
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥξ���(LifeCycleState)��������롣���ꤷ
  # ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ�
  # UNKNOWN_STATE ���֤���롣
  #
  # @param comp ���ּ����о�RT����ݡ��ͥ��
  #
  # @return ���ߤξ���(LifeCycleState)
  #
  # @else
  #
  # @brief Get RT-component's state
  #
  # This operation shall report the LifeCycleState of the given
  # participant RTC.  UNKNOWN_STATE will be returned, if the given
  # RT-Component is not inclued in the participant list.
  #
  # @param comp The target RT-Component to get the state
  #
  # @return The current state of the target RT-Component(LifeCycleState)
  #
  # @endif
  # RTC::LifeCycleState getComponentState(RTC::LightweightRTObject_ptr comp);
  def getComponentState(self, comp):
    self._rtcout.RTC_TRACE("getComponentState()")
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    rtobj_ = self.findComponent(comp)
    if not rtobj_:
      del guard
      self._rtcout.RTC_WARN("Given RTC is not participant of this EC.")
      return RTC.CREATED_STATE

    state_ = rtobj_.getState()
    self._rtcout.RTC_DEBUG("getComponentState() = %s done", self.getStateString(state_))
    return state_


  # const char* getStateString(RTC::LifeCycleState state)
  def getStateString(self, state):
    st = ["CREATED_STATE",
          "INACTIVE_STATE",
          "ACTIVE_STATE",
          "ERROR_STATE"]

    f = lambda x: st[x._v] if x >= RTC.CREATED_STATE and x <= RTC.ERROR_STATE else ""
    return f(state)

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
      self._rtcout.RTC_ERROR("nil reference is given.")
      return RTC.BAD_PARAMETER

    try:
      guard = OpenRTM_aist.ScopedLock(self._addedMutex)
      ec_ = self.getECRef()
      id_ = comp.attach_context(ec_)
      self._addedComps.append(OpenRTM_aist.RTObjectStateMachine(id_, comp))
      del guard
    except:
      del guard
      self._rtcout.RTC_ERROR("addComponent() failed.")
      return RTC.RTC_ERROR

    self._rtcout.RTC_DEBUG("addComponent() succeeded.")
    return RTC.RTC_OK


  ##
  # @if jp
  # @brief ����ݡ��ͥ�Ȥ�Х���ɤ��롣
  #
  # ����ݡ��ͥ�Ȥ�Х���ɤ��롣
  #
  # @param rtc RT����ݡ��ͥ��
  # @return ReturnCode_t ���Υ꥿���󥳡���
  # @else
  # @brief Bind the component.
  #
  # Bind the component.
  #
  # @param rtc RT-Component's instances
  # @return The return code of ReturnCode_t type
  # @endif
  # RTC::ReturnCode_t bindComponent(RTC::RTObject_impl* rtc);
  def bindComponent(self, rtc):
    self._rtcout.RTC_TRACE("bindComponent()")
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    if not rtc:
      del guard
      self._rtcout.RTC_ERROR("NULL pointer is given.")
      return RTC.BAD_PARAMETER

    ec_ = self.getECRef()
    id_ = rtc.bindContext(ec_)
    if id_ < 0 or id_ > OpenRTM_aist.ECOTHER_OFFSET:
      # id should be owned context id < ECOTHER_OFFSET
      del guard
      self._rtcout.RTC_ERROR("bindContext returns invalid id: %d", id_)
      return RTC.RTC_ERROR

    self._rtcout.RTC_DEBUG("bindContext returns id = %d", id_)
    
    # rtc is owner of this EC
    comp_ = rtc.getObjRef()
    #    RTObjectStateMachine o(id, comp);
    self._comps.append(OpenRTM_aist.RTObjectStateMachine(id_, comp_))
    del guard
    self._rtcout.RTC_DEBUG("bindComponent() succeeded.")
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
      self._rtcout.RTC_ERROR("nil reference is given.")
      return RTC.BAD_PARAMETER


    guard = OpenRTM_aist.ScopedLock(self._mutex)
    rtobj_ = self.findComponent(comp)
    del guard

    if not rtobj_:
      self._rtcout.RTC_ERROR("no RTC found in this context.")
      return  RTC.BAD_PARAMETER

    guard = OpenRTM_aist.ScopedLock(self._removedMutex)
    self._removedComps.append(rtobj_)
    del guard
    return RTC.RTC_OK


  # RTObjectStateMachine* findComponent(RTC::LightweightRTObject_ptr comp);
  def findComponent(self, comp):
    for comp_ in self._comps:
      if comp_.isEquivalent(comp):
        return comp_

    return None


  # bool isAllCurrentState(RTC::LifeCycleState state);
  def isAllCurrentState(self, state):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    for comp in self._comps:
      if not comp.isCurrentState(state):
        del guard
        return False

    del guard
    return True


  # bool isAllNextState(RTC::LifeCycleState state);
  def isAllNextState(self, state):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    for comp in self._comps:
      if not comp.isNextState(state):
        del guard
        return False

    del guard
    return True


  # bool isOneOfCurrentState(RTC::LifeCycleState state);
  def isOneOfCurrentState(self, state):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    for comp in self._comps:
      if comp.isCurrentState(state):
        del guard
        return True
    
    del guard
    return False


  # bool isOneOfNextState(RTC::LifeCycleState state);
  def isOneOfNextState(self, state):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    for comp in self._comps:
      if comp.isNextState(state):
        del guard
        return True

    del guard
    return False


  # void invokeWorker();
  def invokeWorker(self):
    self._rtcout.RTC_PARANOID("invokeWorker()")
    # m_comps never changes its size here
    len_ = len(self._comps)
    
    for i in range(len_):
      self._comps[i].workerPreDo()

    for i in range(len_):
      self._comps[i].workerDo()

    for i in range(len_):
      self._comps[i].workerPostDo()

    self.updateComponentList()
    return


  # void invokeWorkerPreDo();
  def invokeWorkerPreDo(self):
    self._rtcout.RTC_PARANOID("invokeWorkerPreDo()")
    # m_comps never changes its size here
    for comp in self._comps:
      comp.workerPreDo()
    return

  # void invokeWorkerDo();
  def invokeWorkerDo(self):
    self._rtcout.RTC_PARANOID("invokeWorkerDo()")
    # m_comps never changes its size here
    for comp in self._comps:
      comp.workerDo()
    return

  # void invokeWorkerPostDo();
  def invokeWorkerPostDo(self):
    self._rtcout.RTC_PARANOID("invokeWorkerPostDo()")
    # m_comps never changes its size here
    for comp in self._comps:
      comp.workerPostDo()
    # m_comps might be changed here
    self.updateComponentList()
    return
    
  # void updateComponentList();
  def updateComponentList(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    # adding component
    guard_added = OpenRTM_aist.ScopedLock(self._addedMutex)
    for comp in self._addedComps:
      self._comps.append(comp)
      self._rtcout.RTC_TRACE("Component added.")

    self._addedComps = []
    del guard_added

    # removing component
    guard_removed = OpenRTM_aist.ScopedLock(self._removedMutex)
    for comp in self._removedComps:
      lwrtobj_ = comp.getRTObject()
      lwrtobj_.detach_context(comp.getExecutionContextHandle())
      idx_ = -1
      try:
        idx_ = self._comps.index(comp)
      except:
        idx_ = -1

      if idx_ >= 0:
        del self._comps[idx_]
        self._rtcout.RTC_TRACE("Component deleted.")

    self._removedComps = []
    return
