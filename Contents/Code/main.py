# -*- coding: utf-8 -*-

import json
import plex_util
import pagination
import history
from flow_builder import FlowBuilder
from media_info import MediaInfo

builder = FlowBuilder()

@route(PREFIX + '/all_movies')
def HandleAllMovies(page=1):
    oc = ObjectContainer(title2=unicode(L('Movies')))

    response = service.get_all_movies(page=page)

    for item in response['movies']:
        name = item['name']
        thumb = item['thumb']

        new_params = {
            'type': "movie",
            'id' :item['path'],
            'name': item['name'],
            'thumb': item['thumb']
        }
        oc.add(DirectoryObject(
            key=Callback(HandleMovie, **new_params),
            title=plex_util.sanitize(name),
            thumb=plex_util.get_thumb(thumb)
        ))

    #pagination.append_controls(oc, response, callback=HandleMovies, path=path, title=title, page=page)

    return oc

@route(PREFIX + '/new_movies')
def HandleNewMovies(page=1):
    oc = ObjectContainer(title2=unicode(L('New Movies')))

    response = service.get_new_movies(page=page)

    for item in response['movies']:
        name = item['name']
        thumb = item['thumb']

        new_params = {
            'type': "movie",
            'id' :item['path'],
            'name': item['name'],
            'thumb': item['thumb']
        }
        oc.add(DirectoryObject(
            key=Callback(HandleMovie, **new_params),
            title=plex_util.sanitize(name),
            thumb=plex_util.get_thumb(thumb)
        ))

    #pagination.append_controls(oc, response, callback=HandleMovies, path=path, title=title, page=page)

    return oc

@route(PREFIX + '/series')
def HandleSeries(page=1):
    oc = ObjectContainer(title2=unicode(L('Series')))

    response = service.get_series(page=page)

    for item in response['movies']:
        name = item['name']
        thumb = item['thumb']

        new_params = {
            'type': "movie",
            'id' :item['path'],
            'name': item['name'],
            'thumb': item['thumb']
        }
        oc.add(DirectoryObject(
            key=Callback(HandleMovie, **new_params),
            title=plex_util.sanitize(name),
            thumb=plex_util.get_thumb(thumb)
        ))

    #pagination.append_controls(oc, response, callback=HandleMovies, path=path, title=title, page=page)

    return oc

@route(PREFIX + '/animation')
def HandleAnimation(page=1):
    oc = ObjectContainer(title2=unicode(L('Animation')))

    response = service.get_animation(page=page)

    for item in response['movies']:
        name = item['name']
        thumb = item['thumb']

        new_params = {
            'type': "movie",
            'id' :item['path'],
            'name': item['name'],
            'thumb': item['thumb']
        }
        oc.add(DirectoryObject(
            key=Callback(HandleMovie, **new_params),
            title=plex_util.sanitize(name),
            thumb=plex_util.get_thumb(thumb)
        ))

    #pagination.append_controls(oc, response, callback=HandleMovies, path=path, title=title, page=page)

    return oc

@route(PREFIX + '/anime')
def HandleAnime(page=1):
    oc = ObjectContainer(title2=unicode(L('Anime')))

    response = service.get_anime(page=page)

    for item in response['movies']:
        name = item['name']
        thumb = item['thumb']

        new_params = {
            'type': "movie",
            'id' :item['path'],
            'name': item['name'],
            'thumb': item['thumb']
        }
        oc.add(DirectoryObject(
            key=Callback(HandleMovie, **new_params),
            title=plex_util.sanitize(name),
            thumb=plex_util.get_thumb(thumb)
        ))

    #pagination.append_controls(oc, response, callback=HandleMovies, path=path, title=title, page=page)

    return oc

@route(PREFIX + '/tv_shows')
def HandleTvShows(page=1):
    oc = ObjectContainer(title2=unicode(L('TV Shows')))

    response = service.get_tv_shows(page=page)

    for item in response['movies']:
        name = item['name']
        thumb = item['thumb']

        new_params = {
            'type': "movie",
            'id' :item['path'],
            'name': item['name'],
            'thumb': item['thumb']
        }
        oc.add(DirectoryObject(
            key=Callback(HandleMovie, **new_params),
            title=plex_util.sanitize(name),
            thumb=plex_util.get_thumb(thumb)
        ))

    #pagination.append_controls(oc, response, callback=HandleMovies, path=path, title=title, page=page)

    return oc

