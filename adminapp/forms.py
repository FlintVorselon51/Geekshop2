from django import forms
from django.db import connection
from django.db.models import F

from authapp.models import ShopUser
from authapp.forms import ShopUserEditForm
from mainapp.models import ProductCategory

from mainapp.models import Product


def db_profile_by_type(prefix, t, queries):
    update_queries = list(filter(lambda x: t in x['sql'], queries))
    print(f'db_profile {t} for {prefix}:')
    [print(query['sql']) for query in update_queries]


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'
        
        
class ProductCategoryEditForm(forms.ModelForm):
    discount = forms.IntegerField(label='скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ProductCategoryEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''

    def form_valid(self, form):
        discount = form.cleaned_data['discount']
        if discount:
            self.object.product_set.update(price=F('price') * (1 - discount / 100))
            db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

            
            
class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ProductEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''