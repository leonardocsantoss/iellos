# -*- coding:utf-8 -*-
import re

from django import forms
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.hashcompat import sha_constructor

from account.utils import get_send_mail
send_mail = get_send_mail()

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site

from emailconfirmation.models import EmailAddress
from account.models import Account, PasswordReset

alnum_re = re.compile(r'^\w+$')


class LoginForm(forms.Form):
    
    username = forms.CharField(label=_(u"Usuário ou email"))
    password = forms.CharField(label=_(u"Senha"), widget=forms.PasswordInput(render_value=False))
    remember = forms.BooleanField(label=_(u"Continuar conectado"), help_text=_(u"Se marcada, você vai ficar conectado por 3 semanas"), required=False)
    
    user = None
    
    def clean(self):
        if self._errors:
            return
        user = authenticate(username=self.cleaned_data["username"], password=self.cleaned_data["password"])
        if user is None:
            try:
                usuario = User.objects.get(email=self.cleaned_data["username"])
                user = authenticate(username=usuario.username, password=self.cleaned_data["password"])
            except:
                pass

        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_(u"Esta conta está inativa."))
        else:
            raise forms.ValidationError(_(u"Os dados que você especificou não estão corretos."))
        return self.cleaned_data
    
    def login(self, request):
        if self.is_valid():
            login(request, self.user)
            if self.cleaned_data['remember']:
                request.session.set_expiry(60 * 60 * 24 * 7 * 3)
            else:
                request.session.set_expiry(0)
            return True
        return False

class SignupForm(forms.Form):

    usuario = forms.CharField(max_length=30, label=_(u"Usuário"), help_text=_(u'Informe um nome de usuário.'))
    nome = forms.CharField(max_length=30, label=_(u"Nome"), help_text=_(u'Informe o seu nome.'))
    sobrenome = forms.CharField(max_length=30, label=_(u"Sobrenome"), help_text=_(u'Informe o seu sobrenome.'))
    email = forms.EmailField(label=_(u"E-mail"), help_text=_(u'Informe o seu e-mail.'), max_length=30)
    password1 = forms.CharField(label=_(u"Senha"), help_text=_(u'Informe uma senha.'), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_(u"Senha (novamente)"), help_text=_(u'Informe uma senha novamente.'), widget=forms.PasswordInput(render_value=False))
    confirmation_key = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput())
    

    def clean_email(self):
        try:
            user = User.objects.get(email=self.cleaned_data["email"])
        except User.DoesNotExist:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"Este email já está cadastrado."))

    def clean_usuario(self):
        if not alnum_re.search(self.cleaned_data["usuario"]):
            raise forms.ValidationError(_(u"Usuario só pode ter letras, numeros e underlines."))
        try:
            user = User.objects.get(username__iexact=self.cleaned_data["usuario"])
        except User.DoesNotExist:
            return self.cleaned_data["usuario"]
        raise forms.ValidationError(_(u"Este usuário já está cadastrado."))
    
    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_(u"Você deve digitar a mesma senha novamente."))
        return self.cleaned_data
    
    def save(self):
        username = self.cleaned_data["usuario"]
        nome = self.cleaned_data["nome"]
        sobrenome = self.cleaned_data["sobrenome"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]

        confirm = settings.ACCOUNT_EMAIL_VERIFICATION
        
        # @@@ clean up some of the repetition below -- DRY!
        
        if confirm:
            new_user = User.objects.create_user(username, email, password)
            if email:
                EmailAddress.objects.add_email(new_user, email)
        else:
            new_user = User.objects.create_user(username, email, password)
            EmailAddress(user=new_user, email=email, verified=True, primary=True).save()
        
        if settings.ACCOUNT_EMAIL_VERIFICATION:
            new_user.is_active = False

        new_user.first_name = nome
        new_user.last_name = sobrenome
        new_user.save()
        new_user.message_set.create( message=ugettext(u"<b>@%(username)s</b> seja bem vindo ao iellos!\nCrie seus elos, convide seus amigos e compartilhe informações.") % { 'username': new_user.username })

        return username, password # required for authenticate()



class UserForm(forms.Form):
    
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class AccountForm(UserForm):
    
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        try:
            self.account = Account.objects.get(user=self.user)
        except Account.DoesNotExist:
            self.account = Account(user=self.user)


