from django.contrib import admin
from .models import Patient, Visit, UserProfile, VisitStage, StageEyeImage, StageMedicine, ProductionOrder

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type']
    list_filter = ['user_type']
    search_fields = ['user__username', 'user__email']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_code', 'first_name', 'last_name', 'birth_date', 'gender']
    search_fields = ['first_name', 'last_name', 'patient_code', 'tc_no']
    list_filter = ['gender', 'blood_type']

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['patient', 'visit_date', 'diagnosis']
    list_filter = ['visit_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'diagnosis']

@admin.register(VisitStage)
class VisitStageAdmin(admin.ModelAdmin):
    list_display = ['visit', 'stage_number', 'date']
    list_filter = ['date']
    search_fields = ['visit__patient__first_name', 'visit__patient__last_name']

admin.site.register(StageEyeImage)
admin.site.register(StageMedicine)

@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'patient_name', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['medicine__name', 'patient_name', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
