#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file PeriodicExecutionContext.py
# @brief PeriodicExecutionContext class
# @date $Date: 2007/08/29$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2006-2008
#     Task-intelligence Research Group,
#     Intelligent Systems Research Institute,
#     National Institute of
#         Advanced Industrial Science and Technology (AIST), Japan
#     All rights reserved.

import sys
import copy
import threading
import time
from omniORB import CORBA, PortableServer

import OpenRTM_aist
import OpenRTM
import RTC, RTC__POA

DEFAULT_PERIOD = 0.000001

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
# @endif
class PeriodicExecutionContext(OpenRTM_aist.ExecutionContextBase,
                               RTC__POA.ExecutionContextService,
                               OpenRTM_aist.Task):
  """
  """

  ##
  # @if jp
  # @brief ���󥹥ȥ饯��
  #
  # ���󥹥ȥ饯��
  # ���ꤵ�줿�ͤ�ץ�ե���������ꤹ�롣
  #
  # @else
  # @brief Constructor
  # @endif
  def __init__(self):
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.periodic_ec")
    self._rtcout.RTC_TRACE("PeriodicExecutionContext.__init__()")
    OpenRTM_aist.ExecutionContextBase.__init__(self, "periodic_ec")
    OpenRTM_aist.Task.__init__(self)

    self._svc = False
    self._nowait = False
    self._svcmutex = threading.RLock()
    self._workerthread = self.WorkerThreadCtrl()

    global DEFAULT_PERIOD
    self.setObjRef(self._this())
    self.setKind(RTC.PERIODIC)
    self.setRate(1.0 / DEFAULT_PERIOD)
    self._rtcout.RTC_DEBUG("Actual rate: %d [sec], %d [usec]",
                           (self._profile.getPeriod().sec(), self._profile.getPeriod().usec()))    

    return


  def __del__(self, Task=OpenRTM_aist.Task):
    import OpenRTM_aist.Guard
    self._rtcout.RTC_TRACE("PeriodicExecutionContext.__del__()")
    guard = OpenRTM_aist.ScopedLock(self._svcmutex)
    self._svc = False
    del guard

    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    self._workerthread._cond.acquire()
    self._workerthread._running = True
    self._workerthread._cond.notify()
    self._workerthread._cond.release()
    del guard
    self.wait()
    Task.__del__(self)
    return


  ##
  # @if jp
  # @brief ����ݡ��ͥ�ȤΥ����ƥ��ӥƥ�����åɴؿ�
  #
  # ����ݡ��ͥ�Ȥ����������ƥ��ӥƥ�����åɤμ¹Դؿ���
  # ACE_Task �����ӥ����饹�᥽�åɤΥ����С��饤�ɡ�
  #
  # @else
  #
  # @brief Create internal activity thread
  #
  # Run by a daemon thread to handle deferred processing.
  # ACE_Task class method override.
  #
  # @endif
  def svc(self):
    self._rtcout.RTC_TRACE("svc()")
    count_ = 0
    
    while self.threadRunning():
      OpenRTM_aist.ExecutionContextBase.invokeWorkerPreDo(self)
      # Thread will stopped when all RTCs are INACTIVE.
      # Therefore WorkerPreDo(updating state) have to be invoked
      # before stopping thread.
      guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
      while not self._workerthread._running:
        self._workerthread._cond.wait()
      del guard

      t0_ = OpenRTM_aist.Time()
      OpenRTM_aist.ExecutionContextBase.invokeWorkerDo(self)
      OpenRTM_aist.ExecutionContextBase.invokeWorkerPostDo(self)
      t1_ = OpenRTM_aist.Time()

      period_ = self.getPeriod()

      if count_ > 1000:
        exctm_ = (t1_ - t0_).getTime().toDouble()
        slptm_ = period_.toDouble() - exctm_
        self._rtcout.RTC_PARANOID("Period:    %f [s]", period_.toDouble())
        self._rtcout.RTC_PARANOID("Execution: %f [s]", exctm_)
        self._rtcout.RTC_PARANOID("Sleep:     %f [s]", slptm_)


      t2_ = OpenRTM_aist.Time()

      if not self._nowait and period_.toDouble() > ((t1_ - t0_).getTime().toDouble()):
        if count_ > 1000:
          self._rtcout.RTC_PARANOID("sleeping...")
        slptm_ = period_.toDouble() - (t1_ - t0_).getTime().toDouble()
        time.sleep(slptm_)

      if count_ > 1000:
        t3_ = OpenRTM_aist.Time()
        self._rtcout.RTC_PARANOID("Slept:     %f [s]", (t3_ - t2_).getTime().toDouble())
        count_ = 0
      count_ += 1

    self._rtcout.RTC_DEBUG("Thread terminated.")
    return 0


  ##
  # @if jp
  # @brief ExecutionContext�ѥ����ƥ��ӥƥ�����åɤ���������
  # @else
  # @brief Generate internal activity thread for ExecutionContext
  # @endif
  #
  # int PeriodicExecutionContext::open(void *args)
  def open(self, *args):
    self._rtcout.RTC_TRACE("open()")
    self.activate()
    return 0


  ##
  # @if jp
  # @brief ExecutionContext �ѤΥ���åɼ¹Դؿ�
  #
  # ExecutionContext �ѤΥ���åɽ�λ���˸ƤФ�롣
  # ����ݡ��ͥ�ȥ��֥������Ȥ��󥢥��ƥ��ֲ����ޥ͡�����ؤ����Τ�Ԥ���
  # ����� ACE_Task �����ӥ����饹�᥽�åɤΥ����С��饤�ɡ�
  #
  # @param self
  # @param flags ��λ�����ե饰
  #
  # @return ��λ�������
  #
  # @else
  #
  # @brief Close activity thread
  #
  # close() method is called when activity thread svc() is returned.
  # This method deactivate this object and notify it to manager.
  # ACE_Task class method override.
  #
  # @endif
  def close(self, flags):
    self._rtcout.RTC_TRACE("close()")
    return 0


  ##
  # @if jp
  # @brief ExecutionContext �¹Ծ��ֳ�ǧ�ؿ�
  #
  # �������� ExecutionContext �� Runnning ���֤ξ��� true ���֤���
  # Executioncontext �� Running �δ֡����� Executioncontext �˻��ä��Ƥ���
  # ���ƤΥ����ƥ���RT����ݡ��ͥ�Ȥ��� ExecutionContext �μ¹Լ���˱�����
  # �¹Ԥ���롣
  #
  # @param self
  #
  # @return ���ֳ�ǧ�ؿ�(ư����:true�������:false)
  #
  # @else
  #
  # @brief Check for ExecutionContext running state
  #
  # This operation shall return true if the context is in the Running state.
  # While the context is Running, all Active RTCs participating
  # in the context shall be executed according to the context��s execution
  # kind.
  #
  # @endif
  def is_running(self):
    self._rtcout.RTC_TRACE("is_running()")
    return OpenRTM_aist.ExecutionContextBase.isRunning(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ򳫻�
  #
  # ExecutionContext �μ¹Ծ��֤� Runnning �Ȥ��뤿��Υꥯ�����Ȥ�ȯ�Ԥ��롣
  # ExecutionContext �ξ��֤����ܤ���� ComponentAction::on_startup ��
  # �ƤӽФ���롣
  # ���ä��Ƥ���RT����ݡ��ͥ�Ȥ�������������ޤ� ExecutionContext �򳫻�
  # ���뤳�ȤϤǤ��ʤ���
  # ExecutionContext ��ʣ���󳫻�/��ߤ򷫤��֤����Ȥ��Ǥ��롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Start ExecutionContext
  #
  # Request that the context enter the Running state. 
  # Once the state transition occurs, the ComponentAction::on_startup 
  # operation will be invoked.
  # An execution context may not be started until the RT components that
  # participate in it have been initialized.
  # An execution context may be started and stopped multiple times.
  #
  # @endif
  def start(self):
    return OpenRTM_aist.ExecutionContextBase.start(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ����
  #
  # ExecutionContext �ξ��֤� Stopped �Ȥ��뤿��Υꥯ�����Ȥ�ȯ�Ԥ��롣
  # ���ܤ�ȯ���������ϡ� ComponentAction::on_shutdown ���ƤӽФ���롣
  # ���ä��Ƥ���RT����ݡ��ͥ�Ȥ���λ�������� ExecutionContext ����ߤ���
  # ɬ�פ����롣
  # ExecutionContext ��ʣ���󳫻�/��ߤ򷫤��֤����Ȥ��Ǥ��롣
  #
  # @param self
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Stop ExecutionContext
  #
  # Request that the context enter the Stopped state. 
  # Once the transition occurs, the ComponentAction::on_shutdown operation
  # will be invoked.
  # An execution context must be stopped before the RT components that
  # participate in it are finalized.
  # An execution context may be started and stopped multiple times.
  #
  # @endif
  def stop(self):
    return OpenRTM_aist.ExecutionContextBase.stop(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)���������
  #
  # Active ���֤ˤ�RT����ݡ��ͥ�Ȥ��¹Ԥ�������(ñ��:Hz)��������롣
  #
  # @param self
  #
  # @return ��������(ñ��:Hz)
  #
  # @else
  #
  # @brief Get ExecutionRate
  #
  # This operation shall return the rate (in hertz) at which its Active
  # participating RTCs are being invoked.
  #
  # @endif
  def get_rate(self):
    return OpenRTM_aist.ExecutionContextBase.getRate(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)�����ꤹ��
  #
  # Active ���֤ˤ�RT����ݡ��ͥ�Ȥ��¹Ԥ�������(ñ��:Hz)�����ꤹ�롣
  # �¹Լ������ѹ��ϡ� DataFlowComponentAction �� on_rate_changed �ˤ�ä�
  # ��RT����ݡ��ͥ�Ȥ���ã����롣
  #
  # @param self
  # @param rate ��������(ñ��:Hz)
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Set ExecutionRate
  #
  # This operation shall set the rate (in hertz) at which this context��s 
  # Active participating RTCs are being called.
  # If the execution kind of the context is PERIODIC, a rate change shall
  # result in the invocation of on_rate_changed on any RTCs realizing
  # DataFlowComponentAction that are registered with any RTCs participating
  # in the context.
  #
  # @endif
  def set_rate(self, rate):
    return OpenRTM_aist.ExecutionContextBase.setRate(self, rate)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ򥢥��ƥ��ֲ�����
  #
  # Inactive ���֤ˤ���RT����ݡ��ͥ�Ȥ�Active �����ܤ����������ƥ��ֲ����롣
  # �������ƤФ줿��̡� on_activate ���ƤӽФ���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ� BAD_PARAMETER 
  # ���֤���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥξ��֤� Inactive �ʳ��ξ��ϡ�
  #  PRECONDITION_NOT_MET ���֤���롣
  #
  # @param self
  # @param comp �����ƥ��ֲ��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Activate a RT-component
  #
  # The given participant RTC is Inactive and is therefore not being invoked
  # according to the execution context��s execution kind. This operation
  # shall cause the RTC to transition to the Active state such that it may
  # subsequently be invoked in this execution context.
  # The callback on_activate shall be called as a result of calling this
  # operation. This operation shall not return until the callback has
  # returned, and shall result in an error if the callback does.
  #
  # @endif
  def activate_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.activateComponent(self, comp)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ�����
  #
  # Inactive ���֤ˤ���RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ�����
  # Inactive �����ܤ����롣
  # �������ƤФ줿��̡� on_deactivate ���ƤӽФ���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ� BAD_PARAMETER 
  # ���֤���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥξ��֤� Active �ʳ��ξ��ϡ�
  # PRECONDITION_NOT_MET ���֤���롣
  #
  # @param self
  # @param comp �󥢥��ƥ��ֲ��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Deactivate a RT-component
  #
  # The given RTC is Active in the execution context. Cause it to transition 
  # to the Inactive state such that it will not be subsequently invoked from
  # the context unless and until it is activated again.
  # The callback on_deactivate shall be called as a result of calling this
  # operation. This operation shall not return until the callback has 
  # returned, and shall result in an error if the callback does.
  #
  # @endif
  def deactivate_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.deactivateComponent(self, comp)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ�ꥻ�åȤ���
  #
  # Error ���֤�RT����ݡ��ͥ�Ȥ��������ߤ롣
  # �������ƤФ줿��̡� on_reset ���ƤӽФ���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ� BAD_PARAMETER
  # ���֤���롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥξ��֤� Error �ʳ��ξ��ϡ� PRECONDITION_NOT_MET
  # ���֤���롣
  #
  # @param self
  # @param comp �ꥻ�å��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Reset a RT-component
  #
  # Attempt to recover the RTC when it is in Error.
  # The ComponentAction::on_reset callback shall be invoked. This operation
  # shall not return until the callback has returned, and shall result in an
  # error if the callback does. If possible, the RTC developer should
  # implement that callback such that the RTC may be returned to a valid
  # state.
  #
  # @endif
  def reset_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.resetComponent(self, comp)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥξ��֤��������
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥξ���(LifeCycleState)��������롣
  # ���ꤷ��RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ˴ޤޤ�ʤ����ϡ� CREATED_STATE 
  # ���֤���롣
  #
  # @param self
  # @param comp ���ּ����о�RT����ݡ��ͥ��
  #
  # @return ���ߤξ���(LifeCycleState)
  #
  # @else
  #
  # @brief Get RT-component's state
  #
  # This operation shall report the LifeCycleState of the given participant
  # RTC.
  #
  # @endif
  def get_component_state(self, comp):
    return OpenRTM_aist.ExecutionContextBase.getComponentState(self, comp)


  ##
  # @if jp
  # @brief ExecutionKind ���������
  #
  # �� ExecutionContext �� ExecutionKind ���������
  #
  # @param self
  #
  # @return ExecutionKind
  #
  # @else
  #
  # @brief Get the ExecutionKind
  #
  # This operation shall report the execution kind of the execution context.
  #
  # @endif
  def get_kind(self):
    return OpenRTM_aist.ExecutionContextBase.getKind(self)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��ɲä���
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ��ɲä��롣
  # �ɲä��줿RT����ݡ��ͥ�Ȥ� attach_context ���ƤФ졢Inactive ���֤�����
  # ���롣
  # ���ꤵ�줿RT����ݡ��ͥ�Ȥ�null�ξ��ϡ�BAD_PARAMETER ���֤���롣
  # ���ꤵ�줿RT����ݡ��ͥ�Ȥ� DataFlowComponent �ʳ��ξ��ϡ�
  # BAD_PARAMETER ���֤���롣
  #
  # @param self
  # @param comp �ɲ��о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Add a RT-component
  #
  # The operation causes the given RTC to begin participating in the
  # execution context.
  # The newly added RTC will receive a call to 
  # LightweightRTComponent::attach_context and then enter the Inactive state.
  #
  # @endif
  def add_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.addComponent(self, comp)


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ���������
  #
  # ���ꤷ��RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ��������롣
  # ������줿RT����ݡ��ͥ�Ȥ� detach_context ���ƤФ�롣
  # ���ꤵ�줿RT����ݡ��ͥ�Ȥ����üԥꥹ�Ȥ���Ͽ����Ƥ��ʤ����ϡ�
  # BAD_PARAMETER ���֤���롣
  #
  # @param self
  # @param comp ����о�RT����ݡ��ͥ��
  #
  # @return ReturnCode_t ���Υ꥿���󥳡���
  #
  # @else
  #
  # @brief Remove the RT-component from participant list
  #
  # This operation causes a participant RTC to stop participating in the
  # execution context.
  # The removed RTC will receive a call to
  # LightweightRTComponent::detach_context.
  #
  # @endif
  def remove_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.removeComponent(self, comp)


  ##
  # @if jp
  # @brief ExecutionContextProfile ���������
  #
  # �� ExecutionContext �Υץ�ե������������롣
  #
  # @param self
  #
  # @return ExecutionContextProfile
  #
  # @else
  #
  # @brief Get the ExecutionContextProfile
  #
  # This operation provides a profile ��descriptor�� for the execution 
  # context.
  #
  # @endif
  def get_profile(self):
    return OpenRTM_aist.ExecutionContextBase.getProfile(self)


  # virtual RTC::ReturnCode_t onStarted();
  def onStarted(self):
    # change EC thread state
    guard = OpenRTM_aist.ScopedLock(self._svcmutex)
    if not self._svc:
      self._svc = True
      self.open(0)
    del guard

    if self.isAllNextState(RTC.INACTIVE_STATE):
      guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
      self._workerthread._running = False
      del guard
    else:
      guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
      self._workerthread._running = True
      self._workerthread._cond.acquire()
      self._workerthread._cond.notify()
      self._workerthread._cond.release()
      del guard
    return RTC.RTC_OK


  # virtual RTC::ReturnCode_t onStopping();
  def onStopping(self):
    # stop thread
    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    self._workerthread._running = False
    return RTC.RTC_OK


  def onStopped(self):
    guard = OpenRTM_aist.ScopedLock(self._svcmutex)
    self._svc = False
    del guard

    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    self._workerthread._cond.acquire()
    self._workerthread._running = True
    self._workerthread._cond.notify()
    self._workerthread._cond.release()
    del guard
    self.wait()
    return RTC.RTC_OK


  # virtual RTC::ReturnCode_t
  # onWaitingActivated(RTC_impl::RTObjectStateMachine* comp, long int count);
  def onWaitingActivated(self, comp, count):
    self._rtcout.RTC_TRACE("onWaitingActivated(count = %d)", count)
    self._rtcout.RTC_PARANOID("curr: %s, next: %s",
                              (self.getStateString(comp.getStates().curr),
                               self.getStateString(comp.getStates().next)))
    # Now comp's next state must be ACTIVE state
    # If worker thread is stopped, restart worker thread.
    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    if self._workerthread._running == False:
      self._workerthread._running = True
      self._workerthread._cond.acquire()
      self._workerthread._cond.notify()
      self._workerthread._cond.release()
    del guard
    return RTC.RTC_OK


  # virtual RTC::ReturnCode_t
  # onActivated(RTC_impl::RTObjectStateMachine* comp, long int count);
  def onActivated(self, comp, count):
    self._rtcout.RTC_TRACE("onActivated(count = %d)", count)
    self._rtcout.RTC_PARANOID("curr: %s, next: %s",
                              (self.getStateString(comp.getStates().curr),
                               self.getStateString(comp.getStates().next)))
    # count = -1; Asynch mode. Since onWaitingActivated is not
    # called, onActivated() have to send restart singnal to worker
    # thread.
    # count > 0: Synch mode.

    # Now comp's next state must be ACTIVE state
    # If worker thread is stopped, restart worker thread.
    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    if self._workerthread._running == False:
      self._workerthread._running = True
      self._workerthread._cond.acquire()
      self._workerthread._cond.notify()
      self._workerthread._cond.release()
    del guard
    return RTC.RTC_OK


  # virtual RTC::ReturnCode_t
  # onWaitingDeactivated(RTC_impl::RTObjectStateMachine* comp, long int count);
  def onWaitingDeactivated(self, comp, count):
    self._rtcout.RTC_TRACE("onWaitingDeactivated(count = %d)", count)
    self._rtcout.RTC_PARANOID("curr: %s, next: %s",
                              (self.getStateString(comp.getStates().curr),
                               self.getStateString(comp.getStates().next)))
    if self.isAllNextState(RTC.INACTIVE_STATE):
      guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
      if self._workerthread._running == True:
        self._workerthread._running = False
        self._rtcout.RTC_TRACE("All RTCs are INACTIVE. Stopping worker thread.")
      del guard

    return RTC.RTC_OK


  # virtual RTC::ReturnCode_t 
  # onDeactivated(RTC_impl::RTObjectStateMachine* comp, long int count);
  def onDeactivated(self, comp, count):
    self._rtcout.RTC_TRACE("onDeactivated(count = %d)", count)
    self._rtcout.RTC_PARANOID("curr: %s, next: %s",
                              (self.getStateString(comp.getStates().curr),
                               self.getStateString(comp.getStates().next)))
    if self.isAllNextState(RTC.INACTIVE_STATE):
      guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
      if self._workerthread._running == True:
        self._workerthread._running = False
        self._rtcout.RTC_TRACE("All RTCs are INACTIVE. Stopping worker thread.")
      del guard

    return RTC.RTC_OK


  # virtual RTC::ReturnCode_t
  # onWaitingReset(RTC_impl::RTObjectStateMachine* comp, long int count);
  def onWaitingReset(self, comp, count):
    self._rtcout.RTC_TRACE("onWaitingReset(count = %d)", count)
    self._rtcout.RTC_PARANOID("curr: %s, next: %s",
                              (self.getStateString(comp.getStates().curr),
                               self.getStateString(comp.getStates().next)))
    if self.isAllNextState(RTC.INACTIVE_STATE):
      guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
      if self._workerthread._running == True:
        self._workerthread._running = False
        self._rtcout.RTC_TRACE("All RTCs are INACTIVE. Stopping worker thread.")
      del guard

    return RTC.RTC_OK


  # virtual RTC::ReturnCode_t 
  # onReset(RTC_impl::RTObjectStateMachine* comp, long int count);
  def onReset(self, comp, count):
    self._rtcout.RTC_TRACE("onReset(count = %d)", count)
    self._rtcout.RTC_PARANOID("curr: %s, next: %s",
                              (self.getStateString(comp.getStates().curr),
                               self.getStateString(comp.getStates().next)))
    if self.isAllNextState(RTC.INACTIVE_STATE):
      guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
      if self._workerthread._running == True:
        self._workerthread._running = False
        self._rtcout.RTC_TRACE("All RTCs are INACTIVE. Stopping worker thread.")
      del guard

    return RTC.RTC_OK
    return

  # bool threadRunning()
  def threadRunning(self):
    guard = OpenRTM_aist.ScopedLock(self._svcmutex)
    return self._svc


  ##
  # @if jp
  # @class WorkerThreadCtrl
  # @brief worker �Ѿ����ѿ����饹
  #
  # @else
  # @class WorkerThreadCtrl
  # @brief Condition variable class for worker
  # @endif
  class WorkerThreadCtrl:
    
    ##
    # @if jp
    # @brief ���󥹥ȥ饯��
    #
    # ���󥹥ȥ饯��
    #
    # @param self
    #
    # @else
    # @brief Constructor
    # @endif
    def __init__(self):
      self._mutex = threading.RLock()
      self._cond = threading.Condition(self._mutex)
      self._running = False

##
# @if jp
# @brief ExecutionContext ����������
#
# ExecutionContext ��ư�ѥե����ȥ����Ͽ���롣
#
# @param manager �ޥ͡����㥪�֥�������
#
# @else
#
# @endif
def PeriodicExecutionContextInit(manager):
  OpenRTM_aist.ExecutionContextFactory.instance().addFactory("PeriodicExecutionContext",
                                                             OpenRTM_aist.PeriodicExecutionContext,
                                                             OpenRTM_aist.ECDelete)
  return
