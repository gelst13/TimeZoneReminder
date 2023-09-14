from django import forms


class TimopForm1(forms.Form):
    # it is not inheriting from forms.ModelForm
    current_time = forms.CharField(label='current_time',
                                   max_length=50, required=False)


class TimopForm2(forms.Form):
    # it is not inheriting from forms.ModelForm
    convert_local_time = forms.CharField(label='convert_local_time',
                                         max_length=50, required=False)


class TimopForm3(forms.Form):
    # it is not inheriting from forms.ModelForm
    convert_other_time = forms.CharField(label='convert_other_time',
                                         max_length=50, required=False)
