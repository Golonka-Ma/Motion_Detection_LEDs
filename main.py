import cv2
import serial
import time
import numpy as np

WIN_NAME = "Inteligentne oświetlenie"

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def main():
    cap = cv2.VideoCapture('video.mp4')
    #cap = cv2.VideoCapture(0)
    window_open = True
    print(WIN_NAME)

    ser = serial.Serial('COM3', 115200, timeout=1)

    LED_COUNT = 12
    LED_MIN_X = 1
    LED_MAX_X = 830

    people_positions = {}
    STANDING_TIME_THRESHOLD_BLUE = 10.0
    STANDING_TIME_THRESHOLD_GREEN = 20.0

    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getUnconnectedOutLayersNames()

    frame_counter = 0
    DETECTION_FRAME_INTERVAL = 11

    last_send_time = time.time()
    SEND_INTERVAL = 1

    while window_open:
        success, frame = cap.read()
        boxes = []

        frame_counter += 1
        if frame_counter >= DETECTION_FRAME_INTERVAL:
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(layer_names)

            class_ids = []
            confidences = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5 and class_id == 0:
                        center_x = int(detection[0] * frame.shape[1])
                        center_y = int(detection[1] * frame.shape[0])
                        w = int(detection[2] * frame.shape[1])
                        h = int(detection[3] * frame.shape[0])

                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        class_ids.append(class_id)
                        confidences.append(float(confidence))
                        boxes.append([x, y, w, h])

            frame_counter = 0

        led_data = []
        current_time = time.time()
        some_threshold = 65

        for i, box in enumerate(boxes):
            x, y, w, h = box
            cv2.rectangle(frame, (x, 0), (x + w, frame.shape[0]), (0, 255, 0), 3)
            hand_x = x + w // 2
            led_index = int(map_value(hand_x, LED_MIN_X, LED_MAX_X, 0, LED_COUNT))
            led_index = max(0, min(led_index, LED_COUNT - 1))

            if led_index not in people_positions:
                people_positions[led_index] = {'start_time': current_time, 'last_position': hand_x, 'color': 'W'}
            else:
                if abs(people_positions[led_index]['last_position'] - hand_x) > some_threshold:  # jeśli wystąpił ruch
                    people_positions[led_index]['start_time'] = current_time
                    people_positions[led_index]['color'] = 'W'
                else:
                    standing_time = current_time - people_positions[led_index]['start_time']
                    if standing_time > STANDING_TIME_THRESHOLD_GREEN:
                        people_positions[led_index]['color'] = 'W'
                    elif standing_time > STANDING_TIME_THRESHOLD_BLUE:
                        people_positions[led_index]['color'] = 'W'

                people_positions[led_index]['last_position'] = hand_x  # aktualizacja ostatniej pozycji

            led_data.append(f"{led_index}{people_positions[led_index]['color']}")

        if current_time - last_send_time > SEND_INTERVAL and led_data:
            data_to_send = ','.join(led_data).encode()
            ser.write(data_to_send)
            last_send_time = current_time
            print("\nSent data to ESP32:", data_to_send)

        cv2.imshow(WIN_NAME, frame)
        if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty(WIN_NAME, cv2.WND_PROP_VISIBLE) < 1:
            window_open = False

    cap.release()
    ser.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
