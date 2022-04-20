from ebook.ebooklib import epub
from instance import *
import BiquPavilionAPI


class EpubFile:
    def __init__(self, book_id, book_name, author_name):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.epub = epub.EpubBook()
        self.EpubList = list()
        self.path = os.path.join
        self.epub.set_language('zh-CN')
        self.epub.set_identifier(book_id)
        self.epub.set_title(book_name)
        self.epub.add_author(author_name)

    def add_intro(self, author_name, up_time, up_chapter, intro, novel_tag):
        intro_ = epub.EpubHtml(title='简介信息', file_name='0000-000000-intro.xhtml', lang='zh-CN')
        intro_.content = '<html><head></head><body><h1>简介</h1>'
        intro_.content += '<p>书籍书名:{}</p><p>书籍序号:{}</p>'.format(self.book_name, self.book_id)
        intro_.content += '<p>书籍作者:{}</p><p>更新时间:{}</p>'.format(author_name, up_time)
        intro_.content += '<p>最新章节:{}</p><p>系统标签:{}</p>'.format(up_chapter, novel_tag)
        intro_.content += '<p>简介信息:</p>{}</body></html>'.format(intro)
        self.epub.add_item(intro_)
        self.EpubList.append(intro_)

    def cover(self):
        cover_url = "https://imgapixs.pigqq.com/BookFiles/BookImages/" + Vars.book_info.cover_url
        cover_jpg = BiquPavilionAPI.Cover.download_cover(cover_url)
        self.epub.set_cover(self.book_name + '.png', cover_jpg)

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
        epub.write_epub(
            self.path(Vars.cfg.data.get('save_book'), self.book_name, self.book_name + '.epub'), self.epub, {}
        )
