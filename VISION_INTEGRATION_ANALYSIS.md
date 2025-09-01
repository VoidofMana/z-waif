# Z-WAIF Vision Integration Analysis & Replacement Guide

## Overview
The Z-WAIF project has a comprehensive vision system that allows the AI character to process and respond to images from multiple sources. This document analyzes the current implementation and provides guidance for replacing or extending the vision capabilities.

## Current Vision Integrations

### 1. **Image Capture Sources**
The system supports multiple image input methods:

#### Camera Capture (`utils/camera.py`)
- **Webcam Input**: Real-time capture from default camera (cv2.VideoCapture)
- **Resolution**: Configurable via `IMG_SCALE` environment variable (320x240 base resolution)
- **Preview System**: Optional image preview before sending (controlled by `cam_image_preview`)
- **File**: `utils/camera.py` - Function: `capture_pic()`

#### Screenshot Capture (`utils/camera.py`)
- **Screen Capture**: Uses pyautogui to capture full screen
- **Auto-resize**: Intelligent resizing based on IMG_SCALE (400x400 base resolution)
- **File**: `utils/camera.py` - Function: `capture_screenshot()`

#### File Upload System (`utils/camera.py`)
- **Image Feed**: File browser for uploading images
- **Supported Formats**: JPG, PNG, JPEG
- **Auto-resize**: Maintains aspect ratio (360x360 base resolution)
- **File**: `utils/camera.py` - Functions: `use_image_feed()`, `browse_feed_image()`

#### Face Tracking System (`utils/camera.py`)
- **Face Detection**: Uses OpenCV Haar Cascades for face detection
- **VTube Studio Integration**: Controls character eye movement based on face position
- **File**: `utils/camera.py` - Function: `capture_follow_pic()`

### 2. **Vision Processing APIs**

#### Oobabooga API Integration (`API/api_controller.py`, `API/Oogabooga_Api_Support.py`)
- **Image Encoding**: Base64 encoding of images
- **Format**: HTML-style image embedding: `<img src="data:image/jpeg;base64,{img_str}">`
- **Configuration**:
  - Character: `OOBA_VISUAL_CHARACTER_NAME`
  - Preset: `OOBA_VISUAL_PRESET_NAME`
  - Port: `IMG_PORT` (separate from main text API)
- **Functions**: `view_image()`, `view_image_streaming()`

#### Ollama API Integration (`API/ollama_api.py`, `API/api_controller.py`)
- **Image Handling**: File path-based image passing
- **Model**: Separate visual model (`ZW_OLLAMA_MODEL_VISUAL`)
- **Configuration**:
  - Guidance messages: `OLLAMA_VISUAL_ENCODE_GUIDANCE`
  - Character card: `OLLAMA_VISUAL_CARD` (BASE/VISUAL/OFF)
- **Functions**: `api_standard_image()`, `api_stream_image()`

### 3. **Vision Control Interface**

#### Web UI Controls (`utils/web_ui.py`)
- **Take/Send Image**: Manual image capture trigger
- **Image Feed Toggle**: Switch between camera and file upload
- **Direct Talk**: Voice input while taking images
- **Image Preview**: Preview before sending to AI
- **Screenshot Mode**: Toggle screenshot vs camera capture

#### Hotkey Integration (`utils/hotkeys.py`)
- **VIEW_IMAGE_PRESSED**: Trigger image capture
- **CANCEL_IMAGE_PRESSED**: Cancel image preview
- **Functions**: `input_view_image()`, `input_cancel_image()`

#### Main Integration (`main.py`)
- **main_view_image()**: Primary image processing function
- **hangout_view_image_reply()**: Hangout mode image processing
- **view_image_prompt_get()**: Voice input during image capture

### 4. **Vision Configuration**

#### Environment Variables (`.env`)
```properties
MODULE_VISUAL = OFF                    # Enable/disable vision system
API_TYPE_VISUAL = Ollama              # Vision API backend
IMG_PORT = 127.0.0.1:5007            # Visual API port
IMG_SCALE = 1.0                       # Image scaling factor
OLLAMA_VISUAL_ENCODE_GUIDANCE = ON    # Include guidance messages
OLLAMA_VISUAL_CARD = VISUAL           # Character card type
ZW_OLLAMA_MODEL_VISUAL = "model_name" # Ollama vision model
OOBA_VISUAL_CHARACTER_NAME = name     # Oobabooga character
OOBA_VISUAL_PRESET_NAME = preset      # Oobabooga preset
EYES_FOLLOW = "Random"                # Eye tracking mode
EYES_START_ID = 14                    # VTube Studio integration
```

#### Character Cards (`Configurables/`)
- **CharacterCardVisual.yaml**: Specialized prompt for vision tasks
- **CharacterCard.yaml**: Main character personality (can be reused)

### 5. **VTube Studio Integration**

#### Eye Tracking (`utils/vtube_studio.py`)
- **Face Following**: Camera-based eye movement control
- **Random Movement**: Automatic eye movement patterns
- **Look Levels**: 6 different eye positions based on face detection
- **Real-time Control**: Continuous face tracking and eye adjustment

## Architecture Flow

