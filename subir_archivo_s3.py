import boto3
import json
import base64

def lambda_handler(event, context):
    # Extraer y procesar el cuerpo del evento
    request_body = event.get("body")
    if isinstance(request_body, str):
        request_body = json.loads(request_body)

    # Obtener parámetros del bucket, directorio, nombre de archivo y contenido
    bucket_name = request_body.get("name")
    directory_name = request_body.get("directory_name")
    file_name = request_body.get("file_name")
    file_content_base64 = request_body.get("file_content")

    # Validar los parámetros obligatorios
    if not all([bucket_name, directory_name, file_name, file_content_base64]):
        return {
            "statusCode": 400,
            "message": "Faltan parámetros requeridos para subir el archivo."
        }

    # Decodificar el contenido del archivo
    try:
        file_content = base64.b64decode(file_content_base64)
    except Exception as e:
        return {
            "statusCode": 400,
            "message": f"Error al decodificar el archivo en base64: {str(e)}"
        }

    # Subir el archivo a S3
    s3 = boto3.client("s3")
    file_key = f"{directory_name}/{file_name}"

    try:
        s3.put_object(Bucket=bucket_name, Key=file_key, Body=file_content)
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": f"Archivo '{file_name}' subido con éxito en '{directory_name}' del bucket '{bucket_name}'."
            })
        }

    except s3.exceptions.ClientError as error:
        error_message = error.response['Error']['Message']
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error al subir el archivo a S3: {error_message}"})
        }

    except Exception as e:
        # Captura cualquier otra excepción inesperada
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error inesperado al subir el archivo: {str(e)}"})
        }
