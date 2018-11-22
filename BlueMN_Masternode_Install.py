#!/usr/bin/env python
# coding:utf-8

"""
需求：

1、初始化linux环境
2、安装和配置钱包masternode

3、日常监控运行masternode状态，推送状态到服务器（任务）
4、添加新钱包，删除钱包，查看钱包

"""

import argparse
import subprocess
import os
import time
import sys
import socket
import copy
import commands
import json
import datetime
import os


print("install pip and python lib...")
ret = subprocess.call(
    ['apt-get install python-pip python-requests python-virtualenv unzip libzmq3-dev  -y'], shell=True)

import requests
import pickle


############
###全局变量##
############


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


APP_VERSION = "1.0"
GET_CONF_API_URL = "https://mn.bluemn.net/mnapi/getconf"
GET_CONF_API_URL_BK = "http://127.0.0.1/mnapi/getconf"
ARGS = None
WALLET_LIST = []


############
##初始化##
############


############
##基础func##
############

def operation_file(file_name):
    try:
        h_file = open(file_name)
        try:
            readlines = h_file.readlines()
            print(readlines)
        finally:
            h_file.close()
    except IOError:
        print("IOError")


def operation_write_file(file_name, strs):
    try:
        h_file = open(file_name, 'w', 1)
        try:
            h_file.write(strs)
        finally:
            h_file.close()
    except IOError:
        print("IOError")


def operation_add_file(file_name, strs):
    try:
        h_file = open(file_name, 'a+', 1)
        try:
            h_file.write(strs)
        finally:
            h_file.close()
    except IOError:
        print("IOError")


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def set_pkjson(pk_json_dict=None, cover=False):
    # 格式：生成时间、主机名、vps绑定ip、mn秘钥，绑定端口，钱包缩写、是否已占用。占用交易tx。
    sava_pk = pk_json_dict
    new_pk_list = []

    print("pkdata.......")
    if pk_json_dict == None:

        print("no save")
        return False
    else:
        # 先读取文件去重
        oldpk_list = load_pkjson("pkdata.json")
        # 没有源文件
        if oldpk_list == []:
            new_pk_list.append(sava_pk)
        else:
            # 有旧版配置文件
            print("old version")
            print(oldpk_list)
            print(sava_pk)

            namelist = []
            for pk in oldpk_list:
                namelist.append(pk.get("mncoin"))
            print(namelist)
            is_use = False
            if sava_pk.get("mncoin") in namelist:
                print("需要保存的已经已存在")
                is_use = True

            for old in oldpk_list:
                print("循环构建新列表")
                if is_use:
                    print("存在同coin，覆盖")
                    if old.get("mncoin") == sava_pk.get("mncoin"):
                        new_pk_list.append(sava_pk)
                new_pk_list.append(old)
        print(new_pk_list)

    # 读取文件 ,设置值,保存
    # jsondata = json.dumps(new_pk_list)
    # operation_write_file('pkdata.json',jsondata)
    dumps_pkjson('pkdata.json', new_pk_list)

    pass


def get_pkjson(file_name="pkdata.json"):

    pk_list = []
    try:
        pkobj = open(file_name, "r")
        try:
            pk_list = json.load(pkobj)
            print(pk_list)
            if type(pk_list) != list:
                print('pkdata.json格式错误，已清空')
                comm = "rm %s " % file_name
                ret = subprocess.call([comm], shell=True)

        finally:
            pkobj.close()
            return pk_list
    except IOError:
        print("找不到pkdata.json配置文件")

    return pk_list


def dumps_pkjson(filename, strtext):

    with open(filename, 'wb') as f:
        #f.write( pickle.dumps(info) )
        pickle.dump(strtext, f)


def load_pkjson(filename):

    # data = pickle.loads(f.read())
    try:
        with open(filename, 'rb') as f:
            try:
                # 跟上面的data = pickle.loads(f.read())语意完全一样。
                data = pickle.load(f)

            except Exception as e:
                print('转换pkjson文件失败,格式错误')
                return []
            else:
                print('data>>>', data)
                if type(data) != list:
                    print('pkdata.json格式非法，已清空')
                    comm = "rm %s " % filename
                    ret = subprocess.call([comm], shell=True)
                    return []
                return data
    except Exception as e:

        print("获取pkdata.json文件失败，可能没有此文件")

    return []


############
##功能func##
############


