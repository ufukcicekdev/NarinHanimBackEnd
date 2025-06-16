from rest_framework import serializers
from .models import Patient, Visit, HerbalTreatment, Medicine, IrisImage

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

    class Meta:
        model = Visit
        fields = ['id', 'patient', 'visit_date', 'diagnosis', 'notes', 'document', 'herbal_treatments', 
                 'medicines', 'iris_images', 'created_at', 'updated_at']

class PatientSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'patient_code', 'first_name', 'last_name', 'birth_date', 'gender',
                 'phone', 'email', 'tc_no', 'city', 'district', 'address', 'blood_type', 
                 'allergies', 'notes', 'visits', 'created_at', 'updated_at'] 