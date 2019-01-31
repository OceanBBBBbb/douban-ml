from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import jieba
import re

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
# text = open(path.join(d, 'chat.txt'),encoding='utf-8').read()
def build_key_word(path):  # 通过词频产生特征
    d = {}
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            for word in jieba.cut(line.strip()):
                # p = re.compile(r'w', re.L)
                # result = p.sub("", word)
                # if not result or result == ' ':  # 空字符
                #     continue
                if len(word) > 1:  # 避免大量无意义的词语进入统计范围
                    d[word] = d.get(word, 0) + 1
    kw_list = sorted(d, key=lambda x: d[x], reverse=True)
    size = int(len(kw_list) * 0.22)  # 取最前的30%
    mood = set(kw_list[:size])
    mood_without_stop=list(mood)
    temp_list={}
    for ii in mood_without_stop:
        temp_list[ii]=d[ii]
    return temp_list

wl_space_split =build_key_word("txt/fkwxr.txt")
# wl_space_split="你好 你好 我号 比尔 fejio berio"
# alice_coloring = np.array(Image.open(path.join(d, "alice_color.png")))
x, y = np.ogrid[:500, :500]
mask = (x - 250) ** 2 + (y - 250) ** 2 > 230 ** 2
mask = 255 * mask.astype(int)
my_wordcloud = WordCloud(background_color='white',  # 设置背景颜色
                         font_path='simhei.ttf',  # 设置字体格式，如不设置显示不了中文
                         max_words=500,
                         max_font_size=80,  # 设置字体最大值
                         random_state=60,  # 设置有多少种随机生成状态，即有多少种配色方案
                         mask=mask,
                         ).generate_from_frequencies(wl_space_split)
plt.figure(figsize=(100, 40))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
my_wordcloud.to_file(path.join(d, "img/fkwxr.png"))

# read the mask / color image taken from
# http://jirkavinse.deviantart.com/art/quot-Real-Life-quot-Alice-282261010
# alice_coloring = np.array(Image.open(path.join(d, "alice_color.png")))
# stopwords = set(STOPWORDS)
# stopwords.add("said")
#
# wc = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
#                stopwords=stopwords, max_font_size=40, random_state=42)
# # generate word cloud
# wc.generate(text)
#
# # create coloring from image
# image_colors = ImageColorGenerator(alice_coloring)
#
# # show
# fig, axes = plt.subplots(1, 3)
# axes[0].imshow(wc, interpolation="bilinear")
# # recolor wordcloud and show
# # we could also give color_func=image_colors directly in the constructor
# axes[1].imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
# axes[2].imshow(alice_coloring, cmap=plt.cm.gray, interpolation="bilinear")
# for ax in axes:
#     ax.set_axis_off()
# plt.show()