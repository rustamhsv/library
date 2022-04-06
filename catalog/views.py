from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre
from django.views import generic


# Create your views here.
def index(request):
    """View function for home page"""

    # Calculate counts of main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Num of available books in library
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Num of authors
    num_authors = Author.objects.count()

    # animal = Book.objects.filter(title__icontains='Pride').count()
    # print(animal)

    # Calc number of visits to this view with session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

    """If we want to override"""
    # context_object_name = 'book_list'
    # queryset = Book.objects.filter(title__icontains='war')[:5]  # return top 5 movies with 'war' in title
    # template_name = 'books/my_arbitrary_template_name_list.html'
    #
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5]  # return top 5 movies with 'war' in title

    """override context data"""
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    # paginate_by = 2


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).\
            filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_all.html"
    permission_required = "catalog.can_mark_returned"

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

