from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from .serializer import CreateEditProjectSerializer, GetProjectSerializer, GetAllProjects, \
    CreateEditEvaluationSerializer, GetResultSerializer, CreateEditResult
from user.models import User, Student
from hackathons.models import Project, Evaluated, Result
from django.db.models import Q


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FormParser, MultiPartParser])
def create_project(request, id):
    response = {}
    # get student object
    user = User.objects.get(email=request.user)
    student = Student.objects.get(uuid=user.id)
    request.data['student'] = user.id
    request.data['hackathon'] = id

    data = dict(request.data)
    print("Data is", data)
    data = {
        "student": student.uuid,
        "hackathon": id,
        "title": data['title'][0],
        "description": data['description'][0],
        "tag_line": data['tag_line'][0],
        "about": data['about'][0],
        "built_with": data['built_with'],
        "links": data['links'][0],
        "video_link": data['video_link'][0],

    }

    file = ""
    logo = ""
    for index, path in enumerate(request.data['file']):
        file = path

    for index, path in enumerate(request.data['logo']):
        logo = path

    serializer = CreateEditProjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        response['success'] = "Project has been added"
        return Response(data=response, status=status.HTTP_201_CREATED)
    else:
        response['error'] = "Error occurred while creating project"
    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_project(request, id):
    response = {}
    # get student object
    user = User.objects.get(email=request.user)
    request.data['student'] = user.id
    request.data['hackathon'] = id
    # get project id
    query = Project.objects.get(Q(hackathon=id, student=user.id))
    serializer = CreateEditProjectSerializer(query, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response['success'] = "Project has been edited"
        response['id'] = serializer.data['id']
        return Response(data=response, status=status.HTTP_201_CREATED)
    else:
        response['error'] = "Error occurred while creating project"
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_user_project_exists(request, id):
    # get user project if any
    response = {}

    try:
        user = User.objects.get(email=request.user)

        query = Project.objects.get(student=user.id, hackathon=id)
        if query:
            serializer = GetProjectSerializer(query)
            response['id'] = serializer.data['id']
            response['success'] = "Getting project data successful"
            return Response(data=response, status=status.HTTP_200_OK)

        response['not_found'] = "No project found"
        return Response(data=response, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while getting your project"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_project(request, id, projectID):
    response = {}

    try:
        query = Project.objects.get(hackathon=id, id=projectID)
        if query:
            serializer = GetProjectSerializer(query)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        response['not_found'] = "No project found"
        return Response(data=response, status=status.HTTP_200_OK)
    except:
        response['error'] = "Error occurred while getting your project"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_projects(request, id):
    response = {}

    try:
        query = Project.objects.filter(hackathon=id)
        if query.exists():
            serializer = GetAllProjects(query, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        response['not_found'] = "No projects found"
        return Response(data=response, status=status.HTTP_200_OK)
    except:
        print(serializer)
        response['error'] = "Error occurred while getting your project"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def evaluate_project(request, id, projectID):
    response = {}

    try:
        data = {
            "project": request.data['id'],
            "idea": request.data['idea'],
            "originality": request.data['originality'],
            "functionality": request.data['functionality'],
            "design": request.data['design'],
            "problem": request.data['problem'],
            "stars": request.data['stars'],
            "remarks": request.data['remarks']
        }

        serializer = CreateEditEvaluationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Evaluation Completed"
            return Response(data=response, status=status.HTTP_201_CREATED)

        response['error'] = "Error occurred while evaluating"
        return Response(data=response, status=status.HTTP_200_OK)

    except:
        response['error'] = "Error occurred while evaluating"
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_result(request, id):
    response = {}
    try:
        # get data
        first_query = Project.objects.get(id=request.data['first'])
        second_query = Project.objects.get(id=request.data['second'])
        third_query = Project.objects.get(id=request.data['third'])
        data = {
            "hackathon": id,
            "first": first_query.id,
            "second": second_query.id,
            "third": third_query.id

        }
        serializer = CreateEditResult(data=data)
        if serializer.is_valid():
            serializer.save()
            response['success'] = "Result has been poster"
            return Response(data=response, status=status.HTTP_201_CREATED)
    except:
        response['error'] = "Error occurred while creating result"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result(request, id):
    response = {}

    try:
        # get result
        query = Result.objects.filter(hackathon=id)
        if query.exists():
            serializer = GetResultSerializer(query, many=True)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        response['not_found'] = "No result found"
        return Response(data=response, status=status.HTTP_200_OK)

    except:
        response['error'] = "Error occurred while creating result"
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
