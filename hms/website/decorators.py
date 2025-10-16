from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

# Custom decorator to check if the user belongs to a specific group
def group_required(group_name):
    def decorator(view_func):
        @login_required  # Using Django's built-in login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return _wrapped_view
    return decorator

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Show a message if the user is not logged in
            messages.error(request, "You must be logged in to view this page.")
            return redirect('home')  # Redirect to the home page
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Decorator to check if the user is a staff member
def staff_required(view_func):
    @wraps(view_func)
    @login_required  # Ensuring the user is logged in first
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            messages.success(request, "You Must be Admin to view this Page!")
            return redirect('home')
    return _wrapped_view
