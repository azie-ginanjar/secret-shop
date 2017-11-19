import hashlib


def toSHA256(value):
    return hashlib.sha256(value).hexdigest()