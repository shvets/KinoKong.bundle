# -*- coding: utf-8 -*-

ART = 'art-default.jpg'
ICON = 'icon-default.png'

PREFIX = '/video/kinokong'

import library_bridge

library_bridge.bridge.export_object('L', L)
library_bridge.bridge.export_object('R', R)
library_bridge.bridge.export_object('Log', Log)
library_bridge.bridge.export_object('Resource', Resource)
library_bridge.bridge.export_object('Datetime', Datetime)
library_bridge.bridge.export_object('Core', Core)
library_bridge.bridge.export_object('Prefs', Prefs)
library_bridge.bridge.export_object('Locale', Locale)
library_bridge.bridge.export_object('Callback', Callback)
library_bridge.bridge.export_object('AudioCodec', AudioCodec)
library_bridge.bridge.export_object('VideoCodec', VideoCodec)
library_bridge.bridge.export_object('AudioStreamObject', AudioStreamObject)
library_bridge.bridge.export_object('VideoStreamObject', VideoStreamObject)
library_bridge.bridge.export_object('DirectoryObject', DirectoryObject)
library_bridge.bridge.export_object('PartObject', PartObject)
library_bridge.bridge.export_object('MediaObject', MediaObject)
library_bridge.bridge.export_object('EpisodeObject', EpisodeObject)
library_bridge.bridge.export_object('TVShowObject', TVShowObject)
library_bridge.bridge.export_object('MovieObject', MovieObject)
library_bridge.bridge.export_object('TrackObject', TrackObject)
library_bridge.bridge.export_object('VideoClipObject', VideoClipObject)
library_bridge.bridge.export_object('MessageContainer', MessageContainer)
library_bridge.bridge.export_object('Container', Container)

import plex_util

from kino_kong_plex_service import KinoKongPlexService

service = KinoKongPlexService()

import main

def Start():
    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
    Plugin.AddViewGroup('PanelStream', viewMode='PanelStream', mediaType='items')
    Plugin.AddViewGroup('MediaPreview', viewMode='MediaPreview', mediaType='items')

    DirectoryObject.art = R(ART)
    VideoClipObject.art = R(ART)

    # HTTP.CacheTime = CACHE_1HOUR

    plex_util.validate_prefs()

@handler(PREFIX, unicode(L('Title')), R(ART), R(ICON))
def MainMenu():
    if not service.available():
        return MessageContainer(L('Error'), L('Service not avaliable'))

    oc = ObjectContainer(title2=unicode(L('Title')), no_cache=True)

    oc.add(DirectoryObject(key=Callback(main.HandleAllMovies), title=unicode(L('Movies'))))
    oc.add(DirectoryObject(key=Callback(main.HandleNewMovies), title=unicode(L('New Movies'))))
    oc.add(DirectoryObject(key=Callback(main.HandleAllSeries), title=unicode(L('Series'))))
    oc.add(DirectoryObject(key=Callback(main.HandleAnimation), title=unicode(L('Animation'))))
    oc.add(DirectoryObject(key=Callback(main.HandleAnime), title=unicode(L('Anime'))))
    oc.add(DirectoryObject(key=Callback(main.HandleTvShows), title=unicode(L('TV Shows'))))
    oc.add(DirectoryObject(key=Callback(main.HandleAllGenres), title=unicode(L('Genres'))))
    oc.add(DirectoryObject(key=Callback(main.HandleTops), title=unicode(L('Top'))))
    oc.add(DirectoryObject(key=Callback(main.HandleHistory), title=unicode(L('History'))))
    oc.add(DirectoryObject(key=Callback(main.HandleQueue), title=unicode(L('Queue'))))

    oc.add(InputDirectoryObject(
        key=Callback(main.HandleSearch),
        title=unicode(L('Search')), prompt=unicode(L('Search on KinoKong.net'))
    ))

    return oc
