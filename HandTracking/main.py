from image_wrap import four_point_transform as fpt
from utility import correct_points as cp, limit, B_spline
from Point import Point
from Canvas import Canvas
from Hand import Hand

import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands

# Array for for calibration points
corner_points = []


def main():
    # TODO: Remove when auto calibration is implemented
    counter = 0

    # TODO: Make resolution dynamic
    camera_height = 480
    camera_width = 640

    # drawing_points = deque(maxlen=5)
    drawing_points = []
    draw_status = False
    old_point = None
    draw_point_skip = 0
    draw_point_skip_guard = 0

    hand = Hand(mp_hand)

    # For webcam input:image
    # TODO: Needs to be dynamically found
    cap = cv2.VideoCapture(0)
    canvas = Canvas()

    # Puts the drawing board in fullscreen
    cv2.namedWindow('Blackboard', cv2.WINDOW_NORMAL)
    cv2.moveWindow('Blackboard', 2500, 0)
    cv2.setWindowProperty('Blackboard', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

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
                cv2.circle(image, (int(i.x), int(i.y)), int(int(10/2) * 2),
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

                    hand.update(hand_landmarks)
                    hand.update(hand_landmarks)

                    # TODO: Needs to only run this once, when the display is set up
                    if counter < 100:
                        hand.set_finger_length()
                        counter += 1
                    elif counter == 100:
                        print("Done calibrating")
                        counter += 1

                    # The actual check whether the program should be drawing or not
                    if hand.is_drawing():
                        if len(corner_points) > 3:
                            draw_point_skip += 1
                            if draw_point_skip > draw_point_skip_guard:

                                ptm, warped_width, warped_height = fpt(image, corner_points)

                                camera_point = Point(
                                    (limit((float(hand.get_drawing_point().x) * camera_width), 0, camera_width)),
                                    (limit((float(hand.get_drawing_point().y) * camera_height), 0, camera_height)))

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
                                                                                             canvas.width, canvas.height)
                                    drawing_points.append(point_on_canvas)
                                    # drawing_points = cp(drawing_points, 6)

                                    if old_point is None:
                                        old_point = point_on_canvas

                                    # TODO: Make debugging using the prints below
                                    # print(x, y)
                                    print("drawing")

                                    # point = drawing_points.popleft()
                                    canvas.draw(old_point, point_on_canvas)

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
            cv2.imshow('Blackboard', cv2.flip(canvas.image, 1))

            img_size = cv2.getWindowImageRect('Blackboard')
            if img_size[3] != canvas.height or img_size[2] != canvas.width:
                canvas.resize(img_size[2], img_size[3])

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
