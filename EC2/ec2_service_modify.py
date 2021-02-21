import boto3
from pprint import pprint
from automation_cl.setup import setup_re_ec2, setup_cli_ec2, setup_cli_s3, setup_cli_iam
import sys

def instance_status(id):
    instance_list = setup_cli_ec2().describe_instances(InstanceIds=id)['Reservations']
    for instance in instance_list:
        for each_instance in instance['Instances']:
            state= each_instance['State']['Name']
            return state

def ec2_operation():
    ec2_list =[]
    while True:
        print("""\n=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=
        
1. Current state EC2 Instance.
2. Start EC2 Instance.
3. Stop EC2 Instance.
4. Reboot EC2 Instance.
5. Terminate EC2 Instance.
6. Switch to main menu.
7. Exit EC2 Service Console.

=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=
        """)
        try:
            option = int(input("Please enter your option (1-7): "))

            if option == 1:
                instance_id = input("Enter your instance ID: ")
                ec2_list.append(instance_id)
                state = instance_status(ec2_list)
                print(f"\nEC2 instance '{instance_id}' is currently '{state}'.\n")
                ec2_list = []

            elif option == 2:
                instance_id = input("Enter your instance ID: ")
                ec2_list.append(instance_id)
                state = instance_status(ec2_list)
                if state != 'running':
                    setup_cli_ec2().start_instances(InstanceIds=ec2_list)
                    print(f"\nStarting EC2 Instance '{instance_id}'\n")
                else:
                    print(f"\n!!!!!!Cannot start the instance as instance '{instance_id}' is alaredy in running state.......\n'")
                ec2_list = []

            elif option == 3:
                instance_id = input("Enter your instance ID: ")
                ec2_list.append(instance_id)
                state = instance_status(ec2_list)
                if state == 'stopped':
                    print(f"\n!!!!!!Cannot stop the instance as instance '{instance_id}' is alaredy in stopped state.......\n")
                else:
                    setup_cli_ec2().stop_instances(InstanceIds=ec2_list)
                    print(f"\nStopping EC2 Instance '{instance_id}'\n")
                ec2_list = []

            elif option == 4:
                instance_id = input("Enter your instance ID: ")
                ec2_list.append(instance_id)
                setup_cli_ec2().reboot_instances(InstanceIds=ec2_list)
                print(f"\nRebooting EC2 Instance '{instance_id}'\n")
                ec2_list = []


            elif option == 5:
                instance_id = input("Enter your instance ID: ")
                ec2_list.append(instance_id)
                setup_cli_ec2().terminate_instances(InstanceIds=ec2_list)
                print(f"\nTerminating EC2 Instance '{instance_id}'\n")
                ec2_list = []

            elif option == 6:
                break

            elif option == 7:
                print(f"\nThank you for using EC2 tool.")
                print("""
=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X= 


 ####### ##   ##  ######  ##    ##  ##  ##   ##    ##  #######  ##   ##
   ##    ##   ##  ##  ##  ## #  ##  ## ##     ##  ##   ##   ##  ##   ##
   ##    #######  ######  ##  # ##  ####        ##     ##   ##  ##   ## 
   ##    ##   ##  ##  ##  ##   ###  ## ##       ##     ##   ##  ##   ##
   ##    ##   ##  ##  ##  ##    ##  ##  ##      ##     #######  #######


   Pardeep Soni
=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=  

                                                        """)
                sys.exit()

            else:
                print("\nYour option is incorrect, please enter correct choice")

        except ValueError:
            print("\nYour option is incorrect, please enter correct choice\n")

        except Exception as e:
            print(f"\n!!!!!! {e}\n")



#Deattach Security ssh inboud rule to a Security group

def deattach_sg_inbound_rule_ssh_rule(security_group_id, region_name='us-east-1'):
    sg_rule=setup_cli_ec2(region_name=region_name).SecurityGroup(security_group_id)
    sg_rule.revoke_ingress(
    CidrIp='0.0.0.0/0',
    FromPort=22,
    IpProtocol='tcp',
    ToPort=22
    )
    print(f"ssh rule revoked from '{security_group_id}'.")


#Deattach Security http inboud rule to a Security group
def deattach_sg_inbound_rule_http_rule(security_group_id,region_name='us-east-1'):
    sg_rule=setup_cli_ec2(region_name=region_name).SecurityGroup(security_group_id)
    sg_rule.revoke_ingress(
    CidrIp='0.0.0.0/0',
    FromPort=80,
    IpProtocol='tcp',
    ToPort=80
    )
    print(f"http rule revoked from '{security_group_id}'.")
