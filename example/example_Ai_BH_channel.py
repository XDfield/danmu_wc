from lxml import etree
from danmu import Danmu

file = 'BH_channel.html'
tree = etree.HTML(open(file, 'r', encoding='utf-8').read())
aids = tree.xpath('//li[@data-aid]')
aid_list = list()
for li in aids:
	aid_list.append(li.attrib['data-aid'])

d = Danmu(aid=aid_list)
d.generate_wc(
    scale=8,
    max_words=2000,
    background_color='white',
    img_file='puyopuyo.png',
    userdict='userdict.txt',
    colored=True,
    output='花Q.jpg'
    )
