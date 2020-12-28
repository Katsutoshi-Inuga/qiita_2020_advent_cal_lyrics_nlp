# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 10:20:48 2020

@author: innse
"""

import pandas as pd
import spacy
from spacy import displacy

import nlplot
import plotly
from plotly.subplots import make_subplots

nlp = spacy.load('ja_ginza')
df_yuming = pd.read_pickle('../../data/lyrics/m.matsutouya/lyrics.pkl')
df_miyuki = pd.read_pickle('../../data/lyrics/m.nakajima/lyrics.pkl')

def make_words_list(text: str) -> list:
    rs = []
    doc = nlp(text)
    for sent in doc.sents:
        for token in sent:
            tag = token.tag_.split('-')[0]
            if tag in ['名詞','形容詞','動詞']:
#            if tag in ['名詞']:
                rs.append(token.lemma_)
    return rs


def show_displacy(text):
    doc = nlp(text)
    displacy.serve(doc, style='dep')

    
def make_n_gram_fig(npt_artist,ngram,title):
    return npt_artist.bar_ngram(
    title=title,
    xaxis_label='word_count',
    yaxis_label='word',
    ngram=ngram,
    top_n=50)

def make_n_gram_tree_map_fig(npt_artist,ngram,title):
    return npt_artist.treemap(
    title=title,
    ngram=ngram,
    top_n=50)

def make_word_cloud(npt_artist):
    return npt_artist.wordcloud()

def make_co_occurrence_nw(npt_artist):
    npt_artist.build_graph(min_edge_frequency=25)
    npt_artist.co_network(
        title='Co-occurrence network',
    )
    return npt_artist

def make_sunburst(npt_artist,title_text):
    npt_artist.build_graph(min_edge_frequency=25)
    npt_artist.co_network(
        title='Co-occurrence network',
    )

    return npt_artist.sunburst(title=title_text)

def show_fig_2in1(yuming_fig,miyuki_fig,title_text):
    trace1 = yuming_fig['data'][0]
    trace2 = miyuki_fig['data'][0]
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=('#松任谷由実', '#中島みゆき'), shared_xaxes=False)
    fig.update_xaxes(title_text='word count', row=1, col=1)
    fig.update_xaxes(title_text='word count', row=1, col=2)

    fig.update_layout(height=1100, width=1900, title_text=title_text)
    fig.add_trace(trace1, row=1, col=1)
    fig.add_trace(trace2, row=1, col=2)
    # plotly.offline.plot(fig, filename='unigram.html', auto_open=False)    
    fig.show()
    

def n_gram(npt_yuming,npt_miyuki):
    # unigram
    yuming_fig1 = make_n_gram_fig(npt_yuming,1,'yuming_unigram')
    miyuki_fig1 = make_n_gram_fig(npt_miyuki,1,'miyuki_unigram') 
    show_fig_2in1(yuming_fig1,miyuki_fig1,title_text='unigram #松任谷由実 vs. #中島みゆき')

    # bigram
    yuming_fig2 = make_n_gram_fig(npt_yuming,2,'yuming_bigram')
    miyuki_fig2 = make_n_gram_fig(npt_miyuki,2,'miyuki_bigram') 
    show_fig_2in1(yuming_fig2,miyuki_fig2,title_text='bigram #松任谷由実 vs. #中島みゆき')

    # # trigram
    # yuming_fig3 = make_n_gram_fig(npt_yuming,3,'yuming_bigram')
    # miyuki_fig3 = make_n_gram_fig(npt_miyuki,3,'miyuki_bigram') 
    # show_fig_2in1(yuming_fig3,miyuki_fig3,title_text='trigram #松任谷由実 vs. #中島みゆき')
    
def n_gram_tree_map(npt_yuming,npt_miyuki):
    # unigram
    yuming_fig1 = make_n_gram_tree_map_fig(npt_yuming,1,'yuming_unigram')
    miyuki_fig1 = make_n_gram_tree_map_fig(npt_miyuki,1,'miyuki_unigram') 
    plotly.io.show(yuming_fig1)
    plotly.io.show(miyuki_fig1)
    # show_fig_2in1(yuming_fig1,miyuki_fig1,title_text='unigram #松任谷由実 vs. #中島みゆき')

    # bigram
    yuming_fig2 = make_n_gram_tree_map_fig(npt_yuming,2,'yuming_bigram')
    miyuki_fig2 = make_n_gram_tree_map_fig(npt_miyuki,2,'miyuki_bigram') 
    plotly.io.show(yuming_fig2)
    plotly.io.show(miyuki_fig2)
    # show_fig_2in1(yuming_fig2,miyuki_fig2,title_text='bigram #松任谷由実 vs. #中島みゆき')

def word_cloud(npt_yuming,npt_miyuki):
    make_word_cloud(npt_yuming)
    make_word_cloud(npt_miyuki)

def co_occurrence_nw(npt_yuming,npt_miyuki):
    make_co_occurrence_nw(npt_yuming)
    make_co_occurrence_nw(npt_miyuki)

def sunburst(npt_yuming,npt_miyuki):
    plotly.io.show(make_sunburst(npt_yuming,title_text='松任谷由実'))
    plotly.io.show(make_sunburst(npt_miyuki,title_text='中島みゆき'))
    
def main():
    df_yuming['words'] = df_yuming.lyric.apply(make_words_list)
    npt_yuming = nlplot.NLPlot(df_yuming, target_col='words')
    
    df_miyuki['words'] = df_miyuki.lyric.apply(make_words_list)
    npt_miyuki = nlplot.NLPlot(df_miyuki, target_col='words')
    
    n_gram(npt_yuming,npt_miyuki)
    n_gram_tree_map(npt_yuming,npt_miyuki)
    word_cloud(npt_yuming,npt_miyuki)
    co_occurrence_nw(npt_yuming,npt_miyuki)
    sunburst(npt_yuming,npt_miyuki)
main()