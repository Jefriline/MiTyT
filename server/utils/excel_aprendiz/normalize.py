import re
import unicodedata

# Solo digitos 0-9: quita espacios, puntos, guiones, fullwidth, zero-width, etc.
NON_DIGIT = re.compile(r"\D")


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
    normalized_unicode = unicodedata.normalize("NFKC", raw_document.strip())
    digits_only = NON_DIGIT.sub("", normalized_unicode)
    if not digits_only or len(digits_only) > 50:
        return None
    return digits_only
