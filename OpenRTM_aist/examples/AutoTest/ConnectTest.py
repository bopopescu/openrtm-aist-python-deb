#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

#
## ConnectTest.py
##
## �⎳�㎳���妾��妵��輧�����⎹��
##

from rtc_handle10_11 import *
from BasicDataType_idl import *
import time
import commands
import SDOPackage
import os
import sys

##--------------------------------------------------------------------
g_test_name = "<< component connection test >>"

## ��妾�㎠�⎵�㎼���妾��鎾��
#env = RtmEnv(sys.argv, ["localhost:2809"])
#list0 = env.name_space["localhost:2809"].list_obj()
#env.name_space['localhost:2809'].rtc_handles.keys()
#ns = env.name_space['localhost:2809']
env = RtmEnv(sys.argv, ["localhost:2809"])
list0 = env.name_space["localhost:2809"].list_obj()
env.name_space['localhost:2809'].rtc_handles.keys()
ns = env.name_space['localhost:2809']

g_compo_send = ns.rtc_handles["AutoTestOut0.rtc"]
g_compo_recv = ns.rtc_handles["AutoTestIn0.rtc"]

ec_send = g_compo_send.rtc_ref.get_owned_contexts()
ec_recv = g_compo_recv.rtc_ref.get_owned_contexts()

g_out_ports = g_compo_send.rtc_ref.get_ports()
g_in_ports = g_compo_recv.rtc_ref.get_ports()
#print "<<< g_out_ports.length=",len(g_out_ports)
#SeqOut�Ꭾꢎ����
#length=8 [0]:Short [1]:Long [2]:Float [3]:Double [4]:ShortSeq [5]:LongSeq [6]:FloatSeq [7]:DoubleSeq
#print "<<<  g_in_ports.length=",len(g_in_ports)

time.sleep(2)

##--------------------------------------------------------------------
## �⎳��失�⎿�㎼���妯���夣�⎤�㎫�����⎩�㎫��玮�鎾��
g_interface_type1 = "corba_cdr"
g_dataflow_type = "push"
g_subscription_type = "flush"
g_push_policy = "NEW"
g_push_rate = "2000"
g_skip_count = "4"
#g_skip_count = "0"

## ���妾���ʬ���玮� ( get_ports()���� )
g_port1 = 0
g_port2 = 1
g_port3 = 2

## ConnectorProfile(name, connector_id, ports, properties)
##   String name
##   String connector_id
##   RTC.PortService ports[]
##   SDOPackage.NameValue properties[]

## ��妾�⎿���妾�� TimedFloat
g_name1 = "out"
g_connector_id1 = "001"
g_data_type1 = "TimedFloat"

g_conprof1 = RTC.ConnectorProfile(g_name1, g_connector_id1, [g_out_ports[g_port1], g_in_ports[g_port1]], [SDOPackage.NameValue("dataport.data_type",any.to_any(g_data_type1)),SDOPackage.NameValue("dataport.interface_type",any.to_any(g_interface_type1)),SDOPackage.NameValue("dataport.dataflow_type",any.to_any(g_dataflow_type)),SDOPackage.NameValue("dataport.subscription_type",any.to_any(g_subscription_type)),SDOPackage.NameValue("dataport.publisher.push_policy",any.to_any(g_push_policy)),SDOPackage.NameValue("dataport.publisher.push_rate",any.to_any(g_push_rate)),SDOPackage.NameValue("dataport.publisher.skip_count",any.to_any(g_skip_count))])

## ��妾�⎿���妾�� TimedFloatSeq
g_name2 = "seqout"
g_connector_id2 = "002"
g_data_type2 = "TimedFloatSeq"

g_conprof2 = RTC.ConnectorProfile(g_name2, g_connector_id2, [g_out_ports[g_port2], g_in_ports[g_port2]], [SDOPackage.NameValue("dataport.data_type",any.to_any(g_data_type2)),SDOPackage.NameValue("dataport.interface_type",any.to_any(g_interface_type1)),SDOPackage.NameValue("dataport.dataflow_type",any.to_any(g_dataflow_type)),SDOPackage.NameValue("dataport.subscription_type",any.to_any(g_subscription_type)),SDOPackage.NameValue("dataport.publisher.push_policy",any.to_any(g_push_policy)),SDOPackage.NameValue("dataport.publisher.push_rate",any.to_any(g_push_rate)),SDOPackage.NameValue("dataport.publisher.skip_count",any.to_any(g_skip_count))])

