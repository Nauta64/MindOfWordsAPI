import random
from flask import request, jsonify,Flask
import requests
import json

from objectSyn import APIObject

# apiUrl = 'http://api.wordnik.com/v4'
# apiKey = 'ggr25tbylicxslhdhqyqg0wwimg6e0lbk5piwzc5oqrh62aa5'
# client = swagger.ApiClient(apiKey, apiUrl)
# from wordnik.models import WordObject, Definition

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = r'files/'


@app.route('/<name>')
def index(name):
    return '<h1>Hola {}!<h1>'.format(name)


@app.route('/adduser', methods=['POST'])
def adduser():
    import json
    from os import path

    filename = 'users.json'
    listObj = []

    # Check if file exists
    if path.isfile(filename) is False:
        raise Exception("File not found")

    # Read JSON file
    with open(filename) as fp:
        listObj = json.load(fp)

    # Verify existing list
    print(listObj)

    print(type(listObj))

    listObj.append({
        request.json.get('userName'): {
            "mail": request.json.get('mail'),
            "password": request.json.get('password'),
            "wordle": {
                "won": 0,
                "lost": 0,
                "streak": {
                    "current": 0,
                    "max": 0
                }

            },
            "spell": {
                "won": 0,
                "lost": 0,
                "streak": {
                    "current": 0,
                    "max": 0
                }

            },
            "syn": {
                "won": 0,
                "lost": 0,
                "streak": {
                    "current": 0,
                    "max": 0
                }

            }
        }
    })

    # Verify updated list
    print(listObj)

    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file,
                  indent=4,
                  separators=(',', ': '))

    print('Successfully appended to the JSON file')

    return "true"

@app.route('/login', methods=['POST'])
def login():
    from os import path

    filename = 'users.json'
    listObj = []

    # Check if file exists
    if path.isfile(filename) is False:
        raise Exception("File not found")

    # Read JSON file
    with open(filename) as fp:
        listObj = json.load(fp)
    print(listObj)
    print(request.json.get('userName'))
    # Search 'brand' for women
    for usr in listObj:
        if usr.get(request.json.get('userName')):
            print("Si esta")
    print("yata")

    return "true"
@app.route('/get5Word')
def word5():
    file = open('words5.txt')
    content = file.readlines()
    n = random.randint(0, 2309)
    json_string = json.dumps({"word": content[n].replace("\n", "")})
    print(json_string)
    return json.loads(json_string)


@app.route('/getWord')
def word():
    file = open('WordKeys.txt')
    content = file.readlines()
    n = random.randint(0, 32428)
    return content[n].replace("\n", "")


@app.route('/getDef')
def get_definition():
    with open("wordsapi_sample.json") as jsonFile:
        data = json.load(jsonFile)
        file = open('WordKeys.txt')
        content = file.readlines()
        n = random.randint(0, 32428)
        jsonData = data["dictionary"][content[n].replace('\n', '')]
        print(jsonData)
        while 'definitions' not in jsonData:
            n = random.randint(0, 32428)
            jsonData = data["dictionary"][content[n].replace('\n', '')]
            print(jsonData)
        json_string = json.dumps({"word": content[n].replace('\n', ''),
                                  "def": jsonData.get('definitions')[0].get('definition')})
    return json.loads(json_string)


@app.route('/getSynonym')
def get_synonym():
    with open("wordsapi_sample.json") as jsonFile:
        data = json.load(jsonFile)
        file = open('WordKeys.txt')
        content = file.readlines()
        pos = len(content)
        hasDefinitions = False
        hasSynonyms = False
        while not hasDefinitions and not hasSynonyms:
            n = random.randint(0, pos)
            jsonData = data["dictionary"][content[n].replace('\n', '')]
            print(jsonData)
            if 'definitions' in jsonData:
                hasDefinitions = True
            else:
                hasDefinitions = False
            while not hasSynonyms and hasDefinitions:
                if isinstance(jsonData.get('definitions')[0].get('synonyms'), type(None)):
                    print(jsonData)
                    hasDefinitions = False
                else:
                    hasSynonyms = True
                    break
            if hasSynonyms:
                break
        print(jsonData)
        json_string = json.dumps({"word": content[n].replace('\n', ''),
                                  "syn": jsonData.get('definitions')[0].get('synonyms')})

    return json.loads(json_string)


@app.route('/getAntonym')
def get_antonym():
    # apiUrl = 'http://api.wordnik.com/v4'
    # apiKey = 'ggr25tbylicxslhdhqyqg0wwimg6e0lbk5piwzc5oqrh62aa5'
    # apiKey2 = 'c551e39a-4ef6-44b0-8070-51ebf8dac233'
    # client = swagger.ApiClient(apiKey, apiUrl)
    x = requests.get('https://random-word-api.herokuapp.com/word?')

    print(x.text)

    # wordApi = WordApi.WordApi(client)
    # synon: list[Related] = wordApi.getRelatedWords(examplew.word, relationshipTypes="antonym",useCanonical=True)
    #
    # json_string = json.dumps({"word": examplew.word, "syn": synon[0].words})

    return json.loads(x.text)


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
