#!/usr/bin/python


__author__ = "ID017437"
__date__ = "$Dec 21, 2015 7:18:51 AM$"

import socket
import json,simplejson
import os
import time
from boto.utils import get_instance_metadata
from boto  import route53
from pymongo import MongoClient
from boto import ec2
from subprocess import Popen, PIPE

region = os.environ.get('AWS_DEFAULT_REGION')
aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_KEY')
scalr_farm_name = os.environ.get('SCALR_FARM_NAME')
scalr_instance_index = os.environ.get('SCALR_INSTANCE_INDEX')
aws_dns_name = os.environ.get('AWS_DNS_NAME')
mongoInternalIP = os.environ.get('SCALR_INTERNAL_IP')
mongoReplicaDNSName = os.environ.get('MONGO_DNS_NAME')

def main():

    print mongoReplicaDNSName
    print aws_dns_name
    print region
    print mongoInternalIP
    
try:
    conn_eu = route53.connect_to_region(region)
    hostedZone = conn_eu.get_zone(aws_dns_name)    
    change_set = route53.record.ResourceRecordSets(conn_eu, hostedZone.id)
    changes1 = change_set.add_change("UPSERT",mongoReplicaDNSName+"."+aws_dns_name, type="A")
    changes1.add_value(mongoInternalIP)
    change_set.commit()
##Add dns name to tag    
    conn_inst = ec2.connect_to_region(region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
    instID=get_instance_metadata()['instance-id']
    conn_inst.create_tags([instID], {"mngDNS": mongoReplicaDNSName+"."+aws_dns_name})
    
except Exception as e: print(e)
  
if __name__ == "__main__":
    main();