## �⎵�㎼���夻���妾�� 
g_name3 = "MyService"
g_connector_id3 = "003"
g_interface_type3 = "MyService"

g_conprof3 = RTC.ConnectorProfile(g_name3, g_connector_id3, [g_out_ports[g_port3], g_in_ports[g_port3]], [SDOPackage.NameValue("dataport.interface_type",any.to_any(g_interface_type3))])

##--------------------------------------------------------------------
## �⎢���������ݘ�������Ύ��⼥
g_diff_send_file = "./original-data"
g_diff_recv_file = "./received-data"
g_check_message = g_diff_recv_file + " file not found."
g_test_result_file = "./ResultTest.log"
g_test_case = "case"
g_test_cnt = "count"
g_test_ok = "OK."
g_test_ng = "NG detected."
g_test_ng_message = "  < received-data >"
g_mess_header = "< "
g_mess_footer = " > "
# ��夻��鎵������玮��
# ���)�⎱�㎼�⎹1���1����ְ -> "<<< case1 count1 >>> OK."
# ���)�⎱�㎼�⎹1���2����ְ -> "<<< case1 count2 >>> NG detected."

##--------------------------------------------------------------------
## ��릪�����������夵��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚(��妾�⎿���妾��)
##
## (�����̎�)
## subscription_type : "flush", "new", "periodic"
## push_policy       : "ALL", "FIFO", "SKIP", "NEW", ""
## connect_direction : 0:outport -> inport, 1:inport -> outport
##--------------------------------------------------------------------
def make_connecter_profile(subscription_type, push_policy, connect_direction):
    global g_conprof1, g_conprof2, g_conprof3

    if connect_direction == 0:
        ## outport -> inport Set
        g_conprof1 = RTC.ConnectorProfile(g_name1, g_connector_id1, [g_out_ports[g_port1], g_in_ports[g_port1]], [SDOPackage.NameValue("dataport.data_type",any.to_any(g_data_type1)),SDOPackage.NameValue("dataport.interface_type",any.to_any(g_interface_type1)),SDOPackage.NameValue("dataport.dataflow_type",any.to_any(g_dataflow_type)),SDOPackage.NameValue("dataport.subscription_type",any.to_any(subscription_type)),SDOPackage.NameValue("dataport.publisher.push_policy",any.to_any(push_policy)),SDOPackage.NameValue("dataport.publisher.push_rate",any.to_any(g_push_rate)),SDOPackage.NameValue("dataport.publisher.skip_count",any.to_any(g_skip_count))])

        g_conprof2 = RTC.ConnectorProfile(g_name2, g_connector_id2, [g_out_ports[g_port2], g_in_ports[g_port2]], [SDOPackage.NameValue("dataport.data_type",any.to_any(g_data_type2)),SDOPackage.NameValue("dataport.interface_type",any.to_any(g_interface_type1)),SDOPackage.NameValue("dataport.dataflow_type",any.to_any(g_dataflow_type)),SDOPackage.NameValue("dataport.subscription_type",any.to_any(subscription_type)),SDOPackage.NameValue("dataport.publisher.push_policy",any.to_any(push_policy)),SDOPackage.NameValue("dataport.publisher.push_rate",any.to_any(g_push_rate)),SDOPackage.NameValue("dataport.publisher.skip_count",any.to_any(g_skip_count))])

        #print "outport -> inport set >>>"
        #print "g_conprof1=",g_conprof1
        #print "g_conprof2=",g_conprof2
    else:
        ## inport -> outport Set
        g_conprof1 = RTC.ConnectorProfile(g_name1, g_connector_id1, [g_in_ports[g_port1], g_out_ports[g_port1]], [SDOPackage.NameValue("dataport.data_type",any.to_any(g_data_type1)),SDOPackage.NameValue("dataport.interface_type",any.to_any(g_interface_type1)),SDOPackage.NameValue("dataport.dataflow_type",any.to_any(g_dataflow_type)),SDOPackage.NameValue("dataport.subscription_type",any.to_any(subscription_type)),SDOPackage.NameValue("dataport.publisher.push_policy",any.to_any(push_policy)),SDOPackage.NameValue("dataport.publisher.push_rate",any.to_any(g_push_rate)),SDOPackage.NameValue("dataport.publisher.skip_count",any.to_any(g_skip_count))])

        g_conprof2 = RTC.ConnectorProfile(g_name2, g_connector_id2, [g_in_ports[g_port2], g_out_ports[g_port2]], [SDOPackage.NameValue("dataport.data_type",any.to_any(g_data_type2)),SDOPackage.NameValue("dataport.interface_type",any.to_any(g_interface_type1)),SDOPackage.NameValue("dataport.dataflow_type",any.to_any(g_dataflow_type)),SDOPackage.NameValue("dataport.subscription_type",any.to_any(subscription_type)),SDOPackage.NameValue("dataport.publisher.push_policy",any.to_any(push_policy)),SDOPackage.NameValue("dataport.publisher.push_rate",any.to_any(g_push_rate)),SDOPackage.NameValue("dataport.publisher.skip_count",any.to_any(g_skip_count))])

        #print "inport -> outport set >>>"
        #print "g_conprof1=",g_conprof1
        #print "g_conprof2=",g_conprof2
    return


