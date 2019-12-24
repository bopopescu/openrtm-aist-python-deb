#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ExtTrigExecutionContext.py
# @brief ExtTrigExecutionContext class
# @date $Date: 2007/09/06$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2007-2008
#    Task-intelligence Research Group,
#    Intelligent Systems Research Institute,
#    National Institute of
#        Advanced Industrial Science and Technology (AIST), Japan
#    All rights reserved.



import threading
import time

import OpenRTM_aist
import OpenRTM, OpenRTM__POA, RTC, RTC__POA


##
# @if jp
# @class ExtTrigExecutionContext
# @brief ���ƥå׼¹Ԥ���ǽ�� ExecutionContext ���饹
#
# ��������μ¹Ԥ���ǽ��Periodic Sampled Data Processing(�����¹���)
# ExecutionContext���饹��
# ��������Υ᥽�åɸƤӤ����ˤ�äƻ��֤򣱼����ŤĿʤ�뤳�Ȥ��Ǥ��롣
#
# @since 0.4.0
#
# @else
# @class ExtTrigExecutionContext
# @endif
class ExtTrigExecutionContext(OpenRTM_aist.ExecutionContextBase,
                              OpenRTM__POA.ExtTrigExecutionContextService,
                              OpenRTM_aist.Task):
  """
  """

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
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("rtobject.exttrig_async_ec")
    self._rtcout.RTC_TRACE("ExtTrigExecutionContext.__init__()")
    OpenRTM_aist.ExecutionContextBase.__init__(self,"exttrig_async_ec")
    OpenRTM_aist.Task.__init__(self)

    # getting my reference
    self.setObjRef(self._this())

    # profile initialization
    self.setKind(RTC.PERIODIC)
    self.setRate(OpenRTM_aist.DEFAULT_EXECUTION_RATE)

    self._rtcout.RTC_DEBUG("Actual period: %d [sec], %d [usec]",
                           (self._profile.getPeriod().sec(), self._profile.getPeriod().usec()))
    self._svc = False
    self._workerthread = self.Worker()
    self._svcmutex = threading.RLock()
    return


  def __del__(self, Task=OpenRTM_aist.Task):
    self._rtcout.RTC_TRACE("ExtTrigExecutionContext.__del__()")
    guard = OpenRTM_aist.ScopedLock(self._svcmutex)
    self._svc = False
    del guard

    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    self._workerthread._cond.acquire()
    self._workerthread._ticked = True
    self._workerthread._cond.notify()
    self._workerthread._cond.release()
    del guard
    self.wait()
    Task.__del__(self)
    return


  ##
  # Start activity
  # ACE_Task class method over ride.
  # ------------------------------------------------------------

  ##
  # @if jp
  # @brief ExecutionContext�ѥ����ƥ��ӥƥ�����åɤ���������
  # @else
  # @brief Generate internal activity thread for ExecutionContext
  # @endif
  # int ExtTrigExecutionContext::open(void *args)
  def open(self, *args):
    self._rtcout.RTC_TRACE("open()")
    self.activate()
    return 0


  ##
  # @if jp
  # @brief �� Component �ν�����ƤӽФ���
  # @else
  # @brief Invoke each component's operation
  # @endif
  # int ExtTrigExecutionContext::svc(void)
  def svc(self):
    self._rtcout.RTC_TRACE("svc()")

    toSTR_ = lambda x: "True" if x else "False"

    while self.threadRunning():
      guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
      self._rtcout.RTC_DEBUG("Start of worker invocation. ticked = %s",
                             toSTR_(self._workerthread._ticked))

      while not self._workerthread._ticked:
        self._workerthread._cond.wait() # wait for tick
        self._rtcout.RTC_DEBUG("Thread was woken up.")

      if not self._workerthread._ticked:
        continue
      del guard

      t0_ = OpenRTM_aist.Time()
      OpenRTM_aist.ExecutionContextBase.invokeWorkerPreDo(self)
      OpenRTM_aist.ExecutionContextBase.invokeWorkerDo(self)
      OpenRTM_aist.ExecutionContextBase.invokeWorkerPostDo(self)
      t1_ = OpenRTM_aist.Time()
      guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
      self._workerthread._ticked = False
      del guard

      period_ = self.getPeriod()

      exctm_ = (t1_ - t0_).getTime().toDouble()
      slptm_ = period_.toDouble() - exctm_
      self._rtcout.RTC_PARANOID("Period:    %f [s]", period_.toDouble())
      self._rtcout.RTC_PARANOID("Execution: %f [s]", exctm_)
      self._rtcout.RTC_PARANOID("Sleep:     %f [s]", slptm_)

      t2_ = OpenRTM_aist.Time()

      if period_.toDouble() > ((t1_ - t0_).getTime().toDouble()):
        self._rtcout.RTC_PARANOID("sleeping...")
        slptm_ = period_.toDouble() - (t1_ - t0_).getTime().toDouble()
        time.sleep(slptm_)

      t3_ = OpenRTM_aist.Time()
      self._rtcout.RTC_PARANOID("Slept:     %f [s]", (t3_ - t2_).getTime().toDouble())
    return 0


  ##
  # @if jp
  # @brief ExecutionContext �ѤΥ���åɼ¹Դؿ�
  # @else
  # @brief Thread execution function for ExecutionContext
  # @endif
  # int ExtTrigExecutionContext::close(unsigned long flags)
  def close(self, flags):
    self._rtcout.RTC_TRACE("close()")
    # At this point, this component have to be finished.
    # Current state and Next state should be RTC_EXITING.
    return 0


  #============================================================
  # ExtTrigExecutionContextService
  #============================================================

  ##
  # @if jp
  # @brief ������1���ƥå׿ʤ��
  # @else
  # @brief Move forward one step of ExecutionContext
  # @endif
  # void ExtTrigExecutionContext::tick()
  #   throw (CORBA::SystemException)
  def tick(self):
    self._rtcout.RTC_TRACE("tick()")
    if not self.isRunning():
      self._rtcout.RTC_DEBUG("EC is not running. do nothing.")
      return

    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    self._workerthread._ticked = True
    self._workerthread._cond.acquire()
    self._workerthread._cond.notify()
    self._workerthread._cond.release()
    self._rtcout.RTC_PARANOID("EC was ticked. Signal was sent to worker thread.")
    del guard
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
  # CORBA::Boolean ExtTrigExecutionContext::is_running()
  #   throw (CORBA::SystemException)
  def is_running(self):
    return OpenRTM_aist.ExecutionContextBase.isRunning(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ򳫻�
  # @else
  # @brief Start the ExecutionContext
  # @endif
  # RTC::ReturnCode_t ExtTrigExecutionContext::start()
  #   throw (CORBA::SystemException)
  def start(self):
    return OpenRTM_aist.ExecutionContextBase.start(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ����
  # @else
  # @brief Stop the ExecutionContext
  # @endif
  # RTC::ReturnCode_t ExtTrigExecutionContext::stop()
  #   throw (CORBA::SystemException)
  def stop(self):
    return OpenRTM_aist.ExecutionContextBase.stop(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)���������
  # @else
  # @brief Get execution rate(Hz) of ExecutionContext
  # @endif
  # CORBA::Double ExtTrigExecutionContext::get_rate()
  #   throw (CORBA::SystemException)
  def get_rate(self):
    return OpenRTM_aist.ExecutionContextBase.getRate(self)


  ##
  # @if jp
  # @brief ExecutionContext �μ¹Լ���(Hz)�����ꤹ��
  # @else
  # @brief Set execution rate(Hz) of ExecutionContext
  # @endif
  # RTC::ReturnCode_t ExtTrigExecutionContext::set_rate(CORBA::Double rate)
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
  # ExtTrigExecutionContext::add_component(RTC::LightweightRTObject_ptr comp)
  #   throw (CORBA::SystemException)
  def add_component(self, comp):
    return OpenRTM_aist.ExecutionContextBase.addComponent(self, comp)


  ##
  # @if jp
  # @brief ����ݡ��ͥ�Ȥ򥳥�ݡ��ͥ�ȥꥹ�Ȥ���������
  # @else
  # @brief Remove the RT-Component from participant list
  # @endif
  # RTC::ReturnCode_t ExtTrigExecutionContext::
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
  # RTC::ReturnCode_t ExtTrigExecutionContext::
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
  # RTC::ReturnCode_t ExtTrigExecutionContext::
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
  # RTC::ReturnCode_t ExtTrigExecutionContext::
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
  # RTC::LifeCycleState ExtTrigExecutionContext::
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
  # RTC::ExecutionKind ExtTrigExecutionContext::get_kind()
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
  # RTC::ExecutionContextProfile* ExtTrigExecutionContext::get_profile()
  #   throw (CORBA::SystemException)
  def get_profile(self):
    return OpenRTM_aist.ExecutionContextBase.getProfile(self)


  #============================================================
  # protected functions
  #============================================================

  ##
  # @brief onStarted() template function
  # RTC::ReturnCode_t ExtTrigExecutionContext::onStarted()
  def onStarted(self):
    # change EC thread state
    guard = OpenRTM_aist.ScopedLock(self._svcmutex)
    if not self._svc:
      # If start() is called first time, start the worker thread.
      self._svc = True
      self.open(0)

    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t onStopping();
  def onStopping(self):
    guard = OpenRTM_aist.ScopedLock(self._svcmutex)
    self._svc = False
    del guard
    
    # stop thread
    self.tick()
    
    return RTC.RTC_OK

  ##
  # @brief onWaitingActivated() template function
  # RTC::ReturnCode_t ExtTrigExecutionContext::
  # onWaitingActivated(RTC_impl::RTObjectStateMachine* comp, long int count)
  def onWaitingActivated(self, comp, count):
    self._rtcout.RTC_TRACE("onWaitingActivated(count = %d)", count)
    self._rtcout.RTC_PARANOID("curr: %s, next: %s",
                              (self.getStateString(comp.getStates().curr),
                               self.getStateString(comp.getStates().next)))
    # Now comp's next state must be ACTIVE state
    # If worker thread is stopped, restart worker thread.
    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    self._workerthread._ticked = True
    self._workerthread._cond.acquire()
    self._workerthread._cond.notify()
    self._workerthread._cond.release()
    return RTC.RTC_OK


  ##
  # @brief onWaitingDeactivated() template function
  # RTC::ReturnCode_t ExtTrigExecutionContext::
  # onWaitingDeactivated(RTC_impl::RTObjectStateMachine* comp, long int count)
  def onWaitingDeactivated(self, comp, count):
    self._rtcout.RTC_TRACE("onWaitingDeactivated(count = %d)", count)
    self._rtcout.RTC_PARANOID("curr: %s, next: %s",
                              (self.getStateString(comp.getStates().curr),
                               self.getStateString(comp.getStates().next)))
    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    self._workerthread._ticked = True
    self._workerthread._cond.acquire()
    self._workerthread._cond.notify()
    self._workerthread._cond.release()
    return RTC.RTC_OK


  ##
  # @brief onWaitingReset() template function
  # RTC::ReturnCode_t ExtTrigExecutionContext::
  # onWaitingReset(RTC_impl::RTObjectStateMachine* comp, long int count)
  def onWaitingReset(self, comp, count):
    self._rtcout.RTC_TRACE("onWaitingReset(count = %d)", count)
    self._rtcout.RTC_PARANOID("curr: %s, next: %s",
                              (self.getStateString(comp.getStates().curr),
                               self.getStateString(comp.getStates().next)))
    guard = OpenRTM_aist.ScopedLock(self._workerthread._mutex)
    self._workerthread._ticked = True
    self._workerthread._cond.acquire()
    self._workerthread._cond.notify()
    self._workerthread._cond.release()
    return RTC.RTC_OK


  # bool threadRunning()
  def threadRunning(self):
    guard = OpenRTM_aist.ScopedLock(self._svcmutex)
    return self._svc



  ##
  # @if jp
  # @class Worker
  # @brief ExecutionContext ��ư���饹
  #
  # �¹Խ����˴ؤ�����¾����ʤɡ��ºݤν�����ƻ롦���椹�뤿��Υ��饹��
  #
  # @since 0.4.0
  #
  # @else
  #
  # @endif
  class Worker:
    """
    """
    
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
      self._ticked = False



##
# @if jp
# @brief ���� ExecutionContext ��Factory���饹����Ͽ��
#
# ����ExecutionContext����������Factory���饹��
# ExecutionContext������ObjectManager����Ͽ���롣
#
# @else
#
# @endif
def ExtTrigExecutionContextInit(manager):
  OpenRTM_aist.ExecutionContextFactory.instance().addFactory("ExtTrigExecutionContext",
                                                             OpenRTM_aist.ExtTrigExecutionContext,
                                                             OpenRTM_aist.ECDelete)
