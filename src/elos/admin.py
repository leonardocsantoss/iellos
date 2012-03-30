from django.contrib import admin
from models import Elo, VotacaoEloFechado, ConviteElo

class EloAdmin(admin.ModelAdmin):
    list_display=('nome','data_criacao','criador',)
    search_fields = ['nome','criador',]
    filter_horizontal = ['membros',]

admin.site.register(Elo,EloAdmin)
admin.site.register(VotacaoEloFechado)
admin.site.register(ConviteElo)
