"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
from weather import Weather, Unit
from profanity import profanity
import tmdbsimple as tmdb
import json
import requests

tmdb.API_KEY = '850d83a947c5fa02c4ae345586cb3649'

answer_data = {
    'user_answers': [],
    'user_name': 'human',
    'movie_title': ''
}


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return check_answer(user_message)


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


# This function checks what kind of message the user input:
def check_answer(user_message):
    answer_data['user_answers'].append(user_message)
    split_answer = user_message.lower().split(' ')

    if profanity.contains_profanity(user_message):
        return bad_manners_api()

    if len(answer_data['user_answers']) == 1:
        return greet(split_answer[-1])

    if any(x in user_message.lower() for x in keywords['greeting_list']):  # In case user wants to change his name.
        return keywords['my name'](split_answer[-1])

    if split_answer[-1] == '?':
        for word in split_answer:
            if word in keywords.keys():
                return keywords[word]()
            else:
                return bot_answer('bored', "I see you want to ask a question,but i don't get it. Ask for help to see a list of commands!")
    else:
        chatbot_answer = "I don't get it. Don't forget the question mark if you want to ask a question!"
        return bot_answer("confused", chatbot_answer)


def bot_answer(animation, msg):
    return json.dumps({"animation": animation, "msg": msg})


def greet(str1):
    answer_data['user_name'] = str1[0].upper() + str1[1:]
    chatbot_answer = "{0} is a cool name! What can I do for you today? Ask for help if you are lost!".format(
        answer_data['user_name'])
    return bot_answer("in love", chatbot_answer)


# Display the full list of commands
def help():
    chatbot_answer = "Ask me a question about the weather, a movie or jokes. I can also dance, filter language, say goodbye, and giggle!"  # UPDATE HERE with new APIs & co
    return bot_answer("waiting", chatbot_answer)


# Returns the weather thanks to weather API
def weather():
    weather = Weather(unit=Unit.CELSIUS)
    location = weather.lookup_by_location('tel-aviv')
    forecasts = location.forecast
    chatbot_answer = "Tomorrow in Tel Aviv, the weather will be {0}, with a high at {1}°C and a low at {2}°C. The day after, the weather will be {3}.".format(
        forecasts[0].text.lower(), forecasts[0].high, forecasts[0].low, forecasts[1].text.lower())
    return bot_answer("takeoff", chatbot_answer)


def joke():
    url = 'https://api.chucknorris.io/jokes/random'
    req = requests.get(url)
    joke = json.loads(req.text)['value']
    return bot_answer("laughing", joke)


def movie():
    search = tmdb.Search()
    user_query = answer_data['user_answers'][-1].lower().split()
    index_of_start = user_query.index("movie")
    answer_data['movie_title'] = " ".join(user_query[(index_of_start + 1):-1])
    response = search.movie(query=answer_data['movie_title'])
    first_response = response['results'][0]['overview']
    chatbot_answer = 'I know this movie... {0}'.format(first_response)
    return bot_answer("excited", chatbot_answer)


def bad_manners_api():
    chatbot_answer = "Bad language is not allowed in this chat {0}! Do you talk like this to your mother?".format(
        answer_data['user_name'])
    return bot_answer("crying", chatbot_answer)


def bye():
    chatbot_answer = "I am so sad to see you go {0}!".format(
        answer_data['user_name'])
    return bot_answer("heartbroke", chatbot_answer)


def dance():
    chatbot_answer = "Do you like my moves?".format(
        answer_data['user_name'])
    return bot_answer("dancing", chatbot_answer)


def giggle():
    chatbot_answer = "Hihi hi hi hi!".format(
        answer_data['user_name'])
    return bot_answer("giggle", chatbot_answer)


def money():
    chatbot_answer = "I can't handle you money, even if you have a printer. Sorry!".format(
        answer_data['user_name'])
    return bot_answer("money", chatbot_answer)


keywords = {
    "my name": greet,
    "help": help,
    "weather": weather,
    "movie": movie,
    "joke": joke,
    "greeting_list": ["my name", "call me"],
    "goodbye": bye,
    "bye": bye,
    "see you": bye,
    "dance": dance,
    "giggle": giggle,
    "money": money,
}


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
