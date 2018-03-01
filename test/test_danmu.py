import unittest
from os import path
from danmu import Danmu


class TestDanmu(unittest.TestCase):
    def test_init(self) -> None:
        d = Danmu(aid='123456')
        assert d.aid_list == ['123456']
        d2 = Danmu(aid=['123', '456'])
        assert d2.aid_list == ['123', '456']

    def test_add_aid(self) -> None:
        d = Danmu(aid='123456')
        d.add_aid('654321')
        assert d.aid_list == ['123456', '654321']

    def test_get_danmu(self) -> None:
        d = Danmu(aid='20111521')
        d.getdanmu()
        cid_list = ['32819890', '32820624', '32821424', '32821882', '32819888']
        cid_dict = d.cid_dict
        assert cid_dict.__contains__('20111521')
        assert len(cid_dict['20111521']) == len(cid_list)
        for c in cid_list:
            assert c in cid_dict['20111521']
            assert c in d.danmu_dict.keys()
    
    def test_generate_wc(self) -> None:
        d = Danmu(aid='20111521')
        d.generate_wc()
        assert path.isfile('result.jpg')

if __name__ == '__main__':
    unittest.main()
