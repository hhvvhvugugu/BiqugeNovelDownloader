import BiquPavilionAPI
import book
import epub
from instance import *


def agreed_read_readme():
    if Vars.cfg.data.get('Disclaimers') != 'yes':
        print(Vars.cfg.data.get('agree_terms'))
        confirm = inputs_('>').strip()
        if confirm == 'yes' or confirm == '同意':
            Vars.cfg.data['Disclaimers'] = 'yes'
            Vars.cfg.save()
        else:
            sys.exit()


def shell_book(inputs):  # 通过小说ID下载单本小说
    if len(inputs) >= 2:
        response = BiquPavilionAPI.Book.novel_info(novel_id_url(inputs[1]))
        if response is not None and isinstance(response, dict):
            Vars.book_info = book.Book(response)
            makedirs(Vars.cfg.data.get('save_book') + "/" + Vars.book_info.book_name)
            print("开始下载《{}》\n{}".format(Vars.book_info.book_name, Vars.book_info.show_book_info()))
            Vars.epub_info = epub.EpubFile()
            Vars.epub_info.add_intro()
        else:
            print("获取书籍信息失败，请检查id或者重新尝试！")
            return False
        makedirs(Vars.book_info.config_book_dir)
        Vars.book_info.download_chapter_threading()
        Vars.book_info.output_text_and_epub()
        print("《{}》下载完成".format(Vars.book_info.book_name))
    else:
        print('未输入Book-id')


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
            Vars.cfg.data['threading_pool_size'] = int(inputs[1])
            Vars.cfg.save(), print("线程已设置为", Vars.cfg.data.get('threading_pool_size'))
        else:
            print("线程数必须为数字")
    else:
        print("默认线程为", Vars.cfg.data.get('threading_pool_size'))


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


def shell(inputs: list):
    choice = inputs[0].lower()
    if choice == "q" or choice == 'quit':
        sys.exit("已退出程序")
    if choice == 'h' or choice == 'help':
        print(Vars.cfg.data.get('help'))
    elif choice == 'd' or choice == 'download':
        shell_book(inputs)
    elif choice == 'u' or choice == 'update':
        shell_list(inputs)
    elif choice == 'p' or choice == 'pool':
        get_pool(inputs)
    else:
        print(choice, '不是有效命令,请输入help查看帮助')


if __name__ == '__main__':
    setup_config()
    agreed_read_readme()
    if len(sys.argv) > 1:
        shell(sys.argv[1:])
    else:
        print(Vars.cfg.data.get('help'))
        while True:
            shell(re.split('\\s+', inputs_('>').strip()))
