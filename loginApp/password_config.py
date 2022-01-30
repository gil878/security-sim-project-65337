import string

class PasswordConfig:
    min_length = 10
    password_char_set = string.ascii_letters+string.digits+string.punctuation+' '
    pass_history=3
    blacklisted_words=[]
    login_attemp=3
