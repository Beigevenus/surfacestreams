from collections import namedtuple
from typing import Optional

from HandTracking.Config import Config
from HandTracking.PaintingToolbox import PaintingToolbox
from HandTracking.Point import Point
from HandTracking.Canvas import Canvas
from HandTracking.Hand import Hand
from HandTracking.Camera import Camera
from HandTracking.Settings import run_settings as run_settings, Settings

import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hand = mp.solutions.hands


def main(config: Settings) -> int:
    # TODO: Remove when auto calibration is implemented
    drawing_point: Optional[Point] = None
    drawing_precision: int = 30
    old_point: Optional[Point] = None
    point_on_canvas: Optional[Point] = None

    drawing_toolbox: PaintingToolbox = PaintingToolbox(5, current_color="WHITE")

    hand: Hand = Hand(mp_hand)
    canvas: Canvas = Canvas("Canvas", config.monitor.width, config.monitor.height)
    canvas.create_layer("DRAWING", drawing_toolbox)
    canvas.move_window(config.monitor.x, config.monitor.y)
    if config.is_fullscreen == 1:
        canvas.fullscreen()

    cal_points: list[Point] = Config.load_calibration_points()
    if cal_points:
        camera = Camera(cal_points, camera=config.camera)
    else:
        camera = Camera([Point(1, 0), Point(canvas.width, 0), Point(0, canvas.height),
                         Point(canvas.width - 1, canvas.height)], camera=config.camera)

    camera.update_image_ptm(canvas.width, canvas.height)
    cv2.setMouseCallback(camera.name, lambda event, x, y, flags, param: mouse_click(camera, canvas.width,
                                                                                    canvas.height, event, x,
                                                                                    y))

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

        drawing_point, old_point, point_on_canvas = analyse_frame(camera, hands, hand, canvas, drawing_point,
                                                                  old_point, drawing_precision, point_on_canvas)

        camera.show_frame()

        # TODO: Save the black spots so we can remember the last seen hand position
        counter = update_hand_mask(counter, canvas)

        status = check_key_presses(canvas, camera)

        if status == 1:
            return 0
        elif status == 2:
            return 1

    camera.capture.release()


def analyse_frame(camera, hands, hand, canvas, drawing_point, old_point, drawing_precision,
                  point_on_canvas: Optional[Point]):
    # TODO: Write docstring for function
    camera.frame = cv2.cvtColor(camera.frame, cv2.COLOR_BGR2RGB)

    camera.frame.flags.writeable = False
    hand_position: namedtuple = hands.process(camera.frame)
    camera.frame.flags.writeable = True

    # TODO: figure out the structure of the hand position and landmarks
    if hand_position.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(hand_position.multi_hand_landmarks,
                                              hand_position.multi_handedness):

            # TODO: Remove call when no longer needed. For debugging only
            draw_hand_landmarks(hand_landmarks, camera.frame)

            hand.update(hand_landmarks)

            # The actual check whether the program should be drawing or not
            if camera.calibration_is_done():
                # TODO: Add erasing when working on the wheel
                hand_sign: str = hand.get_hand_sign(camera.frame, hand_landmarks)
                if hand_sign == "Pointer":
                    point_on_canvas = camera.transform_point(hand.get_index_tip(), canvas.width, canvas.height)

                    drawing_point, old_point = draw_on_layer(point_on_canvas, canvas,
                                                             drawing_point, old_point, drawing_precision)

                else:
                    old_point = None
                    drawing_point = None

                if hand_sign == "Close":
                    pass

                if hand_sign == "Open":
                    pass

            # Mask for removing the hand
            mask_points = []
            for point in hand.get_mask_points():
                mask_points.append(camera.transform_point(point, canvas.width, canvas.height))

            canvas.get_layer("TIP").wipe()
            canvas.get_layer("TIP").draw_circle(camera.transform_point(hand.fingers["INDEX_FINGER"].tip,
                                                                       canvas.width, canvas.height))

            canvas.draw_mask_points(mask_points)
            canvas.print_calibration_cross(camera, canvas.width, canvas.height)

    return drawing_point, old_point, point_on_canvas


def update_hand_mask(counter, canvas):
    canvas.show()
    canvas.get_layer("MASK").wipe()

    return counter


def check_key_presses(canvas, camera):
    # TODO: Write docstring for function
    # Exit program when Esc is pressed
    key = cv2.waitKey(1)
    if key == 27:  # ESC
        return 1
    elif key == 48:  # 0
        canvas.toolbox.change_color_rgba([150, 150, 150, 255])
    elif key == 49:  # 1
        canvas.toolbox.change_color_rgba([15, 150, 255, 255])
    elif key == 50:  # 2
        canvas.toolbox.change_color_rgba([22, 140, 37, 255])
    elif key == 51:  # 3
        canvas.toolbox.change_color_rgba([57, 150, 90, 255])
    elif key == 52:  # 4
        canvas.toolbox.change_color_rgba([27, 255, 100, 255])
    elif key == 53:  # 5
        canvas.toolbox.change_color_rgba([3, 7, 87, 255])
    elif key == 54:  # 6
        canvas.toolbox.change_color_rgba([20, 40, 60, 255])
    elif key == 55:  # 7
        canvas.toolbox.change_color_rgba([0, 0, 0, 255])
    elif key == 115:  # S
        camera.capture.release()
        cv2.destroyAllWindows()
        return 2

    return 0


def mouse_click(camera, width, height, event, x, y) -> None:
    """
    Callback function for mouse clicks in the camera window.
    Left-clicking will update the calibration points.

    :param camera: A reference to the camera
    :param width: The width of the canvas
    :param height: The height of the canvas
    :param event: The event object, specifying the type of event
    :param x: The x position of the mouse when the event is triggered
    :param y: The y position of the mouse when the event is triggered
    """
    if event == cv2.EVENT_LBUTTONUP:
        camera.update_calibration_point(Point(x, y), width, height)


def draw_on_layer(point_on_canvas: Point, canvas: Canvas, drawing_point: Point, old_point: Point,
                  drawing_precision: int):
    # TODO: Write docstring for function

    if drawing_point is None:
        drawing_point = point_on_canvas

    if old_point is None:
        old_point = point_on_canvas

    canvas.get_layer("DRAWING").toolbox.change_color('WHITE')
    canvas.get_layer("DRAWING").toolbox.change_line_size(3)

    if drawing_point is not None:
        if drawing_point.distance_to(point_on_canvas) > drawing_precision:
            drawing_point = drawing_point.next_point_to(point_on_canvas, 2)
            canvas.get_layer("DRAWING").draw_line(old_point, drawing_point)
            old_point = drawing_point

    return drawing_point, old_point


def draw_hand_landmarks(hand_landmarks, frame) -> None:
    """
    TEMPORARY FUNCTION. Draws the hand landmarks in the camera window, for ease of debugging.

    :param hand_landmarks: The hand landmarks to draw
    :param frame: The frame to draw the landmarks in
    """
    mp_drawing.draw_landmarks(
        frame,
        hand_landmarks,
        mp_hand.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style())


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
