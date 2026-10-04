"""
Sign Language Model Training Script
This script processes the collected images, extracts hand landmarks using MediaPipe,
and trains a Random Forest classifier for sign language recognition.
"""

import os
import pickle
import numpy as np
import cv2
import mediapipe as mp
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import time

# Configuration
DATA_DIR = './data/imgs'
DATASET_DIR = './data/dataset'
MODEL_DIR = './models'
MODEL_FILE = 'sign_language_model.pkl'

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def extract_hand_landmarks(image_path):
    """
    Extract hand landmarks from an image using MediaPipe
    Returns a list of 21 (x, y, z) coordinates = 63 features
    """
    img = cv2.imread(image_path)
    
    if img is None:
        return None
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.3
    ) as hands:
        
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract coordinates
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            
            return landmarks
        else:
            return None

def load_and_process_data():
    """
    Load images from data/imgs folder and extract hand landmarks
    Returns features (X) and labels (y)
    """
    print("\n" + "="*60)
    print("Processing Images and Extracting Hand Landmarks")
    print("="*60)
    
    data = []
    labels = []
    
    # Get all class directories
    classes = [d for d in os.listdir(DATA_DIR) 
               if os.path.isdir(os.path.join(DATA_DIR, d))]
    
    if len(classes) == 0:
        print(f"Error: No class folders found in {DATA_DIR}")
        print("Please run collect_data.py first to collect training images.")
        return None, None, None
    
    classes.sort()
    print(f"\nFound {len(classes)} classes: {', '.join(classes)}")
    
    total_images = 0
    successful_extractions = 0
    
    # Process each class
    for class_idx, class_name in enumerate(classes):
        class_dir = os.path.join(DATA_DIR, class_name)
        
        print(f"\nProcessing class '{class_name}' ({class_idx + 1}/{len(classes)})...")
        
        image_files = [f for f in os.listdir(class_dir) 
                      if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        class_successful = 0
        
        for img_idx, img_file in enumerate(image_files):
            img_path = os.path.join(class_dir, img_file)
            total_images += 1
            
            landmarks = extract_hand_landmarks(img_path)
            
            if landmarks is not None:
                data.append(landmarks)
                labels.append(class_idx)
                successful_extractions += 1
                class_successful += 1
            
            # Progress indicator
            if (img_idx + 1) % 20 == 0:
                print(f"  Processed {img_idx + 1}/{len(image_files)} images...", end='\r')
        
        print(f"  ✓ Class '{class_name}': {class_successful}/{len(image_files)} images processed successfully")
    
    print(f"\n{'='*60}")
    print(f"Total images processed: {total_images}")
    print(f"Successful landmark extractions: {successful_extractions}")
    print(f"Failed extractions: {total_images - successful_extractions}")
    print(f"{'='*60}")
    
    if successful_extractions == 0:
        print("\nError: No hand landmarks could be extracted from any image!")
        print("Please ensure images contain clear hand gestures.")
        return None, None, None
    
    return np.array(data), np.array(labels), classes

def save_dataset(X, y, classes):
    """Save processed dataset to disk"""
    create_directory(DATASET_DIR)
    
    dataset_path = os.path.join(DATASET_DIR, 'dataset.pkl')
    
    dataset = {
        'features': X,
        'labels': y,
        'classes': classes
    }
    
    with open(dataset_path, 'wb') as f:
        pickle.dump(dataset, f)
    
    print(f"\n✓ Dataset saved to: {dataset_path}")

def train_model(X, y, classes):
    """
    Train a Random Forest classifier on the extracted features
    """
    print("\n" + "="*60)
    print("Training Sign Language Recognition Model")
    print("="*60)
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\nDataset split:")
    print(f"  Training samples: {len(X_train)}")
    print(f"  Testing samples: {len(X_test)}")
    print(f"  Number of classes: {len(classes)}")
    print(f"  Features per sample: {X.shape[1]}")
    
    # Train Random Forest Classifier
    print("\nTraining Random Forest Classifier...")
    start_time = time.time()
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    training_time = time.time() - start_time
    print(f"✓ Training completed in {training_time:.2f} seconds")
    
    # Evaluate model
    print("\n" + "="*60)
    print("Model Evaluation")
    print("="*60)
    
    # Training accuracy
    y_train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, y_train_pred)
    print(f"\nTraining Accuracy: {train_accuracy * 100:.2f}%")
    
    # Testing accuracy
    y_test_pred = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    print(f"Testing Accuracy: {test_accuracy * 100:.2f}%")
    
    # Detailed classification report
    print("\nClassification Report:")
    print("-" * 60)
    target_names = [classes[i] for i in range(len(classes))]
    print(classification_report(y_test, y_test_pred, target_names=target_names))
    
    # Confusion matrix
    print("\nConfusion Matrix:")
    print("-" * 60)
    cm = confusion_matrix(y_test, y_test_pred)
    print(cm)
    
    return model

def save_model(model, classes):
    """Save trained model and class labels to disk"""
    create_directory(MODEL_DIR)
    
    model_path = os.path.join(MODEL_DIR, MODEL_FILE)
    
    model_data = {
        'model': model,
        'classes': classes
    }
    
    with open(model_path, 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\n✓ Model saved to: {model_path}")
    print(f"✓ Model contains {len(classes)} classes: {', '.join(classes)}")

def main():
    """Main training pipeline"""
    print("\n" + "#"*60)
    print("Sign Language Model Training Pipeline")
    print("#"*60)
    
    # Step 1: Load and process images
    X, y, classes = load_and_process_data()
    
    if X is None:
        return
    
    # Step 2: Save processed dataset
    save_dataset(X, y, classes)
    
    # Step 3: Train model
    model = train_model(X, y, classes)
    
    # Step 4: Save model
    save_model(model, classes)
    
    print("\n" + "="*60)
    print("Training Pipeline Completed Successfully!")
    print("="*60)
    print("\nNext steps:")
    print("  1. The trained model is ready to use")
    print("  2. You can now create the Tkinter UI application")
    print("  3. Load the model from:", os.path.join(MODEL_DIR, MODEL_FILE))
    print("="*60 + "\n")

if __name__ == "__main__":
    main()