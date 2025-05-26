import os.path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
PROJECT_DIR = "/Users/saathvikdirisala/Documents/MCPEmailAssistant/emailassistant/"
CREDENTIALS_FP = os.path.join(PROJECT_DIR, "client_secret_396371009840-fqddcngmeu6m5cp0j6l1qe3t9s4jgkih.apps.googleusercontent.com.json")
TOKEN_FP = os.path.join(PROJECT_DIR, "token.json")


class EmailAssistant:
    
    def __init__(self, cred_fp = CREDENTIALS_FP, token_fp = TOKEN_FP, scopes = SCOPES):
        self.cred_fp = cred_fp
        self.token_fp = token_fp
        self.scopes = scopes
        self.service = None
        self.get_credentials()

    def get_credentials(self):

        if os.path.exists(self.token_fp):
            creds = Credentials.from_authorized_user_file(self.token_fp, self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.cred_fp, self.scopes
                )
                creds = flow.run_local_server(port=0)

            with open(self.token_fp, "w") as token:
                token.write(creds.to_json())

        self.service = build("gmail", "v1", credentials=creds)


    def _get_subject_and_sender(payload_headers):
        subject = sender = None
        for header in payload_headers:
            if header["name"] == "Subject":
                subject = header["value"]
            elif header["name"] == "From":
                sender = header["value"]
        return subject, sender

    def get_email_summary(self, query) -> str:
        """
        query (str): format must be in email filter format.

        Examples: 
        after:2025/05/24 would find emails sent or received after May 24, 2025.
        before:2025/05/24 would find emails sent or received before May 24, 2025.
        older_than:1m would find emails older than one month.
        newer_than:1y would find emails newer than one year. 
        """
        try:

            results = self.service.users().messages().list(userId="me", q=query).execute()
            messages = results.get("messages", [])

            if not messages:
                print("No recent messages found.")
                return

            print(f"Found {len(messages)} message(s) from the last 24 hours:\n")

            build_output = ""
            for msg in messages:
                msg_id = msg["id"]
                msg_detail = self.service.users().messages().get(userId="me", id=msg_id, format="metadata", metadataHeaders=["Subject", "From"]).execute()
                headers = msg_detail["payload"]["headers"]
                snippet = msg_detail.get("snippet", "")
                subject, sender = EmailAssistant._get_subject_and_sender(headers)
                build_output += f"From: {sender}\nSubject: {subject}\nSnippet: {snippet}\n" + "-" * 40
            
            return build_output

        except Exception as e:
            return {"error": str(e)}


    def get_top_matching_email(self, query_keywords) -> str:
        """
        query_keywords (str): keywords to filter inbox
        """

        try:
            # Construct search query
            query = f"{query_keywords} in:inbox"

            # Fetch matching message IDs
            results = self.service.users().messages().list(userId='me', q=query, maxResults=1).execute()
            messages = results.get('messages', [])

            if not messages:
                return {"error": "No matching emails found."}

            # Get the top result
            msg_id = messages[0]['id']
            msg = self.service.users().messages().get(userId='me', id=msg_id, format='metadata', metadataHeaders=['From', 'Subject', 'Date']).execute()

            headers = msg['payload']['headers']
            msg_info = {h['name'].lower(): h['value'] for h in headers}
            snippet = msg.get("snippet", "")

            return {
                "from": msg_info.get("from"),
                "subject": msg_info.get("subject"),
                "date": msg_info.get("date"),
                "snippet": snippet
            }

        except Exception as e:
            return {"error": str(e)}