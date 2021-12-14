import os
import pathlib
import fitz
import requests
import base64
import time

from project.models import generate_upload_log

#get_s3_client didn't used here still imported.
from project.clients import get_s3_client

ALLOWED_EXTENSION = [".pdf", ".PDF"]

s3_client = get_s3_client()
# -- Supportive Ftp service function

def get_ftP_service_ip_address(event):
    if event == "local":
        return '172.16.1.28'

    if event == 'test':
        return '172.16.1.28'

    if event == 'production':
        return '172.16.1.39' 

def send_to_ftp(delta_id, event):
    """ API request to FTP service

    This module connects with asynchronous FTP service with json post request with respective delta_id.
    """
    json_data = {"delta_id": delta_id}
    t0 = time.time()

    ftp_service_address = get_ftP_service_ip_address(event)

    response = requests.post(f"http://{ftp_service_address}:5000/ftp", json=json_data)
    print(response)
    if response.status_code == 200: 
        response_data = response.json()
        print("FTP service response: ", response_data)
        t1 = time.time()
        print('Took', t1 - t0, 'seconds')
    else:
        sg.Print("ERROR in transmitting to FTP service.....")
        print("ERROR in transmitting to FTP service.....")
        t1 = time.time()
        print('Took', t1 - t0, 'seconds')
        pass

# -- Page Count

def get_page_count(file_name):
    """Collects page count as per file_name.
    """
    file_n, file_extension = os.path.splitext(file_name)

    if os.path.getsize(file_name) > 0 and file_extension in ALLOWED_EXTENSION:
        try:
            page_count = fitz.open(file_name).pageCount
            return page_count
        except Exception as e:
            print("Exception happned: ", e)
            print(e)
            page_count = 0
            return page_count
    else:
        page_count = 0
        return page_count

def get_bucket_name(event_type):
    if event_type == "local":
        return base64.b64decode('dmlkYWRhdGE=').decode("utf-8")
    
    if event_type == "test":
        return base64.b64decode('dmlkYWRhdGE=').decode("utf-8")
    
    if event_type == "production":
        return base64.b64decode('dmlkYS1zZXJ2aWNlLXRlYW0tMg==').decode("utf-8")

# def get_database_session(event_type):
#     if event_type == "local":
#         url = database_url(event_type)
#         return prepare_model(url, event_type)
    
#     if event_type == "test":
#         url = database_url(event_type)
#         return prepare_model(url, event_type)
    
#     if event_type == "production":
#         url = database_url(event_type)
#         return prepare_model(url, event_type)

#required import prepare_model, generate_upload_log
def copy_upload(delta_id, file, event_type, med_dir, user_id, full_name, database_session, Upload_log, n):
    bucket_name = get_bucket_name(event_type)
    
    # DBSession, Upload_log = get_database_session(event_type)
    
    file_name, extension = os.path.splitext(file)
    fil_ext = extension.replace(".", "")
    bucket_dir = '%s/%s_%04d.%s' % (delta_id, delta_id, n, fil_ext)
    meds_dir_path = str(pathlib.PurePosixPath(med_dir).joinpath(file))
    print("Source Copy meds_dir_path : ", meds_dir_path)
    if fil_ext.lower() == 'pdf':
        print(f'uploading {file} from {med_dir} as {bucket_dir}')
        page_count = get_page_count(meds_dir_path)
        # s3_upload
        s3_client.upload_file(meds_dir_path, bucket_name, bucket_dir)
        time.sleep(0.1)
        # print(send_to_ftp(delta_id, event_type), flush=True)
        #store into database according to event type:
        print(generate_upload_log(database_session, delta_id, file, bucket_dir, page_count, user_id, full_name, Upload_log))

    # return n+1    
#outside: n+=1

def upload_task(delta_id, med_dir, event, user_id, full_name, database_session, Upload_log, n=1):
    if os.path.isdir(med_dir):
        for file in os.listdir(med_dir):
            print("Files: ", file)
            meds_dir_path = str(pathlib.PurePosixPath(med_dir).joinpath(file))
            print("Source meds_dir_path: ", meds_dir_path)
            if os.path.isdir(meds_dir_path) and os.listdir(meds_dir_path):
                for file in os.listdir(meds_dir_path):
                    #perform complete operations of upload and storing into database
                    copy_upload(delta_id, file, event, meds_dir_path, user_id, full_name, database_session, Upload_log, n)
                    n+=1
                
            else:
                #perform complete operations of upload and storing into database 
                copy_upload(delta_id, file, event, med_dir, user_id, full_name, database_session, Upload_log, n)
                n+=1
            
    # print("Closing database sesssion!", database_session.close())
    # print("Closing database sesssion!", DBSession.remove())


def upload_files(delta_id, med_dir, event, user_id, full_name, database_session, Upload_log, n=1):
        """S3 bucket upload supporting function.

        PARAMETER: 
        ---------
        delta_id: str 
        med_dir: str 
        s3_client as Gloabl 
        event: str 
        user_id:integer 
        full_name: str
        n: starting file number -> default will be 1.

        RETURN: None

        """  
        if event == "local":
            upload_task(delta_id, med_dir, event, user_id, full_name, database_session, Upload_log, n=1)

        if event == "test":
            upload_task(delta_id, med_dir, event, user_id, full_name, database_session, Upload_log, n=1)

        if event == "production":
            upload_task(delta_id, med_dir, event, user_id, full_name, database_session, Upload_log, n=1)