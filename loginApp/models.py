from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models.fields import CharField
from loginApp.password_validator import password_custome_validate as validator
from loginApp.CustomManager import CustomManager

# Create your models here.
class User(AbstractBaseUser):
    username = CharField(max_length=255,unique=True)
    password = CharField(max_length=255,validators=[validator.NumberValidator().validate,validator.SymbolValidator().validate,validator.LowercaseValidator().validate,validator.UppercaseValidator().validate])
    email = CharField(max_length=100)
    history = CharField(max_length=62)
    
    objects=CustomManager()
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    @property
    def is_authenticated(self):
        return True
    
    class Meta:
        db_table = 'loginapp_user'

class SeasonCode(models.Model):
    email = CharField(max_length=100)
    code = CharField(max_length=255)
