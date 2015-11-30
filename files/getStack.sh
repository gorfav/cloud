stackFileName=/home/ansible/staging/files/stacks.txt
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE | grep StackName | cut -f4 -d'"' > $stackFileName
