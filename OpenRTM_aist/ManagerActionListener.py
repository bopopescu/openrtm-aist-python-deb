#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ManagerActionListener.py
# @brief component action listener class
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

import OpenRTM_aist

##
# @if jp
# @class ManagerActionListenerHolder ���饹
# @else
# @class ManagerActionListenerHolder class
# @endif
class ManagerActionListenerHolder(OpenRTM_aist.ListenerHolder):
  """
  """
  
  def __init__(self):
    OpenRTM_aist.ListenerHolder.__init__(self)
    return

  def __del__(self):
    return


  ##
  # @if jp
  # @brief preShutdown ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preShutdown callback function
  # TODO: Documentation
  # @endif
  # virtual void preShutdown();
  def preShutdown(self):
    self.LISTENERHOLDER_CALLBACK("preShutdown")
    return


  ##
  # @if jp
  # @brief postShutdown ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postShutdown callback function
  # TODO: Documentation
  # @endif
  # virtual void postShutdown();
  def postShutdown(self):
    self.LISTENERHOLDER_CALLBACK("postShutdown")
    return


  ##
  # @if jp
  # @brief preReinit ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preReinit callback function
  # TODO: Documentation
  # @endif
  # virtual void preReinit();
  def preReinit(self):
    self.LISTENERHOLDER_CALLBACK("preReinit")
    return


  ##
  # @if jp
  # @brief postReinit ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postReinit callback function
  # TODO: Documentation
  # @endif
  # virtual void postReinit();
  def postReinit(self):
    self.LISTENERHOLDER_CALLBACK("postReinit")
    return
  
  
##
# @if jp
# @class ModuleActionListenerHolder ���饹
# @brief ModuleActionListenerHolder ���饹
#
# @else
# @class ModuleActionListenerHolder class
# @brief ModuleActionListenerHolder class
#
# @endif
class ModuleActionListenerHolder(OpenRTM_aist.ListenerHolder):
  """
  """

  def __init__(self):
    OpenRTM_aist.ListenerHolder.__init__(self)
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    pass
    

  ##
  # @if jp
  # @brief preLoad ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preLoad callback function
  # TODO: Documentation
  # @endif
  # virtual void preLoad(std::string& modname,
  #                      std::string& funcname);
  def preLoad(self, modname, funcname):
    self.LISTENERHOLDER_CALLBACK("preLoad", modname, funcname)
    return

    
  ##
  # @if jp
  # @brief postLoad ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postLoad callback function
  # TODO: Documentation
  # @endif
  # virtual void postLoad(std::string& modname,
  #                       std::string& funcname);
  def postLoad(self, modname, funcname):
    self.LISTENERHOLDER_CALLBACK("postLoad", modname, funcname)
    return
    

  ##
  # @if jp
  # @brief preUnload ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preUnload callback function
  # TODO: Documentation
  # @endif
  # virtual void preUnload(std::string& modname);
  def preUnload(self, modname):
    self.LISTENERHOLDER_CALLBACK("preUnload", modname)
    return
    

  ##
  # @if jp
  # @brief postUnload ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postUnload callback function
  # TODO: Documentation
  # @endif
  # virtual void postUnload(std::string& modname);
  def postUnload(self, modname):
    self.LISTENERHOLDER_CALLBACK("postUnload", modname)
    return
  
  

