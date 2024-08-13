from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.conf import settings
import uuid
import msal
import django.contrib.auth as auth
from models.models import Role, RoleUser

from django.contrib.auth.models import User

def index(request: HttpRequest):
    return HttpResponse("")

def logout(request: HttpRequest):
    auth.logout(request)
    return HttpResponse("You have been logged out. You can close this window.")

def changepass(request: HttpRequest):
    return HttpResponse("There is no password to change!")

def login(request: HttpRequest):
    for key, value in request.GET.items():
        request.session[key] = value
    AUTHORITY = "https://login.microsoftonline.com/common"
    app = msal.ConfidentialClientApplication(settings.MICROSOFT_ID, authority=AUTHORITY,
                                             client_credential=settings.MICROSOFT_TOKEN)
    callback_url = request.build_absolute_uri("/callback")
    SCOPE = ["User.Read"]
    url = app.get_authorization_request_url(SCOPE, state=str(uuid.uuid4()), redirect_uri=callback_url)
    return redirect(url)

def callback(request: HttpRequest):
    ses = {}
    for key, value in request.session.items():
        if not key.startswith("_"):
            ses[key] = value
    if request.user.is_authenticated:
        auth.logout(request)
    params = request.GET
    if 'code' not in params or 'state' not in params or 'session_state' not in params:
        return HttpResponseBadRequest("Missing code and session state! " +
                                      "You probably are signed in using your personal Microsoft account. "
                                      "Clear your cookies and if the issue persists contact technical@cses.carleton.ca")
    code = params['code']
    # state = params['state']
    # session_state = params['session_state']
    AUTHORITY = "https://login.microsoftonline.com/common"
    app = msal.ConfidentialClientApplication(settings.MICROSOFT_ID, authority=AUTHORITY,
                                             client_credential=settings.MICROSOFT_TOKEN)
    SCOPE = []
    callback_url = request.build_absolute_uri("/callback")
    token = app.acquire_token_by_authorization_code(code, SCOPE, redirect_uri=callback_url)
    if 'id_token_claims' not in token:
        return HttpResponseBadRequest("Invalid or expired code!")
    email = token['id_token_claims']['preferred_username'].lower()
    roles = RoleUser.objects.filter(user_email=email)
    for key, value in ses.items():
        request.session[key] = value
    request.session['email'] = email
    return render(request, "pick_role.html", {"roles": roles})

def pick_role(request: HttpRequest):
    ses = {}
    for key, value in request.session.items():
        if not key.startswith("_"):
            ses[key] = value
    email = request.session['email']
    role = request.POST['role']
    roles = RoleUser.objects.filter(user_email=email, role__email=role).first()
    if roles is None:
        return HttpResponseBadRequest("Invalid choice!")
    user = User.objects.filter(email=role).first()
    if user is None:
        user = User(username=role, email=role)
        user.save()

    auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    for key, value in ses.items():
        request.session[key] = value
    return redirect("/idp/login/process")
