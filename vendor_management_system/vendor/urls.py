from django.urls import path
from vendor.views import *

urlpatterns = [
    path('api/vendors/', VendorList.as_view(), name='vendor-list'),
    # path('api/vendors/<int:pk>/', VendorDetail.as_view(), name='vendor-detail'),
    # path('api/purchase_orders/', PurchaseOrderList.as_view(), name='purchase-order-list'),
    # path('api/purchase_orders/<int:pk>/', PurchaseOrderDetail.as_view(), name='purchase-order-detail'),
]
