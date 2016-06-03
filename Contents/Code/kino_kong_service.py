# -*- coding: utf-8 -*-

import urllib
import re

from http_service import HttpService

class KinoKongService(HttpService):
    URL = 'http://kinokong.net'

    def available(self):
        document = self.fetch_document(self.URL)

        return document.xpath('//div[@id="container"]')

    def get_page_path(self, path, page=1):
        if page == 1:
            new_path = path
        else:
            new_path = path + "page/" + str(page) + "/"

        return new_path

    def get_all_movies(self, page=1):
        return self.get_movies("/films/", page=page)

    def get_new_movies(self, page=1):
        return self.get_movies("/films/novinki", page=page)

    def get_all_series(self, page=1):
        return self.get_movies("/serial/", page=page)

    def get_animation(self, page=1):
        return self.get_movies("/multfilm/", page=page)

    def get_anime(self, page=1):
        return self.get_movies("/anime/", page=page)

    def get_tv_shows(self, page=1):
        return self.get_movies("/dokumentalnyy/", page=page)

    def get_movies(self, path, page=1):
        data = []

        page_path = self.get_page_path(path, page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="owl-item"]/div')

        for item in items:
            shadow_node = item.find('div[@class="main-sliders-shadow"]')
            title_node = item.find('div[@class="main-sliders-title"]')
            bg_node = shadow_node.find('div/span[@class="main-sliders-bg"]')

            href_link = bg_node.find('a[@class="main-sliders-play"]')
            thumb_link = shadow_node.find('div/img')

            href = href_link.get('href')
            href = href[len(self.URL):]
            thumb = thumb_link.get('src')
            if thumb.find(self.URL) == -1:
                thumb = self.URL + thumb
            name = title_node.text_content()

            data.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": data, "pagination": pagination["pagination"]}

    def get_movies_by_rating(self, page=1):
        return self.get_movies_by_criteria_paginated( "/?do=top&mode=rating", page=page)

    def get_movies_by_views(self, page=1):
        return self.get_movies_by_criteria_paginated( "/?do=top&mode=views", page=page)

    def get_movies_by_comments(self, page=1):
        return self.get_movies_by_criteria_paginated( "/?do=top&mode=comments", page=page)

    def get_movies_by_criteria(self, path):
        data = []

        document = self.fetch_document(self.URL + path)

        items = document.xpath('//div[@id="dle-content"]/div/div/table/tr')

        for item in items:
            link = item.find('td/a')

            if link is not None:
                href = link.get('href')
                href = href[len(self.URL):]
                name = link.text_content()

                tds = item.xpath('td')
                rating = tds[len(tds)-1].text_content()

                if href:
                    data.append({'path': href, 'name': name, 'rating': rating})

        return data

    def get_movies_by_criteria_paginated(self, path, page=1, per_page=25):
        data = self.get_movies_by_criteria(path=path)

        return {"movies": data[(page-1)*per_page:page*per_page], "pagination": self.build_pagination_data(data, page, per_page)}

    def get_tags(self):
        data = []

        document = self.fetch_document(self.URL + '/podborka.html')

        items = document.xpath('//div[@class="podborki-item-block"]')

        for item in items:
            link = item.find('a')
            img = item.find('a/span/img')
            title = item.find('a/span[@class="podborki-title"]')

            href = link.get('href')
            thumb = img.get('src')
            if thumb.find(self.URL) == -1:
                thumb = self.URL + thumb

            name = title.text_content()

            data.append({'path': href, 'thumb': thumb, 'name': name})

        return data

    def build_pagination_data(self, data, page, per_page):
        pages = len(data) / per_page

        return{
            'page': page,
            'pages': pages,
            'has_next': page < pages,
            'has_previous': page > 1
        }

    def get_series(self, path, page=1):
        return self.get_movies(path=path, page=page)

    def get_urls(self, path):
        urls = None

        document = self.fetch_document(self.URL + path)

        items = document.xpath('//script')

        for item in items:
            text = item.text_content()

            if text:
                index1 = text.find('"file":"')
                index2 = text.find('"};')

                if index1 >=0 and index2 >= 0:
                    urls = text[index1+8:index2].split(',')
                    break

        return urls

    def get_serie_playlist_url(self, path):
        url = None

        document = self.fetch_document(self.URL + path)

        items = document.xpath('//script')

        for item in items:
            text = item.text_content()

            if text:
                index1 = text.find('pl:')

                if index1 >= 0:
                    index2 = text[index1:].find('",')

                    if index2 >= 0:
                        url = text[index1+4:index1+index2]
                        break

        return url

    def get_movie(self, url):
        headers = {}

        return self.http_request(url, headers=headers).read()

    def get_urls_metadata(self, urls):
        urls_items = []

        for index, url in enumerate(urls):
            url_item = {
                "url": url,
                "config": {
                    "container": 'MP4',
                    "audio_codec": 'AAC',
                    "video_codec": 'H264',
                }
            }

            groups = url.split('.')
            text = groups[len(groups)-2]

            result = re.search('(\d+)p_(\d+)', text)

            if result and len(result.groups()) == 2:
                url_item['config']['width'] = result.group(1)
                url_item['config']['video_resolution'] = result.group(1)
                url_item['config']['height'] = result.group(2)
            else:
                result = re.search('_(\d+)', text)

                if result and len(result.groups()) == 1:
                    url_item['config']['width'] = result.group(1)
                    url_item['config']['video_resolution'] = result.group(1)

            urls_items.append(url_item)

        return urls_items

    def get_grouped_genres(self):
        data = {}

        document = self.fetch_document(self.URL)

        items = document.xpath('//div[@id="header"]/div/div/div/ul/li')

        for item in items:
            href_link = item.find('a')
            genres_node1 = item.xpath('span/em/a')
            genres_node2 = item.xpath('span/a')

            href = href_link.get('href')
            href = href[1:len(href)-1]

            if href == '':
                href = 'top'

            if len(genres_node1) > 0:
                genres_node = genres_node1
            else:
                genres_node = genres_node2

            if len(genres_node) > 0:
                data[href] = []

                for genre in genres_node:
                    path = genre.get('href')
                    name = genre.text_content()

                    if path not in ['/recenzii/', '/news/']:
                        data[href].append({'path': path, 'name': name})

        return data

    def search(self, query, page=1, per_page=15):
        page = int(page)

        search_data = {
            'do': 'search',
            'subaction': 'search',
            'search_start': page,
            'full_search': 1,
            'story': urllib.quote(query.decode('utf8').encode('cp1251'))
        }

        if page > 1:
            search_data['result_from'] = page * per_page + 1

        path = "/index.php?do=search"

        response = self.http_request(self.URL + path, method="POST", data=search_data)
        content = response.read()

        document = self.to_document(content)

        data = []

        items = document.xpath('//div[@class="owl-item"]/div')

        for item in items:
            shadow_node = item.find('div[@class="main-sliders-shadow"]')
            title_node = item.find('div[@class="main-sliders-title"]')
            season_node = shadow_node.find('div/div[@class="main-sliders-season"]')
            bg_node = shadow_node.find('div/span[@class="main-sliders-bg"]')

            href_link = bg_node.find('a[@class="main-sliders-play"]')
            thumb_link = shadow_node.find('div/img')

            href = href_link.get('href')
            href = href[len(self.URL):]

            thumb = thumb_link.get('src')

            if thumb.find(self.URL) == -1:
                thumb = self.URL + thumb

            name = title_node.text_content()

            data.append({'path': href, 'thumb': thumb, 'name': name, 'isSeason': season_node is not None})

        pagination = self.extract_pagination_data(path, page=page)

        return {"movies": data, "pagination": pagination["pagination"]}

    def extract_pagination_data(self, path, page):
        page = int(page)

        document = self.fetch_document(self.URL + path)

        pages = 1

        response = {}

        pagination_root = document.xpath('//div[@class="basenavi"]/div[@class="navigation"]')

        if pagination_root:
            pagination_node = pagination_root[0]

            links = pagination_node.xpath('a')

            pages = int(links[len(links)-1].text_content())

        response["pagination"] = {
            "page": page,
            "pages": pages,
            "has_previous": page > 1,
            "has_next": page < pages,
        }

        return response

    def get_serie_info(self, playlist_url):
        content = self.fetch_content(playlist_url)

        index = content.find('{"playlist":')

        serie_info = self.to_json(content[index:])['playlist']

        if serie_info and len(serie_info) > 0 and 'playlist' not in serie_info[0]:
            serie_info = [{
                "comment": "Сезон 1",
                "playlist": serie_info
            }]

        for item in serie_info:
            for item2 in item['playlist']:
                files = item2['file'].split(',')
                item2['file'] = []

                for file in files:
                    if file:
                        item2['file'].append(file)

        return serie_info

    def get_episode_url(self, url, season, episode):
        if season:
            return '%s?season=%d&episode=%d' % (url, int(season), int(episode))

        return url