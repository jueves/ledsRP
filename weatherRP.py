#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from darksky.api import DarkSky
from darksky.types import languages, units, weather
import time, datetime
import signal

lugar = [28.488, -16.322] # la_laguna


with open("/home/pi/weather/darksky_api_key.txt") as file_darksky:
    darksky_key = file_darksky.read()
darksky_key = darksky_key.strip()

# Preparar GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.OUT)

# Parámetros
rains = False

darksky = DarkSky(darksky_key)

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

killer = GracefulKiller()

def rainAction(rains, test=False):
    if test:
        print(rains)
    else:
        GPIO.output(23, rains)

def weatherToLed(refresh_freq=30, simple_mode=False, prob_lluvia = 0.09,
                 test=False):

    while not killer.kill_now:
        forecast = darksky.get_forecast(
               lugar[0], lugar[1],
               extend=False, # default `False`
               lang=languages.ENGLISH, # default `ENGLISH`
               units=units.AUTO, # default `auto`
               exclude=[weather.MINUTELY, weather.ALERTS] # default `[]`
               )
    
        lluvia_esta_hora = forecast.hourly.data[0].precip_probability
        lluvia_prox_hora = forecast.hourly.data[1].precip_probability
    
        max_lluvia_2h = max(lluvia_esta_hora, lluvia_prox_hora)
        rains = max_lluvia_2h>prob_lluvia
        
        if simple_mode:  
            # Set value to LED
            rainAction(rains, test)
            time.sleep(refresh_freq*60)
        else:
            iteration_end = (datetime.datetime.now() +
                             datetime.timedelta(minutes=refresh_freq))
            
            # Se mantiene iterando hasta que pasen refresh_freq minutos.
            # El parpadeo mantiene encendido el porcentaje de prob de lluvia y apagado
            # el opuesto.
            while (not killer.kill_now) and (datetime.datetime.now() < iteration_end):
                rainAction(True, test)
                time.sleep(2*max_lluvia_2h)
                #GPIO.output(23, False)
                rainAction(False, test)
                time.sleep((1-max_lluvia_2h)*2)
    if not test:           
        GPIO.cleanup()
    else:
        print("Simulated cleanup.")

weatherToLed()
