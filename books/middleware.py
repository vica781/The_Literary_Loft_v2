class SessionDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to run before the view
        if not request.session.session_key:
            request.session.create()
            print(f"Middleware: Created new session with ID: {request.session.session_key}")
        
        # Check if bag exists and handle old 'cart' key if needed
        if 'cart' in request.session and not 'bag' in request.session:
            request.session['bag'] = request.session['cart'].copy()
            request.session.modified = True
            print(f"Middleware: Copied cart to bag: {request.session['bag']}")
        
        response = self.get_response(request)
        
        # Code to run after the view
        return response    
    