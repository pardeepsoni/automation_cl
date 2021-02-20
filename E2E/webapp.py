import boto3
from pprint import pprint
from AWS.setup import  setup_cli_ec2,  setup_cli_elb, setup_cli_asg, setup_cli_rds
import os
import base64

class WebApp:
    # Create Security Group ELB

    def __init__(self, profile_name):
        self.profile_name = profile_name

    def write_data_tofile(self, message):
        f = open('data.txt', "a")
        f.write(message)
        f.close()

    def create_sg(self, sg_name, region_name='us-east-1'):
        sg_response = setup_cli_ec2(self.profile_name, region_name=region_name).create_security_group(
            Description='webapp-security-group',
            GroupName=sg_name,
            VpcId='vpc-4b1a1831',
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'webapp-automation'
                        },
                    ]
                }
            ]
        )
        print(f"\nSecurity Group '{sg_response.get('GroupId')}' is created")
        return sg_response.get('GroupId')

    def attach_sg_inbound_rule_http_rule(self, security_group_id):
        setup_cli_ec2(self.profile_name).authorize_security_group_ingress(
        CidrIp='0.0.0.0/0',
        FromPort=80,
        GroupId=security_group_id,
        IpProtocol='tcp',
        ToPort=80,

    )
        pprint(f"http rule attached to '{security_group_id}'.")

    def attach_ref_sgrule(self, security_group_id, refsg_name):
        response = setup_cli_ec2(self.profile_name).authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'FromPort': 80,
                    'IpProtocol': 'tcp',
                    'ToPort': 80,
                    'UserIdGroupPairs': [
                        {
                            'Description': f'traffic from {refsg_name}',
                            'GroupName': refsg_name,
                        },
                    ]
                },
            ],

        )
        print(response)

    # Create ELB
    def create_alb(self, sg_id):
        response_alb = setup_cli_elb(self.profile_name).create_load_balancer(
            Name='wbapp-alb',
            Subnets=[
                'subnet-146c9f4b', 'subnet-89d224ef', 'subnet-22609d03'
            ],

            SecurityGroups=[
                sg_id,
            ],
            Scheme='internet-facing',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'webapp-automation'
                },
            ],
            Type='application',
            IpAddressType='ipv4',
        )
        pprint(response_alb)
        for arn in response_alb['LoadBalancers']:
            albarn = arn['LoadBalancerArn']
        return albarn

    #Create target group

    def create_tg(self):
        response_tg = setup_cli_elb(self.profile_name).create_target_group(
            Name='webapp-tg',
            Protocol='HTTP',
            Port=80,
            VpcId='vpc-4b1a1831',
            HealthCheckProtocol='HTTP',
            HealthCheckEnabled=True,
            HealthCheckPath='/',
            HealthCheckIntervalSeconds=10,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=2,
            UnhealthyThresholdCount=2,
            TargetType='instance',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'webapp-automation'
                },
            ]
        )
        pprint(response_tg)
        for arn in response_tg['TargetGroups']:
            tg_arn = arn['TargetGroupArn']
        return tg_arn

    #Create a listener for the target group and alb

    def create_listner(self,tg_arn,alb_arm):

        response = setup_cli_elb(self.profile_name).create_listener(
            DefaultActions=[
                {
                    'TargetGroupArn': tg_arn,
                    'Type': 'forward',
                },
            ],
            LoadBalancerArn=alb_arm,
            Port=80,
            Protocol='HTTP',
        )
        pprint(response)
        for arn in response['Listeners']:
            lis_arn = arn['ListenerArn']

        return lis_arn

    def create_launch_template(self, sg_id):
        message = '''#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd.service
systemctl enable httpd.service
cd /var/www/html/
wget https://html5up.net/paradigm-shift/download --no-check-certificate
unzip download
'''
        message_bytes = message.encode('"utf-8"')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('"utf-8"')
        response = setup_cli_ec2(self.profile_name).create_launch_template(
            LaunchTemplateName='webapp-lt',
            VersionDescription='01-boto3',
            LaunchTemplateData={
                'ImageId': 'ami-0be2609ba883822ec',
                'InstanceType': 't2.micro',
                'InstanceInitiatedShutdownBehavior': 'terminate',
                'UserData': base64_message,

                'TagSpecifications': [
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': 'webapp-automation'
                            },
                        ]
                    },
                ],

                'SecurityGroupIds': [
                    sg_id,
                ],
            }
        )
        pprint(response['LaunchTemplate'])
        lt_id = response['LaunchTemplate']['LaunchTemplateId']
        return lt_id

    def create_asg(self, tg_arn, lt_id):
        response = setup_cli_asg(self.profile_name).create_auto_scaling_group(
            AutoScalingGroupName='webapp-asg',
            LaunchTemplate={
                'LaunchTemplateId': lt_id,
                'Version': '1'
            },
            MinSize=2,
            MaxSize=3,
            DesiredCapacity=2,
            DefaultCooldown=10,
            AvailabilityZones=[
                'us-east-1a','us-east-1b','us-east-1c'
            ],
            TargetGroupARNs=[
                tg_arn,
            ],
            HealthCheckType='ELB',
            HealthCheckGracePeriod=1,
            VPCZoneIdentifier='subnet-146c9f4b, subnet-89d224ef, subnet-22609d03',

        )
        pprint(response)

    # RDS Database Creation
    def create_rds_mysql_db(self, sg_id):
        response = setup_cli_rds(self.profile_name).create_db_instance(
            DBName='webapp_rds',
            DBInstanceIdentifier='webappdbinstance',
            AllocatedStorage=20,
            DBInstanceClass='db.t2.micro',
            Engine='mysql',
            MasterUsername='admin',
            MasterUserPassword='Mehrauli1!',
            VpcSecurityGroupIds=[
                sg_id,
            ],
            AvailabilityZone='us-east-1a',
            DBSubnetGroupName='default-vpc-4b1a1831',
            DBParameterGroupName='default.mysql8.0',
            BackupRetentionPeriod=7,
            Port=3306,
            MultiAZ=False,
            EngineVersion='8.0.20',
            AutoMinorVersionUpgrade=True,
            LicenseModel='general-public-license',
            PubliclyAccessible=True,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'webapp-automation'
                },
            ],
            StorageType='gp2',
            StorageEncrypted=False,
            DeletionProtection= False,
            MaxAllocatedStorage=1000,
        )
        pprint(response)

    def decribe_db(self, dbinsatnce):
        response = setup_cli_rds(self.profile_name).describe_db_instances(
            DBInstanceIdentifier=dbinsatnce,
        )
        pprint(response)

    # Delete the full flow
    def detach_instances(self):
        response = setup_cli_asg(self.profile_name).detach_instances(
            AutoScalingGroupName='webapp-asg',
            ShouldDecrementDesiredCapacity=True
        )

    def delete_asg(self):
        response = setup_cli_asg(self.profile_name).delete_auto_scaling_group(
                AutoScalingGroupName='webapp-asg',
                ForceDelete=True
        )
        print("ASG Deleted")

    def delete_launch_template(self):
        response = setup_cli_ec2(self.profile_name).delete_launch_template(
            LaunchTemplateName='webapp-lt'
        )
        print("ASG Launch Template")

    def delete_alb(self, albarn):
        response = setup_cli_elb(self.profile_name).delete_load_balancer(
            LoadBalancerArn=albarn
        )
        print("ALB Deleted")

    def delete_listner(self, lis_arn):
        response = setup_cli_elb(self.profile_name).delete_listener(
            ListenerArn=lis_arn
        )
        print("Listner Deleted")

    def delete_tg(self, tg_arn):
        response = setup_cli_elb(self.profile_name).delete_target_group(
            TargetGroupArn=tg_arn
        )

        print("Target Group Deleted")

    def delete_sg(self, sg_id):
        response = setup_cli_ec2(self.profile_name,).delete_security_group(
            GroupId=sg_id,
        )

        print("Security Group Deleted")

    def ec2_instance_delete(self):
        response = setup_cli_ec2(self.profile_name).describe_instances(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': [
                        'webapp-automation',
                    ],
                    'Name': 'instance-state-name',
                    'Values': [
                        'running',
                    ]
                },
            ],
        )
        for inst in response['Reservations']:
            for id in inst['Instances']:
                setup_cli_ec2(self.profile_name).terminate_instances(InstanceIds=[id['InstanceId']])
                print(f"{id['InstanceId']} terminated ")

    def db_deletion(self, dbinstance):
        setup_cli_rds(self.profile_name).delete_db_instance(
            DBInstanceIdentifier=dbinstance,
            SkipFinalSnapshot=True,
            #FinalDBSnapshotIdentifier='string',
            DeleteAutomatedBackups=True
        )
        print("db instance deleting")







