from django.contrib import admin
from fixit_frw.models import User, Items, Payments, Address

admin.site.register(User)
admin.site.register(Items)
# admin.site.register(Payments)
admin.site.register(Address)

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Payments._meta.fields]

    #  Admin doenst update user payments
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False