##
# @if jp
# @class RtcLifecycleActionListenerHolder ���饹
# @brief RtcLifecycleActionListenerHolder ���饹
#
# @else
# @class RtcLifecycleActionListenerHolder class
# @brief RtcLifecycleActionListenerHolder class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in rtobject.
#
# @endif
class RtcLifecycleActionListenerHolder(OpenRTM_aist.ListenerHolder):
  """
  """

  def __init__(self):
    OpenRTM_aist.ListenerHolder.__init__(self)
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    pass
    
    
  ##
  # @if jp
  # @brief preCreate ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preCreate callback function
  # TODO: Documentation
  # @endif
  # virtual void preCreate(std::string& args);
  def preCreate(self, args):
    self.LISTENERHOLDER_CALLBACK("preCreate", args)
    return
    

  ##
  # @if jp
  # @brief postCreate ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postCreate callback function
  # TODO: Documentation
  # @endif
  # virtual void postCreate(RTC::RTObject_impl* rtobj);
  def postCreate(self, rtobj):
    self.LISTENERHOLDER_CALLBACK("postCreate", rtobj)
    return
     

  ##
  # @if jp
  # @brief preConfigure ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preConfigure callback function
  # TODO: Documentation
  # @endif
  # virtual void preConfigure(coil::Properties& prop);
  def preConfigure(self, prop):
    self.LISTENERHOLDER_CALLBACK("preConfigure", prop)
    return
    

  ##
  # @if jp
  # @brief postConfigure ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postConfigure callback function
  # TODO: Documentation
  # @endif
  # virtual void postConfigure(coil::Properties& prop);
  def postConfigure(self, prop):
    self.LISTENERHOLDER_CALLBACK("postConfigure", prop)
    return
    

  ##
  # @if jp
  # @brief preInitialize ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preInitialize callback function
  # TODO: Documentation
  # @endif
  # virtual void preInitialize(void);
  def preInitialize(self):
    self.LISTENERHOLDER_CALLBACK("preInitialize")
    return
    

  ##
  # @if jp
  # @brief postInitialize ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postInitialize callback function
  # TODO: Documentation
  # @endif
  # virtual void postInitialize(void);
  def postInitialize(self):
    self.LISTENERHOLDER_CALLBACK("postInitialize")
    return



##
# @if jp
# @class NamingActionListenerHolder ���饹
# @brief NamingActionListenerHolder ���饹
#
# @else
# @class NamingActionListenerHolder class
# @brief NamingActionListenerHolder class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in rtobject.
#
# @endif
class NamingActionListenerHolder(OpenRTM_aist.ListenerHolder):
  """
  """

  def __init__(self):
    OpenRTM_aist.ListenerHolder.__init__(self)
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    pass
    

  ##
  # @if jp
  # @brief preBind ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preBind callback function
  # TODO: Documentation
  # @endif
  # virtual void preBind(RTC::RTObject_impl# rtobj,
  #                      coil::vstring& name);
  def preBind(self, rtobj, name):
    self.LISTENERHOLDER_CALLBACK("preBind", rtobj, name)
    return


  ##
  # @if jp
  # @brief postBind ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postBind callback function
  # TODO: Documentation
  # @endif
  # virtual void postBind(RTC::RTObject_impl* rtobj,
  #                       coil::vstring& name);
  def postBind(self, rtobj, name):
    self.LISTENERHOLDER_CALLBACK("postBind", rtobj, name)
    return
    

  ##
  # @if jp
  # @brief preUnbind ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preUnbind callback function
  # TODO: Documentation
  # @endif
  # virtual void preUnbind(RTC::RTObject_impl* rtobj,
  #                        coil::vstring& name);
  def preUnbind(self, rtobj, name):
    self.LISTENERHOLDER_CALLBACK("preUnbind", rtobj, name)
    return
    

  ##
  # @if jp
  # @brief postUnbind ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postUnbind callback function
  # TODO: Documentation
  # @endif
  # virtual void postUnbind(RTC::RTObject_impl* rtobj,
  #                         coil::vstring& name);
  def postUnbind(self, rtobj, name):
    self.LISTENERHOLDER_CALLBACK("postUnbind", rtobj, name)
    return
  
  
  
