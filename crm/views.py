from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from .models import Event, Music, Video, Book, About, ContactMessage, Testimonial
from rest_framework import viewsets
from .serializers import (
    EventSerializer, VideoSerializer, MusicSerializer,
    BookSerializer, AboutSerializer, 
    ContactMessageSerializer,
    AllContentSerializer,
    TestimonialSerializer
)
from .paginations import (CustomCursorPagination, CustomMusicPagination, 
    CustomVideoPagination, CustomAdminEventPagination)
from rest_framework.parsers import MultiPartParser, FormParser


# Mixin to add count to GET list responses
class CountMixin:
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        paginated_response = self.get_paginated_response(serializer.data)
        paginated_response.data['count'] = queryset.count()
        return paginated_response


class EventView(CountMixin, generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        return Event.objects.all().order_by('-id')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        total_count = Event.objects.count()
        return Response({
            'message': 'Event created successfully',
            'event': serializer.data,
            'count': total_count
        }, status=status.HTTP_201_CREATED) 
        

class EventListView(CountMixin, generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomAdminEventPagination

    def get_queryset(self):
        return Event.objects.all().order_by('-id')
     
        
class MusicView(CountMixin, generics.ListCreateAPIView):
    serializer_class = MusicSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomMusicPagination
    parser_classes = [MultiPartParser, FormParser] 
    
    def get_queryset(self):
        return Music.objects.all().order_by('-id')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        total_count = Music.objects.count()
        return Response({
            'message': 'Music Playlist created successfully',
            'music': serializer.data,
            'count': total_count
        }, status=status.HTTP_201_CREATED)      
    
      
        
class VideoView(CountMixin, generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomVideoPagination

    def get_queryset(self):
        return Video.objects.all().order_by('-id')
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)  # Debug
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(created_by=request.user)
        total_count = Video.objects.count()
        return Response({
            'message': 'Video created successfully',
            'video': serializer.data,
            'count': total_count
        }, status=status.HTTP_201_CREATED)
        

class BookView(CountMixin, generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomCursorPagination

    def get_queryset(self):
        return Book.objects.all().order_by('-id')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        total_count = Book.objects.count()
        return Response({
            'message': 'Book created successfully',
            'book': serializer.data,
            'count': total_count
        }, status=status.HTTP_201_CREATED)
        

class AboutView(CountMixin, generics.ListCreateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        abouts = self.get_queryset()
        serializer = self.get_serializer(abouts, many=True)
        return Response({
            'message': 'About content retrieved successfully',
            'abouts': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'About content created successfully',
            'about': serializer.data
        }, status=status.HTTP_201_CREATED)
        

class ContactMessageView(CountMixin, generics.ListCreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        messages = self.get_queryset()
        serializer = self.get_serializer(messages, many=True)
        return Response({
            'message': 'Contact messages retrieved successfully',
            'message': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Contact message created successfully',
            'message': serializer.data
        }, status=status.HTTP_201_CREATED)


class TestimonialView(CountMixin, generics.ListCreateAPIView):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    pagination_class = CustomMusicPagination

    def get_queryset(self):
        return Testimonial.objects.all().order_by('-id')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        total_count = Testimonial.objects.count()
        return Response({
            'message': 'Testimonial created successfully',
            'testimonial': serializer.data,
            'count': total_count
        }, status=status.HTTP_201_CREATED)
        
        
class DeleteEventView(APIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
   
    def delete(self, request, pk, *args, **kwargs):
        if not request.user:
            return Response({'detail': 'You do not have permission to delete users.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'detail': 'Event deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
            

class DeleteVideoView(APIView):
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
   
    def delete(self, request, pk, *args, **kwargs):
        if not request.user:
            return Response({'detail': 'You do not have permission to delete users.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = Video.objects.get(id=pk)
        except Video.DoesNotExist:
            return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'detail': 'Event deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        

class DeleteTestimonyView(APIView):
    serializer_class = TestimonialSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
   
    def delete(self, request, pk, *args, **kwargs):
        if not request.user:
            return Response({'detail': 'You do not have permission to delete users.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = Testimonial.objects.get(id=pk)
        except Testimonial.DoesNotExist:
            return Response({'detail': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({'detail': 'Event deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)



class AllContentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        data = {
            "events": Event.objects.all().order_by('-id'),
            "events_count": Event.objects.count(),

            "musics": Music.objects.all().order_by('-id'),
            "musics_count": Music.objects.count(),

            "videos": Video.objects.all().order_by('-id'),
            "videos_count": Video.objects.count(),

            "books": Book.objects.all().order_by('-id'),
            "books_count": Book.objects.count(),

            "abouts": About.objects.all(),
            "abouts_count": About.objects.count(),

            "contacts": ContactMessage.objects.all().order_by('-id'),
            "contacts_count": ContactMessage.objects.count(),

            "testimonials": Testimonial.objects.all().order_by('-id'),
            "testimonials_count": Testimonial.objects.count(),
        }

        serializer = AllContentSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
