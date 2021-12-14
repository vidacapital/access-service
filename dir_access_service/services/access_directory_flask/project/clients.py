import base64
import boto3


def get_s3_client():
    with open(base64.b64decode('L21udC9wdWJsaWMxL19Qb3J0Zm9saW8gQW5hbHl0aWNzL0RhdGFiYXNlLy5qdm4vLmVudi5hY2Nlc3M='.encode("utf-8")).decode("utf-8")) as file_content:
        environmental_value = file_content.read()
        key_id = base64.b64decode(base64.b64encode((environmental_value+'U2hpdCBDb2RlQUtJQUlGVEhQSzRTTFM1NFU2TkE=')\
                                                    .encode("utf-8"))).decode("utf-8")\
                                                    .replace(base64.b64decode("VGhpcyBmaWxlIGhhcyBub3RoaW5nVTJocGRDQkRiMlJs").decode("utf-8"),"")
        aws_access_key_id = base64.b64decode(key_id).decode("utf-8")
        access_key = base64.b64decode(base64.b64encode((environmental_value+'U2hpdCBDb2RlNGF0NVMzRWJkZUlsdEpFYUFTVVc4d1pQaldYZUg4OXpMdVpWdHVXcA==')\
                                                    .encode("utf-8"))).decode("utf-8")\
                                                    .replace(base64.b64decode("VGhpcyBmaWxlIGhhcyBub3RoaW5nVTJocGRDQkRiMlJs").decode("utf-8"),"")        
        
        aws_secret_access_key = base64.b64decode(access_key).decode("utf-8")
    return boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


def database_url(event):

    if event == "local":
        with open(base64.b64decode('L21udC9wdWJsaWMxL19Qb3J0Zm9saW8gQW5hbHl0aWNzL0RhdGFiYXNlLy5qdm4vLmVudi5hY2Nlc3M='.encode("utf-8")).decode("utf-8")) as file_content:
            environmental_value = file_content.read()
            url_value = base64.b64decode(base64.b64encode((environmental_value+'U2hpdCBDb2Rlc3FsaXRlOi8vL3NpdGUuZGI=')\
                                                           .encode("utf-8"))).decode("utf-8")\
                                                           .replace(base64.b64decode("VGhpcyBmaWxlIGhhcyBub3RoaW5nVTJocGRDQkRiMlJs").decode("utf-8"),"")
            database_url_local = base64.b64decode(url_value).decode("utf-8")
        return database_url_local

    if event == "test":
        with open(base64.b64decode('L21udC9wdWJsaWMxL19Qb3J0Zm9saW8gQW5hbHl0aWNzL0RhdGFiYXNlLy5qdm4vLmVudi5hY2Nlc3M='.encode("utf-8")).decode("utf-8")) as file_content:
            environmental_value = file_content.read()
            url_value = base64.b64decode(base64.b64encode((environmental_value+'U2hpdCBDb2RlcG9zdGdyZXM6Ly9kYXR0YXRlbGU6ODQzMk5hdHVyZUBhd3MtcG9zdGdyZXMuY3o3bm44cG0za2k4LnVzLWVhc3QtMS5yZHMuYW1hem9uYXdzLmNvbTo1NDMyL2RldmVsb3BtZW50X3Rlc3Q=')\
                                                           .encode("utf-8"))).decode("utf-8")\
                                                           .replace(base64.b64decode("VGhpcyBmaWxlIGhhcyBub3RoaW5nVTJocGRDQkRiMlJs").decode("utf-8"),"")
            database_test_url = base64.b64decode(url_value).decode("utf-8")
        return database_test_url

    if event == "production":
        with open(base64.b64decode('L21udC9wdWJsaWMxL19Qb3J0Zm9saW8gQW5hbHl0aWNzL0RhdGFiYXNlLy5qdm4vLmVudi5hY2Nlc3M='.encode("utf-8")).decode("utf-8")) as file_content:
            environmental_value = file_content.read()
            url_value = base64.b64decode(base64.b64encode((environmental_value+'U2hpdCBDb2RlcG9zdGdyZXM6Ly92aWRhbGFrZWluYzo0NTg1TGFrZVJhemVyQGxha2UtcG9zdGdyZXMuY3o3bm44cG0za2k4LnVzLWVhc3QtMS5yZHMuYW1hem9uYXdzLmNvbTo1NDMyL3ZpZGFfZGVsdGFfcHJvZHVjdGlvbg==')\
                                                        .encode("utf-8"))).decode("utf-8")\
                                                        .replace(base64.b64decode("VGhpcyBmaWxlIGhhcyBub3RoaW5nVTJocGRDQkRiMlJs").decode("utf-8"),"")
            database_production_url = base64.b64decode(url_value).decode("utf-8")
        return database_production_url