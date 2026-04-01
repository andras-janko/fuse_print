import sys
import datetime
import re

# ANSI színkódok a terminálhoz
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'

def get_mcu_configs():
    return {
        "atmega4809": [
            {"name": "WDTCFG", "bits": {
                "PERIOD": (0x0F, 0, {0: "OFF", 1: "8ms", 2: "16ms", 3: "31ms", 4: "63ms", 5: "125ms", 6: "250ms", 7: "500ms", 8: "1s", 9: "2s", 10: "4s", 11: "8s"}, "Watchdog Timeout Period"),
                "WINDOW": (0xF0, 4, {0: "OFF", 1: "8ms", 2: "16ms", 3: "31ms", 4: "63ms", 5: "125ms", 6: "250ms", 7: "500ms", 8: "1s", 9: "2s", 10: "4s", 11: "8s"}, "Watchdog Window Period")
            }},
            {"name": "BODCFG", "bits": {
                "SLEEP": (0x03, 0, {0: "DIS", 1: "SAMP", 2: "CONT"}, "BOD Operation Mode in Sleep"),
                "ACTIVE": (0x0C, 2, {0: "DIS", 1: "SAMP", 2: "CONT"}, "BOD Operation Mode in Active"),
                "SAMPFREQ": (0x10, 4, {0: "1 kHz", 1: "125 Hz"}, "BOD Sample Frequency"),
                "LVL": (0xE0, 5, {0: "1.8V", 1: "2.1V", 2: "2.4V", 3: "2.7V", 4: "3.3V", 5: "3.7V", 6: "4.1V", 7: "4.3V"}, "BOD Threshold Level")
            }},
            {"name": "OSCCFG", "bits": {
                "FREQSEL": (0x03, 0, {1: "16MHz", 2: "20MHz"}, "Internal Oscillator Frequency"),
                "OSC_RES_2_6": (0x7C, 2, "RES", "Reserved bits"),
                "OSCLOCK": (0x80, 7, {0: "False", 1: "True"}, "Oscillator Frequency Lock")
            }},
            {"name": "SYSCFG0", "bits": {
                "EESAVE": (0x01, 0, {0: "Erased", 1: "Retained"}, "EEPROM Save during Chip Erase"),
                "SYS0_RES_1_2": (0x06, 1, "RES", "Reserved bits"),
                "RSTPINCFG": (0x08, 3, {0: "GPIO", 1: "RESET/UPDI"}, "Reset Pin Configuration"),
                "SYS0_RES_4_5": (0x30, 4, "RES", "Reserved bits"),
                "CRCSRC": (0xC0, 6, {0: "None", 1: "CRC Boot", 2: "CRC Boot+App", 3: "CRC Entire Flash"}, "CRC Source Selection")
            }},
            {"name": "SYSCFG1", "bits": {
                "SUT": (0x07, 0, {0: "0ms", 1: "1ms", 2: "2ms", 4: "8ms", 7: "64ms"}, "System Startup Time"),
                "SYS1_RES_3_7": (0xF8, 3, "RES", "Reserved bits")
            }},
            {"name": "APPEND", "bits": {"APPEND": (0xFF, 0, "RAW", "Application Data Section End")}},
            {"name": "BOOTEND", "bits": {"BOOTEND": (0xFF, 0, "RAW", "Boot Section End")}}
        ],
        "atmega2560": [
            {"name": "LOW", "bits": {
                "CKSEL": (0x0F, 0, {0: "Ext Clk", 1: "Int RC", 15: "Ext Crystal"}, "Clock Source Selection"),
                "SUT": (0x30, 4, {2: "64ms"}, "Select Start-up Time"),
                "CKOUT": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "Clock Output on PORTE7"),
                "CKDIV8": (0x80, 7, {0: "Enabled", 1: "Disabled"}, "Divide Clock by 8")
            }},
            {"name": "HIGH", "bits": {
                "BOOTRST": (0x01, 0, {0: "Enabled", 1: "Disabled"}, "Select Reset Vector"),
                "BOOTSZ": (0x06, 1, {0: "4096w", 1: "2048w", 2: "1024w", 3: "512w"}, "Select Boot Size"),
                "EESAVE": (0x08, 3, {0: "Preserved", 1: "Not Preserved"}, "EEPROM Preserve during Chip Erase"),
                "WDTON": (0x10, 4, {0: "Always On", 1: "Software Ctrl"}, "Watchdog Timer Always On"),
                "SPIEN": (0x20, 5, {0: "Enabled", 1: "Disabled"}, "Enable Serial Download"),
                "JTAGEN": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "Enable JTAG Interface"),
                "OCDEN": (0x80, 7, {0: "Enabled", 1: "Disabled"}, "Enable On-chip Debug")
            }},
            {"name": "EXTENDED", "bits": {
                "BODLEVEL": (0x07, 0, {7: "Disabled", 6: "1.8V", 5: "2.7V", 4: "4.3V"}, "Brown-out Detector Level"),
                "EXT_RES_3_7": (0xF8, 3, "RES", "Reserved bits")
            }}
        ],
        "atmega328p": [
            {"name": "LOW", "bits": {
                "CKSEL": (0x0F, 0, {2: "Int RC 8MHz", 15: "Ext Crystal"}, "Clock Source Selection"),
                "SUT": (0x30, 4, {2: "64ms"}, "Select Start-up Time"),
                "CKOUT": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "Clock Output"),
                "CKDIV8": (0x80, 7, {0: "Enabled", 1: "Disabled"}, "Divide Clock by 8")
            }},
            {"name": "HIGH", "bits": {
                "BOOTRST": (0x01, 0, {0: "Enabled", 1: "Disabled"}, "Select Reset Vector"),
                "BOOTSZ": (0x06, 1, {0: "2048w", 3: "256w"}, "Select Boot Size"),
                "EESAVE": (0x08, 3, {0: "Preserved", 1: "Not Preserved"}, "EEPROM Preserve during Chip Erase"),
                "WDTON": (0x10, 4, {0: "Always On", 1: "Software Ctrl"}, "Watchdog Timer Always On"),
                "SPIEN": (0x20, 5, {0: "Enabled", 1: "Disabled"}, "Enable Serial Download"),
                "DWEN": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "Enable debugWIRE"),
                "RSTDISBL": (0x80, 7, {0: "Reset Disabled", 1: "Reset Enabled"}, "External Reset Disable")
            }},
            {"name": "EXTENDED", "bits": {
                "BODLEVEL": (0x07, 0, {7: "Disabled", 6: "1.8V", 5: "2.7V", 4: "4.3V"}, "Brown-out Detector Level"),
                "EXT_RES_3_7": (0xF8, 3, "RES", "Reserved bits")
            }}
        ],
        "attiny44": [
            {"name": "LOW", "bits": {
                "CKSEL": (0x0F, 0, {2: "Int RC 8MHz", 3: "Int RC 128kHz"}, "Clock Source Selection"),
                "SUT": (0x30, 4, {3: "64ms"}, "Select Start-up Time"),
                "CKOUT": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "Clock Output"),
                "CKDIV8": (0x80, 7, {0: "Enabled", 1: "Disabled"}, "Divide Clock by 8")
            }},
            {"name": "HIGH", "bits": {
                "BODLEVEL": (0x07, 0, {7: "Disabled", 4: "4.3V"}, "Brown-out Detector Level"),
                "EESAVE": (0x08, 3, {0: "Preserved", 1: "Not Preserved"}, "EEPROM Save"),
                "WDTON": (0x10, 4, {0: "Always On", 1: "SW Ctrl"}, "Watchdog Timer"),
                "SPIEN": (0x20, 5, {0: "Enabled", 1: "Disabled"}, "SPI Enable"),
                "DWEN": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "debugWIRE Enable"),
                "RSTDISBL": (0x80, 7, {0: "GPIO", 1: "Reset Pin"}, "Reset Disable")
            }},
            {"name": "EXTENDED", "bits": {
                "SELFPRGEN": (0x01, 0, {0: "Enabled", 1: "Disabled"}, "Self-Programming Enable"),
                "EXT_RES_1_7": (0xFE, 1, "RES", "Reserved bits")
            }}
        ],
        "attiny45": [
            {"name": "LOW", "bits": {
                "CKSEL": (0x0F, 0, {1: "PLL 16MHz", 2: "Int RC 8MHz"}, "Clock Source Selection"),
                "SUT": (0x30, 4, {3: "64ms"}, "Select Start-up Time"),
                "CKOUT": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "Clock Output"),
                "CKDIV8": (0x80, 7, {0: "Enabled", 1: "Disabled"}, "Divide Clock by 8")
            }},
            {"name": "HIGH", "bits": {
                "BODLEVEL": (0x07, 0, {7: "Disabled", 4: "4.3V"}, "Brown-out Detector Level"),
                "EESAVE": (0x08, 3, {0: "Preserved", 1: "Not Preserved"}, "EEPROM Preserve"),
                "WDTON": (0x10, 4, {0: "Always On", 1: "SW Ctrl"}, "Watchdog Timer"),
                "SPIEN": (0x20, 5, {0: "Enabled", 1: "Disabled"}, "SPI Enable"),
                "DWEN": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "debugWIRE Enable"),
                "RSTDISBL": (0x80, 7, {0: "GPIO", 1: "Reset Pin"}, "Reset Disable")
            }},
            {"name": "EXTENDED", "bits": {
                "SELFPRGEN": (0x01, 0, {0: "Enabled", 1: "Disabled"}, "Self-Programming Enable"),
                "EXT_RES_1_7": (0xFE, 1, "RES", "Reserved bits")
            }}
        ],
        "attiny2313": [
            {"name": "LOW", "bits": {
                "CKSEL": (0x0F, 0, {4: "Int RC 8MHz"}, "Clock Source Selection"),
                "SUT": (0x30, 4, {3: "64ms"}, "Select Start-up Time"),
                "CKOUT": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "Clock Output"),
                "CKDIV8": (0x80, 7, {0: "Enabled", 1: "Disabled"}, "Divide Clock by 8")
            }},
            {"name": "HIGH", "bits": {
                "BODLEVEL": (0x07, 0, {7: "Disabled", 6: "1.8V", 4: "4.3V"}, "Brown-out Detector Level"),
                "EESAVE": (0x08, 3, {0: "Preserved", 1: "Not Preserved"}, "EEPROM Preserve"),
                "WDTON": (0x10, 4, {0: "Always On", 1: "SW Ctrl"}, "Watchdog Timer"),
                "SPIEN": (0x20, 5, {0: "Enabled", 1: "Disabled"}, "SPI Enable"),
                "DWEN": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "debugWIRE Enable"),
                "RSTDISBL": (0x80, 7, {0: "GPIO", 1: "Reset Pin"}, "Reset Disable")
            }},
            {"name": "EXTENDED", "bits": {
                "SELFPRGEN": (0x01, 0, {0: "Enabled", 1: "Disabled"}, "Self-Programming Enable"),
                "EXT_RES_1_7": (0xFE, 1, "RES", "Reserved bits")
            }}
        ],
        "atmega8": [
            {"name": "LOW", "bits": {
                "CKSEL": (0x0F, 0, {1: "1MHz RC", 4: "8MHz RC"}, "Clock Source Selection"),
                "SUT": (0x30, 4, {3: "Standard"}, "Select Start-up Time"),
                "BODEN": (0x40, 6, {0: "Enabled", 1: "Disabled"}, "BOD Enable"),
                "BODLEVEL": (0x80, 7, {0: "4.0V", 1: "2.7V"}, "BOD Level")
            }},
            {"name": "HIGH", "bits": {
                "BOOTRST": (0x01, 0, {0: "Enabled", 1: "Disabled"}, "Select Reset Vector"),
                "BOOTSZ": (0x06, 1, {0: "1024w", 3: "128w"}, "Select Boot Size"),
                "EESAVE": (0x08, 3, {0: "Preserved", 1: "Not Preserved"}, "EEPROM Preserve"),
                "CKOPT": (0x10, 4, {0: "Enabled", 1: "Disabled"}, "Oscillator Options"),
                "SPIEN": (0x20, 5, {0: "Enabled", 1: "Disabled"}, "SPI Enable"),
                "WDTON": (0x40, 6, {0: "Always On", 1: "SW Ctrl"}, "Watchdog Timer"),
                "RSTDISBL": (0x80, 7, {0: "GPIO", 1: "Reset Pin"}, "Reset Disable")
            }}
        ]
    }

