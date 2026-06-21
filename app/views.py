from django.db.migrations import serializer
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Author
from .  serializers import BookSerializer, AuthorSerializer


def book_list_view(request):
    books = Book.objects.all() # barcha kitoblarni oladi
    authors = Author.objects.all() #barcha mualliflarni oladi
    context = {'books': books, 'authors': authors} #HTML ga yuboriladigon malumotlar
    return render(request, 'book_list.html', context) # HTML sahifaga qaytaradi

def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk) #URL dagi id ni tekshiradi agar mavjud bolmasa 404 xatolik chaqiradi
    return render(request,'book_detail.html', {'book': book})#

def book_create_view(request):
    if request.method == 'POST': #foydalanuvchiga formani yuboradi
        title = request.POST.get('title')  #formadan "title' maydonini oladi
        author_id = request.POST.get('author')# formadan authoe maydonini oladi (id raqamoni)
        author = get_object_or_404(Author, pk=author_id) #id boyicha muallif ismini topadi
        Book.objects.create(title=title, author=author) #yangi kitob yaratadi va DB ga saqlaydi
        return redirect('book_list') #kitoblar royxatiga qaytaradi
    authors = Author.objects.all() #GET sorovida barcha mualliflarni oladi
    return render(request, 'book_form.html', {'authors': authors})

def book_delete_view(request, pk):
    book = get_object_or_404(Book, pk=pk) #ochiriladigon id dagi kitobni topadi
    if request.method == 'POST': # agar ha ochirish tugmasi bosilsa
        book.delete() #kitobni DB dan ochiradi
        return redirect('book_list') #kitoblar royxatiga qaytaradi
    return render(request, 'book_confirm_delete.html', {'book': book})


def author_create(request):
    if request.method == 'POST': #kitob yaratish uchun forma yuboradi
        name = request.POST.get('name') #formadan 'name' maydonini olib
        Author.objects.create(name=name) #yangi muallif yaratdi
        return redirect('author_list') #mualliflar royxatiga qaytaradi
    return render(request, 'author_create.html')

def author_list(request):
    authors = Author.objects.all() #barcha mualliflarni oladi
    return render(request, 'author_list.html', {'authors': authors})
    #HTML ga yuboradi







class AuthorListAPIVew(APIView):
    # APIView = DRF view klassi, HTTP metodlarini alohida boshqaradi
    #list = yangi qoshish va royaxt korsatish uchun
    def get(self, request): #GET sorovi kelganda ishlaydi, masalan /api/author/ brauserga kirganda
        authors = Author.objects.all() #barcha malumotlarni DB dan oladi
        serializer = AuthorSerializer(authors, many=True)
        # author = royxat bolgani uchun many=true boladi
        #many=True bitta emas, royxat degani
        # serializer = python obektlarini JSON ga tayyorlaydi
        return Response(serializer.data)

    def post(self, request):# post → POST so'rovi kelganda ishlaydi, masalan: yangi muallif qo'shganda
        serializer = AuthorSerializer(data=request.data) # request.data → frontenddan kelgan JSON ma'lumot
        if serializer.is_valid(): # is_valid() → ma'lumot to'g'rimi tekshiradi, name bo'shmi, juda qisqami va h.k.
            serializer.save() # to'g'ri bo'lsa DB ga saqlaydi
            return Response(serializer.data, status=status.HTTP_201_CREATED)# 201 → "muvaffaqiyatli yaratildi" degani
            # serializer.data → yangi yaratilgan muallif ma'lumoti
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # is_valid() False bo'lsa bu ishlaydi
    # serializer.errors → nima xato ekanini ko'rsatadi
    # 400 → "xato ma'lumot yuborildi" degani



# Detail → bitta obyekt bilan ishlash uchun
# GET (ko'rish), PUT (yangilash), DELETE (o'chirish)
class AuthorDetailAPIVew(APIView):
    def get_object(self, pk):
        # get_object → yordamchi method
        # GET, PUT, DELETE hammasi bitta muallifni topadi
        # takrorlamaslik uchun alohida method qilingan
        return get_object_or_404(Author, pk=pk)   # pk bo'yicha muallifni topadi, topilmasa 404

    def get(self, request, pk): # pk → URL dagi raqam, masalan /api/authors/3/ → pk=3
        author = self.get_object(pk)
        # self.get_object() → yuqoridagi yordamchi methodni chaqiradi
        # self → bu klassning o'zi
        serializer = AuthorSerializer(author)
        # bitta obyekt → many=True kerak emas
        return Response(serializer.data)
        # {"id": 3, "name": "Abdulla Qodiriy"}


    def post(self, request): #POST sorovi kelganda ishlaydi, maslan yangi muallif qoshganda
        serializer = AuthorSerializer(data=request.data)
        #request.data = frontdan kelgan JSON malumot
        # data = yangi malumot rkanligini anglatadi
        if serializer.is_valid(): #malumot qoidagifrk togri kiritildimi yoqmi tekshiriladi
             serializer.save() #togri bolsa DB ga saqlaydi
             return Response(serializer.data, status=status.HTTP_201_CREATED)
             # 201 → "muvaffaqiyatli yaratildi" degani
             # serializer.data → yangi yaratilgan muallif ma'lumoti
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        author = self.get_object(pk)
        author.delete()
        return Response(
            {'xabar : Muallif ochirildi'},
            status=status.HTTP_204_NO_CONTENT
            # 204 → "muvaffaqiyatli o'chirildi, qaytariladigan ma'lumot yo'q"
        )


class BookListAPIVew(APIView):
    def get(self, request):
        books = Book.objects.select_related('author').all()
        # select_related('author') → kitob bilan birga muallifni ham
        # bitta SQL query da oladi
        # Bu olmasa: 100 kitob = 101 ta SQL query (sekin!)
        # Bu bilan: 100 kitob = 1 ta SQL query (tez!)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
         # [
         #   {"id":1, "title":"O'tkan kunlar",
         #    "author":1,
         #    "author_detail":{"id":1,"name":"Abdulla Qodiriy"}},
         #   ...
         # ]
    def post(self, request):
        serializer = BookSerializer(data=request.data) #frondan kelgan malumotni oladi
        if serializer.is_valid(): #hamma malumot togri kiritildimi tekshiradi
            serializer.save() #agar ha bolsa saqlaydi
            return Response(serializer.data, status=status.HTTP_201_CREATED)# shunda malumot yangi bolib saqlanadi
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)# agar if ga togri kelmasa serialazer xatoligini chiqaradi



class BookDetailAPIVew(APIView):
    def get_object(self, pk):
        return get_object_or_404(Book, pk=pk)

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk) #yangilanadigon kitobni topadi
        serializer = BookSerializer(book, data=request.data) #book=mavjud malumot edi, data=request.data yangi malumot
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return Response(
            {'xabar : kitob ochirildi'},
        )
    








