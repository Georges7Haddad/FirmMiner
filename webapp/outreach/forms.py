from django import forms


class EmailForm(forms.Form):
    subject = forms.CharField(max_length=127)
    message = forms.CharField(max_length=127, widget=forms.Textarea)
    emails = forms.MultipleChoiceField(choices=())
    fields = [
        "emails",
        "subject",
        "message"
    ]
