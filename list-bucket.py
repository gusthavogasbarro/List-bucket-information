import boto3, datetime

s3 = boto3.client('s3')
bucket = boto3.resource('s3')

print('Existing buckets:\n')
for i in s3.list_buckets()['Buckets']:
    name = i["Name"]
    creationDate = i["CreationDate"]
    print("Bucket name: " + name + "\nCreationDate: " + str(creationDate)) 

    for object in bucket.Bucket(i["Name"]).objects.all():  
        print("File: " + str(object.key) + " " +str(object.size) + "KB" + "\nLast modified: " + str(object.last_modified))

    print("\n")


