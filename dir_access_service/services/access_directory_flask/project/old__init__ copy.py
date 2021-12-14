#old code copy
# #/dir_access_service/services/access_directory_flask/project/__init__.py

# import os
# from pathlib import Path
# import pathlib
# import logging
# from logging.handlers import RotatingFileHandler
# import datetime
# import sys
# import time

# from flask import Flask
# from flask import Blueprint, request, render_template, abort, jsonify,  make_response,url_for, redirect
# import flask
# import pandas as pd

# from threading import Thread

# from pandas.io.json import json_normalize
# from project.clients import get_s3_client, database_url
# from project.supportive_functions import upload_files

# from project.models import prepare_model, generate_request, Upload_log, VIDA_REQUESTS
# # from flask_mail import Mail
# from project.utils import send_email
# # mail = Mail()

# s3_client = get_s3_client() 

# # from flask_mail import Message


# MAIL_DEFAULT_SENDER = 'analytics@vidacapitalinc.com'

# # def send_email(to, subject, template):
# #     msg = Message(
# #         subject,
# #         recipients=[to],
# #         html=template,
# #         sender=MAIL_DEFAULT_SENDER
# #     )
# #     mail.send(msg)

# # logging.basicConfig(filename='id_error_log.log', level=logging.DEBUG)

# # logger = logging.getLogger('mylogger')
# # # Configure logger to write to a file...

# # def my_handler(type, value, tb):
# #     logger.exception("Uncaught exception: {0}".format(str(value)))

# # # Install exception handler
# # sys.excepthook = my_handler

# access_drive_blueprint = Blueprint('id_service', __name__)  

# print("I am runninng outside...")
# #How to mount guide
# #https://stackoverflow.com/questions/28302178/how-can-i-add-a-volume-to-an-existing-docker-container

# user_email_address_dict = {1 : 'datta.tele@vidacapitalinc.com', 5 : 'ed.williams@vidacapitalinc.com', 6 : 'daniel.stokes@magna-life.com', 
#                            9 : "rachel.weiner@vidacapitalinc.com",  8 : "william.byk@vidacapitalinc.com", 19 : "dillon.hamm@magna-life.com", 
#                            20 : "nilofar.vahora@magna-life.com", 21 : "margie.contreras@magna-life.com", 22 : "john.hendrickson@vidacapitalinc.com",
#                            24 : "megan.brown@vidacapitalinc.com", 25 : "lauren.hutchison@vidacapitalinc.com",  26 : "angelica.salas@vidacapitalinc.com", 
#                            27 : "carrie.blackmon@vidacapitalinc.com", 30 : "clarissa.martinez@magna-life.com"}


# if os.path.exists('/mnt/public1'):
#     print("yes")
#     print("List of directory check outside:", os.listdir('/mnt/public1'))
# else:
#     print("List of directory check outside:", os.listdir())

# def create_app(script_info=None):

#     flask_app = Flask(__name__)

#     print("I am runninng...")

#     # app_settings = 'project.config.BaseConfig'
#     # flask_app.config.from_object(app_settings)
    
#     # mail.init_app(flask_app)

#     if os.path.exists('/mnt/public1'):
#         print("yes")
#         print("List of directory:", os.listdir('/mnt/public1'))
#     else:
#         print("List of directory:", os.listdir())

#     flask_app.register_blueprint(access_drive_blueprint)
    
#     return flask_app

# # app = Flask(__name__)
# # app.config["DEBUG"] = True

# # class Compute(Thread):
# #     def __init__(self, request):
# #         Thread.__init__(self)
# #         self.request = request

# #     def run(self):
# #         print("start")
# #         time.sleep(5)
# #         print(self.request)
# #         print("done")
        
# class UploadCompute(Thread):
#     def __init__(self, dataframe, event, upload_files, DBSession, Upload_log, VIDA_REQUESTS):
#         self.dataframe = dataframe
#         self.event = event
#         self.upload_files = upload_files
#         self.DBSession = DBSession
#         self.Upload_log = Upload_log
#         self.VIDA_REQUESTS = VIDA_REQUESTS
#         Thread.__init__(self)

#     def run(self):
#         import requests
#         print("Started upload process on another thread!")
#         # database_session = self.DBSession
#         print(self.dataframe.apply(lambda x: self.upload_files(x.delta_id, x.med_dir, self.event, x.user_id, x.full_name,self.DBSession, self.Upload_log, n=1), axis=1))
        
#         #New
#         vida_requests_df = pd.DataFrame()
#         user_id = int(list(self.dataframe['user_id'].unique())[0])
#         vida_requests_df["delta_id"] = self.dataframe["delta_id"].unique()
#         vida_requests_df["user_id"] = user_id
#         vida_requests_df["data_source"] = "pdf"
#         print(vida_requests_df)

#         #store request
#         print("Storing vida Request: ", vida_requests_df.apply(lambda x: generate_request(self.DBSession, x.delta_id, x.user_id, x.data_source, self.VIDA_REQUESTS), axis=1))

#         self.DBSession.remove()
#         #send_email

