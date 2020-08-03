import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from heapq import nlargest


def text_summarize(raw_doc, list_score=8):
    nlp = spacy.load('en_core_web_sm')
    stopword = list(STOP_WORDS)

    raw_text = raw_doc
    docx = nlp(raw_text)

    word_frequencies = {}
    for word in docx:
        if word.text not in stopword:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/max_frequency)

    # sentence Token
    sentence_list = [sentence for sentence in docx.sents]

    # calculate sentece score and ranking
    sentence_score = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_score.keys():
                        sentence_score[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_score[sent] += word_frequencies[word.text.lower()]

    # find N largest to result summarize
    summary_sentence = nlargest(list_score,sentence_score, key=sentence_score.get)
    final_sentence = [w.text for w in summary_sentence]
    summary = ' '.join(final_sentence)
    return summary