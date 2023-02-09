from django.contrib import admin
from .models import Product,Review,Category,Gallery,Attributes,Sale,Tags
# Register your models here.


class ReviewInline(admin.TabularInline):
    model = Review


class AttributesInline(admin.TabularInline):
    model = Attributes


class GalleryInline(admin.TabularInline):
    model = Gallery
class TagsInline(admin.TabularInline):
    model = Tags
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ReviewInline,AttributesInline,GalleryInline,TagsInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','comment')
    actions = [ 'delete_administration']

    def delete_administration(self, request, queryset):
        queryset.update(comment='отзыв удален администратором')

    delete_administration.short_description = 'Удалить отзыв'


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    pass


@admin.register(Attributes)
class AttributesAdmin(admin.ModelAdmin):
    pass
