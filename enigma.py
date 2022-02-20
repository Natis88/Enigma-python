from datetime import date
import time
from Reader import *
from Rotor import *


class Enigma:
    I: Rotor
    II: Rotor
    III: Rotor
    IV: Rotor
    plugboardDict = {}
    reflector = reader.read_json("reflector.json")
    code_book = reader.read_json("code-book.json")
    day = str(date.weekday(date.today()))

    # Fully parametrize constructor by OS date
    def __init__(self, code_book: dict,wheels:int):


        self.I = Rotor(code_book[self.day]["rotors"][0], code_book[self.day]
                       ["positions"][0], code_book[self.day]["settings"][0])
        self.II = Rotor(code_book[self.day]["rotors"][1], code_book[self.day]
                        ["positions"][1], code_book[self.day]["settings"][1])
        self.III = Rotor(code_book[self.day]["rotors"][2], code_book[self.day]
                         ["positions"][2], code_book[self.day]["settings"][2])
        if wheels==4:
            self.IV = Rotor(code_book[self.day]["rotors"][3], code_book[self.day]
                        ["positions"][3], code_book[self.day]["settings"][3])
        self.make_plugBoard()

    def _reflector(self, to_ref: str):
        return self.reflector[self.day][to_ref]
    # Fully character encrypt

    def encrypt(self, char: str) -> str():

        rotor_trigger = False

        if self.III.at_notch():
            rotor_trigger = True
        self.III.turn()

        if rotor_trigger:
            rotor_trigger = False
            if self.II.at_notch():
                rotor_trigger = True
            self.II.turn

        if rotor_trigger:
            rotor_trigger = False
            self.I.turn()
        else:
            if self.II.at_notch():
                self.II.turn()
                self.I.turn()
        letter = self.plugBoard_encrypt(char)
        letter = self.III.forward_encode(letter)
        letter = self.II.forward_encode(letter)
        letter = self.I.forward_encode(letter)

        letter = self._reflector(letter)

        letter = self.I.backward_encode(letter)
        letter = self.II.backward_encode(letter)
        letter = self.III.backward_encode(letter)
        letter = self.plugBoard_encrypt(letter)
        return letter

    def encrypt_M4(self, char: str) -> str():

        rotor_trigger = False

        if self.IV.at_notch():
            rotor_trigger = True
        self.IV.turn()

        if rotor_trigger:
            rotor_trigger = False
            if self.III.at_notch():
                rotor_trigger = True
            self.III.turn
        if rotor_trigger:
            rotor_trigger = False
            if self.II.at_notch():
                rotor_trigger = True
            self.II.turn

        if rotor_trigger:
            rotor_trigger = False
            self.I.turn()
        else:
            if self.II.at_notch():
                self.II.turn()
                self.I.turn()

        letter = self.plugBoard_encrypt(char)
        letter = self.IV.forward_encode(letter)
        letter = self.III.forward_encode(letter)
        letter = self.II.forward_encode(letter)
        letter = self.I.forward_encode(letter)

        letter = self._reflector(letter)

        letter = self.I.backward_encode(letter)
        letter = self.II.backward_encode(letter)
        letter = self.III.backward_encode(letter)
        letter = self.IV.backward_encode(letter)
        letter = self.plugBoard_encrypt(letter)
        return letter

    def make_plugBoard(self):
        plugboard = "AT BS DE FM IR KN LZ OW PV XY"
        plugboardConnections = plugboard.upper().split(" ")
        for pair in plugboardConnections:
            if len(pair) == 2:
                self.plugboardDict[pair[0]] = pair[1]
                self.plugboardDict[pair[1]] = pair[0]

    def plugBoard_encrypt(self, eLetter: chr):

        if eLetter in self.plugboardDict.keys():
            if self.plugboardDict[eLetter] != "":
                eLetter = self.plugboardDict[eLetter]
        return eLetter
    # Initialize enigma object

    def reset(self,mode):
        return self.__init__(code_book=self.code_book,wheels=mode)

    def run_enigma(self, text: str, mode: int):
        a_list = []
        cnt = 0
        for c in text:
            let = c
            if not let.isalnum():
                continue
            if let.isdigit():
                cnt += 1
                a_list.append(let)
            else:
                if mode == 4:
                    let = self.encrypt_M4(let.upper())
                else:
                    let = self.encrypt(let.upper())
                a_list.append(let)
                cnt += 1

            if cnt == 5:
                cnt = 0
                a_list.append(" ")

        return ''.join(a_list)

    def run_enigma_original_spaces(self, text: str, mode: int):
        a_list = []
        for c in text:
            let = c
            if let == " ":
                a_list.append(" ")
            if not let.isalnum():
                continue
            if let.isdigit():
                a_list.append(let)
            else:
                if mode == 4:
                    let = self.encrypt_M4(let.upper())
                else:
                    let = self.encrypt(let.upper())
                a_list.append(let)

        return ''.join(a_list)


