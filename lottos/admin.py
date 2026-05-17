from django.contrib import admin
from .models import LottoRound, LottoTicket

@admin.register(LottoRound)
class LottoRoundAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'get_numbers', 'bonus', 'created_at')

@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'mode', 'get_numbers', 'is_checked', 'rank', 'purchased_at')
