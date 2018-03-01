from lxml import etree
import requests
from io import BytesIO
from wordcloud import WordCloud, ImageColorGenerator
import jieba
import numpy as np
from PIL import Image
from os import path

d = path.dirname(__file__)
URL_CID = 'https://api.bilibili.com/x/player/pagelist'
URL_DANMU = 'https://comment.bilibili.com/'


class Danmu:
    """弹幕词云处理类
    """
    def __init__(self, aid: str or [str] = None) -> None:
        self._aid_list = (aid if isinstance(aid, list) else [aid]) if aid else list()
        self._cid_dict = dict()
        self._danmu_dict = dict()

    def add_aid(self, aid: str) -> None:
        """直接添加aid
        """
        self._aid_list.append(aid)

    def remove_aid(self, aid: str) -> None:
        """删除指定aid
        """
        self._aid_list.remove(aid)

    def _getcid(self) -> None:
        """提取当前aid的所有cid
        在添加aid后需要先调用此方法请求得到cid字典
        若cid字典已存在, 应当检查是否有新添加的aid未提取cid
        """
        _cid_list = list()
        for aid in self._aid_list:
            if aid not in self._cid_dict.keys():
                _cid_list.append(aid)
        if _cid_list:
            for aid in _cid_list:
                self._cid_dict[aid] = self._get_cid_by_aid(aid)

    def getdanmu(self) -> None:
        """提取弹幕
        得到cid字典后提取弹幕, 弹幕全部整合在一起
        """
        self._getcid()  # 保证全部aid都提取了cid
        for aid in self._cid_dict.keys():
            for cid in self._cid_dict[aid]:
                self._danmu_dict[cid] = self._get_danmu_by_cid(cid)

    def generate_wc(self, 
        img_file: str=None, 
        colored: bool=False,
        userdict: str=None,
        stopwords: str=None,
        output: str='result.jpg',
        font_path: str=path.join(d, 'fonts.ttc'),
        max_words: int=2000,
        *args, **kwargs
        ) -> None:
        """生成词云
        """
        self.getdanmu()
        if userdict:
            jieba.load_userdict(path.join(d, userdict))
        sw = self._get_stopwords if stopwords else None
        mask = np.array(Image.open(path.join(d, img_file))) if img_file else None
        words = ' '.join(jieba.cut(''.join([self._danmu_dict[cid] for cid in self._danmu_dict.keys()])))
        wordcloud = WordCloud(
            mask=mask, 
            font_path=font_path, 
            stopwords=sw,
            max_words=max_words,
            *args, **kwargs)
        wc = wordcloud.generate(words)
        if colored and img_file:
            wc.recolor(color_func=ImageColorGenerator(mask))
        wc.to_file(output)
        print('词云生成成功')

    @property
    def aid_list(self) -> list:
        """返回当前aid(list)
        """
        return self._aid_list

    @property
    def cid_dict(self) -> dict:
        """返回当前cid(dict)
        key: aid
        value" [cid]
        """
        return self._cid_dict
    
    @property
    def danmu_dict(self) -> dict:
        """返回当前danmu(dict)
        key: cid
        value: danmu_string
        """
        return self._danmu_dict

    def _get_cid_by_aid(self, aid: str) -> list:
        """通过aid提取cid(list)
        """
        querystring = {
            'aid': aid,
            'jsonp': 'jsonp'
        }
        result = requests.get(url=URL_CID, params=querystring).json()
        return [str(r.get('cid')) for r in result.get('data')]

    def _get_danmu_by_cid(self, cid: str) -> str:
        """通过cid提取danmu(str)
        """
        url = URL_DANMU + cid + '.xml'
        response = requests.get(url)
        xml = etree.parse(BytesIO(response.content))
        root = xml.getroot()
        return ' '.join([(d.text if d.tag == 'd' else '') for d in root])
        
    @staticmethod
    def _get_stopwords(sw_file: str) -> set:
        """提取停用词集合
        """
        sw_set = set()
        with open(path.join(d, sw_file), 'r', encoding='utf-8') as f:
            sw = f.readlines()
        for s in sw:
            sw_set.add(s.replace('\n', ''))
        return sw_set