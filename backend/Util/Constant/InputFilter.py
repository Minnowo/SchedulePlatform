import re

#Some constants for User validation:

NAME_MAX_LEN = 29
NAME_MIN_LEN = 4

PASS_MAX_LEN = 255
PASS_MIN_LEN = 8

ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'


# matches a-z A-Z 0-9 and _  4 <-> 29 times 
IS_VALID_NAME_1 = re.compile(r"^[a-zA-Z0-9_]{4,29}$") # ensures valid < 4 and > 29
IS_VALID_NAME_2 = re.compile(r"^[a-zA-Z0-9_]+$")      # only ensures valid chars 


def check_username_string(username: str) -> bool:

    # #Check type & length
    
    l = len(username)
    
    if not isinstance(username, str) or l < NAME_MIN_LEN or l > NAME_MAX_LEN:
        return False 

    # since length check above is faster use #2 here 
    return IS_VALID_NAME_2.match(username) is not None 


# validating email is very hard without actually sending an email,
# if you're not using the email for anything this is probably fine,
# but otherwise this is probably a bad idea 
# should look at https://stackoverflow.com/a/201378 if you really want more accurate emails with regex 

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

    # fixed this ( removed the | at the end, this was meant to be 'OR' but it actually made it match '|' chars)
    # example: helloworld@gmail.c|m was valid, this is no longer the case 
    validate_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'  

    if not re.fullmatch(validate_email, email):
        return False

    return True

def check_password_string(password: str) -> bool:

    if not isinstance(password, str) or len(password) > PASS_MAX_LEN or len(password) < PASS_MIN_LEN:
        return False
    return True





# this is just testing to ensure valid regex 
if __name__ == "__main__":
    import hashlib 
    import random 
    
    def generate_valid_sample_data():

        d = set()

        for i in range(10000):

            # random string of hexadecimal 
            sha = hashlib.md5()
            sha.update(str(i + random.randint(0, 50)).encode())
            sha = sha.digest().hex()

            d.add( sha[0:25] )

        return d 


    def generate_invalid_sample_data( random_length = False ):

        d = set()
        
        invalid_chars = "@#$%^&*()-{}/,.`~\\][';\""

        for i in range(10000):

            # random string of hexadecimal 
            sha = hashlib.md5()
            sha.update(str(i + random.randint(0, 50)).encode())
            sha = sha.digest().hex()

            ii = random.randint(0, 24)
            iii = random.randint(0, len(invalid_chars) - 1)

            if not random_length:

                d.add( sha[0:ii] + invalid_chars[iii] + sha[ii:25] )

            else:
                
                # will either be the same length as above or twice the length 
                d.add( ( sha[0:ii] + invalid_chars[iii] + sha[ii:25] ) * random.randint(1,2) )

        return d 

    # print("checking valid garbage names:")
    # for valid in generate_valid_sample_data():
    #     _ = check_username_string(valid)

    #     print("  ", _ , " ", valid)

    #     if not _:
    #         raise Exception("The string '{}' was not considered valid, this does not make sense, check the 'check_username_string' function".format(valid))


    # print("checking invalid garbage names:")
    # for valid in generate_invalid_sample_data():
        
    #     _ = check_username_string(valid)
    #     print("  ", _ , " ", valid)

    #     if _:
    #         raise Exception("The string '{}' was considered valid, this does not make sense, check the 'check_username_string' function".format(valid))


    # print("checking invalid garbage names:")
    # for valid in generate_invalid_sample_data(True):
        
    #     _ = check_username_string(valid)
    #     print("  ", _ , " ", valid)

    #     if _:
    #         raise Exception("The string '{}' was considered valid, this does not make sense, check the 'check_username_string' function".format(valid))

    print(check_email_string(""))