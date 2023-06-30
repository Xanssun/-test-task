from rest_framework import serializers
from api.authentication import CustomAuthentication
from users.models import CustomUser
from posts.models import News, Comment


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Invalid username or password')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid username or password')

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        token = CustomAuthentication().generate_token(user)
        return user, token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'date']


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          queryset=CustomUser.objects.all())
    comments = CommentSerializer(many=True, read_only=True,
                                 source='comment_set')
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['id', 'date', 'title', 'text', 'author',
                  'likes_count', 'comments', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comment_set.count()
