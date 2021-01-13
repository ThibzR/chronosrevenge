from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'groups', views.GroupView)
router.register(r'blacklist_courses', views.CourseView)

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', include(router.urls)),
]