def decode_fuses(mcu_name, file_path):
    configs = get_mcu_configs()
    mcu = mcu_name.lower()

    if mcu in configs: mcu_map = configs[mcu]
    else:
        print(f"{RED}Error: '{mcu}' not supported.{ENDC}"); return

    try:
        with open(file_path, 'rb') as f: data = list(f.read())
    except Exception as e:
        print(f"{RED}Error reading file: {e}{ENDC}"); return

    mcu_map = configs[mcu]
    output_lines = []

    def log(text, only_file=False):
        if not only_file:
            print(text)
        clean_text = re.sub(r'\033\[[0-9;]*m', '', text)
        output_lines.append(clean_text)

    def color_aware_ljust(text, width):
        clean = re.sub(r'\033\[[0-9;]*m', '', text)
        return text + " " * (width - len(clean))

    log(f"\n{BOLD}{CYAN}AVR FUSE DECODER - {mcu.upper()}{ENDC}")
    log("=" * 135)
    header = f"{BOLD}{'SHORT NAME':<15} | {'BITS':<8} | {'RAW BIN':<12} | {'SETTING':<25} | {'LONG DESCRIPTION'}{ENDC}"
    log(header)
    log("-" * 135)

    for i, val in enumerate(data):
        if i >= len(mcu_map): break
        f_def = mcu_map[i]
        log(f"\n{YELLOW}>>> {f_def['name']} BYTE (Hex: 0x{val:02X}, Bin: 0b{val:08b}){ENDC}")

        for short_name, (mask, shift, meanings, long_desc) in f_def['bits'].items():
            raw_val = (val & mask) >> shift
            bits_idx = sorted([b for b in range(8) if (mask & (1 << b))])
            bit_range = f"{min(bits_idx)}:{max(bits_idx)}" if len(bits_idx) > 1 else f"{bits_idx}"
            bit_width = len(bits_idx)
            bin_display = f"0b{raw_val:0{bit_width}b}"

            other_opts = []
            warning = ""
            if meanings == "RES":
                expected = (1 << bit_width) - 1
                if raw_val != expected:
                    res_text = f"{RED}INVALID (0){ENDC}"
                    warning = f" {RED}<- [WARNING: Should be 1]{ENDC}"
                else: res_text = f"{GREEN}OK (1){ENDC}"
                other_opts_str = "None (Fixed bit)"
            elif meanings == "bytes":
                res_text = f"{raw_val * 256} bytes"
                other_opts_str = "Any value * 256 bytes"
            elif isinstance(meanings, dict):
                res_text = meanings.get(raw_val, f"0x{raw_val:X}")
                for k, v in meanings.items():
                    if k != raw_val:
                        other_opts.append(f"{k}:{v}")
                other_opts_str = ", ".join(other_opts)
            else:
                res_text = str(raw_val)
                other_opts_str = "N/A"

            s_name = f"{short_name:<15}"
            b_range = f"{bit_range:<8}"
            b_disp = f"{bin_display:<12}"
            setting_col = color_aware_ljust(res_text, 25)

            log(f"{s_name} | {b_range} | {b_disp} | {setting_col} | {long_desc}{warning}")
            log(f"{' ': <15} | {' ': <8} | {' ': <12} | {' ': <25} | OTHER OPTIONS: {other_opts_str}", only_file=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{mcu}_{timestamp}.txt"
    try:
        with open(log_filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_lines))
        print(f"\n{GREEN}Report saved to: {log_filename} (Includes all Other Options){ENDC}")
    except Exception as e:
        print(f"{RED}Could not save report: {e}{ENDC}")

