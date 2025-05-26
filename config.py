import os

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
PROJECT_DIR = "ADD ABSOLUTE PATH TO PROJECT HERE"
CREDENTIALS_FP = os.path.join(PROJECT_DIR, "ADD NAME OF CLIENT CREDENTIALS FILE")
TOKEN_FP = os.path.join(PROJECT_DIR, "token.json")