##--------------------------------------------------------------------
## ��릪��������������������夣�⎤�㎫���Ҧ
##
## (�����̎�)
## �Ꭺ��
##--------------------------------------------------------------------
def delete_recv_file():
    ## ���夣�⎤�㎫��玭��ت�����ꢎ����
    if os.path.isfile(g_diff_recv_file) == True:
        os.remove(g_diff_recv_file)
    return


##--------------------------------------------------------------------
## ��릪�����������뀢���������夣�⎤�㎫�Ꭾ��妾�⎿��ꎼ�
##
## (�����̎�)
## �Ꭺ��
## (�莻��瀎�)  True : 躀�玴���  False : 躺掸��玴
##--------------------------------------------------------------------
def diff_file():
    bret = True

    ## if connect_direction == 0:
    ## else:
    ## ��掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_send_file) == False:
        print "send_file (%s) not found." % send_file
        return False

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        print "recv_file (%s) not found." % recv_file
        return False

    ## ����������妾�⎿깎���簦갚
    f_send = open(g_diff_send_file, 'r')
    f_recv = open(g_diff_recv_file, 'r')

    while(1):
        str_send = f_send.readline()
        str_recv = f_recv.readline()
        if len(str_send) == 0:
            break

        #print "original send date=(%s)" % str_send
        #print ''.join(['%x ' % ord(s) for s in str_send])
        #print "original recv date=(%s)" % str_recv
        #print ''.join(['%x ' % ord(s) for s in str_recv])

        ## ����겎��Ꭾ���倢玾��꺎��⎳�㎼��������
        str_send2 = str_send.rstrip('\n')
        str_send2 = str_send2.rstrip('\r')
        str_recv2 = str_recv.rstrip('\n')
        str_recv2 = str_recv2.rstrip('\r')

        #print "rstrip after send date=(%s)" % str_send2
        #print "rstrip after recv date=(%s)" % str_recv2

        ## ��妾�⎿��ꎼ�
        if str_send2 != str_recv2:
            #print "data difference"
            #print "send date=(%s)" % str_send2
            #print "recv date=(%s)" % str_recv2
            bret = False
            break;

    f_recv.close()
    f_send.close()
    return bret

##--------------------------------------------------------------------
## ��夻��夳�㎼�⎹������Ꭾ����ء����𪎭갚
##  躴����뀎��������踱�Ꭳ�Ꭶ����
case_no = 0

## �⎱�㎼�⎹챼墰��夻���������
loop_count = 3

## ���掿���Ꮄactivate_component������掿���Ꮄactivate_component�Ꮎ�Ꭷ�Ꭾ�⎹�㎪�㎼���������(���ʲ)
sleep_recv_act_time = 1

