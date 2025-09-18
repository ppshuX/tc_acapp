from django.http import JsonResponse
from urllib.parse import quote
from random import randint
from django.core.cache import cache


def get_state():
    res = ""
    for i in range(8):
        res += str(randint(0, 9))
    return res


def apply_code(request):
    client_id = "102812030"  # 填写 APP ID
    redirect_uri = quote("https://app7581.acapp.acwing.com.cn/settings/qq/receive_code")  # 处理网址中的特殊字符
    scope = "get_user_info"
    state = get_state()

    cache.set(state, True, 600)  # 有效期十分钟

    response_type = "code"

    apply_code_url = "https://graph.qq.com/oauth2.0/authorize"
    return JsonResponse({
        'result': 'success',
        'apply_code_url': apply_code_url + "?response_type=%s&client_id=%s&redirect_uri=%s&scope=%s&state=%s" % (response_type, client_id, redirect_uri, scope, state)
    })
