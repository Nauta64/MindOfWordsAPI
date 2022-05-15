import random
from flask import request, jsonify, Response, Flask
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
        f"{len(listObj) + 1}": {
            "name": request.json.get('userName'),
            "mail": request.json.get('mail'),
            "password": request.json.get('password'),
            "image": "",
            "wordle": {
                "won": 0,
                "lost": 0,
                "streak": {
                    "current": 0,
                    "max": 0
                },
                "guessDistribution": [0, 0, 0, 0, 0, 0],
                "lastGuess": 0,
                "lastBoard": ""

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
    correct = False
    # Check if file exists
    if path.isfile(filename) is False:
        raise Exception("File not found")

    # Read JSON file
    with open(filename) as fp:
        listObj = json.load(fp)
    print(listObj)
    print(request.json.get('userName'))
    # Search 'brand' for women
    user = {}
    count = 0
    for usr in listObj:
        print(usr[f"{count}"]['name'])
        if usr[f"{count}"]['name'] == request.json.get('userName'):
            correct = True
            user = {'userName': usr[f"{count}"]['name'],
                    'password': usr[f"{count}"]['password'],
                    'mail': usr[f"{count}"]['mail'],
                    'img': usr[f"{count}"]['image'] }
            break
        count += 1
    json_string = json.dumps(user)
    print(json_string)
    if correct is True:
        return json.loads(json_string)
    else:
        return Response(
            "No record Found",
            status=400,
        )


@app.route('/getStatsWordle', methods=['POST'])
def getstatsW():
    filename = 'users.json'
    with open(filename) as fp:
        listObj = json.load(fp)
    wordle = {}
    # print(request.json.get('userName'))
    # Search 'brand' for women
    count = 0
    for usr in listObj:
        print(usr[f"{count}"]['name'])
        if usr[f"{count}"]['name'] == request.json.get('userName'):
            print(usr.get("name"))
            wordle = {"stat": usr[f"{count}"]['wordle']}
            break
        else:
            wordle = {"stat": listObj[0]["0"]['wordle']}
        count += 1

    json_string = json.dumps(wordle)
    print(json_string)
    return json.loads(json_string)


@app.route('/setimage', methods=['POST'])
def setimage():
    filename = 'users.json'
    with open(filename) as fp:
        listObj = json.load(fp)
    wordle = {}
    # print(request.json.get('userName'))

    print(request.json.get('stat'))
    count = 0
    for usr in listObj:
        print(usr[f"{count}"]['name'])
        if usr[f"{count}"]['name'] == request.json.get('userName'):
            print(usr.get("name"))
            usr[f"{count}"]['image'] = request.json.get('img')
        count += 1
    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file,
                  indent=4,
                  separators=(',', ': '))
    return "true"


@app.route('/setStatsWordle', methods=['POST'])
def setstatsW():
    filename = 'users.json'
    with open(filename) as fp:
        listObj = json.load(fp)
    wordle = {}
    # print(request.json.get('userName'))

    print(request.json.get('stat'))
    count = 0
    for usr in listObj:
        print(usr[f"{count}"]['name'])
        if usr[f"{count}"]['name'] == request.json.get('userName'):
            print(usr.get("name"))
            usr[f"{count}"]['wordle'] = request.json.get('stat')
        count += 1
    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file,
                  indent=4,
                  separators=(',', ': '))

    return "true"


@app.route('/getStatsSyn', methods=['POST'])
def getstatsS():
    filename = 'users.json'
    with open(filename) as fp:
        listObj = json.load(fp)
    synonym = {}
    # print(request.json.get('userName'))
    # Search 'brand' for women
    count = 0
    for usr in listObj:
        print(usr[f"{count}"]['name'])
        if usr[f"{count}"]['name'] == request.json.get('userName'):
            print(usr.get("name"))
            synonym = {"stat": usr[f"{count}"]['syn']}
            break
        else:
            synonym = {"stat": listObj[0]["0"]['wordle']}
        count += 1
    json_string = json.dumps(synonym)
    print(json_string)
    return json.loads(json_string)


@app.route('/setStatsSyn', methods=['POST'])
def setstatsS():
    filename = 'users.json'
    with open(filename) as fp:
        listObj = json.load(fp)
    wordle = {}
    # print(request.json.get('userName'))

    print(request.json.get('stat'))
    count = 0
    for usr in listObj:
        print(usr[f"{count}"]['name'])
        if usr[f"{count}"]['name'] == request.json.get('userName'):
            print(usr.get("name"))
            usr[f"{count}"]['syn'] = request.json.get('stat')
        count += 1

    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file,
                  indent=4,
                  separators=(',', ': '))

    return "true"


@app.route('/getStatsSpell', methods=['POST'])
def getstatsSpell():
    filename = 'users.json'
    with open(filename) as fp:
        listObj = json.load(fp)
    spell = {}
    # print(request.json.get('userName'))
    # Search 'brand' for women
    count = 0
    for usr in listObj:
        print(usr[f"{count}"]['name'])
        if usr[f"{count}"]['name'] == request.json.get('userName'):
            print(usr.get("name"))
            spell = {"stat": usr[f"{count}"]['spell']}
            break
        else:
            spell = {"stat": listObj[0]["0"]['spell']}
        count += 1
    json_string = json.dumps(spell)
    print(json_string)
    return json.loads(json_string)


@app.route('/setStatsSpell', methods=['POST'])
def setstatsSpell():
    filename = 'users.json'
    with open(filename) as fp:
        listObj = json.load(fp)
    # print(request.json.get('userName'))

    print(request.json.get('stat'))
    count = 0
    for usr in listObj:
        print(usr[f"{count}"]['name'])
        if usr[f"{count}"]['name'] == request.json.get('userName'):
            print(usr.get("name"))
            usr[f"{count}"]['spell'] = request.json.get('stat')
        count += 1

    with open(filename, 'w') as json_file:
        json.dump(listObj, json_file,
                  indent=4,
                  separators=(',', ': '))

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