if __name__ == "__main__":
    configs = get_mcu_configs()
    if len(sys.argv) < 3:
        print(f"\n{BOLD}{YELLOW}=== AVR BINARY FUSE DECODER UTILITY ==={ENDC}")
        print(f"{BOLD}Usage:{ENDC} python {sys.argv[0]} {CYAN}<mcu_type> <file.bin>{ENDC}")
        print("-" * 75)
        print(f"{BOLD}Supported MCU types and required binary fuse sequence:{ENDC}")

        print(f"  {CYAN}atmega4809{ENDC}:")
        print("    1:WDTCFG, 2:BODCFG, 3:OSCCFG, 4:SYSCFG0, 5:SYSCFG1, 6:APPEND, 7:BOOTEND")

        print(f"  {CYAN}atmega2560 / atmega328p{ENDC}:")
        print("    1:LOW byte, 2:HIGH byte, 3:EXTENDED byte")

        print(f"  {CYAN}attiny44 / attiny45 / attiny2313{ENDC}:")
        print("    1:LOW byte, 2:HIGH byte, 3:EXTENDED byte")

        print(f"  {CYAN}atmega8{ENDC}:")
        print("    1:LOW byte, 2:HIGH byte")

        print("-" * 75)
        print(f"{BOLD}Note:{ENDC} Script saves detailed report with {CYAN}Other Options{ENDC} to file.")
        print(f"{BOLD}Note:{ENDC} The script validates {RED}Reserved bits{ENDC} (should be 1 per AVR standard).")
    else:
        decode_fuses(sys.argv[1], sys.argv[2])
