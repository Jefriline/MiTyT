def mask_email(email: str) -> str:
    if not email or not isinstance(email, str):
        return email or ""
    email = email.strip()
    if "@" not in email:
        return email
    local, _, domain = email.partition("@")
    if len(local) <= 5:
        visible = min(2, len(local))
        return local[:visible] + "*" * (len(local) - visible) + "@" + domain
    first = 4
    last = 3
    asterisks = 7
    return local[:first] + "*" * asterisks + local[-last:] + "@" + domain
