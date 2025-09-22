from django.shortcuts import redirect, reverse
from django.core.cache import cache
import requests
from django.contrib.auth.models import User
from game.models.player.player import Player
from random import randint
from rest_framework_simplejwt.tokens import RefreshToken

def receive_code(request):
    data = request.GET
    code = data.get('code')
    state = data.get('state')

    # 改成自己的回调地址
    redirect_uri = "https://app7581.acapp.acwing.com.cn/settings/qq/receive_code"  # 此处不用处理网址中的特殊字符

    if not cache.has_key(state):
        return redirect("index")

    cache.delete(state)

    apply_access_token_url = "https://graph.qq.com/oauth2.0/token"
    params = {
        'grant_type': 'authorization_code',
        'client_id': "102809005",                            # 填入APP ID
        'client_secret': "Wu2waz81e6KL8hrp",                 # 填入APP Key
        'code': code,
        'redirect_uri': redirect_uri,
        'fmt': "json"
    }
    access_token_res = requests.get(apply_access_token_url, params=params).json()
    access_token = access_token_res['access_token']

    apply_openid_url = "https://graph.qq.com/oauth2.0/me"
    params = {
        'access_token': access_token,
        'fmt': "json"
    }
    openid_res = requests.get(apply_openid_url, params=params).json()
    openid = openid_res['openid']

    players = Player.objects.filter(openid=openid)
    if players.exists():
        refresh = RefreshToken.for_user(players[0].user)
        return redirect(reverse("index") +  "?access=%s&refresh=%s" % (str(refresh.access_token), str(refresh)))

    get_user_info_url = "https://graph.qq.com/user/get_user_info"
    params = {
        'access_token': access_token,
        'oauth_consumer_key': "102809005",      # 填入APP ID
        'openid': openid
    }
    userinfo_res = requests.get(get_user_info_url, params=params).json()
    username = userinfo_res['nickname']
    photo = userinfo_res['figureurl_qq_1']

    while User.objects.filter(username=username).exists():
        username += str(randint(0, 9))

    user = User.objects.create(username=username)
    player = Player.objects.create(user=user, photo=photo, openid=openid)

    refresh = RefreshToken.for_user(user)
    return redirect(reverse("index") +  "?access=%s&refresh=%s" % (str(refresh.access_token), str(refresh)))
