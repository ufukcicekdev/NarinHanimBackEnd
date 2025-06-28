from rest_framework import serializers
from .models import Patient, Visit, HerbalTreatment, Medicine, IrisImage, VisitStage, StageEyeImage, StageMedicine, ProductionOrder, Notification

class StageEyeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageEyeImage
        fields = ['id', 'stage', 'image', 'description', 'created_at']

class StageMedicineSerializer(serializers.ModelSerializer):
    production_orders = serializers.SerializerMethodField()
    
    class Meta:
        model = StageMedicine
        fields = ['id', 'stage', 'name', 'dosage', 'frequency', 'duration', 'notes', 'created_at', 'production_orders']
    
    def get_production_orders(self, obj):
        orders = obj.production_orders.all()
        return ProductionOrderSerializer(orders, many=True).data


class ProductionOrderSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = ProductionOrder
        fields = ['id', 'medicine', 'medicine_name', 'status', 'status_display', 'patient_name', 
                 'created_by', 'created_by_username', 'created_at', 'updated_at', 'completed_at', 'notes']

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

class NotificationSerializer(serializers.ModelSerializer):
    production_order_id = serializers.SerializerMethodField()
    medicine_name = serializers.SerializerMethodField()
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'target_user_type', 
                 'production_order_id', 'medicine_name', 'patient_name', 'is_read', 'created_at']
    
    def get_production_order_id(self, obj):
        return obj.production_order.id if obj.production_order else None
    
    def get_medicine_name(self, obj):
        return obj.production_order.medicine.name if obj.production_order and obj.production_order.medicine else None
    
    def get_patient_name(self, obj):
        return obj.production_order.patient_name if obj.production_order else None

class PatientSerializer(serializers.ModelSerializer):
    visits = VisitSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ['id', 'patient_code', 'first_name', 'last_name', 'birth_date', 'gender',
                 'phone', 'email', 'tc_no', 'city', 'district', 'address', 'blood_type', 
                 'allergies', 'notes', 'visits', 'created_at', 'updated_at'] 