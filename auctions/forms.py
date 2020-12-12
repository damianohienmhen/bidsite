from .models import Comment, AuctionListing
from django import forms



class CommentForm(forms.ModelForm):
    new_comment = forms.CharField(label ="", widget = forms.Textarea( 
    attrs ={ 
        'class':'form-control', 
        'placeholder':'Comment here !', 
        'rows':4, 
        'cols':50}))
    class Meta:
        model = Comment
        fields = ['new_comment']

class NewListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['listname','image', 'description', 'price', 'category']
        
    