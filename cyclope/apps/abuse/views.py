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
    ct = ContentType.objects.get_for_id(ct_id)
    obj = ct.get_object_for_this_type(pk=obj_id)
    # already reported by this user
    if AbuseReportElement.objects.filter(user=request.user, object_id=obj_id,
                                          content_type=ct):
        return render(request, "abuse/report.html", {"already_reported": True, "content": obj})

    if request.method == "POST":
        form = ReportElementForm(request.POST)
        if form.is_valid():
            report_el = form.save(commit=False)
            report_el.content_object = obj
            report_el.user = request.user
            report_el.save()
            return render(request, "abuse/report.html", {"content": obj})
    else:
        form = ReportElementForm()

    return render(request, "abuse/report.html", {
                "form": form,
            })
