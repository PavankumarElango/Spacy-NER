# -*- coding: utf-8 -*-
"""Doctustech_interview_task.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U4Rd3sYrW5ydNqGzeK1-E-8D-2SeAW6E

# Installing Models and Libraries
"""

#!pip install flask-ngrok
#!pip install flask==0.12.2  # Newer versions of flask don't work in Colab
#!pip install Flask-Markdown 
#! pip install spacy_stanza
#!pip install stanza
#!pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_ner_bc5cdr_md-0.4.0.tar.gz
#!pip install scispacy

#!/usr/bin/python
# -*- coding: utf-8 -*-

# @author: pavan
#1.import Libraries

from flask import Flask, url_for, render_template, request
from flaskext.markdown import Markdown
from flask_ngrok import run_with_ngrok

import spacy_stanza
import spacy
import stanza
from spacy import displacy

#import pandas as pd

# nlp_med = spacy.load("en_ner_bc5cdr_md")

HTML_WRAPPER = \
    """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
stanza.download('en', package='mimic', processors={'ner': 'i2b2'})

nlp_cli = spacy_stanza.load_pipeline('en', package='mimic',
        disable=['tagger', 'attribute_ruler', 'lemmatizer'],
        processors={'ner': 'i2b2'})

app = Flask(__name__, template_folder='templates')
Markdown(app)
run_with_ngrok(app)  # Start ngrok when app is run


@app.route('/')
def index():

    # raw_text = "Bill Gates is An American Computer Scientist since 1986"
    # docx = nlp(raw_text)
    # html = displacy.render(docx,style="ent")
    # html = html.replace("\n\n","\n")
    # result = HTML_WRAPPER.format(html)

    return render_template('index.html')


@app.route('/extract', methods=['GET', 'POST'])
def extract():
    if request.method == 'POST':
        raw_text = request.form['rawtext']
        docx = nlp_cli(raw_text)
        colors = \
            {'PROBLEM': 'linear-gradient(90deg, ##b92b27, #1565C0)',
             'TEST': 'radial-gradient(#a8ff78, #78ffd6)',
             'TREATMENT': 'radial-gradient(#2980B9, #6DD5FA)'}
        options = {'ents': ['PROBLEM', 'TREATMENT', 'TEST'],
                   'colors': colors}

        html = displacy.render(docx, style='ent', options=options)
        html = html.replace('''

''', '\n')
        result = HTML_WRAPPER.format(html)
        l2 = [(ent.start_char, ent.end_char, ent.text, ent.label_)for ent in docx.ents]
        #data = pd.DataFrame(l2, columns=['Location_start',
                          #  'Location_end', 'Entity', 'Semantics'])

        # clinical_data = data.to_csv("/content/sample_data/data")

    return render_template('result.html', rawtext=raw_text,
                           result=result)


@app.route('/previewer')
def previewer():

    return render_template('previewer.html')


@app.route('/preview', methods=['GET', 'POST'])
def preview():
    if request.method == 'POST':
        newtext = request.form['newtext']
        docx = nlp_med(newtext)
        colors = \
            {'DISEASE ': 'linear-gradient(90deg, #aa9cfc, #fc9ce7)',
             'CHEMICAL ': 'radial-gradient(yellow, green)'}
        options = {'ents': ['DISEASE', 'CHEMICAL'], 'colors': colors}

        html = displacy.render(docx, style='ent', options=options)
        html = html.replace('''

''', '\n')
        result = HTML_WRAPPER.format(html)

    return render_template('preview.html', newtext=newtext,
                           result=result)

if __name__ == '__main__':
    app.run()
