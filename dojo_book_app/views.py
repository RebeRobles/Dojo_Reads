from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *




# Create your views here.


def book(request):
    if "usuario" not in request.session:
        return render(request, 'home.html')
    else:
        context={
            'books': Book.objects.all(),
            'reviews': Reviews.objects.all().order_by('-created_at')[:3],
            'book_with_reviews': Reviews.objects.all().order_by('-created_at')[3:],
        }
        return render(request, 'book.html', context)
    
def add(request):
    context={
        'authors': Author.objects.all(),
    }
    return render(request, 'add.html', context)
    

def create_book(request):
    if request.method == 'GET':
        return redirect('add') 
    else:
        if request.method == 'POST':
            user = User.objects.get(id=request.session['usuario']['id'])            
            book_title = request.POST['title']
            if str(request.POST['new_author']) != '':
                author = Author.objects.create(name=request.POST['new_author'])
                author.save()
            else:
                author = Author.objects.get(id=request.POST['author'])

            review = request.POST['review']
            rating = request.POST['rating']         
            obj_book = Book.objects.create(title=book_title, author=author, users=user)
            obj_book.save()
            obj_review = Reviews.objects.create(comment=review, rating=rating, user=user, book=obj_book)
            obj_review.save()
        return redirect(f"/book/{obj_book.id}")
        #return redirect('book')

def book_id(request, book_id):
    context = {
        'book' : Book.objects.get(id=book_id),
        'author' : Book.objects.get(id=book_id).author,
        'reviews': Book.objects.get(id=book_id).book_reviews.all(),
    }
    return render(request, 'info_book.html', context)

def user_id(request, user_id):
    book_list =[]
    review = Reviews.objects.filter(user__id=user_id)
    for rev in review:
        book_list.append(rev.book)
        
    context = {
        'user_id':User.objects.get(id=user_id),
        'books': book_list,
        'count_review': len(review)
    }
    return render(request, 'user.html', context)

def edit_review(request, book_id):
    
        book_id = request.POST['book_id']
        book= Book.objects.get(id=book_id)    
        user = User.objects.get(id=request.session['usuario']['id'])            
        comment = request.POST['comment']
        rating = request.POST['rating']
        obj_review = Reviews.objects.create(comment=comment, rating=rating, user=user, book=book)
        obj_review.save()
        return redirect(f'/book/{book.id}')    



    

def delete_review(request, review_id):
    review = Reviews.objects.get(id=review_id)
    book = review.book
    review.delete()
    return redirect(f'/book/{book.id}')




def logout(request):
    request.session.flush()
    return redirect('/')
