import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://storage:9000",
    aws_access_key_id="rustfsadmin",
    aws_secret_access_key="rustfsadmin",
)

BUCKET_NAME = "documents"

try:
    s3.create_bucket(Bucket=BUCKET_NAME)
    print(f"Bucket '{BUCKET_NAME}' criado com sucesso.")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print(f"Bucket '{BUCKET_NAME}' já existe e é de sua propriedade.")
