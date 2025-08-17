from rest_framework import serializers
from .models import (
    Event, Video, Book, Music, Book_File, About,
    ContactMessage, Testimonial
)


# ------------------------
# Content Serializers
# ------------------------


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'image', 'description', 'date',
            'location', 'created_at', 'created_by'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']
        
    def validate_image(self, value):
        allowed_exts = ['jpg', 'jpeg', 'png']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_exts:
            raise serializers.ValidationError(
                f"Only image files ({', '.join(allowed_exts)}) are allowed."
            )
        return value

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'music', 'author', 'title', 
                  'uploaded_at', 'created_by']
        read_only_fields = ['id', 'uploaded_at',
                            'created_by']
        
    def validate_music_file(self, value):
        allowed_exts = ['mp3', 'jpg', 'png', 'jpeg']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_exts:
            raise serializers.ValidationError(
                f"Only {', '.join(allowed_exts)} files are allowed."
            )
        return value
    

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description',
            'video_url', 'uploaded_at', 'created_by'
        ]
        read_only_fields = ['id', 'uploaded_at', 'created_by']

    def validate_video_url(self, value):
        ext = value.name.split('.')[-1].lower()
        if ext not in ['mp4', 'mov', 'avi', 'mkv']:
            raise serializers.ValidationError("Only mp4, mov, avi, mkv allowed.")
        if value.size < 2 * 1024 * 1024:
            raise serializers.ValidationError("File too small (min 2 MB).")
        if value.size > 100 * 1024 * 1024:
            raise serializers.ValidationError("File too large (max 100 MB).")
        return value


class BookFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book_File
        fields = ['id', 'file_url']
        read_only_fields = ['id']
        
    def validate_file_url(self, value):
        if value:
            ext = value.name.split('.')[-1].lower()
            if ext not in ['pdf', 'docx']:
                raise serializers.ValidationError("Only PDF or DOCX files are allowed.")
        return value

class BookSerializer(serializers.ModelSerializer):
    file_url = BookFileSerializer(read_only=True)
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description',
            'file_url', 'cover_image_url', 'created_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = ['id', 'content', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'subject',
            'message', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

        
class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ['id', 'name', 'content', 'image_url', 'created_at']
        read_only_fields = ['id', 'created_at']
        
    def validate_image_url(self, value):
        allowed_exts = ['jpg', 'jpeg', 'png']
        ext = value.name.split('.')[-1].lower()
        if ext not in allowed_exts:
            raise serializers.ValidationError(
                f"Only image files ({', '.join(allowed_exts)}) are allowed."
            )
        return value


class AllContentSerializer(serializers.Serializer):
    events = EventSerializer(many=True, read_only=True)
    events_count = serializers.IntegerField(read_only=True)

    musics = MusicSerializer(many=True, read_only=True)
    musics_count = serializers.IntegerField(read_only=True)

    videos = VideoSerializer(many=True, read_only=True)
    videos_count = serializers.IntegerField(read_only=True)

    books = BookSerializer(many=True, read_only=True)
    books_count = serializers.IntegerField(read_only=True)

    abouts = AboutSerializer(many=True, read_only=True)
    abouts_count = serializers.IntegerField(read_only=True)

    contacts = ContactMessageSerializer(many=True, read_only=True)
    contacts_count = serializers.IntegerField(read_only=True)

    testimonials = TestimonialSerializer(many=True, read_only=True)
    testimonials_count = serializers.IntegerField(read_only=True)
        
