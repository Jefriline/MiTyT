import re

FIREBASE_KEY_FORBIDDEN = re.compile(r"[\.\$#\[\]/]")
# Espacios y caracteres invisibles que suelen venir al pegar/escribir en movil (ej. iPhone)
WHITESPACE_AND_INVISIBLE = re.compile(r"[\s\u00a0\u200b\u200c\u200d\ufeff]+")
# Digitos de ancho completo (Unicode), comunes al pegar en iOS: ０(U+FF10) a ９(U+FF19)
FULLWIDTH_TO_HALFWIDTH = str.maketrans("０１２３４５６７８９", "0123456789")


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
    with_normal_digits = cleaned.translate(FULLWIDTH_TO_HALFWIDTH)
    without_spaces_and_invisible = WHITESPACE_AND_INVISIBLE.sub("", with_normal_digits)
    key_without_forbidden = FIREBASE_KEY_FORBIDDEN.sub("", without_spaces_and_invisible)
    key_final = key_without_forbidden.strip()
    if not key_final or len(key_final) > 50:
        return None
    return key_final
