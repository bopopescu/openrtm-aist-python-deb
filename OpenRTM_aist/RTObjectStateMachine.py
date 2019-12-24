#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file RTObjectStateMachine.py
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

from omniORB import CORBA, PortableServer

import OpenRTM_aist
import RTC

NUM_OF_LIFECYCLESTATE = 4

class RTObjectStateMachine:
  """
  """

  # RTObjectStateMachine(RTC::ExecutionContextHandle_t id,
  #                      RTC::LightweightRTObject_ptr comp);
  def __init__(self, id, comp):
    global NUM_OF_LIFECYCLESTATE
    self._id = id
    self._rtobj = comp
    self._sm = OpenRTM_aist.StateMachine(NUM_OF_LIFECYCLESTATE)
    self._ca   = False
    self._dfc  = False
    self._fsm  = False
    self._mode = False
    self._caVar   = None
    self._dfcVar  = None
    self._fsmVar  = None
    self._modeVar = None

    # Setting Action callback objects
    self.setComponentAction(comp)
    self.setDataFlowComponentAction(comp)
    self.setFsmParticipantAction(comp)
    self.setMultiModeComponentAction(comp)
    # Setting callback functions to StateMachine
    self._sm.setListener(self)
    self._sm.setEntryAction (RTC.ACTIVE_STATE,
                             self.onActivated)
    self._sm.setDoAction    (RTC.ACTIVE_STATE,
                             self.onExecute)
    self._sm.setPostDoAction(RTC.ACTIVE_STATE,
                             self.onStateUpdate)
    self._sm.setExitAction  (RTC.ACTIVE_STATE,
                             self.onDeactivated)
    self._sm.setEntryAction (RTC.ERROR_STATE,
                             self.onAborting)
    self._sm.setDoAction    (RTC.ERROR_STATE,
                             self.onError)
    self._sm.setExitAction  (RTC.ERROR_STATE,
                             self.onReset)
    # Setting inital state
    st = OpenRTM_aist.StateHolder()
    st.prev = RTC.INACTIVE_STATE
    st.curr = RTC.INACTIVE_STATE
    st.next = RTC.INACTIVE_STATE
    self._sm.setStartState(st)
    self._sm.goTo(RTC.INACTIVE_STATE)
    return


  def __del__(self):
    if self._ca:
      self._ca = False
      self._caVar = None

    if self._dfc:
      self._dfc = False
      self._dfcVar = None

    if self._fsm:
      self._fsm = False
      self._fsmVar = None

    if self._mode:
      self._mode = False
      self._modeVar = None

    return


  # functions for stored RTObject reference
  # RTC::LightweightRTObject_ptr getRTObject();
  def getRTObject(self):
    return self._rtobj

  # bool isEquivalent(RTC::LightweightRTObject_ptr comp);
  def isEquivalent(self, comp):
    return self._rtobj._is_equivalent(comp)

  # RTC::ExecutionContextHandle_t getExecutionContextHandle();
  def getExecutionContextHandle(self):
    return self._id

  # RTC::ComponentAction operations
  # void onStartup(void);
  def onStartup(self):
    if not self._ca:
      return
    self._caVar.on_startup(self._id)
    return

  # void onShutdown(void);
  def onShutdown(self):
    if not self._ca:
      return
    self._caVar.on_shutdown(self._id)
    return

  # void onActivated(const ExecContextStates& st);
  def onActivated(self, st):
    if not self._ca:
      return
    if self._caVar.on_activated(self._id) != RTC.RTC_OK:
      self._sm.goTo(RTC.ERROR_STATE)
    return

  # void onDeactivated(const ExecContextStates& st);
  def onDeactivated(self, st):
    if not self._ca:
      return
    self._caVar.on_deactivated(self._id)
    return

  # void onAborting(const ExecContextStates& st);
  def onAborting(self, st):
    if not self._ca:
      return
    self._caVar.on_error(self._id)
    return

  # void onError(const ExecContextStates& st);
  def onError(self, st):
    if not self._ca:
      return
    self._caVar.on_error(self._id)
    return

  # void onReset(const ExecContextStates& st);
  def onReset(self, st):
    if not self._ca:
      return
    if self._caVar.on_reset(self._id) != RTC.RTC_OK:
      self._sm.goTo(RTC.ERROR_STATE)
    return

  # RTC::DataflowComponentAction
  # void onExecute(const ExecContextStates& st);
  def onExecute(self, st):
    if not self._dfc:
      return
    
    if self._dfcVar.on_execute(self._id) != RTC.RTC_OK:
      self._sm.goTo(RTC.ERROR_STATE)
    return

  # void onStateUpdate(const ExecContextStates& st);
  def onStateUpdate(self, st):
    if not self._dfc:
      return
    
    if self._dfcVar.on_state_update(self._id) != RTC.RTC_OK:
      self._sm.goTo(RTC.ERROR_STATE)
    return

  # void onRateChanged(void);
  def onRateChanged(self):
    if not self._dfc:
      return
    
    if self._dfcVar.on_rate_changed(self._id) != RTC.RTC_OK:
      self._sm.goTo(RTC.ERROR_STATE)
    return

  # FsmParticipantAction
  # void onAction(const ExecContextStates& st);
  def onAction(self, st):
    if not self._fsm:
      return

    if self._fsmVar.on_action(self._id) != RTC.RTC_OK:
      self._sm.goTo(RTC.ERROR_STATE)
    return
  
  # MultiModeComponentAction
  # void onModeChanged(const ExecContextStates& st);
  def onModeChanged(self, st):
    if not self._mode:
      return

    if self._modeVar.on_mode_changed(self._id) != RTC.RTC_OK:
      self._sm.goTo(RTC.ERROR_STATE)
    return
  
  # Getting state of the context
  # ExecContextState getState(void);
  def getState(self):
    return self._sm.getState()

  # ExecContextStates getStates(void);
  def getStates(self):
    return self._sm.getStates()

  # bool isCurrentState(ExecContextState state);
  def isCurrentState(self, state):
    return self.getState() == state

  # bool isNextState(ExecContextState state);
  def isNextState(self, state):
    return self._sm.getStates().next == state

  # void goTo(ExecContextState state);
  def goTo(self, state):
    self._sm.goTo(state)
    return
    
  # Workers
  # void workerPreDo(void);
  def workerPreDo(self):
    return self._sm.worker_pre()

  # void workerDo(void);
  def workerDo(self):
    return self._sm.worker_do()

  # void workerPostDo(void);
  def workerPostDo(self):
    return self._sm.worker_post()

  # void setComponentAction(const RTC::LightweightRTObject_ptr comp);
  def setComponentAction(self, comp):
    self._caVar = comp._narrow(RTC.ComponentAction)
    if not CORBA.is_nil(self._caVar):
      self._ca = True
    return

  # void setDataFlowComponentAction(const RTC::LightweightRTObject_ptr comp);
  def setDataFlowComponentAction(self, comp):
    self._dfcVar = comp._narrow(RTC.DataFlowComponentAction)
    if not CORBA.is_nil(self._dfcVar):
      self._dfc = True
    return

  # void setFsmParticipantAction(const RTC::LightweightRTObject_ptr comp);
  def setFsmParticipantAction(self, comp):
    self._fsmVar = comp._narrow(RTC.FsmParticipantAction)
    if not CORBA.is_nil(self._fsmVar):
      self._fsm = True
    return

  # void setMultiModeComponentAction(const RTC::LightweightRTObject_ptr comp);
  def setMultiModeComponentAction(self, comp):
    self._modeVar = comp._narrow(RTC.MultiModeComponentAction)
    if not CORBA.is_nil(self._modeVar):
      self._mode = True
    return
