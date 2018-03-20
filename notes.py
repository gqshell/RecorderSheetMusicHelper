import numpy as np
import cv2

class Note:
    """A basic note class.
    Has a string name, e.g. 'F#'.
    Each note goes with an information from a paper fingering chart, that goes with the instrument:
    what holes need to be closed\opened on the instrument to produce the note."""
    _name = ""
    _holes = []
    _staff_pos = 0
    _alternate = False

    def __init__(self, name, holes, staff_pos, alternate=False):
        self._name = name.upper().split('\\')
        self._holes = holes
        self._staff_pos = staff_pos
        self._alternate = alternate

    def compare_holes(self, holes):
        if self._holes.__len__() != holes.__len__():
            return False
        for i in xrange(holes.__len__()):
            if self._holes[i] != holes[i]:
                return False
        return True

    def compare_name(self, name):
        name = name.upper()
        for alias in self._name:
            if name == alias:
                return True
        return False

    def get_name(self):
        return self._name

    def get_holes(self):
        return self._holes

    def get_staff_pos(self):
        return self._staff_pos


class RecorderFingeringChart:
    """A class that provides interface to all notes that can be played on recorder.
    The system used is German."""
    _notes = []

    def __init__(self):
        # first octave
        self.add_note(Note("C", [1.0, 1, 1, 1, 1, 1, 1.0, 1.0], 6))
        self.add_note(Note("C#\Db", [1.0, 1, 1, 1, 1, 1, 1.0, 0.5], 6))
        self.add_note(Note("D", [1.0, 1, 1, 1, 1, 1, 1.0, 0.0], 5))
        self.add_note(Note("D#\Eb", [1.0, 1, 1, 1, 1, 1, 0.5, 0.0], 5))
        self.add_note(Note("E", [1.0, 1, 1, 1, 1, 1, 0.0, 0.0], 4))
        self.add_note(Note("F", [1.0, 1, 1, 1, 1, 0, 0.0, 0.0], 3))  # differs in baroque system
        self.add_note(Note("F#\Gb", [1.0, 1, 1, 1, 0, 1, 1.0, 1.0], 3))  # differs in baroque system
        self.add_note(Note("G", [1.0, 1, 1, 1, 0, 0, 0.0, 0.0], 2))
        self.add_note(Note("G#\Ab", [1.0, 1, 1, 0, 1, 1, 0.5, 0.0], 2))
        self.add_note(Note("A", [1.0, 1, 1, 0, 0, 0, 0.0, 0.0], 1))
        self.add_note(Note("A#\Bb", [1.0, 0, 1, 1, 1, 0, 0.0, 0.0], 1))
        self.add_note(Note("A#\Bb", [1.0, 1, 0, 1, 1, 0, 0.0, 0.0], 1, True))
        self.add_note(Note("B", [1.0, 1, 0, 0, 0, 0, 0.0, 0.0], 0))
        self.add_note(Note("B", [1.0, 0, 1, 1, 0, 0, 0.0, 0.0], 0, True))

        # second octave
        self.add_note(Note("C^", [1.0, 0, 1, 0, 0, 0, 0.0, 0.0], -1))
        self.add_note(Note("C#^\Db^", [0.0, 1, 1, 0, 0, 0, 0.0, 0.0], -1))
        self.add_note(Note("C#^\Db^", [1.0, 0, 0, 0, 0, 0, 0.0, 0.0], -1, True))
        self.add_note(Note("D^", [0.0, 0, 1, 0, 0, 0, 0.0, 0.0], -2,))
        self.add_note(Note("D#^\Eb^", [0.0, 0, 1, 1, 1, 1, 1.0, 0.0], -2))
        self.add_note(Note("E^", [0.5, 1, 1, 1, 1, 1, 0.0, 0.0], -3))
        self.add_note(Note("F^", [0.5, 1, 1, 1, 1, 0, 0.0, 0.0], -4))  # differs in baroque
        self.add_note(Note("F#^\Gb^", [0.5, 1, 1, 1, 0, 1, 0.5, 0.0], -4))  # alternate way for german system only
        self.add_note(Note("F#^\Gb^", [0.5, 1, 1, 1, 0, 1, 0.0, 1.0], -4, True))  # differs in baroque
        self.add_note(Note("G^", [0.5, 1, 1, 1, 0, 0, 0.0, 0.0], -5))
        self.add_note(Note("G#^", [0.5, 1, 1, 1, 0, 1, 1.0, 1.0], -5))  # differs in baroque
        self.add_note(Note("A^", [0.5, 1, 1, 0, 0, 0, 0.0, 0.0], -6))
        self.add_note(Note("A#^", [0.5, 1, 1, 0, 1, 1, 1.0, 0.0], -6))
        self.add_note(Note("B^", [0.5, 1, 1, 0, 1, 1, 0.0, 0.0], -7))

        # third octave
        self.add_note(Note("C^^", [0.5, 1, 0, 0, 1, 1, 0.0, 0.0], -8))
        self.add_note(Note("C#^^", [0.5, 1, 0.5, 1, 1, 0, 1.0, 1.0], -8))
        self.add_note(Note("D^^", [0.5, 1, 0, 1, 1, 0, 1.0, 0.5], -9))

    def add_note(self, note):
        if np.array(note.get_holes()).max() > 1:
            print "Invalid hole status, status must be in [0, 1]"
        else:
            self.get_notes().append(note)

    def find_note_by_holes(self, holes):
        """Finds an object of Note class with matching holes in the 'notes' array.
        Returns Object if found, None otherwise."""
        for i in xrange(self._notes.__len__()):
            note = self._notes[i]
            if note.compare_holes(holes):
                return i, note
        return -1, None

    def find_note_by_name(self, name):
        if type(name) == str:
            alias = name
        else:
            alias = name[0]
        for i in xrange(self.get_notes().__len__()):
            note = self.get_notes()[i]
            if note.compare_name(alias):
                return i, note
        return -1, None

    def get_notes(self):
        return self._notes


