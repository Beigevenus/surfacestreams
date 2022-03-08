from cmath import pi
from turtle import shape
from typing import NamedTuple, Optional

from HandTracking.Config import Config
from HandTracking.utility import limit
from HandTracking.Point import Point
from HandTracking.Canvas import Canvas
from HandTracking.Hand import Hand
from HandTracking.Camera import Camera
from HandTracking.Settings import runsettings as run_settings, Settings
from HandTracking.DrawArea import DrawArea

import cv2
import mediapipe as mp
import numpy as np
import copy

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands


def main(config: Settings):
    # TODO: Remove when auto calibration is implemented
    drawing_point = None
    drawing_precision = 30
    old_point: Point = None

    hand: Hand = Hand(mp_hand)
    canvas: Canvas = Canvas(width=config.monitor.width, height=config.monitor.height)
    hand_mask: Canvas = Canvas(width=config.monitor.width, height=config.monitor.height, name='mask')
    hand_mask.move_window(config.monitor.x, config.monitor.y)
    if config.isFullscreen == 1:
        hand_mask.fullscreen()

    # TODO: Make it able to handle vertical lines
    draw_area = DrawArea(
        [Point(0 + 1, 0), Point(canvas.width, 0), Point(0, canvas.height), Point(canvas.width - 1, canvas.height)])

    points = Config.load_calibration_points()
    if points:
        camera = Camera(draw_area, canvas, points, camera=config.camera)
    else:
        camera = Camera(draw_area, canvas, [Point(1, 0), Point(canvas.width, 0), Point(0, canvas.height),
                                            Point(canvas.width - 1, canvas.height)], camera=config.camera)
    counter = 0

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

                    # The actual check whether the program should be drawing or not
                    if hand.is_drawing():
                        if len(camera.calibration_points) > 3:
                            camera_point: Point = Point(
                                (limit((float(hand.get_drawing_point().x) * camera.width), 0, camera.width)),
                                (limit((float(hand.get_drawing_point().y) * camera.height), 0, camera.height)))

                            # TODO: This is also the reason why the accuracy is bad, if it is not a rectangular
                            #  shaped box. This is where the finger will be registered, so this needs to be more
                            #  accurate. One way to do this is to calculate the linear functions between the four
                            #  points, and then check whether a point is within the box that the lines create.
                            if draw_area.is_position_in_calibration_area(camera_point):
                                point_on_canvas = draw_area.get_position_on_canvas(canvas.width, canvas.height,
                                                                                   camera.warped_width,
                                                                                   camera.warped_height, camera_point,
                                                                                   camera.ptm)

                                if drawing_point is None:
                                    drawing_point = point_on_canvas

                                if old_point is None:
                                    old_point = point_on_canvas

                    else:
                        old_point = None
                        drawing_point = None

                    if drawing_point is not None:
                        if drawing_point.distance_to(point_on_canvas) > drawing_precision:
                            drawing_point = drawing_point.offset_to(point_on_canvas, 2)
                            canvas.draw_line(old_point, drawing_point)
                            old_point = drawing_point

                    mask_points = []
                    for point in hand.get_mask_points():
                        p = Point(point.x * camera.width, point.y * camera.height)
                        mask_points.append(draw_area.get_position_on_canvas(0, 0, 0, 0, p, camera.ptm))
                    
                    hand_mask.draw_points(mask_points)

            camera.show_frame()
            
            # TODO: Save the black spots so we can save the spots
            if counter >= 5:
                cannervasser = copy.deepcopy(canvas.image)
                res = cannervasser
                layer2 = hand_mask.image[:, :, 3] > 0
                if res.shape[0] == hand_mask.image.shape[0]:
                    res[layer2] = hand_mask.image[layer2]
                    hand_mask.image = res
            elif counter < 5:
                counter = counter + 1

            
            hand_mask.show()
            hand_mask.image = np.zeros(shape=[hand_mask.height, hand_mask.width, 4], dtype=np.uint8)

            # Exit program when Esc is pressed
            if cv2.waitKey(1) == 27:
                break
    camera.capture.release()


if __name__ == "__main__":
    startup_dict: dict = Config.load_startup_settings()
    settings: Optional[Settings] = None

    if startup_dict:
        settings = Settings.from_dict(startup_dict)
    else:
        settings = run_settings()

    # use line below instead of above line to bypass settings menu..
    # settings = Settings(fullscreen=1,camera=0)
    # also use line below to move canvas to secondary monitor
    # (if secondary monitor is less than 2500 pixels away)
    # settings.monitor.x = 2500
    main(settings)
