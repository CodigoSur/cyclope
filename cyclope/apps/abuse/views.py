from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from cyclope.utils import CrispyFormsSimpleMixin
from models import AbuseReportElement


class ReportElementForm(forms.ModelForm, CrispyFormsSimpleMixin):
    class Meta:
        model = AbuseReportElement
        fields = ('abuse_type', 'text')


@login_required
def abuse_report(request, ct_id, obj_id):
    #TODO: validate unique of user, ct_id, obj_id
    if request.method == "POST":
        form = ReportElementForm(request.POST)
        if form.is_valid():
            report_el = form.save(commit=False)
            klass = ContentType.objects.get(pk=ct_id).model_class()
            report_el.content_object = klass.objects.get(pk=obj_id)
            report_el.user = request.user
            report_el.save()
            return render(request, "abuse/report.html", {"content": report_el.content_object})
    else:
        form = ReportElementForm()

    return render(request, "abuse/report.html", {
                "form": form,
            })
