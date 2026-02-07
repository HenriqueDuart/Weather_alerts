import requests
import smtplib
from email.message import EmailMessage
import os

# Retrieving data via weather API
END_POINT = 'https://api.openweathermap.org/data/2.5/forecast'
API_KEY = os.environ.get('WEATHER_API_KEY')
parameters = {
    'lat':50.126391,
    'lon':8.698308,
    'appid':API_KEY,
    'units':'metric',
    'cnt':4
}
response = requests.get(END_POINT, params=parameters)
response.raise_for_status()
data = response.json()

forecasts = data['list']
city_name = data['city']['name']

# Retrieving data via twilio
email_sender = 'john.dooe993@gmail.com'
email_password = os.environ.get('JD_EMAIL_PW') # No spaces
email_receiver = ['john.dooe993@gmail.com']

smtp_server = "smtp.gmail.com"
port = 587

msg = EmailMessage()
msg['Subject'] = '[Warning] Bring an umbrella today!'
msg['From'] = email_sender
msg['To'] = email_receiver
msg.set_content(f'Please note that rain is expected today in {city_name}.\n\nYours truly, HD')


rain = False

def does_it_rain(data_set: list):
    global rain
    for forecast in data_set:
        for item in forecast['weather']:
            if item['id'] < 700:
                rain = True
    if rain:
        print('Please, bring an umbrella today!')

        with smtplib.SMTP('smtp.gmail.com', port=port) as connection:
            connection.starttls()
            connection.login(user=email_sender, password=email_password)
            connection.send_message(msg=msg)
            print('Email sent successfully')
    else:
        print(f'Does not seem like raining today in {city_name}.')


does_it_rain(forecasts)

