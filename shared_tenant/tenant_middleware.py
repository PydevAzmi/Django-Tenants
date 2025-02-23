from django.http import Http404
from shared_tenant.models import Tenant
import threading
_thread_locals = threading.local()
    

# Helper function for the router to access the database name
def get_current_db_name():
    return getattr(_thread_locals, 'db', 'default')
class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        subdomains = host.split('.')
        subdomain = subdomains[0]
        if subdomain == 'www' and len(subdomains) > 1:
            subdomain = subdomains[1]
        try:
            tenant = Tenant.objects.get(subdomain=subdomain)
            _thread_locals.db = tenant.database_name
            request.tenant = tenant
        except Tenant.DoesNotExist:
            raise Http404("Tenant not found")
        except Exception as e:
            raise Http404(f"Database connection error: {e}")
        
        
        # Cleanup thread-local after processing the request
        if hasattr(_thread_locals, 'tenant'):
            del _thread_locals.db
            
        response = self.get_response(request)
        return response