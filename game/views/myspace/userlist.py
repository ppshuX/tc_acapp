from game.models.player.player import Player
from rest_framework.views import APIView
from rest_framework.response import Response


class UserList(APIView):
    def get(self, request):
        players = Player.objects.all().exclude(photo="https://cdn.acwing.com/media/article/image/2022/06/21/1_3b60241ef1-photo.png").order_by('id')[:10]
        users = []
        for player in players:
            users.append({
                'id': player.user.id,
                'username': player.user.username,
                'photo': player.photo,
                'followerCount': player.followerCount
            })
        return Response(users)

