from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
urlpatterns = [
    path('busquedaVectorial/', views.BusquedaVectorialAPIView.as_view(), name='busqueda-vectorial'),
    path('busquedaVectorialSBS/', views.BusquedaVectorialSBSAPIView.as_view(), name='busqueda-vectorial'),
]
router.register(r'buscados',views.ProductoAhorroViewSet)
router.register(r'buscadoSBS',views.ProductoAhorroViewSetSBS)
urlpatterns += router.urls  


