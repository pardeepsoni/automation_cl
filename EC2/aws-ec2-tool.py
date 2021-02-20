import sys
import AWS.EC2.ec2_services_list as aws_list
import AWS.EC2.ec2_service_modify as aws_mod
import AWS.EC2.ec2_service_create as aws_create


print("""

=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X= 


 ##     ##  ######  ##       ######  ######  ##     ##  ######
 ##     ##  ##      ##       ##      ##  ##  ## # # ##  ##
 ##  #  ##  ######  ##       ##      ##  ##  ##  #  ##  ######
 ## # # ##  ##      ##       ##      ##  ##  ##     ##  ##
 ##     ##  ######  #######  ######  ######  ##     ##  ######


 AWS Tool - EC2 Services
 Pardeep Soni
=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X=X= 
""")

while True:
    print("""\n=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=
    
 1. List EC2 Services.
 2. Create EC2 Services.
 3. Modify EC2 Services.
 4. Exit EC2 Service Console.

=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=
    """)
    try:
        stage1 = int(input("Enter your choice: "))
        if stage1 > 4:
            print("!! Wrong Input, please Enter your choice between 1 to 4")
        elif stage1 == 4:
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

        elif stage1 == 1:
            region_name = input("Enter your region: ")
            while True:
                print("""\n=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=
                
 1. List all EC2 Machines.
 2. List all Security Groups.
 3. List all Launch Templates.
 4. List all volumes.
 5. List all snapshots.
 6. Switch to main menu.
 7. Exit EC2 Service Console.
 
=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=
                    """)

                stage2 = int(input("Enter your choice: "))
                if stage2 == 6:
                    break
                elif stage2 == 1:
                    aws_list.list_all_ec2(region_name)

                elif stage2 == 2:
                    aws_list.list_all_sg(region_name)

                elif stage2 == 3:
                    aws_list.list_all_template(region_name)

                elif stage2 == 4:
                    aws_list.list_volumes(region_name)

                elif stage2 == 5:
                    aws_list.list_snapshots(region_name)

                elif stage2 == 7:
                    print("Thank you for using the tool.")
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


        elif stage1 == 2:
            region_name = input("Enter your region: ")
            while True:
                print("""\n=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=
                
 1. Provision EC2 Machines.
 2. Provision Security Groups.
 3. Attach inbound rule to a Security Group.
 4. Provision Launch Templates.
 5. Provision volumes.
 6. Provision snapshots.
 7. Switch to main menu.
 8. Exit EC2 Service Console.

=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=x=
                                """)

                stage2 = int(input("Enter your choice: "))
                if stage2 == 7:
                    break

                elif stage2 == 1:
                    lauch_template_id = input("Enter the id of the launch template: ")
                    instance_count_to_create = int(input("Enter the number of ec2 to be provison: "))
                    aws_create.create_ec2_from_launch_template(lauch_template_id, instance_count_to_create,
                                                               region_name=region_name )

                elif stage2 == 2:
                    sg_name = input("Enter the name of Security Group: ")
                    aws_create.create_sg(sg_name,region_name)

                elif stage2 == 3:
                    exception_list = [22, 3389, 1521]
                    sg_id = input("Enter Security Group ID: ")
                    cidr = input("Enter valid Cidr IpRang e.g. 10.0.0.22/32: ")
                    from_port = int(input("Enter valid From port e.g. 22 for SSH: "))
                    if cidr == '0.0.0.0/0' and from_port in exception_list:
                        print(f"!!!Alert you can't open port '{from_port}'' to public, "
                              f"Please contact Security team for an Exception request.")
                        # sys.exit()
                        break
                    to_port = int(input("Enter valid To port: e.g. 22 for SSH: "))
                    ip_protocol = input("Enter valid IP Protocol, e.g. tcp , udp , icmp , icmpv6: ")
                    aws_create.ingress_rule(sg_id,from_port,ip_protocol,cidr,to_port)

                elif stage2 == 4:
                    aws_create.create_launch_template(region_name)

                elif stage2 == 5:
                    aws_create.create_volume(region_name)

                elif stage2 == 6:
                    aws_create.create_snapshot(region_name)
                elif stage2 == 8:
                    print("Thank you for using the tool")
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


        elif stage1 == 3:
            region_name = input("Enter your region: ")
            aws_mod.ec2_operation()


    except Exception as e:
        print("!! Wrong Input, please enter your correct choice")
        print(e)




