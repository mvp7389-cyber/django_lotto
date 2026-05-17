from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LottoRound(models.Model):
    round_number = models.PositiveIntegerField(unique=True, default=0, verbose_name="회차")
    num1 = models.PositiveIntegerField(default=0, verbose_name="번호 1")
    num2 = models.PositiveIntegerField(default=0, verbose_name="번호 2")
    num3 = models.PositiveIntegerField(default=0, verbose_name="번호 3")
    num4 = models.PositiveIntegerField(default=0, verbose_name="번호 4")
    num5 = models.PositiveIntegerField(default=0, verbose_name="번호 5")
    num6 = models.PositiveIntegerField(default=0, verbose_name="번호 6")
    bonus = models.PositiveIntegerField(default=0, verbose_name="보너스 번호")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="추첨 일시")

    def __str__(self):
        return f"제 {self.round_number}회 당첨번호"

    def get_numbers(self):
        return [self.num1, self.num2, self.num3, self.num4, self.num5, self.num6]

class LottoTicket(models.Model):
    SELECTION_CHOICES = [('AUTO', '자동'), ('MANUAL', '수동')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="구매자")
    lotto_round = models.ForeignKey(LottoRound, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="해당 회차")
    mode = models.CharField(max_length=10, choices=SELECTION_CHOICES, verbose_name="구매 방식")
    num1 = models.PositiveIntegerField(default=0)
    num2 = models.PositiveIntegerField(default=0)
    num3 = models.PositiveIntegerField(default=0)
    num4 = models.PositiveIntegerField(default=0)
    num5 = models.PositiveIntegerField(default=0)
    num6 = models.PositiveIntegerField(default=0)
    is_checked = models.BooleanField(default=False, verbose_name="당첨 확인 여부")
    rank = models.IntegerField(default=-1, verbose_name="당첨 등수")
    purchased_at = models.DateTimeField(default=timezone.now, verbose_name="구매 일시")

    def get_numbers(self):
        return [self.num1, self.num2, self.num3, self.num4, self.num5, self.num6]
