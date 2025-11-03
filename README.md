# Virtual-Keyboard-Assistant

# 🎹 Virtual AI Keyboard with Voice Feedback  

This project is an **AI-powered Virtual Keyboard** that allows users to type using **hand gestures** instead of a physical keyboard.  
Each key press is detected through a webcam using **Computer Vision**, and **voice feedback** is provided for every key pressed — making typing more interactive and accessible.  

---

## 🚀 Features  

- 🖐️ **Hand Gesture Control** – Detects finger movements using the camera (via MediaPipe HandTracking).  
- 🔤 **Full Virtual Keyboard** – Supports alphabets, numbers, space, backspace, and more.  
- 🔊 **Voice Feedback** – Each pressed key is announced using a built-in text-to-speech system.  
- ⚡ **Real-Time Processing** – Fast key detection with smooth on-screen visualization.  
- 💻 **No Physical Keyboard Needed** – Type in mid-air using just your hands!  

---

## 🧠 Technologies Used  

- **Python**  
- **OpenCV** – for camera and image processing  
- **cvzone** – for easy hand tracking  
- **MediaPipe** – for hand landmark detection  
- **pynput** – for virtual keyboard control  
- **gTTS (Google Text-to-Speech)** – for voice feedback  
- **playsound** – to play key sound instantly  

---

## ⚙️ How It Works  

1. The webcam detects your hand using **MediaPipe HandDetector**.  
2. When your **index finger** hovers over a key and **touches the middle finger**, that key is considered pressed.  
3. The pressed key appears on screen, and a **voice speaks that letter**.  
4. You can keep typing with gestures — just like on a real keyboard!  

---

## 📸 Output Preview  

🖼️ A virtual keyboard appears on the screen, showing your **face and hand** while typing.  
Each key you press will:  
- Change color  
- Display in the text area  
- Speak out loud  

---

## 🧩 Installation  

```bash
pip install opencv-python cvzone mediapipe pynput gTTS playsound
```

Then run the file:  

```bash
python virtual_keyboard.py
```

---

## 👩‍💻 Author  

**Arpita Bagdawat**  
🎓 B.Tech – Artificial Intelligence & Data Science  
🏫 Mahakal Institute of Technology, Ujjain  





