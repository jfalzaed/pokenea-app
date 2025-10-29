import boto3
import os
from functools import lru_cache
from botocore.exceptions import ClientError


@lru_cache
def get_s3_client():
    """
    Crea y cachea un cliente S3 (para no recrearlo en cada request).
    Usa las credenciales definidas en variables de entorno (.env).
    """
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )


def get_image_url(image_name: str) -> str:
    """
    Genera la URL pública de una imagen almacenada en AWS S3.
    Asegúrate de que el bucket tenga acceso público habilitado.
    """
    bucket_name = os.getenv('S3_BUCKET')
    region = os.getenv('AWS_REGION', 'us-east-1')
    return f"https://{bucket_name}.s3.{region}.amazonaws.com/{image_name}"


def upload_image_to_s3(file_path: str, image_name: str) -> bool:
    """
    Sube una imagen local a un bucket S3 con permisos públicos.
    Solo necesario si vas a automatizar la carga de archivos.
    """
    s3_client = get_s3_client()
    bucket_name = os.getenv('S3_BUCKET')

    try:
        s3_client.upload_file(
            file_path,
            bucket_name,
            image_name,
            ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
        )
        print(f"✅ Imagen '{image_name}' subida correctamente a S3.")
        return True
    except ClientError as e:
        print(f"❌ Error subiendo imagen: {e}")
        return False
