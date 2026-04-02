fuse_decode.py
A command-line Python utility for decoding and analyzing AVR microcontroller fuse bits from binary files.

Overview
This script helps you interpret the binary fuse bytes used to configure various Atmel AVR microcontrollers (such as ATmega4809, ATmega2560, ATmega328p, ATtiny44, and others). It decodes raw binary fuse files, prints a colorized terminal table with human-readable meanings, and saves a detailed report (including alternative/multiple settings) to a file.

Features
Supports multiple AVR MCUs out of the box (ATmega, ATtiny families).
Prints each fuse byte and its decoded values (settings, bit meanings, reserved bits, warnings).
Validates reserved bits as per AVR standards.
Provides recommendations/warnings if any reserved bit is incorrectly set.
Saves a timestamped, plain-text report with all options and settings.
Colorized terminal output for easy reading.
Supported MCUs & Fuse Format
atmega4809: WDTCFG, BODCFG, OSCCFG, SYSCFG0, SYSCFG1, APPEND, BOOTEND (7 bytes)
atmega2560, atmega328p: LOW, HIGH, EXTENDED (3 bytes)
attiny44, attiny45, attiny2313: LOW, HIGH, EXTENDED (3 bytes)
atmega8: LOW, HIGH (2 bytes)
See in-script help for details (python fuse_decode.py without arguments).

Usage
Code
python fuse_decode.py <mcu_type> <file.bin>
<mcu_type>: Chip type (e.g., atmega328p, attiny45, etc.; see list above)
<file.bin>: Raw binary file containing the fuse bytes (in expected order per device)
Example:

Code
python fuse_decode.py atmega328p my_fuse_dump.bin
This will print a detailed, colorized fuse decode table and create a text log file containing the full breakdown.

Output Example
Terminal table showing short names, bit ranges, binary settings, decoded value, and a long description.
Warnings if reserved bits have unexpected values.
Other possible option values are listed in the output file for reference.
Additional Notes
Output report files are saved as <mcu>_<timestamp>.txt.
The script checks and warns if reserved bits aren’t set per Atmel recommendations.
The file and script are in UTF-8.
Requirements
Python 3.x
License
MIT License (or specify your actual license here).

Feel free to modify or expand based on your needs!
