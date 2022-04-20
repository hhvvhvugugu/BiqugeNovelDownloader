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
        cover_jpg = BiquPavilionAPI.Cover.download_cover(Vars.book_info.cover_url)
        self.epub.set_cover(self.book_name + '.png', cover_jpg)

    def add_chapter(self, chapter_id: str, chapter_title: str, content: str, serial_number: str):
        default_style = '''
        body {font-size:100%;}
        p{
            font-family: Auto;
            text-indent: 2em;
        }
        h1{
            font-style: normal;
            font-size: 20px;
            font-family: Auto;
        }      
        '''
        default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css",
                                    content=default_style)

        chapter_serial = epub.EpubHtml(
            title=chapter_title, file_name=str(serial_number).rjust(4, "0") + '-' + str(chapter_id) + '.xhtml',
            lang='zh-CN', uid='chapter_{}'.format(serial_number)
        )

        chapter_serial.content = content.replace('\n', '</p>\r\n<p>')
        chapter_serial.add_item(default_css)
        self.epub.add_item(chapter_serial)
        self.EpubList.append(chapter_serial)

    def save(self):
        self.cover()
        self.epub.toc = tuple(self.EpubList)
        self.epub.spine = ['nav']
        self.epub.spine.extend(self.EpubList)
        self.epub.add_item(epub.EpubNcx())
        self.epub.add_item(epub.EpubNav())
        style = """
                body {
                    font-family: Auto;
                }
                p{
                     font-family: Auto;
                     text-indent: 2em;
                }
                h2 {
                     text-align: left;
                     text-transform: uppercase;
                     font-weight: 200;     
                }
                ol {
                        list-style-type: none;
                }
                ol > li:first-child {
                        margin-top: 0.3em;
                }
                nav[epub|type~='toc'] > ol > li > ol  {
                    list-style-type:square;
                }
                nav[epub|type~='toc'] > ol > li > ol > li {
                        margin-top: 0.3em;
                }"""
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        self.epub.add_item(nav_css)
        epub.write_epub(self.path(Vars.cfg.data.get('save_book'), self.book_name, self.book_name + '.epub'), self.epub,
                        {})
