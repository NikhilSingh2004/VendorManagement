from django.test import TestCase
from .models import Vendor, PurchaseOrder, PerformanceRecord
from django.utils import timezone

class VendorModelTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(username='test_vendor', email='test@example.com')

    def test_vendor_str_method(self):
        self.assertEqual(str(self.vendor), 'test_vendor')

class PurchaseOrderModelTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(username='test_vendor', email='test@example.com')
        self.purchase_order = PurchaseOrder.objects.create(po_number='PO123', vendor=self.vendor,
                                                           order_date=timezone.now(), delivery_date=timezone.now(),
                                                           items=[], quantity=1, status='Pending',
                                                           issue_date=timezone.now())

    def test_purchase_order_str_method(self):
        self.assertEqual(str(self.purchase_order), 'PO123')

class PerformanceRecordModelTestCase(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(username='test_vendor', email='test@example.com')
        self.performance_record = PerformanceRecord.objects.create(vendor=self.vendor, date=timezone.now(),
                                                                   on_time_delivery_rate=0.9, quality_rating_avg=4.5,
                                                                   fulfillment_rate=0.8)

    def test_performance_record_str_method(self):
        self.assertEqual(str(self.performance_record),
                         f"Performance Record for {self.vendor.name} on {self.performance_record.date}")

