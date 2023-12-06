from django.forms import ModelForm
from .models import listing

class listingForm(ModelForm):
    class Meta:
        model = listing
        fields = ['name', 'desc', 'image', 'category', 'starting_price']