import curses
import random
import time
import threading
# Yazma hızı ölçer yapıyorum
global total
total = 1


def clean_text(text):
    clean_list=[".", ",", "?", "\n", ":", "'", "...", "!..."] # Çıkartılması gereken işaretleri çıkartıyorum
    for i in clean_list:
        text = text.replace(i, "").lower()
    return text



def make_list():
    with open("text.txt", "r", encoding="utf-8") as f:  # Metin belgesinden texti çekip gerekli işlemleri uyguluyorum
        text = f.read()
    text = clean_text(text)
    x = ""
    words = []
    for i in text:
        if i == " ":
            words.append(x)  # Bir listeye alıyorum kelimeleri
            x = ""
        else:
            x += i
    return words

words = []
words.append(make_list())  # Fonksiyonu işliyorum


def give_text(words):
    correct_text = ""
    for i in range(1,15):
        z = random.randint(1, 150)
        correct_text += words[0][z]+" "
    return correct_text


def start_text(stdscr):
    stdscr.clear()
    x = -1
    try:
        while True:
            x += 1
            stdscr.addstr(0, x, "#")
    except:
        pass
    stdscr.addstr("Geçmek için bir tuşa basınız...")
    stdscr.getch()

def last_text(stdscr):
    stdscr.clear()
    stdscr.addstr(f"Tebrikler... WPM:{WPM}")
    stdscr.getch()

def user_text_process(stdscr, user_text):
    key = stdscr.getkey()

    if key in ("KEY_BACKSPACE", '\b', "\x7f","'"):  # ı yı ayarla
        if len(user_text) > 0:
            user_text.pop()
    elif key == 'KEY_LHELP':
        user_text.append("Ş")
    elif key == 'KEY_BTAB':
        user_text.append("ş")
    elif key == 'KEY_F(22)':
        user_text.append("Ğ")
    elif key == 'KEY_F(23)':
        user_text.append("ğ")
    elif key == 'KEY_F(40)':
        user_text.append("İ")
    elif key == 'KEY_F(41)':
        user_text.append("ı")
    elif key == '\n':
        pass
    elif len(key) == 1:
        user_text.append(key)


def print_process(stdscr, correct_text, user_text):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    T_COLOR = curses.color_pair(1)
    F_COLOR = curses.color_pair(2)
    stdscr.addstr(0,0,correct_text)
    global total
    t, f, total= 1, 0, 0
    for row_user,char_user in enumerate(user_text):
        for row_correct,char_correct in enumerate(correct_text):
            if row_user == row_correct:
                if f==0:
                    total += t
                    total -= f
                t, f = 0, 0
                if char_user == char_correct:
                    color = T_COLOR
                    stdscr.addstr(0, row_user, char_user, color)
                    t += 1
                else:
                    color = F_COLOR
                    stdscr.addstr(0, row_correct, char_correct, color)
                    f += 1


def time_text(stdscr, start_time):
    while True:

        time_elapsed = int(max(time.time() - start_time, 1))
        global WPM
        WPM = int((total/time_elapsed)*60/5)
        stdscr.addstr(1, 0, f"Zaman:{str(time_elapsed)}")
        stdscr.addstr(2, 0, f"wpm:{str(WPM)}")
        stdscr.refresh()


def wpm(stdscr):
    correct_text = give_text(words)
    user_text = []
    start_time = time.time()
    t1 = threading.Thread(target=time_text, args=(stdscr,start_time,))
    t1.start()
    while True:
        stdscr.clear()
        print_process(stdscr,correct_text,user_text)
        user_text_process(stdscr, user_text)
        stdscr.refresh()


def main(stdscr):
    start_text(stdscr)
    wpm(stdscr)



curses.wrapper(main)
