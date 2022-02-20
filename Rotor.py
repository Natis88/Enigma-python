
from Reader import *

ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rings = reader.read_json("rings.json")


class Rotor:
    name: str
    cypher: str
    notch: chr
    position: chr
    settings: chr

# Fully parametrize constructor
    def __init__(self, name, position, settings):
        self.name = name
        self.cypher = rings[name]["cipher"]
        self.notch = rings[name]["notch"]
        self.position = position
        self.settings = settings
        self._initialize()

# Initialize rotor by the given settings
    def _initialize(self):
        self.cypher = Rotor.caesarShift(
            self.cypher, ALPHA.index(self.settings))
        self.cypher = Rotor._rotate(self.cypher, ALPHA.index(self.settings))

# Check if rotor position is at notch
    def at_notch(self):
        return self.notch == self.position

    @staticmethod
    def caesarShift(string, shift):  # caesarShift on the given string

        cipher = ''
        for char in string:
            if char == ' ':
                cipher += char
            elif char.isupper():
                cipher += chr((ord(char) + shift - 65) % len(ALPHA) + 65)
            else:
                cipher += chr((ord(char) + shift - 97) % len(ALPHA) + 97)

        return cipher
# Revers the string by offset

    @staticmethod
    def _rotate(text: str, offset: int):

        if offset > 0:
            return text[len(ALPHA)-offset:] + text[0:len(ALPHA)-offset]
        return text

    # Increment position by 1
    def turn(self):
        self.position = ALPHA[((ALPHA.index(self.position)) + 1) % len(ALPHA)]

    # Encode string first:ALPHA,second:cypher
    def forward_encode(self, letter: chr):
        return Rotor._encode_letter(letter, self.position, ALPHA, self.cypher)

    # Encode string first:cypher,second:ALPHA
    def backward_encode(self, letter: chr):
        return Rotor._encode_letter(letter, self.position, self.cypher, ALPHA)
    # Return encoded character

    @staticmethod
    def _encode_letter(letter: chr, position: chr, alpha: str, rotor: str):
        size = len(ALPHA)
        offset = ALPHA.index(position)

        pos = ALPHA.index(letter)
        let = rotor[(pos + offset) % len(ALPHA)]
        pos = alpha.index(let)

        return ALPHA[(pos-offset+size) % size]
