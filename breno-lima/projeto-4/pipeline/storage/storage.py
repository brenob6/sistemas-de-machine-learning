from . import s3, BUCKET_NAME


class Storage:
    def __init__(self):
        self.RAW = "raw"
        self.PROCESSED = "processed"
        self.extracted = "extracted"

    def access_processed(self, hash: str) -> str:
        return f"s3://{BUCKET_NAME}/{self.PROCESSED}/{hash}.md"

    def upload_raw(self, filename: str, hash: str):
        s3.upload_file(
            Filename=filename,
            Bucket=BUCKET_NAME,
            Key=f"{self.RAW}/{hash}.pdf",
        )

    def upload_processed(
        self,
        file_content: str,
    ):
        s3.put_object(
            Body=file_content.encode("utf-8"),
            Bucket=BUCKET_NAME,
            Key=f"{self.PROCESSED}/{hash}.md",
        )

    def upload_extracted(self, json_content: str, hash: str):
        s3.put_object(
            Body=json_content.encode("utf-8"),
            Bucket=BUCKET_NAME,
            Key=f"{self.extracted}/{hash}.json",
        )


storage = Storage()
