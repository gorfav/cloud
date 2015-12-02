#!/usr/bin/python

import json,simplejson
import sys
from subprocess import Popen, PIPE

def main():

#    print 'Number of arguments:', len(sys.argv), 'arguments.'
    numArgs=len(sys.argv)
    filename = "/home/ansible/staging/files/test.txt"
    target = open(filename, 'w')
    target.write('Test')
    if numArgs == 1:
        sys.exit()

    inputParam=sys.argv[1]
    status=sys.argv[2]

    target.write(inputParam+'\n')
    target.write(status)
    process=Popen(['/usr/bin/aws','cloudformation','describe-stack-resources','--stack-name',inputParam],stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    jsonObject=json.loads(stdout)
    target.close()

    for key in jsonObject['StackResources']:
        instType=key['ResourceType']
        if instType == 'AWS::EC2::Instance':
           outstr=key['LogicalResourceId'] + " - "+ key['PhysicalResourceId']
           process=Popen(['/usr/bin/aws','ec2','describe-instance-status','--instance-id',key['PhysicalResourceId']],stdout=PIPE, stderr=PIPE)
           stdout, stderr = process.communicate()
           jsonObjectEC2=json.loads(stdout)
           lenDict=len(jsonObjectEC2['InstanceStatuses'])
           if lenDict == 0  and status == 'All':
            print outstr
           elif lenDict == 1:
            for ec2Inst in jsonObjectEC2['InstanceStatuses']:
             ec2Status=ec2Inst['InstanceState']['Name']
             if status == 'All':
                print outstr
             elif (status == 'Running') and (ec2Status == 'running'):
                print  outstr
           if (status == 'Stopped') and (lenDict == 0):
                print outstr

if __name__ == '__main__':
    main()