class RecorderSong:
    """This class stores a song."""
    _fingering_chart = None
    _song = [] # current song

    def __init__(self, sequence_of_notes=None):
        self._fingering_chart = RecorderFingeringChart()
        if sequence_of_notes is not None:
            self.append_string(sequence_of_notes)

    def add_note(self, note):
        self._song.append(note)

    def get_note(self, index):
        if index < 0 or index >= self._song.__len__():
            print "Index is out of bounds, %d" % index
            return None
        return self._song[index]

    def get_song(self):
        return self._song

    def length(self):
        return self._song.__len__()

    def append_string(self, sequence_of_notes):
        """Translates a string of the kind 'C C# D D^ D# E F F# F^ F^^...' into a best fit sequence of notes.
        'Best fit' means the octave of the next note in the sequence is based on the distance to the previous note.
        Always attempts to choose the note closest to the previous one, even if it's in a different octave.
        Returns a list of objects with Note class."""
        for substr in sequence_of_notes.split(" "):
            junk = 0
            junk, note = self._fingering_chart.find_note_by_name(substr)
            if junk < 0:
                print "There is no such note in the Recorder Fingering Chart: %s" % substr
            else:
                self.add_note(note)

    def append_from_file(self, filename):
        lines = [line.rstrip() for line in open(filename)]
        for line in lines:
            self.append_string(line)

    def to_string(self):
        s = ""
        for i in xrange(self.length()):
            s = s + self.get_song()[i].get_name()[0] + " "
        return s


