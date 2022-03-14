from typing import NamedTuple, Optional
from numpy import ndarray

from HandTracking.Config import Config
from HandTracking.utility import limit
from HandTracking.Point import Point
from HandTracking.Canvas import Canvas
from HandTracking.Hand import Hand
from HandTracking.Camera import Camera
from HandTracking.Settings import run_settings as run_settings, Settings

import cv2
import mediapipe as mp
import numpy as np
import copy

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands


def main(config: Settings) -> int:
    # TODO: Remove when auto calibration is implemented
    drawing_point: Optional[Point] = None
    drawing_precision: int = 30
    old_point: Optional[Point] = None
    point_on_canvas: Optional[Point] = None
    draw_color: str = 'WHITE'
    draw_size: int = 5

    hand: Hand = Hand(mp_hand)
    canvas: Canvas = Canvas(width=config.monitor.width, height=config.monitor.height)
    hand_mask: Canvas = Canvas(width=config.monitor.width, height=config.monitor.height, name='mask')
    hand_mask.move_window(config.monitor.x, config.monitor.y)
    if config.isFullscreen == 1:
        hand_mask.fullscreen()

    points: list[Point] = Config.load_calibration_points()
    if points:
        camera = Camera(canvas, points, camera=config.camera)
    else:
        camera = Camera(canvas, [Point(1, 0), Point(canvas.width, 0), Point(0, canvas.height),
                                 Point(canvas.width - 1, canvas.height)], camera=config.camera)
    counter: int = 0

    hands = mp_hand.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5)

    while camera.capture.isOpened():
        camera.update_frame()
        if camera.frame is None:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        camera.frame = cv2.cvtColor(camera.frame, cv2.COLOR_BGR2RGB)

        camera.frame.flags.writeable = False
        hand_position: NamedTuple = hands.process(camera.frame)
        camera.frame.flags.writeable = True

        # TODO: figure out the structure of the hand position and landmarks
        if hand_position.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(hand_position.multi_hand_landmarks,
                                                  hand_position.multi_handedness):

                # TODO: This is the drawing part don't need it in the final product. Only for Debugging
                mp_drawing.draw_landmarks(
                    camera.frame,
                    hand_landmarks,
                    mp_hand.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                hand.update(hand_landmarks)

                # The actual check whether the program should be drawing or not
                if len(camera.calibration_points) > 3:
                    if hand.is_erasing():
                        camera_point: Point = Point(
                            (limit((float(hand.get_erasing_point().x) * camera.width), 0, camera.width)),
                            (limit((float(hand.get_erasing_point().y) * camera.height), 0, camera.height)))

                        point_on_canvas = camera.transform_point(camera_point)

                        if drawing_point is None:
                            drawing_point = point_on_canvas

                        if old_point is None:
                            old_point = point_on_canvas

                        draw_color = 'BLACK'
                        draw_size = 50
                        finger_tip_point = Point(hand.get_erasing_point().x * camera.width,
                                                 hand.get_drawing_point().y * camera.height)
                        finger_tip_point_on_camera = camera.transform_point(finger_tip_point)
                        finger_dot = (finger_tip_point_on_camera, "RED")

                    elif hand.is_drawing():
                        print(hand.get_drawing_point())
                        camera_point: Point = Point(
                            (round(limit((float(hand.get_drawing_point().x) * camera.width), 0, camera.width))),
                            (round(limit((float(hand.get_drawing_point().y) * camera.height), 0, camera.height))))

                        point_on_canvas = camera.transform_point(camera_point)

                        # MADS TEST!!!
                        print("top left:")
                        top_left = camera.transform_point(camera.sorted_calibration_points[0])
                        print(int(top_left.x), int(top_left.y))

                        print("top right:")
                        top_right = camera.transform_point(camera.sorted_calibration_points[1])
                        print(int(top_right.x), int(top_right.y))

                        print("bot left:")
                        bot_left = camera.transform_point(camera.sorted_calibration_points[2])
                        print(int(bot_left.x), int(bot_left.y))

                        print("bot right:")
                        bot_right = camera.transform_point(camera.sorted_calibration_points[3])
                        print(int(bot_right.x), int(bot_right.y))

                        canvas.draw_line(top_left, top_right, "RED", 4)
                        canvas.draw_line(top_right, bot_right, "RED", 4)
                        canvas.draw_line(bot_right, bot_left, "RED", 4)
                        canvas.draw_line(bot_left, top_left, "RED", 4)

                        #############################################################

                        if drawing_point is None:
                            drawing_point = point_on_canvas

                        if old_point is None:
                            old_point = point_on_canvas

                        draw_color = 'WHITE'
                        draw_size = 5
                        finger_tip_point = Point(hand.get_drawing_point().x * camera.width,
                                                 hand.get_drawing_point().y * camera.height)
                        finger_tip_point_on_camera = camera.transform_point(finger_tip_point)
                        finger_dot = (finger_tip_point_on_camera, "GREEN")
                    else:
                        finger_dot = None

                else:
                    old_point = None
                    drawing_point = None
                    finger_dot = None

                if drawing_point is not None:
                    if drawing_point.distance_to(point_on_canvas) > drawing_precision:
                        drawing_point = drawing_point.offset_to(point_on_canvas, 2)
                        canvas.draw_line(old_point, drawing_point, draw_color, draw_size)
                        old_point = drawing_point

                # Mask for removing the hand
                mask_points = []
                for point in hand.get_mask_points():
                    p: Point = Point(point.x * camera.width, point.y * camera.height)
                    mask_points.append(camera.transform_point(p))

                hand_mask.draw_mask_points(mask_points, 'BLACK', 5)
                if finger_dot is not None:
                    hand_mask.draw_mask_points([finger_dot[0]], finger_dot[1], 5)

        camera.show_frame()

        # TODO: Save the black spots so we can save the spots
        if counter >= 5:
            canvas_copy: ndarray = copy.deepcopy(canvas.image)
            res = canvas_copy
            layer2 = hand_mask.image[:, :, 3] > 0
            if res.shape[0] == hand_mask.image.shape[0]:
                res[layer2] = hand_mask.image[layer2]
                hand_mask.image = res
        elif counter < 5:
            counter = counter + 1

        hand_mask.show()
        hand_mask.image = np.zeros(shape=[hand_mask.height, hand_mask.width, 4], dtype=np.uint8)

        # Exit program when Esc is pressed
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            return 0
        elif key == 48:  # 0
            canvas.change_color([150, 150, 150, 255])
        elif key == 49:  # 1
            canvas.change_color([15, 150, 255, 255])
        elif key == 50:  # 2
            canvas.change_color([22, 140, 37, 255])
        elif key == 51:  # 3
            canvas.change_color([57, 150, 90, 255])
        elif key == 52:  # 4
            canvas.change_color([27, 255, 100, 255])
        elif key == 53:  # 5
            canvas.change_color([3, 7, 87, 255])
        elif key == 54:  # 6
            canvas.change_color([20, 40, 60, 255])
        elif key == 55:  # 7
            canvas.change_color([0, 0, 0, 255], 50)
        elif key == 115:  # S
            camera.capture.release()
            cv2.destroyAllWindows()
            return 1

    camera.capture.release()


if __name__ == "__main__":
    startup_dict: dict = Config.load_startup_settings()
    settings: Optional[Settings] = None

    if startup_dict:
        settings = Settings.from_dict(startup_dict)
    else:
        settings = run_settings()

    running = main(settings)
    while running:
        settings = run_settings()
        running = main(settings)
