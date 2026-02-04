import os
import mariadb
from dotenv import load_dotenv

load_dotenv()  #Load .env file

def get_connection():
    return mariadb.connect(
        host=os.environ.get("10.200.14.17"),
        user=os.environ.get("heleneliasi"),
        password=os.environ.get("dorispillow123"),
        database=os.environ.get("neglesalong")
    )
