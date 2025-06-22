from django.db import models
from django.contrib.auth.models import User
import uuid
import os


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('patient_manager', 'Hasta Yöneticisi'),  # Normal hasta girişlerini yapan
        ('logistic', 'Lojistik'),  # Farklı dashboard kullanacak
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='patient_manager')
    
    def __str__(self):
        return f"{self.user.username} ({self.get_user_type_display()})"


class ProductionOrder(models.Model):
    ORDER_STATUS_CHOICES = [
        # Paket Hazırlama Süreci
        ('package_requested', 'Paket Hazırlama Talep Edildi'),
        ('package_preparing', 'Paket Hazırlanıyor'),
        ('package_ready', 'Paket Hazırlandı'),
        
        # Üretim Süreci  
        ('production_requested', 'Üretime Gönderme Talep Edildi'),
        ('production_preparing', 'Üretime Hazırlanıyor'),
        ('production_sent', 'Üretime Gönderildi'),
        ('production_completed', 'Üretim Tamamlandı'),
        
        # Kargo Süreci
        ('cargo_requested', 'Kargo Hazırlama Talep Edildi'), 
        ('cargo_preparing', 'Kargo Hazırlanıyor'),
        ('cargo_ready', 'Kargo Hazırlandı'),
        ('cargo_shipped', 'Kargoya Verildi'),
        
        # Tamamlama
        ('completed', 'Tamamlandı'),
    ]
    
    medicine = models.ForeignKey('StageMedicine', on_delete=models.CASCADE, related_name='production_orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
    patient_name = models.CharField(max_length=200)  # Hasta adı cache için
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.medicine.name} - {self.get_status_display()}"


def visit_document_upload_path(instance, filename):
    """Generate upload path for visit documents"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"visit_documents/{instance.patient.id}/{filename}"


def stage_eye_image_upload_path(instance, filename):
    """Generate upload path for stage eye images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"stage_eye_images/{instance.stage.visit.patient.id}/{instance.stage.id}/{filename}"


def iris_image_upload_path(instance, filename):
    """Generate upload path for iris images"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f"iris_images/{instance.visit.patient.id}/{filename}"

class Patient(models.Model):
    patient_code = models.CharField(max_length=30, blank=True, verbose_name="Hasta Kodu", help_text="Manuel hasta kodu (opsiyonel)")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="E-posta")
    tc_no = models.CharField(max_length=11, blank=True, verbose_name="TC Kimlik No")
    
    # Adres Bilgileri
    city = models.CharField(max_length=100, blank=True, verbose_name="İl")
    district = models.CharField(max_length=100, blank=True, verbose_name="İlçe")
    address = models.TextField(blank=True, verbose_name="Adres")
    
    # Kan Grubu
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A Rh+'),
        ('A-', 'A Rh-'),
        ('B+', 'B Rh+'),
        ('B-', 'B Rh-'),
        ('AB+', 'AB Rh+'),
        ('AB-', 'AB Rh-'),
        ('O+', 'O Rh+'),
        ('O-', 'O Rh-'),
        ('', 'Bilinmiyor'),
    ]
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True, verbose_name="Kan Grubu")
    
    # Alerjiler
    allergies = models.TextField(blank=True, verbose_name="Alerjiler", help_text="Bilinen alerjileri yazın")
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateTimeField()
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    document = models.FileField(upload_to=visit_document_upload_path, blank=True, null=True, verbose_name="Ziyaret Dokümanı")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Visit for {self.patient} on {self.visit_date}"

class HerbalTreatment(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='herbal_treatments')
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for {self.visit}"

class Medicine(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} for {self.visit}"

class VisitStage(models.Model):
    """Ziyaretin etapları - her etapta farklı muayene bilgileri"""
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='stages')
    stage_number = models.PositiveIntegerField(verbose_name="Etap Numarası")
    date = models.DateTimeField(verbose_name="Etap Tarihi")
    complaint = models.TextField(verbose_name="Şikayet", help_text="Hastanın bu etaptaki şikayetleri")
    notes = models.TextField(blank=True, verbose_name="Etap Notları")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['stage_number']
        unique_together = ['visit', 'stage_number']

    def __str__(self):
        return f"Etap {self.stage_number} - {self.visit}"

class StageEyeImage(models.Model):
    """Her etaptaki göz fotoğrafları"""
    stage = models.ForeignKey(VisitStage, on_delete=models.CASCADE, related_name='eye_images')
    image = models.ImageField(upload_to=stage_eye_image_upload_path, verbose_name="Göz Fotoğrafı")
    description = models.TextField(blank=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Göz Fotoğrafı - Etap {self.stage.stage_number}"

class StageMedicine(models.Model):
    """Her etaptaki ilaç bilgileri"""
    stage = models.ForeignKey(VisitStage, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=200, verbose_name="İlaç Adı")
    dosage = models.CharField(max_length=100, verbose_name="Doz")
    frequency = models.CharField(max_length=100, verbose_name="Kullanım Sıklığı")
    duration = models.CharField(max_length=100, verbose_name="Kullanım Süresi")
    notes = models.TextField(blank=True, verbose_name="İlaç Notları")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Etap {self.stage.stage_number}"

# Eski modelleri koruyalım ama artık kullanmayacağız
class IrisImage(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='iris_images')
    image = models.ImageField(upload_to=iris_image_upload_path)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Iris image for {self.visit}"
