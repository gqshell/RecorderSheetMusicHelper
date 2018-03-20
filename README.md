# RecorderSheetMusicHelper
## note.py
A lot of flute beginners have trouble reading sheet music. It takes a lot of practice to be able to play the song without looking into recorder fingering chart. 

This program translates keyboard-written notes (C D E F# etc) into a recorder fingering chart that displays what holes need to be covered to extract each specific note in the given string. The system used is German.

### Example 1
First part of Gravity Falls intro. A song is read from a given string and then visually represented on a page with default width. If filename is specified, a picture is saved. In this instance the output file is [GravityFallsExample.png](/GravityFallsExample.png)

    song = RecorderSong("D E F A G A C D E F E G A G F")
    printer = SongPrinter(song, filename="GravityFallsExample.png")

Result:
![Alt text](/GravityFallsExample.png?raw=true)

### Example 2
Some songs are bigger than others, and it's more convenient to read them from a file rather then provide a very long string for input.

Krusty Krabs theme read from file and printed on a page with width 1024px, which then saved as Spongebob.png

    song = RecorderSong()
    song.append_from_file("Spongebob.txt")  
    printer = SongPrinter(song, 1024, "Spongebob.png")
    
Result: see [the Spongebob.png](/Spongebob.png)

## videoProcessing.py
Sometimes it's hard to find a music sheet for the song you want, and the only place where you can obtain the notes is YouTube tutorials. However, [some of the creators](https://www.youtube.com/watch?v=L-H_XDpiLD0) of such tutorials don't bother sharing the keyboard-written notes for the song they play, representing them graphically note-by-note as they play it instead.

This way of giving out the notes one-by-one is extremely inconvenient and forces you to either replay the video dozens of times, or put it on a very slow playback, so you could write down the notes. 

But then there is another problem: the author didn't explicitly specify the octaves of the notes displayed on the screen, so the only way to tell the octave is to look at the holes covered. Telling the octave that way requires certain skill and is impossible for beginners.

To be more specific, a "C" note can be played in three different octaves on the recorder. To distinguish octaves in this program `^` symbol is used. E.g. "C" is the first octave, "C^" is the second and "C^^" is the third.

The videoProcessing.py file was created to obtain the correct notes from [this Krusty Krabs theme tutorial](https://www.youtube.com/watch?v=L-H_XDpiLD0). 

    hole_00 = (337, 323)
    hole_01 = (337, 328)
    hole_1 = (386, 325)
    hole_2 = (386, 369)
    hole_3 = (386, 417)
    hole_4 = (386, 456)
    hole_5 = (386, 499)
    hole_60 = (380, 532)
    hole_61 = (392, 533)
    hole_70 = (379, 574)
    hole_71 = (391, 575)
    
are the video-specific coordinates of the corresponding holes of the recorder. Some of the holes either have two sub-holes or can be covered only partly, so two coordinates are used to determine the whole state. 

Fully covered hole is represented as 1.0, fully opened is 0.0, and 0.5 stands for partially covered. In this implementation the hole is considered covered if the color of the given pixel is black. However, some adjustments can be easily done to use any other color or even invert the consideration (e.g. if the hole is not black, it's covered).

The system used in the video is Baroque (the author didn't bother to mention about it as well, so I had to learn it the hard way), so some adjustments had to be done to convert it to German system.

To speed up the processing, only each 10th frame is processed. I also had to install `scikit-video` module for video processing, because video-reading-related functions provided in `cv2` do nothing and appear to be a placeholder without implementation.

    video = skvideo.io.vreader('Krusty Krab Recorder Tutorial - YouTube.mp4')
    hole_00 = (337, 323)
    hole_01 = (337, 328)
    hole_1 = (386, 325)
    hole_2 = (386, 369)
    hole_3 = (386, 417)
    hole_4 = (386, 456)
    hole_5 = (386, 499)
    hole_60 = (380, 532)
    hole_61 = (392, 533)
    hole_70 = (379, 574)
    hole_71 = (391, 575)
    print song.to_string()

The result of `print song.to_string()` can be found in [Spongebob.txt](/Spongebob.txt)
