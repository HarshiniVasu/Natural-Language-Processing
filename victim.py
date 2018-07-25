from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import sys
import nltk
from stanfordcorenlp import StanfordCoreNLP
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

nlp = StanfordCoreNLP(r'stanford-corenlp-full-2017-06-09')


wd=WordNetLemmatizer()


def victim(paragraph):
	victimlist=[]; verblist=['VB','VBD','VBN','VBP','VBG','VBZ','JJ']
	names=['NNS','NNP','NN']
	impwords=[]
	shortlistedsent=[]; mainsent=[]; mainsent1=[]; mainsent2=[]
	with open("victim.txt","r") as f1: 
		for i in f1:
			i=i.rstrip()
			victimlist.append(i)
	sent=sent_tokenize(paragraph)
	for s in sent:
		wordset=[]
		wordtokens=word_tokenize(s)
		wordstok=filter(str.isalnum,wordtokens)
		maximum=0
		for w in wordstok:
			postags=nlp.pos_tag(w)
			stemmed=w
			if(str(postags[0][1]) in verblist):	
				stemmed=wd.lemmatize(w,'v')
			if stemmed in victimlist:
				shortlistedsent.append(s)
				impwords.append(stemmed)
				break

	for sw in shortlistedsent:
		words=word_tokenize(sw)
		gram= r'''
		NN1: {<DT>*<NN|NN.>+<IN><CD>*<NN|NN.>+}
		NN2: {<CD>* <NN|NN.>+<WP><VB.>+<IN>*<DT>*<NN|NN.>*}
		NN3: {<VB.>+<DT>*<CD>*<NN.>}
		 '''
		chunked_text = nltk.RegexpParser(gram)
		tokenised_words=word_tokenize(sw)
		poswords = nlp.pos_tag(sw)
		a=[]
		tree = chunked_text.parse(poswords)
		for subtree in tree.subtrees(filter = lambda t: t.label()=='NN1'):
			mainsent.append(subtree.leaves())
		for subtree in tree.subtrees(filter = lambda t: t.label()=='NN2'):
			mainsent1.append(subtree.leaves())
		for subtree in tree.subtrees(filter = lambda t: t.label()=='NN3'):
			mainsent2.append(subtree.leaves())
	a="-"
	if(mainsent2!=0):
		firstword=[]
		for x in mainsent2:
			stemmed1=wd.lemmatize(str(x[0][0]),'v')
			for j in impwords:
				if j ==stemmed1:
					firstword.append(x)
					break
		for x in firstword:
			for y in range(len(x)):
				if x[y][1] in names:
					a=x[y][0]
			break
	return a
