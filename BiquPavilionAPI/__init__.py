import demjson

from BiquPavilionAPI import HttpUtil


def get(api_url: str, params: dict = None) -> [str, dict]:
    # api_url = UrlConstants.WEB_SITE + api_url.replace(UrlConstants.WEB_SITE, '')
    return demjson.decode(str(HttpUtil.get(api_url, params).text))


class Book:

    @staticmethod
    def novel_info(novel_id: str):
        response = get("https://infosxs.pigqq.com/BookFiles/Html/{}/info.html".format(novel_id))
        if response.get('status') == 1 and response.get('info') == 'success':
            return response.get('data')

    @staticmethod
    def catalogue(novel_id: str):
        response = get("https://infosxs.pigqq.com/BookFiles/Html/{}/index.html".format(novel_id))

        if response.get('status') == 1 and response.get('info') == 'success':
            return response.get('data').get('list')


class Chapter:
    @staticmethod
    def content(book_id: str, chapter_id: str):
        response = get("https://contentxs.pigqq.com/BookFiles/Html/{}/{}.html".format(book_id, chapter_id))
        if response.get('status') == 1 and response.get('info') == 'success':
            return response.get('data')


class Cover:
    @staticmethod
    def download_cover(url: str, params: dict = None) -> bytes:
        response = HttpUtil.get(url, params=params).content
        if response:
            return response
