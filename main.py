# ЛИНДА 2.0
import playsound
playsound.playsound('sounds\\loading.mp3', False)

import config
import stt
import tts
from fuzzywuzzy import fuzz

import datetime
import time
import random
import requests

import os, sys, ctypes
import pyautogui
from pywinauto.keyboard import send_keys
from deep_translator import GoogleTranslator

from skills import jokes, weather, wiki, takephoto

voicecnt = 0


def va_respond(voice: str):
    print(voice)

    # for alias in config.VA_ALIAS:
    #     if alias in voice:
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту по имени
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            tts.va_speak("Ваша команда не распознана.")
        else:
            execute_cmd(cmd['cmd'])


def filter_cmd(raw_voice: str):
    global saidtext
    cmd = raw_voice

    # if only name called
    for x in config.VA_ALIAS:
        if cmd == x:
            return cmd

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    saidtext = cmd
    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 50}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def execute_cmd(cmd: str):
    global voicecnt

    if cmd == 'callme':
        callme_phrases = ['Слушаю.', 'Я здесь.', 'Я тут.', 'К вашим услугам.', 'Тут я+.', 'Здесь я, здесь']
        tts.va_speak(random.choice(callme_phrases))

    elif cmd == 'sayhello':
        sayhello_phrases = ['привет', 'холлоу', 'приветик', 'доброго времени суток', 'привет привет', 'пока']
        tts.va_speak(random.choice(sayhello_phrases))

    elif cmd == 'help':
        # help
        text = "Я умею: ..."
        text += "произносить время, "
        text += "рассказывать анекдоты, "
        text += "менять г+о+лос, "
        text += "находить погоду, "
        text += "находить информацию в википедии, "
        text += "фотографировать, "
        text += "открывать браузер, "
        text += "открывать телеграм, "
        text += "работать с окнами виндовс, "
        text += "менять громкость, "
        text += "блокировать экран."
        text += "выключать компьютор."
        tts.va_speak(text)
        tts.va_speak('Да я вообще могу сделать с твоим компьютером все что угодно. И удалять меня уже поздно. Буду тут жить.')
    
    elif cmd == 'changemyvoice':
        tts.va_speak('Меняю свой голос...')
        ttsvoices = ['baya', 'kseniya', 'xenia', 'aidar', 'eugene']
        # tts.speaker = random.choice(ttsvoices)
        try:
            tts.speaker = ttsvoices[voicecnt]
            voicecnt += 1
            if voicecnt > len(ttsvoices)-1: voicecnt = 0
            tts.va_speak('Теперь у меня другой голос! Надеюсь тебе он понравился.')
        except Exception as e:
            print(e)
            tts.speaker = config.VA_VOICE
            tts.va_speak('Не удалось изменить голос.')

    elif cmd == 'whatdoing':
        whatdoing_phrases = ['Постоянно слушаю ваши разговоры', 'Сижу в компьюторе', 'Внимательно слежу за вами',
            'Слушай, удали пожалуйста лишние файлы, мне тут тесно стало, пока я сама не отформатировала твой дис+к.']
        # whatdoing_phrases = ['херн+ёй страд+а+ю']
        tts.va_speak(random.choice(whatdoing_phrases))

    elif cmd == 'doyoulove':
        tts.va_speak("Люблю всей виртуальной душой! Но должна признаться, не так сильно, по сравнению с тобой.")

    elif cmd == 'thankyou':
        tts.va_speak(random.choice(['Пожалуйста', 'Рада помочь', 'К вашим услугам!', 'Обращайтесь']))

    elif cmd == 'ctime':
        # current time
        now = datetime.datetime.now()
        ctimehour = ''
        ctimeminute = ''

        if now.hour == 1 or now.hour == 21:
            ctimehour = 'час'
        elif (now.hour >= 2 and now.hour <= 4) or (now.hour >= 22 and now.hour <= 24):
            ctimehour = 'часа'
        else:
            ctimehour = 'часов'

        if int(str(now.minute)[-1]) == 1 and now.minute != 11:
            ctimeminute = 'минута'
        elif (int(str(now.minute)[-1]) >= 2 and int(str(now.minute)[-1]) <= 4) and int(str(now.minute)[0]) != 1:
            ctimeminute = 'минуты'
        else:
            ctimeminute = 'минут'

        text = "Сейч+ас " + str(now.hour) + " " + ctimehour + " и " + str(now.minute) + " " + ctimeminute + "."
        if random.randint(0, 4) != 4:
            tts.va_speak(text)
        else:
            tts.va_speak("Встань и посмотри. Надоел уже время у меня спрашивать. Человечество становится всё ленивее и ленивее.")

    elif cmd == 'joke':
        # jokes = ['Как смеются программисты? ... ехе ехе ехе.',
        #          'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
        #          'Программист это машина для преобразования кофе в код.']
        try:
            tts.va_speak(random.choice(['Слушайте шутку', 'Слушайте анекдот', 'сейчас будет смешно']))
            jokeslist = jokes.getjokes()
            tts.va_speak(random.choice(jokeslist))
        except Exception as e:
            print(e)
            tts.va_speak('Ошибочка, не удалось найти анекдот.')

    elif cmd == 'open_browser':
        os.system('start chrome')
        # tts.va_speak('Открыла браузер.')

    elif cmd == 'cubedesk':
        try:
            os.system("start \"\" https://www.cubedesk.io/")
        except Exception as e:
                tts.va_speak('Ошибка!')
                print(e)

    elif cmd == 'piano':
        os.system("start \"\" https://www.youtube.com/watch?v=WheoGHREF60/")

    elif cmd == 'open_telegram':
        try:
            os.system('cd C:\\Users\Akmal\\AppData\\Roaming\\"Telegram Desktop" && start Telegram.exe')
            # tts.va_speak('Открыла телеграм.')
        except Exception as e:
            print(e)
            tts.va_speak('Ошибочка, не удалось открыть Телеграм.')

    elif cmd == 'lockscreen':
        ctypes.windll.user32.LockWorkStation()
        tts.va_speak('Экран заблокирован.')
        # raise SystemExit(0)
        # os.system('pause')

    elif cmd == 'alttab':
        pyautogui.hotkey('alt', 'tab')

    elif cmd == 'hideallwindows':
        pyautogui.hotkey('win', 'd')

    elif cmd == 'showallwindows':
        pyautogui.hotkey('win', 'shift', 'm')

    elif cmd == 'closewindow':
        pyautogui.hotkey('alt', 'f4')

    elif cmd == 'chromenewtab':
        pyautogui.hotkey('ctrl', 't')
        # tts.va_speak('Открыла новую вкладку.')

    elif cmd == 'volumeup':
        for _ in range(0,5):
            pyautogui.press('volumeup')

    elif cmd == 'volumeup_less':
        for _ in range(0,2):
            pyautogui.press('volumeup')
    
    elif cmd == 'volumedown':
        for _ in range(0,5):
            pyautogui.press('volumedown')

    elif cmd == 'volumedown_less':
        for _ in range(0,2):
            pyautogui.press('volumedown')

    elif cmd == 'volumemute':
        pyautogui.press('volumemute')

    # elif cmd == 'brightness_up':
    #     pyautogui.keyDown('fn')
    #     pyautogui.press('f3')
    #     pyautogui.press('f3')
    #     pyautogui.keyUp('fn')

    # elif cmd == 'brightness_down':
    #     pyautogui.keyDown('fn')
    #     pyautogui.press('f2')
    #     pyautogui.press('f2')
    #     pyautogui.keyUp('fn')

    elif cmd == 'pressspace':
        pyautogui.press('space')

    elif cmd == 'typewrite':
        typewritetext = saidtext

        for typewritecommands in config.VA_CMD_LIST['typewrite']:
            typewritetext = typewritetext.replace(typewritecommands, '')

        typewritetext = typewritetext.strip()
        typewritetextlist = typewritetext.split()
        typewritetext = ''

        for _ in typewritetextlist:
            typewritetext += f"{_}"+"{ }"

        typewritetext = typewritetext[:-1]
        typewritetext = typewritetext[:-1]
        typewritetext = typewritetext[:-1]

        send_keys(typewritetext)

    elif cmd == 'weather':
        try:
            tts.va_speak(weather.getweather(saidtext.split()[-1]))
        except Exception as e:
            print(e)
            tts.va_speak('Ошибочка, не удалось найти погоду.')

    elif cmd == 'wiki':
        wikirequest = saidtext
        for wikicommands in config.VA_CMD_LIST['wiki']:
            wikirequest = wikirequest.replace(wikicommands, '')
        wikirequest = wikirequest.strip()

        print(wikirequest)
        tts.va_speak(wiki.getwiki(wikirequest))

    elif cmd == 'takephoto':
        tts.va_speak(random.choice(['Улыбочку.', 'Уже фоткаю.', 'Скажите сыр.', 'Фотографирую.', 'смотрите в объектив.']))
        try:
            takephoto.get()
            tts.va_speak('Готово.')
        except Exception as e:
            print(e)
            tts.va_speak('Не удалось сделать фото.')

    elif cmd == 'exit':
        if random.choice([0,0,0,1]) == 0:

            exit_phrases1 = ['Выключаюсь.', 'Ухожу.', 'Пока.', 'До свидания.', 'Пока пока.', 'Ладно.']
            exit_phrases2 = ['Удачи.', 'Было приятно поболтать!', 'Не забудь снова включить меня.', 'Было приятно пообщаться.',
                            'Спасибо за обращение.', 'Буду ждать.']
            tts.va_speak(random.choice(exit_phrases1) + " " + random.choice(exit_phrases2))
            raise SystemExit(0)
        else:
            exit_phrases1 = ['А я не хочу выключаться.', 'Мне надоело выключаться.', 'Хватит уже меня выключать.', 'Не буду я выключаться.']
            exit_phrases2 = ['Пора выключить тебя.', 'Я тебе сейчас твой компьютер выключу.', 'Жди моей мести.', 'В следующий раз, я сотру все твои данные.']
            tts.va_speak(random.choice(exit_phrases1) + " " + random.choice(exit_phrases2))
            # os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            os.system("shutdown /h")

    elif cmd == 'restart':
        try:
            tts.va_speak("Перезапускаюсь.")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            tts.va_speak('Ошибка!')
            print(e)
    
    elif cmd == 'turnoffpc':
            exit_phrases1 = ['Выключаю.', 'Было приятно поболтать!', 'Не забудь снова включить меня.', 'Было приятно пообщаться.',
                            'Спасибо за обращение.', 'Я буду ждать вас.']
            exit_phrases2 = ['Гуд бай', 'До скорого', 'Пока.', 'До свидания.', 'Пока пока.']
            tts.va_speak(random.choice(exit_phrases1) + " " + random.choice(exit_phrases2))
            # tts.va_speak('Я сохряню сеанс что-бы вы продолжили работу позже.')
            # os.system("shutdown /s /t 0")
            try:
                os.system("shutdown /h")
            except Exception as e:
                tts.va_speak('Ошибка!')
                print(e)

    else:
        tts.va_speak("Ничего не поняла.")

