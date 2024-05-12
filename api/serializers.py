from rest_framework import serializers
from .models import Vendor, PurchaseOrder, PerformanceRecord


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'phone_number', 'email', 'address', 'vendor_code', 
                  'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 
                  'fulfillment_rate', 'username', 'password']

    def create(self, validated_data):
        """
            Create and return a new `Vendor` instance, given the validated data.
        """
        print('1.1')
        return Vendor.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
            Update and return an existing `Vendor` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.vendor_code = validated_data.get('vendor_code', instance.vendor_code)
        instance.on_time_delivery_rate = validated_data.get('on_time_delivery_rate', instance.on_time_delivery_rate)
        instance.quality_rating_avg = validated_data.get('quality_rating_avg', instance.quality_rating_avg)
        instance.average_response_time = validated_data.get('average_response_time', instance.average_response_time)
        instance.fulfillment_rate = validated_data.get('fulfillment_rate', instance.fulfillment_rate)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.save()

        return instance
    
    # Implementing Field Level Validation Rather than Object Level
    
    def validate_name(self, value):
        if len(value) >= 100:
            raise serializers.ValidationError("Name is too Long")
        return str(value).capitalize()

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date', 'delivery_date', 
                  'items', 'quantity', 'status', 'quality_rating', 'issue_date', 
                  'acknowledgment_date', 'delivered_on', 'any_issue']

    def create(self, validated_data):
        """
            Create and return a new `Purchase Order` instance, given the validated data.
        """
        return PurchaseOrder.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
            Update and return an existing `Purchase Order` instance, given the validated data.
        """
        instance.po_number = validated_data.get('po_number', instance.po_number)
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        instance.items = validated_data.get('items', instance.items)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.quality_rating = validated_data.get('quality_rating', instance.quality_rating)
        instance.issue_date = validated_data.get('issue_date', instance.issue_date)
        instance.acknowledgment_date = validated_data.get('acknowledgment_date', instance.acknowledgment_date)
        instance.delivered_on = validated_data.get('delivered_on', instance.delivered_on)
        
        instance.any_issue = validated_data.get('any_issue', instance.any_issue)

        instance.save()

        return instance
    

class PerformanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceRecord
        fields = ['vendor', 'date', 'on_time_delivery_rate', 
                  'quality_rating_avg', 'average_response_time', 
                  'fulfillment_rate']

    def create(self, validated_data):
        """
            Create and return a new `Performance Record` instance, given the validated data.
        """
        return PerformanceRecord.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
            Update and return an existing `PerformanceRecord` instance, given the validated data.
        """
        instance.vendor = validated_data.get('vendor', instance.vendor)
        instance.date = validated_data.get('date', instance.date)
        instance.on_time_delivery_rate = validated_data.get('on_time_delivery_rate', instance.on_time_delivery_rate)
        instance.quality_rating_avg = validated_data.get('quality_rating_avg', instance.quality_rating_avg)
        instance.average_response_time = validated_data.get('average_response_time', instance.average_response_time)
        instance.fulfillment_rate = validated_data.get('fulfillment_rate', instance.fulfillment_rate)

        instance.save()
        return instance

