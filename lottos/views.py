from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import LottoRound, LottoTicket
import random

# 유저 가상머니 가져오기 또는 생성 (세션/대체 기법 활용)
def get_user_balance(request):
    if 'balance' not in request.session:
        request.session['balance'] = 50000  # 최초 가입/접속 시 5만원 지급
    return request.session['balance']

def change_user_balance(request, amount):
    request.session['balance'] = request.session.get('balance', 50000) + amount
    request.session.modified = True

def lobby(request):
    latest_round = LottoRound.objects.order_by('-round_number').first()
    balance = get_user_balance(request)
    return render(request, 'lottos/lobby.html', {
        'latest_round': latest_round,
        'balance': balance
    })

@login_required
def buy_lotto(request):
    balance = get_user_balance(request)
    if request.method == 'POST':
        if balance < 1000:
            messages.error(request, "잔액이 부족합니다! 로비에서 머니를 충전해주세요.")
            return redirect('buy_lotto')
        
        mode = request.POST.get('mode')
        
        if mode == 'AUTO':
            numbers = sorted(random.sample(range(1, 46), 6))
        else: # MANUAL
            try:
                numbers = sorted([
                    int(request.POST.get('num_1')), int(request.POST.get('num_2')),
                    int(request.POST.get('num_3')), int(request.POST.get('num_4')),
                    int(request.POST.get('num_5')), int(request.POST.get('num_6'))
                ])
            except (TypeError, ValueError):
                messages.error(request, "올바르지 않은 번호 선택입니다.")
                return redirect('buy_lotto')

        # 복권 생성 및 금액 차감
        LottoTicket.objects.create(
            user=request.user, mode=mode,
            num1=numbers[0], num2=numbers[1], num3=numbers[2],
            num4=numbers[3], num5=numbers[4], num6=numbers[5]
        )
        change_user_balance(request, -1000)
        messages.success(request, f"복권 1게임을 성공적으로 구매했습니다! (1,000원 차감 / 잔액: {balance-1000}원)")
        return redirect('my_tickets')

    return render(request, 'lottos/buy.html', {'balance': balance})

@login_required
def my_tickets(request):
    tickets = LottoTicket.objects.filter(user=request.user).order_by('-purchased_at')
    
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        ticket = LottoTicket.objects.get(id=ticket_id)
        
        # 현재 활성화된 가장 최신 회차와 대조
        latest_round = LottoRound.objects.order_by('-round_number').first()
        if not latest_round:
            messages.error(request, "아직 진행된 추첨 회차가 없어 당첨 확인이 불가능합니다.")
            return redirect('my_tickets')
            
        # 당첨 대조 정밀 알고리즘 (1등 ~ 5등)
        win_nums = set(latest_round.get_numbers())
        my_nums = set(ticket.get_numbers())
        match_count = len(win_nums.intersection(my_nums))
        
        rank = 0  # 낙첨 기본값
        prize = 0
        
        if match_count == 6:
            rank = 1
            prize = 10000000
        elif match_count == 5:
            # 5개가 맞고 보너스 번호까지 맞으면 2등, 아니면 3등
            if latest_round.bonus in my_nums:
                rank = 2
                prize = 2000000
            else:
                rank = 3
                prize = 1000000
        elif match_count == 4:
            rank = 4
            prize = 50000
        elif match_count == 3:
            rank = 5
            prize = 5000

        ticket.is_checked = True
        ticket.rank = rank
        ticket.lotto_round = latest_round
        ticket.save()
        
        if rank > 0:
            change_user_balance(request, prize)
            messages.success(request, f"🎉 대박! {rank}등에 당첨되어 상금 {prize:,}원이 적립되었습니다!")
        else:
            messages.success(request, "😭 아쉽게도 낙첨되었습니다. 다음 기회를 노려보세요!")
            
        return redirect('my_tickets')
        
    return render(request, 'lottos/my_tickets.html', {'tickets': tickets})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('lobby')
    all_rounds = LottoRound.objects.order_by('-round_number')
    return render(request, 'lottos/admin_dashboard.html', {'all_rounds': all_rounds})

@login_required
def admin_draw(request):
    if not request.user.is_staff or request.method != 'POST':
        return redirect('lobby')
        
    # 랜덤 7개 추출 (6개 당첨번호 + 1개 보너스 번호)
    all_nums = random.sample(range(1, 46), 7)
    win_nums = sorted(all_nums[:6])
    bonus_num = all_nums[6]
    
    # 회차 연산
    latest_round = LottoRound.objects.order_by('-round_number').first()
    next_round = (latest_round.round_number + 1) if latest_round else 1
    
    LottoRound.objects.create(
        round_number=next_round,
        num1=win_nums[0], num2=win_nums[1], num3=win_nums[2],
        num4=win_nums[3], num5=win_nums[4], num6=win_nums[5],
        bonus=bonus_num
    )
    messages.success(request, f"제 {next_round}회 차 당첨 번호가 성공적으로 추첨되었습니다!")
    return redirect('admin_dashboard')

# 무료 가상 머니 충전소 루틴
@login_required
def charge_money(request):
    change_user_balance(request, 10000)
    messages.success(request, "💰 가상 머니 10,000원이 충전되었습니다!")
    return redirect('lobby')
