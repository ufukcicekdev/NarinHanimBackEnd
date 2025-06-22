from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet)
router.register(r'visits', views.VisitViewSet)
router.register(r'herbaltreatments', views.HerbalTreatmentViewSet)
router.register(r'medicines', views.MedicineViewSet)
router.register(r'irisimages', views.IrisImageViewSet)
router.register(r'visit-stages', views.VisitStageViewSet)
router.register(r'stage-eye-images', views.StageEyeImageViewSet)
router.register(r'stage-medicines', views.StageMedicineViewSet)
router.register(r'production-orders', views.ProductionOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logistic-stats/', views.logistic_dashboard_stats, name='logistic-stats'),
] 