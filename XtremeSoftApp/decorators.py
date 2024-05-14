from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden

def check_user_role(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user == "AnonymousUser" or not hasattr(request.user, 'rol') or request.user.rol != required_role:
                return redirect('acceso_denegado')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def check_user_roles(required_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user == "AnonymousUser" or not hasattr(request.user, 'rol') or request.user.rol not  in required_roles:
                return redirect('acceso_denegado')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def user_required(view_func):
    decorated_view_func = login_required(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_active:
            return redirect('do_login')
        return decorated_view_func(request, *args, **kwargs)
    return wrapper

def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden()
            if not request.user.role == role:
                return HttpResponseForbidden()
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator