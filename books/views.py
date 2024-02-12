from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from books.models import Author, Book
from books.serializers import AuthorSerializer, BookSerializer, PaginationSerializer
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from books.utilities import round_up

class AuthorListView(APIView):
   
    #Listing all the author
    def get(self, request):
        """
        API endpoint for listing all authors without pagination

        - Method: GET
        - Response: List of all authors with details.
        - URL: /api/authors/
        """

        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response({
            "status":  1,
            "message": "Author details retrieved successfully",
            "data": serializer.data}, status = status.HTTP_200_OK
        )
    
    #Create a new author
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'bio': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['name', 'email', 'bio']
        ),
        responses={status.HTTP_201_CREATED: AuthorSerializer()}
    )
    def post(self, request):
        """
        API endpoint for creating a new author.

        - Method: POST
        - Input: Author details (name, email, bio)
        - Response: Details of the created author.
        - URL: /api/authors/
        """

        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 1,
                "message": "New author details created successfully",
                "data": serializer.data}, status = status.HTTP_201_CREATED
            )
        return Response({
            "status": 0,
            "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST
        )

class AuthorDetailView(APIView):
   
    def get_object(self, id):
        try:
            return Author.objects.get(id=id)
        except Author.DoesNotExist:
           raise Http404

    #Get a single author
    def get(self, request, id):
        """
        API endpoint for retrieving single author.

        - Method: GET
        - Response: Retrieve a single author with details.
        - URL: /api/authors/<int:id>/
        """

        author = self.get_object(id)
        serializer = AuthorSerializer(author)
        return Response({
            "status": 1, 
            "message": "success", 
            "data":serializer.data}, status = status.HTTP_200_OK
        )

    #Updating an author
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'bio': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['name', 'email', 'bio']
        ),
        responses={status.HTTP_200_OK: AuthorSerializer()}
    )
    def put(self, request, id):
        """
        API endpoint for updating an author.

        - Method: PUT
        - Input: Author details (name, email, bio)
        - Response: Details of the updated author.
        - URL: /api/authors/<int:id>/
        """

        author = self.get_object(id)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 1, 
                "message": "Author details updated successfully", 
                "data":serializer.data}, status = status.HTTP_200_OK
            )
        return Response({
            "status": 0,
            "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST
        )

    #Deleting an author --> Hard delete
    def delete(self, request, id):
        """
        API endpoint for deleting an author.

        - Method: DELETE
        - Response: Deleting an author.
        - URL: /api/authors/<int:id>/
        """

        author = self.get_object(id)
        author.delete()
        return Response({
            "status": 1, 
            "message": "Author details deleted successfully"}, status = status.HTTP_200_OK
        )
class GetAuthorList(APIView):

    #Listing all author details ---> Pagination Added
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                'page_size': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['page', 'page_size']
        ),
        responses={status.HTTP_200_OK: AuthorSerializer()}
    )

    def post(self, request):
        """
        API endpoint for listing all author details with pagination

        - Method: POST
        - Input: Pagination details (page, page_size)
        - Response:  List of all authors with details.
        - URL: /api/listing-all-authors/
        """
        serializer = PaginationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": 0, 
                "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST
            )
        page = serializer.validated_data.get('page')
        page_size = serializer.validated_data.get('page_size')

        # Calculate skip value for pagination
        skip = (page - 1) * page_size

        # Retrieve paginated authors
        authors = Author.objects.all()[skip: skip + page_size]
        serializer = AuthorSerializer(authors, many=True)
        total_records = Author.objects.all().count()
        num_pages = (total_records / page_size)
        num_pages = round_up(num_pages)
        return Response({
            "status":  1,
            "message": "Author details retrieved successfully",
            "paginator":  {
                "total_records": total_records,
                "total_pages":num_pages,
                "current_page":page,
                "current_page_size": len(serializer.data),
                'next_page': None if (num_pages == page or total_records == 0) else (page+1),
                'previous_page': (page-1),
            },
            "data": serializer.data}, status = status.HTTP_200_OK
        )

class BookListView(APIView):
  
    #Listing all the books
    def get(self, request):
        """
        API endpoint for listing all books.

        - Method: GET
        - Response: List of all books with details.
        - URL: /api/books/
        """

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({
            "status":  1,
            "message": "Book details retrieved successfully",
            "data": serializer.data}, status = status.HTTP_200_OK
        )

    #Create a new book
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'author': openapi.Schema(type=openapi.TYPE_INTEGER),
                'published_date': openapi.Schema(type=openapi.TYPE_STRING),
                'price': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['title', 'author', 'published_date', 'price']
        ),
        responses={status.HTTP_201_CREATED: BookSerializer()}
    )
    def post(self, request):
        """
        API endpoint for creating a new book.

        - Method: POST
        - Input: Book details (title, author, published_date, price)
        - Response: Details of the created book.
        - URL: /api/books/
        """

        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 1,
                "message": "New Book details created successfully",
                "data": serializer.data}, status = status.HTTP_201_CREATED
            )
        return Response({
            "status": 0,
            "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST
        )

class BookDetailView(APIView):
   
    def get_object(self, id):
        try:
            return Book.objects.get(id=id)
        except Book.DoesNotExist:
            raise Http404

    #Get a single book
    def get(self, request, id):
        """
        API endpoint for retrieving single book.

        - Method: GET
        - Response: Retrieve a single book with details.
        - URL: /api/books/<int:id>/
        """

        book = self.get_object(id)
        serializer = BookSerializer(book)
        return Response({
            "status": 1, 
            "message": "success", 
            "data":serializer.data}, status = status.HTTP_200_OK
        )

    #Updating a book
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'author': openapi.Schema(type=openapi.TYPE_INTEGER),
                'published_date': openapi.Schema(type=openapi.TYPE_STRING),
                'price': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['title', 'author', 'published_date', 'price']
        ),
        responses={status.HTTP_200_OK: BookSerializer()}
    )
    def put(self, request, id):
        """
        API endpoint for updating a book.

        - Method: PUT
        - Input: Book details (title, author, published_date, price)
        - Response: Details of the updated book.
        - URL: /api/books/<int:id>/
        """

        book = self.get_object(id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": 1, 
                "message": "Book details updated successfully", 
                "data":serializer.data}, status = status.HTTP_200_OK
            )
        return Response({
            "status": 0,
            "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST
        )

    #Deleting a book --> Hard delete
    def delete(self, request, id):
        """
        API endpoint for deleting a book.

        - Method: DELETE
        - Response: Deleting a book.
        - URL: /api/books/<int:id>/
        """

        book = self.get_object(id)
        book.delete()
        return Response({
            "status": 1, 
            "message": "Book details deleted successfully"}, status = status.HTTP_200_OK
        )

class GetBookList(APIView):
    
    #Listing all book details ---> Pagination Added
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'page': openapi.Schema(type=openapi.TYPE_INTEGER),
                'page_size': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
            required=['page', 'page_size']
        ),
        responses={status.HTTP_200_OK: BookSerializer()}
    )

    def post(self, request):
        """
        API endpoint for listing all book details with pagination

        - Method: POST
        - Input: Pagination details (page, page_size)
        - Response:  List of all book with details.
        - URL: /api/listing-all-books/
        """
        serializer = PaginationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": 0, 
                "message": serializer.errors}, status = status.HTTP_400_BAD_REQUEST
            )
        page = serializer.validated_data.get('page')
        page_size = serializer.validated_data.get('page_size')

        # Calculate skip value for pagination
        skip = (page - 1) * page_size

        # Retrieve paginated books
        books = Book.objects.all()[skip: skip + page_size]
        serializer = BookSerializer(books, many=True)
        total_records = Book.objects.all().count()
        num_pages = (total_records / page_size)
        num_pages = round_up(num_pages)
        return Response({
            "status":  1,
            "message": "Book details retrieved successfully",
            "paginator":  {
                "total_records": total_records,
                "total_pages":num_pages,
                "current_page":page,
                "current_page_size": len(serializer.data),
                'next_page': None if (num_pages == page or total_records == 0) else (page+1),
                'previous_page': (page-1),
            },
            "data": serializer.data}, status = status.HTTP_200_OK
        )