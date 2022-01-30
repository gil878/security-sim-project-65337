import bcrypt
from loginApp.models import User

def passwored_hasher(password):
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode('utf8')

def hashed_password_validation(password,hashed):
    return bcrypt.checkpw(password.encode('utf8'),hashed.encode('utf8'))

def encode_and_hash(string):
    string = string.encode()
    return passwored_hasher(string)


def get_pass_history(user='',email=''):
    history = User.objects.raw("SELECT * FROM djangodb.loginApp_user WHERE username=\'"+user +"'") if user!='' else User.objects.raw("SELECT * FROM djangodb.loginApp_user WHERE email=\'"+email +"'")
    return history[0].history
    
def edite_history(history_array,new_pass,history_length):
    if len(history_array) < history_length:
        history_array.append(new_pass)
        return history_array
    return history_array

def history_to_string(array):
    res=''
    for i in array:
        res+=str(i)+' '
    res.strip()
    return res

def history_to_array(string,history_length):
    res = string.strip().split(' ')
    print(res)
    return res

def history(string,history_length,user='',email=''):
    history_str = get_pass_history(user,email)
    array = history_to_array(history_str,history_length)
    print(array)
    array= edite_history(array,string,history_length)
    print(array)
    return history_to_string(array)





