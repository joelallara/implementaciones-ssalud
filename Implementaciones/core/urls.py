from django.urls import path
from .views import home
# from .views import HomePageView

urlpatterns = [
    # path('', HomePageView.as_view(), name="home"),
    path('', home, name="home"),
]