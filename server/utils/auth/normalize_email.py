import re


FIREBASE_EMAIL_KEY_FORBIDDEN = re.compile(r"[\$#\[\]/]")


def normalize_email_key(email: str) -> str | None:
    if not email or not isinstance(email, str):
        return None
    cleaned = email.strip().lower()
    if not cleaned:
        return None

    cleaned = cleaned.replace("@", "_at_")
    cleaned = cleaned.replace(".", "_dot_")

    if FIREBASE_EMAIL_KEY_FORBIDDEN.search(cleaned):
        return None

    if len(cleaned) > 100:
        return None

    return cleaned

