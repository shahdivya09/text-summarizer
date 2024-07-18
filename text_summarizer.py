import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from transformers import Pipeline
from collections import defaultdict
from transformers import pipeline
import tensorflow as tf

def absummarizer(textt):
    summarizer = pipeline("summarization")
    absummary = summarizer(textt, max_length=500, min_length=50, do_sample=False)[0]['summary_text']
    return absummary, textt , len(textt.split(' ')), len(absummary.split(' '))

def summarizer(rawdocs):
        stopwords = list(STOP_WORDS)
        #   print (stopwords)
        nlp = spacy.load('en_core_web_sm') 
        doc = nlp(rawdocs) 
        #print(doc)
        tokens = [token.text for token in doc]
        #print(tokens)
        word_freq = {}
        for word in doc:
            if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
                if word.text.lower() not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] +=1
        #print(word_freq)

        max_frq = max(word_freq.values())
        #print(max_frq)

        for word in word_freq.keys():
            word_freq[word] = word_freq[word]/max_frq #normalised freq
        #print(word_freq)

        sent_tkn = [sent for sent in doc.sents]
        

        sent_scores = {}
        for sent in sent_tkn:
            for word in sent:
                if word.text in word_freq.keys():
                    if sent not in sent_scores.keys():
                        sent_scores[sent] = word_freq[word.text]
                    else:
                        sent_scores[sent] += word_freq[word.text]
           

        select_len = int(len(sent_tkn)* 0.3)
        

        summary = nlargest(select_len, sent_scores, key=sent_scores.get)
        
        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)
        
        return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))


