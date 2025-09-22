from django.shortcuts import redirect
from django.core.cache import cache
import requests
from django.contrib.auth.models import User
from django.contrib.auth import login
from game.models.player.player import Player
from random import randint

def receive_code(request):
    data = request.GET
    code = data.get('code')
    state = data.get('state')

    # 改成自己的回调地址
    redirect_uri = "https://app7581.acapp.acwing.com.cn/settings/qq/receive_code"  # 此处不用处理网址中的特殊字符

    if not cache.has_key(state):  # 若无此state返回主页面
        return redirect("index")

    cache.delete(state)


    apply_access_token_url = "https://graph.qq.com/oauth2.0/token"
    params = {
        'grant_type': 'authorization_code',
        'client_id': "102808975",                            # 填入APP ID
        'client_secret': "PgiU0OYXIn49za1E",                 # 填入APP Key
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
    if players.exists():  # 如果该用户已存在，则无需获取信息，直接登录
        login(request, players[0].user)
        return redirect("index")


    get_user_info_url = "https://graph.qq.com/user/get_user_info"
    params = {
        'access_token': access_token,
        'oauth_consumer_key': "102808975",      # 填入APP ID
        'openid': openid
    }
    userinfo_res = requests.get(get_user_info_url, params=params).json()
    username = userinfo_res['nickname']
    photo = userinfo_res['figureurl_qq_1']


    while User.objects.filter(username=username).exists():  # 给重名的用户找一个不重名的名字
        username += str(randint(0, 9))

    user = User.objects.create(username=username)
    player = Player.objects.create(user=user, photo=photo, openid=openid)

    login(request, user)

    return redirect("index")
