# -*- coding: utf-8 -*-

from django.contrib import admin

from cyclope.core.collections.admin import CollectibleAdmin
from cyclope.admin import BaseContentAdmin

from models import *

class MediaAdmin(CollectibleAdmin, BaseContentAdmin):
    pass

admin.site.register(Picture, MediaAdmin)
admin.site.register(SoundTrack, MediaAdmin)
admin.site.register(MovieClip, MediaAdmin)
admin.site.register(Document, MediaAdmin)
admin.site.register(FlashMovie, MediaAdmin)
admin.site.register(RegularFile, MediaAdmin)