## activate_component����deactivate_component�Ꮎ�Ꭷ�Ꭾ�⎹�㎪�㎼���������(���ʲ)
sleep_act_time = 10

## for�㎫�㎼���墰�⎹�㎪�㎼���������(���ʲ)
sleep_for_time = 2

## connect����disconnect�Ꮎ�Ꭷ�Ꭾ�⎹�㎪�㎼���������(���ʲ)
sleep_connect_time = 2

# ��夻��鎵�������夣�⎤�㎫�Ꭾ����
fout = open(g_test_result_file, 'w')
fout.write(g_test_name + '\n')
fout.close()
#print g_test_name

time.sleep(1)

##--------------------------------------------------------------------
## ������⎤������lush  ����������ut->in  ���妽���̯��夻��2
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, flush) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������lush  ����������n->out  ���妽���̯��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, flush) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������lush  ����������ut->in  Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(out->in, flush), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("flush", "", 0)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������lush  ����������n->out  Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(in->out, flush), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("flush", "", 1)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������lush  ����������ut->in  Activate�㎻Deactivate��夻��10
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Not Connect(out->in, flush), Activate -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 0)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������lush  ����������ut->in  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, flush) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������lush  ����������n->out  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, flush) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������lush  ����������ut->in  ���妽���̯�㎻Activate�㎻Deactivate��夻��2
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, flush) -> Activate -> send/recv -> Disconnect -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������lush  ����������n->out  ���妽���̯�㎻Activate�㎻Deactivate��夻��2
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, flush) -> Activate -> send/recv -> Disconnect -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)


