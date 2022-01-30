from django.db import connection
from django.db.models.query import RawQuerySet
from django.db.utils import IntegrityError, ProgrammingError
from django.shortcuts import redirect, render
from loginApp.forms import *
from loginApp.passwordUtile import *
from loginApp.passwordUtile import encode_and_hash as hash_pass 
from django.views.decorators.csrf import csrf_protect
from loginApp.models import SeasonCode, User 
import random
import string
import hashlib
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login
from django.core import exceptions
from django.db import Error,IntegrityError



# Create your views here.
def login_view(request):
    user=''
    enter_valid = False   
    if(request.method == 'Get'):
        if(len(request.GET) == 0):#first load
            return render(request,"login_page.html",{'register_url':'register/','forgot_url':'forgot/'})
    elif request.method == 'POST':
        user = request.POST.get('user_field','')
        password = request.POST.get('password_field','')
        try:
            rows,enter_valid,messege = get_rows_not_secure(user,password,'login')
            
        except Error as e:
            return render(request,"login_page.html",{'messege':str(e)+"\nNot valid credentials",'register_url':'register/','forgot_url':'forgot/'})
        
        if enter_valid:
            login(request,user=rows[0])
            return redirect('system/')
        else:
            for item in rows:
                messege+=str(item)
            return render(request,"login_page.html",{'messege':messege+"\nNot valid credentials",'register_url':'register/','forgot_url':'forgot/'})
    return render(request,"login_page.html",{'messege':'','register_url':'register/','forgot_url':'forgot/'})
    

def register_view(request):
    messege = ''
    if request.method == 'POST':
        user = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email','')
        repeat = request.POST.get('reg_repeat_field','')
        if(password != repeat):
            messege += 'Password fields are not the same'
            return render(request,"register_page.html",{'messege':messege})
        form = register_form(request.POST)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO djangodb.loginapp_user(id,last_login,password,email,history,username) VALUES (0,NULL,'"+passwored_hasher(password)+"','"+email+"','','"+user+"')")
                #create_row(user,password,email)
            except Error as e:
                messege+=str(e)
                return render(request,"register_page.html",{'messege':messege})
            return redirect('/')
        else:
            error_dict = dict(form.errors)
            print(error_dict)
            for key in error_dict:
                messege += error_dict[key]
            return render(request,"register_page.html",{'messege':messege})       
    return render(request,"register_page.html",{})
             


def forgot_view(request):
    email =''
    if request.method == 'GET':
        if(len(request.GET) == 0):#first load
            return render(request,"Forgot_Password.html",{})
        
        email = request.GET.get('email_input','')
        #check if email in db
        if is_email_exists(email):
            return render(request,"Forgot_Password.html",{'messege':'Code was already send','email_p':email})
        row = get_rows_by_email(email)
        if(RawQuerySet_isempty(row)==False):
            #generate send code
            code = generate_code()
            print(code)
            send_mail(
                'Password Change Code',#mailtitle
                'Code: '+code,#mail body
                'geda34385@gmail.com',#from
                [email],#to (hardcode to minimize damage)
                fail_silently=False,)
            code = hashlib.sha1(code.encode())
            SeasonCode.objects.create(email=email,code=code.hexdigest())
            return render(request,"Forgot_Password.html",{'messeg':'Code was send','email_p':email})
        else:
            return render(request,"Forgot_Password.html",{'messege':'Email was not found'})
        
    elif(request.method == 'POST'):
        
        email = request.POST.get('email_paragraph','')
        code = request.POST.get('code_input','')
        print(code)
        print(email)
        if(code != "" and email !=''):
            print("hererererererererer")
            code = hashlib.sha1(code.encode()).hexdigest()
            print(code)
            row =  SeasonCode.objects.raw('SELECT * FROM djangodb.loginapp_seasoncode WHERE email=\'' + email+"'")
            if(row[0].code == code and RawQuerySet_isempty(row)==False):
                SeasonCode.objects.filter(code=code).delete()
                return redirect('change_password/'+email+'/')
            else:
                return render(request,"Forgot_Password.html",{'messege':'incorrect code'})
        else:
            return render(request,"Forgot_Password.html",{'messege':'no code was found, or no Email'})
        
    return render(request,"Forgot_Password.html",{})

@login_required(redirect_field_name='/',login_url='/')
def system_view(request):
    messege=''
    if request.method=='POST':
        user = request.POST.get('username','')
        password = request.POST.get('password','')
        email = request.POST.get('email','')
        form = register_form(request.POST)
        if(form.is_valid()): 
            create_row(user,password,email)
            return redirect('/system/')
        elif(RawQuerySet_isempty(get_rows(user))==False):
            return render(request,"system_page.html",{'messege':'user already exists'})
        else:
            error_dict = dict(form.errors)
            print(error_dict)
            for key in error_dict:
                messege += error_dict[key]
            return render(request,"system_page.html",{'messege':messege})
    return render(request,"system_page.html",{'messege':'','pass_change_url':'/system/change_password/'})

