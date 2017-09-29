import jieba.analyse

def get_word_from_sentence(sentence):

	word_list = jieba.cut(sentence, cut_all = False)
	top_word = jieba.analyse.extract_tags(sentence, topK = 4, allowPOS = ['ns','nr','nt','nz'])
	key_word_list = []

	for word in word_list:
		if word in top_word:
			key_word_list.append(word)

	return sorted(set(key_word_list), key = key_word_list.index)


