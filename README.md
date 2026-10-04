# 🤟 Sign Language to Speech and Text Converter

## Gestura – Sign Language Interpreter

**Gestura** is a real-time sign language recognition application that uses a webcam to detect hand gestures and convert them into **text and speech**.

The project is designed to make communication easier between people who use sign language and people who may not understand it. The application captures hand gestures through the webcam, detects the hand landmarks using **MediaPipe**, classifies the gesture using a **Random Forest machine learning model**, displays the recognized sign as text, and converts the generated text into speech.

---

## ✨ Features

- 🎥 Real-time sign language recognition using a webcam
- ✋ Hand detection and landmark extraction using MediaPipe
- 🤖 Machine learning based gesture classification
- 📝 Converts recognized gestures into text
- 🔊 Converts the interpreted text into speech
- 📊 Displays prediction confidence
- ⚙️ Adjustable detection speed
- ▶️ Start and stop camera controls
- 🗑️ Clear interpreted text
- ⌫ Backspace support
- 🗣️ Manual text-to-speech using the **Speak** button
- ℹ️ About Us section
- 🌙 Dark and simple desktop interface

---

## 🧠 How It Works

The system works in the following stages:

```text
Webcam
   ↓
Capture Hand Gesture
   ↓
MediaPipe Hand Detection
   ↓
Extract 21 Hand Landmarks
   ↓
63 Landmark Features
   ↓
Random Forest Classifier
   ↓
Recognized Sign
   ↓
Text Output
   ↓
Text-to-Speech
   ↓
Audio Output
```

The training pipeline extracts **21 hand landmarks**, with each landmark containing `x`, `y`, and `z` coordinates. This results in **63 features per hand gesture**. These features are used to train a Random Forest classifier.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Main programming language |
| **OpenCV** | Webcam access and image processing |
| **MediaPipe** | Hand detection and landmark extraction |
| **Scikit-learn** | Machine learning model |
| **Random Forest** | Sign classification |
| **NumPy** | Numerical operations |
| **Pillow** | Image handling in the GUI |
| **Tkinter** | Desktop graphical user interface |
| **pyttsx3** | Text-to-speech conversion |
| **Pickle** | Saving and loading the trained model |

The project's `requirements.txt` currently lists OpenCV, MediaPipe, Scikit-learn, NumPy, TensorFlow, Pillow, and pyttsx3.

---

## 📁 Project Structure

```text
Sign-language-to-speech-and-text-converter/
│
├── Reports/
│   └── Project reports and documentation
│
├── data/
│   ├── imgs/
│   │   └── Training images organized by sign/class
│   │
│   └── dataset/
│       └── Processed dataset
│
├── models/
│   └── sign_language_model.pkl
│
├── app.py
├── collect_data.py
├── train_model.py
├── requirements.txt
└── README.md
```

The trained model is stored as `models/sign_language_model.pkl`. The application loads both the trained model and its class labels from this file.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/hamzashaikh8e-ship-it/Sign-language-to-speech-and-text-converter.git
```

Move into the project directory:

```bash
cd Sign-language-to-speech-and-text-converter
```

---

## 2. Create a Virtual Environment

It is recommended to use a virtual environment.

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The project dependencies include OpenCV, MediaPipe, Scikit-learn, NumPy, Pillow and pyttsx3.

---

# ▶️ Running the Application

After installing the dependencies and making sure the trained model is available in the `models` folder, run:

```bash
python app.py
```

The application will open the **Gestura – Sign Language Interpreter** interface.

The application starts with a splash screen and then displays the main interface.

---

# 📷 Using the Application

### Step 1 — Start the Camera

Click:

```text
Start Camera
```

The application will access your webcam and display the camera feed.

### Step 2 — Show a Sign

Place your hand in front of the camera and perform one of the gestures included in the trained dataset.

### Step 3 — Recognition

The application detects the hand and extracts its landmarks using MediaPipe.

The extracted landmarks are passed to the trained Random Forest model.

### Step 4 — Text Output

When the model recognizes a gesture with sufficient confidence, the corresponding class is added to the **Interpreted** text area.

The application also prevents the same detected gesture from being repeatedly added when it remains unchanged.

### Step 5 — Speech Output

Click:

```text
Speak
```

The recognized text will be converted into speech using `pyttsx3`.

---

# 🤖 Machine Learning Model

The project uses a **Random Forest Classifier** for sign language recognition.

The training process is:

```text
Training Images
      ↓
