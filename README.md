# Laser Engraving with Lasergrbl and Ender 3 S1 pro
This project describes how to perform laser engraving and cutting using a Creality Ender 3 S1 pro. This involves both equipping the I/O of the Ender motherboard with an opto-coupler to prevent damage during hot plug of the laser as well as python scripts to translate the G-code from Lasergrbl into code that can be digested by the Ender 3 board. The Ender 3 S1 operates with Marlin firmware, and the developer states that Marlin-support is in an early stage and the code generated may not be compatible with the board. I can confirm this. The ender connects and communicates with Lasergrbl, but the commands are not fully compatible.

Ender 3 S1 pro offers laser capability without any extensions. I purchased a 5 W Creality laser in the hope of using it on an Ender 3 S1 pro with the laser engraving mode offered by the the printer itself (without buying the Falcon extension). My hardware configuration was
- Ender 3 S1 pro, switched to engraving mode
- Laser connected to 3 contact port with 24 V, GND and PWM
- Printer connected to a Windows 11 operated PC via USBC cable

If you did all this similarly, you may have bumped into the same problems as I did:

- Damaging your printer motherboard with a simple hot plug of the laser cable
   and
- Finding that the gcode produced by Lasergrbl cannot be digested by the Ender 3 S1 pro as is

Damage to the Ender motherboard:

I received my Creality 5 W laser and set out to install it on my Ender. Connected everything as described in the manual, but the laser would not come on, when the x/y-table moved. investigation showed that there was no PWM signal supplied to the laser. Further investigation in the web showed that many people had the same problem after a simple hot plug of the cable that supplies power and PWM to the laser. Obviously, the I/O that supplies the PWM signal connects to the board and microprocessor completely unprotected, so any voltage surge kills the I/O channel instantly. To make a long story short, my motherboard was killed, and Creality refused any responsibility. 50€ and a new motherboard later I decided to prevent this to happen a second time before I proceed. I installed an optocoupler between motherboard and laser. The circuit and some shots of the system are appended in the files. The Ender 3 board supplies a 3.3 V PWM signal with 1 kHz frequency. The PC817 opto coupler can handle this frequency easily with the simple circuit described. I "stole" the 24 V from the output socket to the laser and  regulated it doewn to 5V with L7805CV voltage regulator. With the little power absorbed by the optocoupler, no cooling is needed. You can also operate the Ender with a laser and w/o optocoupler, but be damn sure NEVER to hotplug the laser cable. If you kill the I/O, you will also not be able to print anymore, as this PWM is shared with the fan cooling your nozzle during 3D printing mode. So it will wreck your entire printer. Therefore I highly recommend to do this modification if you are serious about using your ender for Laser-Engraving.

Files provided
- Circuit_Diagram.jpg
- Ender_3_Bottom.jpg
- Steal_24V
- Breakout_Board

Having done this modification the laser operated well, but the next problems started...

Rendering and engraving software and the Ender 3 S1 pro

I shopped around to find a good solution. Unfortunately, I did not find much under Linux. For Windows the most prominent protagonists were Lasergrbl (free) and Lightburn (commercial).
Lasergrbl handles rendering of graphics very well and transforms them into gcode, which can be saved and edited. Unfortunately, the Ender 3 S1 pro cannot handle the gcode put out by Lasergrbl as is.
It is not well documented, what the Ender 3 S1 "eats", but it obviously handles unambiguous, complete commands flawlessly. 

like: G1 X5.345 Y6.641 S300 F1200
Which contains info of command (G1), x-coordinate (X), y-coordinate (Y), laser power (S) and feed rate (F)

Most programs consist of G0, G1, G2, G3, M3 and M5 statements. According to my experience, an M4 statement makes the Ender get stuck. I replaced it by "M3 I". If later all command lines contain the Sxxx info, this works fine.

Lasergrbl however does not always supply complete command lines. If only the X-coordinate changes, then it supplies only an X-value, assuming that the laser cutter keeps the constant "sticky" commands and parameters.
As I favor open source projects, the approach was to write a script that reads each new command line and, if the command or some parameters are missing, completes them with those of the previous fully valid command. Sounds simple, but some special cases needed to be handled.
Again to make a long story short, I wrote a python script that does all this, I got it to work and I want to to share it with other people coping with the same problems.

I cover 4 use cases: Cutting, Engraving with const. power (B/W), Engraving with varying power (photo), run a calibration table for power and speed generated by Lasergrbl
I do not interfere with documentation of Lasergrbl, it is well documented. I put the setting to "Marlin" for generating gcode. 
Please add any commands yourself, that you wish at the beginning and end of the gcode file, like homing or similar. Lasergrbl allows for that, or you can add it to the code.

Workflow:
- Do the rendering of your picture (jpg, png, ...) in Lasergrbl according to the use case and create the gcode
- Save the gcode in a file (xxxxx-source.nc)
- Run the python script to complete the gcode on the saved file (the script will ask you for the path to your source- and output file). Let the file extension be .nc
- Load the out- (completed) file into Lasergrbl
- Run your engraving job

Source Code of the Python Script
- Gfix1.2.py

The code is plain vanilla python. You need to adjust the pathnames to your working directory to make it work for you. after that, it should run just fine.
There are 2 flags you can set:
- Tracking mode: Each line will be processed, the results will be shown, and the code waits for enter to process the next line
- Loggin mode: A logfile is written with the input and output for each line processed for analysis later on
None of the flags affects thwe result, just the speed of processing, which should not be an issue for normal PCs.

Examples provided:

Cutting
- Snowflake.jpg
- Snowflake-source.nc
- Snowflake-out.nc

Engraving (b/w)
- BW-photo.jpg
- BW-photo-source.nc
- BW-photo-out.nc

Engraving grayscale Photographs
- Photo.jpg
- Photo-source.nc
- Photo-out.nc

Run a power/speed calibration table
- Calibration-source.nc
- Calibration-output
- Calibration.jpg

The results of the outfiles lasered into 2mm plywood
- Results.jpg


I do not claim that this is the only or the best way to work, nor that my code is perfect, but it makes my Ender3 S1 pro work with Lasergrbl.

If the developer of Lasergrbl would incorporate this algorithm or way to put out gcode (supplying complete, unambiguous command lines), the Ender would work with Lasergrbl out of the box.

It would be interesting to learn, if the generated gcode also works with other printers or with the Falcon box from Creality.

Comments welcome, have fun playing!

P.S. Watch out for your eyes, wear safety goggles, adjust laser power and speed of before you test on your system ! Mine was a 5 W laser, if yours is 20 W or higher, the absolute power put out will be much higher!
No warranty that the translated code will work on your system nor that anything may get damaged. I only tested on ender 3 S1 pro w/o falcon module.