@route(PREFIX + '/movie')
def HandleMovie(operation=None, container=False, **params):
    oc = ObjectContainer(title2=unicode(L(params['name'])), user_agent = 'Plex')

    # if 'season' in params:
    #     season = params['season']
    # else:
    #     season = None
    #
    # if 'episode' in params:
    #     episode = params['episode']
    # else:
    #     episode = None
    #
    # if season and int(season) > 0 and episode:
    #     urls = service.get_urls(url=params['id'])
    # else:
    #     urls = service.get_urls(path=params['id'])
    #
    # if len(urls) == 0:
    #     return plex_util.no_contents()
    # else:

    urls = service.get_movie_urls(params['id'])

    url_items = service.get_movie_urls_metadata(urls)

    media_info = MediaInfo(**params)

    service.queue.handle_bookmark_operation(operation, media_info)

    oc.add(MetadataObjectForURL(media_info=media_info, url_items=url_items, player=PlayVideo))

    if str(container) == 'False':
        history.push_to_history(Data, media_info)
        service.queue.append_bookmark_controls(oc, HandleMovie, media_info)

    return oc

@route(PREFIX + '/tops')
def HandleTops():
    oc = ObjectContainer(title2=unicode(L('Top')))

    names = ['By Rating', 'By Views', 'By Comments', 'Selections']

    for name in names:
        oc.add(DirectoryObject(
            key=Callback(HandleTop, name=name),
            title=plex_util.sanitize(unicode(L(name)))
        ))

    return oc

@route(PREFIX + '/top')
def HandleTop(name):
    oc = ObjectContainer(title2=unicode(L(name)))

    return oc

@route(PREFIX + '/search')
def HandleSearch(query=None, page=1):
    oc = ObjectContainer(title2=unicode(L('Search')))

    # response = service.search(query=query, page=page)
    #
    # for movie in response['movies']:
    #     name = movie['name']
    #     thumb = movie['thumb']
    #
    #     new_params = {
    #         'id': movie['path'],
    #         'title': name,
    #         'name': name,
    #         'thumb': thumb
    #     }
    #     oc.add(DirectoryObject(
    #         key=Callback(HandleMovieOrSerie, **new_params),
    #         title=unicode(name),
    #         thumb=plex_util.get_thumb(thumb)
    #     ))
    #
    # pagination.append_controls(oc, response, callback=HandleSearch, query=query, page=page)

    return oc

@route(PREFIX + '/container')
def HandleContainer(**params):
    type = params['type']

    if type == 'movie':
        return HandleMovie(**params)
    # elif type == 'episode':
    #     return HandleEpisode(**params)
    # elif type == 'season':
    #     return HandleSeason(**params)
    # elif type == 'serie':
    #     return HandleSerie(**params)

@route(PREFIX + '/queue')
def HandleQueue():
    oc = ObjectContainer(title2=unicode(L('Queue')))

    service.queue.handle_queue_items(oc, HandleContainer, service.queue.data)

    if len(service.queue.data) > 0:
        oc.add(DirectoryObject(
            key=Callback(ClearQueue),
            title=unicode(L("Clear Queue"))
        ))

    return oc

@route(PREFIX + '/clear_queue')
def ClearQueue():
    service.queue.clear()

    return HandleQueue()

@route(PREFIX + '/history')
def HandleHistory():
    history_object = history.load_history(Data)

    oc = ObjectContainer(title2=unicode(L('History')))

    if history_object:
        data = sorted(history_object.values(), key=lambda k: k['time'], reverse=True)

        service.queue.handle_queue_items(oc, HandleContainer, data)

    return oc

def MetadataObjectForURL(media_info, url_items, player):
    metadata_object = builder.build_metadata_object(media_type=media_info['type'], title=media_info['name'])

    metadata_object.key = Callback(HandleMovie, container=True, **media_info)

    # metadata_object.rating_key = 'rating_key'
    metadata_object.rating_key = unicode(media_info['name'])
    # metadata_object.rating = data['rating']
    metadata_object.thumb = media_info['thumb']
    # metadata_object.url = urls['m3u8'][0]
    # metadata_object.art = data['thumb']
    # metadata_object.tags = data['tags']
    # metadata_object.duration = data['duration'] * 1000
    # metadata_object.summary = data['summary']
    # metadata_object.directors = data['directors']

    metadata_object.items = MediaObjectsForURL(url_items, player=player)

    return metadata_object

def MediaObjectsForURL(url_items, player):
    media_objects = []

    for item in url_items:
        url = item['url']
        config = item['config']

        play_callback = Callback(player, url=url, play_list=False)

        media_object = builder.build_media_object(play_callback, config)

        media_objects.append(media_object)

    return media_objects

@indirect
@route(PREFIX + '/play_video')
def PlayVideo(url, play_list=True):
    if not url:
        return plex_util.no_contents()
    else:
        if str(play_list) == 'True':
            url = Callback(PlayList, url=url)

        return IndirectResponse(MovieObject, key=RTMPVideoURL(url))

@route(PREFIX + '/play_list.m3u8')
def PlayList(url):
    play_list = service.get_play_list(url)

    return play_list