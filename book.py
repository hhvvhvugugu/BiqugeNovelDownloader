import threading
import BiquPavilionAPI
from instance import *


class Book:

    def __init__(self, book_info: dict, index=None):
        self.index = index
        self.progress_bar = 1
        self.chapter_info_list = list()
        self.threading_pool = list()
        self.download_chapter_list = list()
        self.pool_sema = threading.BoundedSemaphore(Vars.cfg.data.get('threading_pool_size'))
        self.book_name = book_info.get('Name')
        self.book_id = novel_id_url(book_info.get('Id'))
        self.author_name = book_info.get('Author')
        self.book_intro = book_info.get('Desc')
        self.book_state = book_info.get('BookStatus')
        self.book_tag = book_info.get('CName')
        self.book_updated = book_info.get('LastTime')
        self.last_chapter = del_title(book_info.get('LastChapter'))
        self.cover_url = "https://imgapixs.pigqq.com/BookFiles/BookImages/" + book_info.get('Img')

    def show_book_info(self) -> str:
        show_info = '作者:{0:<{2}}状态:{1}\n'.format(self.author_name, self.book_state, isCN(self.author_name))
        show_info += '最新:{0:<{2}}更新:{1}\n'.format(self.last_chapter, self.book_updated, isCN(self.last_chapter))
        print(show_info)
        return '{}简介:\n{}'.format(show_info, self.arrange(self.book_intro, intro=True))

    def progress(self, download_length) -> None:
        percentage = (self.progress_bar / download_length) * 100
        print('{}/{} 进度:{:^3.0f}%'.format(self.progress_bar, download_length, percentage), end='\r')
        self.progress_bar += 1

    def download_content_threading(self, chapter_info, download_length) -> None:
        self.pool_sema.acquire()
        content_info = BiquPavilionAPI.Chapter.content(self.book_id, chapter_info.get('id'))
        if content_info.get('cname') != "该章节未审核通过":
            file_name = "{}/{}/{}.txt".format(Vars.cfg.data.get('config_book'), self.book_name, content_info.get('cid'))
            write(file_name, 'w', self.arrange(content_info.get('content'), content_info.get('cname')))
            self.progress(download_length)
        self.pool_sema.release()

    def output_text_and_epub(self, config_dir, save_dir) -> None:
        write(save_dir + '/' + f'{self.book_name}.txt', 'w', self.show_book_info())
        for chapter_index, info in enumerate(self.chapter_info_list):  # 获取目录文,并且 遍历文件名
            if os.path.exists(os.path.join(config_dir, str(info.get('id')) + ".txt")):
                content = write(os.path.join(config_dir, str(info.get('id')) + ".txt"), 'r').read()
                Vars.epub_info.add_chapter(info.get('id'), info.get('name'), content, chapter_index)
                write(f'{save_dir}/{self.book_name}.txt', 'a', "\n\n\n" + content)
        Vars.epub_info.save()
        self.chapter_info_list.clear()
        self.download_chapter_list.clear()

    def get_chapter_api(self) -> int:
        filename_list = os.listdir(os.path.join(Vars.cfg.data.get('config_book'), self.book_name))
        catalogue_info_list = BiquPavilionAPI.Book.catalogue(self.book_id)
        for index, catalogue_info in enumerate(catalogue_info_list):
            print(f"第{index}卷", catalogue_info.get('name'))
            for info in catalogue_info.get('list'):
                self.chapter_info_list.append(info)
                if str(info.get('id')) + ".txt" in filename_list:
                    continue
                self.download_chapter_list.append(info)
        return len(self.download_chapter_list)

    def download_chapter_threading(self):
        download_length = self.get_chapter_api()
        if download_length == 0:
            print("没有需要下载的章节！")
            return download_length
        for index, chapter_info in enumerate(self.download_chapter_list):
            self.threading_pool.append(
                threading.Thread(target=self.download_content_threading, args=(chapter_info, download_length,))
            )
        for thread in self.threading_pool:
            thread.start()

        for thread in self.threading_pool:
            thread.join()
        self.threading_pool.clear()

    def arrange(self, chapter_content, chapter_title="", intro=False):
        content = ""
        if intro is True:
            for line in chapter_content.splitlines():
                chapter_line = line.strip("　").strip()
                if chapter_line != "":
                    content += "\n" + chapter_line[:60]
            return content
        for line in chapter_content.splitlines():
            chapter_line = line.strip("　").strip()
            if chapter_line != "" and len(chapter_line) > 2:
                if "http" in chapter_line:
                    continue
                content += "\n　　{}".format(chapter_line)
        return f"{chapter_title}\n{content}"
