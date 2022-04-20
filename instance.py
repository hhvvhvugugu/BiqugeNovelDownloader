import re
import time
from config import *


class Vars:
    cfg = Config('Config.json', os.getcwd())
    book_info = None
    epub_info = None


def novel_id_url(novel_id: int) -> str:
    return "{}/{}".format(int(int(novel_id) / 1000) + 1, novel_id)


def mkdir(file_path: str):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def makedirs(file_path: str):
    if not os.path.exists(os.path.join(file_path)):
        os.makedirs(os.path.join(file_path))


def isCN(book_name):
    cn_no = 0
    for ch in book_name:
        if '\u4e00' <= ch <= '\u9fff':
            cn_no += 1
    return 40 - cn_no


def inputs_(prompt, default=None):
    while True:
        ret = input(prompt)
        if ret != '':
            return ret
        elif default is not None:
            return default


def del_title(title: str):
    """删去windowns不规范字符"""
    title = title.replace("\x06", "").replace("\x05", "").replace("\x07", "")
    return re.sub(r'[？?。*|“<>:/\\]', '', title)


def content_(content: str):
    return ''.join([re.sub(r'^\s*', "\n　　", content)
                    for content in content.split("\n") if re.search(r'\S', content) is not None])


def write(path: str, mode: str, info=None):
    if info is not None:
        try:
            with open(path, f'{mode}', encoding='UTF-8', newline='') as file:
                file.writelines(info)
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            with open(path, f'{mode}', encoding='gbk', newline='') as file:
                file.writelines(info)
    else:
        try:
            return open(path, f'{mode}', encoding='UTF-8')
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            return open(path, f'{mode}', encoding='gbk')


def setup_config():
    Vars.cfg.load()
    config_change = False
    if type(Vars.cfg.data.get('save_book')) is not str or Vars.cfg.data.get('save_book') == "":
        Vars.cfg.data['save_book'] = 'novel'
        config_change = True
    if type(Vars.cfg.data.get('config_book')) is not str or Vars.cfg.data.get('config_book') == "":
        Vars.cfg.data['config_book'] = 'config'
        config_change = True
    if type(Vars.cfg.data.get('Pool')) is not int or Vars.cfg.data.get('ThVars.cfg.data_Pool') == "":
        Vars.cfg.data['Pool'] = 12
        config_change = True
    if type(Vars.cfg.data.get('agreed_to_Vars.cfg.datame')) is not str or Vars.cfg.data.get(
            'agreed_to_Vars.cfg.datame') == "":
        Vars.cfg.data['agreed_to_Vars.cfg.datame'] = 'No'
        config_change = True
    if type(Vars.cfg.data.get('agree_terms')) is not str or Vars.cfg.data.get('agree_terms') == "":
        Vars.cfg.data['agree_terms'] = '是否以仔细阅读且同意LICENSE中叙述免责声明\n如果同意声明，请输入英文 \"yes\" 或者中文 \"同意\" 后按Enter建，如果不同意请关闭此程式'
        config_change = True
    if type(Vars.cfg.data.get('show_book_info')) is not str or Vars.cfg.data.get('show_book_info') == "":
        Vars.cfg.data['show_book_info'] = '书名:{}\n作者:{}\n状态:{}\n字数:{}\n更新:{}\n标签:{}\n最后更新章节:{}\n简介信息\n{}'
        config_change = True
    if type(Vars.cfg.data.get('help')) is not str or Vars.cfg.data.get('help') == "":
        Vars.cfg.data['help'] = 'https://m.aixdzs.com/\nd | bookid\t\t\t\t\t———输入书籍序号下载单本小说\nt | ' \
                                'tagid\t\t\t\t\t———输入分类号批量下载分类小说\nn | bookname\t\t\t\t\t———下载单本小说\nh | ' \
                                'help\t\t\t\t\t———获取使用程序帮助\nq | quit\t\t\t\t\t———退出运行的程序\nm | method\t\t\t\t\t———切换多线程和多进程\np | ' \
                                'pool\t\t\t\t\t———改变线程数目\nu | updata\t\t\t\t\t———下载指定文本中的bookid '
        config_change = True
    if type(Vars.cfg.data.get('tag')) is not dict or Vars.cfg.data.get('tag') == "":
        Vars.cfg.data['tag'] = {1: '玄幻', 2: '奇幻', 3: '武侠', 4: '仙侠', 5: '都市', 6: '职场', 7: '历史',
                                8: '军事', 9: '游戏', 10: '竞技', 11: '科幻', 12: '灵异', 13: '同人', 14: '轻小说'}
        config_change = True

    if config_change:
        Vars.cfg.save()
        if os.path.exists(Vars.cfg.data.get('save_book')) and os.path.exists(Vars.cfg.data.get('config_book')):
            pass
        else:
            mkdir(Vars.cfg.data.get('save_book'))
            mkdir(Vars.cfg.data.get('config_book'))
