from django.urls import path
from authenticate import views
urlpatterns = [
    # path('', views.authenticate),
    path('signin/', views.sign_in),
    path('signup/', views.sign_up.as_view()),
    path('signout/', views.LogoutView.as_view()),
    path('forgotPassword/', views.forgot_password.as_view()),
    path('resetPassword/', views.reset_password.as_view()),
    path('verifyOTP/', views.verify_OTP.as_view()),
    path('profile/', views.UserProfileAPIView.as_view()),
]