```
Image Source (Camera/Screenshot/File)
    ↓
Image Processing (Resize/Format)
    ↓ 
Save to LiveImage.png
    ↓
API Selection (Oobabooga/Ollama)
    ↓
Vision Processing (Base64/File Path)
    ↓
Response Generation (Streaming/Standard)
    ↓
Post-processing (RP suppression, HTML decode)
    ↓
History Storage & Voice Output
```

## Key Files for Vision Integration

### Core Vision Files
1. **`utils/camera.py`** - Image capture and processing
2. **`API/api_controller.py`** - Main vision API coordination
3. **`API/ollama_api.py`** - Ollama vision integration
4. **`API/Oogabooga_Api_Support.py`** - Oobabooga vision integration
5. **`utils/web_ui.py`** - Vision UI controls
6. **`main.py`** - Vision workflow integration

### Configuration Files
1. **`.env`** - Vision environment variables
2. **`Configurables/CharacterCardVisual.yaml`** - Vision prompts
3. **`utils/hotkeys.py`** - Vision keyboard controls
4. **`utils/vtube_studio.py`** - Eye tracking integration

## Replacement Strategy Guide

### To Replace the Entire Vision System:

#### 1. **New Image Processing Backend**
Replace functions in `utils/camera.py`:
- `capture_pic()` - Webcam capture
- `capture_screenshot()` - Screen capture  
- `use_image_feed()` - File upload
- Update image format/resolution as needed

#### 2. **New Vision API Integration**
Create new API module following pattern of `API/ollama_api.py`:
- Implement `api_standard_image(history)` function
- Implement `api_stream_image(history)` function  
- Handle your specific image format requirements
- Add new API type to `API_TYPE_VISUAL` options

#### 3. **Update Main Controller**
Modify `API/api_controller.py`:
- Add new API type condition in `view_image()` and `view_image_streaming()`
- Implement image encoding/formatting for your API
- Configure request structure for your vision service

#### 4. **Environment Configuration** 
Update `.env` file:
- Add new environment variables for your vision service
- Update `API_TYPE_VISUAL` to your new type
- Configure connection details (URLs, keys, models)

#### 5. **Character Prompting**
Modify `Configurables/CharacterCardVisual.yaml`:
- Adapt prompts for your vision model's expectations
- Include specific instructions for your model's capabilities

### To Add Additional Vision Sources:

#### 1. **New Capture Methods**
Add functions to `utils/camera.py`:
- Follow existing pattern (capture → resize → save to LiveImage.png)
- Add corresponding UI controls in `utils/web_ui.py`
- Add hotkey support in `utils/hotkeys.py`

#### 2. **Specialized Processing**
- Add preprocessing functions for specific image types
- Implement custom resize/formatting logic
- Add validation for image quality/format

### To Integrate Different Vision Models:

#### 1. **API Abstraction**
- Create new module in `API/` directory
- Implement standard interface: `api_standard_image()`, `api_stream_image()`
- Handle model-specific image formatting

#### 2. **Model Configuration**
- Add environment variables for model settings
- Create configuration files for model parameters
- Implement temperature/sampling controls if supported

#### 3. **Response Processing**
- Handle model-specific response formats
- Implement streaming if supported by your model
- Add error handling for vision-specific failures

## Dependencies Required for Vision

### Python Packages
- `opencv-python` (cv2) - Camera and image processing
- `pyautogui` - Screenshot capture
- `numpy` - Image array processing
- `tkinter` - File dialog interface
- `base64` - Image encoding for APIs
- `requests` - API communication
- `ollama` (if using Ollama)

### System Requirements
- Camera access for webcam features
- Screen capture permissions for screenshot mode
- File system access for image uploads
- Network access for vision API calls

## Integration Points for Replacement

### Minimal Integration Points:
1. **Image Input**: Any system that saves to `LiveImage.png`
2. **API Call**: Function that takes image + text and returns description
3. **Response Handling**: Text processing and history storage

### Full Integration Points:
1. **UI Controls**: Web interface for vision settings
2. **Hotkey System**: Keyboard shortcuts for image capture  
3. **Streaming Support**: Real-time response generation
4. **VTube Integration**: Eye tracking and character animation
5. **Voice Integration**: Speaking during/after image processing
6. **Memory System**: RAG database integration for visual memories

## Current Limitations & Improvement Opportunities

### Current Limitations:
1. **Single Image Processing**: Only processes one image at a time
2. **Fixed Resolution**: Image size controlled by single scale factor
3. **Limited Format Support**: Only JPG/PNG/JPEG for uploads
4. **Basic Face Detection**: Simple Haar cascade implementation
5. **Static API Selection**: Cannot dynamically switch vision APIs

### Improvement Opportunities:
1. **Multi-modal Processing**: Support video streams or multiple images
2. **Advanced Computer Vision**: Object detection, scene understanding
3. **Dynamic Resolution**: Intelligent resolution selection based on content
4. **API Fallback**: Multiple vision services with automatic failover
5. **Image History**: Visual memory system with image embeddings
6. **Real-time Processing**: Continuous vision during conversations

This document provides a complete foundation for understanding and replacing the Z-WAIF vision integration system.
