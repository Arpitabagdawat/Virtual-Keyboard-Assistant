# 🎯 AI Virtual Keyboard using Hand Gestures

Welcome to my **AI Virtual Keyboard** project — an intelligent and interactive keyboard that works completely on **hand gestures** detected through your webcam. 🖐💻  
No physical typing needed — just your hands, camera, and a bit of AI magic! ✨  

---

## 🚀 Project Overview

This project uses **Computer Vision** and **Artificial Intelligence** to build a **gesture-controlled virtual keyboard** that recognizes your finger positions to simulate key presses.  
It’s designed to give a **realistic typing experience** and make typing more accessible, futuristic, and fun! 🤖

---

## 🧩 Features Implemented So Far

✅ **1. Voice Feedback (Text-to-Speech)**  
Every time you press a key, the system *speaks* the letter or key name aloud using `gTTS`.  
> Example: “You pressed A” 🔊  

✅ **2. Full QWERTY Keyboard Layout**  
Includes all standard keys — **A–Z, numbers, Shift, Caps, Space, Enter, and Backspace** for a realistic typing experience.  

✅ **3. Typing Area with Word Prediction**  
Displays a text box showing typed text with **real-time word prediction** using `nltk`.  
Predicted words appear below the typing area and can be selected by pinching your fingers together.  

✅ **4. Common Daily Words Prediction**  
The prediction system focuses on **frequently used conversational words** (like *okay, fine, thanks, serious, sure, amazing,* etc.) to make typing more natural and human-like.  

---

## 🧠 Technologies & Libraries Used

| Library | Purpose |
|----------|----------|
| `cv2 (OpenCV)` | Hand tracking, button drawing, video feed |
| `cvzone` | Simplified hand detection interface |
| `HandDetector` | Finger position detection |
| `nltk` | Word prediction logic |
| `gTTS` | Text-to-speech (voice feedback) |
| `playsound` | Audio playback |
| `threading` | Smooth non-blocking sound handling |
| `pynput` | Keyboard control (optional) |

---

## ⚙️ Installation & Setup

Clone the repository:
```bash
git clone https://github.com/<your-username>/AI-Virtual-Keyboard.git
cd AI-Virtual-Keyboard
```

Install the required dependencies:
```bash
pip install opencv-python cvzone nltk gTTS playsound pynput
```

Download the `nltk` word corpus (only once):
```python
import nltk
nltk.download('words')
```

Run the project:
```bash
python ai_virtual_keyboard.py
```

---

## 🧩 How It Works

1. The webcam captures real-time video feed.  
2. The `HandDetector` module tracks hand landmarks and finger positions.  
3. When the index and middle finger come close to a key region → it’s registered as a key press.  
4. Pressed key triggers:  
   - Text appears on screen  
   - Voice feedback plays (using gTTS)  
   - Word predictions update instantly below the text box.  

---

## 💡 Future Enhancements

🔹 Add support for **multiple languages**  
🔹 Include **emoji prediction**  
🔹 Save typed text as a `.txt` file  
🔹 Add **handwriting recognition mode**  

---

## 📸 Demo & Preview

🎥 *Demo video available on my LinkedIn profile:*  
👉 [www.linkedin.com/in/arpita-b-66a996292](https://www.linkedin.com/in/arpita-b-66a996292)

---

## 🧑‍💻 Author

**Arpita Bagdawat**  
🎓 B.Tech (AI & Data Science) | Mahakal Institute of Technology, Ujjain  
💼 Aspiring Data Scientist & AI Enthusiast  
🔗 [LinkedIn](https://www.linkedin.com/in/arpita-b-66a996292)

---

## 🌟 Show Your Support

If you like this project, don’t forget to ⭐ **star the repo** and share your feedback! 💬  
Let’s make AI-based interaction more creative and accessible. ✨