##--------------------------------------------------------------------
## ������⎤������lush  ����������ut->in  ���妽���̯�㎻Activate�㎻Deactivate��夻��3
##--------------------------------------------------------------------
##  ���莳�����Ӣctivate������Ꭻ�墥�Ꭶ�����⎺����������妾�⎿�Ꭿ���掸�������Ꭾ��玮���Ꭻ�Ꭺ�������倂
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Activate -> Connect(out->in, flush) -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 0)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������lush  ����������n->out  ���妽���̯�㎻Activate�㎻Deactivate��夻��3
##--------------------------------------------------------------------
##  ���莳�����Ӣctivate������Ꭻ�墥�Ꭶ�����⎺����������妾�⎿�Ꭿ���掸�������Ꭾ��玮���Ꭻ�Ꭺ�������倂
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Activate -> Connect(in->out, flush) -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 1)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������lush  ����������ut->in  ���妽���̯�㎻Activate�㎻Deactivate��夻��4
##--------------------------------------------------------------------
##  ���莳�����Ӣctivate������Ꭻ�墥�Ꭶ�����⎺����������妾�⎿�Ꭿ���掸�������Ꭾ��玮���Ꭻ�Ꭺ�������倂
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Activate -> Connect(out->in, flush) -> send/recv -> Disconnect -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 0)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_act_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������lush  ����������n->out  ���妽���̯�㎻Activate�㎻Deactivate��夻��4
##--------------------------------------------------------------------
##  ���莳�����Ӣctivate������Ꭻ�墥�Ꭶ�����⎺����������妾�⎿�Ꭿ���掸�������Ꭾ��玮���Ꭻ�Ꭺ�������倂
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Activate -> Connect(in->out, flush) -> send/recv -> Disconnect -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("flush", "", 1)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_act_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӢLL  ���妽���̯��夻��3
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, new,ALL) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "ALL", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӧIFO  ���妽���̯��夻��4
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, new,FIFO) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "FIFO", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӯEW  ���妽���̯��夻��6
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, new,NEW) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "NEW", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӴKIP  ���妽���̯��夻��5
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, new,SKIP) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "SKIP", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӢLL  ���妽���̯��夻��3
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, new,ALL) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "ALL", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӧIFO  ���妽���̯��夻��4
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, new,FIFO) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "FIFO", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӯEW  ���妽���̯��夻��6
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, new,NEW) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "NEW", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӴKIP  ���妽���̯��夻��5
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, new,SKIP) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "SKIP", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӢLL  Activate�㎻Deactivate��夻��2
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(out->in, new,ALL), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("new", "ALL", 0)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӧIFO  Activate�㎻Deactivate��夻��3
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(out->in, new,FIFO), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("new", "FIFO", 0)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӯEW  Activate�㎻Deactivate��夻��5
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(out->in, new,NEW), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("new", "NEW", 0)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӴKIP  Activate�㎻Deactivate��夻��4
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(out->in, new,SKIP), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("new", "SKIP", 0)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӢLL  Activate�㎻Deactivate��夻��2
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(in->out, new,ALL), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("new", "ALL", 1)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӧIFO  Activate�㎻Deactivate��夻��3
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(in->out, new,FIFO), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("new", "FIFO", 1)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӯEW  Activate�㎻Deactivate��夻��5
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(in->out, new,NEW), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("new", "NEW", 1)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӴKIP  Activate�㎻Deactivate��夻��4
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(in->out, new,SKIP), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("new", "SKIP", 1)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӢLL  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, new,ALL) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "ALL", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӧIFO  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, new,FIFO) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "FIFO", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӯEW  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, new,NEW) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "NEW", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������ut->in  ���妬�⎷�㎼��ӴKIP  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, new,SKIP) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "SKIP", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӢLL  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, new,ALL) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "ALL", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӧIFO  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, new,FIFO) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "FIFO", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӯEW  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, new,NEW) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "NEW", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������ew  ����������n->out  ���妬�⎷�㎼��ӴKIP  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, new,SKIP) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("new", "SKIP", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӢLL  ���妽���̯��夻��7
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, periodic,ALL) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "ALL", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӧIFO  ���妽���̯��夻��8
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, periodic,FIFO) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "FIFO", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӯEW  ���妽���̯��夻��10
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, periodic,NEW) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "NEW", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӴKIP  ���妽���̯��夻��9
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, periodic,SKIP) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "SKIP", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӢLL  ���妽���̯��夻��7
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, periodic,ALL) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "ALL", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӧIFO  ���妽���̯��夻��8
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, periodic,FIFO) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "FIFO", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӯEW  ���妽���̯��夻��10
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, periodic,NEW) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "NEW", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӴKIP  ���妽���̯��夻��9
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, periodic,SKIP) -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "SKIP", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    time.sleep(sleep_connect_time)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ��夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    message = message + g_test_ok
    print message
    fout.write(message + '\n')
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӢLL    Activate�㎻Deactivate��夻��6
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(out->in, periodic,ALL), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("periodic", "ALL", 0)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӧIFO    Activate�㎻Deactivate��夻��7
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(out->in, periodic,FIFO), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("periodic", "FIFO", 0)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӯEW    Activate�㎻Deactivate��夻��9
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(out->in, periodic,NEW), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("periodic", "NEW", 0)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӴKIP    Activate�㎻Deactivate��夻��8
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(out->in, periodic,SKIP), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("periodic", "SKIP", 0)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӢLL    Activate�㎻Deactivate��夻��6
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(in->out, periodic,ALL), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("periodic", "ALL", 1)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӧIFO    Activate�㎻Deactivate��夻��7
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(in->out, periodic,FIFO), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("periodic", "FIFO", 1)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӯEW    Activate�㎻Deactivate��夻��9
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(in->out, periodic,NEW), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("periodic", "NEW", 1)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӴKIP    Activate�㎻Deactivate��夻��8
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connecting(in->out, periodic,SKIP), Activate -> send/recv -> Deactivate"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
make_connecter_profile("periodic", "SKIP", 1)

## 3 ���妾��輧
# ��妾�⎿���妾��1 TimedFloat
ret0 = g_out_ports[g_port1].connect(g_conprof1)

# ��妾�⎿���妾��2 TimedFloatSeq
ret1 = g_out_ports[g_port2].connect(g_conprof2)

# �⎵�㎼���夻���妾�� MyService
ret2 = g_out_ports[g_port3].connect(g_conprof3)

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

