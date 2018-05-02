from django.shortcuts import render, redirect
from .models import Book, Author, BookInstance, Genre, Cart
from django.contrib.auth.models import User
from profiles.models import Profile
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm, KeywordSearchForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

from django.views.generic import ListView
from django.http import HttpResponse

from django.db.models import Q

import decimal

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    """
    View function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors, 'num_visits':num_visits},
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    form_class = KeywordSearchForm
    search_error = False
    query_keyword = None

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            self.query_keyword = form.cleaned_data['keyword']
            obj_list  = Book.objects.filter(   
                                                (
                                                    Q(title__icontains=form.cleaned_data['keyword'])
                                                )
                                            ).order_by('title')
            # If search results return empty, raise error flag:
            if not obj_list: self.search_error = True
            return obj_list
        return Book.objects.all()

    # Pass error flag to prompt search error
    def get_context_data(self, **kwargs):
        context=super(BookListView, self).get_context_data(**kwargs)
        context['search_error']=self.search_error
        context['query_keyword']=self.query_keyword
        return context
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

    form_class = KeywordSearchForm
    search_error = False
    query_keyword = None

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        if form.is_valid():
            self.query_keyword = form.cleaned_data['keyword']
            obj_list  = Author.objects.filter(   
                                                (
                                                    Q(first_name__icontains=form.cleaned_data['keyword']) |
                                                    Q(last_name__icontains=form.cleaned_data['keyword'])
                                                )
                                            ).order_by('last_name')
            # If search results return empty, raise error flag:
            if not obj_list: self.search_error = True
            return obj_list
        return Author.objects.all()



class AuthorDetailView(generic.DetailView):
    model = Author

class AuthorCreate(PermissionRequiredMixin, CreateView):
	current_date = datetime.datetime.now()
	current_date_formatted = current_date.strftime('%m/%d/%Y')
	model = Author
	fields = '__all__'
	initial={'date_of_death':current_date_formatted,}
	permission_required = 'ecommerce.can_add_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
	model = Author
	fields = ['first_name','last_name','date_of_birth','date_of_death']
	permission_required = 'ecommerce.can_change_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
	model = Author
	success_url = reverse_lazy('authors')
	permission_required = 'ecommerce.can_delete_author'

class BookCreate(PermissionRequiredMixin, CreateView):
	model = Book
	fields = '__all__'
	permission_required = 'ecommerce.can_add_book'

class BookAddInstance(PermissionRequiredMixin, CreateView):
    model = BookInstance
    fields = '__all__'
    permission_required = 'ecommerce.can_add_book'
    success_url = reverse_lazy('books')

class BookUpdate(PermissionRequiredMixin, UpdateView):
	model = Book
	fields = '__all__'
	permission_required = 'ecommerce.can_change_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
	model = Book
	success_url = reverse_lazy('books')
	permission_required = 'ecommerce.can_delete_book'

class BookPurchase(LoginRequiredMixin, TemplateView):
	template_name = "book_page.html"

@login_required
def CartView(request):

    books = Book.objects.all()

    books_owned = request.user.profile.bookinstance_set

    total_price = 0
    texas_tax = 0.0825

    owned_books = []
    for book in books_owned.all():
        owned_books.append(book)
        total_price = total_price + book.price

    tax = round(total_price * decimal.Decimal(texas_tax),2)
    total_price_with_tax = total_price + tax

    return render(
        request,
        'book_cart.html',
        context = {'books': books,
                    'owned_books': owned_books,
                    'total_price': total_price,
                    'total_price_with_tax': total_price_with_tax,
                    'tax': tax}
    )

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='ecommerce/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
    """
    model = BookInstance
    permission_required = 'ecommerce.can_mark_returned'
    template_name ='ecommerce/bookinstance_list_borrowed_all.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')  

@permission_required('ecommerce.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'ecommerce/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

@login_required
def borrow_book(request, book_id):
    book_instance = get_object_or_404(BookInstance, pk=book_id)
    book_instance.status = 'o' 

    # set due date 3 weeks from borrow date
    current_time = datetime.datetime.now()
    three_week_offset = datetime.timedelta(days=21)
    due_date = current_time + three_week_offset

    book_instance.due_back = due_date
    book_instance.borrower = request.user
    book_instance.save()

    return HttpResponseRedirect(reverse('my-borrowed'))

@login_required
def add_to_cart(request, book_id):
    book_instance = get_object_or_404(BookInstance, pk=book_id)
    book_instance.status = 'r' 

    book_instance.owner = request.user.profile
    book_instance.save()

    return HttpResponseRedirect(reverse('cart'))

@login_required
def remove_from_cart(request, book_id):
    book_instance = get_object_or_404(BookInstance, pk=book_id)
    book_instance.status = 'a'

    book_instance.owner = None
    book_instance.save()

    return HttpResponseRedirect(reverse('cart'))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

class ProfileCheckout(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'address', 'city', 'state', 'zip_code', 'phone_number']

    success_url = reverse_lazy('success')

    def get_context_data(self, **kwargs):
        context = super(ProfileCheckout, self).get_context_data(**kwargs)

        books = Book.objects.all()

        books_owned = self.request.user.profile.bookinstance_set

        total_price = 0
        texas_tax = 0.0825

        owned_books = []
        for book in books_owned.all():
            owned_books.append(book)
            total_price = total_price + book.price

        tax = round(total_price * decimal.Decimal(texas_tax),2)
        total_price_with_tax = total_price + tax

        context['books'] = books
        context['owned_books'] = owned_books
        context['total_price'] = total_price
        context['total_price_with_tax'] = total_price_with_tax
        context['tax'] = tax

        return context

@login_required
def success_page(request):
    books = Book.objects.all()

    books_owned = request.user.profile.bookinstance_set

    for book in books_owned.all():
        book.delete()

    return render(
        request,
        'success_page.html',
        context = {}
    )
