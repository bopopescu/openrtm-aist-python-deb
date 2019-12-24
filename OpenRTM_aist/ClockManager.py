#!/usr/bin/env python
# -*- coding: euc-jp -*-

##
# @file ClockManager.py
# @brief Global clock management class
# @date $Date$
# @author Noriaki Ando <n-ando@aist.go.jp>
#
# Copyright (C) 2012
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
# @class �������ꡦ�������֥������ȤΥ��󥿡��ե�����
#
# ���Υ��饹�� ClockManager �ˤ�äƴ�������륯��å����֥������Ȥ�
# ����Υ��󥿡��ե������Ǥ��롣ClockManager ��ʣ���Υ���å����֥���
# ���Ȥ��������ɬ�פ˱�����Ŭ�ڤʥ���å����֥������Ȥ� IClock ����
# �����ե��������ĥ��֥������ȤȤ����֤�������å����֥������Ȥ�ñ
# �˥����ƥ������֤���Τ䡢�ȼ��������������ĥ���å����֥�����
# �������ͤ����롣
#
# @else
# @brief An interface to set and get time
#
# This class is a interface for clock objects managed by
# ClockManager. ClockManager manages one or more clocks, and it
# returns appropriate clock objects according to demands. The clock
# object might be clock which just returns system time, or a clock
# which returns individual logical time.
#
# @endif
class IClock:
  """
  """

  ##
  # @if jp
  # @brief ������������
  # @return ���ߤλ���
  # @else
  # @brief Getting time
  # @return Current time
  # @endif
  # virtual coil::TimeValue gettime() const = 0;
  def gettime(self):
    pass


  ##
  # @if jp
  # @brief ��������ꤹ��
  # @param clocktime ���ߤλ���
  # @else
  # @brief Setting time
  # @param clocktime Current time
  # @endif
  # virtual bool settime(coil::TimeValue clocktime) = 0;
  def settime(self, clocktime):
    pass


##
# @if jp
# @class �����ƥ����򰷤�����å����֥�������
#
# ���Υ��饹�ϥ����ƥ९��å�������ޤ��ϼ������륯�饹�Ǥ��롣
#
# @else
# @brief clock object to handle system clock
#
# This class sets and gets system clock.
#
# @endif
class SystemClock(IClock):
  """
  """

  # virtual coil::TimeValue gettime() const;
  def gettime(self):
    return OpenRTM_aist.Time().getTime()

  # virtual bool settime(coil::TimeValue clocktime);
  def settime(self, clocktime):
    return OpenRTM_aist.Time().settimeofday(clocktime, 0)


##
# @if jp
# @class �������֤򰷤�����å����֥�������
#
# ���Υ��饹���������֤�����ޤ��ϼ������륯�饹�Ǥ��롣
# ñ��� settime() �ˤ�ä����ꤵ�줿����� gettime() �ˤ�äƼ������롣
#
# @else
# @brief Clock object to handle logical clock
#
# This class sets and gets system clock.
# It just sets time by settime() and gets time by gettime().
#
# @endif
class LogicalClock(IClock):
  """
  """

  def __init__(self):
    self._currentTime = OpenRTM_aist.TimeValue(0.0)
    self._currentTimeMutex = threading.RLock()
    return

  # virtual coil::TimeValue gettime() const;
  def gettime(self):
    guard = OpenRTM_aist.ScopedLock(self._currentTimeMutex)
    return self._currentTime

  # virtual bool settime(coil::TimeValue clocktime);
  def settime(self, clocktime):
    guard = OpenRTM_aist.ScopedLock(self._currentTimeMutex)
    self._currentTime = clocktime
    return True
    

##
# @if jp
# @class Ĵ���Ѥ߻���򰷤�����å����֥�������
#
# settime() �ƤӽФ����˸��߻���Ȥκ��򥪥ե��åȤȤ����ݻ�����
# gettime() �ˤ�äƥ��ե��å�Ĵ���Ѥߤλ�����֤���
#
# @else
# @brief Clock object to handle adjusted clock
#
# This class stores a offset time with current system clock when
# settime(), and gettime() returns adjusted clock by the offset.
#
# @endif
class AdjustedClock(IClock):
  """
  """

  def __init__(self):
    self._offset = OpenRTM_aist.TimeValue(0.0)
    self._offsetMutex = threading.RLock()
    return


  # virtual coil::TimeValue gettime() const;
  def gettime(self):
    guard = OpenRTM_aist.ScopedLock(self._offsetMutex)
    return OpenRTM_aist.Time().getTime() - self._offset
    
  # virtual bool settime(coil::TimeValue clocktime);
  def settime(self, clocktime):
    guard = OpenRTM_aist.ScopedLock(self._offsetMutex)
    self._offset = OpenRTM_aist.Time().getTime() - clocktime
    return True

clockmgr = None
clockmgr_mutex = threading.RLock()

##
# @if jp
# @class �����Х�ʥ���å��������饹��
#
# ���Υ��饹�ϥ����Х�˥���å����֥������Ȥ��󶡤��륷�󥰥�ȥ�
# ���饹�Ǥ��롣getClocK(����å�̾) �ˤ�� IClock ���Υ���å�����
# �������Ȥ��֤������Ѳ�ǽ�ʥ���å��� "system", "logical" �����
# "adjusted" �Σ�����Ǥ��롣
#
# @else
# @brief A global clock management class
#
# This class is a singleton class that provides clock objects
# globally. It provides a IClock object by getClock(<clock
# type>). As clock types, "system", "logical" and "adjusted" are
# available.
#
# @endif
class ClockManager:
  """
  """
  
  def __init__(self):
    self._systemClock   = SystemClock()
    self._logicalClock  = LogicalClock()
    self._adjustedClock = AdjustedClock()
    return

  def getClock(self, clocktype):
    if clocktype == "logical":
      return self._logicalClock
    elif clocktype == "adjusted":
      return self._adjustedClock
    elif clocktype == "system":
      return self._systemClock

    return self._systemClock

  def instance():
    global clockmgr
    global clockmgr_mutex

    if not clockmgr:
      guard = OpenRTM_aist.ScopedLock(clockmgr_mutex)
      clockmgr = ClockManager()

    return clockmgr
  instance = staticmethod(instance)

