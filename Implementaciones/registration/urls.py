from django.urls import path
from .views import SignUpView, ProfileUpdate, EmailUpdate, LoginStaffView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
    path('profile/email/', EmailUpdate.as_view(), name='profile_email'),
    path('staff_required/', LoginStaffView.as_view(), name='login_staff'),
]