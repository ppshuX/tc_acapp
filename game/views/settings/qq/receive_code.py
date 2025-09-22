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

    if not cache.has_key(state):  # 若无此state返回主页面
        return redirect(reverse("index"))

    cache.delete(state)


    try:
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
        
        if 'access_token' not in access_token_res:
            return redirect(reverse("index"))
        
        access_token = access_token_res['access_token']

        apply_openid_url = "https://graph.qq.com/oauth2.0/me"
        params = {
            'access_token': access_token,
            'fmt': "json"
        }
        openid_res = requests.get(apply_openid_url, params=params).json()
        
        if 'openid' not in openid_res:
            return redirect(reverse("index"))
            
        openid = openid_res['openid']
    except Exception as e:
        return redirect(reverse("index"))


    players = Player.objects.filter(openid=openid)
    if players.exists():  # 如果该用户已存在，则无需获取信息，直接登录
        player = players[0]
        refresh = RefreshToken.for_user(player.user)
        return redirect(reverse("index") + "?access=%s&refresh=%s" % (str(refresh.access_token), str(refresh)))


    try:
        get_user_info_url = "https://graph.qq.com/user/get_user_info"
        params = {
            'access_token': access_token,
            'oauth_consumer_key': "102812476",      # 填入APP ID
            'openid': openid
        }
        userinfo_res = requests.get(get_user_info_url, params=params).json()
        
        if 'nickname' not in userinfo_res:
            return redirect(reverse("index"))
            
        username = userinfo_res['nickname']
        photo = userinfo_res['figureurl_qq_1']
    except Exception as e:
        return redirect(reverse("index"))


    while User.objects.filter(username=username).exists():  # 给重名的用户找一个不重名的名字
        username += str(randint(0, 9))

    user = User.objects.create(username=username)
    player = Player.objects.create(user=user, photo=photo, openid=openid)

    refresh = RefreshToken.for_user(user)

    return redirect(reverse("index") + "?access=%s&refresh=%s" % (str(refresh.access_token), str(refresh)))
