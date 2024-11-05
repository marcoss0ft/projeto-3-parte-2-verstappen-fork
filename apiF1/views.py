from django.http import Http404, HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Driver, Team
from .serializers import DriverSerializer, TeamSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_driver(request, driver_id):
    try:
        driver = Driver.objects.get(id=driver_id, user=request.user)
    except Driver.DoesNotExist:
        raise Http404("Driver not found")
    
    if request.method == 'POST':
        new_driver_data = request.data
        if 'driverId' in new_driver_data:
            driver.driverId = new_driver_data['driverId']
            driver.user = request.user
            driver.save()
        else:
            return Response({'error': 'driverId is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        driver.delete()
        return Response({'message': 'Driver deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    serialized_driver = DriverSerializer(driver)
    return Response(serialized_driver.data)

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_team(request, team_id):
    try:
        team = Team.objects.get(id=team_id, user=request.user)
    except Team.DoesNotExist:
        raise Http404("Team not found")

    if request.method == 'POST':
        new_team_data = request.data
        if 'teamId' in new_team_data:
            team.teamId = new_team_data['teamId']
            team.user = request.user
            team.save()
        else:
            return Response({'error': 'teamId is required.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        team.delete()
        return Response({'message': 'Team deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
    serialized_team = TeamSerializer(team)
    return Response(serialized_team.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_drivers(request):
    if request.method == 'POST':
        new_driver_data = request.data
        if 'driverId' not in new_driver_data:
            return Response({'error': 'driverId is required.'}, status=status.HTTP_400_BAD_REQUEST)
        driver = Driver(driverId=new_driver_data['driverId'], user=request.user)
        driver.save()

    drivers = Driver.objects.filter(user=request.user)
    serialized_driver = DriverSerializer(drivers, many=True)
    return Response(serialized_driver.data)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_teams(request):
    if request.method == 'POST':
        if hasattr(request.user, 'team'):
            return Response({'error': 'O usuário já possui uma equipe.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            new_team_data = request.data
            if 'teamId' not in new_team_data:
                return Response({'error': 'teamId is required.'}, status=status.HTTP_400_BAD_REQUEST)
            team = Team(teamId=new_team_data['teamId'], user=request.user)
            team.save()

    teams = Team.objects.filter(user=request.user)
    serialized_team = TeamSerializer(teams, many=True)
    return Response(serialized_team.data)

def index(request):
    return HttpResponse("Bem vindo à F1Stats 2024 API! Acesse /drivers ou /teams para ver os favoritos disponíveis.")

@api_view(['POST'])
def api_get_token(request):
    if request.method == 'POST':
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({"token": token.key})
            else:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def api_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'User with this username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)