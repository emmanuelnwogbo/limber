from rest_framework.response import Response
from rest_framework import viewsets, renderers, status, permissions
from django.db.models import Q
from app.serializers import OrgSerializer, UserSerializer, ProjectSerializer, TeamMemberSerializer
from app.models.user import User, Member
from app.models.project import Project, TeamMember
from rest_framework.decorators import detail_route

# A serializer_view_set class for creating an organisation
class OrgSignUpViewSet(viewsets.ModelViewSet):
    """This is to be used to signup an organisation"""
    queryset = User.objects.filter(user_type=2)
    serializer_class = OrgSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            current_user_id = request.user.id
            # create an organisation when you call this viewset
            User.create_orgprofile(current_user_id, **serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status' : "Bad request",
            'message' : "Failed to create an organisation"
        },status=status.HTTP_400_BAD_REQUEST)

# A serializer_view_set class for creating a user
class UserSignUpViewSet(viewsets.ModelViewSet):
    """This is to be used to signup a user"""
    queryset = User.objects.filter(user_type=1)
    serializer_class = UserSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # create a user when you call this viewset
            User.create_userprofile(**serializer.validated_data)
            return Response({
                    'status': 'User Created',
                    'message': 'User Created'
                },
                status=status.HTTP_201_CREATED)

        return Response({
            'status' : "Bad request",
            'message' : "Failed to create user"
        },status=status.HTTP_400_BAD_REQUEST)


class TeamMemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows project team members to be viewed or edited.
    """
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        orgs = Member.objects.filter(user_id=user.id).values_list('org_id', flat=True)
        users = User.objects.filter(Q(id=user.profile_id)| Q(id__in=orgs)).all()
        return Project.objects.filter(owner=users)

    def post_queryset(self):
        user = self.request.user
        orgs = Member.objects.filter(user_id=user.id).values_list('org_id', flat=True)
        users = User.objects.filter(Q(id=user.id)| Q(id__in=orgs)).all()
        return Project.objects.filter(owner=users)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # create a project when you call this viewset
            Project.create_project(**serializer.validated_data)
            return Response({
                    'status': 'Project Created',
                    'message': 'Project Created'
                }, status=status.HTTP_201_CREATED)

        return Response({
            'status' : "Bad request",
            'message' : "Failed to create an project"
        }, status=status.HTTP_400_BAD_REQUEST)