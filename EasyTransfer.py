import win32clipboard as wc
import msvcrt
import time
import os
import sys

# --- Try to enable ANSI colors on Windows consoles ---
def _enable_windows_ansi_colors() -> bool:
    if os.name != "nt":
        return True
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        for handle_id in (-11, -12):  # STD_OUTPUT_HANDLE, STD_ERROR_HANDLE
            h = kernel32.GetStdHandle(handle_id)
            if h == 0 or h == -1:
                continue
            mode = ctypes.c_uint()
            if not kernel32.GetConsoleMode(h, ctypes.byref(mode)):
                continue
            if not kernel32.SetConsoleMode(h, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING):
                continue
        return True
    except Exception:
        return False

_USE_COLOR = _enable_windows_ansi_colors()

# ANSI color codes (fallback to empty strings if unsupported)
RED = "\033[91m" if _USE_COLOR else ""
GREEN = "\033[92m" if _USE_COLOR else ""
BOLD_GREEN = "\033[1;92m" if _USE_COLOR else ""
YELLOW = "\033[93m" if _USE_COLOR else ""
BOLD_YELLOW = "\033[1;93m" if _USE_COLOR else ""
CYAN = "\033[96m" if _USE_COLOR else ""
BOLD_CYAN = "\033[1;96m" if _USE_COLOR else ""
RESET = "\033[0m" if _USE_COLOR else ""

last_map_id = None  # remembers the last entered Map ID

def extract_event_coords():
    wc.OpenClipboard()
    try:
        data = wc.GetClipboardData(563)  # RPG Maker event data
        if not isinstance(data, bytes):
            return None, None
        for i in range(len(data) - 5):
            if data[i] == 0x02 and data[i+1] == 0x01 and data[i+3] == 0x03 and data[i+4] == 0x01:
                return data[i+2], data[i+5]
        return None, None
    except Exception:
        return None, None
    finally:
        wc.CloseClipboard()

def copy_to_clipboard(text: str):
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardText(text)  # CF_UNICODETEXT
    wc.CloseClipboard()

def main():
    global last_map_id

    # Banner
    print(f"{BOLD_YELLOW}★━━━━━━━━━━━━━━━━━━━━━━━━━━━━★{RESET}")
    print(f"{YELLOW}        Easy Transfer{RESET}")
    print(f"{BOLD_YELLOW}★━━━━━━━━━━━━━━━━━━━━━━━━━━━━★{RESET}\n")

    print(f"{CYAN}Copy an event (Ctrl+C), then press SHIFT+C to grab X/Y coords.{RESET}")
    print(f"{CYAN}Enter Map ID manually (last one remembered).{RESET}")
    print(f"{CYAN}Press Ctrl+Q to quit.{RESET}")
    print(f"{BOLD_CYAN}Current Map ID: {last_map_id if last_map_id else 'None'}{RESET}")

    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getch()

            if ch in (b'\x11',):  # Ctrl+Q
                print(f"{RED}Exiting...{RESET}")
                break

            if ch == b'C':  # Shift+C
                x, y = extract_event_coords()
                if x is None or y is None:
                    print(f"{RED}❌ Could not find X/Y in clipboard (copy an event first).{RESET}")
                else:
                    if last_map_id:
                        user_input = input(f"{CYAN}Enter Map ID [{last_map_id}]: {RESET}").strip()
                        if user_input:
                            last_map_id = user_input
                    else:
                        last_map_id = input(f"{CYAN}Enter Map ID: {RESET}").strip()

                    code_line = f"    MovePlace({last_map_id}, {x}, {y})"
                    print(f"{BOLD_GREEN}{code_line}{RESET}")
                    copy_to_clipboard(code_line)
                    print(f"{GREEN}✔ Event code copied to clipboard!{RESET}")
                    time.sleep(1)
                    print(f"{BOLD_YELLOW}Now copy and paste it into TkoolBridge and Click Generate Event Code(X)!{RESET}")

if __name__ == "__main__":
    main()
