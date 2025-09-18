from game.models.player.player import Player
from game.models.myspace.follow import Follow
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class GetInfo(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        try:
            user_id = int(request.GET.get('user_id', 1))
            me_id = request.user.id
            player = Player.objects.get(user_id=user_id)
            return Response({
                'id': player.user.id,
                'username': player.user.username,
                'photo': player.photo,
                'followerCount': player.followerCount,
                'is_followed': Follow.objects.filter(source=me_id, target=user_id).exists()
            })
        except:
            return Response({
                'result': "输入参数错误"
            })

