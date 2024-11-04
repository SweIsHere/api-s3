import boto3
import json

def lambda_handler(event, context):
    # Parsear el cuerpo del evento
    request_body = event.get("body")
    if isinstance(request_body, str):
        request_body = json.loads(request_body)

    # Validar el parámetro del nombre del bucket
    bucket_name = request_body.get("name")
    if not bucket_name:
        return {
            "statusCode": 400,
            "message": "Es necesario proporcionar el nombre del bucket."
        }

    # Inicializar el cliente de S3
    s3 = boto3.client("s3")

    try:
        # Crear el bucket con las configuraciones de propiedad
        s3.create_bucket(
            Bucket=bucket_name,
            ObjectOwnership="BucketOwnerPreferred"
        )

        # Configurar las políticas de acceso público para el bucket
        public_access_config = {
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
        }
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration=public_access_config
        )

        # Asignar permisos de lectura y escritura pública al bucket
        s3.put_bucket_acl(Bucket=bucket_name, ACL='public-read-write')

        # Devolver una respuesta exitosa
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": f"Bucket '{bucket_name}' creado exitosamente con acceso público.",
                "bucket_name": bucket_name
            })
        }

    except s3.exceptions.BucketAlreadyExists:
        return {
            "statusCode": 409,
            "body": json.dumps({"message": "El bucket ya existe en la región especificada."})
        }

    except s3.exceptions.ClientError as error:
        error_message = error.response['Error']['Message']
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error al crear el bucket: {error_message}"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error inesperado: {str(e)}"})
        }
