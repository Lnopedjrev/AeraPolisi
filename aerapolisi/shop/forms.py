from django import forms

from captcha.fields import CaptchaField

from .models import ProductCategory, ShippingAdress, Products


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductPurchaseForm(forms.ModelForm):
    discord = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()
    number = forms.IntegerField(min_value=1)
    address = forms.CharField(max_length=200, required=False)
    city = forms.CharField(max_length=200, required=False)
    state = forms.CharField(max_length=200, required=False)

    class Meta:
        model = ShippingAdress
        fields = '__all__'


try:
    cagors = ProductCategory.objects.all()
    CHOICES1 = [(c.name, c.name.lower()) for c in cagors]
except Exception as e:
    print(e)
    CHOICES1 = []



class FilterProductForm(forms.Form):

    CHOICES2 = [('Service', 'Service'), ('Products', 'Products')]
    categories = forms.MultipleChoiceField(choices=CHOICES1, required=False)
    name = forms.CharField(max_length=200, required=False)
    is_service = forms.ChoiceField(widget=forms.RadioSelect,
                                   choices=CHOICES2,
                                   required=False)
    minprice = forms.FloatField()
    maxprice = forms.FloatField()
    seller_name = forms.CharField(max_length=200, required=False)

    class Meta:
        fields = '__all__'


class SupposeProductForm(forms.ModelForm):
    images = MultipleFileField()
    captcha = CaptchaField()
    price = forms.FloatField(min_value=0.1)

    class Meta:
        model = Products
        fields = ('name', 'description', 'images', 'quantity',
                  'price', 'service', 'categories', 'captcha')


class ShippingChangeForm(forms.ModelForm):
    number = forms.IntegerField(min_value=1)

    class Meta:
        model = ShippingAdress
        fields = ('address', 'city', 'state', 'zipcode', 'number')
