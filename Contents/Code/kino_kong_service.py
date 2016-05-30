# -*- coding: utf-8 -*-

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
            new_path = self.build_url(path, p=str(page))

        return new_path

    def get_all_movies(self, page=1):
        return self.get_movies("/films/", page=page)

    def get_movies(self, path, page=1):
        list = []

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

            list.append({'path': href, 'thumb': thumb, 'name': name})

        # pagination = self.extract_pagination_data(page_path, page=page)
        pagination = {'pagination': {}}

        return {"movies": list, "pagination": pagination["pagination"]}

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


