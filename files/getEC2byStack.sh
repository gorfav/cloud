INSTANCE_FILE=/home/ansible/staging/files/instances.txt
STACK_NAME=$1
aws cloudformation describe-stack-resources --stack-name $STACK_NAME  | grep LogicalResourceId | cut -f4 -d'"' > $INSTANCE_FILE
