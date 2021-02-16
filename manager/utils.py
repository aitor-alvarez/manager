from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect

from social.exceptions import AuthForbidden


def logout_clean(request):
    logout(request)
    return redirect('https://accounts.google.com/Logout?&continue=https://www.google.com')


def auth_allowed(response, details, *args, **kwargs):
    
    try:
        # print 'Google USER ==> ', details
        soc_user = User.objects.get(email=details.get('email'))
        return soc_user
    except:
        return None


def soc_auth_allowed(backend, details, response, *args, **kwargs):

    soc_user = auth_allowed(response, details)
    if not soc_user:
        raise AuthForbidden(backend)
    else:
        return {'user': soc_user}


def soc_social_user(backend, uid, user=None, *args, **kwargs):

    if user:
        provider = backend.name
        social = backend.strategy.storage.user.get_social_auth(provider, uid)
        if not social:  # user has not logged in previously (e.g., no social auth obj exists) -- make their account active.
            user.is_active = True
    else:
        raise AuthForbidden(backend)
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}

