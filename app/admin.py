from django.contrib import admin
from app.models import Patient, Investigation, Consultation


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'date_joined', 'is_active']
    list_editable = ['is_active']
    list_filter = ['is_active']


@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'title', 'file', 'created_at']


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'speciality', 'complaint', 'created_at']
    list_filter = ['speciality']
