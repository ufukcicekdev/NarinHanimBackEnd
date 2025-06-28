from .models import Notification, ProductionOrder

def create_notification(title, message, notification_type, target_user_type, production_order=None, created_by=None):
    """Yeni bildirim oluştur"""
    notification = Notification.objects.create(
        title=title,
        message=message,
        notification_type=notification_type,
        target_user_type=target_user_type,
        production_order=production_order,
        created_by=created_by
    )
    return notification

def create_production_request_notification(production_order, created_by):
    """Farklı talep tipine göre bildirim oluştur (Lojistik için)"""
    
    # Status'a göre bildirim tipini ve mesajını belirle
    if production_order.status == 'package_requested':
        title = f"📦 Yeni Paket Hazırlama Talebi"
        message = f"{production_order.medicine.name} ilacı için paket hazırlama talebi geldi. Hasta: {production_order.patient_name}"
        notification_type = 'package_request'
    elif production_order.status == 'production_requested':
        title = f"🏭 Yeni Üretim Talebi"
        message = f"{production_order.medicine.name} ilacı için üretim talebi geldi. Hasta: {production_order.patient_name}"
        notification_type = 'production_request'
    elif production_order.status == 'cargo_requested':
        title = f"🚚 Yeni Kargo Hazırlama Talebi"
        message = f"{production_order.medicine.name} ilacı için kargo hazırlama talebi geldi. Hasta: {production_order.patient_name}"
        notification_type = 'cargo_request'
    else:
        title = f"🔔 Yeni Talep"
        message = f"{production_order.medicine.name} ilacı için {production_order.get_status_display().lower()} talebi geldi. Hasta: {production_order.patient_name}"
        notification_type = 'general_request'
    
    return create_notification(
        title=title,
        message=message,
        notification_type=notification_type,
        target_user_type='logistic',
        production_order=production_order,
        created_by=created_by
    )

def create_status_update_notification(production_order, old_status, new_status, updated_by):
    """Durum güncelleme bildirimi oluştur (Hasta Yöneticisi için)"""
    status_messages = {
        'package_preparing': '📦 Paket hazırlanmaya başlandı',
        'package_ready': '✅ Paket hazırlandı',
        'production_preparing': '🏭 Üretime hazırlanıyor',
        'production_sent': '🚀 Üretime gönderildi',
        'production_completed': '✅ Üretim tamamlandı',
        'cargo_preparing': '🚚 Kargo hazırlanıyor',
        'cargo_ready': '📦 Kargo hazırlandı',
        'cargo_shipped': '🚛 Kargoya verildi',
        'completed': '🎉 İşlem tamamlandı'
    }
    
    title = f"📋 İşlem Güncellendi"
    status_text = status_messages.get(new_status, production_order.get_status_display())
    message = f"{production_order.medicine.name} ilacı için: {status_text}. Hasta: {production_order.patient_name}"
    
    return create_notification(
        title=title,
        message=message,
        notification_type='status_update',
        target_user_type='patient_manager',
        production_order=production_order,
        created_by=updated_by
    )

def create_completion_notification(production_order, completed_by):
    """Tamamlama bildirimi oluştur (Hasta Yöneticisi için)"""
    title = f"🎉 İşlem Tamamlandı"
    message = f"{production_order.medicine.name} ilacının tüm işlemleri tamamlandı ve kargoya verildi. Hasta: {production_order.patient_name}"
    
    return create_notification(
        title=title,
        message=message,
        notification_type='production_complete',
        target_user_type='patient_manager',
        production_order=production_order,
        created_by=completed_by
    ) 