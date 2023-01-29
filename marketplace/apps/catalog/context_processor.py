from  .models import Category

def list_category(request):
    return  {'categories':Category.objects.filter(parent_category=None)}