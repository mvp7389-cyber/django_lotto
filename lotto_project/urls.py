from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 메인 홈('/')으로 들어오면 바로 lottos 앱의 주소 규칙을 따르도록 설정
    path('', include('lottos.urls')),
]
