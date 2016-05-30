# -*- coding: utf-8 -*-

import urllib

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

    def get_series(self, page=1):
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
            thumb = self.URL + thumb_link.get('src')
            name = title_node.text_content()

            data.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": data, "pagination": pagination["pagination"]}

    def get_movie_urls(self, path):
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

    def get_movie(self, url):
        headers = {}

        return self.http_request(url, headers=headers).read()

    def get_movie_urls_metadata(self, urls):
        urls_items = []

        for index, url in enumerate(urls):

            urls_items.append({
                "url": url,
                "config": {
                }
            })

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
            'full_search': 0,
            'story': urllib.quote(query.decode('utf8').encode('cp1251'))
        }

        if page == 1:
            search_data['full_search'] = 1
        else:
            search_data['full_search'] = 0
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
            bg_node = shadow_node.find('div/span[@class="main-sliders-bg"]')

            href_link = bg_node.find('a[@class="main-sliders-play"]')
            thumb_link = shadow_node.find('div/img')

            href = href_link.get('href')
            href = href[len(self.URL):]
            thumb = self.URL + thumb_link.get('src')
            name = title_node.text_content()

            data.append({'path': href, 'thumb': thumb, 'name': name})

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