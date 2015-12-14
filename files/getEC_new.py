#!/usr/bin/python

import json,simplejson
import sys
from subprocess import Popen, PIPE

def main():

#    print 'Number of arguments:', len(sys.argv), 'arguments.'
    numArgs=len(sys.argv)

    if numArgs == 1:
        sys.exit()

    inputParam=sys.argv[1]
    status=sys.argv[2]

    process=Popen(['/usr/bin/aws','cloudformation','describe-stack-resources','--stack-name',inputParam],stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    jsonObject=json.loads(stdout)


    for key in jsonObject['StackResources']:
        instType=key['ResourceType']
        if instType == 'AWS::EC2::Instance':
           outstr=key['LogicalResourceId'] + " - "+ key['PhysicalResourceId']
           process=Popen(['/usr/bin/aws','ec2','describe-instance-status','--instance-id',key['PhysicalResourceId']],stdout=PIPE, stderr=PIPE)
           stdout, stderr = process.communicate()
           jsonObjectEC2=json.loads(stdout)
           if len(jsonObjectEC2) <= 1:
            print outstr
           else:
            for ec2Inst in jsonObjectEC2['InstanceStatuses']:
             ec2Status=ec2Inst['InstanceState']['name']  
             if status == 'All':
                print outstr
             elif (status == 'Running') and (ec2Status == 'running'):
                print  outstr
             elif (status == 'Stopped') and (ec2Status == 'stopped'):
                print outstr

if __name__ == '__main__':
    main()
