import boto3
import datetime
import re
import argparse

s3 = boto3.client('s3')
bucket = boto3.resource('s3')
ce = boto3.client('ce')

parser = argparse.ArgumentParser()
parser.add_argument('--days', type=int, default=30)
args = parser.parse_args()

now = datetime.datetime.utcnow()
end = datetime.datetime(year=now.year, month=now.month, day=30)
start = now.strftime('%Y-%m-%d')
end = end.strftime('%Y-%m-%d')
cd = boto3.client('ce')

results = []

token = None
while True:
    if token:
        kwargs = {'NextPageToken': token}
    else:
        kwargs = {}
    data = cd.get_cost_and_usage(TimePeriod={'Start': start, 'End':  end}, Granularity='DAILY', Metrics=['UnblendedCost'], GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}])
    results += data['ResultsByTime']
    token = data.get('NextPageToken')
    if not token:
        break

print('Total cost')
for result_by_time in results:
    for group in result_by_time['Groups']:
        amount = group['Metrics']['UnblendedCost']['Amount']
        unit = group['Metrics']['UnblendedCost']['Unit']
        if '\t'.join(group['Keys']) == 'Amazon Simple Storage Service':
            print(result_by_time['TimePeriod']['Start'], '\t'.join(group['Keys']),' $', amount, '\n')

print('Existing buckets:\n')
for i in s3.list_buckets()['Buckets']:
    name = i["Name"]
    creationDate = i["CreationDate"]
    print("Bucket name: " , name , "\nCreationDate: " , str(creationDate)) 

    for object in bucket.Bucket(i["Name"]).objects.all():
        print("File: " , str(object.key) , " " ,str(object.size) , "KB" , " | Last modified: " , str(object.last_modified))
    print("\n")

    


