import io
import jwt
import uuid
import json
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Vendor, PurchaseOrder, PerformanceRecord
from django.http import HttpRequest, HttpResponse, JsonResponse 
from .serializers import VendorSerializer, PurchaseOrderSerializer, PerformanceRecordSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from rest_framework_simplejwt.exceptions import InvalidToken

def no_end_point(request : HttpRequest) -> HttpResponse :
    try:
        response = {
            "error" : "This API End Point Does not Exist"
        }
        return JsonResponse(response, safe=True)
    except Exception as e:
        return HttpResponse("Something Went Wrong!")


def get_user_id(request):
    try:
        token = request.headers.get('Authorization', '').split(' ')[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            
            return {'user_id': user_id}
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}
    except Exception as e:
        return {'error': 'Token Not Provided'}
    

def get_vendor(v_id):
    try:
        return Vendor.objects.get(id=v_id, deleted=False)
    except Vendor.DoesNotExist:
        return False
        

def get_id(request):
        try:
            return int(request.data.get('id'))
        except Exception as e:
            return False
        

class VendorAPI(APIView):
    """
        GET - List all the Vendors
        POST - Creata a new Vendor
    """

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        return [IsAuthenticated()]

    def get(self, request, id=None,*args, **kwargs):
        try:
            print(id)
            if id is not None:
                vendor = get_vendor(id)
                if vendor:
                    serializer = VendorSerializer(vendor)
                    return Response(serializer.data, status=status.HTTP_200_OK)    
                return Response({"error" : "Vendor Not Found"}, status=status.HTTP_404_NOT_FOUND)    
            vendors = Vendor.objects.filter(deleted=False)
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, *args, **kwargs):
        try:
            raw_data = request.body
            print('1')
            stream = io.BytesIO(raw_data)
            print('2')
            json_data = JSONParser().parse(stream)
            print('3')
            json_data['vendor_code'] = str(uuid.uuid4())
            print('4')
            serializer = VendorSerializer(data=json_data)
            if serializer.is_valid():
                print('5')
                serializer.save()
                message = f"Vendor Created, {serializer.data['vendor_code']}"
                return Response({"message": message}, status=status.HTTP_200_OK)
            return Response({"error": "Input Data not Valid", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e.__str__())
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, *args, **kwargs):
        try:
            vendor_id = self.kwargs.get('id')
            if vendor_id is not None:
                vendor = get_vendor(vendor_id)
                if vendor:
                    serializer = VendorSerializer(vendor, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    serializer_errors = json.loads(JSONRenderer().render(serializer.errors))
                    return Response(serializer_errors, status=status.HTTP_400_BAD_REQUEST)
                return JsonResponse({"error": "Vendor Not Found"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Please Provide the Vendor ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, *args, **kwargs):
        try:
            vendor_id = self.kwargs.get('id')
            if vendor_id is not None:
                try:
                    vendor = Vendor.objects.get(id=vendor_id, deleted=False)
                    vendor.deleted = True
                    vendor.save()
                    message = f"Vendor Deleted, {vendor.name}"
                    return Response({"message" : message}, status=status.HTTP_200_OK)
                except Vendor.DoesNotExist:
                    return Response({"error": "Vendor Not Found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error": "Please Provide the Vendor ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class PurchaseOrderAcknowledgment(APIView):
    """
        This class Contains the Acknowledgment End Point through which the Vendor Will be able to Acknowledge its intended Purchase Orders
        POST - To Acknowledge the intended Purchase Order
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = get_user_id(request)
        po_id = self.kwargs.get('id')

        if data.get('user_id') is not None:
            user_id = data.get('user_id')
            try:
                vendor = Vendor.objects.get(id=user_id, deleted = False)
                purchasr_order = PurchaseOrder.objects.get(id=po_id, deleted = False)
            except Vendor.DoesNotExist:
                return Response({"error": "Vendor Not Found"}, status=status.HTTP_404_NOT_FOUND)
            except PurchaseOrder.DoesNotExist:
                return Response({"error": "Purchase Order Not Found"}, status=status.HTTP_404_NOT_FOUND)
            
            if not (purchasr_order.acknowledgment_date) and purchasr_order.vendor == vendor:
                purchasr_order.acknowledgment_date = datetime.now()
                purchasr_order.save()
                return JsonResponse({"message" : "Purchase Order Acknowledged"}, status=status.HTTP_200_OK)
            
            return Response({"error": "Purchase Order Already Acknowledged"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({"error" : "Currepted Token"}, status=status.HTTP_400_BAD_REQUEST)


class VendorPerformance(APIView):
    """
        GET - Retrieve Vendor Performance Data
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            vendor_id = get_user_id(request)
            vendor = get_vendor(vendor_id['user_id'])
            if vendor:
                print("Inside Serialization")
                serializer = VendorSerializer(vendor)

                # Convert microseconds to timedelta
                average_response_time_microseconds = serializer.data.get('average_response_time')
                if average_response_time_microseconds is not None:
                    average_response_time = timedelta(microseconds=average_response_time_microseconds)
                else:
                    average_response_time = None

                print(vendor.average_response_time)

                # Construct response data
                data = {
                    "Vendor Name": serializer.data['name'],
                    "On Time Delivery Rate": serializer.data['on_time_delivery_rate'],
                    "Quality Rating Average": serializer.data['quality_rating_avg'],
                    "Average Response Time": vendor.average_response_time,
                    "Fulfillment Rate": serializer.data['fulfillment_rate']
                }

                return Response(data, status=status.HTTP_200_OK)
            return Response({"error": "Vendor Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except InvalidToken:
            return Response({"error": "Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PurchaseOrderAPI(APIView):
    """
        GET - List all the Purchase Order 
        POST - Creata a new Purchase Order 
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            po_id = self.kwargs.get('id')
            if po_id is not None:
                try:
                    purchase_order = PurchaseOrder.objects.get(id=po_id, deleted=False)
                    serializer = PurchaseOrderSerializer(purchase_order)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except PurchaseOrder.DoesNotExist:
                    return Response({"message": "Purchase Order Not Found"}, status=status.HTTP_404_NOT_FOUND)
            purchase_orders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            raw_data = request.body
            stream = io.BytesIO(raw_data)
            json_data = JSONParser().parse(stream)
            json_data['po_number'] = str(uuid.uuid4())
            serializer = PurchaseOrderSerializer(data=json_data)
            if serializer.is_valid():
                serializer.save()
                message = f"Purchase Order Created : {json_data['po_number']}"
                return Response({"message": message}, status=status.HTTP_200_OK)
            return Response({"error": "Input Data not Valid", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            po_id = self.kwargs.get('id')
            if po_id is not None:
                try:
                    purchase_order = PurchaseOrder.objects.get(id = po_id)
                    serializer = PurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
                    if purchase_order.acknowledgment_date or purchase_order.status == "Completed":
                        if serializer.is_valid():
                            serializer.save()
                            return Response(serializer.data)
                        return Response({"error": "Input Data Not valid"}, status=status.HTTP_400_BAD_REQUEST)
                    return Response({"error": "Purchase Order Not Acknowledgment"}, status=status.HTTP_400_BAD_REQUEST)
                except PurchaseOrder.DoesNotExist :
                    return Response({"error": "Purchase Order Not Found"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Please Provide the Purchase Order ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            po_id = self.kwargs.get('id')
            if po_id is not None:
                try:
                    purchase_order = PurchaseOrder.objects.get(id=po_id, deleted=False)
                    purchase_order.deleted = True
                    purchase_order.save()
                    message = f"Purchase Order Deleted Successfuly {purchase_order.po_number}"
                    return Response({"message" : message}, status=status.HTTP_200_OK)
                except PurchaseOrder.DoesNotExist:
                    return Response({"error": "Purchase Order Not Found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "Please Provide the Purchase Order ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Something Went Wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        