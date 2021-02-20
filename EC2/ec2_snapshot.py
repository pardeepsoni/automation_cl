import boto3
import sys
from pprint import pprint


def setup_re(profile_name='pardeepsoni'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    ec2_console_re = aws_console.resource(service_name='ec2')
    return ec2_console_re


def setup_cli(profile_name='pardeepsoni'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    ec2_console_cli = aws_console.client(service_name='ec2')
    return ec2_console_cli


def list_snapshots():
    console = setup_re()
    for each_snapshot in console.snapshots.filter(OwnerIds=['261635990162']):
        #pprint(dir(each_snapshot))
        print(each_snapshot.owner_id, each_snapshot.snapshot_id, each_snapshot.state, each_snapshot.tags,
              each_snapshot.description)

def delete_snapshot(id):
    console = setup_re()
    #print(dir(console.Snapshot(id)))
    response=console.Snapshot(id)
    response.delete()
    print(f"Sanpshot '{id}' Deleted.")

def create_snapshot():
    console = setup_re()
    console.create_snapshot(
        Description='my snapshot',
        VolumeId='vol-0616230508c20e8cd',
    )
    print("Snapshot created...")

delete_snapshot('snap-09a3424733a9f4d42')


Ec2_console = boto3.resource(service_name='ec2', region_name='us-east-1')

f1 = [{'Name': 'instance-state-name', 'Values': ['stopped']}]
for each_insstance in Ec2_console.instances.filter(Filters=f1):

    print(each_insstance.id, each_insstance.state['Name'])

# create_snapshot()
#list_snapshots()