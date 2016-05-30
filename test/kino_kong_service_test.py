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

    def test_get_movie_urls(self):
        path = "/26545-lovushka-dlya-privideniya-2015-smotret-online.html"

        result = self.service.get_movie_urls(path)

        print(json.dumps(result, indent=4))

    def test_get_movie(self):
        path = "/26545-lovushka-dlya-privideniya-2015-smotret-online.html"

        urls = self.service.get_movie_urls(path)

        result = self.service.get_movie(urls[0])

        r = open('test.mp4', 'w')

        r.write(result)

        r.close()

        #print(json.dumps(result, indent=4))

    def test_get_movie_urls_metadata(self):
        path = "/26545-lovushka-dlya-privideniya-2015-smotret-online.html"

        urls = self.service.get_movie_urls(path)

        result = self.service.get_movie_urls_metadata(urls)

        print(json.dumps(result, indent=4))

#        "http://c1.kinokong.net/crossdomain.xml"
# Referer:http://kinokong.net/26545-lovushka-dlya-privideniya-2015-smotret-online.html
# User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
# X-Requested-With:ShockwaveFlash/21.0.0.242

# Accept:*/*
# Accept-Encoding:gzip, deflate, sdch
# Accept-Language:en-US,en;q=0.8,ru;q=0.6
# Connection:keep-alive
# Cookie:_ym_uid=1457917175601539712; PHPSESSID=aodu1mjq6ju1gp416nge5dadb4; _ym_isad=2; hotnumtime=1464444618
# Host:c1.kinokong.net
# Referer:http://kinokong.net/26545-lovushka-dlya-privideniya-2015-smotret-online.html
# User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36
# X-Requested-With:ShockwaveFlash/21.0.0.242

if __name__ == '__main__':
    unittest.main()
