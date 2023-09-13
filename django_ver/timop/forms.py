from django import forms


class TimopForm1(forms.Form):
    # it is not inheriting from forms.ModelForm
    current_time = forms.CharField(label='current_time', max_length=50, required=False)
    # convert_local_time = forms.CharField(max_length=50, required=False)
    # convert_other_time = forms.CharField(max_length=50, required=False)
