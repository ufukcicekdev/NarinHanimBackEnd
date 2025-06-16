from rest_framework import serializers
from .models import Patient, Visit, HerbalTreatment, Medicine, IrisImage, VisitStage, StageEyeImage, StageMedicine

class StageEyeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageEyeImage
        fields = ['id', 'stage', 'image', 'description', 'created_at']

class StageMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageMedicine
        fields = ['id', 'stage', 'name', 'dosage', 'frequency', 'duration', 'notes', 'created_at']

class VisitStageSerializer(serializers.ModelSerializer):
    eye_images = StageEyeImageSerializer(many=True, read_only=True)
    medicines = StageMedicineSerializer(many=True, read_only=True)

    class Meta:
        model = VisitStage
        fields = ['id', 'visit', 'stage_number', 'date', 'complaint', 'notes', 'eye_images', 'medicines', 'created_at', 'updated_at']

class IrisImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IrisImage
        fields = ['id', 'image', 'description', 'created_at']

class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'dosage', 'duration', 'notes', 'created_at']

class HerbalTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = HerbalTreatment
        fields = ['id', 'name', 'dosage', 'duration', 'notes', 'created_at']

class VisitSerializer(serializers.ModelSerializer):
    herbal_treatments = HerbalTreatmentSerializer(many=True, read_only=True)
    medicines = MedicineSerializer(many=True, read_only=True)
    iris_images = IrisImageSerializer(many=True, read_only=True)
    stages = VisitStageSerializer(many=True, read_only=True)

    class Meta:
        model = Visit
        fields = ['id', 'patient', 'visit_date', 'diagnosis', 'notes', 'document', 'herbal_treatments', 
                 'medicines', 'iris_images', 'stages', 'created_at', 'updated_at']

class PatientSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'patient_code', 'first_name', 'last_name', 'birth_date', 'gender',
                 'phone', 'email', 'tc_no', 'city', 'district', 'address', 'blood_type', 
                 'allergies', 'notes', 'visits', 'created_at', 'updated_at'] 