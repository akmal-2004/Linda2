import pyowm # pyowm==2.10.0
from num2t4ru import num2text
import requests
from deep_translator import GoogleTranslator

def getweather(city):
    try:
        if city == '':
            city = str(GoogleTranslator(source='auto', target='ru').translate(requests.get('https://ipinfo.io/city').text))
        owm = pyowm.OWM('a99967bc9ee70d5b4bd387902982f400', language = "RU")
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        temperature = w.get_temperature('celsius')['temp']
    except Exception as e:
        return "Не удалось найти погоду в городе " + city + ". Попробуйте четко произнести город в конце речи"
        

    a = ("В городе " + city + " сейчас температура: " + num2text(temperature) + " градусов по Ц+eльсию.")
    b = ('Пог+ода в указаном городе: ' + w.get_detailed_status())
    return a + '\n' + b