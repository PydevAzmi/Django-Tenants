from django.http import Http404
from django.db import connections
from shared_tenant.models import Tenant

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
        except Tenant.DoesNotExist:
            raise Http404("Tenant not found")
        except Exception as e:
            raise Http404(f"Database connection error: {e}")
    
        # Configure the tenant database
        connection = connections[f"{subdomain}_db"]
        connection.settings_dict['NAME'] = tenant.database_name
        request.tenant = tenant 

        response = self.get_response(request)
        return response
    