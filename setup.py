import boto3



def setup_re_ec2(profile_name='pardeepsoni', region_name='us-east-1'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    ec2_console_re = aws_console.resource(service_name='ec2', region_name=region_name)
    return ec2_console_re


def setup_cli_ec2(profile_name='pardeepsoni', region_name ='us-east-1'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    ec2_console_cli = aws_console.client(service_name='ec2',region_name=region_name)
    return ec2_console_cli


def setup_cli_s3(profile_name='pardeepsoni', region_name ='us-east-1'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    s3_console = aws_console.client(service_name='s3', region_name=region_name)
    return s3_console


def setup_cli_iam(profile_name='pardeepsoni', region_name='us-east-1'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    iam_console = aws_console.client(service_name='iam')
    return  iam_console


def setup_re_iam(profile_name='pardeepsoni', region_name='us-east-1'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    iam_console_re = aws_console.resource(service_name='iam', region_name=region_name)
    return  iam_console_re


def setup_cli_elb(profile_name='pardeepsoni', region_name='us-east-1'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    elb_console = aws_console.client(service_name='elbv2')
    return  elb_console


def setup_cli_asg(profile_name='pardeepsoni', region_name='us-east-1'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    asg_console = aws_console.client(service_name='autoscaling')
    return  asg_console


def setup_cli_rds(profile_name='pardeepsoni', region_name='us-east-1'):
    aws_console = boto3.session.Session(profile_name=profile_name)
    rds_console = aws_console.client(service_name='rds')
    return rds_console




