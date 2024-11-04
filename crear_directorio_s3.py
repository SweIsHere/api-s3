import boto3
import json

def lambda_handler(event, context):
    # Extraer y procesar el cuerpo del evento
    request_body = event.get("body")
    if isinstance(request_body, str):
        request_body = json.loads(request_body)

    # Obtener parámetros del bucket y directorio
    bucket_name = request_body.get("name")
    directory_name = request_body.get("directory_name")

    if not bucket_name or not directory_name:
        return {
            "statusCode": 400,
            "message": "Se requieren el nombre del bucket y el nombre del directorio."
        }

    s3 = boto3.client("s3")

    try:
        # Crear un objeto que actúa como un "directorio" en S3
        s3.put_object(Bucket=bucket_name, Key=f"{directory_name}/")
        
        # Respuesta de éxito
        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": f"Directorio '{directory_name}' creado exitosamente en el bucket '{bucket_name}'."
            })
        }

    except s3.exceptions.ClientError as error:
        error_message = error.response['Error']['Message']
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error al crear el directorio: {error_message}"})
        }

    except Exception as e:
        # Captura cualquier otra excepción inesperada
        return {
            "statusCode": 500,
            "body": json.dumps({"message": f"Error inesperado: {str(e)}"})
        }
