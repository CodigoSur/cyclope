#!/usr/bin/env python
# -*- coding: utf-8 -*-

from haystack import indexes
from cyclope.apps.medialibrary import models

class BaseMediaIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True) #template: author, description
    author = indexes.CharField(model_attr='author', null=True)

class PictureIndex(BaseMediaIndex, indexes.Indexable):
    def get_model(self):
        return models.Picture

class SoundTrackIndex(BaseMediaIndex, indexes.Indexable):
    def get_model(self):
        return models.SoundTrack

class MovieClipIndex(BaseMediaIndex, indexes.Indexable):
    def get_model(self):
        return models.MovieClip

class DocumentIndex(BaseMediaIndex, indexes.Indexable):
    def get_model(self):
        return models.Document

class FlashMovieIndex(BaseMediaIndex, indexes.Indexable):
    def get_model(self):
        return models.FlashMovie

class RegularFileIndex(BaseMediaIndex, indexes.Indexable):
    def get_model(self):
        return models.RegularFile

class ExternalContentIndex(BaseMediaIndex, indexes.Indexable):
    def get_model(self):
        return models.ExternalContent
