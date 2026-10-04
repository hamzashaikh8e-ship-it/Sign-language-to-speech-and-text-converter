"""
Sign Language Data Collection Script
This script captures images from webcam for training the sign language model.
Press 's' to start/stop capturing, 'q' to quit and move to next class.
"""

import cv2
import os
import time

# Configuration
DATA_DIR = './data/imgs'
NUM_IMAGES_PER_CLASS = 100
CAPTURE_DELAY = 0.1  # Delay between captures in seconds

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def collect_images_for_class(class_name, num_images):
    """Collect images for a specific class"""
    class_dir = os.path.join(DATA_DIR, class_name)
    create_directory(class_dir)
    
    # Check how many images already exist
    existing_images = len([f for f in os.listdir(class_dir) if f.endswith('.jpg')])
    
    if existing_images >= num_images:
        print(f"\n✓ Class '{class_name}' already has {existing_images} images.")
        choice = input("Do you want to add more images? (y/n): ")
        if choice.lower() != 'y':
            return
        start_index = existing_images
    else:
        start_index = existing_images
        print(f"\nFound {existing_images} existing images. Need {num_images - existing_images} more.")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not access webcam!")
        return
    
    print(f"\n{'='*60}")
    print(f"Collecting images for class: {class_name}")
    print(f"{'='*60}")
    print("\nInstructions:")
    print("  - Position your hand in the frame")
    print("  - Press 's' to START/STOP capturing")
    print("  - Press 'q' to QUIT and move to next class")
    print("  - Keep your hand steady and vary position slightly between captures")
    print(f"\nTarget: {num_images} images")
    
    capturing = False
    counter = start_index
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Create display copy
        display_frame = frame.copy()
        
        # Draw info on frame
        cv2.putText(display_frame, f"Class: {class_name}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(display_frame, f"Images: {counter}/{num_images}", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if capturing:
            cv2.putText(display_frame, "CAPTURING...", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.rectangle(display_frame, (10, 10), (630, 470), (0, 255, 0), 2)
        else:
            cv2.putText(display_frame, "Press 's' to start", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.rectangle(display_frame, (10, 10), (630, 470), (0, 0, 255), 2)
        
        cv2.imshow('Data Collection', display_frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s'):
            capturing = not capturing
            if capturing:
                print(f"\n▶ Started capturing images for '{class_name}'")
            else:
                print(f"\n⏸ Paused capturing")
        
        elif key == ord('q'):
            print(f"\n✓ Finished collecting for '{class_name}'. Total: {counter} images")
            break
        
        # Capture image if in capturing mode
        if capturing and counter < num_images:
            img_path = os.path.join(class_dir, f'{class_name}_{counter}.jpg')
            cv2.imwrite(img_path, frame)
            print(f"  Saved: {img_path} ({counter + 1}/{num_images})", end='\r')
            counter += 1
            
            if counter >= num_images:
                print(f"\n✓ Completed! Collected {num_images} images for '{class_name}'")
                capturing = False
            
            time.sleep(CAPTURE_DELAY)
    
    cap.release()
    cv2.destroyAllWindows()

def main():
    """Main function to collect data for all classes"""
    print("\n" + "="*60)
    print("Sign Language Data Collection Tool")
    print("="*60)
    
    create_directory(DATA_DIR)
    
    # Get class names from user
    print("\nEnter the classes/gestures you want to collect data for.")
    print("Examples: A, B, C, Hello, Thanks, etc.")
    print("Type 'done' when finished entering classes.\n")
    
    classes = []
    while True:
        class_name = input(f"Enter class name #{len(classes) + 1} (or 'done'): ").strip()
        
        if class_name.lower() == 'done':
            if len(classes) == 0:
                print("Please enter at least one class!")
                continue
            break
        
        if class_name == '':
            print("Class name cannot be empty!")
            continue
        
        if class_name in classes:
            print(f"Class '{class_name}' already added!")
            continue
        
        classes.append(class_name)
        print(f"  ✓ Added: {class_name}")
    
    print(f"\n{'='*60}")
    print(f"Will collect {NUM_IMAGES_PER_CLASS} images for {len(classes)} classes:")
    for i, cls in enumerate(classes, 1):
        print(f"  {i}. {cls}")
    print(f"{'='*60}")
    
    input("\nPress Enter to start data collection...")
    
    # Collect images for each class
    for i, class_name in enumerate(classes, 1):
        print(f"\n\n{'#'*60}")
        print(f"Class {i}/{len(classes)}")
        print(f"{'#'*60}")
        collect_images_for_class(class_name, NUM_IMAGES_PER_CLASS)
        
        if i < len(classes):
            print(f"\nGet ready for next class: {classes[i]}")
            time.sleep(2)
    
    print("\n" + "="*60)
    print("Data collection completed!")
    print("="*60)
    print(f"\nImages saved in: {DATA_DIR}")
    print(f"Total classes: {len(classes)}")
    print("\nYou can now run 'train_model.py' to train the model.")

if __name__ == "__main__":
    main()