import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import pyjokes


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print("listening....")
            talk('sri im listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'kiko' in command:
                command = command.replace('kiko', '')
                print(command)
    except:
        pass
    return command


def run_kiko():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M %p')
        print(time)
        talk('Current time is ' + time)

    elif 'call' in command:
        import requests

        # Twilio API credentials
        account_sid = 'AC2601f69b69654262612522bcb7966a31'
        auth_token = '45cf00f53dced8a469a21d7c9ff5c6d3'

        # Phone numbers
        from_number = '+13159037812'
        to_number = '+918778209692'

        twiml = f'<Response><Dial>{to_number}</Dial></Response>'

            # Twilio API URL
        api_url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Calls.json'

            # HTTP POST request to make a call
        response = requests.post(api_url, auth=(account_sid, auth_token), data={
            'From': from_number,
            'To': to_number,
           'Twiml': twiml
        })

            # Check the response status
        if response.status_code == 201:
            talk('Call initiated successfully.')
        else:
            talk(f'Call could not be initiated. Error: {response.text}')



    elif 'joke' in command:
        print(pyjokes.get_joke())
        talk(pyjokes.get_joke())
    else:
        talk('Please say the command again.')


while True:
    run_kiko()
