# lamp_shade

Very simple animated desk lamp based on RPI Pico, that was made in a hurry... 

Prepared animations include (in order):
1. simply_on - lamp shines the brightest light possible
2. simply_off - light is turned off
3. breeze - slowly oscillates between dim and bright light 
4. candle - emulates flame of a candle


# Set up guide

1. Install RPI Pico SDK - one approach is to use [Thonny](https://thonny.org/)
2. Flash your board with  MircroPython, it can be downloaded from official site[MircoPython download](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html), or one can use version [attached in repository](./RPI_PICO-20241129-v1.24.1.uf2)
3. Connect to pico and run [main.py](./src/main.py) file
4. Once your scrip is running successfully, flash main.py file to the board using Thonny 

That's it!




[3d models](https://a360.co/41rl0oj)



Problems:
1. LED's are shit, so the corelation between PWM duty cycle and brightness is not linear, I need to create function that takes that into account
2. Timing is not precise (I think) this should be investigated
3. We need proto-threads for the button to feel good - Done
4. Remodeled cover would be nice - Done Requires printing
5. Remember last animation [en example](https://electrocredible.com/rpi-pico-save-data-permanently-flash-micropython/) - Unnecessary if we have animation "OFF", PRI simply newer will be turned off 
6. Flash program to permanent storage 
