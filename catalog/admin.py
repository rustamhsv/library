from django.contrib import admin
from .models import Book, Genre, Author, BookInstance, Language

# Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


# Define the admin class
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
        list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]


# Define the admin class
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # list_display = ('title', 'author')

    list_display = ('title', 'author', 'display_genre')

    inlines = [BookInstanceInline]


# Define the admin class
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('display_book_title', 'status', 'due_back', 'id')

    # add filters to book instances
    list_filter = ('status', 'due_back')

    # add fieldsets
    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id')}),
        ('Availability', {'fields': ('status', 'due_back')})
    )

