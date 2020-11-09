from rest_framework import serializers
from .models import Post,Tag,Image,Interest
from django.contrib.auth.models import User

class TagSerializer(serializers.Serializer):

	name = serializers.CharField(max_length=30)
	weight = serializers.IntegerField()

	def create(self, validated_data):
		return Tag.objects.create(**validated_data)

class PostSerializer(serializers.Serializer):

	description 		= serializers.CharField(max_length=255)
	likes				= serializers.IntegerField()
	dislikes			= serializers.IntegerField()
	tags 				= serializers.PrimaryKeyRelatedField(allow_empty=False, many=True, queryset=Tag.objects.all())
	pictures			= serializers.SerializerMethodField('_images')
	date_created		= serializers.DateField()
	likedusers 			= serializers.SerializerMethodField('_get_likedusers')
	dislikedusers 		= serializers.SerializerMethodField('_get_dislikedusers')

	def _get_likedusers(self,obj):

		queryset = Interest.objects.filter(post=obj).filter(status=True).values('user')
		users_liked = User.objects.filter(id__in=queryset)
		users_liked_serializer = UserSerializer(users_liked,many=True).data
		return users_liked_serializer

	def _get_dislikedusers(self,obj):

		queryset = Interest.objects.filter(post=obj).filter(status=False).values('user')
		users_disliked = User.objects.filter(id__in=queryset)
		users_disliked_serializer = UserSerializer(users_disliked,many=True).data
		return users_disliked_serializer

	def _images(self,obj):

		i = Image.objects.filter(post = obj)
		images = ImageSerializer(i,many=True).data
		return images

class ImageSerializer(serializers.Serializer):
 
    post_image = serializers.ImageField(max_length=100)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

class HomeSerializer(serializers.Serializer):

	description 		= serializers.CharField(max_length=255)
	likes				= serializers.IntegerField()
	dislikes			= serializers.IntegerField()
	tags 				= serializers.PrimaryKeyRelatedField(allow_empty=False, many=True, queryset=Tag.objects.all())
	current_user_status = serializers.SerializerMethodField('user')
	pictures			= serializers.SerializerMethodField('images')
	likedusers 			= serializers.SerializerMethodField('_get_likedusers')
	dislikedusers 		= serializers.SerializerMethodField('_get_dislikedusers')
	date_created		= serializers.DateField()

	def _get_likedusers(self,obj):

		queryset = Interest.objects.filter(post=obj).filter(status=True).values('user')
		users_liked = User.objects.filter(id__in=queryset)
		users_liked_serializer = UserSerializer(users_liked,many=True).data
		return users_liked_serializer

	def _get_dislikedusers(self,obj):

		queryset = Interest.objects.filter(post=obj).filter(status=False).values('user')
		users_disliked = User.objects.filter(id__in=queryset)
		users_disliked_serializer = UserSerializer(users_disliked,many=True).data
		return users_disliked_serializer

	def user(self,obj):

		if "request" in self.context:
			print("yes req")
			stat = Interest.objects.filter(user=self.context["request"]).filter(post=obj)
			if stat.exists():
				return stat[0].status
			else:
				print("no reqy")
				return None
		else:
			return None

	def images(self,obj):

		i = Image.objects.filter(post = obj)
		images = ImageSerializer(i,many=True).data
		return images    	     
    

class UserSerializer(serializers.Serializer):

	username = serializers.CharField(max_length=255)
