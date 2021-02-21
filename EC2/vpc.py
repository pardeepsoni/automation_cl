import boto3
from pprint import pprint
from automation_cl.setup import setup_re_ec2, setup_cli_ec2
import sys


variable={}

def create_vpc(cidr, region_name='us-east-1'):
    try:
        response = setup_cli_ec2(region_name=region_name).create_vpc(
            CidrBlock=cidr,
            AmazonProvidedIpv6CidrBlock=False,
            #Ipv6Pool='string',
            #Ipv6CidrBlock='string',
            #DryRun=True | False,
            InstanceTenancy='default',
            #Ipv6CidrBlockNetworkBorderGroup='string',
            TagSpecifications=[
                {
                    'ResourceType': 'vpc',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'UAT1-VPC-boto3'
                        },
                    ]
                },
            ]
        )
        pprint(response)
        variable['vpcid'] = response['Vpc']['VpcId']
        return response['Vpc']['VpcId']
    except Exception as e:
        print(e)



def create_subnet(vpcid):
    try:
        subnet_names = ['SubnetA-Public', 'SubnetB-Public', 'SubnetA-Private', 'SubnetB-Private']
        cidrs = ['10.0.1.0/24', '10.0.2.0/24', '10.0.3.0/24', '10.0.4.0/24']
        az=['us-east-1a','us-east-1b','us-east-1a', 'us-east-1b']

        for i in range(4):
            response = setup_cli_ec2().create_subnet(
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': subnet_names[i]
                            },
                        ]
                    },
                ],
                AvailabilityZone=az[i],
                #AvailabilityZoneId='string',
                CidrBlock=cidrs[i],
                VpcId=vpcid,

            )
            print("Subnet Created.....")
            variable[subnet_names[i]] = response['Subnet']['SubnetId']
            pprint(response)
    except Exception as e:
        print(e)


def create_internet_gateway():
    try:
        response = setup_cli_ec2().create_internet_gateway(
            TagSpecifications=[
                {
                    'ResourceType': 'internet-gateway',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'InternetGateway-boto3'
                        },
                    ]
                },
            ],
        )
        print("Internet Gateway Created...")
        pprint(response)
        variable['internet_gateway'] = response['InternetGateway']['InternetGatewayId']
    except Exception as e:
        print(e)


def attach_ig_to_vpc(vpc_id=variable.get('vpcid')):
    try:
        response = setup_cli_ec2().attach_internet_gateway(
            InternetGatewayId=variable.get('internet_gateway'),
            VpcId=vpc_id
        )
        print("Internet gateway attached")
    except Exception as e:
        print(e)


def create_route_table(route_table_name='', vpc_id = variable.get('vpcid')):
    try:
        response = setup_cli_ec2().create_route_table(
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'route-table',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': route_table_name
                        },
                    ]
                },
            ]
        )
        pprint(response)
        variable[route_table_name]= response['RouteTable']['RouteTableId']
    except Exception as e:
        print(e)

def associate_subnet_to_route_table(route_table_id, subnet_id):
    try:
        response = setup_cli_ec2().associate_route_table(
            RouteTableId=route_table_id,
            SubnetId=subnet_id,
        )
        print("Subnet is associated with the route table.")
    except Exception as e:
        print(e)



def associate_subnet_to_route_table(route_table_id, subnet_id):
    try:
        response = setup_cli_ec2().associate_route_table(
            RouteTableId=route_table_id,
            SubnetId=subnet_id,
        )
        print("Subnet is associated with the route table.")
    except Exception as e:
        print(e)


def create_route_to_ig(ig = variable.get('internet_gateway'), route_tableid = variable.get('PublicRouteTable')):
    try:
        response = setup_cli_ec2().create_route(
            DestinationCidrBlock='0.0.0.0/0',
            GatewayId=ig,
            RouteTableId=route_tableid,
        )
        print("internet route added to route table")
    except Exception as e:
        print(e)

def modify_public_ip_auto_assign_subnet(subnet_id):
    response = setup_cli_ec2().modify_subnet_attribute(
        MapPublicIpOnLaunch={
            'Value': True,
        },
        SubnetId=subnet_id,
    )
    print(f"Enable the public Ip for the subnet {subnet_id}")


def deattach_ig_from_vpc(vpc_id):
    try:
        response = setup_cli_ec2().detach_internet_gateway(
            InternetGatewayId='igw-047ae58e7c697f174',
            VpcId=vpc_id
        )
        print("Internet Gateway Deattach")

    except Exception as e:
        print(e)

def delete_internet_gateway():
    try:
        response = setup_cli_ec2().delete_internet_gateway(
            InternetGatewayId='igw-047ae58e7c697f174'
        )
        print("Internet Gateway Deleted.")

    except Exception as e:
        print(e)


def delete_vpc(vpcid):
    try:
        response = setup_cli_ec2().delete_vpc(
            VpcId=vpcid,
        )
        print(f" VPC '{vpcid}' Deleted..")
    except Exception as e:
        print(e)






create_vpc('10.0.0.0/16')
create_subnet(variable['vpcid'])
create_internet_gateway()
attach_ig_to_vpc(variable['vpcid'])
create_route_table('PrivateRouteTable',variable['vpcid'])
create_route_table('PublicRouteTable',variable['vpcid'])
associate_subnet_to_route_table(variable['PublicRouteTable'], variable['SubnetA-Public'])
associate_subnet_to_route_table(variable['PublicRouteTable'], variable['SubnetB-Public'])
associate_subnet_to_route_table(variable['PrivateRouteTable'], variable['SubnetA-Private'])
associate_subnet_to_route_table(variable['PrivateRouteTable'], variable['SubnetB-Private'])
create_route_to_ig(ig = variable.get('internet_gateway'), route_tableid = variable.get('PublicRouteTable'))
modify_public_ip_auto_assign_subnet(variable['SubnetA-Public'])
modify_public_ip_auto_assign_subnet(variable['SubnetB-Public'])

# deattach_ig_from_vpc()
# delete_internet_gateway()
#delete_vpc('vpc-09e4bdad4be60369e')