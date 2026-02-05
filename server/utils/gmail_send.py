import base64
import os
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_gmail_service():
    client_id = (os.getenv("CLIENT_ID") or "").strip()
    client_secret = (os.getenv("SECRET_CLIENT_ID") or "").strip()
    refresh_token = (os.getenv("REFRESH_TOKEN") or "").strip()
    if not client_id or not client_secret or not refresh_token:
        raise ValueError(
            "Faltan variables de entorno: CLIENT_ID, SECRET_CLIENT_ID o REFRESH_TOKEN"
        )
    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
        token_uri="https://oauth2.googleapis.com/token",
    )
    return build("gmail", "v1", credentials=creds)


def send_email(
    to_address: str,
    subject: str,
    body_html: str,
    from_address: str | None = None,
) -> dict:
    
    sender = (from_address or os.getenv("EMAIL_SEND") or "").strip()
    if not sender:
        raise ValueError("Falta EMAIL_SEND en .env o argumento from_address")
    service = get_gmail_service()
    message = MIMEText(body_html, "html")
    message["To"] = to_address
    message["From"] = sender
    message["Subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return service.users().messages().send(userId="me", body={"raw": raw}).execute()
