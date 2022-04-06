import boto3
from pprint import pprint
import botocore.exceptions
import time


s3=boto3.client('s3')
name="adarsh"
bucket_name=f"watchguard-infrared-cloud-bucket-training-{name}"
topic="arn:aws:sns:ap-south-1:434758973508:boto3"


def change_name():
    print("Enter the name you want your S3 buckets to associate to: ")
    global name
    global bucket_name
    x=input()
    name=x
    bucket_name=f"watchguard-infrared-cloud-bucket-training-{name}"

def publish(message, subject):
    try:
        sns=boto3.client('sns')
        sns.publish(TopicArn=topic,
                Message=message,
                Subject=subject
        )
    except:
        print("Failed to send email. Returning to the function...")
        return

def create_bucket():
    print("\nCreating bucket:\n")
    try:
        response = s3.create_bucket(
        Bucket= bucket_name,
        CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1',
            },
        )
        print(f"Created bucket {bucket_name} successfully\nwith response {response}")
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'InvalidBucketName':
            print("Can't have this name for the bucket. Remember it should not contain capital letters!")
        elif error.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            print('This bucket is already owned by you')
        elif error.response['Error']['Code'] == 'BucketAlreadyExists': 
            message=f"The bucket that you tried to create, namely '{bucket_name}' already exists somewhere globally and thus can't be created."
            subject="Can't create S3 Bucket"
            publish(message, subject)
            raise error
        else:
            raise error


def enable_versioning():
    print("\nEnabling versioning:\n")
    try:
        s3_resource=boto3.resource('s3')
        versioning = s3_resource.BucketVersioning(bucket_name)
        versioning.enable()
        if(versioning.status):
            print("Versioning enabled successfully!")
    except:
        print('Check bucket name')


def upload_items():
    print("\nUploading items:\n")
    try:
        for i in range(201):
            response = s3.upload_file('download.jpg', bucket_name, f'images/doge_{i}.jpg')
            print(f"File uploaded successfully\nwith response {response}")

    except:
        raise


def list_items():
    print("\nListing all items:\n")
    try:
        paginator=s3.get_paginator('list_objects')
        page_iterator = paginator.paginate(Bucket=bucket_name)
        for page in page_iterator:
            pprint(page['Contents'])
    except:
        raise


def delete_items():
    print("\nDeleting all times:\n")
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)

    for i in range(201):
        object_key=f'images/doge_{i}.jpg'
        try:
            if object_key:
                bucket.object_versions.filter(Prefix=object_key).delete()
                print(f"Permanently deleted all versions of object {object_key} in {bucket_name}", )
            else:
                bucket.object_versions.delete()
                print(f"Permanently deleted all versions of all objects in {bucket_name}")
        except botocore.exceptions.ClientError:
            print(f"Couldn't delete all versions of {object_key} in {bucket_name}")
            raise


def delete_bucket():
    print("\nDeleting the bucket:\n")
    try:
        response = s3.delete_bucket(
                    Bucket=bucket_name,)
        print(f"Deleted {bucket_name} successfully\nwith response {response}")
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'NoSuchBucket':
            print("The Bucket does not seem to exist. Kindly check again")
        elif error.response['Error']['Code'] == 'BucketNotEmpty':
            print("The Bucket does not seem to be empty. Kindly check again\nNOTE: Ensure that all versions of the file are deleted as well.")
        else:
            raise error


def everything_in_sequence():
    create_bucket()
    enable_versioning()
    upload_items()
    list_items() 
    delete_items()
    delete_bucket()


execute={
    1 : create_bucket,
    2 : enable_versioning,
    3 : upload_items,
    4 : list_items,
    5 : delete_items,
    6 : delete_bucket,
    7 : everything_in_sequence,
    8 : change_name
}


if __name__=='__main__':
    PROMPT="""Choose your operation:
    1. Create a bucket
    2. Enable versioning in the bucket
    3. Upload files
    4. List files
    5. Delete all files
    6. Delete the bucket
    7. Everything in sequence
    8. Change your default name

    Anything else: To quit
    """
    execute[8]()
    time.sleep(1)

    while(True):
        print(PROMPT)
        choice=int(input())
        try:
            execute[choice]()
            if choice==7:
                print("\nAll operations completed successfully!\n")
            time.sleep(2)
        except KeyError as error:
            break
