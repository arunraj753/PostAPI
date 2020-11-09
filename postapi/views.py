from rest_framework.response import Response
from django.db.models import Max
from .models import Post,Tag,Image,Interest
from rest_framework.views import APIView


class LikePost(APIView):

	def get(self,request,pk):
		postObject  = Post.objects.get(pk=pk)
		searchQuery = Interest.objects.filter(user=request.user).filter(post=postObject)
		if searchQuery.exists():
			likePost = searchQuery[0]
			if likePost.status	== True:
				searchQuery[0].delete()
				postObject.likes -= 1
				postObject.save()
				return Response({"message":"Post Like Remvoed"},status=200)
			else:
				postObject.dislikes -= 1
		else:
			likePost 	  	= Interest()
			likePost.user 	= request.user
			likePost.post 	= postObject
		likePost.status	= True
		likePost.save()
		postObject.likes += 1
		postObject.save()
		return Response({"message":"Liked"},status=200)

class DislikePost(APIView):

	def get(self,request,pk):

		postObject  = Post.objects.get(pk=pk)
		searchQuery = Interest.objects.filter(user=request.user).filter(post=postObject)

		if searchQuery.exists():
			dislikePost = searchQuery[0]
			if dislikePost.status	== False:
				searchQuery[0].delete()
				postObject.dislikes -= 1
				postObject.save()
				return Response({"message":"Post DisLike Remvoed"},status=200)
			else:
				postObject.likes -= 1
		else:
			dislikePost 	  	= Interest()
			dislikePost.user 	= request.user
			dislikePost.post 	= postObject

		dislikePost.status	= False
		dislikePost.save()
		postObject.dislikes += 1
		postObject.save()
		return Response({"message":"DisLiked"},status=200)

