# lamp_shade

Very simple animated desk lamp based on RPI Pico, that was made in a hurry... 

Prepared animations include (in order):
1. simply_on - lamp shines the brightest light possible
2. breeze - slowly oscillates between dim and bright light 
3. small_candle - emulates dynamic flame of a candle
4. big_candle - emulates more static, slow flame of a candle
5. simply_off - light is turned off

During runtime, lamp can switch between animation modes simply by pressing on the top cover, thick activates buttons in the base of a lamp, and sends signal to change animation to next in the queue.

# Set up guide
1. Install RPI Pico SDK - one approach is to use [Thonny](https://thonny.org/)
2. Flash your board with  MircroPython, it can be downloaded from official site[MircoPython download](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html), or one can use version [attached in repository](./RPI_PICO-20241129-v1.24.1.uf2)
3. Whole program is one file and does not require any custom libraries, simply run it the same way one would run [blink.py](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/5)
4. Remember to save project to pico board before switching to remote power supply. 

[3d models](https://a360.co/41rl0oj)

Problems:
1. LED's are shit, so the corelation between PWM duty cycle and brightness is not linear, I need to create function that takes that into account - This was not necessary in the end 
2. Timing is not precise (I think) this should be investigated, turns out Rpi is not as fast as I imagined, the minimal delay between PWM duty cycle changes was like 0.01s. 
3. We need proto-threads for the button to feel good - Done
4. Remodeled cover would be nice - Done Requires printing
5. Remember last animation [en example](https://electrocredible.com/rpi-pico-save-data-permanently-flash-micropython/) - Unnecessary if we have animation "OFF", PRI simply newer will be turned off 
6. Flash program to permanent storage - Done
