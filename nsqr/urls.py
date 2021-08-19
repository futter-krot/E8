from django.urls import path
from . import views

app_name = "nsqr"

urlpatterns = [
    path("", views.ResultView.as_view(), name="result-view"),
    path("add", views.TaskCreate.as_view(), name="task-create"),
    path("contact", views.contact, name="contact")
]
