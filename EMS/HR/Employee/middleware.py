# Employee/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class BlockAccessAfterLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is not authenticated and the logout flag is set
        if not request.user.is_authenticated and request.session.get('logged_out', False):
            # Clear the logout flag from the session
            del request.session['logged_out']
            # Redirect to the login page
            return redirect(reverse('login'))

        return response
