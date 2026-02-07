# Enhanced File Management System with OCR

## New Features Added

### 1. Image to Text Conversion (OCR)
- Convert images to text using Tesseract OCR
- Drag-and-drop image upload
- Copy extracted text to clipboard
- Download extracted text as .txt file

### 2. Enhanced CSS Styling
- Colorful animated gradient background (orange, pink, blue, teal)
- Button hover effects with ripple animation
- Glowing card animations
- Smooth fade-in and slide-in animations
- Modern card design with blur effect
- Responsive design for mobile devices
- Custom scrollbar styling
- Hover effects on uploaded file items

### 3. Visual Effects
- Gradient backgrounds on all major elements
- Smooth transitions and animations
- Box-shadow glows on interactive elements
- Transform effects on hover
- Staggered animation timing for sequential elements

## Installation & Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install Tesseract OCR Engine
**Important**: Tesseract OCR engine must be installed separately.

#### For Windows:
1. Download the installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (e.g., `tesseract-ocr-w64-setup-v5.x.exe`)
3. Keep default installation path: `C:\Program Files\Tesseract-OCR`
4. The Python code will automatically find it

#### For Mac:
```bash
brew install tesseract
```

#### For Linux:
```bash
sudo apt-get install tesseract-ocr
```

### Step 3: Run the Application
```bash
python app.py
```

Then open: http://localhost:5000

## Features Overview

### Dashboard Page (/)
- Shows online users count
- Shows total uploaded files
- Upload new files with registration number
- View all uploaded files with timestamps
- Navigation to OCR and Files pages

### OCR Page (/ocr)
- Drag & drop image upload
- Image preview before extraction
- Extract text from images instantly
- Copy extracted text to clipboard
- Download extracted text as .txt file
- Beautiful UI with visual effects

### Files Page (/files)
- View all uploaded files
- Navigate through file system

## File Structure
```
.
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── static/
│   └── style.css            # Enhanced styling with animations
├── templates/
│   ├── dashboard.html       # Main dashboard page
│   ├── ocr.html            # OCR conversion page
│   └── files.html          # Files listing page
└── uploads/                 # Directory for uploaded files
```

## Customization

### Change Color Scheme
Edit the CSS in `static/style.css` to modify gradient colors:
- Line 43: Background gradient colors
- Line 79-83: Card gradient
- Line 160-161: Button gradient

### Modify Animation Speed
- Change animation durations in keyframes (e.g., `15s`, `0.8s`)
- Change transition durations in hover effects

## Troubleshooting

### Tesseract Not Found Error
If you see "TesseractNotFoundError", ensure:
1. Tesseract is installed correctly
2. For Windows: Check installation path is `C:\Program Files\Tesseract-OCR`
3. Add to environment variables if needed

### OCR Returns Empty Text
- Image quality may be too low
- Try a clearer image with better contrast
- Supported formats: PNG, JPG, JPEG, BMP, TIFF

## Browser Support
- Chrome/Edge (Recommended)
- Firefox
- Safari
- Modern mobile browsers

Enjoy your enhanced file management system with OCR!
