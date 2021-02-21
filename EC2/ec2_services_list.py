import boto3
from pprint import pprint
from automation_cl.setup import setup_re_ec2, setup_cli_ec2, setup_cli_s3, setup_cli_iam
import sys


# List all EC2 instance in a region

def list_all_ec2(region_name='us-east-1'):
    instance_list = setup_cli_ec2(region_name=region_name).describe_instances()['Reservations']
    count = 1
    for instance in instance_list:
        for each_instance in instance.get('Instances'):
            instance_id = each_instance.get('InstanceId'),
            image_id = each_instance.get('ImageId'),
            instance_type = each_instance.get('InstanceType')
            tags = each_instance.get('Tags')
            az = each_instance['Placement']['AvailabilityZone']
            state = each_instance['State']['Name']
            private_dns_name = each_instance.get('PrivateDnsName')
            sg = each_instance.get('SecurityGroups')
            launch_time = each_instance.get('LaunchTime').strftime("%d-%B-%Y")
            sg_name=''
            for sg_grp in sg:
                sg_name = sg_grp.get('GroupName')


            for tag in tags:
                if tag['Key'] == "Name":
                    name = tag['Value']

            print(f"{count}. Instance Label: {name} | Instance ID: {instance_id[0]} | Instance Type: {instance_type} | "
                  f"Image ID: {image_id[0]} | AZ: {az} | State: {state} | Private_DNS_Name: {private_dns_name} "
                  f" | Launch Time: {launch_time} | {sg_name}")
            count += 1

# List all Security Groups
def list_all_sg(region_name='us-east-1'):
    response = setup_cli_ec2(region_name=region_name).describe_security_groups()
    count =0
    for each_sg in response['SecurityGroups']:
        #print(each_sg.get('IpPermissions'))
        count += 1
        if each_sg.get('IpPermissions','null') == []:
            print(f"{count}. SG Name: {each_sg['GroupName']} | SG ID: {each_sg['GroupId']} | SG Description : '{each_sg.get('Description','None')}' | "
                  f"From/To Port: null / null |  Protocol: 'null' | IP Range: ([], 'null')")
        else:
            for ip_perm in each_sg.get('IpPermissions','null'):
                print(f"{count}. SG Name: {each_sg['GroupName']} | SG ID: {each_sg['GroupId']} | SG Description : '{each_sg.get('Description','None')}' | "
                          f" From/To Port: {ip_perm.get('FromPort','null')} / {ip_perm.get('ToPort', 'null')} | "
                          f" Protocol: {ip_perm.get('IpProtocol','null')} | IP Range: {ip_perm.get('IpRanges'), 'null'}")


def list_snapshots(region_name='us-east-1'):
    console = setup_re_ec2(region_name=region_name)
    for each_snapshot in console.snapshots.filter(OwnerIds=['261635990162']):
        #pprint(dir(each_snapshot))
        print(f"Owner ID: {each_snapshot.owner_id} | Snapshot ID: {each_snapshot.snapshot_id} | "
              f"State: {each_snapshot.state} | Tag: {each_snapshot.tags} | Description: {each_snapshot.description}")


# List All S3 buckets

def list_all_buckets(region_name='us-west-1'):
    response = setup_cli_s3(region_name=region_name).list_buckets()
    bucket_list = response['Buckets']
    print("Bucket List")
    for each_bucket in bucket_list:
        creation_time = each_bucket['CreationDate'].strftime('%d-%B-%Y')
        bucket_name = each_bucket['Name']
        print(f"Bucket Name: {bucket_name} | Creation Time: {creation_time}")

# List all launch templates in the given region

def list_all_template(region_name='us-west-1'):
    launch_templates = setup_cli_ec2(region_name=region_name).describe_launch_templates()
    for each_template in launch_templates['LaunchTemplates']:
        launch_template_name = each_template['LaunchTemplateName']
        launch_template_id = each_template['LaunchTemplateId']
        default_version_number = each_template['DefaultVersionNumber']
        latest_version_number = each_template['LatestVersionNumber']
        create_time = each_template['CreateTime'].strftime('%d-%B-%Y')

        print(f"Launch Template Name: {launch_template_name} | Launch Template Id: {launch_template_id}"
              f"| Default Version Number: {default_version_number} | Latest Version Number: {latest_version_number} "
              f"| Create Time: {create_time}")

# List all Volumes

def list_volumes(region_name='us-east-1'):
    volumes = setup_re_ec2(region_name=region_name).volumes.filter()
    for each_volume in volumes:
        print(f"Volume ID: {each_volume.volume_id} | Volume Type: {each_volume.volume_type} | "
              f"Volume State: {each_volume.state} | Volume Size : {each_volume.size} GB| "
              f"Volume Tag: {each_volume.tags} | AZ: {each_volume.availability_zone}")



# Describe the details of a launch template
def describe_launch_template(lauch_template_id, version_id,region_name='us-east-1'):
    response = setup_cli_ec2(region_name=region_name).describe_launch_template_versions(
        LaunchTemplateId=lauch_template_id,
        Versions=[
            version_id,
        ]
    )
    pprint(response)





# Create Security Group Creation




#Delete Security Group
def delete_sg(security_group_id, region_name='us-east-1'):
    response = setup_cli_ec2(region_name=region_name).delete_security_group(
        GroupId=security_group_id,
    )
    print(f"Security Group '{security_group_id}' is deleted")




