import cv2
import time
import cvzone
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
import os
from gtts import gTTS
from playsound import playsound
import threading
import nltk
from nltk.corpus import words


try:
    nltk.data.find("corpora/words")
except LookupError:
    nltk.download("words")

word_list = set(words.words())

# --- Prediction helper ---
def predict_next_words(current_text, top_n=3):
    if not current_text or current_text[-1] == " ":
        return []
    last_word = current_text.split()[-1].lower()
    preds = [w for w in word_list if w.startswith(last_word)][:top_n]
    return preds


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
keyboard = Controller()

layout = [
    [("`", "~"), ("1","!"), ("2","@"), ("3","#"), ("4","$"), ("5","%"), ("6","^"), ("7","&"), ("8","*"), ("9","("), ("0",")"), ("-","_"), ("=","+"), ("Backspace","Backspace")],
    [("Tab","Tab"), ("q","Q"), ("w","W"), ("e","E"), ("r","R"), ("t","T"), ("y","Y"), ("u","U"), ("i","I"), ("o","O"), ("p","P"), ("[","{"), ("]","}"), ("\\","|")],
    [("Caps","Caps"), ("a","A"), ("s","S"), ("d","D"), ("f","F"), ("g","G"), ("h","H"), ("j","J"), ("k","K"), ("l","L"), (";"," :"), ("'","\""), ("Enter","Enter")],
    [("Shift","Shift"), ("z","Z"), ("x","X"), ("c","C"), ("v","V"), ("b","B"), ("n","N"), ("m","M"), (",","<"), (".",">"), ("/","?"), ("Shift","Shift")],
    [("Space","Space")]
]

def label_to_speak(ch):
    names = {
        "`": "backtick", "~": "tilde", "-": "minus", "_": "underscore",
        "=":"equals", "+":"plus", "[":"left bracket", "{":"left brace",
        "]":"right bracket", "}":"right brace", "\\":"backslash", "|":"pipe",
        ";":"semicolon", ":":"colon", "'":"single quote", '"':"double quote",
        ",":"comma", "<":"less than", ".":"dot", ">":"greater than",
        "/":"slash", "?":"question mark", "1":"one","2":"two","3":"three","4":"four",
        "5":"five","6":"six","7":"seven","8":"eight","9":"nine","0":"zero",
        "!":"exclamation","@":"at","#":"hash","$":"dollar","%":"percent","^":"caret",
        "&":"ampersand","*":"asterisk","(":"left paren",")":"right paren"
    }
    return names.get(ch, ch)

if not os.path.exists("voices"):
    os.mkdir("voices")

def filename_for(ch):
    safe = ch.lower().replace(" ", "_").replace("/", "").replace("\\", "")
    return f"voices/{safe}.mp3"

def play_sound_for(ch):
    path = filename_for(ch)
    if not os.path.exists(path):
        try:
            tts = gTTS(text=label_to_speak(ch), lang='en')
            tts.save(path)
        except:
            pass
    threading.Thread(target=lambda: playsound(path), daemon=True).start()

class Button:
    def __init__(self, pos, text, size=(80,80)):
        self.pos = pos
        self.text = text
        self.size = size

def draw_button(img, btn, color=(255,0,255)):
    x,y = btn.pos
    w,h = btn.size
    cv2.rectangle(img, (x,y), (x+w,y+h), color, cv2.FILLED)
    cv2.putText(img, btn.text, (x+10, y+50), cv2.FONT_HERSHEY_PLAIN, 1.7, (255,255,255), 2)

buttonList = []
start_x, start_y = 40, 90
key_w, key_h, gap_x, gap_y = 80, 70, 10, 15

for r, row in enumerate(layout):
    x = start_x
    y = start_y + r * (key_h + gap_y)
    for normal, shifted in row:
        w = key_w
        if normal.lower() == "backspace": w = key_w * 2
        elif normal.lower() == "tab": w = int(key_w * 1.5)
        elif normal.lower() == "caps": w = int(key_w * 1.7)
        elif normal.lower() == "enter": w = int(key_w * 2)
        elif normal.lower() == "shift": w = int(key_w * 2.2)
        elif normal.lower() == "space":
            w = int(key_w * 7)
            x = start_x + 2*(key_w+gap_x)
        text = f"{normal} {shifted}" if normal != shifted else normal
        buttonList.append((Button((x,y), text, (w, key_h)), (normal, shifted)))
        x += w + gap_x

finalText = ""
shift_active, caps_active = False, False
prev_pinch_length = 100
last_press_time = 0
cooldown = 0.25 

prediction_boxes = []  

while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    for btn, _ in buttonList:
        draw_button(img, btn)

    if hands:
        lmList = hands[0]["lmList"]
        fx, fy = lmList[8][0], lmList[8][1]
        pinch_length, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

       
        for (x, y, w, h, word) in prediction_boxes:
            if x < fx < x+w and y < fy < y+h:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
                if pinch_length < 35:
                    last_word = finalText.split()[-1] if finalText.strip() else ""
                    if last_word:
                        finalText = finalText[:-(len(last_word))] + word + " "
                    else:
                        finalText += word + " "
                    play_sound_for(word)
                    time.sleep(0.2)

        for btn, pair in buttonList:
            normal, shifted = pair
            x, y = btn.pos
            w, h = btn.size
            if x < fx < x + w and y < fy < y + h:
                draw_button(img, btn, (175, 0, 175))
                current_time = time.time()
                if prev_pinch_length > 45 and pinch_length < 35 and (current_time - last_press_time) > cooldown:
                    key_lower = normal.lower()
                    if key_lower == "backspace":
                        finalText = finalText[:-1]; play_sound_for("backspace")
                    elif key_lower == "enter":
                        finalText += "\n"; play_sound_for("enter")
                    elif key_lower == "space":
                        finalText += " "; play_sound_for("space")
                    elif key_lower == "shift":
                        shift_active = True; play_sound_for("shift")
                    elif key_lower == "caps":
                        caps_active = not caps_active; play_sound_for("caps")
                    else:
                        output = shifted if (shift_active or (caps_active and normal.isalpha())) else normal
                        finalText += output
                        play_sound_for(output)
                        if shift_active: shift_active = False
                    last_press_time = current_time
                    draw_button(img, btn, (0,255,0))

        cv2.line(img, lmList[8][:2], lmList[12][:2], (0,255,0), 3)
        prev_pinch_length = pinch_length

 
    cv2.rectangle(img, (40, 560), (1240, 700), (175,0,175), cv2.FILLED)
    lines = finalText[-120:].split("\n")[-3:]
    for i, line in enumerate(lines):
        cv2.putText(img, line, (50, 600 + i*35), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)

   
    preds = predict_next_words(finalText)
    prediction_boxes = []
    if preds:
        x_start = 50
        y_start = 530
        box_w = 200
        box_h = 40
        for i, word in enumerate(preds):
            x = x_start + i*(box_w + 20)
            y = y_start
            cv2.rectangle(img, (x, y), (x+box_w, y+box_h), (50, 150, 255), cv2.FILLED)
            cv2.putText(img, word, (x+10, y+28), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)
            prediction_boxes.append((x, y, box_w, box_h, word))

    cv2.imshow("Virtual QWERTY Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
