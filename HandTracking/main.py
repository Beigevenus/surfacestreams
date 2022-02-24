from typing import NamedTuple
from image_wrap import four_point_transform as fpt
from utility import limit
from Point import Point
from Canvas import Canvas
from Hand import Hand
from Camera import Camera
from Settings import runsettings as run_settings

import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands


def main():
    # TODO: Remove when auto calibration is implemented
    counter: int = 0

    # drawing_points = deque(maxlen=5)
    drawing_points: list[Point] = []
    old_point: Point = None
    draw_point_skip: int = 0
    draw_point_skip_guard: int = 0

    hand: Hand = Hand(mp_hand)
    canvas: Canvas = Canvas()
    canvas.fullscreen()
    camera: Camera = Camera()

    with mp_hand.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.1) as hands:
        while camera.capture.isOpened():
            camera.update_frame()
            if camera.frame is None:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            hand_position: NamedTuple = hands.process(camera.frame)

            # TODO: figure out the structure of the hand position and landmarks
            if hand_position.multi_hand_landmarks:
                for hand_landmarks in hand_position.multi_hand_landmarks:
                    # TODO: This is the drawing part don't need it in the final product. Only for Debugging
                    mp_drawing.draw_landmarks(
                        camera.frame,
                        hand_landmarks,
                        mp_hand.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    hand.update(hand_landmarks)

                    # TODO: Needs to only run this once, when the display is set up or something
                    if counter < 100:
                        hand.set_finger_length()
                        counter += 1
                    elif counter == 100:
                        print("Done calibrating")
                        counter += 1

                    # The actual check whether the program should be drawing or not
                    if hand.is_drawing():
                        if len(camera.calibration_points) > 3:
                            draw_point_skip += 1
                            if draw_point_skip > draw_point_skip_guard:
                                ptm, warped_width, warped_height = fpt(camera.frame, camera.calibration_points)

                                camera_point: Point = Point(
                                    (limit((float(hand.get_drawing_point().x) * camera.width), 0, camera.width)),
                                    (limit((float(hand.get_drawing_point().y) * camera.height), 0, camera.height)))

                                # TODO: This is also the reason why the accuracy is bad, if it is not a rectangular
                                #  shaped box. This is where the finger will be registered, so this needs to be more
                                #  accurate. One way to do this is to calculate the linear functions between the four
                                #  points, and then check whether a point is within the box that the lines create.
                                if (limit(camera_point.x, camera.calibration_points[0].x,
                                          camera.calibration_points[3].x) == camera_point.x and
                                        limit(camera_point.y, camera.calibration_points[0].y,
                                              camera.calibration_points[3].y) == camera_point.y):

                                    # Does matrix multiplication on the perspective transform matrix and the original
                                    # position of the finger on the camera
                                    corrected_coordinates = np.matmul(ptm, [
                                        camera_point.x,
                                        camera_point.y, 1])

                                    corrected_point: Point = Point(corrected_coordinates[0], corrected_coordinates[1])

                                    point_on_canvas: Point = corrected_point.get_position_on_canvas(warped_width,
                                                                                             warped_height,
                                                                                             canvas.width,
                                                                                             canvas.height)
                                    drawing_points.append(point_on_canvas)
                                    # drawing_points = cp(drawing_points, 6)

                                    if old_point is None:
                                        old_point = point_on_canvas

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

            canvas.show()
            camera.show_frame()

            # Exit program when Esc is pressed
            if cv2.waitKey(1) == 27:
                break
    camera.capture.release()


if __name__ == "__main__":
    run_settings()
    main()
