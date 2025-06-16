from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Patient, Visit, HerbalTreatment, Medicine, IrisImage, VisitStage, StageEyeImage, StageMedicine
from .serializers import (
    PatientSerializer, VisitSerializer, HerbalTreatmentSerializer,
    MedicineSerializer, IrisImageSerializer, VisitStageSerializer,
    StageEyeImageSerializer, StageMedicineSerializer
)

# Create your views here.

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
