from django.urls import path
from . import views 

urlpatterns=[
    path("",views.home,name="home"),
    path("new/",views.new,name="new"),
    path('linkmoovit/', views.mylinkview, name='linkmoovit'),
    # path("eliminar/<int:tarea_id>/",views.eliminar,name="eliminar"),
    # path("editar/<int:tarea_id>/",views.editar,name="editar"),


]