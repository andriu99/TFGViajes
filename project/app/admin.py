from django.contrib import admin
from .models import Request,RESTApi,Node

admin.site.register(Request)
admin.site.register(RESTApi)
admin.site.register(Node)