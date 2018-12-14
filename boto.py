"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
from weather import Weather, Unit
import json

answer_data = {
    'greeting': ["my name"],
    'counter': 0,  # might delete that
    'user_answers': []
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
    split_answer = user_message.split()

    if len(answer_data['user_answers']) == 1:
        return greet(split_answer[-1])

    for x in answer_data['greeting']:  # In case user wants to change his name... not very useful
        if x in user_message:
            return greet(split_answer[-1])

    for x in split_answer:  # In case user wants to change his name... not very useful
        if x == "help":
            return help()
        elif x == "weather":
            return weather_api()
        # OTHERS CHECKS HERE


def greet(str1):
    chatbot_answer = "{0} is a cool name! What can I do for you today? Ask for help if you are lost!".format(str1)
    return json.dumps({"animation": "inlove", "msg": chatbot_answer})


def help():
    chatbot_answer = "I can: predict the weather, get quotes, tell a joke, talk about a movie, etc..."  # UPDATE HERE with new APIs & co
    return json.dumps({"animation": "waiting", "msg": chatbot_answer})


# Returns the weather thanks to weather API
def weather_api():
    weather = Weather(unit=Unit.CELSIUS)

    location = weather.lookup_by_location('tel-aviv')
    forecasts = location.forecast
    chatbot_answer = "Tomorrow in Tel Aviv, the weather will be {0}, with a high at {1} and a low at {2}. The day after, the weather will be {3}.".format(
        forecasts[0].text.lower(), forecasts[0].high, forecasts[0].low, forecasts[1].text.lower())
    return json.dumps({"animation": "excited", "msg": chatbot_answer})


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
