PYTHON BOTO3 AWS S3 OPERATIONS


Description:

A python script to manage s3 operations on AWS when the AWS CLI and Boto3 are already configured accordingly.


Operations:

The script.py file performs the following operations:

    -Creates a bucket specific to the Mumbai region (ap-south-1)
    -Enables versioning for the bucket
    -Uploads a set of 200 images in the bucket
    -Lists all the items of the bucket using pagination
    -Permanently deletes all versions of all files from the bucket
    -Deletes the bucket 


Pre-requisites to run:

    -An AWS Account 
    -Access to a root or an IAM user with programmatic access
    -Pre-configured AWS CLI for any of the such users
    -A python 3 interpreter with boto3 library installed


For additional information, refer to the following links:

    -How to start an AWS account : https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/
    -Create an IAM user and assign access : https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html
    -Download AWS CLI : https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
    -Configure AWS CLI : https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html