def init_env():

    # 基础依赖
    ret = subprocess.call(
        [' apt-get wget curl unzip zip git vim python nano pwgen dnsutils zip  unzip net-tools -y'], shell=True)
    ret = subprocess.call(
        [' apt-get install software-properties-common python-software-properties -y'], shell=True)
    ret = subprocess.call(
        [' add-apt-repository ppa:bitcoin/bitcoin -y'], shell=True)
    ret = subprocess.call(['apt-get update -y'], shell=True)
    ret = subprocess.call(['apt-get upgrade -y'], shell=True)
    ret = subprocess.call(
        [' apt-get install libzmq3-dev libboost-all-dev build-essential  libssl-dev libminiupnpc-dev libevent-dev -y'], shell=True)
    ret = subprocess.call(
        [' apt-get install build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils -y'], shell=True)
    ret = subprocess.call(
        [' apt-get install libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev -y'], shell=True)
    ret = subprocess.call(
        [' apt-get install libboost-all-dev libdb4.8-dev libdb4.8++-dev  libminiupnpc-dev  libzmq3-dev -y'], shell=True)
    ret = subprocess.call(
        [' apt-get install libqt5gui5 libqt5core5a libqt5dbus5 qttools5-dev qttools5-dev-tools libprotobuf-dev protobuf-compiler -y'], shell=True)

    # 虚拟内存
    ret = subprocess.call(['free -h'], shell=True)
    ret = subprocess.call([' fallocate -l 4G /swapfile'], shell=True)
    ret = subprocess.call(['ls -lh /swapfile'], shell=True)
    ret = subprocess.call([' chmod 600 /swapfile'], shell=True)
    ret = subprocess.call([' mkswap /swapfile'], shell=True)
    txt = r"echo \'/swapfile none swap sw 0 0\' |  tee -a /etc/fstab "
    ret = subprocess.call([txt], shell=True)
    txt = ' bash -c \"echo \'vm.swappiness = 10\' >> /etc/sysctl.conf\"'
    ret = subprocess.call([txt], shell=True)
    ret = subprocess.call(['free -h'], shell=True)
    ret = subprocess.call(['echo \"SWAP setup complete...\"'], shell=True)

    return ret


def remove_wallet(wallet_data, delconf=False):

    pass
    wallet_path = wallet_data.get("wallet_path")
    ser_path = wallet_data.get("wallet_path") + wallet_data.get("servbin")
    cli_path = wallet_data.get("wallet_path") + wallet_data.get("clibin")
    tx_path = wallet_data.get("wallet_path") + wallet_data.get("txbin")
    config_path = wallet_data.get("config_path")

    print("Deleting old wallet file...")

    comm = "rm -rf %s " % ser_path
    print(comm)
    ret = subprocess.call([comm], shell=True)

    comm = "rm -rf %s " % cli_path
    print(comm)
    ret = subprocess.call([comm], shell=True)

    comm = "rm -rf %s " % tx_path
    print(comm)
    ret = subprocess.call([comm], shell=True)

    comm = "rm -rf %s " % wallet_path
    print(comm)
    ret = subprocess.call([comm], shell=True)

    if delconf == True:

        print("Remove old wallet config")
        comm = "rm -rf %s " % config_path
        print(comm)
        ret = subprocess.call([comm], shell=True)

        comm = "rm pkdata.json"
        print(comm)
        ret = subprocess.call([comm], shell=True)

    return ret


def stop_wallet(wallet_data):

    wallet_path = wallet_data.get("wallet_path")
    ser_path = wallet_data.get("wallet_path") + wallet_data.get("servbin")
    cli_path = wallet_data.get("wallet_path") + wallet_data.get("clibin")
    tx_path = wallet_data.get("wallet_path") + wallet_data.get("txbin")
    config_path = wallet_data.get("config_path")

    print("Stop Wallet ...")

    comm = r" netstat -tunlp"
    print(comm)
    ret = subprocess.call([comm], shell=True)

    comm = "%s stop " % cli_path
    print(comm)
    ret = subprocess.call([comm], shell=True)

    comm = "kill -9 $(ps -ef|grep %s | gawk '$0 !~/grep/ {print $2}' |tr -s '\n' ' ')" % wallet_data.get(
        "servbin")
    print(comm)
    ret = subprocess.call([comm], shell=True)

    comm = "kill -9 `pgrep %s ` " % wallet_data.get("servbin")
    print(comm)
    ret = subprocess.call([comm], shell=True)

    comm = r" netstat -tunlp"
    print(comm)
    ret = subprocess.call([comm], shell=True)

    return True


def start_wallet(wallet_data):

    wallet_path = wallet_data.get("wallet_path")
    ser_path = wallet_data.get("wallet_path") + wallet_data.get("servbin")
    cli_path = wallet_data.get("wallet_path") + wallet_data.get("clibin")
    tx_path = wallet_data.get("wallet_path") + wallet_data.get("txbin")
    config_path = wallet_data.get("config_path")

    print("Start Wallet...")
    comm = "%s -deamon &  " % ser_path
    print(comm)
    ret = subprocess.call([comm], shell=True)

    print("Wait 5 minutes, synchronize the network...")
    time.sleep(280)

    comm = "%s getinfo " % cli_path
    print(comm)
    ret = subprocess.call([comm], shell=True)

    return True


