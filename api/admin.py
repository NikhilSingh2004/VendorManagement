from django.contrib import admin
from api.models import Vendor, PurchaseOrder, PurchaseOrder

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name', 'address']

# @admin.register(PurchaseOrder)
# class PurchaseOrderAdmin(admin.ModelAdmin):
#     list_display = ['po_number']

@admin.register(PurchaseOrder)
class PerformanceRecordAdmin(admin.ModelAdmin):
    list_display = ['vendor']