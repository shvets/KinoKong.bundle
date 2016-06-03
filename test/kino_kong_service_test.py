# coding=utf-8

import test_helper

import unittest
import json

from kino_kong_service import KinoKongService

class MyHitServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = KinoKongService()

    def test_get_all_movies(self):
        result = self.service.get_all_movies()

        print(json.dumps(result, indent=4))

    def test_get_grouped_genres(self):
        result = self.service.get_grouped_genres()

        print(json.dumps(result, indent=4))

    def test_get_urls(self):
        path = "/26545-lovushka-dlya-privideniya-2015-smotret-online.html"

        result = self.service.get_urls(path)

        print(json.dumps(result, indent=4))

    def test_get_get_serie_playlist_url(self):
        path = "/25213-rodoslovnaya-03-06-2016.html"

        result = self.service.get_serie_playlist_url(path)

        print(json.dumps(result, indent=4))

    def test_get_urls_metadata(self):
        path = "/26545-lovushka-dlya-privideniya-2015-smotret-online.html"

        urls = self.service.get_urls(path)

        result = self.service.get_urls_metadata(urls)

        print(json.dumps(result, indent=4))

    def test_search(self):
        query = 'красный'

        result = self.service.search(query)

        print(json.dumps(result, indent=4))

    def test_pagination_in_all_movies(self):
        result = self.service.get_all_movies(page=1)

        # print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], False)
        self.assertEqual(pagination['page'], 1)

        result = self.service.get_all_movies(page=2)

        #print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], True)
        self.assertEqual(pagination['page'], 2)

    def test_pagination_in_movies_by_rating(self):
        result = self.service.get_movies_by_rating(page=1)

        # print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], False)
        self.assertEqual(pagination['page'], 1)

        result = self.service.get_movies_by_rating(page=2)

        #print(json.dumps(result, indent=4))

        pagination = result['pagination']

        self.assertEqual(pagination['has_next'], True)
        self.assertEqual(pagination['has_previous'], True)
        self.assertEqual(pagination['page'], 2)

    def test_get_serie_info(self):
        series = self.service.get_all_series()['movies']

        #path = series[0]['path']
        path = "/28206-v-obezd-2015-07-06-2016.html"

        playlist_url = self.get_serie_playlist_url(path)
        result = self.service.get_serie_info(playlist_url)

        print(json.dumps(result, indent=4))

    def test_get_movies_by_rating(self):
        result = self.service.get_movies_by_rating()

        print(json.dumps(result, indent=4))

    def test_get_tags(self):
        result = self.service.get_tags()

        print(json.dumps(result, indent=4))

    def test_get_soundtracks(self):
        path = '/15479-smotret-dedpul-2016-smotet-online.html'

        playlist_url = self.service.get_serie_playlist_url(path)
        result = self.service.get_serie_info(playlist_url)

        print(json.dumps(result, indent=4))


if __name__ == '__main__':
    unittest.main()
