import boto3
from pprint import pprint
import sys


aws_console= boto3.session.Session(profile_name='root')
cli_org = aws_console.client(service_name='organizations')


def create_org():
    response=cli_org.create_organization(
    FeatureSet='ALL'
    )
    pprint(response)


def create_ou(ou_name):
    response = cli_org.create_organizational_unit(
        ParentId='r-xde5',
        Name=ou_name,
    )
    pprint(response)


def creats_ous():
    ou_names = ['Test', 'Dev', 'UAT', 'SIT',
                'Phase1', 'Lab', 'Phase2', 'Prod1', 'UnitTest']
    for ou_name in ou_names:
        create_ou(ou_name)


def list_all_ous():
    response = cli_org.list_organizational_units_for_parent(
        ParentId='r-xde5',
        MaxResults=20
    )
    ou_ids= []
    for each_ou in response['OrganizationalUnits']:
        print(f"Name: {each_ou['Name']} | ARN: {each_ou['Arn']} | OU_ID: {each_ou['Id']} ")
        ou_ids.append(each_ou.get('Id'))
    print(ou_ids)



def list_child_org():
    response = cli_org.list_children(
        ParentId='r-xde5',
        #option: 'ACCOUNT' | 'ORGANIZATIONAL_UNIT',
        ChildType='ORGANIZATIONAL_UNIT',
        MaxResults=20
    )
    pprint(response)



def del_ous(ou_ids_list):

    for ou_id in ou_ids_list:
        response = cli_org.delete_organizational_unit(
        OrganizationalUnitId=ou_id)

        print(f"OU_id '{ou_id}' Deleted")

def create_account():
    response = cli_org.create_account(
        Email='ps###@gmail.com',
        AccountName='Test123',
        #RoleName='string',
        IamUserAccessToBilling='DENY'
    )

def remove_account():
    response = cli_org.remove_account_from_organization(
        AccountId='070767131738')


def move_account():
    response = cli_org.move_account(
        AccountId='070767131738',
        SourceParentId='r-xde5',
        DestinationParentId='ou-xde5-anmz281h'
    )


#move_account()
#remove_account()
#create_account()
#creats_ous()
#list_all_ous()
ou_ids_list=['ou-xde5-6hdwrunr', 'ou-xde5-bre0kb5u', 'ou-xde5-0jva0ck9', 'ou-xde5-r65fg1ww', 'ou-xde5-2980gtl8', 'ou-xde5-hp5yr7x2', 'ou-xde5-a3r8m6zj', 'ou-xde5-kv4rqsh5', 'ou-xde5-lpz1l9gh']

del_ous(ou_ids_list)