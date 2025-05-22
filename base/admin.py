from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Contact)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('email',)

admin.site.register(Category)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Service)

admin.site.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ('sum', 'plan')

admin.site.register(Plan)
