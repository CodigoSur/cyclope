from string import strip

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import permission_required
from django.template import loader
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cyclope.core import frontend
from cyclope import settings as cyc_settings
from cyclope.core.collections.models import Category
from models import Newsletter


def _newsletter_html(newsletter, request):
    template_name = cyc_settings.CYCLOPE_THEME_PREFIX + newsletter.layout.template
    nl_template = loader.get_template(template_name)
    categorizations_list = newsletter.content_category.categorizations.all()
    categorizations_list = sorted(categorizations_list,
                                  key=lambda c: c.object_modification_date,
                                  reverse=True)
    
    contents = newsletter.content_category
    context = RequestContext(request, {'host_template': nl_template,
                                       'layout': newsletter.layout,
                                       'newsletter': newsletter,
                                       'categorizations': categorizations_list,
                                       })
    content_view = frontend.site.get_view(Newsletter, newsletter.view)
    html = content_view.get_response(request, context, newsletter)
    return html


@permission_required('newsletter.can_modify')
def preview(request, id):
    newsletter = Newsletter.objects.get(id=id)
    result = _newsletter_html(newsletter, request)
    return HttpResponse(result)


@permission_required('newsletter.can_modify')
def send(request, id, test=False):
    nl = Newsletter.objects.get(id=id)    
    subject = nl.name
    html_message = _newsletter_html(nl, request)
    sender = nl.sender
    if test:
        recipients = map(strip, nl.test_recipients.split(','))
    else:
        recipients = map(strip, nl.recipients.split(','))

    msg = EmailMessage(subject, html_message, sender, recipients)
    msg.content_subtype = "html"
    try:
        msg.send()
    except:
        return HttpResponseRedirect(reverse('newsletter_failed', args=[id]))
    else:    
        return HttpResponseRedirect(reverse('newsletter_sent', args=[id]))

@permission_required('newsletter.can_modify')
def sent(request, id, test=False):
    t = loader.get_template("newsletter/mail_sent.html")
    newsletter = Newsletter.objects.get(id=id)
    c = RequestContext(request, {'newsletter': newsletter,})
    return HttpResponse(t.render(c))

@permission_required('newsletter.can_modify')
def failed(request, id, test=False):
    t = loader.get_template("newsletter/send_failed.html")
    newsletter = Newsletter.objects.get(id=id)
    c = RequestContext(request, {'newsletter': newsletter,})
    return HttpResponse(t.render(c))

    