if __name__ == '__main__':
    # Validate user input
    def validate(min, max):
        while True:
            try:
                num = int(input(f"Enter an integer {min} - {max}: "))
                while num > max or num < min:
                    num = int(input(f"Enter an integer {min} - {max}: "))
                break
            except ValueError:
                print("Please input integer only...")
                continue
        return num
    # Print transmission to console originally

    def print_and_encrypt_with_spaces(text, file_name: str, action: str, mode):
        print("\nOriginal Spaces")
        l = []
        for line in text:
            a = enigma.run_enigma_original_spaces(line, mode)
            l.append(a)
            reader.write_to_file(a, file_name)
        print(f"\n>>>{action}<<< ", *l, sep="\n")
        enigma.reset()
        return l
      # Print transmission to console without spaces

    def print_and_encrypt(text, file_name: str, action: str, mode):
        print("\nAlex Spaces")
        l = []
        for line in text:

            a = enigma.run_enigma(line, mode)
            l.append(a)
            reader.write_to_file(a, file_name)
        print(f"\n>>>{action}<<<", *l, sep="\n")
        enigma.reset()
        return l

    # Handle write to file function
    def handle_toFileEncryption(file_name: str, fromFile: str, mode):
        text = reader.read_text(fromFile)
        print("\nOriginal\n", *text, sep="\n")
        a = print_and_encrypt(text, file_name+"-encoded", "Encoded", mode)
        reader.write_to_file(
            "\nAlex Spaces\n***********************\nOriginal Spaces", file_name+"-encoded")
        print_and_encrypt(a, file_name + "-decoded", "Decoded", mode)
        reader.write_to_file(
            "\nAlex Spaces\n***********************\nOriginal Spaces", file_name+"-decoded")
        b = print_and_encrypt_with_spaces(
            text, file_name+"-encoded", "Encoded", mode)
        print_and_encrypt_with_spaces(
            b, file_name + "-decoded", "Decoded", mode)
        print(f"\nFile {file_name}-encoded created successfully ")
        print(f"\nFile {file_name}-decoded created successfully ")

    # Main function of enigma for handling user requests

    def work(choice, mode):
        print(f"Machine M{mode}")
        match choice:

            case 1:
                enigma.reset(mode)
                text = input("Enter text to encrypt: ")
                print("Encode")
                encrypted = enigma.run_enigma(text, mode)
                print("Alex =", encrypted)
                enigma.reset(mode)
                encrypted1 = enigma.run_enigma_original_spaces(text, mode)
                print("Original =", encrypted1)
                print("Decode")
                enigma.reset(mode)
                print("Alex =", enigma.run_enigma(encrypted, mode))
                enigma.reset(mode)
                print("Original =", enigma.run_enigma_original_spaces(
                    encrypted1, mode))
                show_Menu()
                work(validate(1, 3), mode)
            case 2:
                print(f"Machine M{mode}")
                enigma.reset(mode)
                print("\nChoose file to encrypt: ")
                print(
                    "1.transmissions1.txt\n2.transmissions2.txt \n3.transmissions3.txt")
                y = validate(1, 3)
                file_name = input("Enter the new file name to encrypt text:")
                print(
                    f"the machine will now create two files:\nfile name = {file_name} + encoded / decoded")
                match y:
                    case 1:
                        handle_toFileEncryption(
                            file_name, "transmissions/transmissions1.txt", mode)
                        show_Menu()
                        work(validate(1, 3), mode)
                    case 2:
                        handle_toFileEncryption(
                            file_name, "transmissions/transmissions2.txt", mode)
                        show_Menu()
                        work(validate(1, 3), mode)
                    case 3:
                        handle_toFileEncryption(
                            file_name, "transmissions/transmissions3.txt", mode)
                        show_Menu()
                        work(validate(1, 3), mode)
            case 3:
                exit()

    def starter():
        print("Welcome To Berlin The Year is 1939 ")
        time.sleep(2)
        print("Your Mission Is : \nTo Check if The Enigma Machine Is Working Well")
        time.sleep(2)
        print("Good Luck!!")
        time.sleep(2)
        print("The machine is automatically set by date ")
        print(f"The day in the week is: {enigma.day} ")
        print("Let's Start\n")
        time.sleep(2)

    def show_Menu():
        print("-------Menu------")
        print("1.Plain text to encrypt")
        print("2.Load file from directory")
        print("3.Exit")

    def choose_machine():
        print(("to check the Enigma M3 enter 3\nfor the Enigma M4 enter 4"))
        mode = validate(3, 4)
        return mode

cb = reader.read_json("code-book.json")
enigma = Enigma(cb,3)
starter()
mode = choose_machine()
show_Menu()
work(validate(1, 3), mode)
