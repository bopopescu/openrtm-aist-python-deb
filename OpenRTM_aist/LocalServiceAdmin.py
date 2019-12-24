#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file LocalServiceAdmin.py
# @brief SDO service administration class
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

import threading
import OpenRTM_aist

localserviceadmin = None
services_mutex = threading.RLock()

##
# @if jp
#
# @class LocalService administration class
# @brief LocalService �������饹
#
# TODO: Documentation
#
# @since 1.1.0
#
#
# @else
#
# @class SDO service administration class
# @brief SDO service administration class
#
# TODO: Documentation
#
# @since 1.1.0
#
# @endif
class LocalServiceAdmin:
  """
  """

  ##
  # @if jp
  #
  # @brief ���󥹥ȥ饯��
  # 
  # ���󥹥ȥ饯��
  #
  # @else
  #
  # @brief Constructor
  # 
  # Constructor
  #
  # @endif
  def __init__(self):
    self._services = []
    self._rtcout = OpenRTM_aist.Manager.instance().getLogbuf("LocalServiceAdmin")
    self._rtcout.RTC_TRACE("LocalServiceAdmin.__init__()")
    self._factory = OpenRTM_aist.LocalServiceFactory.instance()
    return


  def __del__(self):
    self.finalize()
    return


  ##
  # @if jp
  #
  # @brief LocaServiceAdmin�ν����
  #
  # TODO: Documentation
  #
  # @else
  #
  # @brief Initialization of LocalServiceAdmin
  #
  # TODO: Documentation
  #
  # @endif
  # void init(coil::Properties& props);
  def init(self, props):
    self._rtcout.RTC_TRACE("LocalServiceAdmin.init()")
    svcs_ = props.getProperty("enabled_services").split(",")
    svcs_lower_ = [s.lower() for s in svcs_]
    all_enable_ = False
    if "all" in svcs_lower_:
      self._rtcout.RTC_INFO("All the local services are enabled.")
      all_enable_ = True
    
    ids_ = self._factory.getIdentifiers()
    self._rtcout.RTC_DEBUG("Available services: %s", OpenRTM_aist.flatten(ids_))
    for id_ in ids_:
      if all_enable_ or self.isEnabled(id_, svcs_):
        if self.notExisting(id_):
          service_ = self._factory.createObject(id_)
          self._rtcout.RTC_DEBUG("Service created: %s", id_)
          prop_ = props.getNode(id_)
          service_.init(prop_)
          self.addLocalService(service_)
    return
    

  ##
  # @if jp
  #
  # @brief LocalserviceAdmin �ν�λ����
  #
  # TODO: Documentation
  #
  # @else
  #
  # @brief Finalization ofLocalServiceAdmin
  #
  # TODO: Documentation
  #
  # @endif
  # void finalize();
  def finalize(self):
    for svc_ in self._services:
      svc_.finalize()
      self._factory.deleteObject(svc_)
    self._services = []

    return
    

  ##
  # @if jp
  #
  # @brief LocalServiceProfileList�μ���
  # 
  # TODO: Documentation
  #
  # @else
  #
  # @brief Getting LocalServiceProfileList
  #
  # TODO: Documentation
  #
  # @endif
  # ::RTM::LocalServiceProfileList getServiceProfiles();
  def getServiceProfiles(self):
    profs_ = []
    for svc_ in self._services:
      profs_.append(svc_.getProfile())
    return profs_
    

  ##
  # @if jp
  #
  # @brief LocalServiceProfile ���������
  #
  # id �ǻ��ꤵ�줿ID�����LocalService ��
  # LocalServiceProfile ��������롣id �� NULL �ݥ��󥿤ξ�硢���ꤵ�줿
  # id �˳�������ServiceProfile ��¸�ߤ��ʤ���硢false���֤���
  #
  # @param id LocalService �� IFR ID
  # @return ���ꤵ�줿 id ����� LocalServiceProfile
  # 
  # @else
  #
  # @brief Get LocalServiceProfile of an LocalService
  #
  # This operation returns LocalServiceProfile of a LocalService
  # which has the specified id. If the specified id is
  # NULL pointer or the specified id does not exist in the
  # ServiceProfile list, false will be returned.
  #
  # @param id ID of an LocalService
  # @return LocalServiceProfile which has the specified id
  #
  # @endif
  # bool getServiceProfile(std::string name,
  #                        ::RTM::LocalServiceProfile& prof);
  def getServiceProfile(self, name, prof):
    global services_mutex
    guard_ = OpenRTM_aist.ScopedLock(services_mutex)
    for svc_ in self._services:
      if name == svc_.getProfile().name:
        prof[0] = svc_.getProfile()
        del guard_
        return True
    del guard_
    return False
    

  ##
  # @if jp
  #
  # @brief LocalService �� Service ���������
  #
  # id �ǻ��ꤵ�줿ID�����LocalService �Υݥ��󥿤�������롣id ��
  # NULL �ݥ��󥿤ξ�硢���ꤵ�줿 id �˳�������ServiceProfile ��¸
  # �ߤ��ʤ���硢NULL���֤���
  #
  # @param id LocalService �� ID
  # @return ���ꤵ�줿 id ����� LocalService �Υݥ���
  # 
  # @else
  #
  # @brief Get a pointer of a LocalService
  #
  # This operation returnes a pointer to the LocalService
  # which has the specified id. If the specified id is
  # NULL pointer or the specified id does not exist in the
  # ServiceProfile list, NULL pointer will be returned.
  #
  # @param id ID of a LocalService
  # @return a pointer which has the specified id
  #
  # @endif
  # ::RTM::LocalServiceBase* getService(const char* id);
  def getService(self, id):
    for svc_ in self._services:
      if svc_.getProfile().name == id:
        return svc_
    return None
    

  ##
  # @if jp
  # @brief SDO service provider �򥻥åȤ���
  #
  # TODO: Documentation
  # 
  # @else
  # @brief Set a SDO service provider
  #
  # TODO: Documentation
  #
  # @endif
  # bool addLocalService(::RTM::LocalServiceBase* service);
  def addLocalService(self, service):
    global services_mutex
    if not service:
      self._rtcout.RTC_ERROR("Invalid argument: addLocalService(service == NULL)")
      return False
    self._rtcout.RTC_TRACE("LocalServiceAdmin.addLocalService(%s)",
                           service.getProfile().name)
    guard_ = OpenRTM_aist.ScopedLock(services_mutex)
    self._services.append(service)
    del guard_
    return True
    

  ##
  # @if jp
  # @brief LocalService ��������
  #
  # TODO: Documentation
  #
  # @else
  # @brief Remove a LocalService
  #
  # TODO: Documentation
  #
  # @endif
  # bool removeLocalService(const std::string name);
  def removeLocalService(self, name):
    global services_mutex
    self._rtcout.RTC_TRACE("removeLocalService(%s)", name)
    guard_ = OpenRTM_aist.ScopedLock(services_mutex)

    for (i,svc_) in enumerate(self._services):
      if name == svc_.getProfile().name:
        svc_.finalize()
        self._factory.deleteObject(svc_)
        del self._services[i]
        self._rtcout.RTC_INFO("SDO service  has been deleted: %s", name)
        del guard_
        return True;
    self._rtcout.RTC_WARN("Specified SDO service  not found: %s", name)
    del guard_
    return False

    
  ##
  # @if jp
  # @brief ���ꤵ�줿ID��ͭ�����ɤ��������å�����
  # @else
  # @brief Check if specified ID is enabled
  # @endif
  # bool isEnabled(const std::string& id, const coil::vstring& enabled);
  def isEnabled(self, id, enabled):
    if id in enabled:
      self._rtcout.RTC_DEBUG("Local service %s is enabled.", id)
      return True
    self._rtcout.RTC_DEBUG("Local service %s is not enabled.", id)
    return False
    

  ##
  # @if jp
  # @brief ���ꤵ�줿ID�����Ǥ�¸�ߤ��뤫�ɤ��������å�����
  # @else
  # @brief Check if specified ID is existing
  # @endif
  # bool notExisting(const std::string& id);
  def notExisting(self, id):
    for svc_ in self._services:
      if svc_.getProfile().name == id:
        self._rtcout.RTC_WARN("Local service %s already exists.", id)
        return False
    self._rtcout.RTC_DEBUG("Local service %s does not exist.", id)
    return True

  def instance():
    global localserviceadmin
    global services_mutex

    if localserviceadmin is None:
      guard_ = OpenRTM_aist.ScopedLock(services_mutex)
      if localserviceadmin is None:
        localserviceadmin = LocalServiceAdmin()
      del guard_
    return localserviceadmin
  
  instance = staticmethod(instance)
