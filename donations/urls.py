from django.urls import path
from .views import InitializePaymentView, VerifyPaymentView

urlpatterns = [
    path("pay/init/", InitializePaymentView.as_view(), name="pay-init"),
    path("pay/verify/<str:reference>/", VerifyPaymentView.as_view(), name="pay-verify"),
]
