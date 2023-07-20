from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.RegisterUserView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('checkAccess/',views.CheckAccessView.as_view()),
    path('checkCar/',views.CheckCar.as_view()),
    path('createOrder/',views.CreateOrder.as_view()),
    path('brands/', views.AllBrands.as_view()),
    path('logout/', views.LogoutView.as_view())
]