class ChangePasswordForm(UserForm):
    
    oldpassword = forms.CharField(label=_(u"Senha atual"), widget=forms.PasswordInput(render_value=False))
    password1 = forms.CharField(label=_(u"Nova senha"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_(u"Nova senha (novamente)"), widget=forms.PasswordInput(render_value=False))
    
    def clean_oldpassword(self):
        if not self.user.check_password(self.cleaned_data.get("oldpassword")):
            raise forms.ValidationError(_(u"Por favor entre com sua senha."))
        return self.cleaned_data["oldpassword"]
    
    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_(u"Você deve digitar a mesma senha novamente."))
        return self.cleaned_data["password2"]
    
    def save(self):
        self.user.set_password(self.cleaned_data['password1'])
        self.user.save()
        self.user.message_set.create(message=ugettext(u"Sua senha foi alterada com sucesso."))


class SetPasswordForm(UserForm):
    
    password1 = forms.CharField(label=_(u"Senha"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_(u"Senha (digite novamente)"), widget=forms.PasswordInput(render_value=False))
    
    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_(u"Você deve digitar a mesma senha novamente novamente."))
        return self.cleaned_data["password2"]
    
    def save(self):
        self.user.set_password(self.cleaned_data["password1"])
        self.user.save()
        self.user.message_set.create(message=ugettext(u"Sua senha foi alterada com sucesso."))


class ResetPasswordForm(forms.Form):
    
    email = forms.EmailField(label=_("Email"), required=True, widget=forms.TextInput(attrs={'size':'30'}))
    
    def clean_email(self):
        if EmailAddress.objects.filter(email__iexact=self.cleaned_data["email"], verified=True).count() == 0:
            raise forms.ValidationError(_(u"Endereço de email não verificado."))
        return self.cleaned_data["email"]
    
    def save(self):
        for user in User.objects.filter(email__iexact=self.cleaned_data["email"]):
            temp_key = sha_constructor("%s%s%s" % (
                settings.SECRET_KEY,
                user.email,
                settings.SECRET_KEY,
            )).hexdigest()
            
            # save it to the password reset model
            password_reset = PasswordReset(user=user, temp_key=temp_key)
            password_reset.save()
            
            current_site = Site.objects.get_current()
            domain = unicode(current_site.domain)
            
            #send the password reset email
            subject = _(u"Email de redefinição de senha enviado")
            message = render_to_string("account/password_reset_key_message.txt", {
                "user": user,
                "temp_key": temp_key,
                "domain": domain,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], priority="high")
        return self.cleaned_data["email"]


class ResetPasswordKeyForm(forms.Form):
    
    password1 = forms.CharField(label=_(u"Nova senha"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_(u"Nova senha (digite novamente)"), widget=forms.PasswordInput(render_value=False))
    temp_key = forms.CharField(widget=forms.HiddenInput)
    
    def clean_temp_key(self):
        temp_key = self.cleaned_data.get("temp_key")
        if not PasswordReset.objects.filter(temp_key=temp_key, reset=False).count() == 1:
            raise forms.ValidationError(_(u"A chave temporária é inválida."))
        return temp_key
    
    def clean_password2(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(_(u"Você deve digitar a mesma senha novamente novamente."))
        return self.cleaned_data["password2"]
    
    def save(self):
        # get the password_reset object
        temp_key = self.cleaned_data.get("temp_key")
        password_reset = PasswordReset.objects.get(temp_key__exact=temp_key)
        
        # now set the new user password
        user = User.objects.get(passwordreset__exact=password_reset)
        user.set_password(self.cleaned_data["password1"])
        user.save()
        user.message_set.create(message=ugettext(u"Senha alterada com sucesso."))
        
        # change all the password reset records to this person to be true.
        for password_reset in PasswordReset.objects.filter(user=user):
            password_reset.reset = True
            password_reset.save()


class ChangeLanguageForm(AccountForm):
    
    language = forms.ChoiceField(label=_(u"Linguagem"), required=True, choices=settings.LANGUAGES)
    
    def __init__(self, *args, **kwargs):
        super(ChangeLanguageForm, self).__init__(*args, **kwargs)
        self.initial.update({"language": self.account.language})
    
    def save(self):
        self.account.language = self.cleaned_data["language"]
        self.account.save()
        self.user.message_set.create(message=ugettext(u"Linguagem alterada com sucesso."))