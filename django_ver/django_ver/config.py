import os
from dotenv import load_dotenv  # pip install python-dotenv


load_dotenv(override=True)


class Config:
    EMAIL_USER_G = os.environ.get('EMAIL_USER_G')
    EMAIL_PASS_G = os.environ.get('EMAIL_PASS_G')
    EXTERNAL_PASS_G = os.environ.get('EXTERNAL_PASS_G')
    EMAIL_USER_R = os.environ.get('EMAIL_USER_R')
    EMAIL_PASS_R = os.environ.get('EMAIL_PASS_R')
    EMAIL_USER_M = os.environ.get('EMAIL_USER_M')
    EMAIL_PASS_M = os.environ.get('EMAIL_PASS_M')
    EXTERNAL_PASS_M = os.environ.get('EXTERNAL_PASS_M')
