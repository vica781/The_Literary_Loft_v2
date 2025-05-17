"""Custom middleware to debug sessions and migrate 'cart' to 'bag'."""

import logging

logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class SessionDebugMiddleware:
    """Middleware to ensure sessions exist and migrate 'cart' to 'bag'."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure the session exists
        if not request.session.session_key:
            request.session.create()
            logger.debug(
                "Middleware: Created session with ID: %s",
                request.session.session_key
            )

        # Migrate old 'cart' key to 'bag' if needed
        if 'cart' in request.session and 'bag' not in request.session:
            request.session['bag'] = request.session['cart'].copy()
            del request.session['cart']  # Optional cleanup
            request.session.modified = True
            logger.debug(
                "Middleware: Migrated 'cart' to 'bag': %s",
                request.session['bag']
            )

        response = self.get_response(request)
        return response
