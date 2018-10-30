import speech_recognition as sr 
from time import ctime
import time
import os
from gtts import gTTS 
import sys
import pyowm
import json
import googlemaps
import wikipedia
from file_writing_module import *

keywords_start=['okay computer','ok computer'] 

owm= pyowm.OWM(all_apis().get_apis()[1])

def speak(audiostring):
    "Enables the microphone for output data its basically a text to speech"
    print (audiostring)
    tts= gTTS(text=audiostring, lang='en')
    tts.save('./talk_speech/audio.mp3')
    os.system("mpg321 ./talk_speech/audio.mp3")

def welcome_msg():
    "print welcome msg first when jarvis starts up"
    welcome_message =  """
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++  Welcome to JARVIS.  ++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                                                              +
+                 Say 'Jarvis' to start!                +
+                                                              +
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	"""
    print (welcome_message)

def recordAudio():


    r= sr.Recognizer()
    m=sr.Microphone()
    m.CHUNK = 8192

    with m as source:
        print ("Say Something!!")
        audio= r.listen(source)
    # Speech recognition using Google Speech Recognition 
    data= ""
    try:
        data= r.recognize_google(audio)
        print ("You said:"+data)
    except sr.UnknownValueError:
        print ("Google Speech could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return data 


def jarvis_weather(location_name):
    obs= owm.weather_at_place(location_name.lower()) 
    w= obs.get_weather()
    weather_status= w.get_status()
    weather_status= weather_status + 'y'
    speak('Its %d' %(w.get_temperature('celsius')['temp']))
    speak( 'degree celsius here at %s' %(location_name))
    speak('with %s weather' %(weather_status)) 

def find_location(location_geo):
    gmaps = googlemaps.Client(key=all_apis().get_apis()[0])
    res= gmaps.geocode(location_geo)
    cntry= res[0]['address_components'][2]['long_name']
    return cntry

def jarvis_wiki(topic):
    speak("top five results are following which one would you like to know")
    print (wikipedia.search(topic)[:5])
    enter_topic= recordAudio()
    speak("here is a short summary")
    print (wikipedia.summary(enter_topic))

def main(data):
    bye_key=['bye','ok bye']
    for words in bye_key:
        if words in data:
            speak("see you soon")
            sys.exit(1) 

    weather_key=["what is the weather at","how is the weather at"]
    for words in weather_key:
        if words in data:
            location= data.split(' at ')[1]
            jarvis_weather(location) 

    if "where is" in data:
        location_geo= data.split(' is')[1]
        speak('Its in %s'%(find_location(location_geo))) 

    search_key=['wiki search','search'] 
    for words in search_key:
        if words in data:
            speak("who or what topic would you like to search") 
            topic= recordAudio()
            jarvis_wiki(topic) 

    if "thanks" in data:
        speak("pleasure")

    


welcome_msg()
data1= recordAudio() 
if "Jarvis" in data1:
    speak("hey there how can i help you")
else:
    speak("exiting now since start not initiated")
    sys.exit(1)


while 1:
    data= recordAudio() 
    main(data)

         
        


