# S3 KMS Encrypt

> Be aware that this code is written to run with Python 3.6

## Description

This is a script that will take all items in an S3 bucket and copy them while applying default AWS KMS encryption to the object.
Currently this only allows default KMS encryption of objects. This was done so as to not affect the API call when retrieving objects. For more information about how AWS S3 handles Encryption at rest, [see here.](https://docs.aws.amazon.com/AmazonS3/latest/dev/serv-side-encryption.html)

The script allows the following variables to be added at run time that will alter the behaviour of the script:

- `--region` This will define the AWS region to run the script within. For more information [see here.](https://docs.aws.amazon.com/cli/latest/userguide/cli-command-line.html)
- `--profile` This is the awscli profile to use with the script. This is to allow the script to be run with difference accounts easily. For more information [see here.](https://docs.aws.amazon.com/cli/latest/userguide/cli-multiple-profiles.html)
- `--bucket-name` This is the name of the S3 bucket to run the script against.
- `--detailed-output` THis will output more useful info at the end of the script run. This includes the names of the objectst that were encrypted as well as ones that are already encrpyted.
- `--debug` This will output debug information.

## Usage

### Basic Usage

```shell
# Run script with detailed output
python s3_encrypt.py --profile ${awscli_profile} --bucket-name ${bucket_name_to_work_on} --detailed-output

# Run script with debug output
python s3_encrypt.py --profile ${awscli_profile} --bucket-name ${bucket_name_to_work_on} --debug
```

### Docker Usage

```shell
# Will first need to build the docker image based on the Dockerfile in the repo:
docker build s3_encrypt .

# Once the image has been built you can run it with:
docker run --rm --name s3_encrypt -v "$HOME/.aws/":/root/.aws/ -v "$PWD":/src/app/ -w /src/app s3_encrypt python s3_encrypt.py --profile ${awscli_profile} --bucket-name ${bucket_name}

# If you don't want to have to think about the docker commands then you can use make:
make build
make run script_profile=${awscli_profile} script_bucket=${bucket_name}
```

## Todo

- [ ] Predict Run Time Of Script
- [x] Count Number Of Objects
- [ ] Improve Testing
- [x] Summary Output
- [x] Ensure Idempotency

## License

MIT
