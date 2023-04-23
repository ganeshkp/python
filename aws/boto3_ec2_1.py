import boto3
import sys
from botocore.exceptions import ClientError

ec2 = boto3.client('ec2')
#-------------------------------------------------------------------------------------
# Describe instances
response = ec2.describe_instances()
print(response)


instance_ids=[]
instance_ids = [instance["InstanceId"] for instance in response.get("Reservations")[0].get("Instances")]

#Instance id1: 'i-0a7c9c27b9d594df0'
#Instance id2: 'i-020f61779ba7e81ba'

#---------------------------------------------------------------------
# Monitor and unmonitor instances
# if sys.argv[1] == 'ON':
#     response = ec2.monitor_instances(InstanceIds=['i-0a7c9c27b9d594df0'])
# else:
#     response = ec2.unmonitor_instances(InstanceIds=['i-0a7c9c27b9d594df0'])
# print(response)

#------------------------------------------------------------------------------------
# Start and Stop instances
# instance_id = instance_ids
# action = sys.argv[1].upper()

# ec2 = boto3.client('ec2')

# if action == 'ON':
#     # Do a dryrun first to verify permissions
#     try:
#         ec2.start_instances(InstanceIds=instance_ids, DryRun=True)
#     except ClientError as e:
#         if 'DryRunOperation' not in str(e):
#             raise

#     # Dry run succeeded, run start_instances without dryrun
#     try:
#         response = ec2.start_instances(InstanceIds=instance_ids, DryRun=False)
#         print(response)
#     except ClientError as e:
#         print(e)
# else:
#     # Do a dryrun first to verify permissions
#     try:
#         ec2.stop_instances(InstanceIds=instance_ids, DryRun=True)
#     except ClientError as e:
#         if 'DryRunOperation' not in str(e):
#             raise

#     # Dry run succeeded, call stop_instances without dryrun
#     try:
#         response = ec2.stop_instances(InstanceIds=instance_ids, DryRun=False)
#         print(response)
#     except ClientError as e:
#         print(e)

#--------------------------------------------------------------------------------------
# Reboot Instances
try:
    ec2.reboot_instances(InstanceIds=instance_ids, DryRun=True)
except ClientError as e:
    if 'DryRunOperation' not in str(e):
        print("You don't have permission to reboot instances.")
        raise

try:
    response = ec2.reboot_instances(InstanceIds=instance_ids, DryRun=False)
    print('Success', response)
except ClientError as e:
    print('Error', e)

#--------------------------------------------------------------
print("END")