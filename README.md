# Laser-engraving-with-Lasergrbl-and-and-Ender-3-S1-pro
This project describes how to perform laser engraving and cutting using a Creality Ender 3 S1 pro. This involves both equipping the I/O of the Ender motherboard with an opto-coupler to prevent damage during hot plug of the laser as well as python scripts to translate the G-code from Lasergrbl into code that can be digested by the Ender 3 board

If you purchased a laser in the hope of using it on an Ender 3 S1 pro with the laser engraving mode (without buying the Falcon extension) offered by the the Ender, you may have bumped into the same problems that I had.

1. Damaging the motherboard with a simple hot plug of the laser cable
   and
2. Finding that the gcode produced by lasergrbl cannot be digested by the Ender 3 S1 pro as is

Damage to the Ender motherboard

I received my Creality 5 W laser and set out to install it on my Ender. Connected evrything as described in the manual, but the laser would not come on, when the x/y-table moved. investigation showed that there was no PWM signal supplied to the laser. Further investigation in the web showed that many people had the same problem after a simple hot plug of the cable that supplies power and PWM to the laser. Obviously, the I/O that supplies the PEM signal connects to the board completely unprotected, so any voltage surge kills the I/O. To make a long story short, my motherboard was killed, and Creality refused to replace it. 50€ and a new motherboard later I decided to prevent this to happen a second time. I installed an opto coupler between motherboard and laser. The circuit and some shots, where I "stole" the 5V for the secondary side are appended inthe files. The board supplies 3.3 V PWM with 1 kHz frquency. The xyz optocoupler can handle this frequency easily with the simple circuit described. You can try to operate the Ender with a laser and w/o opto coupler, but be damn sure NEVER to hotplug the laser cable. If you kill the I/O, you will also not be able to print anymore, as this PWM is hared with the fan cooling your nozzle during 3D printing. So it is highly recommended to to this modification.
Having done this modification the laser operated well, but the. the next problems started...

Rendering and engraving software and the Ender 3 S1 pro

I shopped around to find a good solution. Unfortunately, I did not find much under Linux. For Windows the most prominent protagonists were Lasergrbl (free) and Lightburn (commercial).
Lasergrbl handles rendering of graphics well and transforms them into gcode. Unfortunately, the Ender 3 S1 pro cannot handle the gcode put out by Lasergrbl as is.
It is not well documented, what the Ender 3 S1 "eats", but it obviously handles complete commands flawlessly.
like: G1 X5.345 Y6.641 S300 F1200
Which contains info of command (G1), x-coordinate (X), y-coordinate (X), laser power (S) and feed rate (F)
Lasergrbl however does not supply complete command lines. If only the X-coordinate changes, then it supplies only an X-value, assuming that the laser cutter keeps the constant "sticky" commands and parameters.
So the approach is to run ascript that reads each new command line and, if the command or some Parameters are missing, completes them with those of the previous command. Sounds simple, but some special cases need to be handled.
Again to make a long story short, I wrote a python Script that does all this, I got it to work and I want to to supply it to other people coping with the same problems.

I cover 4 use cases: Cutting, Engraving with const. power (B/W), Engraving with varying power (photo), Run a calibration table for power and speed supplied by Lasergrbl

Workflow:
- Do the Rendering of your picture in Lasergrbl according to the use case and create gcode
- Save the gcode
- Run the python script to complete the gcode
- Load the completed file into Lasergrbl
- Run your engraving
