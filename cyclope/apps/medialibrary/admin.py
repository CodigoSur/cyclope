#!/usr/bin/env python
# -*- coding: UTF-8 -*-
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


from django.contrib import admin

from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin

from models import *

class MediaAdmin(CollectibleAdmin, BaseContentAdmin):
    inlines = CollectibleAdmin.inlines + BaseContentAdmin.inlines

admin.site.register(Picture, MediaAdmin)
admin.site.register(SoundTrack, MediaAdmin)
admin.site.register(MovieClip, MediaAdmin)
admin.site.register(Document, MediaAdmin)
admin.site.register(FlashMovie, MediaAdmin)
admin.site.register(RegularFile, MediaAdmin)
admin.site.register(ExternalContent, MediaAdmin)
