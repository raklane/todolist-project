from django.contrib import admin
from .models import TodoList

# Register your models here.

class TotoListAdmin(admin.ModelAdmin):
    readonly_fields = ('timeCreated',)

admin.site.register(TodoList, TotoListAdmin)
