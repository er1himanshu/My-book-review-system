from rest_framework import viewsets, generics
from rest_framework.pagination import PageNumberPagination
from .models import Book, Review
from .serializers import BookSerializer, ReviewSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.views.generic import TemplateView

# Filter for Book model
class BookFilter(filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'genre': ['exact'],
            'published_date': ['exact', 'year__gt', 'year__lt'],
        }

# ViewSet for Book model
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = BookFilter
    search_fields = ['title', 'author']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5  

# ViewSet for Review model
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]  
    def create(self, request, *args, **kwargs):
        """Handle review submission with error handling."""
        try:
            # Attempt to create the review
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            # Catch validation errors and return a 400 response with error details
            return Response({"error": str(e)}, status=400)

# User Registration View
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  

# User Login View
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid credentials"}, status=400)

# Home View for serving React app
class HomeView(TemplateView):
    template_name = "index.html"
