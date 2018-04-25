from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.
    
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        #Check date is not in past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

# Search Form template for views that only query keywords (no filters):
class KeywordSearchForm(forms.Form):
    keyword = forms.CharField(max_length=20,required=True)

    def clean(self):
        cleaned_data=super(KeywordSearchForm, self).clean()
        search_word=cleaned_data.get("keyword",None)
        if search_word == None:
            raise ValidationError("No Search")
