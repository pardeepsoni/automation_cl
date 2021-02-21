import boto3
import sys
from pprint import pprint
from automation_cl.setup import setup_cli_iam, setup_re_iam
from datetime import datetime
import random
import botocore
from automation_cl.IAM import iam_list


class IamModify:

    def __init__(self, profile_name):
        self.profile_name = profile_name

    def iam_detech_policy_from_group(self, groupname, policyarn):
        try:
            response = setup_cli_iam(self.profile_name).detach_group_policy(
                GroupName=groupname,
                PolicyArn=policyarn
            )
            print("Policy detech from group")
        except Exception as e:
            print(e)
            print("!!!! Enter Correct inputs.")

    #Remove a policy from a User.
    def iam_detech_policy_from_user(self, username, policyarn):
        try:
            response = setup_cli_iam(self.profile_name).detach_user_policy(
                UserName=username,
                PolicyArn=policyarn
            )
            print("Policy detech from user")
        except Exception as e:
            print(e)
            print("!!!! Enter Correct inputs.")

    def remove_user_from_group(self, groupname, username):
        try:
            response = setup_cli_iam(self.profile_name).remove_user_from_group(
                GroupName=groupname,
                UserName=username
            )
            print("User Successfully removed from the group.")
        except Exception as e:
            print(e)

    def list_group_for_user(self, username):
        response = setup_cli_iam(self.profile_name).list_groups_for_user(
            UserName=username,

        )
        group_count = len(response['Groups'])
        for group in response['Groups']:
            print(group['GroupName'])

        return group_count

    def iam_delete_group(self, groupname):
        try:
            response1 = setup_cli_iam(self.profile_name).get_group(
                GroupName=groupname,
            )
            if len(response1['Users']) == 0:
                x = iam_list.IamInventory.list_group_policies(self,groupname)
                if x == 0:
                    response2 = setup_cli_iam(self.profile_name).delete_group(
                        GroupName=groupname
                    )
                else:
                    for policyarn in x:
                        IamModify.iam_detech_policy_from_group(self, groupname, policyarn)

                    response3 = setup_cli_iam(self.profile_name).delete_group(
                        GroupName=groupname)
                    print(f"Group '{groupname}' Deleted")
            else:
                print("Removed attached user before deleting the group")



        except Exception as e:
            print(e)

    def iam_delete_user(self, username):
        try:
            group_count = IamModify.list_group_for_user(self,username)

            if group_count == 0:
                try:
                    response = setup_cli_iam(self.profile_name).get_login_profile(
                        UserName=username
                    )
                    setup_cli_iam(self.profile_name).delete_login_profile(
                        UserName=username
                    )
                except Exception as e:
                    pass
                try:
                    response1 = setup_cli_iam().list_attached_user_policies(
                        UserName=username,
                    )
                    if len(response1['AttachedPolicies']) == 0:
                        setup_cli_iam(self.profile_name).delete_user(
                            UserName=username
                    )
                        print(f"User '{username}' Deleted")
                    else:
                        for policy in response1['AttachedPolicies']:
                            IamModify.iam_detech_policy_from_user(self, username,policy['PolicyArn'])

                        setup_cli_iam(self.profile_name).delete_user(
                            UserName=username)
                        print(f"User '{username}' Deleted")
                except Exception as e:
                    print(e)
            else:
                print("User is attached to above group/s, please remove user from above group before deleting this user.")
        except Exception as e:
            print(e)

    def iam_delete_role(self, rolename):
        try:
            # response = setup_cli_iam(self.profile_name).get_instance_profile(
            #     InstanceProfileName=rolename
            # )
            setup_cli_iam(self.profile_name).delete_instance_profile(
                InstanceProfileName=rolename
            )
            setup_cli_iam(self.profile_name).delete_role(
                RoleName=rolename
            )
            print(f"Role '{rolename}' Deleted")

        except botocore.errorfactory.NoSuchEntityException :
            print()

