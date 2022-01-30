from django.core.exceptions import ValidationError
from django.utils.translation import ugettext
import re
from  django.core.validators import RegexValidator as validator

class password_custome_validate():
    class NumberValidator(validator):
        def validate(self, password, user=None):
            if not re.findall('[0-9]', password):
                print(password)
                raise ValidationError(
                    ugettext("The password must contain at least 1 digit, 0-9."),
                    code='password_no_number',
                )
        def get_help_text(self):
            return ugettext("Your password must contain at least 1 digit, 0-9.")
        
    class UppercaseValidator(validator):
        def validate(self, password, user=None):
            if not re.findall('[A-Z]', password):
                raise ValidationError(
                ugettext("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )
        def get_help_text(self):
            return ugettext("Your password must contain at least 1 uppercase letter, A-Z.")
            
    class LowercaseValidator(validator):
        def validate(self, password, user=None):
            if not re.findall('[a-z]', password):
                raise ValidationError(
                    ugettext("The password must contain at least 1 lowercase letter, a-z."),
                    code='password_no_lower',
                    )
        def get_help_text(self):
            return ugettext("Your password must contain at least 1 lowercase letter, a-z.")
        
    class SymbolValidator(validator):
        symbols='[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]'
        def validate(self, password, user=None):
            if not re.findall(self.symbols, password):
                raise ValidationError(
                    ugettext("The password must contain at least 1 symbol: " +
                             self.symbols),
                    code='password_no_symbol',
                )
        def get_help_text(self):
            return ugettext("Your password must contain at least 1 symbol: " + self.symbols)
        
    def validate(self,password,user=None):
        self.SymbolValidator().validate(password,user=None)
        self.UppercaseValidator().validate(password,user=None)
        self.LowercaseValidator().validate(password,user=None)
        self.NumberValidator().validate(password,user=None)
    
    def validate_repeat(password,repeat):
        return password == repeat