from ebook.ebooklib import epub
from instance import *
import BiquPavilionAPI


class EpubFile:
    def __init__(self):
        self.epub = epub.EpubBook()
        self.EpubList = list()
        self.path = os.path.join
        self.epub.set_language('zh-CN')
        self.epub.set_identifier(Vars.book_info.book_id)
        self.epub.set_title(Vars.book_info.book_name)
        self.epub.add_author(Vars.book_info.author_name)

    def add_intro(self):
        write_intro = epub.EpubHtml(title='简介信息', file_name='0000-000000-intro.xhtml', lang='zh-CN')
        write_intro.content = '<html><head></head><body><h1>简介</h1>'
        write_intro.content += '<p>书籍书名:{}</p><p>书籍序号:{}</p>'.format(
            Vars.book_info.book_name, Vars.book_info.book_id)
        write_intro.content += '<p>书籍作者:{}</p><p>更新时间:{}</p>'.format(
            Vars.book_info.author_name, Vars.book_info.book_updated)
        write_intro.content += '<p>最新章节:{}</p><p>系统标签:{}</p>'.format(
            Vars.book_info.last_chapter, Vars.book_info.book_tag)
        write_intro.content += '<p>简介信息:</p>{}</body></html>'.format(Vars.book_info.book_intro)
        self.epub.add_item(write_intro)
        self.EpubList.append(write_intro)

    def cover(self):
        cover_url = "https://imgapixs.pigqq.com/BookFiles/BookImages/" + Vars.book_info.cover_url
        cover_jpg = BiquPavilionAPI.Cover.download_cover(cover_url)
        self.epub.set_cover(Vars.book_info.book_name + '.png', cover_jpg)

    def add_chapter(self, chapter_id: str, chapter_title: str, content: str, serial_number: str):
        file_name = str(serial_number + 1).rjust(4, "0") + '-' + str(chapter_id) + '.xhtml'
        chapter_serial = epub.EpubHtml(
            title=chapter_title, file_name=file_name, lang='zh-CN', uid='index-{}'.format(serial_number + 1)
        )
        chapter_serial.content = content.replace('\n', '</p>\r\n<p>')
        self.epub.add_item(chapter_serial)
        self.EpubList.append(chapter_serial)

    def save(self):
        self.cover()
        self.epub.toc = tuple(self.EpubList)
        self.epub.spine = ['nav']
        self.epub.spine.extend(self.EpubList)
        self.epub.add_item(epub.EpubNcx())
        self.epub.add_item(epub.EpubNav())
        epub.write_epub(Vars.book_info.save_book_dir.replace('.txt', ".epub"), self.epub, {})
