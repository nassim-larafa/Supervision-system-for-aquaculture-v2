from django.contrib import admin
from users.models import *
from django.contrib.gis import admin
from .models import node, myProject, parcelle, Data


# Register your models here.


class clientAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','NB_GSM','pseudo','e_mail')

class supervisorAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','NB_GSM','pseudo','e_mail')


class PolygonAdmin(admin.GISModelAdmin):
    list_display = ('geom',)

class myProjectAdmin(admin.ModelAdmin):
    list_display = ['polygon_id', 'nomp', 'descp', 'debutp', 'finp', 'cityp', 'clientp']
    

admin.site.register(client,clientAdmin)
admin.site.register(supervisor,supervisorAdmin)
admin.site.register(Data)
admin.site.register(parcelle)
admin.site.register(node)
admin.site.register(myProject)
