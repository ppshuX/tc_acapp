from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from game.models.myspace.post import Post



class PostView(APIView):
    permission_classes = ([IsAuthenticated])

    def get(self, request):
        user = request.user
        user_id = int(request.GET.get('user_id', 1))
        posts = Post.objects.filter(user_id=user_id).order_by('-pk')
        data = []
        for post in posts:
            data.append({
                'id': post.id,
                'content': post.content,
            })
        return Response(data)

    def post(self, request):
        Post.objects.create(user_id = request.user.id, content=request.POST.get('content', ''))
        return Response({
            'result': "success",
        })

    def delete(self, request, pk=None):
        user = request.user
        post_id = int(request.POST.get('post_id', 1))
        Post.objects.filter(user_id=user.id, pk=post_id).delete()
        return Response({
            'result': "success",
        })

