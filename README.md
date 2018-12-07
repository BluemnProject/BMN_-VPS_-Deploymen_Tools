# BMN_Massternode_VPS_Deploy_Tools【ubuntu 16.04 only】

Use this tool to complete the BMN Masternode deployment in your own VPS
This tools only applies to ubuntu16.04. Please do not run on ubuntu18.

# Prepare

```
1、With 1001 BMN
2、Create a new receiving address.(open File-> receiving addresses -> New and Copy the address) 
3、and sent 1000BMN to this addr,and wait for 6 Confirmation at least
4、Get TXID and Index.Copy and save it somewhere. (open Tools-> Debug console and input "masternode outputs" ,check TDIX and Index(must be 0 or 1))
5、Turn on maternode.conf(open tools-> open masternode configuration file ) and ready start configuring VPS 
6、Install BMN masternode using tools(tutorial below)
7、Copy the text, modify it, put it in masternode.conf, restart the wallet,

```


# Guide

Log in to your VPS using the root role (our default deployment path is /root, all users need to use root).

1、Git clone project
```
apt-get update && apt-get install git -y && git clone https://github.com/BluemnProject/BMN_Massternode_VPS_Deploy_Tools.git 

```
2、RUN Tools and Copy Parameters.

```
cd BMN_Massternode_VPS_Deploy_Tools && apt-get install python -y && python BlueMN_Masternode_Install.py
```

Wait until it's finished, print the text at the end, copy it out, and then replace it with your TXID and Index.

For example,

```
BMNMASTERNODEA %s:%s %s xxxx(replace your TXID here)xxxxx (replace your Index here)

```
# RUN Tools and Copy Parameters.

The purse to restart

Put the updated configuration entry into masternode.conf, then restart the wallet, and the masternode is visible.It's time to manage masternode





-BlueMN TEAM
