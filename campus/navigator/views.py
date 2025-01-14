from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models.expressions import result
from django.shortcuts import render, get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Notification,Request
from .serializers import EventSerializer, UserSerializer, NotificationSerializer, LoginSerializer,RequestSerializer


# Create your views here.
@api_view(['POST'])
def age(request):
    info = request.data
    if info['age'] < 18:
        result = 'not eligible for vote'
    else:
        result = 'eligible for vote'
    return Response({'message': result}, status=status.HTTP_200_OK)


class EventViewSet(viewsets.ModelViewSet):
    # import pdb;pdb.set_trace()
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        data = request.data
        sr = self.serializer_class(data=data)
        if sr.is_valid():
            msg = sr.save()
            notification = Notification.objects.create(
                message=f"New Event {msg.title} registered at {msg.location} on {msg.date} {msg.time}", type=1)
            notification.save()
            return Response({'message': "success", "data": sr.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "failed", "data": sr.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        formatted_datetime = f"{instance.date.strftime('%B %d, %Y')} at {instance.time.strftime('%I:%M %p')}"
        event_details = f"'{instance.title}' at {instance.location} on {formatted_datetime}"
        self.perform_destroy(instance)
        notification = Notification.objects.create(
            message=f"Event {event_details} has been deleted.",
            type=0,
        )
        notification.save()
        return Response({'message': "Event deleted successfully"}, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationView(APIView):
    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = NotificationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    login_key = False
    admin_key = False
    sts = status.HTTP_403_FORBIDDEN

    # Use the LoginSerializer to validate input data
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():  # Validate the data using the serializer
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:  # If authentication is successful
            login(request, user)
            if user.is_superuser:
                admin_key = True
            login_key = True
            sts = status.HTTP_200_OK
        else:  # If authentication fails
            sts = status.HTTP_401_UNAUTHORIZED
    else:  # If serializer validation fails
        sts = status.HTTP_400_BAD_REQUEST

    return Response({"login_key": login_key, "admin": admin_key,"username":user.username}, status=sts)
class RequestViewSet(viewsets.ModelViewSet):
    # import pdb;pdb.set_trace()
    queryset = Request.objects.all()
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        data = request.data
        sr = self.serializer_class(data=data)
        if sr.is_valid():
            msg = sr.save()
            return Response({'message': "success", "data": sr.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "failed", "data": sr.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def req_create(request):
    info = request.data
    try:
        req_from = User.objects.get(username=info['req_from'])
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

    message = info['message']
    date = info['date']
    from_time = info['from_time']
    to_time = info['to_time']

    # Create the request object
    req = Request.objects.create(req_from=req_from, message=message, date=date, from_time=from_time, to_time=to_time,
                                 status=0)
    req.save()

    return Response({'message': "Success"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def req_list(request):
    reqs = Request.objects.all()
    serializer = RequestSerializer(reqs, many=True)  # Serialize the queryset
    # user=User.objects.get(id=serializer.data.req_from.id)
    return Response({'message': "Success", 'req': serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def req_update(request):
    if request.method != 'PUT':
        return Response({'message': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    info = request.data
    try:
        req = Request.objects.get(id=info['request_id'])  # Find the request by its ID
    except Request.DoesNotExist:
        return Response({'message': 'Request not found'}, status=status.HTTP_400_BAD_REQUEST)
    req.replay=info.get('replay', req.replay)

    req.status = info.get('status', req.status)  # Can update the status as well

    req.save()  # Save the updated request

    return Response({'message': "Request updated successfully"}, status=status.HTTP_200_OK)
@api_view(['GET'])
def req_list_user(request,username):
    user=User.objects.get(username=username)
    reqs = Request.objects.filter(req_from=user)
    serializer = RequestSerializer(reqs, many=True)  # Serialize the queryset
    # user=User.objects.get(id=serializer.data.req_from.id)
    return Response({'message': "Success", 'req': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_list(request):
    user=User.objects.all()

    serializer = UserSerializer(user, many=True)  # Serialize the queryset
    # user=User.objects.get(id=serializer.data.req_from.id)
    return Response({'message': "Success", 'req': serializer.data}, status=status.HTTP_200_OK)