Hand Landmark Detection
      ↓
21 Hand Landmarks
      ↓
63 Features
      ↓
Train/Test Split
      ↓
Random Forest Classifier
      ↓
Model Evaluation
      ↓
Save Trained Model
```

The dataset is divided into training and testing sets using an 80/20 split. The Random Forest model uses 100 estimators with additional parameters to control tree depth and minimum sample requirements.

---

# 📚 Training Your Own Model

If you want to collect your own sign language data, first run:

```bash
python collect_data.py
```

The data collection script stores images under:

```text
data/imgs/
```

It is configured to collect **100 images per class** by default, with a short delay between captures.

After collecting the images, train the model using:

```bash
python train_model.py
```

The training script:

1. Reads the collected images.
2. Detects hands using MediaPipe.
3. Extracts hand landmarks.
4. Creates the feature dataset.
5. Splits the data into training and testing sets.
6. Trains the Random Forest classifier.
7. Calculates training and testing accuracy.
8. Generates a classification report.
9. Generates a confusion matrix.
10. Saves the trained model.

The processed dataset is saved as:

```text
data/dataset/dataset.pkl
```

and the trained model is saved as:

```text
models/sign_language_model.pkl
```


---

# 📊 Model Evaluation

The training script evaluates the model using:

- Training Accuracy
- Testing Accuracy
- Classification Report
- Confusion Matrix

The model is trained using the extracted hand-landmark features rather than directly using raw images.

---

# 🖥️ Application Interface

The application contains two main sections.

### Camera Section

The left side contains:

- Live camera feed
- Start Camera button
- Stop Camera button
- About Us button

### Interpretation Section

The right side contains:

- Recognized text
- Speak button
- Backspace button
- Clear button
- Detection speed control
- Confidence threshold control

These controls are implemented directly in the Tkinter interface.

---

# 🔊 Text-to-Speech

The project uses **pyttsx3** for speech synthesis.

Once text has been generated, clicking the **Speak** button reads the text aloud.

The speech engine is initialized when the application starts and uses a default speech rate configured in the application.

---

# 🎯 Project Objective

The main objective of this project is to develop an accessible system that can recognize sign language gestures and convert them into understandable text and speech.

The project demonstrates how **Computer Vision + Machine Learning + Text-to-Speech** can be combined to create a practical communication-assistance application.

---

# 🔮 Future Scope

The project can be improved further by adding:

- Support for a larger sign language vocabulary
- Recognition of complete words and sentences
- Dynamic gesture recognition for moving signs
- Support for both hands
- Improved accuracy with larger datasets
- Deep learning based recognition
- Mobile application support
- Web-based version
- Multiple language speech output
- Cloud-based model deployment
- Personalized/custom sign training
- Automatic sentence formation

---

# ⚠️ Limitations

The current system depends on the gestures/classes available in the training dataset.

Recognition performance can be affected by:

- Poor lighting
- Hand position
- Camera quality
- Background conditions
- Distance from the camera
- Similar-looking gestures
- Gestures that are not present in the training dataset

The current implementation is primarily designed for **static hand gesture recognition** using extracted hand landmarks.

---

# 👥 Developers

**Gestura – Sign Language Interpreter**

Developed by:

- **Ishwari Tungar**
- **Ashuta Acharya**
- **Hamza Shaikh**

The developer names are also included in the project application's source code.

---

# 📄 Project Documentation

Additional project documentation and reports can be found in the:

```text
Reports/
```

folder.

---

# ⭐ Acknowledgement

This project was developed as an academic/project implementation to explore the use of:

- Computer Vision
- Machine Learning
- MediaPipe
- Hand Landmark Detection
- Random Forest Classification
- Text-to-Speech

The project aims to demonstrate how these technologies can be combined to create an assistive communication system.

---

## 📌 Repository

**GitHub Repository:**  
[Sign Language to Speech and Text Converter — GitHub](https://github.com/hamzashaikh8e-ship-it/Sign-language-to-speech-and-text-converter?utm_source=chatgpt.com)

---

## 📜 License

This project is intended for educational and academic purposes.