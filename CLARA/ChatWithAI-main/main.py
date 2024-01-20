import datetime
import os
import random
import subprocess
import webbrowser

from tkinter import *

import openai
import requests
import speech_recognition as sr
import win32com.client
import json

from config import apikey, apikey2

speaker = win32com.client.Dispatch("SAPI.SpVoice")
BASE_URL = "http://api.openwethermap.org/date/2.5/weather?"


def system(query):
    ano = "You are not YUVRAJ sorry  i will not access system for you  "
    psw = "***"
    askpsw = "say verification code "
    speaker.Speak(askpsw)
    verify = takeCommand()
    if verify.lower() == psw:

        req = "Hello YUVRAJ SINGH opening system  "
        speaker.Speak(req)
        if "command prompt".lower() in query.lower():
            subprocess.call("cmd.exe")
        elif "calculator".lower() in query.lower():
            subprocess.call("calc.exe")
        elif "notepad".lower() in query.lower():
            subprocess.call("notepad.exe")
        elif "character map".lower() in query.lower():
            subprocess.call("charmap.exe")
        elif "ms paint".lower() in query.lower():
            subprocess.call("mspaint.exe")
        elif "task manager".lower() in query.lower():
            subprocess.call("taskmgr.exe")
    else:

        speaker.Speak(ano)


def weather(apikey2, city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey2}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        if weather_data:
            # Extracting relevant information from the response
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            weather_description = weather_data['weather'][0]['description']
            temp = f"Temperature: {temperature} K"
            hum = f"Humidity: {humidity}%"
            weth_des = f"Weather Description: {weather_description}"
            speaker.Speak(temp)
            speaker.Speak(hum)
            speaker.Speak(weth_des)

            print(temp)
            print(hum)
            print(weth_des)
        return weather_data
    else:
        print("Error occurred while fetching weather data.")
        return None


def ai(prompt):
    openai.api_key = apikey
    text = f"Open AI response for prompt: {prompt} \n **********\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: add try catch method

    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/prompt- {random.randint(1, 1222212)}") as f:
        f.write(text)


chatstr = ""


def chat(query):
    global chatstr
    print(chatstr)
    openai.api_key = apikey

    chatstr += f"YUVRAJ SINGH: {query} \n AI: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatstr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: add try catch method

    print(response["choices"][0]["text"])
    speaker.Speak(response["choices"][0]["text"])
    chatstr += f"{response['choices'][0]['text']}"
    return response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/prompt- {random.randint(1, 1222212)}") as f:
        f.write(text)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "some error occurred. sorry "


intro = "Hello i am  Clara"
req = "How may i help you"
speaker.Speak(intro)
speaker.Speak(req)


while 1:
    print("listening...")
    #w = Label(screen, text='GeeksForGeeks.org!')
    #w.pack()
    query = takeCommand()
    speaker.Speak(query)
    sites = [["youtube", "https://youtube.com"], ["google", "https://www.google.co.in"],
             ["wikipedia", "https://www.wikipedia.org/"], ["spotify", "https://open.spotify.com/?"]]

    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            speaker.Speak(f"Opening {site[0]}..")
            webbrowser.open(site[1])

    if "the time" in query:
        strftime = datetime.datetime.now().strftime("%H:%M:%S")
        speaker.Speak(f"The time is {strftime}")
    elif "using artificial intelligence ".lower() in query.lower():
        ai(prompt=query)
    elif "AI reset chat".lower() in query:
        chatstr = ""
    elif "the weather".lower() in query:
        ci = "sorry couldnt hear location please repeat location"
        speaker.Speak(ci)
        city_name = takeCommand()
        weather(apikey2, city_name)

    elif "open system".lower() in query.lower():
        system(query)

    elif "AI end chat".lower() in query:
        exit()
    elif "tell me about yourself".lower() in query.lower():
        myself = "My name is CLARA . I am an A I created by YUVRAJ SINGH on 4th june 2023. Now tell me how may i help you."
        speaker.Speak(myself)
    else:
        chat(query)
