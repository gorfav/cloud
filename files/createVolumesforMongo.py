#!/usr/bin/env python
# the script will create snapshots of volumes and delete volumes which are older than 2 weeks

__author__ = "ID017437"
__date__ = "$Dec 16, 2015 8:48:52 AM$"

import boto
import os
import time
from boto import ec2

region = os.environ.get('AWS_DEFAULT_REGION')
aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_key = os.environ.get('AWS_SECRET_KEY')
aws_instance_id = os.environ.get('SCALR_CLOUD_SERVER_ID')
aws_instance_name = os.environ.get('SCALR_SERVER_HOSTNAME')
aws_zone = os.environ.get('AWS_ZONE')
aws_vol_type= os.environ.get('MONGODB_VOLUME_TYPE')
aws_vol_size= os.environ.get('MONGODB_VOLUME_SIZE')
aws_vol_iops= os.environ.get('MONGODB_VOLUME_IOPS')

def createMongoVolsGP2(conn_eu):
    # Create Data Volume
    vol=conn_eu.create_volume(aws_vol_size,aws_zone,None,aws_vol_type)       
    # Add a Name tag to the new volume so we can find it.    
    conn_eu.create_tags([vol.id], {"Name":"Data Volume for:"+aws_instance_name})    
    #Attach Data volume to instance
    time.sleep(20)
    result = conn_eu.attach_volume (vol.id,aws_instance_id, "/dev/xvdh")
    print 'Attach Volume Result: ', result
    
    # Create Log Volume
    vol=conn_eu.create_volume(aws_vol_size,aws_zone,None,aws_vol_type)       
    # Add a Name tag to the new volume so we can find it.    
    conn_eu.create_tags([vol.id], {"Name":"Log Volume for:"+aws_instance_name})
    #Attach Log volume to instance
    time.sleep(20)
    result = conn_eu.attach_volume (vol.id,aws_instance_id, "/dev/xvdi")
    print 'Attach Volume Result: ', result
    
    # Create Journal Volume
    vol=conn_eu.create_volume(aws_vol_size,aws_zone,None,aws_vol_type)       
    # Add a Name tag to the new volume so we can find it.    
    conn_eu.create_tags([vol.id], {"Name":"Journal Volume for:"+aws_instance_name})
    #Attach Journal volume to instance
    time.sleep(20)
    result = conn_eu.attach_volume (vol.id,aws_instance_id, "/dev/xvdj")
    print 'Attach Volume Result: ', result
    
    

    return

def createMongoVolsIO1(conn_eu,aws_vol_iops):
    
    
    # Create Data Volume
    vol=conn_eu.create_volume(aws_vol_size,aws_zone,None,aws_vol_type,aws_vol_iops)       
    # Add a Name tag to the new volume so we can find it.    
    conn_eu.create_tags([vol.id], {"Name":"Data Volume for:"+aws_instance_name})    
    #Attach Data volume to instance
    time.sleep(20)
    result = conn_eu.attach_volume (vol.id,aws_instance_id, "/dev/xvdh")
    print 'Attach Volume Result: ', result
    
    # Create Log Volume
    vol=conn_eu.create_volume(aws_vol_size,aws_zone,None,aws_vol_type,aws_vol_iops)       
    # Add a Name tag to the new volume so we can find it.    
    conn_eu.create_tags([vol.id], {"Name":"Log Volume for:"+aws_instance_name})
    #Attach Log volume to instance
    time.sleep(20)
    result = conn_eu.attach_volume (vol.id,aws_instance_id, "/dev/xvdi")
    print 'Attach Volume Result: ', result
    
    # Create Journal Volume
    vol=conn_eu.create_volume(aws_vol_size,aws_zone,None,aws_vol_type,aws_vol_iops)       
    # Add a Name tag to the new volume so we can find it.    
    conn_eu.create_tags([vol.id], {"Name":"Journal Volume for:"+aws_instance_name})
    #Attach Journal volume to instance
    time.sleep(20)
    result = conn_eu.attach_volume (vol.id,aws_instance_id, "/dev/xvdj")
    print 'Attach Volume Result: ', result


    return


def main():


    #conn_eu = ec2.connect_to_region(region,aws_access_key,aws_secret_key)
    conn_eu = ec2.connect_to_region(region)    
    
    if aws_vol_iops is None :
        createMongoVolsGP2(conn_eu)
    else:
        createMongoVolsIO1(conn_eu,aws_vol_iops)
        
if __name__ == "__main__":
    main()
