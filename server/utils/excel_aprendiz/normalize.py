import re

FIREBASE_KEY_FORBIDDEN = re.compile(r"[\.\$#\[\]/]")


def _normalizar_header(celda: object) -> str:
    if celda is None:
        return ""
    return str(celda).strip().lower().replace(" ", "")


def _celda_str(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_document_key(raw_document: str) -> str | None:
    if not raw_document or not isinstance(raw_document, str):
        return None
    cleaned = raw_document.strip()
    if not cleaned:
        return None
    if FIREBASE_KEY_FORBIDDEN.search(cleaned):
        return None
    if len(cleaned) > 50:
        return None
    return cleaned
