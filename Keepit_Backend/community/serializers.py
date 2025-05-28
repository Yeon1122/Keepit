from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(source='author.userid', read_only=True)
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_id', 'author_nickname', 'content', 'created_at', 'updated_at', 'likes_count', 'is_liked']
        read_only_fields = ['post']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(source='author.userid', read_only=True)
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'board_type', 'title', 'content', 'author_id', 'author_nickname', 
                 'created_at', 'updated_at', 'comments', 'likes_count', 'is_liked']
        read_only_fields = ['board_type', 'author_id']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        print("Validated data in create:", validated_data)  # 디버깅용
        author = self.context['request'].user
        validated_data['author'] = author
        return super().create(validated_data) 