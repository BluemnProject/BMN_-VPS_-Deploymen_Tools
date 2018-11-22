# BMN_Massternode_VPS_Deploy_Tools

Use this tool to complete the BMN Masternode deployment in your own VPS

# Guide

Log in to your VPS using the root role (our default deployment path is /root, all users need to use root).

1、Git clone project
```
git clone https://github.com/BluemnProject/BMN_Massternode_VPS_Deploy_Tools.git 

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



- BlueMN TEAM
