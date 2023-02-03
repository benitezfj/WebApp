import os
from dotenv import load_dotenv
# import ee
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ec8466a71d3153c8f7adfb411dffdc47f7adfb411dffdc47'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    


    # The service account email address authorized by your Google contact.
    # Set up a service account as described in the README.
    # EE_ACCOUNT = 'user@mail.com'

    # The private key associated with your service account in Privacy Enhanced
    # Email format (.pem suffix).  To convert a private key from the RSA format
    # (.p12 suffix) to .pem, run the openssl command like this:
    # openssl pkcs12 -in downloaded-privatekey.p12 -nodes -nocerts > privatekey.pem
    # https://cloud.google.com/iam/docs/creating-managing-service-account-keys
    # Install the Gclould, then in the command line generated the private key
    # gcloud iam service-accounts keys create KEY_FILE --iam-account=SERVICE_ACCOUNT
    # Before intalling the gclould sdk check the following page
    # https://cloud.google.com/sdk/docs/configurations?hl=es-419

    # EE_PRIVATE_KEY_FILE = 'credentials/privatekey.pem'

    # EE_CREDENTIALS = ee.ServiceAccountCredentials(EE_ACCOUNT, EE_PRIVATE_KEY_FILE)