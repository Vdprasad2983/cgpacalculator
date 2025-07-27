# utils/s3_utils.py

import os
import pandas as pd
import boto3
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = "cgpa-calculator-prasad"

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def read_user_csv_from_s3(username):
    key = f"{username}.csv"
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        return pd.read_csv(response['Body'])
    except s3.exceptions.NoSuchKey:
        return None
    except Exception as e:
        return None

def write_user_csv_to_s3(username, df):
    buffer = StringIO()
    df.to_csv(buffer, index=False)
    s3.put_object(Bucket=BUCKET_NAME, Key=f"{username}.csv", Body=buffer.getvalue())

def create_user_csv_in_s3(username):
    df = pd.DataFrame(columns=[
        "subject_names", "grades", "credits", "actual_credits",
        "sem", "grade", "percentage"
    ])
    write_user_csv_to_s3(username, df)
