from jpeg_bot.google_image import GoogleImage, ImageFile

def test_search():
    assert len(GoogleImage('miku').search_result) > 0

def test_image_binary():
    assert len(ImageFile("https://github.com/favicon.ico").binary) > 0

def test_image_buffer():
    assert len(ImageFile("https://github.com/favicon.ico").buffer.read()) > 0
