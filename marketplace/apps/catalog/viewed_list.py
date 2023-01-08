from decimal import Decimal
from django.conf import settings
from models import Product

class Viewed_list:

    def __init__(self, request):
        self.session = request.session
        viewed = self.session.get(settings.VIEWED_SESSION_ID)
        if not viewed:
            # save an empty cart in the session
            viewed = self.session[settings.VIEWED_SESSION_ID] = {}
        self.viewed = viewed

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.viewed:
            self.viewed[product_id] = {'name':str(product.name),
                                       'price': str(product.price)}
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.VIEWED_SESSION_ID] = self.viewed
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.viewed:
            del self.viewed[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.viewed.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.viewed[str(product.id)]['product'] = product

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.VIEWED_SESSION_ID]
        self.session.modified = True
