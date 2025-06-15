from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'visits', views.VisitViewSet)
router.register(r'herbaltreatments', views.HerbalTreatmentViewSet)
router.register(r'medicines', views.MedicineViewSet)
router.register(r'irisimages', views.IrisImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 