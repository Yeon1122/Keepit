from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(source='author.userid', read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author_id', 'content', 'created_at', 'updated_at', 'likes_count']
        read_only_fields = ['post']

    def get_likes_count(self, obj):
        return obj.likes.count()

class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(source='author.userid', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'board_type', 'title', 'content', 'author_id', 'created_at', 
                 'updated_at', 'comments', 'likes_count']
        read_only_fields = ['board_type', 'author_id']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        print("Validated data in create:", validated_data)  # 디버깅용
        author = self.context['request'].user
        validated_data['author'] = author
        return super().create(validated_data) 