@login_required(redirect_field_name='/',login_url='/system/change_password/')
def change_pass_view(request):
    print(request.user.is_authenticated)
    error_msg=''
    if(request.method =='POST'):
        password = request.POST.get('currPassIn','')
        new_password = request.POST.get('password','')
        repeat=request.POST.get('newPass2','')
        condition1 = new_password==repeat
        row = User.objects.raw('SELECT * FROM djangodb.loginapp_user WHERE username=\'' + request.user.username+"'")
        condition2 = hashed_password_validation(password,row[0].password)
        if(condition1 and condition2):
            print("here")
            form = forgot_form(request.POST)
            if form.is_valid():
                User.objects.filter(username=request.user.username).update(password=passwored_hasher(new_password),history=history(user=request.user.username,string=new_password,history_length=3,email=request.user.email))
                logout(request)
                return redirect('/system/')
            else:
                error_dict = dict(form.errors)
                print(error_dict)
                for key in error_dict:
                    error_msg += error_dict[key]
                return render(request,"change_password.html",{'messege':error_msg})
                
        return render(request,"change_password.html",{'messege':'passwords were not the same or incorrect password'})
    return render(request,"change_password.html",{})

def forgot_change_pass_view(request,email):
    messege=''
    if(request.method =='POST'):
        new_password = request.POST.get('password','')
        repeat=request.POST.get('newPass2','')
        if(new_password==repeat):
            form = forgot_form(request.POST)
            if form.is_valid():
                User.objects.filter(email=email).update(password=passwored_hasher(new_password),history=history(email=email,string=new_password,history_length=3))
                return redirect('/')
            else:
                error_dict = dict(form.errors)
                for key in error_dict:
                    messege += error_dict[key]
                return render(request,"forgor_pass_change.html",{'messege':messege})
        return render(request,"forgor_pass_change.html",{'messege':'passwords were not the same'})
    return render(request,'forgor_pass_change.html',{})





def get_rows_by_email(email):
    return User.objects.raw('SELECT * FROM djangodb.loginapp_user WHERE email=\'' + email +"'")
            

def create_row(username,password,email):
    result = None
    if(username is not None and password is not None and email is not None):
        if(RawQuerySet_isempty(get_rows_by_email(email))):
            result = User.objects.create(username=username,password=passwored_hasher(password),email=email)
    return result

def RawQuerySet_isempty(rawset):
    list =[]
    for index in range(0,len(rawset)):
        list.append(rawset[index])
    return len(list) == 0
    
def generate_code():
    letters = string.ascii_letters #+ string.digits
    return ''.join(random.choice(letters) for i in range(4))

def is_email_exists(email):
    row = SeasonCode.objects.raw('SELECT * FROM djangodb.loginapp_seasoncode WHERE email=\'' + email+"'")
    return row != None and RawQuerySet_isempty(row)==False


def printRawQuery(raw_query):
    for row in raw_query:
        print(row)

def get_rows_secure(user,password,page=''):#secured using sql params
    messege=''
    enter_valid = False
    rows = get_rows(user)
    print(rows)
    if(RawQuerySet_isempty(rows)):
        enter_valid = False
    else:
       enter_valid = (rows[0].username == user) and (hashed_password_validation(password,rows[0].password)) and page=='login'
    return rows,enter_valid,messege
       
def get_rows_not_secure(user,password,page=''):
    enter_valid=False
    rows,messege = model_sql_query(user)
    if(RawQuerySet_isempty(rows)):
        enter_valid = False
    else:
        enter_valid = (rows[0].username == user) and (hashed_password_validation(password,rows[0].password)) and page=='login'
    return rows,enter_valid,messege      
       
def get_rows(from_user,email =''):#secured using sql params
    print(from_user)    
    result =  User.objects.raw('SELECT * FROM djangodb.loginapp_user WHERE username=%s',params=[from_user])
    if(email != ''):
       result =  User.objects.raw('SELECT * FROM djangodb.loginapp_user WHERE username=%s email=%s',params=[from_user,email])
    return result


def my_custom_sql(username):
    messege=''
    with connection.cursor() as cursor:
        try:
            cursor.execute('SELECT * FROM djangodb.loginapp_user WHERE username=\'' + username +"'")
        except Exception as e:
            messege+=str(e)            
        row = cursor.fetchall()
        res_row = list()
        for tuple in row:
            res_row.append(User(username=tuple[1]))
        print(res_row)
        print(messege)
    return res_row,messege

def model_sql_query(username):
    result = User.objects.raw('SELECT * FROM djangodb.loginapp_user WHERE username=\'' + username +"'")
    print(result)
    return result,''
        
    