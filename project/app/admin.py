from django.contrib import admin
from .models import Request,RESTApi,Node,Trip,skyscannerTrip,blablaTrip,busOrTrainTrip

admin.site.register(Request)
admin.site.register(RESTApi)
admin.site.register(Node)
admin.site.register(Trip)
admin.site.register(skyscannerTrip)
admin.site.register(blablaTrip)
admin.site.register(busOrTrainTrip)

