from django.urls import path
from . import views
urlpatterns = [
    # path('', views.api),
    path('send-alert-email/',views.SendAlertEmailAPIView.as_view()),
    path('send-marketing-email/',views.SendMarketingEmailAPIView.as_view()),
    path('send-subscription-email/',views.SendSubscriptionEmailAPIView.as_view()),
    path('send-invoice-email/',views.SendInvoiceEmailAPIView.as_view()),
    path('send-waitlist-email/',views.SendWaitlistEmailAPIView.as_view()),
     path('project/<int:id>/',views.ProjectAPIView.as_view()),
    path('project/',views.ProjectAPIView.as_view()),
    path('testing/<int:id>/',views.TestingAPIView.as_view()),
    path('testing/',views.TestingAPIView.as_view())
]