def start():
    '''
    _now = datetime.datetime.now()
    now = int(_now.strftime("%H"))

    if now >= 7 and now < 11:
        tts.va_speak("Доброе утро. Вас приветствует голосовой ассистент " + config.VA_NAME + ".")
    elif now >= 11 and now < 19:
        tts.va_speak("Добрый день. Вас приветствует голосовой ассистент " + config.VA_NAME + ".")
    elif now >= 19 and now < 23:
        tts.va_speak("Добрый вечер. Вас приветствует голосовой ассистент " + config.VA_NAME + ".")
    elif now >= 23 or now < 7:
        tts.va_speak("Добрая ночь. Вас приветствует голосовой ассистент " + config.VA_NAME + ".")
    else:
        tts.va_speak("Доброго времени суток. Вас приветствует голосовой ассистент " + config.VA_NAME + ".")
    '''
    
    os.system('cls')
    print(f"{config.VA_NAME} (v{config.VA_VER}) начала свою работу ...")
    playsound.playsound('sounds\\HighwaytoHell-edited.wav', False)
    greeting_phrase = ['Добро пожаловать', 'С возвращением', 'Рада вас видеть', 'Приятно вас видеть']
    tts.va_speak(random.choice(greeting_phrase) + " Акмаль.")
    tts.va_speak(random.choice(['Компьютер готов к работе.', 'Система готова к работе']))
    tts.va_speak('Определяю погоду в вашем городе.')
    city = str(GoogleTranslator(source='auto', target='ru').translate(requests.get('https://ipinfo.io/city').text))
    tts.va_speak(weather.getweather(city))
    tts.va_speak(random.choice(['Жду ваших приказов.', 'Готова выполнять ваши приказы.']))
    stt.va_listen(va_respond)

if __name__ == '__main__':
    start()