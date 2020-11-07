from django.urls import path
from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('sign_in/', views.SignInView.as_view(), name='sign_in'),
    path('sign_out/', views.SignOutView.as_view(), name='sign_out'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('preferences/<int:pk>/', views.UserPreferenceView.as_view(), name='preferences'),
]