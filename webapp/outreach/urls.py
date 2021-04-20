from django.urls import path
from .views import firms_table_view, attorneys_view

urlpatterns = [
    path("", firms_table_view),
    path("firm/<str:firm_name>/attorneys", attorneys_view),
]