class SongPrinter:
    """Prints a fingering chart for a song on a page with given width."""
    _hole_radius = 7
    _staff_spacing = 10
    _block_width = None
    _block_height = _staff_spacing * 10 + _hole_radius * 15
    _vspacing = _staff_spacing * 5
    _blocks_per_line = 16
    _page_margin = 0.05
    _canvas = None

    def __init__(self, song, width=1000, filename=None, notes_per_line=None):
        if notes_per_line is not None:
            self._blocks_per_line = notes_per_line
        self._block_width = int (round ((width - width * self._page_margin * 2) / float(self._blocks_per_line)))
        rows = song.length() / self._blocks_per_line
        if song.length() % self._blocks_per_line > 0:
            rows = rows + 1
        height = int(width * self._page_margin * 2 + rows * self._block_height + (rows - 1) * self._vspacing)
        self._canvas = np.zeros([height, width, 3], dtype=np.uint8)
        self._canvas[:] = 255
        for i in xrange(rows):
            for j in xrange(self._blocks_per_line):
                index = i * self._blocks_per_line + j
                note = song.get_note(index)
                if note is None:
                    continue
                x = width * self._page_margin + j * self._block_width
                y = width * self._page_margin + i * (self._block_height + self._vspacing)
                self._draw_block(x, y, note)
        if filename is not None:
            cv2.imwrite(filename, self._canvas)
        while True:
            cv2.imshow('SongPrinter', self._canvas)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

    def _draw_block(self, x, y, note):
        self._draw_staff(x, y, note)
        y = y + self._staff_spacing * 7
        self._draw_holes(x, y, note)

    def _draw_staff(self, x, y, note):
        # draw basic staff
        for i in xrange(5):
            p1 = (int(x), int(y + i * self._staff_spacing))
            p2 = (int(x + self._block_width), int(y + i * self._staff_spacing))
            cv2.line(self._canvas, p1, p2, (0,0,0), 1)
        # draw note symbol
        xx = x + self._block_width / 2.0
        yy = y + (4 + note.get_staff_pos()) * self._staff_spacing / 2.0
        cv2.ellipse(self._canvas, (int(xx), int(yy)), (int(self._staff_spacing / 2.0), int(self._staff_spacing / 1.5)), 75, 0, 360, (0,0,0), -1)
        direction = 1
        if note.get_staff_pos() < 0:
            direction = -1
        p1 = (int(xx + self._staff_spacing / 2.0), int(yy))
        p2 = (int(xx + self._staff_spacing / 2.0), int(yy - 3 * direction * self._staff_spacing))
        cv2.line(self._canvas, p1, p2, (0,0,0), 2)
        # draw extended staff if needed :
        # below basic staff
        if note.get_staff_pos() > 4:
            for i in xrange((note.get_staff_pos() - 4) / 2):
                p1 = (int(xx - self._staff_spacing), int(y + (i + 5) * self._staff_spacing))
                p2 = (int(xx + self._staff_spacing), int(y + (i + 5) * self._staff_spacing))
                cv2.line(self._canvas, p1, p2, (0, 0, 0), 1)
        # above basic staff
        if note.get_staff_pos() < -4:
            for i in xrange(abs(note.get_staff_pos()) / 2 - 1):
                p1 = (int(xx - self._staff_spacing), int(y - i * self._staff_spacing))
                p2 = (int(xx + self._staff_spacing), int(y - i * self._staff_spacing))
                cv2.line(self._canvas, p1, p2, (0, 0, 0), 1)

    def _draw_holes(self, x, y, note):
        blue = (255, 0, 0)
        red = (0, 0, 255)
        color = blue
        holes = note.get_holes()
        x = x + self._block_width / 2.0
        for i in xrange(holes.__len__()):
            if i == 0:
                # drawing a backside hole
                xx = x + self._hole_radius
                yy = y
                self._draw_hole(xx, yy, holes[i], self._hole_radius / 1.25, color)
            else:
                # drawing frontside holes
                if i == 4:
                    color = red
                    y = y + self._hole_radius * 0.5
                self._draw_hole(x, y + i * 2.5 * self._hole_radius, holes[i], self._hole_radius, color)

    def _draw_hole(self, x, y, status, radius, color):
        if status == 1:
            cv2.ellipse(self._canvas, (int(x), int(y)), (int(radius), int(radius)), 0, 0, 360, color, -1)
        if 0 < status < 1:
            cv2.ellipse(self._canvas, (int(x), int(y)), (int(radius), int(radius)), 0, 0, 180, color, -1)
        # black outline
        cv2.ellipse(self._canvas, (int(x), int(y)), (int(radius), int(radius)), 0, 0, 360, (0,0,0), 1)


# Example 1
# Basic example. First part of Gravity Falls intro.
# A song is read from a given string and then visually represented on a page with default width.
# If filename is specified, a picture is saved. In this instance the output file is GravityFallsExample.png

song = RecorderSong("D E F A G A C D E F E G A G F")
printer = SongPrinter(song, filename="GravityFallsExample.png")

# Example 2
# Krusty Krabs theme read from file and printed on a page with width 1024px, which then saved as Spongebob.png

# song = RecorderSong()
# song.append_from_file("Spongebob.txt")
# printer = SongPrinter(song, 1024, "Spongebob.png")