def add_wallet(wallet_data, cover=True):

    # 路径
    wallet_path = wallet_data.get("wallet_path")
    ser_path = wallet_data.get("wallet_path") + wallet_data.get("servbin")
    cli_path = wallet_data.get("wallet_path") + wallet_data.get("clibin")
    tx_path = wallet_data.get("wallet_path") + wallet_data.get("txbin")
    config_path = wallet_data.get("config_path")
    wallet_conf_path = wallet_data.get("conf_path")

    #
    print(wallet_data)

    # 判断是否强制更新
    # 判断过往钱包是否已经存在
    binpath = wallet_data.get("wallet_path") + wallet_data.get("servbin")
    print("check wallet path : %s" % binpath)
    exists_flag = os.path.exists(binpath)
    print(exists_flag)
    if exists_flag == True:
        if cover == False:
            return False
        else:
            stop_wallet(wallet_data)
            remove_wallet(wallet_data, delconf=True)

    # 下载和解压

    if wallet_data.get('type') == "zip":

        comm = "wget " + wallet_data.get("url") + \
            " -O " + wallet_data.get('filename')
        ret = subprocess.call([comm], shell=True)
        # 没有就创建目录
        if os.path.exists(wallet_path) == False:
            comm = "mkdir -p %s " % wallet_path
            ret = subprocess.call([comm], shell=True)

        comm = "unzip -o " + \
            wallet_data.get('filename') + "  -d  /tmp"
        ret = subprocess.call([comm], shell=True)

        # 复制文件到钱包
        comm = "find /tmp -name '%s' -exec cp {} %s " % (
            wallet_data.get('servbin'), wallet_path)
        comm = comm + r"\;"
        print(comm)
        ret = subprocess.call([comm], shell=True)

        comm = "find /tmp -name '%s' -exec cp {} %s " % (
            wallet_data.get('clibin'), wallet_path)
        comm = comm + r"\;"
        print(comm)
        ret = subprocess.call([comm], shell=True)

        comm = "find /tmp -name '%s' -exec cp {} %s " % (
            wallet_data.get('txbin'), wallet_path)
        comm = comm + r"\;"
        print(comm)
        ret = subprocess.call([comm], shell=True)

    elif wallet_data.get('type') == "tar.gz":

        comm = "wget " + wallet_data.get("url") + \
            " -O " + wallet_data.get('filename')
        ret = subprocess.call([comm], shell=True)
        # 没有就创建目录
        if os.path.exists(wallet_path) == False:
            comm = "mkdir -p %s " % wallet_path
            ret = subprocess.call([comm], shell=True)

        comm = " tar -zxvf  " + \
            wallet_data.get('filename') + "  -C  /tmp "
        ret = subprocess.call([comm], shell=True)

        # 复制文件到钱包
        comm = "find /tmp -name '%s' -exec cp {} %s " % (
            wallet_data.get('servbin'), wallet_path)
        comm = comm + r"\;"
        print(comm)
        ret = subprocess.call([comm], shell=True)

        comm = "find /tmp -name '%s' -exec cp {} %s " % (
            wallet_data.get('clibin'), wallet_path)
        comm = comm + r"\;"
        print(comm)
        ret = subprocess.call([comm], shell=True)

        comm = "find /tmp -name '%s' -exec cp {} %s " % (
            wallet_data.get('txbin'), wallet_path)
        comm = comm + r"\;"
        print(comm)
        ret = subprocess.call([comm], shell=True)

    # 给权限
    comm = " chmod 777 -R %s " % wallet_data.get('wallet_path')
    ret = subprocess.call([comm], shell=True)

    # 运行钱包、同步网络
    stop_wallet(wallet_data)

    # 配置文件写入，重启钱包
    text = (

        "server=1 \n"
        "listen=1 \n"
        "maxconnections=256 \n"
        "port=%s \n"
        "deamon=1 \n"
        "rpcport=%s \n"
        "rpcuser=%s \n"
        "rpcpassword=%s \n"
        "rpcallowip=%s \n"
        "%s \n" % (
            wallet_data.get('port'),
            wallet_data.get('rpcport'),
            wallet_data.get('rpcuser'),
            wallet_data.get('rpcpassword'),
            wallet_data.get('rpcallowip'),
            wallet_data.get('nodelist'))
    )

    print("write conf...")
    operation_write_file(wallet_conf_path, text)

    # 启动钱包,第一次启动要久一点四件同步
    start_wallet(wallet_data)
    time.sleep(60)

    # 第二次启动,设置模式
    stop_wallet(wallet_data)
    start_wallet(wallet_data)

    # 获取masternode秘钥
    masternode_pk = ''
    print("Making genkey...")
    comm = "%s " % cli_path + " masternode genkey"
    print(comm)
    ret, pk = commands.getstatusoutput(comm)
    if ret == 0:
        masternode_pk = pk
    print(masternode_pk)

    # 获取IP地址
    # 获取本机ip
    ip = get_host_ip()
    print(ip)

    # pk写入配置文件

    print("update config")
    print(masternode_pk)
    addtext = (
        "masternode=1 \n"
        "masternodeprivkey=%s \n"
        "externalip=%s \n" % (masternode_pk, ip))

    operation_add_file(wallet_conf_path, addtext)
    comm = "cat  %s " % wallet_conf_path
    ret = subprocess.call([comm], shell=True)

    # 保存pk值
    pk_json_dict = {
        "addtime": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        "vpsname": socket.gethostname(),
        "coin": wallet_data.get("name"),
        "ip": ip,
        "port": wallet_data.get("port"),
        "pk": masternode_pk,
        "copythisip": "%s:%s" % (ip, wallet_data.get("port")),
        "copypk": masternode_pk,
    }

    print(pk_json_dict)
    # set_pkjson(pk_json_dict)

    # 重启钱包
    stop_wallet(wallet_data)
    start_wallet(wallet_data)

    # 打印状态
    comm = "%s masternode status " % cli_path
    ret = subprocess.call([comm], shell=True)

    str = """

    # Copy the following entries, replace your TXID with Index, and add to your masternode.conf, restart wallet and start masternode


    BMNMASTERNODEA %s:%s %s replace-your-TXID-here replace-your-Index-here


    # example

    BMNMASTERNODEA 182.44.2.142:15003 3s7BnJMCkos787zqrCCqajJipLBGZpRFNkDsuUNUuzrmv5bSBHj 261cc28ba4326b92a11c344d418507baf06d1c86de593ba880f40fd701ec25b7 1


    # by BlueMN Tools


    """ % (pk_json_dict.get("ip"), pk_json_dict.get("port"), pk_json_dict.get("pk"))

    print(str)
    print("Congratulations. Setup is Complete. ")

    return True


