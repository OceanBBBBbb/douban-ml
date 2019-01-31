# 简单的监督学习例子
# 使用朴素贝叶斯算法进行分类训练。
from nltk.stem import WordNetLemmatizer
from nltk.classify import NaiveBayesClassifier
import pickle
import jieba

def proc_text(text):
    # 分词
    raw_words = jieba.cut(text, cut_all=True)
    # 词形归一化
    wordnet_lematizer = WordNetLemmatizer()
    words = [wordnet_lematizer.lemmatize(raw_word) for raw_word in raw_words]
    # True 表示该词在文本中，为了使用nltk中的分类器
    return {word: True for word in words}

def train_data_from_txt(model_name,txt):
    # 读取文本
    # a = numpy.loadtxt('data_xxjzw.txt',encoding='UTF-8') #这个是读数的。。
    with open(txt, encoding="utf-8") as fp:
        train_data=[]
        for line in fp:
            txt_split=line.split(' ')
            train_data.append([proc_text(txt_split[0]),int(txt_split[1])])
        # 训练模型
        nb_model = NaiveBayesClassifier.train(train_data)
        # 把模型训练集存起来
        f = open(model_name, 'wb')
        pickle.dump(nb_model, f)
        f.close()

if __name__ == '__main__':
    # train_data_from_txt('data_xxjzw_classifier.pickle','../doc/data_xxjzw.txt') #得到心训练模型
    # # 测试模型
    text6 = '期待'
    f = open('data_xxjzw_classifier.pickle', 'rb')
    classifier = pickle.load(f) #读取结果集就可以了
    f.close()
    print(classifier.classify(proc_text(text6)))
