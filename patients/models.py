from django.db import models
from django.contrib.auth.models import User

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
    document = models.FileField(upload_to='visit_documents/', blank=True, null=True, verbose_name="Ziyaret Dokümanı")
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

class IrisImage(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name='iris_images')
    image = models.ImageField(upload_to='iris_images/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Iris image for {self.visit}"
