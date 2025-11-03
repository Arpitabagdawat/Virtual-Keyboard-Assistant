import cv2
import time
import cvzone
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key
import os
from gtts import gTTS
from playsound import playsound
import threading

# ---------------- SETUP ----------------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8)
keyboard = Controller()

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", "Backspace"]]

finalText = ""
pressedKeys = {}
keyCooldown = {}

# ---------------- PRELOAD VOICE FILES ----------------
if not os.path.exists("voices"):
    os.mkdir("voices")

for row in keys:
    for key in row:
        file_path = f"voices/{key}.mp3"
        if not os.path.exists(file_path):
            tts = gTTS(text=key, lang='en')
            tts.save(file_path)

def play_sound(key):
    threading.Thread(target=lambda: playsound(f"voices/{key}.mp3"), daemon=True).start()

# ---------------- BUTTON CLASS ----------------
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.text = text
        self.size = size

def drawALL(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

# ---------------- CREATE BUTTONS ----------------
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == 'Backspace':
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key, size=[370, 90]))
        else:
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
        pressedKeys[key] = False
        keyCooldown[key] = 0

# ---------------- MAIN LOOP ----------------
while True:
    success, img = cap.read()
    if not success:
        break

    hands, img = detector.findHands(img)
    img = drawALL(img, buttonList)
    currentTime = time.time()

    if hands:
        lmList = hands[0]["lmList"]

        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            key = button.text

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x, y), (x + w, y + h), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, key, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

                if l < 35:
                    if not pressedKeys[key] and currentTime > keyCooldown[key]:
                        if key == 'Backspace':
                            keyboard.press(Key.backspace)
                            finalText = finalText[:-1]
                        else:
                            keyboard.press(key)
                            finalText += key
                            play_sound(key)  # ✅ Fast voice feedback

                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, key, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        pressedKeys[key] = True
                        keyCooldown[key] = currentTime + 0.25
                else:
                    pressedKeys[key] = False

    cv2.rectangle(img, (50, 350), (1200, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
 #  half keyboad + voice