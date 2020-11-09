from rest_framework import viewsets
from rest_framework.response import Response
from .models import Tag,Post,Image,Interest
from .serializers import TagSerializer,PostSerializer,HomeSerializer,ImageSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import FileUploadParser
from django.db.models import Max
from .pagination import PostPageNumberPagination

class TagViewSet(viewsets.ModelViewSet):
	
	permission_classes = [IsAdminUser]
	queryset   		 = Tag.objects.all()
	serializer_class = TagSerializer

class PostViewSet(viewsets.ViewSet):

	permission_classes  = [IsAdminUser]
	parser_class 		= (FileUploadParser)

	def list(self,request):

		paginator    = PostPageNumberPagination()
		queryset 	 = Post.objects.annotate(max_weight=Max('tags__weight')).order_by('-max_weight')
		content		 = paginator.paginate_queryset(queryset, request)
		serializer   = PostSerializer(content, many=True)
		return paginator.get_paginated_response(serializer.data)
		

	def create(self,request):

		try:
			newpost = Post()
			newpost.description = request.data['description']
		except:
			return Response({"message":"Error:Post Description not added. Post not created"},status=400)

		tagslist = request.data.getlist('tags')
		if len(tagslist)==0:
			return Response({"message":"Error:Tags not added. Post not created"},status=400)

		try:
			file = 	request.data['file']
		except:
			return Response({"message":"Error:No image files added. Post not created"},status=400)

		newpost.save()

		for tag in tagslist:				
			newpost.tags.add(Tag.objects.get(pk=int(tag)))

		for picture in request.FILES.getlist('file'):
			newimage = Image()
			newimage.post_image = picture
			newimage.post = newpost
			newimage.save()

		serializer  = PostSerializer(newpost)
		return Response(serializer.data)

class HomeViewSet(viewsets.ViewSet):

	def list(self,request,*args,**kwargs):
		print("Helo")
		print(request.user)
		paginator    = PostPageNumberPagination()
		searchQuery = Interest.objects.filter(user=request.user).order_by('-id')

		if searchQuery.exists():
			LastLikePost 	   = searchQuery[0].post
			if searchQuery[0].status == True : 
				queryset	 = Post.objects.filter(tags__in=LastLikePost.tags.all()).annotate(max_weight=Max('tags__weight')).order_by('-max_weight')
				remain		 = Post.objects.exclude(id__in=queryset).annotate(max_weight=Max('tags__weight')).order_by('-max_weight')
				send =list(queryset)+list(remain)
			else:
				queryset	 = Post.objects.filter(tags__in=LastLikePost.tags.all()).annotate(max_weight=Max('tags__weight')).order_by('max_weight')
				remain		 = Post.objects.exclude(id__in=queryset).annotate(max_weight=Max('tags__weight')).order_by('-max_weight')
				send =list(remain)+list(queryset)
		else:
			send 	= Post.objects.annotate(max_weight=Max('tags__weight')).order_by('-max_weight')

		content		 = paginator.paginate_queryset(send, request)
		serializer   = HomeSerializer(content, many=True,context={"request": request.user})
		return paginator.get_paginated_response(serializer.data)

