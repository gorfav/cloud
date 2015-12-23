#!/usr/bin/env python

import socket
import json
import sys
import os
import time
import smtplib
from email.mime.text import MIMEText
from pprint import pprint

from boto import ec2
from subprocess import Popen, PIPE
from boto import vpc

import socket
import json,simplejson
import os
import time
from pymongo import MongoClient
from boto import ec2
from subprocess import Popen, PIPE

#time.sleep(300)
region = os.environ.get('AWS_DEFAULT_REGION')
aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_KEY')
scalr_farm_name = os.environ.get('SCALR_FARM_NAME')
scalr_instance_index = os.environ.get('SCALR_INSTANCE_INDEX')
aws_dns_name = os.environ.get('AWS_DNS_NAME')
mailfl = "/tmp/email.txt"
emailOutput = open(mailfl, "w")
receiever = os.environ.get('EMAIL_RECIPIENT')

def sendEmail(filename):

    sender =  "scalr@t-mobile.nl"
    attachFile = open(filename,"rb")
#    msg = {}
    msg = MIMEText(attachFile.read())
    attachFile.close()
    msg['Subject'] = 'The contents of %s' % filename
    msg['From'] = sender
    msg['To'] = receiever
    try:
        s = smtplib.SMTP('localhost')
        s.sendmail(sender,receiever, msg.as_string())
        s.quit()
        print "Successfully sent email"
    except:
        print "Error: unable to send email"


def writeEmailFile(r, filename):

        try:
            #filename.write(key + ":" + join(r[key]) + "\n")
            pprint(r, filename)
            filename.write("====================================================================================\n")
            filename.write("====================================================================================\n")
            filename.write("====================================================================================\n")
        except:
            pass

        #for k, v in r.items():
        #    line = '{}, {}'.format(k, v)
        #    filename.write(line)
        #    filename.write("\n")


def getReplicSetDetails(conn):


    instStatus = 'terminated'
    instList = conn.get_all_reservations(filters={"tag:farmName" : scalr_farm_name})


    for r in instList:
        for i in r.instances:
         try:
          instStatus = i.state
         except:
          pass
         if instStatus == "running":
            writeEmailFile(i.__dict__,emailOutput)


    return


def main():
    conn_eu = ec2.connect_to_region(region,aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)
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

    if replicaState != 0 and scalr_instance_index == '1':
        emailOutput.write("MongoDB Replica Set Information \n")
        emailOutput.write("====================================================================================\n")
        writeEmailFile(replicaStatus,emailOutput)
        emailOutput.write("Instances Created for Farm - " + scalr_farm_name + "\n")
        emailOutput.write("====================================================================================\n")
        getReplicSetDetails(conn_eu)
    elif scalr_instance_index != '1':
        emailOutput.write("Instances Created for Farm - " + scalr_farm_name + "\n")
        emailOutput.write("====================================================================================\n")
        getReplicSetDetails(conn_eu)

    emailOutput.close()
    sendEmail(mailfl)

if __name__ == "__main__":
    main()
