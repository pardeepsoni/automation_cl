import boto3
from pprint import pprint
import datetime
import sys


def setup_re(profile_name='pardeepsoni'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    ec2_console_re = aws_console.resource(service_name='ec2', region_name='us-east-1')
    return ec2_console_re


def setup_cli(profile_name='pardeepsoni'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    ec2_console_cli = aws_console.client(service_name='ec2')
    return ec2_console_cli


def list_volume():
    f1=[{"Name":'status', "Values":['available']}]
    volumes = setup_re().volumes.filter(Filters=f1)
    for each_volume in volumes:
        print(each_volume.volume_id, each_volume.volume_type, each_volume.state, each_volume.size, each_volume.tags,
              each_volume.availability_zone)


def delete_volume():
    f1 = [{"Name": 'status', "Values": ['available']}]
    volumes = setup_re().volumes.filter(Filters=f1)
    for each_volume in volumes:
        if not each_volume.tags:
            each_volume.delete()
        print(f"Volume - {each_volume.volume_id} deleted.")


def attach_volume(instance_id, volume_id_to_attach, device='/dev/sdh'):
    instance = setup_re().Instance(instance_id)
    instance.attach_volume(Device=device, VolumeId=volume_id_to_attach)


def deattach_volume(instance_id, volume_id_to_deattach, device='/dev/sdh'):
    instance = setup_re().Instance(instance_id)
    instance.detach_volume(Device= device, VolumeId=volume_id_to_deattach)



def create_volume(az, volume_type, size_in_gb):
    #console=setup_re()
    setup_re().create_volume(AvailabilityZone=az,
        Size=size_in_gb,
        VolumeType = volume_type)



def volume_operation():
    while True:
        print("""\n1. List all avilable volume.
2. Attach Volume to a instance.
3. De-attach Volume from a instance.
4. Create Volume.
5. Delete an available and un-taged Volume.
6. Quit Operation.
        """)

        try:
            option = int(input("Please Enter your valid option (1-5): "))

            if option == 1:
                print("\nBelow are the avaiable volume.")
                list_volume()

            elif option == 2:
                instance_id = input("Enter Instance Id: ")
                volume_id_to_attach= input("Enter volume id to attach: ")
                device = input("Enter Device e.g /dev/sdh, xvdh, /dev/xvda: ")
                attach_volume(instance_id, volume_id_to_attach, device='/dev/sdh')
                print("\nVolume attached.")


            elif option == 3:
                instance_id = input("Enter Instance Id: ")
                volume_id_to_deattach= input("Enter volume id to attach: ")
                device = input("Enter Device e.g /dev/sdh, xvdh, /dev/xvda: ")
                deattach_volume(instance_id, volume_id_to_deattach, device='/dev/sdh')
                print("\nVolume deattached.")

            elif option == 4:
                az = input("Enter AvailabilityZone: ")
                volume_type= input("Enter volume_type \n'standard'|'io1'|'io2'|'gp2'|'sc1'|'st1'|'gp3': ")
                size_in_gb = int(input("Enter size_in_gb: "))
                create_volume(az, volume_type, size_in_gb)
                print("\nVolume Created.")

            elif option == 5:
                delete_volume()
                print("\nVolume Deleted.")

            elif option == 6:
                print("\n!!!!Operation quit......")
                sys.exit()

            else:
                print("\n!!!!!Option is incorrect, Please choose between 1-6.")

        except ValueError:
            print("\n!!!!!Option is incorrect, Please choose between 1-6.")


volume_operation()



