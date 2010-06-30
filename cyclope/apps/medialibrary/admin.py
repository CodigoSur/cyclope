# -*- coding: utf-8 -*-

from django.contrib import admin

from cyclope.core.collections.admin import CollectibleAdmin

from models import *

class MediaAdmin(CollectibleAdmin):
    pass

admin.site.register(Picture, MediaAdmin)
admin.site.register(SoundTrack, MediaAdmin)
admin.site.register(MovieClip, MediaAdmin)
admin.site.register(Document, MediaAdmin)
admin.site.register(FlashMovie, MediaAdmin)
admin.site.register(RegularFile, MediaAdmin)
admin.site.register(ExternalContent, MediaAdmin)
