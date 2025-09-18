from django.urls import path
from game.views.settings.qq.apply_code import apply_code
from game.views.settings.qq.receive_code import receive_code

urlpatterns = [
    path("apply_code/", apply_code, name="settings_qq_apply_code"),
    path("receive_code", receive_code, name="settings_qq_receive_code"),
]

