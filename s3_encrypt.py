#!/user/bin/env python3
"""
s3_encrypt
  Takes all the objects in a bucket, reencrypts them with KMS and reuploads.

DavyJ0nes 2017
"""

import argparse
import sys
import boto3


def main():
    """main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', action='store',
                        dest='region', default='eu-west-1')
    parser.add_argument('--profile', action='store',
                        dest='profile', default='default')
    parser.add_argument('--bucket-name', action='store',
                        dest='bucket_name', required=True)
    args = parser.parse_args()

    # set boto session parameters
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    s3client = session.client('s3')
    s3resource = session.resource('s3')

    # Checking if bucket exists
    if args.bucket_name not in list_buckets(s3resource):
        print("Bucket: {} does not exist".format(args.bucket_name))
        sys.exit(1)

    bucket_objects = get_bucket_objects(s3resource, args.bucket_name)
    copy_object_with_encryption(s3client, args.bucket_name, bucket_objects)


def list_buckets(s3client):
    """lists buckets in region"""
    bucket_list = []
    for bucket in s3client.buckets.all():
        bucket_list.append(bucket.name)

    return bucket_list


def get_bucket_objects(s3client, bucket_name):
    """gets objects from bucket"""
    bucket = s3client.Bucket(bucket_name)

    bucket_object_list = []
    for obj in bucket.objects.all():
        if not obj.key.endswith('/'):
            obj_fullinfo = s3client.Object(bucket_name, obj.key)
            bucket_object_list.append(obj_fullinfo)

    return bucket_object_list


def copy_object_with_encryption(s3client, bucket, objects):
    """Copies list of objects in place with encryption"""
    for obj in objects:
        if obj.server_side_encryption is None:
            copy_source = {
                'Bucket': bucket,
                'Key': obj.key
            }

            resp = s3client.copy_object(
                Bucket=bucket,
                CopySource=copy_source,
                Key=obj.key,
                ServerSideEncryption='aws:kms'
            )

            print("Object Name:       {}".format(obj.key))
            print("Object Encryption: {}".format(resp['ServerSideEncryption']))
        else:
            print("Object {} already encrypted".format(obj.key))

        print("--------------------")

    return True


if __name__ == "__main__":
    main()
