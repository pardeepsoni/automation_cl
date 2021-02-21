import boto3
import sys
from pprint import pprint
from automation_cl.setup import setup_cli_iam
from automation_cl.IAM import iam_list, iam_provision, iam_modify


iam_list_option = iam_list.IamInventory('pardeepsoni')
iam_service_creation = iam_provision.IamProvision('pardeepsoni')
iam_mod = iam_modify.IamModify('pardeepsoni')

startbanner= """

=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X= 


 ##     ##  ######  ##       ######  ######  ##     ##  ######
 ##     ##  ##      ##       ##      ##  ##  ## # # ##  ##
 ##  #  ##  ######  ##       ##      ##  ##  ##  #  ##  ######
 ## # # ##  ##      ##       ##      ##  ##  ##     ##  ##
 ##     ##  ######  #######  ######  ######  ##     ##  ######


 AWS Tool - IAM (Identity and Access Management) 
 Pardeep Soni
=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X= 
"""

endbanner= """

=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X= 


#######  ##   ##  ######  ##    ##  ##  ##   ##    ##  #######  ##   ##
   ##    ##   ##  ##  ##  ## #  ##  ## ##     ##  ##   ##   ##  ##   ##
   ##    #######  ######  ##  # ##  ####        ##     ##   ##  ##   ## 
   ##    ##   ##  ##  ##  ##   ###  ## ##       ##     ##   ##  ##   ##
   ##    ##   ##  ##  ##  ##    ##  ##  ##      ##     #######  #######


Pardeep Soni

=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=  

                                                                                """

print(startbanner)
while True:
    print("""=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=\n
 1. IAM Inventories.
 2. Provision IAM Services.
 3. Modify IAM Service.
 4. Exit the tool.\n
=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=\n""")
    try:
        stage1 = int(input("Enter your choice: "))
        if stage1 > 4:
            print("!! Wrong Input, please Enter your choice between 1 to 4")
        elif stage1 == 4:
            print(endbanner)
            sys.exit()

        elif stage1 == 1:

            while True:
                print("""\n=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=\n
 1. List All Users.
 2. List All Groups.
 3. List All Roles.
 4. List All Policies.
 5. Switch to Main Menu
 6. Exit the tool.\n
=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=\n""")
                stage2 = int(input("Enter your choice: "))
                if stage2 == 5:
                    break
                elif stage2 == 1:
                    iam_list_option.list_iam_users()

                elif stage2 == 2:
                    iam_list_option.list_iam_groups()

                elif stage2 == 3:
                    iam_list_option.list_all_roles()

                elif stage2 == 4:
                    f1= input("Enter filter criteria to extract policy. e.g S3 for all S3 related policies or "
                              "'all' for All policies : ")
                    iam_list_option.list_all_policies(f1)

                elif stage2 == 6:
                    print(endbanner)
                    sys.exit()
                else:
                    print("!! Wrong Input, please Enter your correct choice. ")


        elif stage1 == 2:
            while True:
                print("""\n=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=\n
 1. Create Group.
 2. Attach policy to a group.
 3. Create a User with console access.
 4. Add User to a Group.
 5. Attach policy to a user.
 6. Switch to Main Menu
 7. Exit the tool.\n
=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=\n""")

                stage2 = int(input("Enter your choice: "))
                if stage2 == 6:
                    break

                #1.Create Group.

                elif stage2 == 1:
                    groupname = input("Enter an unique group name: ")
                    iam_service_creation.create_group(groupname)

                #2. Attach policy to a group.

                elif stage2 == 2:
                    groupname = input("Enter the  group name: ")
                    policyarn = input("Enter the Policy ARN to attach: ")
                    iam_service_creation.attach_policy_to_group(groupname,policyarn)

                #3. Create a User with console access.

                elif stage2 == 3:
                    username = input("Enter an unique username: ")
                    uname=iam_service_creation.create_user(username)
                    iam_service_creation.user_login_profile(uname)

                # 4. Add User to a Group.
                elif stage2 == 4:
                    groupname = input("Enter group name: ")
                    username = input("Enter username: ")
                    iam_service_creation.add_user_to_group(groupname,username)

                # 5. Attach policy to a user.
                elif stage2 == 5:
                    username = input("Enter username: ")
                    policyarn = input("Enter Policy's ARN to attach: ")
                    iam_service_creation.add_policy_to_user(policyarn, username)

                elif stage2 == 7:
                    print(endbanner)
                    sys.exit()

                else:
                    print("!! Wrong Input, please Enter correct choice.")

        elif stage1 == 3:
            while True:
                print("""\n=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=\n
 1. Delete Group.
 2. Delete User.
 3. Delete Role.
 4. Remove a policy from a Group.
 5. Attach policy to a Group.
 6. Remove a policy from a User.
 7. Attach policy to a User.
 8. Remove User from a group.
 9. Switch to Main Menu
 10. Exit the tool.\n
=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=\n""")
                stage3 = int(input("Enter your choice: "))
                if stage3 == 9:
                    break

                #1.Delete Group.

                elif stage3 == 1:
                    groupname = input("Enter the unique group name: ")
                    option = input("Are you sure, you want to delete group.(y/n): ")
                    if option.lower() == 'y':
                        iam_mod.iam_delete_group(groupname)
                    else:
                        break

                #2. Delete User.

                elif stage3 == 2:
                    username = input("Enter the  user name: ")
                    iam_mod.iam_delete_user(username)

                #3. Delete Role.

                elif stage3 == 3:
                    rolename = input("Enter the rolename: ")
                    print("Feature yet to build.")

                # 4. Remove a policy from a Group.
                elif stage3 == 4:
                    groupname = input("Enter group name: ")
                    policyarn = input("Enter Policy's ARN to attach: ")
                    iam_mod.iam_detech_policy_from_group(groupname,policyarn)

                # 5. Attach policy to a Group.
                elif stage3 == 5:
                    username = input("Enter username: ")
                    policyarn = input("Enter Policy ARN to attach: ")
                    iam_service_creation.add_policy_to_user(policyarn, username)

                # 6. Remove a policy from a User.
                elif stage3 == 6:
                    username = input("Enter username: ")
                    policyarn = input("Enter Policy's ARN to attach: ")
                    iam_mod.iam_detech_policy_from_user(policyarn, username)

                # 7. Attach policy to a Group.
                elif stage3 == 7:
                    username = input("Enter the username: ")
                    policyarn = input("Enter Policy's ARN to attach: ")
                    iam_service_creation.add_policy_to_user(policyarn, username)

                elif stage3 == 8:
                    username = input("Enter the username: ")
                    groupname = input("Enter group name: ")
                    iam_mod.remove_user_from_group(groupname,username)

                elif stage3 == 10:
                    print(endbanner)
                    sys.exit()
                else:
                    print("!! Wrong Input, please Enter correct choice.")

    except Exception as e:
        print("!! Wrong Input, please enter your correct choice")
        print(e)


