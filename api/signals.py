from django.db.models import F
from django.db.models import Avg
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from .models import Vendor, PurchaseOrder, PerformanceRecord

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

                # Calculate On Time Delivery Rate, But using the Delivered on Date
                on_time_deliveries = completed_orders.filter(delivered_on__lte=F('delivery_date')).count()
                vendor.on_time_delivery_rate = (on_time_deliveries / completed_orders.count())*100

                # Calculate Quality Ratinng Average : Add all the Quality Rating of the Completed Orders and Divide it with the PO's
                vendor.quality_rating_avg = completed_orders.exclude(quality_rating__isnull=True).aggregate(Avg('quality_rating'))['quality_rating__avg']

                # Calculate the fulfilment rate using the any_issue filed
                successfully_fulfilled = PurchaseOrder.objects.filter(vendor=vendor, status='Completed', any_issue=False).count()

                print(successfully_fulfilled)
                vendor.fulfillment_rate = (successfully_fulfilled / total_completed_orders)*100
                print(vendor.fulfillment_rate)

                # Calculate Average Response Time 
                total_response_time = timedelta()
                print('1')
                for order in completed_orders:
                    if order.acknowledgment_date:
                        response_time = order.acknowledgment_date - order.issue_date
                        total_response_time += response_time

                print(total_response_time)
                if total_completed_orders > 0:
                    average_response_time = total_response_time / total_completed_orders
                else:
                    average_response_time = timedelta() 

                vendor.average_response_time = (average_response_time)
                print(vendor.average_response_time)

                vendor.save()

                print('10')

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

