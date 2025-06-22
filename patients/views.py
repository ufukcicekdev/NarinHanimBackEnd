from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Patient, Visit, HerbalTreatment, Medicine, IrisImage, VisitStage, StageEyeImage, StageMedicine, UserProfile, ProductionOrder
from .serializers import (
    PatientSerializer, VisitSerializer, HerbalTreatmentSerializer,
    MedicineSerializer, IrisImageSerializer, VisitStageSerializer,
    StageEyeImageSerializer, StageMedicineSerializer, ProductionOrderSerializer
)
from .pdf_generator import generate_production_order_pdf_response

# Create your views here.

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Kullanıcı tipini response'a ekle
        profile, created = UserProfile.objects.get_or_create(user=self.user)
        data['user_type'] = profile.user_type
        data['user_id'] = self.user.id
        data['username'] = self.user.username
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def logistic_dashboard_stats(request):
    """Lojistik dashboard için istatistik verileri"""
    try:
        # Tarih hesaplamaları
        today = timezone.now().date()
        this_month_start = today.replace(day=1)
        this_week_start = today - timedelta(days=today.weekday())
        
        # Temel istatistikler
        total_patients = Patient.objects.count()
        total_visits = Visit.objects.count()
        this_month_visits = Visit.objects.filter(visit_date__date__gte=this_month_start).count()
        today_visits = Visit.objects.filter(visit_date__date=today).count()
        
        # Son 30 günde eklenen hasta sayısı
        last_30_days = today - timedelta(days=30)
        new_patients_last_month = Patient.objects.filter(created_at__date__gte=last_30_days).count()
        
        # Üretim emirleri istatistikleri
        total_orders = ProductionOrder.objects.count()
        pending_orders = ProductionOrder.objects.exclude(status='completed').count()
        completed_orders = ProductionOrder.objects.filter(status='completed').count()
        today_orders = ProductionOrder.objects.filter(created_at__date=today).count()
        
        # Son aktiviteler (son 10 işlem)
        recent_patients = Patient.objects.order_by('-created_at')[:3]
        recent_visits = Visit.objects.order_by('-created_at')[:3]
        recent_orders = ProductionOrder.objects.order_by('-created_at')[:4]
        
        recent_activities = []
        
        # Son hastaları ekle
        for patient in recent_patients:
            recent_activities.append({
                'activity': f'Yeni hasta kaydı: {patient.first_name} {patient.last_name}',
                'time': patient.created_at,
                'type': 'success'
            })
        
        # Son ziyaretleri ekle
        for visit in recent_visits:
            recent_activities.append({
                'activity': f'Yeni ziyaret: {visit.patient.first_name} {visit.patient.last_name}',
                'time': visit.created_at,
                'type': 'info'
            })
        
        # Son üretim emirlerini ekle
        for order in recent_orders:
            recent_activities.append({
                'activity': f'{order.get_status_display()}: {order.medicine.name} - {order.patient_name}',
                'time': order.created_at,
                'type': 'warning'
            })
        
        # Zamana göre sırala ve son 8 tanesini al
        recent_activities.sort(key=lambda x: x['time'], reverse=True)
        recent_activities = recent_activities[:8]
        
        # Zamanları relative format'a çevir
        for activity in recent_activities:
            time_diff = timezone.now() - activity['time']
            if time_diff.days > 0:
                activity['time'] = f"{time_diff.days} gün önce"
            elif time_diff.seconds > 3600:
                activity['time'] = f"{time_diff.seconds // 3600} saat önce"
            elif time_diff.seconds > 60:
                activity['time'] = f"{time_diff.seconds // 60} dakika önce"
            else:
                activity['time'] = "Az önce"
        
        # Aylık ziyaret yüzdesi (geçen aya göre)
        last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
        last_month_visits = Visit.objects.filter(
            visit_date__date__gte=last_month_start,
            visit_date__date__lt=this_month_start
        ).count()
        
        visit_percentage = 0
        if last_month_visits > 0:
            visit_percentage = round(((this_month_visits - last_month_visits) / last_month_visits) * 100, 1)
        
        data = {
            'stats': {
                'total_patients': total_patients,
                'total_visits': total_visits,
                'this_month_visits': this_month_visits,
                'today_visits': today_visits,
                'new_patients_last_month': new_patients_last_month,
                'visit_percentage': visit_percentage,
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'completed_orders': completed_orders,
                'today_orders': today_orders
            },
            'recent_activities': recent_activities,
            'production_orders': ProductionOrderSerializer(
                ProductionOrder.objects.exclude(status='completed').order_by('-created_at')[:10], 
                many=True
            ).data,
            'system_status': {
                'server': 'active',
                'database': 'active',
                'api': 'active',
                'last_backup': '2 saat önce'
            }
        }
        
        return Response(data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def visits(self, request, pk=None):
        patient = self.get_object()
        visits = Visit.objects.filter(patient=patient)
        serializer = VisitSerializer(visits, many=True)
        return Response(serializer.data)

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id:
            return Visit.objects.filter(patient_id=patient_id)
        return Visit.objects.all()

    @action(detail=True, methods=['post'])
    def add_treatment(self, request, pk=None):
        visit = self.get_object()
        serializer = HerbalTreatmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(visit=visit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_medicine(self, request, pk=None):
        visit = self.get_object()
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(visit=visit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_iris_image(self, request, pk=None):
        visit = self.get_object()
        serializer = IrisImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(visit=visit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        visit = self.get_object()
        images = IrisImage.objects.filter(visit=visit)
        serializer = IrisImageSerializer(images, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def treatments(self, request, pk=None):
        visit = self.get_object()
        treatments = HerbalTreatment.objects.filter(visit=visit)
        serializer = HerbalTreatmentSerializer(treatments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def medicines(self, request, pk=None):
        visit = self.get_object()
        medicines = Medicine.objects.filter(visit=visit)
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data)

class HerbalTreatmentViewSet(viewsets.ModelViewSet):
    queryset = HerbalTreatment.objects.all()
    serializer_class = HerbalTreatmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]

class IrisImageViewSet(viewsets.ModelViewSet):
    queryset = IrisImage.objects.all()
    serializer_class = IrisImageSerializer
    permission_classes = [permissions.IsAuthenticated]

class VisitStageViewSet(viewsets.ModelViewSet):
    queryset = VisitStage.objects.all()
    serializer_class = VisitStageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        visit_id = self.request.query_params.get('visit_id', None)
        if visit_id:
            return VisitStage.objects.filter(visit_id=visit_id)
        return VisitStage.objects.all()

    @action(detail=True, methods=['post'])
    def add_eye_image(self, request, pk=None):
        stage = self.get_object()
        serializer = StageEyeImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(stage=stage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_medicine(self, request, pk=None):
        stage = self.get_object()
        serializer = StageMedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(stage=stage)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StageEyeImageViewSet(viewsets.ModelViewSet):
    queryset = StageEyeImage.objects.all()
    serializer_class = StageEyeImageSerializer
    permission_classes = [permissions.IsAuthenticated]

class StageMedicineViewSet(viewsets.ModelViewSet):
    queryset = StageMedicine.objects.all()
    serializer_class = StageMedicineSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def create_production_order(self, request, pk=None):
        """İlaç için üretim emri oluştur"""
        medicine = self.get_object()
        order_type = request.data.get('status')
        
        # Eski status'ları yeni status'lara map et
        status_mapping = {
            'package_prepare': 'package_requested',
            'send_production': 'production_requested', 
            'prepare_cargo': 'cargo_requested'
        }
        
        if not order_type or order_type not in status_mapping:
            return Response({'error': 'Geçerli bir durum seçin'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Hasta adını al
        patient_name = f"{medicine.stage.visit.patient.first_name} {medicine.stage.visit.patient.last_name}"
        
        # Production order oluştur
        production_order = ProductionOrder.objects.create(
            medicine=medicine,
            status=status_mapping[order_type],
            patient_name=patient_name,
            created_by=request.user
        )
        
        serializer = ProductionOrderSerializer(production_order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductionOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductionOrder.objects.all()
    serializer_class = ProductionOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        filter_status = self.request.query_params.get('status', None)
        if filter_status:
            return ProductionOrder.objects.filter(status=filter_status)
        return ProductionOrder.objects.all()
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Üretim emri durumunu güncelle"""
        order = self.get_object()
        new_status = request.data.get('status')
        
        valid_statuses = [
            'package_requested', 'package_preparing', 'package_ready',
            'production_requested', 'production_preparing', 'production_sent', 'production_completed',
            'cargo_requested', 'cargo_preparing', 'cargo_ready', 'cargo_shipped',
            'completed'
        ]
        
        if new_status not in valid_statuses:
            return Response({'error': 'Geçerli bir durum seçin'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        if new_status == 'completed':
            from django.utils import timezone
            order.completed_at = timezone.now()
        order.save()
        
        serializer = ProductionOrderSerializer(order)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Üretim emri PDF'ini indir"""
        order = self.get_object()
        return generate_production_order_pdf_response(order)
