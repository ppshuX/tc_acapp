from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from game.models.player.player import Player
from django.contrib.auth.models import User


class PlayerView(APIView):
    def post(self, request):
        data = request.POST
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        password_confirm = data.get("password_confirm", "").strip()
        if not username or not password:
            return Response({
                'result': "用户名和密码不能为空"
            })
        if password != password_confirm:
            return Response({
                'result': "两个密码不一致",
            })
        if User.objects.filter(username=username).exists():
            return Response({
                'result': "用户名已存在"
            })
        user = User(username=username)
        user.set_password(password)
        user.save()
        Player.objects.create(user=user, photo="https://cdn.acwing.com/media/article/image/2022/06/21/1_3b60241ef1-photo.png")
        return Response({
            'result': "success"
        })

