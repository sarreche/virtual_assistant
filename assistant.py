# pyttsx3 is a text-to-speech conversion library in Python. 
import pyttsx3
# Library for performing speech recognition, with support for several engines and APIs, online and offline.
import speech_recognition as sr
# PyWhatKit is a Python library with various helpful features. It's easy-to-use and does not require you to do any additional setup.
import pywhatkit
# yfinance is a Python library that allows users to access financial data from Yahoo Finance.
import yfinance as yf
# pyjokes is a Python library that provides jokes in various languages.
import pyjokes
# webbrowser is a Python module that provides a high-level interface to allow displaying Web-based documents to users.
import webbrowser
# datetime is a module for manipulating dates and times in both simple and complex ways.
import datetime
# wikipedia is a Python library that allows you to access and retrieve information from Wikipedia.
import wikipedia


# voice/language options
#id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
#id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# Listen to the microphone and return the audio as text
def transform_audio_to_text():


    # store recognizer in variable
    r = sr.Recognizer()

    # configure the microphone
    with sr.Microphone() as source:

        # waiting time
        r.pause_threshold = 0.8

        # inform that recording has started
        print("You can speak now")

        # save what is heard as audio
        audio = r.listen(source)

        try:
            # Performs speech recognition on audio_data (an AudioData instance), using the Google Speech Recognition API.
            pedido = r.recognize_google(audio, language="es-ar")


            # test that input was received
            print("You said: " + pedido)

            # return request
            return pedido


        # if audio is not understood
        except sr.UnknownValueError:

            # test that audio was not understood
            print("Oops, I didn't understand")

            # return error
            return "still waiting"


        # if request cannot be resolved
        except sr.RequestError:

            # test that service is unavailable
            print("Oops, no service")

            # return error
            return "still waiting"


        # unexpected error
        except:

            # test that something went wrong
            print("Oops, something went wrong")

            # return error
            return "still waiting"



# Function for the assistant to speak
def speak(message):


    # turn on pyttsx3 engine
    engine = pyttsx3.init()
    #engine.setProperty('voice', id3)

    # speak message
    engine.say(message)
    engine.runAndWait()



# Inform the day of the week
def get_day():


    # create variable with today's date
    today = datetime.date.today()
    print(today)

    # create variable for weekday
    weekday = today.weekday()
    print(weekday)

    # dictionary with day names
    calendar = {0: 'Monday',
                1: 'Tuesday',
                2: 'Wednesday',
                3: 'Thursday',
                4: 'Friday',
                5: 'Saturday',
                6: 'Sunday'}

    # say the day of the week
    speak(f'Today is {calendar[weekday]}')



# Inform the current time
def get_time():


    # create a variable with current time data
    now = datetime.datetime.now()
    time_str = f'At this moment it is {now.hour} hours, {now.minute} minutes and {now.second} seconds'
    print(time_str)

    # say the time
    speak(time_str)



# Initial greeting function
def initial_greeting():


    # create variable with current hour
    now = datetime.datetime.now()
    if now.hour < 6 or now.hour > 20:
        moment = 'Good evening'
    elif 6 <= now.hour < 13:
        moment = 'Good morning'
    else:
        moment = 'Good afternoon'

    # say the greeting
    speak(f'{moment}, I am Helena, your personal assistant. Please tell me how I can help you')



# Main assistant function
def main_loop():


    # activate initial greeting
    initial_greeting()

    # loop control variable
    running = True

    # main loop
    while running:

        # activate microphone and save request as string
        request = transform_audio_to_text().lower()

        if 'open youtube' in request:
            speak('Sure, opening YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'open browser' in request:
            speak('Of course, opening browser')
            webbrowser.open('https://www.google.com')
            continue
        elif "what day is today" in request:
            get_day()
            continue
        elif "what time is it" in request:
            get_time()
            continue
        elif 'search wikipedia' in request:
            speak('Searching that on Wikipedia')
            request = request.replace('search wikipedia', '')
            wikipedia.set_lang('en')
            result = wikipedia.summary(request, sentences=1)
            speak('Wikipedia says the following:')
            speak(result)
            continue
        elif 'search internet' in request:
            speak('Searching the internet now')
            request = request.replace('search internet', '')
            pywhatkit.search(request)
            speak('This is what I found')
            continue
        elif 'play' in request:
            speak('Good idea, starting playback')
            pywhatkit.playonyt(request)
            continue
        elif 'joke' in request:
            speak(pyjokes.get_joke('en'))
            continue
        elif 'stock price' in request:
            stock = request.split('of')[-1].strip()
            portfolio = {'apple':'APPL',
                         'amazon':'AMZN',
                         'google':'GOOGL'}
            try:
                searched_stock = portfolio[stock]
                searched_stock = yf.Ticker(searched_stock)
                current_price = searched_stock.info['regularMarketPrice']
                speak(f'Found it, the price of {stock} is {current_price}')
                continue
            except:
                speak("Sorry, I couldn't find it")
                continue
        elif 'goodbye' in request:
            speak("I'm going to rest, let me know if you need anything")
            break


main_loop()