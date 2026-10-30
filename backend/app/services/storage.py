import json
import logging
import time
import uuid

import boto3
import httpx
from botocore.client import Config
from botocore.exceptions import ClientError, ConnectionClosedError

from app.core.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self) -> None:
        self._client = boto3.client(
            "s3",
            endpoint_url=self._endpoint_url(),
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
            config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
            region_name="us-east-1",
        )
        self._bucket = settings.minio_bucket

    @staticmethod
    def _endpoint_url() -> str:
        scheme = "https" if settings.minio_use_ssl else "http"
        return f"{scheme}://{settings.minio_endpoint}"

    def upload_image(self, data: bytes, content_type: str) -> str:
        ext = "jpg"
        if content_type == "image/png":
            ext = "png"
        elif content_type == "image/webp":
            ext = "webp"
        key = f"{uuid.uuid4().hex}.{ext}"
        try:
            self._client.put_object(
                Bucket=self._bucket,
                Key=key,
                Body=data,
                ContentType=content_type,
            )
        except (ConnectionClosedError, ClientError) as exc:
            logger.warning("S3 put_object failed (%s), retrying plain HTTP PUT", exc)
            self._put_object_http(key, data, content_type)
        return key

    def _put_object_http(self, key: str, data: bytes, content_type: str) -> None:
        url = f"{self._endpoint_url()}/{self._bucket}/{key}"
        response = httpx.put(
            url,
            content=data,
            headers={"Content-Type": content_type},
            timeout=60.0,
        )
        response.raise_for_status()

    def public_url(self, key: str) -> str:
        base = settings.minio_public_url.rstrip("/")
        return f"{base}/{self._bucket}/{key}"

    def ensure_bucket(self, *, attempts: int = 30, delay_sec: float = 2.0) -> None:
        last_error: Exception | None = None
        for _ in range(attempts):
            try:
                self._client.head_bucket(Bucket=self._bucket)
                self._ensure_public_read_policy()
                return
            except ClientError as exc:
                code = exc.response.get("Error", {}).get("Code", "")
                if code in {"404", "NoSuchBucket", "NotFound"}:
                    self._client.create_bucket(Bucket=self._bucket)
                    self._ensure_public_read_policy()
                    return
                last_error = exc
            except Exception as exc:  # noqa: BLE001
                last_error = exc
            time.sleep(delay_sec)
        raise RuntimeError(f"MinIO bucket {self._bucket!r} is not ready") from last_error

    def _ensure_public_read_policy(self) -> None:
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": ["*"]},
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{self._bucket}/*"],
                }
            ],
        }
        try:
            self._client.put_bucket_policy(
                Bucket=self._bucket,
                Policy=json.dumps(policy),
            )
        except ClientError as exc:
            logger.warning("Could not set public bucket policy: %s", exc)


storage_service = StorageService()
