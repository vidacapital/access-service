# services/access_directory_flask/project/models.py

# This will be different type of approach and connected with database as per event based: local, test and production
# in local no saving will happen but it will sent to local database to perform savings in SQLITE
# in test in development database
# Production


#SQLALCHEMY_DATABASE_URI = control follwing according to event type:
#sqlalchemy related imports
from datetime import datetime
import pytz

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Date, DateTime, Integer, String, ForeignKey, Boolean, BigInteger, ForeignKey, Float
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import relationship
import pytz  
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, func


def local_table_create(Base, event3, AWS_ENGINE, DBSession):  #passed inspection
    if event3 == "local":
        Base.metadata.create_all(AWS_ENGINE)
        DBSession.commit() 
    if event3 == "test":
        pass
    if event3 == "production":
        pass   

Base = declarative_base()

metadata = Base.metadata

class User(Base):  #passed inspection
    __tablename__ = "user"
    __talbe_args__ = {'schema':'public'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(50), unique=False, nullable=False)
    last_name = Column(String(50), unique=False, nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')
    password = Column(String(60), nullable=False)
    registered_on = Column(DateTime, default=func.now(), nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    confirmed = Column(Boolean, nullable=False, default=False)
    confirmed_on = Column(DateTime, nullable=True)

    # Upload_log = relationship('Upload_log', backref="user")
    # vida_request = relationship('VIDA_REQUSTS', backref="user")

    def __init__(self, username, email, password, first_name, last_name, confirmed, admin=False, confirmed_on=None):
        self.email = email
        self.username = username
        self.password = password
        self.registered_on = datetime.now()
        self.admin = admin
        self.first_name = first_name
        self.last_name = last_name
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

class Upload_log(Base):   #passed inspection

    __tablename__  = "Upload_log"
    # __table_args__ = {'schema':'public'}

    id = Column(Integer, primary_key=True)
    delta_id = Column(String, nullable=False)
    medical_filenames = Column(String, nullable=False)
    bucket_dir = Column(String, nullable=False)
    upload_date = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.current_timestamp())
    user_id = Column(ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT', match='FULL'),  nullable=False, index=True)
    full_name = Column(String, nullable=False)
    page_count = Column(Integer)
    user = relationship('User')

    # user = relationship('User', backref='Upload_log')


    def __init__(self, delta_id, medical_filenames, bucket_dir, user_id, full_name, page_count):
        self.delta_id = delta_id
        self.medical_filenames = medical_filenames
        self.bucket_dir = bucket_dir
        self.user_id = user_id
        self.full_name = full_name
        self.page_count = page_count
        super(Upload_log, self).__init__()

    __mapper_args__ = {
        'version_id_col': upload_date,
        'version_id_generator': lambda v:datetime.now(tz=pytz.timezone("UTC"))
    }

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Upload_log('{self.delta_id}', '{self.medical_filenames}', '{self.bucket_dir}', , '{self.user_id}', '{self.full_name}', '{self.page_count}')"

class VIDA_REQUESTS(Base):    #passed inspection

    __tablename__ = "VIDA_REQUESTS"
    __talbe_args__ = {'schema':'public'}

    id = Column(Integer, primary_key=True)
    delta_id = Column(String, nullable=False)
    request_date = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.current_timestamp())
    user_id = Column(ForeignKey('user.id', ondelete='RESTRICT', onupdate='RESTRICT', match='FULL'),  nullable=False, index=True)
    data_source = Column(String)

    # user = relationship('User', backref='VIDA_REQUESTS')

    user = relationship('User')

    def __repr__(self):
        return f"VIDA_REQUESTS('{self.delta_id}', '{self.request_date}', '{self.data_source}')"         

    __mapper_args__ = {
        'version_id_col': request_date,
        'version_id_generator': lambda v:datetime.now(tz=pytz.timezone("UTC"))
    }



def prepare_model(SQLALCHEMY_DATABASE_URI, event):
    """
    Currently Session created inside, The limitation is only one task of upload will be handled 
    """

    AWS_ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
    DBSession = scoped_session(sessionmaker(autoflush=True, autocommit=False, bind=AWS_ENGINE))

    print("Working on table decision according to event enviornment ... ", local_table_create(Base, event, AWS_ENGINE, DBSession))
    # DBSession.commit()
        # Session for testing server

    print("DataBase session :", DBSession)

    return DBSession


def generate_upload_log(database_session, delta_id, file_name, s3_destination, page_count, user_id, full_name, Upload_log):
    """This function will used to store database values according session condition.
    PARAMETERS:
    ---------- 
    database_session: local, test, production sqlalchemy session object. This will be scoped session and needs to be closed aftwards.
    delta_id: str
    file_name: str, most likely named as file
    s3_destination: str, most likely named as bucket_dir
    page_count: integer, pymupdf => import fitz, fitz.open(file_name).pageCount
    user_id: integer
    full_name: str
    Upload_log: Sqlalchemy database model

    """
    upload_log = Upload_log(delta_id=delta_id, medical_filenames=file_name, bucket_dir=s3_destination, user_id=user_id, full_name=full_name, page_count=page_count)
    database_session.add(upload_log)
    database_session.commit()   
    return "commit successful"


def generate_request(database_session, delta_id, user_id, data_source, VIDA_REQUESTS):
    vida_request = VIDA_REQUESTS(delta_id=delta_id, user_id=user_id, data_source=data_source)
    database_session.add(vida_request)
    database_session.commit()   
    return "commit successful"