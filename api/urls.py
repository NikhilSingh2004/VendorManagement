from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    # Vendor and Purchase Order End Points
    path('vendor/', views.VendorAPI.as_view()),
    path('vendor/<int:id>/', views.VendorAPI.as_view()),
    path('purchase_orders/', views.PurchaseOrderAPI.as_view()),
    path('purchase_orders/<int:id>/', views.PurchaseOrderAPI.as_view()),

    # End Point for the Vendors to Acknowledge there Orders
    path('purchase_orders/<int:id>/acknowledgment/', views.PurchaseOrderAcknowledgment.as_view()),

    # End Point for Vendor Performance Data 
    path('vendors/<int:id>/performance/', views.VendorPerformance.as_view()),
    
    # Token Access, Refresh & Validation End Points
    path('token/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('verify/', TokenVerifyView.as_view())
]
