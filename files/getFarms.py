#!/usr/bin/env python

import socket
import json
import sys
import os
import time
from boto import ec2
from subprocess import Popen, PIPE
from boto import vpc



def main():

    farmDict={}
    connectionstring=""
    numArgs=len(sys.argv)
    if numArgs == 1:
        sys.exit()

    VPCName=sys.argv[1]
    VPCName = VPCName.lower()
    #farmList = open("/home/ansible/staging/files/farms.txt", "w")
    connStrFL = open("/home/ansible/staging/files/connStrSVT.txt", "w")

    if VPCName == "staging":
      cidrBlock = "172.0.0.0/16"

###Find the VPC
    myregion = ec2.get_region(region_name='eu-central-1')
    c = vpc.VPCConnection(region=myregion)
    vpcs = c.get_all_vpcs(filters=[("cidrBlock", cidrBlock)])
##create an ec2 connection
    conn = ec2.connect_to_region('eu-central-1')
    instList = conn.get_only_instances(filters={'vpc_id':vpcs[0].id})
    for i in instList:
      if 'farmName' in i.tags:
         frmName = i.tags['farmName']
         farmDict[frmName] = frmName
         connectionstring = connectionstring + "," + i.private_ip_address + ":27017"

    for fList in farmDict:
        print fList
    connStrFL.write(connectionstring)
    connStrFL.close()
    #farmList.close()

if __name__ == "__main__":
    main()
