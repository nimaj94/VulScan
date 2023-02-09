from django.urls import path

from scanner.views import Scan, Result

app_name = 'scanner'

urlpatterns = [
    path('scan', Scan.as_view({'get': 'list', 'post': 'create'}), name='scan_general_actions'),
    path('result/<str:id>', Result.as_view(), name='scan_result'),
]
