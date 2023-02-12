from decimal import Decimal
from django.conf import settings
from .models import Product


class Viewed_list:

    def __init__(self, request):
        self.session = request.session
        viewed = self.session.get(settings.VIEWED_SESSION_ID)
        if not viewed:
            viewed = self.session[settings.VIEWED_SESSION_ID] = {}
        self.viewed = viewed

    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.viewed:
            self.viewed[product_id] = {
                'price': str(product.price)
            }
        self.save()

    def save(self):
        self.session[settings.VIEWED_SESSION_ID] = self.viewed
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.viewed:
            del self.viewed[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.viewed.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.viewed[str(product.id)]['product'] = product
        for item in self.viewed.values():
            item['price'] = Decimal(item['price'])
            yield item

    def clear(self):
        # очищение просмотров из сессии
        del self.session[settings.VIEWED_SESSION_ID]
        self.session.modified = True
