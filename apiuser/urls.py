from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from . import views
from rest_framework_simplejwt.views import (TokenRefreshView)


urlpatterns = [
      path('', views.home, name='index'), 
      path('twono/', views.addtwono, name='addtwono'),  

      # path('test/', views.run, name='test'),
      # path('test2/', views.daterecords, name='daterecords'),
      path('restaurant/', views.Restaurnat.as_view(), name='Restaurnat'),
      #path('otpquery/', views.usersotpview.as_view(), name='verify'),
      path('verify-email/', views.VerifyUserEmail.as_view(), name='verify'),
      path('register/', views.RegisterView.as_view()),
      path('login/', views.LoginUserView.as_view(), name='login-user'),
      path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset'),
      path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='reset-password-confirm'),
      path('set-new-password/', views.SetNewPasswordView.as_view(), name='set-new-password'),
      path('logout/', views.LogoutView.as_view(), name='logout'),
     # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
      path('birth',views.refmodule, name='demo')
     
      

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)