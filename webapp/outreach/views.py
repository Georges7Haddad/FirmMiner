import django_filters
from django.forms import MultipleChoiceField
from django.shortcuts import render, redirect
from django.core.mail import send_mass_mail

from .forms import EmailForm
from .models import Firm, Ranking, Attorney
from ..webapp.settings import EMAIL_HOST_USER


class FirmFilter(django_filters.FilterSet):
    top_tier_firm_rankings = django_filters.filters.ModelChoiceFilter(queryset=Ranking.objects.all().order_by("name"))
    firm_rankings = django_filters.filters.ModelChoiceFilter(queryset=Ranking.objects.all().order_by("name"))

    class Meta:
        model = Firm
        fields = {
            "name": ["icontains"],
            "address": ["icontains"],
        }


def firms_table_view(request):
    firms = FirmFilter(request.GET, queryset=Firm.objects.all())
    return render(request, "table.html", {"firms": firms})


def attorneys_view(request, firm_name):
    firm_name = firm_name.replace("%20", "")
    firm = Firm.objects.get(name__icontains=firm_name)
    attorneys = Attorney.objects.filter(firm_name__name__icontains=firm_name)
    if request.method == "POST":
        email_form = EmailForm(request.POST)
        subject = email_form.data["subject"]
        recipients = email_form.data.getlist("emails")
        if not recipients:
            recipients = [firm.email]
        message = email_form.data["message"]
        messages = ((subject, message, EMAIL_HOST_USER, [email]) for email in recipients)
        send_mass_mail(messages, fail_silently=False)
        return redirect("/")
    email_form = EmailForm()
    email_form.fields['emails'] = MultipleChoiceField(
        choices=((attorney.email, attorney.email) for attorney in attorneys), required=False)
    return render(request, "attorneys.html", {"attorneys": attorneys, "firm": firm, "email_form": email_form})
