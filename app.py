"""
Gestura - Sign Language Interpreter
A real-time sign language recognition application
Designed by: Ishwari Tungar, Ashuta Acharya, Hamza Shaikh
"""

import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import pickle
import numpy as np
import mediapipe as mp
import threading
import time
import pyttsx3

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


class SplashScreen:
    """Splash screen matching the design sketch"""
    
    def __init__(self, root, duration=5000):
        self.root = root
        self.duration = duration
        
        # Create splash window
        self.splash = tk.Toplevel(root)
        self.splash.title("Gestura")
        
        # Center the splash screen
        window_width = 800
        window_height = 600
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.splash.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Remove window decorations
        self.splash.overrideredirect(True)
        
        # Dark aesthetic colors
        bg_color = "#1a1a1a"
        text_color = "#ffffff"
        subtext_color = "#888888"
        accent_color = "#2a2a2a"
        
        self.splash.configure(bg=bg_color)
        
        # Main frame with subtle border
        border_frame = tk.Frame(self.splash, bg=accent_color, padx=2, pady=2)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        content_frame = tk.Frame(border_frame, bg=bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Hand logo with G1
        logo_frame = tk.Frame(content_frame, bg=bg_color)
        logo_frame.pack(pady=(60, 20))
        
        # Simple hand representation
        logo_canvas = tk.Canvas(logo_frame, width=150, height=150, bg=bg_color, highlightthickness=0)
        logo_canvas.pack()
        
        # Draw hand outline
        logo_canvas.create_oval(60, 60, 90, 90, outline=text_color, width=3)
        logo_canvas.create_text(75, 75, text="G1", font=("Helvetica", 20, "bold"), fill=text_color)
        # Fingers
        logo_canvas.create_line(75, 60, 75, 20, width=3, fill=text_color)
        logo_canvas.create_line(85, 60, 95, 25, width=3, fill=text_color)
        logo_canvas.create_line(95, 70, 110, 35, width=3, fill=text_color)
        logo_canvas.create_line(55, 70, 40, 35, width=3, fill=text_color)
        logo_canvas.create_line(65, 60, 55, 25, width=3, fill=text_color)
        # Wave lines
        logo_canvas.create_arc(35, 55, 50, 70, start=90, extent=90, style=tk.ARC, outline=text_color, width=2)
        logo_canvas.create_arc(30, 50, 45, 65, start=90, extent=90, style=tk.ARC, outline=text_color, width=2)
        
        # App name
        app_name = tk.Label(
            content_frame,
            text="GESTURA",
            font=("Helvetica", 48, "bold"),
            bg=bg_color,
            fg=text_color
        )
        app_name.pack(pady=(10, 10))
        
        # Tagline
        tagline = tk.Label(
            content_frame,
            text="(Where gestures speak!)",
            font=("Helvetica", 16, "italic"),
            bg=bg_color,
            fg=subtext_color
        )
        tagline.pack(pady=(0, 50))
        
        # Separator line
        separator = tk.Frame(content_frame, bg=accent_color, height=1)
        separator.pack(fill=tk.X, padx=100, pady=20)
        
        # Developers section
        dev_label = tk.Label(
            content_frame,
            text="Developed By :-",
            font=("Helvetica", 14),
            bg=bg_color,
            fg=subtext_color
        )
        dev_label.pack(pady=(10, 15))
        
        # Developer names in a row
        dev_container = tk.Frame(content_frame, bg=bg_color)
        dev_container.pack()
        
        developers = ["Ishwari", "Ashuta", "Hamza"]
        
        for i, dev in enumerate(developers):
            dev_frame = tk.Frame(dev_container, bg=bg_color)
            dev_frame.pack(side=tk.LEFT, padx=30)
            
            bullet = tk.Label(
                dev_frame,
                text="○",
                font=("Helvetica", 12),
                bg=bg_color,
                fg=text_color
            )
            bullet.pack(side=tk.LEFT, padx=(0, 5))
            
            dev_name = tk.Label(
                dev_frame,
                text=dev,
                font=("Helvetica", 13),
                bg=bg_color,
                fg=text_color
            )
            dev_name.pack(side=tk.LEFT)
        
        # Loading animation
        self.loading_label = tk.Label(
            content_frame,
            text="Loading",
            font=("Helvetica", 11),
            bg=bg_color,
            fg=subtext_color
        )
        self.loading_label.pack(side=tk.BOTTOM, pady=40)
        
        # Animate loading
        self.animate_loading()
        
        # Schedule close
        self.splash.after(duration, self.close_splash)
    
    def animate_loading(self, dots=0):
        """Animate loading text"""
        if self.splash.winfo_exists():
            text = "Loading" + "." * (dots % 4)
            self.loading_label.config(text=text)
            self.splash.after(400, lambda: self.animate_loading(dots + 1))
    
    def close_splash(self):
        """Close splash and show main window"""
        self.splash.destroy()
        self.root.deiconify()


class AboutWindow:
    """About Us window matching the design sketch"""
    
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("About Us")
        self.window.geometry("700x600")
        self.window.resizable(False, False)
        
        # Dark colors
        bg_color = "#1a1a1a"
        text_color = "#ffffff"
        subtext_color = "#888888"
        border_color = "#2a2a2a"
        
        self.window.configure(bg=bg_color)
        
        # Main container
        main_frame = tk.Frame(self.window, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Title
        title = tk.Label(
            main_frame,
            text="ABOUT US",
            font=("Helvetica", 28, "bold"),
            bg=bg_color,
            fg=text_color
        )
        title.pack(pady=(0, 30))
        
        # Team members
        members = [
            {
                "name": "Ishwari Sanjay Tungar",
                "prn": "23612590134"
            },
            {
                "name": "Ashuta Deepak Acharya",
                "prn": "23612590081"
            },
            {
                "name": "Shaikh Mohammad Hamza Mohasin",
                "prn": "23612590126"
            }
        ]
        
        for member in members:
            member_frame = tk.Frame(main_frame, bg=border_color, padx=2, pady=2)
            member_frame.pack(fill=tk.X, pady=10)
            
            inner_frame = tk.Frame(member_frame, bg=bg_color)
            inner_frame.pack(fill=tk.X, padx=15, pady=15)
            
            bullet = tk.Label(
                inner_frame,
                text="○",
                font=("Helvetica", 14),
                bg=bg_color,
                fg=text_color
            )
            bullet.pack(side=tk.LEFT, padx=(0, 10))
            
            info_frame = tk.Frame(inner_frame, bg=bg_color)
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            name_label = tk.Label(
                info_frame,
                text=member["name"],
                font=("Helvetica", 14, "bold"),
                bg=bg_color,
                fg=text_color,
                anchor='w'
            )
            name_label.pack(fill=tk.X)
            
            prn_label = tk.Label(
                info_frame,
                text=member["prn"],
                font=("Helvetica", 12),
                bg=bg_color,
                fg=subtext_color,
                anchor='w'
            )
            prn_label.pack(fill=tk.X, pady=(3, 0))
        
        # Separator
        separator = tk.Frame(main_frame, bg=border_color, height=2)
        separator.pack(fill=tk.X, pady=30)
        
        # College info
        college_label = tk.Label(
            main_frame,
            text="SIR DR. M.S. GOSAVI POLYTECHNIC\nINSTITUTE - 1800",
            font=("Helvetica", 13, "bold"),
            bg=bg_color,
            fg=text_color,
            justify='center'
        )
        college_label.pack(pady=(0, 20))
        
        # Guided by
        guided_label = tk.Label(
            main_frame,
            text="GUIDED BY :-",
            font=("Helvetica", 12),
            bg=bg_color,
            fg=subtext_color
        )
        guided_label.pack(pady=(0, 10))
        
        guide_label = tk.Label(
            main_frame,
            text="Prof. H. R. Mankar",
            font=("Helvetica", 14, "bold"),
            bg=bg_color,
            fg=text_color
        )
        guide_label.pack()
        
        # Close button
        close_btn = tk.Button(
            main_frame,
            text="Close",
            font=("Helvetica", 11, "bold"),
            bg="#2a2a2a",
            fg=text_color,
            activebackground="#3a3a3a",
            activeforeground=text_color,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.window.destroy,
            padx=30,
            pady=10
        )
        close_btn.pack(side=tk.BOTTOM, pady=(20, 0))


class GesturaApp:
    """Main application matching the design sketch"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gestura - Sign Language Interpreter")
        self.root.geometry("1400x850")
        self.root.configure(bg="#0d0d0d")
        
        # Hide main window initially
        self.root.withdraw()
        
        # Dark minimal colors
        self.colors = {
            'bg': '#0d0d0d',
            'panel': '#1a1a1a',
            'border': '#2a2a2a',
            'text': '#ffffff',
            'subtext': '#888888',
            'button': '#2a2a2a',
            'button_hover': '#3a3a3a',
            'accent': '#4a9eff'
        }
        
        # Application state
        self.camera_running = False
        self.cap = None
        self.model = None
        self.classes = None
        self.detection_speed = 0.5
        self.confidence_threshold = 0.5
        self.last_detection_time = 0
        self.detected_text = []
        
        # Text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        
        # Load model
        self.load_model()
        
        # Create UI
        self.create_ui()
        
        # Show splash screen
        SplashScreen(self.root, duration=5000)
    
    def load_model(self):
        """Load the trained model"""
        try:
            with open('./models/sign_language_model.pkl', 'rb') as f:
                model_data = pickle.load(f)
                self.model = model_data['model']
                self.classes = model_data['classes']
            print(f"✓ Model loaded with {len(self.classes)} classes")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model:\n{str(e)}")
    
    def create_ui(self):
        """Create main UI matching the sketch"""
        
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Left side - Camera and buttons
        left_panel = tk.Frame(main_container, bg=self.colors['bg'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Camera section with label
        camera_label_frame = tk.Frame(left_panel, bg=self.colors['panel'])
        camera_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(
            camera_label_frame,
            text="Camera",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['panel'],
            fg=self.colors['text'],
            anchor='w'
        ).pack(padx=10, pady=8)
        
        # Camera display with FIXED size
        camera_container = tk.Frame(left_panel, bg=self.colors['bg'])
        camera_container.pack(fill=tk.BOTH, expand=True)
        
        camera_frame = tk.Frame(camera_container, bg=self.colors['border'], padx=2, pady=2, width=800, height=600)
        camera_frame.pack(anchor='center', padx=10, pady=10)
        camera_frame.pack_propagate(False)
        
        self.camera_label = tk.Label(
            camera_frame,
            bg='black',
            text="Camera Inactive",
            font=("Helvetica", 14),
            fg=self.colors['subtext']
        )
        self.camera_label.pack(fill=tk.BOTH, expand=True)
        
        # Bottom buttons (Start, Stop, About Us)
        bottom_buttons = tk.Frame(left_panel, bg=self.colors['bg'])
        bottom_buttons.pack(fill=tk.X, pady=(10, 0))
        
        btn_style = {
            'font': ('Helvetica', 11, 'bold'),
            'bg': self.colors['button'],
            'fg': self.colors['text'],
            'activebackground': self.colors['button_hover'],
            'activeforeground': self.colors['text'],
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'bd': 0
        }
        
        self.start_btn = tk.Button(
            bottom_buttons,
            text="Start Camera",
            command=self.start_camera,
            **btn_style
        )
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=10)
        
        self.stop_btn = tk.Button(
            bottom_buttons,
            text="Stop Camera",
            command=self.stop_camera,
            state=tk.DISABLED,
            **btn_style
        )
        self.stop_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=10)
        
        about_btn = tk.Button(
            bottom_buttons,
            text="About Us",
            command=self.show_about,
            **btn_style
        )
        about_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0), ipady=10)
        
        # Right side - Output and controls
        right_panel = tk.Frame(main_container, bg=self.colors['bg'], width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Interpreted text section
        text_label_frame = tk.Frame(right_panel, bg=self.colors['panel'])
        text_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(
            text_label_frame,
            text="Interpreted:",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['panel'],
            fg=self.colors['text'],
            anchor='w'
        ).pack(padx=10, pady=8)
        
        # Text display
        text_frame = tk.Frame(right_panel, bg=self.colors['border'], padx=2, pady=2)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_display = tk.Text(
            text_frame,
            font=("Consolas", 12),
            bg=self.colors['panel'],
            fg=self.colors['text'],
            wrap=tk.WORD,
            padx=10,
            pady=10,
            insertbackground=self.colors['accent'],
            selectbackground=self.colors['accent'],
            relief=tk.FLAT,
            height=8
        )
        self.text_display.pack(fill=tk.BOTH, expand=True)
        
        # Text control buttons
        text_buttons = tk.Frame(right_panel, bg=self.colors['bg'])
        text_buttons.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(
            text_buttons,
            text="Speak",
            command=self.speak_text,
            **btn_style
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3), ipady=8)
        
        tk.Button(
            text_buttons,
            text="Backspace",
            command=self.backspace_text,
            **btn_style
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3, ipady=8)
        
        tk.Button(
            text_buttons,
            text="Clear",
            command=self.clear_text,
            **btn_style
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0), ipady=8)
        
        # Sliders section
        sliders_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        sliders_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Detection speed label
        speed_label_frame = tk.Frame(sliders_frame, bg=self.colors['bg'])
        speed_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(
            speed_label_frame,
            text="Speak:",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        self.speed_value_label = tk.Label(
            speed_label_frame,
            text="50",
            font=("Helvetica", 10),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.speed_value_label.pack(side=tk.RIGHT)
        
        tk.Label(
            speed_label_frame,
            text="100",
            font=("Helvetica", 9),
            bg=self.colors['bg'],
            fg=self.colors['subtext']
        ).pack(side=tk.RIGHT, padx=(0, 5))
        
        tk.Label(
            speed_label_frame,
            text="0",
            font=("Helvetica", 9),
            bg=self.colors['bg'],
            fg=self.colors['subtext']
        ).pack(side=tk.LEFT, padx=(60, 0))
        
        # Detection speed slider
        self.speed_slider = tk.Scale(
            sliders_frame,
            from_=0.1,
            to=2.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            highlightthickness=0,
            troughcolor=self.colors['button'],
            activebackground=self.colors['accent'],
            command=self.update_speed,
            showvalue=False,
            length=380
        )
        self.speed_slider.set(0.5)
        self.speed_slider.pack(fill=tk.X, pady=(0, 15))
        
        # Confidence label
        conf_label_frame = tk.Frame(sliders_frame, bg=self.colors['bg'])
        conf_label_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(
            conf_label_frame,
            text="Confidence:",
            font=("Helvetica", 10, "bold"),
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(side=tk.LEFT)
        
        self.conf_value_label = tk.Label(
            conf_label_frame,
            text="50",
            font=("Helvetica", 10),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.conf_value_label.pack(side=tk.RIGHT)
        
        tk.Label(
            conf_label_frame,
            text="100",
            font=("Helvetica", 9),
            bg=self.colors['bg'],
            fg=self.colors['subtext']
        ).pack(side=tk.RIGHT, padx=(0, 5))
        
        tk.Label(
            conf_label_frame,
            text="0",
            font=("Helvetica", 9),
            bg=self.colors['bg'],
            fg=self.colors['subtext']
        ).pack(side=tk.LEFT, padx=(90, 0))
        
        # Confidence slider
        self.confidence_slider = tk.Scale(
            sliders_frame,
            from_=0.1,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            bg=self.colors['bg'],
            fg=self.colors['text'],
            highlightthickness=0,
            troughcolor=self.colors['button'],
            activebackground=self.colors['accent'],
            command=self.update_confidence,
            showvalue=False,
            length=380
        )
        self.confidence_slider.set(0.5)
        self.confidence_slider.pack(fill=tk.X, pady=(0, 15))
        
        # Current prediction section
        pred_section = tk.Frame(right_panel, bg=self.colors['border'], padx=2, pady=2)
        pred_section.pack(fill=tk.X, pady=(10, 0))
        
        pred_inner = tk.Frame(pred_section, bg=self.colors['panel'])
        pred_inner.pack(fill=tk.X, padx=15, pady=15)
        
        self.prediction_label = tk.Label(
            pred_inner,
            text="A",
            font=("Helvetica", 60, "bold"),
            bg=self.colors['panel'],
            fg=self.colors['accent']
        )
        self.prediction_label.pack()
        
        self.confidence_display = tk.Label(
            pred_inner,
            text="Confidence: 40%",
            font=("Helvetica", 11),
            bg=self.colors['panel'],
            fg=self.colors['subtext']
        )
        self.confidence_display.pack(pady=(5, 0))
    
    def update_speed(self, value):
        """Update detection speed"""
        self.detection_speed = float(value)
        display_val = int((float(value) - 0.1) / 1.9 * 100)
        self.speed_value_label.config(text=str(display_val))
    
    def update_confidence(self, value):
        """Update confidence threshold"""
        self.confidence_threshold = float(value)
        display_val = int(float(value) * 100)
        self.conf_value_label.config(text=str(display_val))
    
    def start_camera(self):
        """Start camera"""
        if not self.camera_running:
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Cannot access camera!")
                return
            
            self.camera_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            
            # Start detection thread
            self.detection_thread = threading.Thread(target=self.detect_signs, daemon=True)
            self.detection_thread.start()
    
    def stop_camera(self):
        """Stop camera"""
        if self.camera_running:
            self.camera_running = False
            
            if self.cap:
                self.cap.release()
                self.cap = None
            
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            
            self.camera_label.config(image='', text="Camera Inactive", bg='black')
            self.prediction_label.config(text="-")
            self.confidence_display.config(text="Confidence: -")
    
    def detect_signs(self):
        """Detection loop"""
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.3,
            min_tracking_confidence=0.3
        ) as hands:
            
            while self.camera_running:
                ret, frame = self.cap.read()
                if not ret:
                    continue
                
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                results = hands.process(frame_rgb)
                
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style()
                        )
                    
                    current_time = time.time()
                    if current_time - self.last_detection_time >= self.detection_speed:
                        self.predict_sign(results.multi_hand_landmarks[0])
                        self.last_detection_time = current_time
                
                # Convert and resize frame to FIXED size (796x596 to fit in 800x600 container)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (796, 596), interpolation=cv2.INTER_LINEAR)
                
                # Convert to PhotoImage
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update camera label
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk, text='')
                
                # Small delay to prevent glitching
                time.sleep(0.03)
    
    def predict_sign(self, hand_landmarks):
        """Predict sign"""
        if not self.model:
            return
        
        landmarks = []
        for landmark in hand_landmarks.landmark:
            landmarks.extend([landmark.x, landmark.y, landmark.z])
        
        landmarks_array = np.array([landmarks])
        prediction = self.model.predict(landmarks_array)
        probabilities = self.model.predict_proba(landmarks_array)
        
        predicted_class = self.classes[prediction[0]]
        confidence = np.max(probabilities)
        
        self.root.after(0, self.update_prediction_display, predicted_class, confidence)
        
        if confidence >= self.confidence_threshold:
            self.root.after(0, self.add_to_text, predicted_class)
    
    def update_prediction_display(self, predicted_class, confidence):
        """Update prediction"""
        self.prediction_label.config(text=predicted_class)
        self.confidence_display.config(text=f"Confidence: {confidence * 100:.0f}%")
    
    def add_to_text(self, text):
        """Add to text display"""
        if len(self.detected_text) == 0 or self.detected_text[-1] != text:
            self.detected_text.append(text)
            current_text = self.text_display.get("1.0", tk.END).strip()
            
            if current_text:
                new_text = current_text + " " + text
            else:
                new_text = text
            
            self.text_display.delete("1.0", tk.END)
            self.text_display.insert("1.0", new_text)
    
    def speak_text(self):
        """Speak text"""
        text = self.text_display.get("1.0", tk.END).strip()
        if not text:
            return
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()
    
    def _speak(self, text):
        """Internal speak"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def backspace_text(self):
        """Backspace"""
        if self.detected_text:
            self.detected_text.pop()
            new_text = " ".join(self.detected_text)
            self.text_display.delete("1.0", tk.END)
            self.text_display.insert("1.0", new_text)
    
    def clear_text(self):
        """Clear text"""
        self.detected_text.clear()
        self.text_display.delete("1.0", tk.END)
    
    def show_about(self):
        """Show about window"""
        AboutWindow(self.root)
    
    def on_closing(self):
        """Handle closing"""
        self.stop_camera()
        self.root.destroy()


def main():
    """Main entry"""
    root = tk.Tk()
    app = GesturaApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()