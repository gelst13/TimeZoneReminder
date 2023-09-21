from django import forms


class TimopForm1(forms.Form):
    # it is not inheriting from forms.ModelForm
    current_time = forms.CharField(label='current_time',
                                   max_length=50, required=False)
    calculate_time = forms.CharField(label='calculate_time',
                                     max_length=50, required=False)
    convert_local_time = forms.CharField(label='convert_local_time',
                                         max_length=50, required=False)
    convert_other_time = forms.CharField(label='convert_other_time',
                                         max_length=50, required=False)


class TimopForm2(forms.Form):
    # it is not inheriting from forms.ModelForm
    local_offset = forms.CharField(label='local_offset',
                                   max_length=50)
