from django.urls import path
from .views import AttendanceList, AttendanceDetail, AttendanceUpdate


urlpatterns = [
    path('', AttendanceList.as_view()),
    path('<int:pk>/', AttendanceDetail.as_view()),
    path('update/<int:id>/', AttendanceUpdate.as_view()),
]
