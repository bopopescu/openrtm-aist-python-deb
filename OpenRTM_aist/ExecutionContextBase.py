#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ExecutionContextBase.py
# @brief ExecutionContext base class
# @date $Date: 2007/08/31$
# @author Noriaki Ando <n-ando@aist.go.jp> and Shinji Kurihara
#
# Copyright (C) 2011
#    Task-intelligence Research Group,
#    Intelligent Systems Research Institute,
#    National Institute of
#       Advanced Industrial Science and Technology (AIST), Japan
#    All rights reserved.

import time
import OpenRTM_aist
import RTC

DEFAULT_EXECUTION_RATE = 1000

##
# @if jp
# @class ExecutionContextBase
# @brief ExecutionContext�Ѵ��쥯�饹
#
# EC�μ������饹�Ǥϡ����δ��쥯�饹��Ѿ���������EC��CORBA���ڥ졼
# ������������ʤ���Фʤ�ʤ�������ˡ��ºݤ˥��å����ư���뤿
# �ᡢ���Ĥ�����«��§��ExecutionContextBase�δؿ���ƤӽФ�ɬ�פ���
# �롣EC��CORBA���ڥ졼�����ϰʲ��Τ�Τ����ꡢ���줾��
# ExecutionContextBase�Υ��дؿ����б����Ƥ��롣
#
# - is_running(): ExecutionContextBase.isRunning()
# - start(): ExecutionContextBase.start()
# - stop(): ExecutionContextBase.stop()
#
# - get_rate(): ExecutionContextBase.gatRate()
# - set_rate(): ExecutioinContextBase.setRate()
#
# - add_component(): ExecutionContextBase.addComponent()
# - remove_component(): ExecutionContextBase.removeComponent()
#
# - activate_component(): ExecutionContextBase.activateComponent()
# - deactivate_component(): ExecutionContextBase.deactivateComponent()
# - reset_component(): ExecutionContextBase.resetComponent()
#
# - get_component_state(): ExecutionContextBase.getComponentState()
# - get_kind(): ExecutionContextBase.getKind()
# - get_profile(): ExecutionContextBase.getProfile()
#
# @par �¹Ծ��֤˴ط�����ؿ��ȼ�����ˡ
# - is_running(): ExecutionContextBase.isRunning()
# - start(): ExecutionContextBase.start()
# - stop(): ExecutionContextBase.stop()
#
# �¹Ծ��֤˴ط�����ؿ��ϡ�is_running(), start(), stop() ��3�Ĥ���
# �롣ExecutionContextBase�Ǥ�ñ��� running/stopped �Υե饰�����
# �Ƥ��ꡢstart/stop�ǥե饰��ON/OFF�ڤ��ؤ���is_running()�Ǿ����ɤ�
# �Ф���ԤäƤ��롣�̾EC�μ������饹�Ǥϡ�protected �ʲ��ۥ��
# �дؿ� onStarting(), onStarted(), onStopping(), onStopped() �ؿ���
# �������������ǡ�CORBA���ڥ졼������ʲ��Τ褦�˼�������ɬ�פ����롣
#
# is_running() ��CORBA���ڥ졼�����Ǥϡ�ñ���
# ExecutionContextBase �� isRunning() ��ƤӽФ������Ǥ��롣���δؿ�
# �˴�Ϣ���� protected ���۴ؿ���onIsRunning() ���Ѱդ���Ƥ��뤬��
# �̾��ä˼�������ɬ�פϤʤ��������ơ����ߤ� running/stopped ���֤�
# �񤭴����������ˤ��δؿ������Ѥ��뤳�Ȥ��Ǥ��뤬�侩�Ϥ���ʤ���
#
# <pre>
# public:
#  CORBA::Boolean is_runing()
#  {
#    return ExecutionContextBase::isRunning();
#  }
# protected:
#  CORBA::Boolean onIsRunning(CORBA::Boolean running)
#  {
#    return running;
#  }
# </pre>
#
# start(), stop() CORBA���ڥ졼�����Ǥϡ��̾�
# ExecutionContextBase �� start(), stop() �ؿ���ƤӽФ��褦�������롣
# ���δؿ��˴�Ϣ���� protected ���۴ؿ��ϡ�start() ����� stop() ��
# �Ĥ��Ƥ��줾��2�ĤŤĤ� onStarting(), onStarted(), �����
# onStopping(), onStopped() �ؿ������롣EC�μ������饹�ˤ����Ƥϡ���
# �줾��ʲ��Τ褦�˼������롣
#
# <pre>
#  RTC::ReturnCode_t start()
#  {
#    return ExecutionContextBase::start();
#  }
#  RTC::ReturnCode_t stop()
#  {
#    return ExecutionContextBase::stop();
#  }
# protected:
#  RTC::ReturnCode_t onStarting()
#  {
#    RTC::ReturnCode_t ret = // ����åɤ򳫻Ϥ�������ʤ�
#    return ret;
#  }
#  RTC::ReturnCode_t onStarted()
#  {
#    RTC::ReturnCode_t ret = // ����åɤ򳫻Ϥ�������ʤ�
#    return ret;
#  }
#  RTC::ReturnCode_t onStopping()
#  {
#    // ����åɤ���ߤ�������ʤ�
#    return retcode;
#  }
#  RTC::ReturnCode_t onStopped()
#  {
#    // ����åɤ���ߤ�������ʤ�
#    return retcode;
#  }
# </pre>
#
# @par �¹Լ����˴ؤ���ؿ��ȼ�����ˡ
# - get_rate(): ExecutionContextBase.gatRate()
# - set_rate(): ExecutioinContextBase.setRate()
#
# �¹Լ����˴ؤ���ؿ��� set_rate(), get_rate() ��2���ब���롣����
# ����¹ԥ���ƥ����Ȥ��⤷ set_rate() �ˤ����ꤵ�����������Ѥ���
# ��硢�ƥ�ץ졼�ȴؿ� onSetRate() �򥪡��С��饤�ɤ��������롣
# onSetRate() �ϰ����� double ���μ������ꡢ�����ͤ��������ͤǤ���
# ���Ȥ��ݾڤ���Ƥ��롣onSetRate() ��RTC::RTC_OK �ʳ����ͤ��֤�����
# �硢EC��Profile�μ��������ꤵ���������ͤ��ݻ����뤳�Ȥ��ݾڤ���
# �롣
#
# set_rate() Ʊ�� get_rate() �ƤӽФ�����onGetRate() ���ƤӽФ����
# ����������̾索���С��饤�ɤ���ɬ�פϤʤ�����������get_rate() ��
# �֤��ͤ��ѹ���������硢onGetRate() �򥪡��С��饤�ɤ��뤳�ȤǤ���
# �ͤ�񤭴����뤳�Ȥ��Ǥ��롣������������Ͽ侩����ʤ���
#
# <pre>
# public:
#  RTC::ReturnCode_t set_rate(double rate)
#  {
#    return setRate(rate);
#  }
#  double get_rate(void) const
#  {
#    return getRate();
#  }
# protected:
#  virtual RTC::ReturnCode_t onSetRate(double rate)
#  {
#    RTC::ReturnCode_t ret = // ���������ꤹ�벿�餫�ν���
#    if (ret != RTC::RTC_OK)
#      {
#        RTC_ERROR(("Error message"));
#      }
#    return ret;
#  }
#  virtual double onGetRate(rate)
#  {
#    // get_rate() ���֤��ͤ�ù����������
#    // �̾�Ϥ��δؿ����������ɬ�פϤʤ���
#    return rate;
#  }
# </pre>
#
# @par ����ݡ��ͥ�Ȥ��ɲäȺ���˴ؤ���ؿ�
# - add_component(): ExecutionContextBase.addComponent()
# - remove_component(): ExecutionContextBase.removeComponent()
#
# ����ݡ��ͥ�Ȥ��ɲäȺ���˴ؤ���ؿ��ϡ�add_component(),
# remove_component() ������ब���롣�¹ԥ���ƥ����Ȥμ������饹��
# �����Ƥϡ�ExecutionContextBase �Τ��줾�� addComponent(),
# removeComponent() ��ƤӽФ����Ǽ�����Ԥ��������δؿ��˴�Ϣ����
# protected ���۴ؿ��� onAddingComponent(), onAddedComponent(),
# onRemovingComponent(), onRemovedComponent() ��4���ढ�롣��������
# �����β��۴ؿ����̾索���С��饤�ɤ���ɬ�פϤʤ������ѤϿ侩����
# �ʤ���
#
# <pre>
# public:
#  RTC::ReturnCode_t add_component(RTC::LightweightRTObject_ptr comp)
#  {
#    return ExecutionContextBase::addComponent(comp);
#  }
#  RTC::ReturnCode_t remove_component(RTC::LightweightRTObject_ptr comp)
#  {
#    return ExecutionContextBase::removeComponent(comp);
#  }
# protected:
#  virtual RTC::ReturnCode_t
#  onAddingComponent(RTC::LightweightRTObject rtobj)
#  {
#     // ����ݡ��ͥ���ɲû��˼¹Ԥ����������򵭽�
#     // RTC::RTC_OK �ʳ����֤�����硢����ݡ��ͥ�Ȥ��ɲäϹԤ��ʤ���
#     return RTC::RTC_OK;
#  }
#  virtual RTC::ReturnCode_t
#  onAddedComponent(RTC::LightweightRTObject rtobj)
#  {
#     // ����ݡ��ͥ���ɲû��˼¹Ԥ����������򵭽�
#     // RTC::RTC_OK �ʳ����֤�����硢removeComponent() ���ƤӽФ��졢
#     // �ɲä��줿����ݡ��ͥ�Ȥ��������롣
#     return RTC::RTC_OK;
#  }
#  virtual RTC::ReturnCode_t
#  onRemovingComponent(RTC::LightweightRTObject rtobj)
#  {
#     // ����ݡ��ͥ�Ⱥ�����˼¹Ԥ����������򵭽�
#     // RTC::RTC_OK �ʳ����֤�����硢����ݡ��ͥ�Ȥκ���ϹԤ��ʤ���
#     return RTC::RTC_OK;
#  }
#  virtual RTC::ReturnCode_t
#  onRemovedComponent(RTC::LightweightRTObject rtobj)
#  {
#     // ����ݡ��ͥ���ɲû��˼¹Ԥ����������򵭽�
#     // RTC::RTC_OK �ʳ����֤�����硢addComponent() ���ƤӽФ��졢
#     // ������줿����ݡ��ͥ�Ȥ��Ƥ��ɲä���롣
#     return RTC::RTC_OK;
#  }
# </pre>
#
# @par ����ݡ��ͥ�ȤΥ����ƥ��ֲ����˴ؤ���ؿ�
# - activate_component(): ExecutionContextBase.activateComponent()
# - deactivate_component(): ExecutionContextBase.deactivateComponent()
# - reset_component(): ExecutionContextBase.resetComponent()
#
# ����ݡ��ͥ�ȤΥ����ƥ��ֲ����˴ؤ���ؿ��ϡ�
# activate_component(), deactivate_component(), reset_component() ��
# �����ब���롣�¹ԥ���ƥ����Ȥμ������饹�ˤ����Ƥϡ�
# ExecutionContextBase �Τ��줾�� activateComponent(),
# deactivateComponent(), resetComponent() ��ƤӽФ����Ǽ�����Ԥ���
# �����δؿ��˴�Ϣ���� protected ���۴ؿ���
# onActivatingComponent(), onAtivatingComponent(),
# onActivatedComponent(), onDeactivatingComponent(),
# onDeactivatedComponent(), onResettingComponent(),
# onResetComponent() ��6���ढ�롣�������������β��۴ؿ����̾索��
# �С��饤�ɤ���ɬ�פϤʤ������ѤϿ侩����ʤ���
#
# <pre>
# public:
#  RTC::ReturnCode_t add_component(RTC::LightweightRTObject_ptr comp)
#  {
#    return ExecutionContextBase::addComponent(comp);
#  }
#  RTC::ReturnCode_t remove_component(RTC::LightweightRTObject_ptr comp)
#  {
#    return ExecutionContextBase::removeComponent(comp);
#  }
# protected:
#  virtual RTC::ReturnCode_t
#  onAddingComponent(RTC::LightweightRTObject rtobj)
#  {
#    // ����ݡ��ͥ���ɲû��˼¹Ԥ����������򵭽�
#    // RTC::RTC_OK �ʳ����֤�����硢����ݡ��ͥ�Ȥ��ɲäϹԤ��ʤ���
#    return RTC::RTC_OK;
#  }
#  virtual RTC::ReturnCode_t
#  onAddedComponent(RTC::LightweightRTObject rtobj)
#  {
#    // ����ݡ��ͥ���ɲû��˼¹Ԥ����������򵭽�
#    // RTC::RTC_OK �ʳ����֤�����硢removeComponent() ���ƤӽФ��졢
#    // �ɲä��줿����ݡ��ͥ�Ȥ��������롣
#    return RTC::RTC_OK;
#  }
#  virtual RTC::ReturnCode_t
#  onRemovingComponent(RTC::LightweightRTObject rtobj)
#  {
#    // ����ݡ��ͥ�Ⱥ�����˼¹Ԥ����������򵭽�
#    // RTC::RTC_OK �ʳ����֤�����硢����ݡ��ͥ�Ȥκ���ϹԤ��ʤ���
#    return RTC::RTC_OK;
#  }
#  virtual RTC::ReturnCode_t
#  onRemovedComponent(RTC::LightweightRTObject rtobj)
#  {
#    // ����ݡ��ͥ���ɲû��˼¹Ԥ����������򵭽�
#    // RTC::RTC_OK �ʳ����֤�����硢addComponent() ���ƤӽФ��졢
#    // ������줿����ݡ��ͥ�Ȥ��Ƥ��ɲä���롣
#    return RTC::RTC_OK;
#  }
# </pre>
#
# @par �¹ԥ���ƥ����Ȥξ�������˴ؤ���ؿ�
# - get_component_state(): ExecutionContextBase.getComponentState()
# - get_kind(): ExecutionContextBase.getKind()
# - get_profile(): ExecutionContextBase.getProfile()
#
# �¹ԥ���ƥ����Ȥξ�������˴ؤ���ؿ��ϡ�get_component_state(),
# get_kind(), get_profile() ��3���ब���롣�¹ԥ���ƥ����Ȥμ�����
# �饹�ˤ����Ƥϡ�ExecutionContextBase �Τ��줾��
# getComponentState(), getKind(), getProfile() ��ƤӽФ����Ǽ�����
# �Ԥ��������δؿ��˴�Ϣ���� protected ���۴ؿ���
# onGetComponentState(), onGetKind(), onGetProfile() ��3���ढ�롣��
# ���β��۴ؿ����̾索���С��饤�ɤ���ɬ�פϤʤ������ѤϿ侩�����
# �������������֤�������ѹ����������ϡ������δؿ���Ŭ�ڤ˼�����
# �뤳�Ȥǡ��ƤӽФ�¦���֤��ͤ��񤭤��뤳�Ȥ��Ǥ��롣
#
# <pre>
# public:
#  LifeCycleState get_component_state(RTC::LightweightRTObject_ptr comp)
#  {
#    return getComponentState(comp);
#  }
#  ExecutionKind PeriodicExecutionContext::get_kind()
#  {
#    return getKind();
#  }
#  ExecutionContextProfile* get_profile()
#  {
#    return getProfile();
#  }
#
# protected:
#  virtual LifeCycleState onGetComponentState(LifeCycleState state)
#  { // �֤�state��񤭴����������Ϥ��δؿ����������
#    return state;
#  }
#  virtual ExecutionKind onGetKind(ExecutionKind kind)
#  { // �֤�kind��񤭴����������Ϥ��δؿ����������
#    return kind;
#  }
#  virtual ExecutionContextProfile*
#  onGetProfile(ExecutionContextProfile*& profile)
#  { // �֤�profile��񤭴����������Ϥ��δؿ����������
#    return profile;
#  }
# </pre>
#
# ExecutionContext�δ��쥯�饹��
#
# @since 0.4.0
#
# @else
# @class ExecutionContextBase
# @brief A base class for ExecutionContext
#
# A base class of ExecutionContext.
#
# @since 0.4.0
#
# @endif
#
class ExecutionContextBase:
  """
  """

  def __init__(self, name):
    self._rtcout  = OpenRTM_aist.Manager.instance().getLogbuf("ec_base")
    self._activationTimeout   = OpenRTM_aist.TimeValue(0.5)
    self._deactivationTimeout = OpenRTM_aist.TimeValue(0.5)
    self._resetTimeout        = OpenRTM_aist.TimeValue(0.5)
    self._syncActivation   = True
    self._syncDeactivation = True
    self._syncReset        = True
    self._worker  = OpenRTM_aist.ExecutionContextWorker()
    self._profile = OpenRTM_aist.ExecutionContextProfile()


  ##
  # @if jp
  # @brief ExecutionContext�ν��������
  #
  # @else
  # @brief Initialization function of the ExecutionContext
  #
  # @endif
  # virtual void init(coil::Properties& props);
  def init(self, props):
    self._rtcout.RTC_TRACE("init()")
    self._rtcout.RTC_DEBUG(props)
    
    # setting rate
    self.setExecutionRate(props)
    
    # getting sync/async mode flag
    transitionMode_ = [False]
    if self.setTransitionMode(props, "sync_transition", transitionMode_):
      self._syncActivation   = transitionMode_[0]
      self._syncDeactivation = transitionMode_[0]
      self._syncReset        = transitionMode_[0]

    syncactivation_   = [self._syncActivation]
    syncdeactivation_ = [self._syncDeactivation]
    syncreset_        = [self._syncReset]
    self.setTransitionMode(props, "sync_activation", syncactivation_)
    self.setTransitionMode(props, "sync_deactivation", syncdeactivation_)
    self.setTransitionMode(props, "sync_reset", syncreset_)
    self._syncActivation   = syncactivation_[0]
    self._syncDeactivation = syncdeactivation_[0]
    self._syncReset        = syncreset_[0]
    
    # getting transition timeout
    timeout_ = [0.0]
    if self.setTimeout(props, "transition_timeout", timeout_):
      self._activationTimeout   = timeout_[0]
      self._deactivationTimeout = timeout_[0]
      self._resetTimeout        = timeout_[0]

    activationTO_   = [self._activationTimeout]
    deactivationTO_ = [self._deactivationTimeout]
    resetTO_        = [self._resetTimeout]
    self.setTimeout(props, "activation_timeout",   activationTO_)
    self.setTimeout(props, "deactivation_timeout", deactivationTO_)
    self.setTimeout(props, "reset_timeout",        resetTO_)
    self._activationTimeout   = activationTO_[0]
    self._deactivationTimeout = deactivationTO_[0]
    self._resetTimeout        = resetTO_[0]

    self._rtcout.RTC_DEBUG("ExecutionContext's configurations:")
    self._rtcout.RTC_DEBUG("Exec rate   : %f [Hz]", self.getRate())

    toSTR_ = lambda x: "YES" if x else "NO"

    self._rtcout.RTC_DEBUG("Activation  : Sync = %s, Timeout = %f",
                           (toSTR_(self._syncActivation), float(self._activationTimeout.toDouble())))
    self._rtcout.RTC_DEBUG("Deactivation: Sync = %s, Timeout = %f",
                           (toSTR_(self._syncActivation), float(self._deactivationTimeout.toDouble())))
    self._rtcout.RTC_DEBUG("Reset       : Sync = %s, Timeout = %f",
                           (toSTR_(self._syncReset), float(self._resetTimeout.toDouble())))
    # Setting given Properties to EC's profile::properties
    self.setProperties(props)
    return


  ##
  # @if jp
  # @brief ExecutionContext�ν�����ʤ��(���֥��饹������)
  #
  # ExecutionContext�ν����򣱼���ʬ�ʤ�롣<BR>
  # �����֥��饹�Ǥμ���������
  #
  # @param self
  #
  # @else
  # @brief Destructor
  # @endif
  #def tick(self):
  #  pass


  ##
  # @if jp
  # @brief ����ݡ��ͥ�Ȥ�Х���ɤ��롣
  #
  # ����ݡ��ͥ�Ȥ�Х���ɤ��롣
  #
  # @else
  # @brief Bind the component.
  #
  # Bind the component.
  #
  # @endif
  def bindComponent(self, rtc):
    return self._worker.bindComponent(rtc)


  #============================================================
  # Functions to be delegated by EC's CORBA operations

  ##
  # @if jp
  # @brief ExecutionContext �¹Ծ��ֳ�ǧ�ؿ�
  # @else
  # @brief Check for ExecutionContext running state
  # @endif
  # CORBA::Boolean ExecutionContextBase::isRunning()
  def isRunning(self):
    self._rtcout.RTC_TRACE("isRunning()")
    return self._worker.isRunning()

  
  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ򳫻�
  # @else
  # @brief Start the ExecutionContext
  # @endif
  # RTC::ReturnCode_t ExecutionContextBase::start()
  def start(self):
    self._rtcout.RTC_TRACE("start()")
    ret_ = self.onStarting() # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onStarting() failed. Starting EC aborted.")
      return ret_

    ret_ = self._worker.start() # Actual start()
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Invoking on_startup() for each RTC failed.")
      return ret_

    ret_ = self.onStarted() # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onStartted() failed. Started EC aborted..")
      self._worker.stop()
      self._rtcout.RTC_ERROR("on_shutdown() was invoked, because of onStarted")
      return ret_

    return ret_

  
  ##
  # @if jp
  # @brief ExecutionContext �μ¹Ԥ����
  # @else
  # @brief Stopping the ExecutionContext
  # @endif
  # RTC::ReturnCode_t ExecutionContextBase::stop()
  def stop(self):
    self._rtcout.RTC_TRACE("stop()")
    ret_ = self.onStopping() # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onStopping() failed. Stopping EC aborted.")
      return ret_

    ret_ = self._worker.stop() # Actual stop()
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Invoking on_shutdown() for each RTC failed.")
      return ret_

    ret_ = self.onStopped() # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onStopped() failed. Stopped EC aborted.")
      return ret_

    return ret_

  
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
  # double getRate(void) const
  def getRate(self):
    rate_ = self._profile.getRate() # Actual getRate()
    return self.onGetRate(rate_) # Template

  
  # coil::TimeValue ExecutionContextBase::getPeriod(void) const
  def getPeriod(self):
    return self._profile.getPeriod()

  
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
  # RTC::ReturnCode_t setRate(double rate)
  def setRate(self, rate):
    self._rtcout.RTC_TRACE("setRate(%f)", rate)
    ret_ = self._profile.setRate(self.onSettingRate(rate))
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Setting execution rate failed. %f", rate)
      return ret_

    ret_ = self.onSetRate(rate)
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onSetRate(%f) failed.", rate)
      return ret_

    self._rtcout.RTC_INFO("setRate(%f) done", rate)
    return ret_

  
  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��ɲä���
  # @else
  # @brief Add an RT-component
  # @endif
  # RTC::ReturnCode_t ExecutionContextBase::
  # addComponent(RTC::LightweightRTObject_ptr comp)
  def addComponent(self, comp):
    self._rtcout.RTC_TRACE("addComponent()")
    ret_ = self.onAddingComponent(comp) # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Error: onAddingComponent(). RTC is not attached.")
      return ret_

    ret_ = self._worker.addComponent(comp) # Actual addComponent()
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Error: ECWorker addComponent() faild.")
      return ret_

    ret_ = self._profile.addComponent(comp) # Actual addComponent()
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Error: ECProfile addComponent() faild.")
      return ret_

    ret_ = self.onAddedComponent(comp) # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Error: onAddedComponent() faild.")
      self._rtcout.RTC_INFO("Removing attached RTC.")
      self._worker.removeComponent(comp)
      self._profile.removeComponent(comp)
      return ret_

    self._rtcout.RTC_INFO("Component has been added to this EC.")
    return RTC.RTC_OK

  
  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ򻲲üԥꥹ�Ȥ���������
  # @else
  # @brief Remove the RT-Component from participant list
  # @endif
  # RTC::ReturnCode_t ExecutionContextBase::
  # removeComponent(RTC::LightweightRTObject_ptr comp)
  def removeComponent(self, comp):
    self._rtcout.RTC_TRACE("removeComponent()")
    ret_ = self.onRemovingComponent(comp) # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Error: onRemovingComponent(). "
                             "RTC will not not attached.")
      return ret_

    ret_ = self._worker.removeComponent(comp) # Actual removeComponent()
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Error: ECWorker removeComponent() faild.")
      return ret_

    ret_ = self._profile.removeComponent(comp) # Actual removeComponent()
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Error: ECProfile removeComponent() faild.")
      return ret_

    ret_ = self.onRemovedComponent(comp) # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("Error: onRemovedComponent() faild.")
      self._rtcout.RTC_INFO("Removing attached RTC.")
      self._worker.removeComponent(comp)
      self._profile.removeComponent(comp)
      return ret_

    self._rtcout.RTC_INFO("Component has been removeed to this EC.")
    return RTC.RTC_OK

  
  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ򥢥��ƥ��ֲ�����
  # @else
  # @brief Activate an RT-component
  # @endif
  # RTC::ReturnCode_t ExecutionContextBase::
  # activateComponent(RTC::LightweightRTObject_ptr comp)
  def activateComponent(self, comp):
    self._rtcout.RTC_TRACE("activateComponent()")
    ret_ = self.onActivating(comp) # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onActivating() failed.")
      return ret_

    rtobj_ = [None]
    ret_ = self._worker.activateComponent(comp, rtobj_) # Actual activateComponent()
    if ret_ != RTC.RTC_OK:
      return ret_

    if not self._syncActivation: # Asynchronous activation mode
      ret_ = self.onActivated(rtobj_[0], -1)
      if ret_ != RTC.RTC_OK:
        self._rtcout.RTC_ERROR("onActivated() failed.")

      return ret_

    #------------------------------------------------------------
    # Synchronized activation mode
    self._rtcout.RTC_DEBUG("Synchronous activation mode. "
                           "Waiting for the RTC to be ACTIVE state. ")
    return self.waitForActivated(rtobj_[0])


  # RTC::ReturnCode_t ExecutionContextBase::
  # waitForActivated(RTC_impl::RTObjectStateMachine* rtobj)
  def waitForActivated(self, rtobj):
    count_ = 0
    ret_ = self.onWaitingActivated(rtobj, count_)
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onWaitingActivated failed.")
      return ret_

    cycle_ = int(float(self._activationTimeout.toDouble()) / float(self.getPeriod().toDouble()))
    self._rtcout.RTC_DEBUG("Timeout is %f [s] (%f [s] in %d times)",
                           (float(self._activationTimeout.toDouble()), self.getRate(), cycle_))
    # Wating INACTIVE -> ACTIVE
    starttime_ = OpenRTM_aist.Time().gettimeofday()
    while rtobj.isCurrentState(RTC.INACTIVE_STATE):
      ret_ = self.onWaitingActivated(rtobj, count_) # Template method
      if ret_ != RTC.RTC_OK:
        self._rtcout.RTC_ERROR("onWaitingActivated failed.")
        return ret_

      time.sleep(self.getPeriod().toDouble())
      delta_ = OpenRTM_aist.Time().gettimeofday() - starttime_
      self._rtcout.RTC_DEBUG("Waiting to be ACTIVE state. %f [s] slept (%d/%d)",
                             (float(delta_.toDouble()), count_, cycle_))
      count_ += 1
      if delta_.toDouble() > self._activationTimeout.toDouble() or count_ > cycle_:
        self._rtcout.RTC_WARN("The component is not responding.")
        break


    # Now State must be ACTIVE or ERROR
    if rtobj.isCurrentState(RTC.INACTIVE_STATE):
      self._rtcout.RTC_ERROR("Unknown error: Invalid state transition.")
      return RTC.RTC_ERROR

    self._rtcout.RTC_DEBUG("Current state is %s", self.getStateString(rtobj.getState()))
    ret_ = self.onActivated(rtobj, count_) # Template method
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onActivated() failed.")

    self._rtcout.RTC_DEBUG("onActivated() done.")
    return ret_


  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ��󥢥��ƥ��ֲ�����
  # @else
  # @brief Deactivate an RT-component
  # @endif
  # RTC::ReturnCode_t ExecutionContextBase::
  # deactivateComponent(RTC::LightweightRTObject_ptr comp)
  def deactivateComponent(self, comp):
    self._rtcout.RTC_TRACE("deactivateComponent()")
    ret_ = self.onDeactivating(comp) # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onDeactivatingComponent() failed.")
      return ret_

    # Deactivate all the RTCs
    rtobj_ = [None]
    ret_ = self._worker.deactivateComponent(comp, rtobj_)
    if ret_ != RTC.RTC_OK:
      return ret_

    if not self._syncDeactivation:
      ret_ = self.onDeactivated(rtobj_[0], -1)
      if ret_ != RTC.RTC_OK:
        self._rtcout.RTC_ERROR("onDeactivated() failed.")
      return ret_

    #------------------------------------------------------------
    # Waiting for synchronized deactivation
    self._rtcout.RTC_DEBUG("Synchronous deactivation mode. "
                           "Waiting for the RTC to be INACTIVE state. ")
    return self.waitForDeactivated(rtobj_[0])


  # RTC::ReturnCode_t ExecutionContextBase::
  # waitForDeactivated(RTC_impl::RTObjectStateMachine* rtobj)
  def waitForDeactivated(self, rtobj):
    count_ = 0
    ret_ = self.onWaitingDeactivated(rtobj, count_)
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onWaitingDeactivated failed.")
      return ret_

    cycle_ = int(float(self._deactivationTimeout.toDouble()) / float(self.getPeriod().toDouble()))
    self._rtcout.RTC_DEBUG("Timeout is %f [s] (%f [s] in %d times)",
                           (float(self._deactivationTimeout.toDouble()), self.getRate(), cycle_))
    # Wating ACTIVE -> INACTIVE
    starttime_ = OpenRTM_aist.Time().gettimeofday()
    while rtobj.isCurrentState(RTC.ACTIVE_STATE):
      ret_ = self.onWaitingDeactivated(rtobj, count_) # Template method
      if ret_ != RTC.RTC_OK:
        self._rtcout.RTC_ERROR("onWaitingDeactivated failed.")
        return ret_

      time.sleep(self.getPeriod().toDouble())
      delta_ = OpenRTM_aist.Time().gettimeofday() - starttime_
      self._rtcout.RTC_DEBUG("Waiting to be INACTIVE state. Sleeping %f [s] (%d/%d)",
                             (float(delta_.toDouble()), count_, cycle_))
      count_ += 1
      if delta_.toDouble() > self._deactivationTimeout.toDouble() or count_ > cycle_:
        self._rtcout.RTC_ERROR("The component is not responding.")
        break


    # Now State must be INACTIVE or ERROR
    if rtobj.isCurrentState(RTC.ACTIVE_STATE):
      self._rtcout.RTC_ERROR("Unknown error: Invalid state transition.")
      return RTC.RTC_ERROR

    self._rtcout.RTC_DEBUG("Current state is %s", self.getStateString(rtobj.getState()))
    ret_ = self.onDeactivated(rtobj, count_)
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onDeactivated() failed.")

    self._rtcout.RTC_DEBUG("onDeactivated() done.")
    return ret_

  
  ##
  # @if jp
  # @brief RT����ݡ��ͥ�Ȥ�ꥻ�åȤ���
  # @else
  # @brief Reset the RT-component
  # @endif
  # RTC::ReturnCode_t ExecutionContextBase::
  # resetComponent(RTC::LightweightRTObject_ptr comp)
  def resetComponent(self, comp):
    self._rtcout.RTC_TRACE("resetComponent()")
    ret_ = self.onResetting(comp) # Template
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onResetting() failed.")
      return ret_

    rtobj_ = [None]
    ret_ = self._worker.resetComponent(comp, rtobj_) # Actual resetComponent()
    if ret_ != RTC.RTC_OK:
      return ret_
    if not self._syncReset:
      ret_ = self.onReset(rtobj_[0], -1)
      if ret_ != RTC.RTC_OK:
        self._rtcout.RTC_ERROR("onReset() failed.")
      return ret_

    #------------------------------------------------------------
    # Waiting for synchronized reset
    self._rtcout.RTC_DEBUG("Synchronous reset mode. "
                           "Waiting for the RTC to be INACTIVE state. ")
    return self.waitForReset(rtobj_[0])

  
  # RTC::ReturnCode_t ExecutionContextBase::
  # waitForReset(RTC_impl::RTObjectStateMachine* rtobj)
  def waitForReset(self, rtobj):
    count_ = 0
    ret_ = self.onWaitingReset(rtobj, count_)
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onWaitingReset() failed.")
      return ret_

    cycle_ = int(float(self._resetTimeout.toDouble()) / float(self.getPeriod().toDouble()))
    self._rtcout.RTC_DEBUG("Timeout is %f [s] (%f [s] in %d times)",
                           (float(self._resetTimeout.toDouble()), self.getRate(), cycle_))
    # Wating ERROR -> INACTIVE
    starttime_ = OpenRTM_aist.Time().gettimeofday()
    while rtobj.isCurrentState(RTC.ERROR_STATE):
      ret_ = self.onWaitingReset(rtobj, count_) # Template
      if ret_ != RTC.RTC_OK:
        self._rtcout.RTC_ERROR("onWaitingReset failed.")
        return ret_

      time.sleep(self.getPeriod().toDouble())
      delta_ = OpenRTM_aist.Time().gettimeofday() - starttime_
      self._rtcout.RTC_DEBUG("Waiting to be INACTIVE state. Sleeping %f [s] (%d/%d)",
                             (float(delta_.toDouble()), count_, cycle_))
      count_ += 1
      if delta_.toDouble() > self._resetTimeout.toDouble() or count_ > cycle_:
        self._rtcout.RTC_ERROR("The component is not responding.")
        break

    # Now State must be INACTIVE
    if not rtobj.isCurrentState(RTC.INACTIVE_STATE):
      self._rtcout.RTC_ERROR("Unknown error: Invalid state transition.")
      return RTC.RTC_ERROR

    self._rtcout.RTC_DEBUG("Current state is %s", self.getStateString(rtobj.getState()))
    ret_ = self.onReset(rtobj, count_) # Template method
    if ret_ != RTC.RTC_OK:
      self._rtcout.RTC_ERROR("onResetd() failed.")

    self._rtcout.RTC_DEBUG("onReset() done.")
    return ret_


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
  # RTC::LifeCycleState ExecutionContextBase::
  # getComponentState(RTC::LightweightRTObject_ptr comp)
  def getComponentState(self, comp):
    state_ = self._worker.getComponentState(comp)
    self._rtcout.RTC_TRACE("getComponentState() = %s", self.getStateString(state_))
    if state_ == RTC.CREATED_STATE:
      self._rtcout.RTC_ERROR("CREATED state: not initialized "
                             "RTC or unknwon RTC specified.")

    return self.onGetComponentState(state_)


  # const char* ExecutionContextBase::getStateString(RTC::LifeCycleState state)
  def getStateString(self, state):
    return self._worker.getStateString(state)


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
  # RTC::ExecutionKind ExecutionContextBase::getKind(void) const
  def getKind(self):
    kind_ = self._profile.getKind()
    self._rtcout.RTC_TRACE("getKind() = %s", self.getKindString(kind_))
    kind_ = self.onGetKind(kind_)
    self._rtcout.RTC_DEBUG("onGetKind() returns %s", self.getKindString(kind_))
    return kind_

  
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
  # RTC::ExecutionContextProfile* ExecutionContextBase::getProfile(void)
  def getProfile(self):
    self._rtcout.RTC_TRACE("getProfile()")
    prof_ = self._profile.getProfile()
    self._rtcout.RTC_DEBUG("kind: %s", self.getKindString(prof_.kind))
    self._rtcout.RTC_DEBUG("rate: %f", prof_.rate)
    self._rtcout.RTC_DEBUG("properties:")
    props_ = OpenRTM_aist.Properties()
    OpenRTM_aist.NVUtil.copyToProperties(props_, prof_.properties)
    self._rtcout.RTC_DEBUG(props_)
    return self.onGetProfile(prof_)

  

  #============================================================
  # Delegated functions to ExecutionContextProfile
  #============================================================
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
  # void setObjRef(RTC::ExecutionContextService_ptr ec_ptr)
  def setObjRef(self, ec_ptr):
    self._worker.setECRef(ec_ptr)
    self._profile.setObjRef(ec_ptr)
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
  def getObjRef(self):
    return self._profile.getObjRef()


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
  # const char* getKindString(RTC::ExecutionKind kind) const
  def getKindString(self, kind):
    return self._profile.getKindString(kind)


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
  # RTC::ReturnCode_t setKind(RTC::ExecutionKind kind)
  def setKind(self, kind):
    return self._profile.setKind(kind)


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
  # RTC::ReturnCode_t setOwner(RTC::LightweightRTObject_ptr comp)
  def setOwner(self, comp):
    return self._profile.setOwner(comp)


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
  # const RTC::RTObject_ptr getOwner() const
  def getOwner(self):
    return self._profile.getOwner()


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
  # const RTC::RTCList& getComponentList() const
  def getComponentList(self):
    return self._profile.getComponentList()


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
  # void setProperties(coil::Properties& props)
  def setProperties(self, props):
    self._profile.setProperties(props)
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
  # const coil::Properties getProperties() const
  def getProperties(self):
    return self._profile.getProperties()


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
  # RTC::ExecutionContextProfile* getProfile(void)
  def getProfile(self):
    return self._profile.getProfile()


  # end of delegated functions to ExecutionContextProfile
  #============================================================

  #============================================================
  # Delegated functions to ExecutionContextWorker
  #============================================================
  # bool isAllCurrentState(RTC::LifeCycleState state)
  def isAllCurrentState(self, state):
    return self._worker.isAllCurrentState(state)

  # bool isAllNextState(RTC::LifeCycleState state)
  def isAllNextState(self, state):
    return self._worker.isAllNextState(state)

  # bool isOneOfCurrentState(RTC::LifeCycleState state)
  def isOneOfCurrentState(self, state):
    return self._worker.isOneOfCurrentState(state)

  # bool isOneOfNextState(RTC::LifeCycleState state)
  def isOneOfNextState(self, state):
    return self._worker.isOneOfNextState(state)
    
  # void invokeWorker()       { m_worker.invokeWorker(); }
  def invokeWorker(self):
    self._worker.invokeWorker()
    return

  # void invokeWorkerPreDo()  { m_worker.invokeWorkerPreDo(); }
  def invokeWorkerPreDo(self):
    self._worker.invokeWorkerPreDo()
    return

  # void invokeWorkerDo()     { m_worker.invokeWorkerDo(); }
  def invokeWorkerDo(self):
    self._worker.invokeWorkerDo()
    return

  # void invokeWorkerPostDo() { m_worker.invokeWorkerPostDo(); }
  def invokeWorkerPostDo(self):
    self._worker.invokeWorkerPostDo()
    return

  # template virtual functions related to start/stop
  # virtual bool onIsRunning(bool running) { return running; }
  def onIsRunning(self, running):
    return running

  # virtual RTC::ReturnCode_t onStarting() { return RTC::RTC_OK; }
  def onStarting(self):
    return RTC.RTC_OK
  
  # virtual RTC::ReturnCode_t onStarted() { return RTC::RTC_OK; }
  def onStarted(self):
    return RTC.RTC_OK
  
  # virtual RTC::ReturnCode_t onStopping() { return RTC::RTC_OK; }
  def onStopping(self):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t onStopped() { return RTC::RTC_OK; }
  def onStopped(self):
    return RTC.RTC_OK

  # template virtual functions getting/setting execution rate
  # virtual double onGetRate(double rate) const { return rate; }
  def onGetRate(self, rate):
    return rate

  # virtual double onSettingRate(double rate) { return rate; }
  def onSettingRate(self, rate):
    return rate

  # virtual RTC::ReturnCode_t onSetRate(double rate) { return RTC::RTC_OK; }
  def onSetRate(self, rate):
    return RTC.RTC_OK

  # template virtual functions adding/removing component
  # virtual RTC::ReturnCode_t
  # onAddingComponent(RTC::LightweightRTObject_ptr rtobj)
  def onAddingComponent(self, rtobj):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onAddedComponent(RTC::LightweightRTObject_ptr rtobj)
  def onAddedComponent(self, rtobj):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onRemovingComponent(RTC::LightweightRTObject_ptr rtobj)
  def onRemovingComponent(self, rtobj):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onRemovedComponent(RTC::LightweightRTObject_ptr rtobj)
  def onRemovedComponent(self, rtobj):
    return RTC.RTC_OK

  # template virtual functions related to activation/deactivation/reset
  # virtual RTC::ReturnCode_t
  # onActivating(RTC::LightweightRTObject_ptr comp)
  def onActivating(self, comp):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onWaitingActivated(RTC_impl::RTObjectStateMachine* comp, long int count)
  def onWaitingActivated(self, comp, count):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onActivated(RTC_impl::RTObjectStateMachine* comp,
  #             long int count)
  def onActivated(self, comp, count):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onDeactivating(RTC::LightweightRTObject_ptr comp)
  def onDeactivating(self, comp):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onWaitingDeactivated(RTC_impl::RTObjectStateMachine* comp, long int count)
  def onWaitingDeactivated(self, comp, count):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onDeactivated(RTC_impl::RTObjectStateMachine* comp, long int count)
  def onDeactivated(self, comp, count):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t onResetting(RTC::LightweightRTObject_ptr comp)
  def onResetting(self, comp):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onWaitingReset(RTC_impl::RTObjectStateMachine* comp, long int count)
  def onWaitingReset(self, comp, count):
    return RTC.RTC_OK

  # virtual RTC::ReturnCode_t
  # onReset(RTC_impl::RTObjectStateMachine* comp, long int count)
  def onReset(self, comp, count):
    return RTC.RTC_OK

  # virtual RTC::LifeCycleState
  # onGetComponentState(RTC::LifeCycleState state)
  def onGetComponentState(self, state):
    return state

  # virtual RTC::ExecutionKind
  # onGetKind(RTC::ExecutionKind kind) const
  def onGetKind(self, kind):
    return kind

  # virtual RTC::ExecutionContextProfile*
  # onGetProfile(RTC::ExecutionContextProfile*& profile)
  def onGetProfile(self, profile):
    return profile


  #============================================================
  # private functions

  ##
  # @if jp
  # @brief Properties����¹ԥ���ƥ����Ȥ򥻥åȤ���
  # @else
  # @brief Setting execution rate from given properties.
  # @endif
  # bool ExecutionContextBase::setExecutionRate(coil::Properties& props)
  def setExecutionRate(self, props):
    if props.findNode("rate"):
      rate_ = [0.0]
      if OpenRTM_aist.stringTo(rate_, props.getProperty("rate")):
        self.setRate(rate_[0])
        return True
    return False

  
  ##
  # @if jp
  # @brief Properties����������ܥ⡼�ɤ򥻥åȤ���
  # @else
  # @brief Setting state transition mode from given properties.
  # @endif
  # bool ExecutionContextBase::
  # setTransitionMode(coil::Properties& props, const char* key, bool& flag)
  def setTransitionMode(self, props, key, flag):
    self._rtcout.RTC_TRACE("setTransitionMode(%s)", key)
    toSTR_ = lambda x: "YES" if x else "NO"
    if props.findNode(key):
      flag[0] = OpenRTM_aist.toBool(props.getProperty(key), "YES", "NO", "YES")
      self._rtcout.RTC_DEBUG("Transition Mode: %s = %s",
                             (key, toSTR_(flag[0])))
      return True

    self._rtcout.RTC_DEBUG("Configuration %s not found.", key)
    return False

  
  ##
  # @if jp
  # @brief Properties�����������Timeout�򥻥åȤ���
  # @else
  # @brief Setting state transition timeout from given properties.
  # @endif
  # bool ExecutionContextBase::
  # setTimeout(coil::Properties& props, const char* key,
  #            coil::TimeValue& timevalue)
  def setTimeout(self, props, key, timevalue):
    self._rtcout.RTC_TRACE("setTimeout(%s)", key)
    if props.findNode(key):
      timeout_ = [0.0]
      if OpenRTM_aist.stringTo(timeout_, props.getProperty(key)):
        timevalue[0] = OpenRTM_aist.TimeValue(timeout_[0])
        self._rtcout.RTC_DEBUG("Timeout (%s): %f [s]", (key, timeout_[0]))
        return True
    self._rtcout.RTC_DEBUG("Configuration %s not found.", key)
    return False


executioncontextfactory = None
  
class ExecutionContextFactory(OpenRTM_aist.Factory,ExecutionContextBase):
  def __init__(self):
    OpenRTM_aist.Factory.__init__(self)
    return

  def __del__(self):
    pass

  def instance():
    global executioncontextfactory

    if executioncontextfactory is None:
      executioncontextfactory = ExecutionContextFactory()

    return executioncontextfactory

  instance = staticmethod(instance)

