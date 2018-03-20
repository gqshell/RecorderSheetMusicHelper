import numpy as np
import cv2
from operator import ne, eq
import skvideo.io
import notes as rs


def toByte(value):
    if value <= 0:
        return 0
    if value >= 255:
        return 255
    return value


def getMask(color, cv2_image, range=120):
    # calculating upper and lower shades
    lower_color = np.array([toByte(color[0] - range), toByte(color[1] - range), toByte(color[2] - range)])
    upper_color = np.array([toByte(color[0] + range / 2), toByte(color[1] + range / 2), toByte(color[2] + range / 2)])
    # Threshold the HSV image to get only key colors
    mask = cv2.inRange(cv2_image, lower_color, upper_color)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel=np.ones((3,3),np.uint8))
    return mask


def getHoleStatus(mask, coord1, coord2=None):
    status = 0
    value = mask[coord1[1], coord1[0]]
    if value > 0:
        status += 1
    if coord2 is not None:
        value = mask[coord2[1], coord2[0]]
        if value > 0:
            status += 1
        status /= 2.0
    return status


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

#video = skvideo.io.vreader('The Pink Panther Theme - Recorder Notes Tutorial - La Panter.mp4')
# hole_00 = (952, 496)
# hole_01 = (970, 508)
# hole_1 = (991, 464)
# hole_2 = (1015, 488)
# hole_3 = (1041, 512)
# hole_4 = (1067, 534)
# hole_5 = (1093, 561)
# hole_60 = (1120, 586)
# hole_61 = (1147, 568)
# hole_70 = (1148, 612)
# hole_71 = (1169, 593)

song = rs.RecorderSong()
fg = rs.RecorderFingeringChart()

f1 = [1.0, 1, 1, 1, 1, 0, 1.0, 1.0]
fsharp1 = [1.0, 1, 1, 1, 0, 1, 1.0, 0.0]
f2 = [0.5, 1, 1, 1, 1, 0, 1.0, 0.0]
fsharp2 = [0.5, 1, 1, 1, 0, 1, 0.0, 0.0]
gsharp2 = [0.5, 1, 1, 0, 1, 0, 0.0, 0.0]

col = (0,0,0)
prev_row = []
skip_counter = 0
for frame in video:
    skip_counter = skip_counter + 1
    if skip_counter != 10:
        continue
    skip_counter = 0

    mask = getMask(col, frame)
    row = [
        getHoleStatus(mask, hole_00, hole_01),
        getHoleStatus(mask, hole_1),
        getHoleStatus(mask, hole_2),
        getHoleStatus(mask, hole_3),
        getHoleStatus(mask, hole_4),
        getHoleStatus(mask, hole_5),
        getHoleStatus(mask, hole_60, hole_61),
        getHoleStatus(mask, hole_70, hole_71)
    ]
    if (np.array(row).max() != 0) and any(map(ne, prev_row, row)):
        junk, note = fg.find_note_by_holes(row)

        # compensating for Baroque system F#
        if all(map(eq, f1, row)):
            junk, note = fg.find_note_by_name("F")
        elif all(map(eq, fsharp1, row)):
            junk, note = fg.find_note_by_name("F#")
        elif all(map(eq, f2, row)):
            junk, note = fg.find_note_by_name("F^")
        elif all(map(eq, fsharp2, row)):
            junk, note = fg.find_note_by_name("F#^")
        elif all(map(eq, gsharp2, row)):
            junk, note = fg.find_note_by_name("G#^")

        if note is None:
            print "There is no such note %s" % row
            cv2.imshow('frame', mask)
            while True:
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break
        else:
            song.add_note(note)

    prev_row = row

    cv2.imshow('frame', mask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

print song.to_string()
printer = rs.SongPrinter(song, 1024, "Spongebob.png")
