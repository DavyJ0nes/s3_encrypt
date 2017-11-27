#!/user/bin/env python3
"""
s3_encrypt
  Takes all the objects in a bucket, reencrypts them with KMS and reuploads.

DavyJ0nes 2017
"""

import argparse
import logging
import sys
import boto3


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger('s3_encrypt')


def main():
    """main function"""
    # Set up Command Line Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--region', action='store', dest='region', default='eu-west-1')
    parser.add_argument('--profile', action='store', dest='profile', default='default')
    parser.add_argument('--bucket-name', action='store', dest='bucket_name', required=True)
    parser.add_argument('--detailed-output', action='store_true', dest='detailed_output', default=False)
    parser.add_argument('--debug', action='store_true', dest='debug', default=False)
    args = parser.parse_args()

    # Set up Debug Logging
    if args.debug:
        LOGGER.setLevel(logging.DEBUG)

    # Set up boto Session Parameters
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    s3client = session.client('s3')
    s3resource = session.resource('s3')

    # Checking if bucket exists
    if args.bucket_name not in list_buckets(s3resource):
        print("Bucket: {} does not exist".format(args.bucket_name))
        sys.exit(1)

    LOGGER.debug('Getting buckets')
    bucket_objects = get_bucket_objects(s3resource, args.bucket_name)

    LOGGER.debug("Working over %d objects", len(bucket_objects))
    summary = copy_object_with_encryption(
        s3client, args.bucket_name, bucket_objects
    )

    print("===================================================================")
    print("============================= SUMMARY =============================")
    print("Already Encrypted:    {}".format(len(summary['already_encrypted'])))
    print("Copied and Encrypted: {}".format(
        len(summary['copied_and_encrypted'])))
    print("===================================================================")
    if args.detailed_output:
        print("==================== OBJECTS ALREADY ENCRYPTED ====================")
        for oae in summary['already_encrypted']:
            print("Name: %25s\tEncryption: %10s" % (oae['key'], oae['sse']))
        print("====================== COPIED AND ENCRYPTED =======================")
        for cae in summary['copied_and_encrypted']:
            print("Name: %25s\tEncryption: %10s" % (cae['key'], cae['sse']))


def list_buckets(s3client):
    """lists buckets in region"""
    LOGGER.debug('Starting: list_buckets')
    bucket_list = []
    for bucket in s3client.buckets.all():
        bucket_list.append(bucket.name)

    return bucket_list


def get_bucket_objects(s3client, bucket_name):
    """gets objects from bucket"""
    LOGGER.debug('Starting: get_bucket_objects')
    bucket = s3client.Bucket(bucket_name)

    bucket_object_list = []
    for obj in bucket.objects.all():
        if not obj.key.endswith('/'):
            obj_fullinfo = s3client.Object(bucket_name, obj.key)
            bucket_object_list.append(obj_fullinfo)

    return bucket_object_list


def copy_object_with_encryption(s3client, bucket, objects):
    """Copies list of objects in place with encryption"""
    LOGGER.debug('Starting: copy_object_with_encryption')
    already_encrypted = []
    copied_and_encrypted = []

    for obj in objects:
        LOGGER.debug('Object: %s', obj.key)
        if obj.server_side_encryption is None:
            LOGGER.debug('Encrypting object: %s', obj.key)
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

            copied_and_encrypted.append({
                "key": obj.key,
                "sse": resp['ServerSideEncryption']
            })
        else:
            LOGGER.debug('Object already encrypted: %s', obj.key)
            already_encrypted.append({
                "key": obj.key,
                "sse": obj.server_side_encryption
            })

    return {
        "already_encrypted": already_encrypted,
        "copied_and_encrypted": copied_and_encrypted
    }


if __name__ == "__main__":
    main()
