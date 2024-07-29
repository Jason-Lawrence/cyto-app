"""Register models to the backend."""
from django.contrib import admin
from .models import NetworkMap, Node, Edge


admin.site.register(NetworkMap)
admin.site.register(Node)
admin.site.register(Edge)
