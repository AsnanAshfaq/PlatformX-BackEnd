from rest_framework.decorators import api_view, permission_classes, parser_classes
from .serializer import CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from posts.models import Comment
from rest_framework.permissions import IsAuthenticated


# creating comment
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request):
    response = {}
    comment_serializer = CommentSerializer(data=request.data, context={"request": request})
    if comment_serializer.is_valid():
        print("Comment Serializer is valid")
        comment_serializer.save()
        response["success"] = "Comment has been created"
        return Response(data=response, status=status.HTTP_201_CREATED)
    else:
        response["error"] = "Error while posting comment"
        return Response(data=response, status=status.HTTP_201_CREATED)


# getting comments
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments(request, id):
    response = {}
    try:
        comment = Comment.objects.filter(post=id)
        comment_serializer = CommentSerializer(comment, many=True)
        response["success"] = "Comments found"
        return Response(data=comment_serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        response["error"] = "Error while fetching comments"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)