#         user_email_address = user_email_address_dict[user_id]
#         user_name = str(list(self.dataframe['full_name'].unique())[0])

#         send_from = MAIL_DEFAULT_SENDER
#         send_to = user_email_address
#         server = 'west.EXCH081.serverdata.net'
#         username = MAIL_DEFAULT_SENDER
#         password = 'ShoalCreek14$'

#         print("Finished! Next will be email user...", send_email(send_from, send_to, server, username, password, user_name, use_tls=True))

#         # print("Finished! Next will be email user...", send_email(user_email_address, subject, html))
        

# #-------------------------------------------------
# #Supporting functions:
# #import os
# import hashlib

# #Buffer size for hashlib to handle when read file. Speed up the process for large files.
# BUF_SIZE = 65536

# def filter_dir(starting_dir, sub_dir):
    
#     dir_list = os.listdir(starting_dir)
#     return [dir_name for dir_name in dir_list 
#             if sub_dir.lower() in dir_name.lower()]

# def find_folder(starting_dir, *sub_dirs):
#     sub_dir = sub_dirs[0]
#     print(sub_dir)
#     filtered = filter_dir(starting_dir, str(sub_dir))
#     print("filtered", filtered)
#     if len(filtered) == 0:
#         print('could not find %s' % sub_dir)
#         return None
    
#     next_dir = os.path.join(starting_dir, filtered[0])
#     print("next_dir", next_dir)
#     if os.path.isdir(next_dir):
#         if len(sub_dirs) > 1:
            
#             result = find_folder(next_dir, *sub_dirs[1:])
#             print("Dir result: ", result)
#             if result:
#                 if os.path.isdir(result):
#                     return result
#             return next_dir
#         return next_dir
    
# def check_files(med_dir):
#     dir_list = os.listdir(med_dir)
#     file_paths = [os.path.join(med_dir, med) for med in dir_list]
#     return len([file_path for file_path in file_paths if not os.path.exists(file_path)])

# #upcoming features: find medical folder from any level.
# def find_dir(starting_dir: str, case_id: str, folder_name: str) -> str:
#     file_paths = []
#     hashcodes = []
#     filenames = []
#     case_dir = os.path.join(starting_dir, case_id)
#     for dirpath, subdirs, files in os.walk(f'{case_dir}'):
#         if folder_name in dirpath:
#             for filename in files:
#                 filepath = os.path.join(dirpath, filename)
#                 file_paths.append(filepath)
#                 filenames.append(os.path.basename(filename))
#                 md5 = hashlib.md5() 
#                 with open(filepath, 'rb') as afile:
#                     while True:
#                         data = afile.read(BUF_SIZE)
#                         if not data:
#                             break
#                         file_hashcode = md5.update(data)
#                 hashcode_value = md5.hexdigest()
# #                     print(hashcode_value)
#                 hashcodes.append(hashcode_value)

#     return str()
# #-------------------------------------------------
        
# #Only one threading: Peform getting files and uploading and storing into database.
# @access_drive_blueprint.route('/api/peform_uploads', methods=["GET", "POST"])
# def uploads():
#     if request.method == 'GET':
#         # thread_a = Compute(request.__copy__())
#         # thread_a.start()
#         return '''<H1> Access service api: please perform post request with following requirements </H1> '''

#     if request.method == 'POST':
#         print("I am inside the post requests!!")
#         if not request.json:
#             return make_response(jsonify({'error': 'Not a json request! '}), 400)

#         else:
#             post_data = request.get_json()
#             event = post_data.get("event")
#             print("Post event: ", event)
#             print("Post Data: ", post_data.get("data"))
#             upload_data = post_data.get("data")

#             #before upload df will look like: insured_id, delta_id, case_id, meds_dir and other columns (date_of_birth, gender, le_date, le_mean, le_provider) 
#             # with dropped duplicates on delta id
#             if upload_data:

#                 if event == "local":
#                     url = database_url(event)
#                     DBSession = prepare_model(url, event)
                    
#                     upload_data_df = json_normalize(upload_data)
#                     upload_data_df = upload_data_df[["delta_id", "med_dir", "user_id", "full_name"]]
#                     print("About to start Upload Compute part.....")

#                     thread_upload = UploadCompute(upload_data_df.__copy__(), event, upload_files, DBSession, Upload_log, VIDA_REQUESTS)
#                     thread_upload.start()
                    
#                     response_object = {
#                         'status': 'success',
#                         'message': 'Upload process has been started!',
#                         'data' : upload_data_df.to_dict(orient="records")
#                         }
#                     print("About to make response!")
#                     DBSession.remove()
#                     return make_response(jsonify(response_object), 200)

#                     # print(df.apply(lambda x: upload(x.delta_id, x.med_dir, s3_client), axis=1))

#                 if event == "test":
#                     url = database_url(event)
#                     DBSession = prepare_model(url, event)
                    
#                     upload_data_df = json_normalize(upload_data)
#                     upload_data_df = upload_data_df[["delta_id", "med_dir", "user_id", "full_name"]]
#                     thread_upload = UploadCompute(upload_data_df.__copy__(), event, upload_files, DBSession, Upload_log, VIDA_REQUESTS)
#                     thread_upload.start()

