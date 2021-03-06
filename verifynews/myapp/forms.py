from django import forms
from verifynews.myapp.models import Image, User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit



class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',) #must be tuple not string hence the , 


class UserForm(forms.ModelForm):


    class Meta:
        model=User
        fields=('phone',) 
    


class ImageAdminForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('category','title','description',)

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.helper = FormHelper()
        #     self.helper.form_id = 'id-exampleForm'
        #     self.helper.form_class = 'blueForms'
        #     self.helper.form_method = 'post'
        #     self.helper.form_action = 'submit_survey'

        #     self.helper.add_input(Submit('submit', 'Submit'))