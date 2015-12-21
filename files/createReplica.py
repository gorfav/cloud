#!/usr/bin/env python

import socket
import json,simplejson
import os
import time
from pymongo import MongoClient
from boto import ec2
from subprocess import Popen, PIPE

#time.sleep(60)
region = os.environ.get('AWS_DEFAULT_REGION')
aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_KEY')
scalr_farm_name = os.environ.get('SCALR_FARM_NAME')
scalr_instance_index = os.environ.get('SCALR_INSTANCE_INDEX')
aws_dns_name = os.environ.get('AWS_DNS_NAME')
replConfig = open("/tmp/replset.js", "w")

def getMyIP():

    f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    your_ip=f.read()
    return your_ip


def inititateReplica(conn):
    line = replConfig.write("rs.initiate()\n")
    line = replConfig.write("sleep(13000)\n")
    print scalr_farm_name
    print aws_secret_key
    instList = conn.get_all_reservations(filters={"tag:farmName" : scalr_farm_name,'instance-state-name': 'running'})
    print instList
    for r in instList:
        for i in r.instances:
#          cmdRepl="rs.add('" + i.private_ip_address +"')\n"
          cmdRepl="rs.add('" + i.tags['mngDNS'] +"')\n"      
          line = replConfig.write(cmdRepl)
          line = replConfig.write("sleep(8000)\n")
    return

def addMembertoSet(conn):

    print "iam here"
    instStatus = 'terminated'    
    instList = conn.get_all_reservations(filters={"tag:farmName" : scalr_farm_name})
    

    for r in instList:        
        for i in r.instances:         
         print i
         try:
          instStatus = i.state
         except:
          pass
         if instStatus == "running":          
#          cmdRepl="rs.add('" + i.private_ip_address +"')\n"
          cmdRepl="rs.add('" + i.tags['mngDNS'] +"')\n"          
          line = replConfig.write(cmdRepl)
          line = replConfig.write("sleep(8000)\n")
#         elif instStatus == 'running':
#          cmdRepl="rs.remove('" + i.private_ip_address +"')\n"
#          line = replConfig.write(cmdRepl)

    return

def getReplicaState(replicaStatus):

 #get machine IP
 eth0_IP = getMyIP().rstrip('\n')
 try:
    for key in replicaStatus['members']:
      memberIP=key['name']
      memberIP=memberIP.rsplit(':',1)[0]
      stateStr=key['stateStr']
      if eth0_IP == memberIP and stateStr == "PRIMARY":
        return 1
      if eth0_IP == memberIP and stateStr == "SECONDARY":
        return 2

 except:
    return 0

    return 0

def main():
    client = MongoClient(host = "127.0.0.1", port = 27017)
    db = client.admin
    replicaState=0
    isPrimary = 0

    try:
        replicaStatus =  db.command("replSetGetStatus")
        replicaState =  replicaStatus['myState']
    except:
        pass

    try:
        isPrimary = getReplicaState(replicaStatus)
    except:
        pass

    print "Replica State is: " , replicaState
    print "Scalr Index Name is:"  + scalr_instance_index
    
    conn_eu = ec2.connect_to_region(region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

    
    
    
    
    
#    if replicaState >= 1 and isPrimary == 1:
#        print "AlreadyReplicated"
#        addMembertoSet(conn_eu)
#        replConfig.close()
#        process=Popen(["/usr/bin/mongo","localhost:27017/admin","/tmp/replset.js"],stdout=PIPE)
#        process.wait()
#        for line in process.stdout:
#          print line
#        print process.returncode
    if replicaState == 0 and scalr_instance_index == '1':
        print "New Replica Set"        
        inititateReplica(conn_eu)
        replConfig.close()
#        time.sleep(15)
        print "File created"
        process=Popen(["/usr/bin/mongo","localhost:27017/admin","/tmp/replset.js"],stdout=PIPE,stderr=PIPE)
        process.wait()
#        while process.poll() is None:
#            print("Still working...")
        for line in process.stdout:
          print line
        print process.returncode

    replConfig.close()

if __name__ == "__main__":
    main()
