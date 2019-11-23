# Raspberry Pi LED Manager
It sets a led notification depending on the rain forecast.  

## Files
* `weatherRP.py` Gets forecast and sets the led state.
* `weatherRP.sh` Starts and stops service either locally or in the Raspberry Pi. It can also push local modifications in the code to the Raspberry Pi.
* `darksky_api_key.txt` You have to create this one with your DarkSky API key. You can get one [on their website](https://darksky.net/dev).

## You may want to change
* The geolocation variable `lugar` in `weatherRP.py` to point to your location of interest.
* If you set the simple mode to True, you may want to change the rain treshold. It is 0.09 chance of rain by default.
* You also need to create the `darksky_api_key.txt` file with your own API key.

## Hardware
I set up a led to the 23 pin (don't forget to add a resistor).  
By default the led blinks in loops of 2 seconds lenght, being the proportion of that time with the light on equal to the probability of rain in the current hour or the next one. It chooses the maximum probability between these two.

## Future plans
This is a proof of concept. It is still much harder to visually read the led than checking the forecast on the phone.  
At some point in the future I would like to improve it setting diferent leds in a way that is more intuitive to read and understand the forecast.
