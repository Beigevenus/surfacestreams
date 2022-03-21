from typing import NamedTuple, Optional

from HandTracking.Config import Config
from HandTracking.PaintingToolbox import PaintingToolbox
from HandTracking.utility import limit
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
                                                                                    y, flags, param))

    counter: int = 0
    calibration_color_flag: bool = True
    draw_mode: str = 'DRAW'
    switch_draw_mode: bool = True

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

        drawing_point, old_point, \
        point_on_canvas, calibration_color_flag, \
        switch_draw_mode, draw_mode = analyse_frame(camera, hands, hand,
                                                    canvas, drawing_point,
                                                    old_point, point_on_canvas,
                                                    calibration_color_flag,
                                                    switch_draw_mode,
                                                    draw_mode)

        camera.show_frame()

        # TODO: Save the black spots so we can remember the last seen hand position
        counter = update_hand_mask(counter, canvas)

        status = check_key_presses(canvas, camera)

        if status == 1:
            return 0
        elif status == 2:
            return 1

    camera.capture.release()


def analyse_frame(camera, hands, hand, canvas, drawing_point, old_point, point_on_canvas: Optional[Point],
                  calibration_color_flag, switch_mode, draw_mode):
    # TODO: Write docstring for function
    camera.frame = cv2.cvtColor(camera.frame, cv2.COLOR_BGR2RGB)
    camera.frame.flags.writeable = False
    # TODO: make highlighting work again
    hand_position: NamedTuple = hands.process(camera.frame)
    camera.frame.flags.writeable = True

    if camera.calibration_is_done():
        if calibration_color_flag:
            canvas.get_layer('DRAWING').fill(0)
            calibration_color_flag = False

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
                hand_sign: str = hand.get_hand_sign(camera.frame, hand_landmarks)
                if hand_sign == "Pointer":
                    point_on_camera = camera.convert_point_to_res(hand.get_index_tip())
                    point_on_canvas = camera.transform_point(point_on_camera)

                    if draw_mode == 'DRAW':
                        drawing_point, old_point = draw_on_layer(point_on_canvas, canvas,
                                                                 drawing_point, old_point,
                                                                 15)

                    if draw_mode == 'ERASE':
                        drawing_point, old_point = draw_on_layer(point_on_canvas, canvas,
                                                                 drawing_point, old_point,
                                                                 1, 'BLACK',
                                                                 100)

                    switch_mode = True

                elif hand_sign == "Open":
                    old_point = None
                    drawing_point = None
                    switch_mode = True

                elif hand_sign == "Close":
                    if switch_mode:
                        switch_mode = False
                        if draw_mode == 'ERASE':
                            draw_mode = 'DRAW'
                            break
                        if draw_mode == 'DRAW':
                            draw_mode = 'ERASE'
                            break

                # Mask for removing the hand
                mask_points = []
                for point in hand.get_mask_points():
                    p: Point = Point(point.x * camera.width, point.y * camera.height)
                    mask_points.append(camera.transform_point(p))

                # if point_on_canvas is not None:
                #     canvas.toolbox.change_color('GREEN')
                #     hand_mask.draw_point(point_on_canvas)
                canvas.draw_mask_points(mask_points)
                # canvas.print_calibration_cross(camera)

    else:
        canvas.get_layer('DRAWING').fill(255)
        calibration_color_flag = True

    return drawing_point, old_point, point_on_canvas, calibration_color_flag, switch_mode, draw_mode


def update_hand_mask(counter, canvas):
    # if counter >= 5:
    #     canvas.draw_mask_points()
    # elif counter < 5:
    #     counter += 1

    canvas.show()
    canvas.get_layer("MASK").wipe()

    return counter


def check_key_presses(canvas, camera):
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


def mouse_click(camera, width, height, event, x, y, flags, param) -> None:
    # TODO: Write docstring for function
    if event == cv2.EVENT_LBUTTONUP:
        camera.update_calibration_point(Point(x, y), width, height)


def draw_on_layer(point_on_canvas: Point, canvas: Canvas, drawing_point: Point, old_point: Point,
                  drawing_precision: int, draw_color: str = 'WHITE', draw_size: int = 4):
    # TODO: Write docstring for function
    if drawing_point is None:
        drawing_point = point_on_canvas

    if old_point is None:
        old_point = point_on_canvas

    canvas.get_layer("DRAWING").toolbox.change_color(draw_color)
    canvas.get_layer("DRAWING").toolbox.change_line_size(draw_size)

    if drawing_point is not None:
        if drawing_point.distance_to(point_on_canvas) > drawing_precision:
            drawing_point = drawing_point.next_point_to(point_on_canvas)
            canvas.get_layer("DRAWING").draw_line(old_point, drawing_point)
            old_point = drawing_point

    return drawing_point, old_point


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
