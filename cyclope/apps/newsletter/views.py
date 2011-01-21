from string import strip
from premailer import Premailer

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


def _newsletter_html(request, newsletter):
    category = newsletter.content_category
    template_name = cyc_settings.CYCLOPE_THEME_PREFIX + newsletter.layout.template
    nl_template = loader.get_template(template_name)
    categorizations_list = category.categorizations.all()
    categorizations_list = sorted(categorizations_list,
                                  key=lambda c: c.object_modification_date,
                                  reverse=True)
    
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

    # some of these are the default parameters but we include them in case some tunning is needed later on. Premailer documentation is scarce
    pm = Premailer(_newsletter_html(request, newsletter),
                   base_url=cyc_settings.CYCLOPE_BASE_URL,
                   exclude_pseudoclasses=False,
                   keep_style_tags=False, include_star_selectors=False,
                   external_styles=None)
    result = pm.transform()
    return HttpResponse(result)


@permission_required('newsletter.can_modify')
def send(request, id, test=False):
    newsletter = Newsletter.objects.get(id=id)
    subject = newsletter.name
    pm = Premailer(_newsletter_html(request, newsletter),
                   base_url=cyc_settings.CYCLOPE_BASE_URL)
    html_message = pm.transform()
    sender = newsletter.sender
    if test:
        recipients = map(strip, newsletter.test_recipients.split(','))
    else:
        recipients = map(strip, newsletter.recipients.split(','))

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

    