##
# @if jp
# @class LocalServiceActionListenerHolder ���饹
# @brief LocalServiceActionListenerHolder ���饹
#
# �ƥ����������б�����桼���������ɤ��ƤФ��ľ���Υ����ߥ�
# �ǥ����뤵���ꥹ�ʥ��饹�δ��쥯�饹��
#
# - ADD_PORT:
# - REMOVE_PORT:
#
# @else
# @class LocalServiceActionListenerHolder class
# @brief LocalServiceActionListenerHolder class
#
# This class is abstract base class for listener classes that
# provides callbacks for various events in rtobject.
#
# @endif
class LocalServiceActionListenerHolder(OpenRTM_aist.ListenerHolder):
  """
  """

  def __init__(self):
    OpenRTM_aist.ListenerHolder.__init__(self)
    return


  ##
  # @if jp
  # @brief �ǥ��ȥ饯��
  # @else
  # @brief Destructor
  # @endif
  def __del__(self):
    pass
    

  # registration instance of service to svc admin
  ##
  # @if jp
  # @brief preServiceRegister ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preServiceRegister callback function
  # TODO: Documentation
  # @endif
  # virtual void preServiceRegister(std::string service_name);
  def preServiceRegister(self, service_name):
    self.LISTENERHOLDER_CALLBACK("preServiceRegister", service_name)
    return
    

  ##
  # @if jp
  # @brief postServiceRegister ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postServiceRegister callback function
  # TODO: Documentation
  # @endif
  # virtual void postServiceRegister(std::string service_name,
  #                                  RTM::LocalServiceBase* service);
  def postServiceRegister(self, service_name, service):
    self.LISTENERHOLDER_CALLBACK("postServiceRegister", service_name, service)
    return
    

  ##
  # @if jp
  # @brief preServiceInit ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preServiceInit callback function
  # TODO: Documentation
  # @endif
  # virtual void preServiceInit(coil::Properties& prop,
  #                             RTM::LocalServiceBase* service);
  def preServiceInit(self, prop, service):
    self.LISTENERHOLDER_CALLBACK("preServiceInit", prop, service)
    return


  ##
  # @if jp
  # @brief postServiceInit ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postServiceInit callback function
  # TODO: Documentation
  # @endif
  # virtual void postServiceInit(coil::Properties& prop,
  #                              RTM::LocalServiceBase* service);
  def postServiceInit(self, prop, service):
    self.LISTENERHOLDER_CALLBACK("postServiceInit", prop, service)
    return
    

  ##
  # @if jp
  # @brief preServiceReinit ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preServiceReinit callback function
  # TODO: Documentation
  # @endif
  # virtual void preServiceReinit(coil::Properties& prop,
  #                               RTM::LocalServiceBase* service);
  def preServiceReinit(self, prop, service):
    self.LISTENERHOLDER_CALLBACK("preServiceReinit", prop, service)
    return


  ##
  # @if jp
  # @brief postServiceReinit ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postServiceReinit callback function
  # TODO: Documentation
  # @endif
  # virtual void postServiceReinit(coil::Properties& prop,
  #                                RTM::LocalServiceBase* service);
  def postServiceReinit(self, prop, service):
    self.LISTENERHOLDER_CALLBACK("postServiceReinit", prop, service)
    return


  ##
  # @if jp
  # @brief preServiceFinalize ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief preServiceFinalize callback function
  # TODO: Documentation
  # @endif
  # virtual void preServiceFinalize(std::string service_name,
  #                                 RTM::LocalServiceBase* service);
  def preServiceFinalize(self, service_name, service):
    self.LISTENERHOLDER_CALLBACK("preServiceFinalize", service_name, service)
    return


  ##
  # @if jp
  # @brief postServiceFinalize ������Хå��ؿ�
  # TODO: Documentation
  # @else
  # @brief postServiceFinalize callback function
  # TODO: Documentation
  # @endif
  # virtual void postServiceFinalize(std::string service_name,
  #                                  RTM::LocalServiceBase* service);
  def postServiceFinalize(self, service_name, service):
    self.LISTENERHOLDER_CALLBACK("postServiceFinalize", service_name, service)
    return

  
  
  
##
# @if jp
# @class ManagerActionListeners
# @brief ManagerActionListeners ���饹
#
#
# @else
# @class ManagerActionListeners
# @brief ManagerActionListeners class
#
#
# @endif
class ManagerActionListeners:
  """
  """

  def __init__(self):
    self.manager_      = ManagerActionListenerHolder()
    self.module_       = ModuleActionListenerHolder() 
    self.rtclifecycle_ = RtcLifecycleActionListenerHolder()
    self.naming_       = NamingActionListenerHolder()
    self.localservice_ = LocalServiceActionListenerHolder()

