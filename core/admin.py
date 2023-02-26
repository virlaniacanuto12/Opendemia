from django.contrib import admin
from .models import Cruzamento, DadosDemograficos, Doencas, Usuarios, LocaisVisitados, Relatorios
# Register your models here.

@admin.register(DadosDemograficos)
class DadosDemograficosAdmin(admin.ModelAdmin):
    list_display = ['pais', 'estado', 'populacao', 'area', 'id']

@admin.register(Doencas)
class DoencasAdmin(admin.ModelAdmin):
    list_display = ['nome', 'origem', 'tipo', 'id']

@admin.register(Usuarios)
class UsuariosAdmin(admin.ModelAdmin):
    list_display = ['nome', 'idade', 'cidade', 'id_facebook']

@admin.register(LocaisVisitados)
class LocaisVisitadosAdmin(admin.ModelAdmin):
    list_display = ['cidade', 'estado', 'pais']

@admin.register(Relatorios)
class RelatoriosAdmin(admin.ModelAdmin):
    list_display = ['doenca', 'casos', 'dadosdemograficos']

@admin.register(Cruzamento)
class CruzamentoAdmin(admin.ModelAdmin):
    list_display = ['usuario_id', 'doenca_id']
