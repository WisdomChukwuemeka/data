from django.urls import path
from .views import (  EventView, VideoView,
                     BookView, AboutView, ContactMessageView,
                     TestimonialView,
                     DeleteEventView, DeleteTestimonyView,
                     MusicView, AllContentView, DeleteVideoView, EventListView)

urlpatterns = [
    path('events/', EventView.as_view(), name='events'),
    path('event_list/', EventListView.as_view(), name='event_list'),
    path('videos/', VideoView.as_view(), name='videos'),
    path('music/', MusicView.as_view(), name='music'),
    path('books/', BookView.as_view(), name='books'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactMessageView.as_view(), name='contact'),
    path('testimonials/', TestimonialView.as_view(), name='testimonials'),
    path('delete_event/<int:pk>/', DeleteEventView.as_view(), name='delete_event'),
    path('delete_video/<int:pk>/', DeleteVideoView.as_view(), name='delete_video'),
    path('delete_testimony/<int:pk>/', DeleteTestimonyView.as_view(), name='delete_testimony'),
    path('all_content/', AllContentView.as_view(), name='allcontent'),
]

