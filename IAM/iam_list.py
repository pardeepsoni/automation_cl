import boto3
import sys
from pprint import pprint
from AWS.setup import setup_cli_iam, setup_re_iam
from datetime import datetime
import re


class IamInventory:
    user_group = {}

    def __init__(self, profile_name):
        self.profile_name = profile_name


# Return the dictionary of username and group name
    def list_iam_group(self, group_name):
        message_output=setup_cli_iam(self.profile_name).get_group(
            GroupName=group_name,
        )
        count = 1
        for each_user in message_output['Users']:
            IamInventory(self.profile_name).user_group[each_user['UserName']] = group_name
            count += 1
        return IamInventory(self.profile_name).user_group

    def all_groups_user_dict(self):
        paginator = setup_cli_iam(self.profile_name).get_paginator('list_groups')
        response_iterator = paginator.paginate()
        for each_page in response_iterator:
            for each_group in each_page['Groups']:
                group_name = each_group['GroupName']
                IamInventory(self.profile_name).list_iam_group(group_name)
        return IamInventory(self.profile_name).user_group

    def list_iam_users(self):
        paginator = setup_cli_iam(self.profile_name).get_paginator('list_users')
        message_output = paginator.paginate()
        user_group = IamInventory(self.profile_name).all_groups_user_dict()
        count = 1
        print("\nUser information is as follows:\n")
        for each_page in message_output:
            for each_user in each_page['Users']:

                print(f"{count}. UserName : {each_user['UserName']}, UserId : {each_user['UserId']}, "
                      f"Group Name: {user_group.get(each_user['UserName'])}, "
                      f"CreationDate : {each_user['CreateDate'].strftime('%d-%b-%Y')}, ")

                count += 1

    def list_iam_groups(self):
        paginator = setup_cli_iam(self.profile_name).get_paginator('list_groups')
        response_iterator = paginator.paginate()
        count = 1
        print("\nGroup information is as follows:\n")
        for each_page in response_iterator:
            for each_group in each_page['Groups']:
                print(f"{count}. {each_group['GroupName']}")
                count += 1

    def list_all_policies(self, pattern_to_filter="all"):
        try:
            paginator = setup_cli_iam(self.profile_name).get_paginator('list_policies')
            response_iterator = paginator.paginate()
            count = 1
            filter = pattern_to_filter.lower()
            print("\nUser Policy information is as follows:\n")
            for each_policy in response_iterator:
                for policy in each_policy['Policies']:
                    if pattern_to_filter != "all":
                        x = re.search(filter, policy['PolicyName'].lower())
                        if x is not None:
                            print(f"{count}. {policy['PolicyName']} | {policy['Arn']}")
                            count += 1
                    else:
                        print(f"{count}. {policy['PolicyName']} | {policy['Arn']}")
                        count += 1
        except Exception as e:
            print(e)


    def list_all_roles(self):
        try:
            paginator = setup_cli_iam(self.profile_name).get_paginator('list_roles')
            response_iterator = paginator.paginate()
            print("Requested Roles information is as follows:\nRole Name, Role Id, Role Arn\n")
            count =1
            for page in response_iterator:
                for role in page["Roles"]:
                    print(f"{count}. {role['RoleName']}, {role['RoleId']}, {role['Arn']}")
                    count += 1
        except Exception as e:
            print(e)

    def list_group_policies(self, groupname):
        response = setup_cli_iam(self.profile_name).list_attached_group_policies(
            GroupName=groupname,

        )
        policy_count = len(response['AttachedPolicies'])
        if policy_count > 0:
            policy_list = []
            for arn in response['AttachedPolicies']:
                policy_list.append(arn['PolicyArn'])
            return policy_list
        else:
            return policy_count












iam = IamInventory('pardeepsoni')
# iam.list_iam_groups()
# print("============================")
# iam.list_iam_users()
# print("============================")
# iam.list_all_policies('admin')
#iam.list_all_roles()
#print(iam.list_group_policies('iamgroup'))



