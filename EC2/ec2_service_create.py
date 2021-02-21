import boto3
from pprint import pprint
from automation_cl.setup import setup_re_ec2, setup_cli_ec2, setup_cli_s3, setup_cli_iam
import sys





def create_volume(az, volume_type, size_in_gb, region_name='us-east-1'):
    #console=setup_re()
    setup_re_ec2(region_name=region_name).create_volume(AvailabilityZone=az,
        Size=size_in_gb,
        VolumeType = volume_type)


def create_snapshot(volume_id, region_name='us-east-1' ):
    console = setup_re_ec2(region_name='us-east-1')
    console.create_snapshot(
        Description='my snapshot',
        VolumeId=volume_id,
    )
    print("Snapshot created...")


def create_sg(sg_name, region_name='us-east-1'):
    response=setup_cli_ec2(region_name=region_name).create_security_group(
        Description='SSH Security Group Created by boto3',
        GroupName=sg_name,
        VpcId='vpc-4b1a1831',
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'SSH-boto3'
                    },
                ]
            }
                        ]
    )
    print(f"\nSecurity Group '{response.get('GroupId')}' is created")
    return response.get('GroupId')




#Attach Security SSH inboud rule
def attach_sg_inbound_rule_ssh_rule(security_group_id, region_name='us-east-1'):
    sg_rule = setup_cli_ec2(region_name=region_name).SecurityGroup(security_group_id)
    sg_rule.authorize_ingress(
        IpPermissions=[
            {
                'FromPort': 22,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'SSH rule boto3'
                    },
                ],

                'ToPort': 22,

            },
        ],

    )
    print(f"ssh rule attached to '{security_group_id}'.")


#Attach Security http inboud rule to a Security group

def attach_sg_inbound_rule_http_rule(security_group_id, region_name='us-east-1'):
    sg_rule = setup_cli_ec2(region_name=region_name).SecurityGroup(security_group_id)
    sg_rule.authorize_ingress(
        IpPermissions=[
            {
                'FromPort': 80,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'http rule boto3'
                    },
                ],

                'ToPort': 80,

            },
        ],

    )
    print(f"http rule attached to '{security_group_id}'.")



# Creat a Launch Template for building Dev Hosts
def create_launch_template(region_name='us-east-1'):
    response = setup_cli_ec2(region_name=region_name).create_launch_template(
        LaunchTemplateName='Dev-instance-template-boto3',
        VersionDescription='01-boto3',
        LaunchTemplateData={
            'ImageId': 'ami-0be2609ba883822ec',
            'InstanceType': 't2.micro',
            'Monitoring': {
                'Enabled': False
            },

            'InstanceInitiatedShutdownBehavior': 'terminate',

            'TagSpecifications': [
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'Server-boto3'
                        },
                    ]
                },
            ],

            'SecurityGroupIds': [
                'sg-07d5ce1ffa7eff245',
            ],
        }
    )
    pprint(response)



# Creating EC2 Host form a given Launch tempplate
def create_ec2_from_launch_template(lauch_template_id, instance_count_to_create, region_name='us-east-1'):
    instance = setup_re_ec2(region_name=region_name).create_instances(
        MaxCount = instance_count_to_create,
        MinCount = 1,
        LaunchTemplate={
            'LaunchTemplateId': lauch_template_id,
            'Version': '1',

        },

    )
    pprint(instance)

def ingress_rule(sg_id, from_port,ip_protocol, cidr, to_port, profile_name='pardeepsoni',):

    response = setup_cli_ec2(profile_name).authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                'FromPort': from_port,
                'IpProtocol': ip_protocol,
                'IpRanges': [
                    {
                        'CidrIp': cidr,
                        'Description': 'boto3 rule'
                    },
                ],

                'ToPort': to_port,

            },
        ],

    )
    print("Rule attached to security group.")

