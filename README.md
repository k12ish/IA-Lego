# IA-Lego

![IMG_20211013_115814](https://github.com/user-attachments/assets/d0f7f94a-b4a1-4076-9154-084469bf19d4)
![IMG_20211013_120216](https://github.com/user-attachments/assets/d3a12d33-77d8-4bf6-b04c-6f1153a66f54)


At the start of Michaelmas, I worked with two other engineers to build and program a Photocopier made from Lego.  

### Hardware
Creating the hardware was surprisingly difficult.
The print head fits a large motor and light scanner, but it must somehow hold its centre of mass above the beam.
It also has to be as small as possible, because a larger mechanism would restrict the range of available motion.

### Software
The software is really pushing Lego to its limit - We encountered latency issues where the sensors were giving us data that was about 40ms out of date, which would completely skew the resulting image.  
Ultimately this was solved by moving the print head in a way that would effectively cancel out the latency effects.

Our final prototype collected 60x more data than a competing team and could scan as well as print black and white images.