## 6 ���妾��������
g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӢLL  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, periodic,ALL) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "ALL", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӧIFO  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, periodic,FIFO) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "FIFO", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӯEW  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, periodic,NEW) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "NEW", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������ut->in  ���妬�⎷�㎼��ӴKIP  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(out->in, periodic,SKIP) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "SKIP", 0)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӢLL  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, periodic,ALL) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "ALL", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӧIFO  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, periodic,FIFO) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "FIFO", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӯEW  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, periodic,NEW) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "NEW", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

##--------------------------------------------------------------------
## ������⎤������eriodic  ����������n->out  ���妬�⎷�㎼��ӴKIP  ���妽���̯�㎻Activate�㎻Deactivate��夻��1
##--------------------------------------------------------------------
case_no = case_no + 1
fout = open(g_test_result_file, 'a')
message = g_mess_header + g_test_case + str(case_no) + " "
message = message + "Connect(in->out, periodic,SKIP) -> Activate -> send/recv -> Deactivate -> Disconnect"
message = message + g_mess_footer
fout.write(message + '\n')
fout.close()
print message

for i in range(loop_count):

    ## 2 ���掿����妾�⎿���夣�⎤�㎫���Ҧ
    delete_recv_file()

    ## 1 �⎳��失�⎿�㎼���妯���夣�⎤�㎫𪎭갚
    make_connecter_profile("periodic", "SKIP", 1)

    ## 3 ���妾��輧
    # ��妾�⎿���妾��1 TimedFloat
    ret0 = g_out_ports[g_port1].connect(g_conprof1)

    # ��妾�⎿���妾��2 TimedFloatSeq
    ret1 = g_out_ports[g_port2].connect(g_conprof2)

    # �⎵�㎼���夻���妾�� MyService
    ret2 = g_out_ports[g_port3].connect(g_conprof3)

    ## 4 �⎢�⎯��夥���妾��
    ec_recv[0].activate_component(g_compo_recv.rtc_ref)
    time.sleep(sleep_recv_act_time)
    ec_send[0].activate_component(g_compo_send.rtc_ref)

    time.sleep(sleep_act_time)

    ## 5 ��夥�⎢�⎯��夥���妾��
    ec_send[0].deactivate_component(g_compo_send.rtc_ref)
    ec_recv[0].deactivate_component(g_compo_recv.rtc_ref)

    ## 6 ���妾��������
    g_in_ports[g_port3].disconnect(g_conprof3.connector_id)
    g_in_ports[g_port2].disconnect(g_conprof2.connector_id)
    g_in_ports[g_port1].disconnect(g_conprof1.connector_id)

    ## ���掿�����夣�⎤�㎫���騣�莤갚
    if os.path.isfile(g_diff_recv_file) == False:
        fout = open(g_test_result_file, 'a')
        message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
        message = message + g_check_message
        fout.write(message + '\n')
        fout.close()
        print message
        time.sleep(sleep_for_time)
        continue

    ## 7 ����������妾�⎿��ꎼ�
    time.sleep(sleep_act_time)
    bret = diff_file()

    ## 깎������⎡�⎤�㎫������夻��鎵�����玺��
    fout = open(g_test_result_file, 'a')
    message = g_mess_header + g_test_case + str(case_no) + " " + g_test_cnt + str(i+1) + g_mess_footer
    # bret==True �Ꭺ��뀢��������妾�⎿躀�玴
    if bret == True:
        # ��夻��鎵���� OK
        message = message + g_test_ok
        print message
        fout.write(message + '\n')
    else:
        # ��夻��鎵���� NG
        message = message + g_test_ng
        print message
        message = message + g_test_ng_message
        fout.write(message + '\n')
        # ���掿����妾�⎿������⎹��鎵�������夣�⎤�㎫�Ꮈ�⎳���妾
        fin2 = open(g_diff_recv_file, 'r')
        while(1):
            s2 = fin2.readline()
            if len(s2) == 0:
                break
            fout.write(s2)
        fin2.close()
    fout.close()

    time.sleep(sleep_for_time)

print "Test Complete."
