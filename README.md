# Intelligent Lighting System

A motion-tracking LED control system that reacts to movement captured by a camera.

## Project Overview

This system uses computer vision to detect human movement through a camera connected via USB. When motion is detected, the system lights up individual LEDs on an LED strip based on the position of the detected movement. For example, if a person moves from right to left, the LEDs will illuminate sequentially from right to left.

The system also changes the LED color based on how long a person remains stationary:
- **White**: Initial color when movement is detected
- **Blue**: After standing still for 5 seconds
- **Green**: After standing still for 30 seconds
- **Red**: After standing still for 1 minute

This color progression is designed to represent light intensity.

## Components

### Hardware Requirements
- Computer with USB camera
- ESP32 microcontroller
- WS2812 LED strip (12 LEDs in the current configuration)
- USB cable for connecting ESP32 to computer

### Software Requirements
- Python 3.x
- OpenCV
- PySerial
- NumPy
- Arduino IDE (for ESP32 programming)
- YOLO v3 model files:
  - `yolov3.weights`
  - `yolov3.cfg`
  - `coco.names`

## Installation

1. Clone this repository
   ```bash
   git clone https://github.com/username/intelligent-lighting.git
   cd intelligent-lighting
   ```

2. Install Python dependencies
   ```bash
   pip install opencv-python numpy pyserial
   ```

3. Download YOLO v3 model files
   - Download `yolov3.weights` from the official YOLO website
   - Place `yolov3.cfg` and `coco.names` in the project directory

4. Upload ESP32 code
   - Open the `esp32_code.ino` file in Arduino IDE
   - Install the FastLED library if not already installed
   - Select the correct board and port
   - Upload the code to your ESP32

## Usage

1. Connect the ESP32 to your computer
2. Connect the LED strip to the ESP32 (data pin to GPIO 12)
3. Run the Python script
   ```bash
   python motion_detector.py
   ```
4. The system will start detecting movement and controlling the LEDs accordingly
5. Press `ESC` to exit the application

## Configuration

You can adjust the following parameters in the Python script:
| Parameter | Description | Default |
|-----------|-------------|---------|
| `LED_COUNT` | Number of LEDs in your strip | 12 |
| `LED_MIN_X` and `LED_MAX_X` | Camera frame boundaries for mapping positions | 1, 830 |
| `STANDING_TIME_THRESHOLD_BLUE` | Time in seconds before LED turns blue | 10s |
| `STANDING_TIME_THRESHOLD_GREEN` | Time in seconds before LED turns green | 20s |
| `DETECTION_FRAME_INTERVAL` | How often to run detection (every N frames) | 11 |
| `SEND_INTERVAL` | Minimum time between commands sent to ESP32 | 1s |

To use a live camera feed instead of a video file, uncomment the line:
```python
# cap = cv2.VideoCapture(0)
```
and comment out:
```python
cap = cv2.VideoCapture('video.mp4')
```

## Technical Details

### Python Application
The Python script uses OpenCV and YOLO v3 for human detection. It tracks the position of detected people and maps their horizontal position to the LED strip. The script communicates with the ESP32 over serial connection, sending commands that specify which LEDs to light and in what color.

### ESP32 Controller
The ESP32 receives commands from the Python application and controls the LED strip using the FastLED library. Each command includes the LED index and color code (W for white, B for blue, G for green).

## Troubleshooting

- If the LED strip doesn't respond, check the serial port name in the Python script (`COM3` by default)
- Ensure all dependencies are installed correctly
- Verify that the YOLO model files are in the correct directory

## Contact
For any questions or suggestions, feel free to contact the developer:
- **Email**: marcin.golonka21@gmail.com  
- **GitHub**: [Intelligent Lighting System](https://github.com/Golonka-Ma/Motion_Detection_LEDs)  
- **LinkedIn**: [Marcin Golonka](https://www.linkedin.com/in/marcin-golonka-4510a928b/)  
