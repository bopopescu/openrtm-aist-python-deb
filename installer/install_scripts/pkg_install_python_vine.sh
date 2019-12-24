#!/bin/sh
#
# @file pkg_install_vine.sh
# @brief OpenRTM-aist dependent packages installation script for Vine Linux
# @author Noriaki Ando <n-ando@aist.go.jp>
#         Shinji Kurihara
#         Tetsuo Ando
#         Saburo Takahashi
#
# ���Υ����륹����ץȤϡ�ace�����omniORB�Υѥå������򥤥󥹥ȡ��뤷��
# Vine Linux�γ�ȯ�Ķ����ۤ��ޤ���
#
# Usage: sudo pkg_install_python_vine.sh [-u -y -h]
# option -u            : Uninstall tool_packages.
# option -y            : When yes/no prompt for installing would be presente    d, assume that the user entered "yes".
# option -h            : Display a brief help message.
#

#---------------------------------------
# Vine�С����������
#---------------------------------------
vinever=`cat /etc/vine-release | sed 's/.*\([0-9].[0-9]\).*/\1/'`

#---------------------------------------
# ��ݥ��ȥꥵ����
#---------------------------------------
openrtm_repo="rpm     http://www.openrtm.org/pub/Linux/Vine/apt $vinever/\$(ARCH) main"

#---------------------------------------
# �ѥå������ꥹ��
#---------------------------------------
omnipy="python omniORB-servers omniORBpy omniORBpy-devel omniORBpy-standard"
openrtm="OpenRTM-aist-Python OpenRTM-aist-Python-example"
packages="$omnipy $openrtm"




#----------------------------------------
# root ���ɤ���������å�
#----------------------------------------
check_root () {
    if test ! `id -u` = 0 ; then
	echo ""
	echo "This script should be run by root user."
	echo "Abort."
	echo ""
	exit 1
    fi
}

#---------------------------------------
# �������ꥹ�ȹ����ؿ������
#---------------------------------------
update_source_list () {
    rtmsite=`grep openrtm /etc/apt/sources.list`
    if test "x$rtmsite" = "x" ; then
	echo "OpenRTM-aist �Υ�ݥ��ȥ꤬��Ͽ����Ƥ��ޤ���"
	echo "Source.list �� OpenRTM-aist �Υ�ݥ��ȥ�: "
	echo "  " $openrtm_repo
	read -p "���ɲä��ޤ���������Ǥ����� (y/n) [y] " kick_shell

	if test "x$kick_shell" = "xn" ; then
	    echo "���Ǥ��ޤ���"
	    exit 0
	else
	    echo $openrtm_repo >> /etc/apt/sources.list
	fi
    fi
}

#----------------------------------------
# �ѥå������򥤥󥹥ȡ��뤹��
#----------------------------------------
install_packages () {
    for p in $*; do
	if test "x$p" = "x0.4.2" ; then
	    :
	else
	    if echo "$p" | grep -q '=0.4.2' ; then
		str=`echo "$p" |sed 's/=0.4.2//'`
	    else
		str="$p"
	    fi

	    ins=`rpm -qa $str`

	    if test "x$ins" = "x"; then
		echo "Now installing: " $p
		apt-get install $p $force_yes
		echo "done."
		echo ""
	    else
		if echo "$ins" |grep -q '0.4.2-0' ; then
			apt-get install $p $force_yes
			echo "done."
			echo ""
	       else
 		    echo $ins
		    echo $str "is already installed."
		    echo ""
		fi
	    fi
	fi
    done
}


#------------------------------------------------------------
# �ꥹ�Ȥ�ս�ˤ���
#------------------------------------------------------------
reverse () {
    for i in $*; do
	echo $i
    done | sed '1!G;h;$!d'
}

#----------------------------------------
# �ѥå������򥢥󥤥󥹥ȡ��뤹��
#----------------------------------------
uninstall_packages () {
    for p in $*; do
	echo "Now uninstalling: " $p
	rpm -e $p
	echo "done."
	echo ""
    done
}

#---------------------------------------
# USAGE
#---------------------------------------
howto_usage(){
    cat << EOF
Usage: sudo $0 [-u -y -h]
       option -u            : Uninstall tool_packages.
       option -y            : When yes/no prompt for installing would be presented, assume that the user entered "yes".
       option -h            : Display a brief help message.
EOF
}

#---------------------------------------
# �ᥤ��
#---------------------------------------
if test "x$1" = "x-h" ; then
    howto_usage
    exit 1
fi

check_root

if test "x$1" = "x-y" ; then
    force_yes="-y --force-yes"
fi

if test "x$1" = "x-u" ; then
    uninstall_packages `reverse $packages`
else
    update_source_list
    apt-get update
    install_packages $packages
fi

