import random
import boto3
from automation_cl.setup import setup_re_ec2, setup_cli_ec2
from pprint import pprint
import sys



class SecurityAudit:

    def __init__(self, profile_name):
        self.profile_name = profile_name

    def testsg(self):
        security_groups = setup_re_ec2(self.profile_name).security_groups.all()
        for each_sg in security_groups:
            print(each_sg.group_id, each_sg.id)
            for iprule in each_sg.ip_permissions:
                pprint(iprule)
                break
                print(iprule.get('FromPort'))
                for ip in iprule.get('IpRanges'):
                    print(ip.get('CidrIp'))
            print("===================")

    def sg_violation(self):
        security_groups = setup_re_ec2(self.profile_name).security_groups.all()
        violation_list =[]
        for each_sg in security_groups:
            for iprule in each_sg.ip_permissions:
                #print(type(iprule.get('FromPort')))
                for ip in iprule.get('IpRanges'):
                    if ip.get('CidrIp') == '0.0.0.0/0':
                            if iprule.get('FromPort') == 22 or iprule.get('FromPort') == 80:
                                dict={}
                                dict['group_name']=each_sg.group_name
                                dict['group_id'] = each_sg.group_id
                                dict['FromPort'] = iprule.get('FromPort')
                                dict['ToPort'] = iprule.get('ToPort')
                                dict['IpProtocol'] = iprule.get('IpProtocol')
                                dict['CidrIp'] = ip.get('CidrIp')
                                # print(each_sg.group_name, each_sg.group_id, iprule.get('FromPort'), ip.get('CidrIp'),
                                #       iprule.get('ToPort'),iprule.get('IpProtocol'))
                                violation_list.append(dict)
        return violation_list

    def revoke_sg_violated_ingress_rule(self, sg_id,from_port, to_port, ip_protocol):
        security_group = setup_re_ec2(self.profile_name).SecurityGroup(sg_id)
        response = security_group.revoke_ingress(
            CidrIp='0.0.0.0/0',
            FromPort=from_port,
            IpProtocol=ip_protocol,
            ToPort=to_port
        )
        pprint(response)
        print("rule revoked")

    def attach_ingress_rule_to_sg_with_cidr(self, sg_id, cidr, from_port, to_port, ip_protocol):
        try:
            response = setup_cli_ec2(self.profile_name).authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        'FromPort': from_port,
                        'IpProtocol': ip_protocol,
                        'IpRanges': [
                            {
                                'CidrIp': cidr,
                                'Description': 'boto3 rule'
                            },
                        ],

                        'ToPort': to_port,

                    },
                ],

            )
        except Exception as e:
            print(e)



def ingress_rule():
    exception_list = [22, 3389, 1521]
    sg_id = input("Enter Security Group ID: ")
    cidr = input("Enter valid Cidr IpRang e.g. 10.0.0.22/32: ")
    from_port = int(input("Enter valid From port e.g. 22 for SSH: "))
    if cidr == '0.0.0.0/0' and from_port in exception_list:
        print(f"!!!Alert you can't open port '{from_port}'' to public, "
              f"Please contact Security team for an Exception request.")
        sys.exit()
    to_port = int(input("Enter valid To port: e.g. 22 for SSH: "))
    ip_protocol = input("Enter valid IP Protocol, e.g. tcp , udp , icmp , icmpv6: ")
    SecurityAudit('pardeepsoni').attach_ingress_rule_to_sg_with_cidr(sg_id, cidr, from_port, to_port, ip_protocol)
    print("Rule attached to security group.")

