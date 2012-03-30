# -*- coding:utf-8 -*-
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from account.utils import get_default_redirect
from account.forms import SignupForm, LoginForm, \
    ChangePasswordForm, SetPasswordForm, ResetPasswordForm, \
    ChangeLanguageForm, ResetPasswordKeyForm

    
def login(request, form_class=LoginForm, template_name="login.html", success_url=None):
    if success_url is None:
        success_url = get_default_redirect(request)
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = form_class(request.POST)
            if form.login(request):
                return HttpResponseRedirect(success_url)
        else:
            form = form_class()
        ctx = {
            "form": form,
        }
        return render_to_response(template_name, ctx,
            context_instance = RequestContext(request)
        )
    else:
        return HttpResponseRedirect(success_url)

def signup(request, form_class=SignupForm,
        template_name="account/signup.html", success_url=None):
    if success_url is None:
        success_url = get_default_redirect(request)
    if not request.user.is_authenticated():
        if request.method == "POST":
            form = form_class(request.POST)
            if form.is_valid():
                username, password = form.save()
                if settings.ACCOUNT_EMAIL_VERIFICATION:
                    return render_to_response("account/verification_sent.html", {
                        "email": form.cleaned_data["email"],
                    }, context_instance=RequestContext(request))
                else:
                    user = authenticate(username=username, password=password)
                    auth_login(request, user)
                    return HttpResponseRedirect(success_url)
        else:
            form = form_class()
        return render_to_response(template_name,
              context_instance=RequestContext(
                    request,
                    { "form": form,
                    }
            )
        )
    else:
        return HttpResponseRedirect(success_url)

@login_required
def password_change(request, form_class=ChangePasswordForm,
        template_name="account/password_change.html"):
    if not request.user.password:
        return HttpResponseRedirect(reverse("acct_passwd_set"))
    if request.method == "POST":
        password_change_form = form_class(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            password_change_form = form_class(request.user)
    else:
        password_change_form = form_class(request.user)
    return render_to_response(template_name, {
        "password_change_form": password_change_form,
    }, context_instance=RequestContext(request))

@login_required
def password_set(request, form_class=SetPasswordForm,
        template_name="account/password_set.html"):
    if request.user.password:
        return HttpResponseRedirect(reverse("acct_passwd"))
    if request.method == "POST":
        password_set_form = form_class(request.user, request.POST)
        if password_set_form.is_valid():
            password_set_form.save()
            return HttpResponseRedirect(reverse("acct_passwd"))
    else:
        password_set_form = form_class(request.user)
    return render_to_response(template_name, {
        "password_set_form": password_set_form,
    }, context_instance=RequestContext(request))


def password_reset(request, form_class=ResetPasswordForm,
        template_name="account/password_reset.html",
        template_name_done="account/password_reset_done.html"):
    if request.method == "POST":
        password_reset_form = form_class(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.save()
            return render_to_response(template_name_done, {
                "email": email,
            }, context_instance=RequestContext(request))
    else:
        password_reset_form = form_class()
    
    return render_to_response(template_name, {
        "password_reset_form": password_reset_form,
    }, context_instance=RequestContext(request))
    
def password_reset_from_key(request, key, form_class=ResetPasswordKeyForm,
        template_name="account/password_reset_from_key.html"):
    if request.method == "POST":
        password_reset_key_form = form_class(request.POST)
        if password_reset_key_form.is_valid():
            password_reset_key_form.save()
            password_reset_key_form = None
    else:
        password_reset_key_form = form_class(initial={"temp_key": key})
    
    return render_to_response(template_name, {
        "form": password_reset_key_form,
    }, context_instance=RequestContext(request))

@login_required
def language_change(request, form_class=ChangeLanguageForm,
        template_name="account/language_change.html"):
    if request.method == "POST":
        form = form_class(request.user, request.POST)
        if form.is_valid():
            form.save()
            next = request.META.get('HTTP_REFERER', None)
            return HttpResponseRedirect(next)
    else:
        form = form_class(request.user)
    return render_to_response(template_name, {
        "form": form,
    }, context_instance=RequestContext(request))