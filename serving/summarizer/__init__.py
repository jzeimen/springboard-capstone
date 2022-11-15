import os
import sys
import tarfile
import boto3
from botocore import UNSIGNED
import botocore
from botocore.client import Config
from botocore.exceptions import NoCredentialsError
import logging

from flask import Flask
from flask import render_template
from flask import request

from .predict import Predictor
predictor = Predictor()
logging.basicConfig(level=logging.INFO)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    logging.info("Downloading model file...")
    bucket_env = os.getenv("S3_BUCKET")
    object_env = os.getenv("MODEL_OBJECT")

    bucket = "springboard-summarizer"
    object = "model1.tar"

    if bucket_env is not None:
        logging.info(f"Overriding bucket to {bucket_env}")
        bucket = bucket_env

    if object_env is not None:
        logging.info(f"Overriding object to {object}")
        object = object_env

    logging.info(f"Downloading model bucket:{bucket}, object:{object}")
    logging.info("This will take several minutes")
    try : 
        s3 = boto3.client("s3")
        s3.download_file(bucket, object , "model1.tar")
    except NoCredentialsError:
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        s3.download_file(bucket, object , "model1.tar")    


    with tarfile.open("model1.tar") as f:
        logging.info("Extracting model file")
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(f, "model")

    logging.info("Setting up tf model")
    predictor.init()


    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            article = request.form['article'].strip()
            summary = predictor.predict(article)
            return render_template('index.html', article=article, summary=summary)
        else:
            pass
        return render_template('index.html')
    
    return app
