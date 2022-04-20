import demjson

from BiquPavilionAPI import HttpUtil


def get(api_url: str, params: dict = None) -> [str, dict]:
    # api_url = UrlConstants.WEB_SITE + api_url.replace(UrlConstants.WEB_SITE, '')
    return demjson.decode(HttpUtil.get(api_url, params))


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
    def download_cover(max_retry=10) -> str:
        for retry in range(max_retry):
            params = {'type': 'moe', 'size': '1920x1080'}
            response = HttpUtil.get('https://api.yimian.xyz/img', params=params)
            if response.status_code == 200:
                return HttpUtil.get(response.url).content
            else:
                print("msg:", response.text)
