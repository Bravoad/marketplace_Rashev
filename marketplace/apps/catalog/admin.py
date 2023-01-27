from django.contrib import admin
from .models import Product,Review,Category
# Register your models here.


class ReviewInline(admin.TabularInline):
    model = Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','comment')
    actions = [ 'delete_administration']

    def delete_administration(self, request, queryset):
        queryset.update(comment='отзыв удален администратором')

    delete_administration.short_description = 'Удалить отзыв'
