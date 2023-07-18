from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('checkAccess/',views.CheckAccessView.as_view()),
    path('checkCar/',views.CheckCar.as_view()),
    path('brands/', views.AllBrands.as_view()),
    path('logout/', views.LogoutView.as_view())
]
