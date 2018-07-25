import sys
import math
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from stanfordcorenlp import StanfordCoreNLP
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from re import search
from victim import *

nlp = StanfordCoreNLP(r'stanford-corenlp-full-2017-06-09')

st="/"
ids=[]
weapon_final=[]
t = sys.argv[1]+".templates"
outputfile = open(t,"w")
A = 0.3
B = 0.7
individvocab={}			
incident_values=['arson','attack','bombing','kidnapping','robbery']
stopwords = stopwords.words('english')



wd=WordNetLemmatizer()

#LIST OF WEAPONS
def weaponlist():
	with open("weapon.txt") as f1:
		weapon_list = []
		for line in f1:
			word_weapon = line.strip()
			if word_weapon not in weapon_list:
				weapon_list.append(word_weapon)

	return weapon_list


#WEAPON EXTRACTION
def weapons(para):
	prevtags=["JJ","NN","NNS","NNP","VB","VBD","VBN","VBP","VBZ","VBG",","]
	weap="-"
	sent=sent_tokenize(para)
	tag=[]
	count=0
	#print weapon_final
	for s in sent:
		words=word_tokenize(str(s))
		pos_t=pos_tag(words)	
		#print pos_t
		for i in range(len(pos_t)):
			if(i!=0):
				if((pos_t[i][1]=="NN" or pos_t[i][1]=="JJ" or pos_t[i][1]=="NNP" or pos_t[i][1]=="NNS") and pos_t[i][0] in weapon_final and count==0):
					if(pos_t[i-1][1] in prevtags):
						weap=pos_t[i][0]
						count=count+1
						break
			else:
				if(pos_t[i][0] in weapon_final):
					weap=pos_t[i][0]
					break
	#print ("WEAPON:         {}".format(weap.upper()))
	return weap

#SYNSET PAIR
def bestsynspair(w1, w2):
  
	maxsyn = -1.0
	s1 = wordnet.synsets(w1)
        s2 = wordnet.synsets(w2)
	if len(s1) == 0 or len(s2) == 0:
        	return None, None
	else:
        	maxsyn = -1.0
        	pairofwords = None, None
        	for i in s1:
        	    for j in s2:
                	max1 = wordnet.path_similarity(i, j)
               		if max1 > maxsyn:
                		maxsyn = max1
                		pairofwords = i, j
        return pairofwords


#DISTANCE(WORDS)
def ldistance(s1, s2):
 	set11=[]; set22=[]
   	distance = sys.maxint
	if s1 is None or s2 is None: 
	        return 0.0
	if s1 == s2:
	        distance = 0.0
	else:
		for ss in s1.lemmas():
	        	set11.append(str(ss.name()))
		set1=set(set11)
		for ss1 in s2.lemmas():
			set22.append(str(ss1.name()))
		set2=set(set22)
        	if len(set1.intersection(set2)) > 0:
	            	distance = 1.0
        	else:
			distance = s1.shortest_path_distance(s2)
	            	if distance is None:
        	    		distance = 0.0
	return math.exp(-A * distance)

#HIERARCHICAL DISTANCE
def hdistance(s1, s2):
	dist = sys.maxint
	if s1 is None or s2 is None: 
	        return dist
	if s1 == s2:
	        dist = max([i[1] for i in s1.hypernym_distances()])
	else:
	        h1 = {i[0]:i[1] for i in s1.hypernym_distances()}
		#print h1
	        h2 = {j[0]:j[1] for j in s2.hypernym_distances()}
	        commonterms = set(h1.keys()).intersection(set(h2.keys()))
		if len(commonterms) > 0:
			commondist = []
            		for i in commonterms:
                		d1 = 0
                		if h1.has_key(i):
                    			d1 = h1[i]
                		d2 = 0
                		if h2.has_key(i):
                   			d2 = h2[i]
                		commondist.append(max([d1, d2]))
            		dist = max(commondist)
		else:
            	 	dist = 0
	return ((math.exp(B * dist) - math.exp(-B * dist)) / (math.exp(B * dist) + math.exp(-B * dist)))
	#return dist

#WORD SIMILARITY
def word_compare(wordstok, w):
	maxsimilar=0
	for i in wordstok:
		value = bestsynspair(i, w)
		a=(ldistance(value[0], value[1]) * hdistance(value[0], value[1]))
		#maxsimilar.append(a)
		if(a>maxsimilar):
			maxsimilar=a
			maxstr=i
	#print maxsimilar
	#print maxstr 
	return maxsimilar, maxstr
		 
	
#INCIDENT MAIN	
def incidents(para):
	
	para_list=[]; individvocab={}; wordset=[]
	para_list=para
	wordtokens=word_tokenize(para_list)
	wordstok=filter(str.isalnum,wordtokens)
	maximum=0
	stopped_words = [i for i in wordstok if not i in stopwords]

	lem_incident = WordNetLemmatizer()

	for w in stopped_words:

		if lem_incident.lemmatize(w) not in wordset:
			wordset.append(str(lem_incident.lemmatize(w)))

	for i in incident_values:
		maxvalue,maxstr=word_compare(wordset,i)
		if(maximum<maxvalue):
			maximum=maxvalue
			maximumstr=i

	return maximumstr

def functioncall(paragraph,idvalue):
	outputfile.write("ID:             {}\n".format(idvalue))
	incidentvalue=incidents(paragraph)
	outputfile.write("INCIDENT:       {}\n".format(incidentvalue.upper()))
	weaponvalue=weapons(paragraph.lower())	
	outputfile.write("WEAPON:         {}\n".format(weaponvalue.upper()))
	outputfile.write("PERP INDIV:     {}\n".format("-"))
	outputfile.write("PERP ORG:       {}\n".format("-"))
	outputfile.write("TARGET:         {}\n".format("-"))
	victimvalue=victim(paragraph.lower())	
	outputfile.write("VICTIM:         {}\n\n".format(victimvalue.upper()))
	

				
def maincode():	
	id_print=[]; ids=[];count=1;paragraph=" ";line_list=[]; idcount=0
	with open(sys.argv[1]) as f1:
		for line in f1:
			id_search=search(r'(?:D|T)(?:E|S)(?:V|T)[0-9]*\-MUC[0-9]\-[0-9]{4}',line)
			line=line.rstrip()
			line_list.append(line)
			if(id_search):
				id_print.append(id_search.group())
				ids.append(line)
			
	
	for i in line_list:
		temp=i.strip()
		#print k
		if temp not in ids:
			if count<3:
				paragraph=paragraph + "".join(temp) + " "
				#print paragraph		
		else:
			count=count+1
		if(count==3):
			functioncall(paragraph,id_print[idcount])
			#print "\n"
			idcount=idcount+1
			count=2
			paragraph=" "
	functioncall(paragraph,id_print[idcount])	


#MAIN
weapon_final=weaponlist()			
maincode()
outputfile.close()
	

