import BiquPavilionAPI
import book
import epub
from instance import *


def agreed_read_readme():
    if Vars.cfg.data.get('agreed_to_readme') != 'yes':
        print(Vars.cfg.data.get('agree_terms'))
        confirm = inputs_('>').strip()
        if confirm == 'yes' or confirm == '同意':
            Vars.cfg.data['agreed_to_readme'] = 'yes'
            Vars.cfg.save()
        else:
            sys.exit()


def shell_book(inputs):  # 通过小说ID下载单本小说
    if len(inputs) >= 2:
        Vars.book_info = BiquPavilionAPI.Book.novel_info(novel_id_url(inputs[1]))
        if Vars.book_info is not None and isinstance(Vars.book_info, dict):
            Vars.book_info = book.Book(Vars.book_info)
            book_name = Vars.book_info.book_name
            Vars.epub_info = epub.EpubFile(Vars.book_info.book_id, book_name, Vars.book_info.author_name)
            Vars.epub_info.add_intro(
                Vars.book_info.author_name, Vars.book_info.book_updated, Vars.book_info.last_chapter,
                Vars.book_info.book_intro, Vars.book_info.book_tag
            )
            print("开始下载《{}》".format(book_name))
            config_dir = Vars.cfg.data.get('config_book') + "/" + book_name
            save_dir = Vars.cfg.data.get('save_book') + "/" + book_name
            makedirs(config_dir), makedirs(save_dir)
            Vars.book_info.download_chapter_threading()
            # Vars.epub_info.epub_file_save(save_dir)
            Vars.book_info.output_text_and_epub(config_dir, save_dir)
            print("《{}》下载完成".format(book_name))
        else:
            print("获取书籍信息失败，请检查id或者重新尝试！")
    else:
        print('未输入Bookid')


# def shell_search_book(inputs):
#     if len(inputs) >= 2:
#         start = time.time()
#         response = BiquPavilionAPI.Book.search_book(inputs[1])
#         for index, books in enumerate(response):
#             shell_book([index, books.get('_id')])
#         print(f'下载耗时:{round(time.time() - start, 2)} 秒')
#     else:
#         print('未输入书名')


def get_pool(inputs):
    if len(inputs) >= 2:
        if inputs[1].isdigit():
            Vars.cfg.data['Thread_Pool'] = int(inputs[1])
            Vars.cfg.save(), print("线程已设置为", Vars.cfg.data.get('Thread_Pool'))
        else:
            print("线程数必须为数字")
    else:
        print("默认线程为", Vars.cfg.data.get('Thread_Pool'))


def shell_list(inputs):
    start = time.time()
    list_file_name = inputs[1] + '.txt' if len(inputs) >= 2 else 'list.txt'
    try:
        list_file_input = open(list_file_name, 'r', encoding='utf-8')
        book_list = [line for line in list_file_input.readlines() if re.match("^\\s*([0-9]{1,7}).*$", line)]
        for book_id in book_list:
            shell_book(['', re.sub("^\\s*([0-9]{1,7}).*$\\n?", "\\1", book_id)])
        print(f'下载耗时:{round(time.time() - start, 2)} 秒')
    except OSError:
        print(f"{list_file_name}文件不存在")


def shell():
    if len(sys.argv) > 1:
        command_line, inputs = True, sys.argv[1:]
    else:
        print(Vars.cfg.data.get('help'))
        command_line, inputs = False, re.split('\\s+', inputs_('>').strip())
    while True:
        if inputs[0].startswith('q') or inputs[0] == '--quit':
            sys.exit("已退出程序")
        if inputs[0] == 'h' or inputs[0] == '--help':
            print(Vars.cfg.data.get('help'))
        elif inputs[0] == 'd' or inputs[0] == '--download':
            shell_book(inputs)
        elif inputs[0] == 'u' or inputs[0] == '--update':
            shell_list(inputs)
        elif inputs[0] == 'p' or inputs[0] == '--pool':
            get_pool(inputs)
        else:
            print(inputs[0], '不是有效命令')
        if command_line is True:
            sys.exit(1)
        inputs = re.split('\\s+', inputs_('>').strip())


if __name__ == '__main__':
    setup_config()
    agreed_read_readme()
    shell()
