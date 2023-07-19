from django.forms import ModelForm
from django.core.exceptions import NON_FIELD_ERRORS
from .models import Scan
class ScanForm(ModelForm):
    class Meta:
        model = Scan
        fields = ['title',]
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }
