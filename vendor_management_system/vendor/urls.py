from django.urls import path
from vendor.views import *

urlpatterns = [
    path('api/vendors/', VendorViews.as_view(), name='vendor-list'),
    path('api/vendors/<int:vendor_id>/', VendorManagement.as_view(), name='vendor-detail'),
    path('api/purchase_orders/', PurchaseOrders.as_view(), name='purchase-orders'),
    path('api/purchase_orders/<int:po_id>/', PurchaseOrderTracking.as_view(), name='purchase-order-tracking'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', UpdateAcknowlegement.as_view(), name='purchase-order-tracking'),
    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance-metrics'),
]