#                     response_object = {
#                         'status': 'success',
#                         'message': 'Upload process has been started!',
#                         'data' : upload_data_df.to_dict(orient="records")
#                         }
#                     DBSession.remove()    
#                     return make_response(jsonify(response_object), 200)

#                 if event == "production":
#                     url = database_url(event)
#                     DBSession = prepare_model(url, event)
                    
#                     # upload_data_df = json_normalize(upload_data)
#                     # upload_data_df = upload_data_df[["delta_id", "med_dir", "user_id", "full_name"]]
#                     # thread_upload = UploadCompute(upload_data_df.__copy__(), event, upload_files, DBSession, Upload_log, VIDA_REQUESTS)
#                     # thread_upload.start()

#                     # response_object = {
#                     #     'status': 'success',
#                     #     'message': 'Upload process has been started!'
#                     #     'data' : upload_data_df.to_dict(orient="records")
#                     #     }
#                     # return make_response(jsonify(response_object), 200)
#                     DBSession.remove()
#                     pass
#                     return make_response(jsonify({"message": "Not Running production content!!"}), 200)
                
#                 response_object = {
#                     'status': 'fail',
#                     'message' : "Missing Upload data!!"
#                 }
#                 return make_response(jsonify(response_object), 400)
#         response_object = {
#             'status': 'fail',
#             'message' : "Provided information is unclear!!"
#             }
#         return make_response(jsonify(response_object), 400)

# #file_Path check
# @access_drive_blueprint.route('/api/path_check', methods=["POST"])
# def dir_path_check():

#     if not request.json:
#         return make_response(jsonify({'error': 'Not a json request! '}), 400)

#     if request.method == "POST":
#         post_data = request.get_json()
#         print("POST DATA: ", post_data)

#         dir_path = post_data.get("dir_path") 

#         #Need to add another path replace: \\Vida-FS.vidacapital.local\Public1\VLF Submission Database\Tertiary 2020\Abacus\Portfolios\January 2020\Big Dipper\Project Big Dipper\Medical + LE

#         if dir_path:
#             dir_path = str(pathlib.PurePosixPath('/mnt/public1').joinpath(dir_path.replace("//","/").replace("P:/", "").replace("P:\\", "").replace("O:/", "").replace("O:\\", "").replace("\\\\", "/").replace("\\", "/").replace("/vida-fs/Public1/", "")))
#             #.replace("\\\\vida-fs\Public1", "").replace("\\vida-fs\Public1", "").replace("/vida-fs/Public1", "")
#             print("Dir path after transformation: ", dir_path)
#             #alternative way to do: dir_path = os.path.join('/mnt/public1', dir_path)
#             if os.path.exists(dir_path):
#                 print("Dir path:", dir_path)
#                 print("Directory path Exists!")
#                 response_object = {
#                     'status': 'success',
#                     'dir_path' : dir_path
#                 }
#                 return make_response(jsonify(response_object), 200)
#             else:
#                 response_object = {
#                     'status': 'fail',
#                     'message' : "The directory path does not exists!"
#                 }
#                 return make_response(jsonify(response_object), 400)

#         else:
#             response_object = {
#                     'status': 'fail',
#                     'message' :  "Empty directory Path. Please provide dir_path!"
#                 }
#             return make_response(jsonify(response_object), 400)


#         # return make_response(jsonify({"sucuss": "YEs"}), 200)

# #Find folder and get directory path from bulk and return that data bulk.
# @access_drive_blueprint.route('/api/find_folder', methods=["POST"])
# def find_folder_api():

#     if not request.json:
#         response_object = {
#             'status': 'error',
#             'message' : 'Not a json request!'
#             }        
#         return make_response(jsonify({'error': response_object}), 400)

#     if request.method == "POST":
#         post_data = request.get_json()
# #         print("POST DATA: ", post_data)
#         post_data_df = json_normalize(post_data)

#         if not post_data_df.empty:
            
#             post_data_df['med_dir'] = post_data_df.apply(lambda x: find_folder(x.dir_path, x.case_id, x.folder_name), axis=1)

#             # post_data_df = post_data_df[post_data_df['med_dir'].notnull()].copy()
#             # post_data_df = post_data_df.drop_duplicates(['med_dir'])

#             print(post_data_df)
            
#             if not post_data_df.empty:
#                 response_object = {
#                     'status': 'success',
#                     'data' : post_data_df.to_dict(orient="records")
#                     }
#                 return make_response(jsonify(response_object), 200)
#             else:
#                 response_object = {
#                     'status': 'not_found',
#                     'messaage': 'Not a single files found with provided path!'
#                 }
#                 return make_response(jsonify(response_object), 400)
#         response_object = {
#             'status': 'error',
#             'message' : 'Empty dataframe provided!'
#             }
#         return make_response(jsonify(response_object), 400)
#     response_object = {
#         'status': 'error',
#         'message' : 'Not a POST request!'
#         }
#     return make_response(jsonify(response_object), 400)