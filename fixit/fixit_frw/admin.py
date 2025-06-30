from django.contrib import admin
from fixit_frw.models import User, Items, Payments, Address

admin.site.register(User)
admin.site.register(Items)
admin.site.register(Payments)
admin.site.register(Address)