from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from .serializer import ShareSerializer
from user.models import User


# creating share
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_share(request, ):
    response = {}

    try:
        # get the queries
        user_id = User.objects.get(email=request.user)
        post_query = Post.objects.get(id=request.data['post_id'])

        data = {
            "user": user_id.id,
            "post": post_query.id
        }
        serializer = ShareSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Post has been shared"
            return Response(data=response, status=status.HTTP_201_CREATED)
        response['error'] = "Error occurred while sharing post"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
    except:
        response['error'] = "Error occurred while sharing post"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
