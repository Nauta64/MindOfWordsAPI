import random

from erfa import apio
from flask import Flask
import requests
import json
from wordnik import *
from wordnik import swagger, WordApi, WordsApi
from wordnik.models.Related import Related

from objectSyn import APIObject

apiUrl = 'http://api.wordnik.com/v4'
apiKey = 'ggr25tbylicxslhdhqyqg0wwimg6e0lbk5piwzc5oqrh62aa5'
client = swagger.ApiClient(apiKey, apiUrl)
from wordnik.models import WordObject, Definition

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = r'files/'



@app.route('/<name>')
def index(name):
    return '<h1>Hola {}!<h1>'.format(name)


@app.route('/get5Word')
def word5():


    file = open('words5.txt')
    content = file.readlines()
    n = random.randint(0, 5749)
    json_string = json.dumps({"word": content[n].replace("\n","")})
    print(json_string)
    return json.loads(json_string)

@app.route('/getWord')
def word():
    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = 'ggr25tbylicxslhdhqyqg0wwimg6e0lbk5piwzc5oqrh62aa5'

    client = swagger.ApiClient(apiKey, apiUrl)
    wordApi = WordsApi.WordsApi(client)
    example: WordObject = wordApi.getRandomWord(minLength=5, maxLength=5)
    json_string = json.dumps(example.__dict__)
    return example.word
@app.route('/getDef')
def get_definition():
    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = 'ggr25tbylicxslhdhqyqg0wwimg6e0lbk5piwzc5oqrh62aa5'
    client = swagger.ApiClient(apiKey, apiUrl)
    wordApi = WordsApi.WordsApi(client)
    example: WordObject = wordApi.getRandomWord()

    wordApi = WordApi.WordApi(client)
    example: WordObject = wordApi.getDefinitions(word=example.word,
                                     sourceDictionaries='wiktionary')
    text = example[len(example)-1].text.replace("<xref>","").replace("</xref>","")

    json_string = json.dumps({"word":example[0].word,
                              "text": text})
    return json.loads(json_string)

@app.route('/getSynonym')
def get_synonym():
    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = 'ggr25tbylicxslhdhqyqg0wwimg6e0lbk5piwzc5oqrh62aa5'
    apiKey2 = 'c551e39a-4ef6-44b0-8070-51ebf8dac233'
    client = swagger.ApiClient(apiKey, apiUrl)
    wordApi = WordsApi.WordsApi(client)
    examplew: WordObject = wordApi.getRandomWord(hasDictionaryDef=True)

    wordApi = WordApi.WordApi(client)
    synon: list[Related] = wordApi.getRelatedWords(examplew.word, relationshipTypes="synonym", useCanonical=True)

    json_string = json.dumps({"word": examplew.word, "syn": synon[0].words})

    return json.loads(json_string)


@app.route('/getAntonym')
def get_antonym():
    apiUrl = 'http://api.wordnik.com/v4'
    apiKey = 'ggr25tbylicxslhdhqyqg0wwimg6e0lbk5piwzc5oqrh62aa5'
    apiKey2 = 'c551e39a-4ef6-44b0-8070-51ebf8dac233'
    client = swagger.ApiClient(apiKey, apiUrl)
    wordApi = WordsApi.WordsApi(client)
    examplew: WordObject = wordApi.getRandomWord(hasDictionaryDef=True)

    wordApi = WordApi.WordApi(client)
    synon: list[Related] = wordApi.getRelatedWords(examplew.word, relationshipTypes="antonym",useCanonical=True)

    json_string = json.dumps({"word": examplew.word, "syn": synon[0].words})

    return json.loads(json_string)
@app.route('/find=<word>')
def searchW(word):

    with open('words5.txt') as f:
        if word in f.read():
            json_string = json.dumps({"result": True})
        else:
            json_string = json.dumps({"result": False})

    return json.loads(json_string)

def obj_dict(obj):
    return obj.__dict__
if __name__ == '__main__':

    app.run(host="0.0.0.0")