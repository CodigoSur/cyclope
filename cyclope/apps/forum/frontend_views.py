#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2010 Código Sur - Nuestra América Asoc. Civil / Fundación Pacificar.
# All rights reserved.
#
# This file is part of Cyclope.
#
# Cyclope is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cyclope is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.http import urlquote

from cyclope.core import frontend
from cyclope import views
from cyclope.core.collections.models import Category

from models import Topic
from forms import CreateTopicForm


class TopicDetail(frontend.FrontendView):
    name = 'detail'
    verbose_name= _('detailed view of the selected Topic')
    is_default = True
    is_instance_view = True
    is_content_view = True

    def get_response(self, request, host_template, content_object):

        try:
            profile = content_object.author.get_profile()
            avatar = profile.avatar
        except ObjectDoesNotExist:
            avatar = None

        context = {'avatar': avatar}
        return views.object_detail(request, host_template, content_object,
                                   extra_context=context)

frontend.site.register_view(Topic, TopicDetail)

class CreateTopic(frontend.FrontendView):
    name = 'create-topic'
    verbose_name = _('create a new topic in the Forum selected')
    is_instance_view = True
    is_content_view = True

    def get_response(self, request, host_template, content_object):
        if not request.user.is_authenticated():
            from django.conf import settings
            tup = (settings.LOGIN_URL, REDIRECT_FIELD_NAME,
                   urlquote(request.get_full_path()))
            return HttpResponseRedirect('%s?%s=%s' % tup)
        category = content_object

        context = {'forum': category.name}

        topic_ctype = ContentType.objects.get_for_model(Topic)
        if topic_ctype not in category.collection.content_types.all():
            not_allowed = True
            form = None
        else:
            not_allowed = False
            if request.method == 'POST':
                form = CreateTopicForm(data=request.POST)
                if form.is_valid():
                    # partial save
                    topic = form.save(commit=False)
                    topic.author = request.user
                    topic.allow_comments = 'YES'
                    topic.save()
                    # category added
                    topic.categories.get_or_create(category=category,
                                    defaults={'category': category,
                                              'content_type_id': topic_ctype.id,
                                              'object_id': topic.id})
                    topic.save()
                    return redirect(topic)
            else:
                form = CreateTopicForm()

        context.update({'form': form,
                        'not_allowed': not_allowed,
                        'action_url': reverse('category-create-topic',
                                               args=[category.slug]),
                       })

        return views.object_detail(request, host_template, content_object,
                                   view_name = self.name, extra_context=context)

frontend.site.register_view(Category, CreateTopic)
