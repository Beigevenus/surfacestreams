import numpy as np
import cv2
from numpy import ndarray

from HandTracking.Point import Point


def order_points(pts: ndarray) -> ndarray:
    # TODO: Write docstring for function
    # initialize a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect: ndarray = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s: ndarray = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff: ndarray = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


# TODO: Refactor this to not abuse variables for multiple types
def four_point_transform(points: list[Point], width: int, height: int):
    # TODO: Write docstring for function
    # put the points into an numpy array
    pts: list[list[float]] = []
    for p in points:
        pts.append([p.x, p.y])
    pts: ndarray = np.array(pts)

    # obtain a consistent order of the points and unpack them
    # individually
    rect: ndarray = order_points(pts)

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst: ndarray = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    m = cv2.getPerspectiveTransform(rect, dst)

    # return the warped image
    return m
