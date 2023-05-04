import urllib.parse
import requests
import re
import io

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
}


class ImageFile():
    def __init__(self, uri):
        self.uri = uri
        self._binary = None

    @property
    def binary(self):
        if not self._binary:
            response = requests.get(self.uri, headers=HEADERS)
            if not response.content or len(response.content) == 0:
                raise Exception
            self._binary = response.content

        return self._binary

    @property
    def buffer(self):
        return io.BytesIO(self.binary)

class GoogleImage():

    def __init__(self, keyword: str):
        self.keyword = keyword
        self._search_result = None
        self._target_images = None

    @property
    def search_result(self):
        if not self._search_result:
            uri = rf'https://www.google.com.tw/search?q={urllib.parse.quote(self.keyword)}&espv=2&biw=1920&bih=966&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg&safe=active'
            response = requests.get(
                uri,
                headers=HEADERS,
            )
            _search_result = re.finditer(r'\["(https?[^"]+\.(?:jpe?g|JPE?G|png|PNG))",\d+,\d+\]', response.text)
            self._search_result = list(map(lambda match: match.group(1), _search_result))
            
        return self._search_result

    @property
    def target_images(self):
        if not self._target_images:
            self._target_images = list(map(ImageFile, self.search_result))

        return self._target_images
