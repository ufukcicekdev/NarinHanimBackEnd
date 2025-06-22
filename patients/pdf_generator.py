from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from django.http import HttpResponse
from django.utils import timezone
from .models import ProductionOrder, StageMedicine
import io
import os

def generate_production_order_pdf(production_order):
    """Production order için PDF döküman oluştur"""
    
    # PDF buffer oluştur
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=1.5*cm, 
        leftMargin=1.5*cm, 
        topMargin=1*cm, 
        bottomMargin=1*cm
    )
    
    # Hikaye listesi
    story = []
    
    # Stil tanımları
    styles = getSampleStyleSheet()
    
    # Türkçe karakterler için font ayarları
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=15,
        alignment=1,  # Center alignment
        textColor=colors.HexColor('#2563eb'),
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=11,
        spaceAfter=8,
        spaceBefore=8,
        textColor=colors.HexColor('#1f2937'),
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=3,
        fontName='Helvetica'
    )
    
    # Başlık
    title = Paragraph("ILAC URETIM EMRI", title_style)
    story.append(title)
    story.append(Spacer(1, 10))
    
    # Tarih ve Sipariş Bilgileri
    date_info = [
        ['Tarih:', timezone.now().strftime('%d/%m/%Y %H:%M')],
        ['Siparis No:', f'#{production_order.id}'],
        ['Durum:', production_order.get_status_display()],
    ]
    
    date_table = Table(date_info, colWidths=[3*cm, 5*cm])
    date_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(date_table)
    story.append(Spacer(1, 10))
    
    # Hasta ve İlaç Bilgilerini Yan Yana Yerleştir
    patient = production_order.medicine.stage.visit.patient
    medicine = production_order.medicine
    
    # Sol kolon - Hasta Bilgileri
    left_data = [
        ['HASTA BILGILERI', ''],
        ['Ad Soyad:', f'{patient.first_name} {patient.last_name}'],
        ['TC Kimlik No:', patient.tc_no or 'Belirtilmemis'],
        ['Telefon:', patient.phone or 'Belirtilmemis'],
        ['E-posta:', patient.email or 'Belirtilmemis'],
        ['Kan Grubu:', patient.get_blood_type_display() or 'Belirtilmemis'],
        ['Dogum Tarihi:', patient.birth_date.strftime('%d/%m/%Y') if patient.birth_date else 'Belirtilmemis'],
    ]
    
    # Sağ kolon - İlaç Bilgileri  
    right_data = [
        ['ILAC BILGILERI', ''],
        ['Ilac Adi:', medicine.name],
        ['Doz:', medicine.dosage],
        ['Kullanim Sikligi:', medicine.frequency],
        ['Kullanim Suresi:', medicine.duration],
        ['', ''],
        ['', ''],
    ]
    
    # İki kolonu birleştir
    combined_data = []
    for i in range(len(left_data)):
        combined_data.append([left_data[i][0], left_data[i][1], right_data[i][0], right_data[i][1]])
    
    main_table = Table(combined_data, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
    main_table.setStyle(TableStyle([
        # Sol kolon başlık
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('SPAN', (0, 0), (1, 0)),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        
        # Sağ kolon başlık
        ('BACKGROUND', (2, 0), (3, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (2, 0), (3, 0), colors.white),
        ('FONTNAME', (2, 0), (3, 0), 'Helvetica-Bold'),
        ('SPAN', (2, 0), (3, 0)),
        ('ALIGN', (2, 0), (3, 0), 'CENTER'),
        
        # Sol kolon veriler
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(main_table)
    story.append(Spacer(1, 10))
    
    # Adres ve Ziyaret Bilgilerini Yan Yana
    visit = medicine.stage.visit
    
    address_visit_data = [
        ['ADRES BILGILERI', '', 'ZIYARET BILGILERI', ''],
        ['Il:', patient.city or 'Belirtilmemis', 'Ziyaret Tarihi:', visit.visit_date.strftime('%d/%m/%Y %H:%M')],
        ['Ilce:', patient.district or 'Belirtilmemis', 'Etap:', f'Etap {medicine.stage.stage_number}'],
        ['Adres:', patient.address or 'Belirtilmemis', 'Sikayet:', medicine.stage.complaint[:50] + '...' if len(medicine.stage.complaint) > 50 else medicine.stage.complaint],
    ]
    
    address_visit_table = Table(address_visit_data, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
    address_visit_table.setStyle(TableStyle([
        # Adres başlık
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#f59e0b')),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
        ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
        ('SPAN', (0, 0), (1, 0)),
        ('ALIGN', (0, 0), (1, 0), 'CENTER'),
        
        # Ziyaret başlık
        ('BACKGROUND', (2, 0), (3, 0), colors.HexColor('#8b5cf6')),
        ('TEXTCOLOR', (2, 0), (3, 0), colors.white),
        ('FONTNAME', (2, 0), (3, 0), 'Helvetica-Bold'),
        ('SPAN', (2, 0), (3, 0)),
        ('ALIGN', (2, 0), (3, 0), 'CENTER'),
        
        # Veriler
        ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f3f4f6')),
        ('BACKGROUND', (2, 1), (2, -1), colors.HexColor('#f3f4f6')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ('TOPPADDING', (0, 1), (-1, -1), 3),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
    ]))
    
    story.append(address_visit_table)
    story.append(Spacer(1, 10))
    
    # Kullanım Talimatları ve Önemli Notlar
    notes_data = []
    
    if medicine.notes:
        notes_data.append(['KULLANIM TALIMATLARI', medicine.notes])
    
    if patient.allergies:
        notes_data.append(['ONEMLI: ALERJI BILGILERI', f'DIKKAT: {patient.allergies}'])
    
    if visit.diagnosis:
        notes_data.append(['TANI', visit.diagnosis])
    
    if notes_data:
        notes_table = Table(notes_data, colWidths=[4*cm, 12*cm])
        notes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ef4444')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(notes_table)
        story.append(Spacer(1, 15))
    
    # İmza Alanları
    signature_info = [
        ['Hazirlayan:', '____________________', 'Tarih:', '____________________'],
        ['Imza:', '____________________', 'Onaylayan:', '____________________'],
    ]
    
    signature_table = Table(signature_info, colWidths=[3*cm, 5*cm, 3*cm, 5*cm])
    signature_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(signature_table)
    
    # PDF oluştur
    doc.build(story)
    
    # Buffer'ı başa al
    buffer.seek(0)
    
    return buffer


def generate_production_order_pdf_response(production_order):
    """PDF response döndür"""
    buffer = generate_production_order_pdf(production_order)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="uretim_emri_{production_order.id}.pdf"'
    response.write(buffer.getvalue())
    buffer.close()
    
    return response 