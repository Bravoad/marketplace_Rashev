from  .models import Category

def list_category(request):
    return  {'categories':Category.objects.all()}