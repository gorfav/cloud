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

    process=Popen(['/usr/bin/aws','cloudformation','describe-stack-resources','--stack-name',inputParam],stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    jsonObject=json.loads(stdout)


    for key in jsonObject['StackResources']:
        instType=key['ResourceType']
        if instType == 'AWS::EC2::Instance':
           outstr=key['LogicalResourceId'] + " - "+ key['PhysicalResourceId']
           print outstr

if __name__ == '__main__':
    main()
