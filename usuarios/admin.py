from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nome', 'telefone', 'cpf')
    search_fields = ('username', 'email', 'nome')  

admin.site.register(User, UserAdmin)

# Register your models here.
