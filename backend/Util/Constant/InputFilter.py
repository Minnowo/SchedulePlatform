import re

#Some constants for User validation:

NAME_MAX_LEN = 29
NAME_MIN_LEN = 4

PASS_MAX_LEN = 255
PASS_MIN_LEN = 8

ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'

def check_username_string(username: str) -> bool:

    #Check type & length
    if not isinstance(username, str) or len(username) > NAME_MAX_LEN or len(username) < NAME_MIN_LEN:
        return False

    #Check characters

    for i in username:
        if i not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789':
            return False

    return True        

def check_email_string(email: str) -> bool:

    #Check type & length (Email & Password field have same # of available chars)
    if not isinstance(email, str) or len(email) > PASS_MAX_LEN or len(email) < PASS_MIN_LEN:
        return False

    """
    Regular Expression validate email strings:

    >> username of email | a-z, A-Z, 0,9
    >> followed by an '@'
    >> followed by another a-z, A-Z, 0,9 string (the domain name)
    >> followed by a dot '.' , then a 2-n length string of a-z || A-Z (com,ca,cz,de,ru) (the DNS)

    username @ domain . dns

    """

    validate_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  

    if not re.fullmatch(validate_email, email):
        return False

    return True

def check_password_string(password: str) -> bool:

    if not isinstance(password, str) or len(password) > PASS_MAX_LEN or len(password) < PASS_MIN_LEN:
        return False
    return True