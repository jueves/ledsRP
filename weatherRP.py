#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 18:11:56 2019

@author: luis
"""

import RPi.GPIO as GPIO
from darksky.api import DarkSky
from darksky.types import languages, units, weather
import time
import datetime

with open("darksky_api_key.txt") as file_darksky:
    darksky_key = file_darksky.read()
darksky_key = darksky_key.strip()

# Preparar GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.OUT)





# Parámetros
lugar = [28.488, -16.322] # la_laguna
rains = False

darksky = DarkSky(darksky_key)

initial_time = datetime.datetime.now()

default_end_time = datetime.datetime(initial_time.year, initial_time.month,
                                     initial_time.day+1, 3, 0)

test_time = datetime.datetime(initial_time.year, initial_time.month,
                                     initial_time.day, 19, 0)



def rainAction(rains, test=False):
    if test:
        print(rains)
    else:
        GPIO.output(23, rains)

def weatherToLed(refresh_freq=30, end_time=default_end_time, simple_mode=True,
                 prob_lluvia = 0.05, test=False):

    while datetime.datetime.now() < end_time:
    
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
            while datetime.datetime.now() < iteration_end:
                rainAction(rains, test)
                time.sleep(2*max_lluvia_2h)
                #GPIO.output(23, False)
                rainAction(not rains, test)
                time.sleep((1-max_lluvia_2h)*2)

    if not test:           
        GPIO.cleanup()

weatherToLed(prob_lluvia=0.09, simple_mode=False)