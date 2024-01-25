from django.forms import ModelForm
from .models import listing, bid, comment

class listingForm(ModelForm):
    class Meta:
        model = listing
        fields = ['name', 'desc', 'image','image_url', 'category', 'starting_price']


class bidForm(ModelForm):
    class Meta:
        model = bid
        fields = ['bid_amount']


class commentForm(ModelForm):
    class Meta:
        model = comment
        fields = ['comment']