def check_mnstat(wallet_data):

    # 路径
    wallet_path = wallet_data.get("wallet_path")
    ser_path = wallet_data.get("wallet_path") + wallet_data.get("servbin")
    cli_path = wallet_data.get("wallet_path") + wallet_data.get("clibin")
    tx_path = wallet_data.get("wallet_path") + wallet_data.get("txbin")
    config_path = wallet_data.get("config_path")
    wallet_conf_path = wallet_data.get("conf_path")

    comm = "cat %s " % wallet_conf_path
    ret, mnconf = commands.getstatusoutput(comm)

    comm = "%s " % cli_path + " getinfo "
    ret, getinfo = commands.getstatusoutput(comm)
    comm = "%s " % cli_path + " getmininginfo "
    ret, getmininginfo = commands.getstatusoutput(comm)

    comm = "%s " % cli_path + " masternode status "
    ret, mnstat = commands.getstatusoutput(comm)

    print(mnconf)
    print(getinfo)
    print(getmininginfo)
    print(mnstat)

    return ret


def check_all_status(local_config_data):

    # 循环检查状态
    for coin in local_config_data.get('coinlist'):
        print(coin)
        check_mnstat(local_config_data.get(coin.upper()))

    return 0


def get_cloud_conf(filename="wallet_config.json"):

    conf = {}
    api_url = GET_CONF_API_URL

    try:
        print("Get BlueMN main API server ...")
        payload = {'IP': get_host_ip(), 'VPSNAME': os.name}
        r = requests.get(api_url, params=payload)
        print(r.url)
        try:
            print(r.text)
            conf = json.loads(r.text)

        except Exception as e:
            print("api error")
            return conf
    except Exception as e:
        print("et BlueMN backup API server ...")
        try:

            payload = {'IP': get_host_ip(), 'VPSNAME': socket.gethostname()}
            r = requests.get(GET_CONF_API_URL_BK, params=payload)
            print(r.url)
            try:
                print(r.text)
                conf = json.loads(r.text)
            except Exception as e:
                print("api error")
                return conf

        except Exception as e:
            print("api error")
            pass
    return conf


############
###判断程序##
############


def main_app():

    print("BlueMN Masternode install Tools")
    init_env()
    print("Initialize the system environment....")

    print("Download BMN Wallet Dat from BlueMN api")
    cloud_coin_list = get_cloud_conf()

    print(cloud_coin_list.get("BMN"))

    print("Install BMN Wallet")
    add_wallet(cloud_coin_list.get("BMN"))


if __name__ == "__main__":

    main_app()
