from image_wrap import four_point_transform as fpt
from utility import correct_points as cp, limit, B_spline
from Point import Point
from collections import deque

import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands

total_finger_length = {
    "INDEX_FINGER": 0,
    "MIDDLE_FINGER": 0,
    "RING_FINGER": 0,
    "PINKY_FINGER": 0
}

finger_stretched = {
    "INDEX_FINGER": False,
    "MIDDLE_FINGER": False,
    "RING_FINGER": False,
    "PINKY_FINGER": False
}

points_for_auto_calibration = [
    [0, 0],
    [1920, 0],
    [0, 1080],
    [1920, 1080]
]

# Array for for calibration points
corner_points = []


def main():
    # TODO: Remove when auto calibration is implemented
    counter = 0

    # TODO: Make resolution dynamic
    width, height = 1920, 1080
    res_height = height
    res_width = width
    camera_height = 480
    camera_width = 640

    line_size = int(10)
    circle_size = line_size / 2
    drawing_color = (255, 255, 255)
    calibration_color = [0, 255, 255]

    # Variables for holding the previous position of index finger tip

    # drawing_points = deque(maxlen=5)
    drawing_points = []
    draw_status = False
    old_point = None
    draw_point_skip = 0
    draw_point_skip_guard = 0

    # For webcam input:image
    # TODO: Needs to be dynamically found
    cap = cv2.VideoCapture(0)
    black_image = np.zeros(shape=[res_height, res_width, 3], dtype=np.uint8)

    # Puts the drawing board in fullscreen
    cv2.namedWindow('Blackboard', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Blackboard', 2500, 0)
    cv2.setWindowProperty('Blackboard', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # for i in points_for_auto_calibration:
    #    cv2.circle(black_image, (int(i[0]), int(i[1])), int(circle_size/2),
    #                            (255, 243, 0), cv2.FILLED)
    # black_image = cv2.rectangle(black_image, i[0], i[1], (255, 243, 0), -1)

    with mp_hand.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.1) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)

            # Drawing corner points
            for i in corner_points:
                cv2.circle(image, (int(i.x), int(i.y)), int(circle_size * 2),
                           [255, 255, 0], cv2.FILLED)

                # image = fpt(image, corner_points)

            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # corners = find_corners_from_color(image, calibration_color)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # TODO: This is the drawing part don't need it in the final product. Only for Debugging
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hand.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    wrist = hand_landmarks.landmark[mp_hand.HandLandmark.WRIST]
                    index_tip = hand_landmarks.landmark[mp_hand.HandLandmark.INDEX_FINGER_TIP]
                    middle_tip = hand_landmarks.landmark[mp_hand.HandLandmark.MIDDLE_FINGER_TIP]
                    ring_tip = hand_landmarks.landmark[mp_hand.HandLandmark.RING_FINGER_TIP]
                    pinky_tip = hand_landmarks.landmark[mp_hand.HandLandmark.PINKY_TIP]

                    # TODO: Needs to only run this once, when the display is set up
                    if counter < 100:
                        if results.multi_hand_landmarks:
                            for hand_landmarks in results.multi_hand_landmarks:
                                total_finger_length["INDEX_FINGER"] = pyt(
                                    hand_landmarks.landmark[mp_hand.HandLandmark.WRIST],
                                    hand_landmarks.landmark[
                                        mp_hand.HandLandmark.INDEX_FINGER_TIP])
                                total_finger_length["MIDDLE_FINGER"] = pyt(
                                    hand_landmarks.landmark[mp_hand.HandLandmark.WRIST],
                                    hand_landmarks.landmark[
                                        mp_hand.HandLandmark.MIDDLE_FINGER_TIP])
                                total_finger_length["RING_FINGER"] = pyt(
                                    hand_landmarks.landmark[mp_hand.HandLandmark.WRIST],
                                    hand_landmarks.landmark[
                                        mp_hand.HandLandmark.RING_FINGER_TIP])
                                total_finger_length["PINKY_FINGER"] = pyt(
                                    hand_landmarks.landmark[mp_hand.HandLandmark.WRIST],
                                    hand_landmarks.landmark[
                                        mp_hand.HandLandmark.PINKY_TIP])
                            counter += 1
                    elif counter == 100:
                        print("Done calibrating")
                        counter += 1

                    # TODO: Make one time lookup instead of making several
                    if (wrist.distance_to(index_tip)) > (0.9 * total_finger_length["INDEX_FINGER"]):
                        finger_stretched["INDEX_FINGER"] = True
                    else:
                        finger_stretched["INDEX_FINGER"] = False

                    if (wrist.distance_to(middle_tip)) > (0.9 * total_finger_length["MIDDLE_FINGER"]):
                        finger_stretched["MIDDLE_FINGER"] = True
                    else:
                        finger_stretched["MIDDLE_FINGER"] = False

                    if (wrist.distance_to(ring_tip)) > (0.9 * total_finger_length["RING_FINGER"]):
                        finger_stretched["RING_FINGER"] = True
                    else:
                        finger_stretched["RING_FINGER"] = False

                    if (wrist.distance_to(pinky_tip)) > (0.9 * total_finger_length["PINKY_FINGER"]):
                        finger_stretched["PINKY_FINGER"] = True
                    else:
                        finger_stretched["PINKY_FINGER"] = False

                    # The actual check whether the program should be drawing or not
                    if (finger_stretched["INDEX_FINGER"] == True and
                            finger_stretched["MIDDLE_FINGER"] == False and
                            finger_stretched["PINKY_FINGER"] == False and
                            finger_stretched["RING_FINGER"] == False):

                        if len(corner_points) > 3:
                            draw_point_skip += 1
                            if draw_point_skip > draw_point_skip_guard:

                                ptm, warped_width, warped_height = fpt(image, corner_points)

                                camera_point = Point((limit((float(index_tip.x) * camera_width), 0, camera_width)),
                                                     (limit((float(index_tip.y) * camera_height), 0, camera_height)))

                                # This is where the finger will be registered, so this needs to be more accurate.
                                # One way to do this is to calculate the linear functions between the four points,
                                # and then check whether a point is within the box that the lines create.
                                # TODO: This is also the reason why the accuracy is bad, if it is not a rectangular shaped box
                                if (limit(camera_point.x, corner_points[0].x, corner_points[3].x) == camera_point.x and
                                        limit(camera_point.y, corner_points[0].y,
                                              corner_points[3].y) == camera_point.y):
                                    # TODO: Refactor all for the love of god

                                    # Does matrix multipication on the perspective transform matrix and the original
                                    # position of the finger on the camera
                                    corrected_coordinates = np.matmul(ptm, [
                                        camera_point.x,
                                        camera_point.y, 1])

                                    corrected_point = Point(corrected_coordinates[0], corrected_coordinates[1])

                                    # TODO: Make debugging using the prints below
                                    # print(x, y)
                                    # print(posx, posy)
                                    # print(corrected_coordinates[0], corrected_coordinates[1])
                                    # print(corrected_coordinates[0] / warped_width, corrected_coordinates[1] / warped_height)

                                    point_on_canvas = corrected_point.get_position_on_canvas(warped_width,
                                                                                                 warped_height, 
                                                                                                 res_width, res_height)
                                    drawing_points.append(point_on_canvas)
                                    # drawing_points = cp(drawing_points, 6)

                                    if old_point is None:
                                        old_point = point_on_canvas

                                    # TODO: Make debugging using the prints below
                                    # print(x, y)
                                    print("drawing")

                                    # point = drawing_points.popleft()
                                    cv2.circle(black_image, (int(point_on_canvas.x), int(point_on_canvas.y)),
                                               int(circle_size), calibration_color, cv2.FILLED)

                                    # Draws line between old index finger tip position, and actual position
                                    cv2.line(black_image, (int(old_point.x), int(old_point.y)),
                                             (int(point_on_canvas.x), int(point_on_canvas.y)),
                                             calibration_color, line_size)

                                    old_point = point_on_canvas

                                    draw_point_skip = 0

                    elif drawing_points:
                        """ drawing_points = B_spline(drawing_points) 
                            old_point = drawing_points[0]
                            for point in drawing_points:
                                cv2.circle(black_image, (int(point.x), int(point.y)), int(circle_size),
                                drawing_color, cv2.FILLED)
                                cv2.line(black_image, (int(old_point.x), int(old_point.y)), (int(point.x), int(point.y)), 
                                drawing_color, line_size)
                                old_point = point """

                        drawing_points.clear()

                        old_point = None

            # TODO: Add auto calibration for the "cropped" image, that is supposed to be the actual drawing point
            cv2.namedWindow('Camera')
            cv2.setMouseCallback('Camera', mouse_click)
            cv2.imshow('Camera', image)

            # Showing the actual blackboard.
            # Moving the blackboard to the second screen (if it is to the left of the main one)
            # and sets it to full screen, but with white boarders >:(
            cv2.imshow('Blackboard', cv2.flip(black_image, 1))

            # Update the screen resolution to fit the computer screen
            img_size = cv2.getWindowImageRect('Blackboard')

            if img_size[3] != res_height or img_size[2] != res_width:
                res_height = img_size[3]
                res_width = img_size[2]
                black_image = cv2.resize(black_image, (res_width, res_height), interpolation=cv2.INTER_AREA)

            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()


# Callback function for the manual calibration
def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        if len(corner_points) > 3:
            corner_points.clear()
        else:
            corner_points.append(Point(x, y))


if __name__ == "__main__":
    main()
