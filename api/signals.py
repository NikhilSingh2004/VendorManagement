from django.db import models
from django.db.models import Avg
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Vendor, PurchaseOrder, PerformanceRecord
from datetime import datetime, timedelta

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    try:
        print("Executing")
        if instance.status == 'Completed' and instance.vendor:
            vendor = instance.vendor
            completed_orders = vendor.purchase_orders.filter(status='Completed')
            total_completed_orders = completed_orders.count()
            if total_completed_orders > 0:
                total_response_time = timedelta()

                vendor.on_time_delivery_rate = completed_orders.filter(delivery_date__lte=models.F('delivery_date')).count() / total_completed_orders
                vendor.quality_rating_avg = completed_orders.exclude(quality_rating__isnull=True).aggregate(Avg('quality_rating'))['quality_rating__avg']
                vendor.fulfillment_rate = completed_orders.filter(status='completed').exclude(quality_rating__lt=5).count() / total_completed_orders
                for order in completed_orders:
                    if order.acknowledgment_date:
                        response_time = order.acknowledgment_date - order.issue_date
                        total_response_time += response_time
                average_response_time = total_response_time.total_seconds() / total_completed_orders / 60
                vendor.average_response_time = average_response_time

                vendor.save()

                performance_record = PerformanceRecord.objects.create(
                    vendor=vendor,
                    date= datetime.now(),
                    on_time_delivery_rate=vendor.on_time_delivery_rate,
                    quality_rating_avg=vendor.quality_rating_avg,
                    average_response_time=vendor.average_response_time,
                    fulfillment_rate=vendor.fulfillment_rate
                )
                performance_record.save()
            else:
                vendor.on_time_delivery_rate = None
                vendor.quality_rating_avg = None
                vendor.average_response_time = None
                vendor.fulfillment_rate = None
            vendor.save()

        print('Done')
    except Exception as e:
        return False

