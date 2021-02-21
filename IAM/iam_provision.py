import boto3
import sys
from pprint import pprint
from automation_cl.setup import setup_cli_iam, setup_re_iam
from datetime import datetime
import re
import random


class IamProvision:
    def __init__(self, profile_name):
        self.profile_name = profile_name

    def create_user(self, username):
        try:
            message_output = setup_cli_iam(self.profile_name).create_user(
                UserName=username,
                #PermissionsBoundary='string',
                # Tags=[
                #     {
                #         'Key': 'string',
                #         'Value': 'string'
                #     },
                #]
            )
            output = f"User/User Id : {message_output['User']['UserName']}/{message_output['User']['UserId']} Created."
        except Exception as e:
            print(e)
        #print(output)
        return username

    def create_random_password(self):
        st1="1234567890"
        st2="!@#$%^&*()_+{}|[]"
        st3="qwertyuiopasdfghjklzxcvbnm"
        st4="QEWRTYUIOPLKJHGFDSAZXCVBNM"
        password = ''
        for i in range(1, 4):
            password = password + random.choice(st3)
        for i in range(1, 4):
            password = password + random.choice(st2)
        for i in range(1, 3):
            password = password + random.choice(st1)
        for i in range(1, 3):
            password = password + random.choice(st4)
        return password

    def user_login_profile(self, username):
        password = IamProvision(self.profile_name).create_random_password()
        response = setup_cli_iam(self.profile_name).create_login_profile(
            UserName=username,
            Password = password,
            PasswordResetRequired=True
        )
        print(f"Username: '{username}' with password : {password} is created.")

    def add_user_to_group(self,groupname, username):
        try:
            output = setup_cli_iam(self.profile_name).add_user_to_group(
                GroupName=groupname,
                UserName=username
            )
            print("User added to the Group")
        except Exception as e:
            print(e)


    def add_policy_to_user(self,username,policyarn):
        try:
            output = setup_cli_iam(self.profile_name).attach_user_policy(
                    UserName=username,
                    PolicyArn=policyarn
            )
            print("Policy added to the User")
        except Exception as e:
            print(e)


    def create_group(self, groupname):
        try:
            message_output = setup_cli_iam(self.profile_name).create_group(
                #Path='string',
                GroupName=groupname
            )
            output = f"Group '{message_output['Group']['GroupName']}' created"
        except Exception as e:
            print(e)
        return output

    def attach_policy_to_group(self, groupname, policy_arn):
        try:
            message_output = setup_cli_iam(self.profile_name).attach_group_policy(
                GroupName=groupname,
                PolicyArn=policy_arn
            )
            print(f"Policy attached to {groupname}.....")
        except Exception as e:
            print(e)



iam_create = IamProvision('pardeepsoni')

# a=iam_service_creation.create_user("testu")
#
# iam_service_creation.user_login_profile(a)

# iam_service_creation.create_random_password()