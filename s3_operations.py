import boto3
from pprint import pprint
import csv
import json

def s3_setup():
    aws_client= boto3.session.Session(profile_name='pardeepsoni')
    s3_client= aws_client.client(service_name='s3', region_name='us-east-1')
    return s3_client

def list_all_bucket():
    bucket_list=[]
    buckets = s3_setup().list_buckets()['Buckets']
    for each_bucket in buckets:
        bucket_list.append(each_bucket['Name'])
    return bucket_list

def list_all_objects():
    bucket_names = list_all_bucket()
    for each_bucket in bucket_names:
        response=s3_setup().list_objects(Bucket=each_bucket)
        print(f"\nbucket_name = {each_bucket},\n===============================")
        try:
            for obj in (response['Contents']):
                if obj['Size'] !=0:
                    print(obj.get('Key'))
        except KeyError:
            print(f'{each_bucket} is empty')


#s3_setup().download_file('pardeepsoni', 'username-password.xlsx', '/tmp/username-password.xlsx')


with open('filename', 'wb') as data:
    response=s3_setup().download_fileobj('pardeepsoni', 'username-password.xlsx', data)
    files=data.close()

with open(data, 'r') as file:
    file.read()


#
# response=s3_setup().get_object(Bucket='pardeepsoni',Key='username-password.xlsx')




# with open('/Users/soni/Documents/PS/Study/R/cricket-data.csv', 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         print(",".join(row))

#list_all_objects()



