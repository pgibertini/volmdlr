# cython: language_level=3
# distutils: language = c++
"""
Pure python module to define cython function.
This module needs to be compiled!
"""
from typing import List, Set, Tuple

import cython
import cython.cimports.libc.math as math_c
import numpy as np
from cython.cimports.libcpp.stack import stack
from cython.cimports.libcpp.vector import vector
from cython.cimports.libcpp.unordered_set import unordered_set

# CUSTOM PYTHON TYPES

Point = Tuple[float, ...]
Triangle = Tuple[Point, ...]


@cython.cfunc
@cython.cdivision(True)
def round_to_digits(num: cython.double, digits: cython.int) -> cython.double:
    multiplier: cython.double = math_c.pow(10.0, digits)
    return math_c.round(num * multiplier) / multiplier


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
def triangle_intersects_voxel(
    triangle: cython.double[3][3],
    voxel_center: cython.double[3],
    voxel_extents: cython.double[3],
) -> cython.bint:
    # Ported from https://gist.github.com/zvonicek/fe73ba9903f49d57314cf7e8e0f05dcf

    v0: cython.double[3]
    v1: cython.double[3]
    v2: cython.double[3]
    f0: cython.double[3]
    f1: cython.double[3]
    f2: cython.double[3]
    box_center: cython.double[3]
    box_extents: cython.double[3]
    plane_normal: cython.double[3]
    plane_distance: cython.double
    r: cython.double
    a00: cython.double[3]
    a01: cython.double[3]
    a02: cython.double[3]
    a10: cython.double[3]
    a11: cython.double[3]
    a12: cython.double[3]
    a20: cython.double[3]
    a21: cython.double[3]
    a22: cython.double[3]
    p0: cython.double
    p1: cython.double
    p2: cython.double

    # Translate triangle as conceptually moving AABB to origin
    v0[0] = triangle[0][0] - voxel_center[0]
    v0[1] = triangle[0][1] - voxel_center[1]
    v0[2] = triangle[0][2] - voxel_center[2]

    v1[0] = triangle[1][0] - voxel_center[0]
    v1[1] = triangle[1][1] - voxel_center[1]
    v1[2] = triangle[1][2] - voxel_center[2]

    v2[0] = triangle[2][0] - voxel_center[0]
    v2[1] = triangle[2][1] - voxel_center[1]
    v2[2] = triangle[2][2] - voxel_center[2]

    # Compute edge vectors for triangle
    f0[0] = triangle[1][0] - triangle[0][0]
    f0[1] = triangle[1][1] - triangle[0][1]
    f0[2] = triangle[1][2] - triangle[0][2]

    f1[0] = triangle[2][0] - triangle[1][0]
    f1[1] = triangle[2][1] - triangle[1][1]
    f1[2] = triangle[2][2] - triangle[1][2]

    f2[0] = triangle[0][0] - triangle[2][0]
    f2[1] = triangle[0][1] - triangle[2][1]
    f2[2] = triangle[0][2] - triangle[2][2]

    # REGION TEST THE THREE AXES CORRESPONDING TO THE FACE NORMALS OF AABB B (CATEGORY 1)

    # Exit if...
    # ... [-extents.X, extents.X] and [min(v0.X,v1.X,v2.X), max(v0.X,v1.X,v2.X)] do not overlap
    if max(v0[0], v1[0], v2[0]) < -voxel_extents[0] or min(v0[0], v1[0], v2[0]) > voxel_extents[0]:
        return False

    # ... [-extents.Y, extents.Y] and [min(v0.Y,v1.Y,v2.Y), max(v0.Y,v1.Y,v2.Y)] do not overlap
    if max(v0[1], v1[1], v2[1]) < -voxel_extents[1] or min(v0[1], v1[1], v2[1]) > voxel_extents[1]:
        return False

    # ... [-extents.Z, extents.Z] and [min(v0.Z,v1.Z,v2.Z), max(v0.Z,v1.Z,v2.Z)] do not overlap
    if max(v0[2], v1[2], v2[2]) < -voxel_extents[2] or min(v0[2], v1[2], v2[2]) > voxel_extents[2]:
        return False

    # ENDREGION

    # REGION TEST SEPARATING AXIS CORRESPONDING TO TRIANGLE FACE NORMAL (CATEGORY 2)

    plane_normal[0] = f0[1] * f1[2] - f0[2] * f1[1]
    plane_normal[1] = f0[2] * f1[0] - f0[0] * f1[2]
    plane_normal[2] = f0[0] * f1[1] - f0[1] * f1[0]

    plane_distance = math_c.fabs(plane_normal[0] * v0[0] + plane_normal[1] * v0[1] + plane_normal[2] * v0[2])

    # Compute the projection interval radius of b onto L(t) = b.c + t * p.n
    r = (
        voxel_extents[0] * math_c.fabs(plane_normal[0])
        + voxel_extents[1] * math_c.fabs(plane_normal[1])
        + voxel_extents[2] * math_c.fabs(plane_normal[2])
    )

    # Intersection occurs when plane distance falls within [-r,+r] interval
    if plane_distance > r:
        return False

    # ENDREGION

    # REGION TEST AXES a00..a22 (CATEGORY 3)

    # Test axis a00
    a00[0] = 0
    a00[1] = -f0[2]
    a00[2] = f0[1]
    if calculate_axis_values(v0, v1, v2, a00, f0, voxel_extents):
        return False

    # Test axis a01
    a01[0] = 0
    a01[1] = -f1[2]
    a01[2] = f1[1]
    if calculate_axis_values(v0, v1, v2, a01, f1, voxel_extents):
        return False

    # Test axis a02
    a02[0] = 0
    a02[1] = -f2[2]
    a02[2] = f2[1]
    if calculate_axis_values(v0, v1, v2, a02, f2, voxel_extents):
        return False

    # Test axis a10
    a10[0] = f0[2]
    a10[1] = 0
    a10[2] = -f0[0]
    if calculate_axis_values(v0, v1, v2, a10, f0, voxel_extents):
        return False

    # Test axis a11
    a11[0] = f1[2]
    a11[1] = 0
    a11[2] = -f1[0]
    if calculate_axis_values(v0, v1, v2, a11, f1, voxel_extents):
        return False

    # Test axis a12
    a12[0] = f2[2]
    a12[1] = 0
    a12[2] = -f2[0]
    if calculate_axis_values(v0, v1, v2, a12, f2, voxel_extents):
        return False

    # Test axis a20
    a20[0] = -f0[1]
    a20[1] = f0[0]
    a20[2] = 0
    if calculate_axis_values(v0, v1, v2, a20, f0, voxel_extents):
        return False

    # Test axis a21
    a21[0] = -f1[1]
    a21[1] = f1[0]
    a21[2] = 0
    if calculate_axis_values(v0, v1, v2, a21, f1, voxel_extents):
        return False

    # Test axis a22
    a22[0] = -f2[1]
    a22[1] = f2[0]
    a22[2] = 0
    if calculate_axis_values(v0, v1, v2, a22, f2, voxel_extents):
        return False

    # ENDREGION

    return True


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.exceptval(check=False)
def calculate_axis_values(
    v0: cython.double[3],
    v1: cython.double[3],
    v2: cython.double[3],
    ax: cython.double[3],
    f: cython.double[3],
    voxel_extents: cython.double[3],
) -> cython.bint:
    p0 = v0[0] * ax[0] + v0[1] * ax[1] + v0[2] * ax[2]
    p1 = v1[0] * ax[0] + v1[1] * ax[1] + v1[2] * ax[2]
    p2 = v2[0] * ax[0] + v2[1] * ax[1] + v2[2] * ax[2]
    r = (
        voxel_extents[0] * math_c.fabs(f[2])
        + voxel_extents[1] * math_c.fabs(f[0])
        + voxel_extents[2] * math_c.fabs(f[1])
    )

    return max(-max(p0, p1, p2), min(p0, p1, p2)) > r


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def aabb_intersecting_boxes(
    min_point: cython.double[3], max_point: cython.double[3], voxel_size: cython.double
) -> vector[Tuple[cython.double, cython.double, cython.double]]:
    x_start: cython.int
    x_end: cython.int
    y_start: cython.int
    y_end: cython.int
    z_start: cython.int
    z_end: cython.int
    x: cython.int
    y: cython.int
    z: cython.int
    num_centers: cython.int

    x_start = cython.cast(cython.int, (min_point[0] / voxel_size) - 1)
    x_end = cython.cast(cython.int, (max_point[0] / voxel_size) + 1)
    y_start = cython.cast(cython.int, (min_point[1] / voxel_size) - 1)
    y_end = cython.cast(cython.int, (max_point[1] / voxel_size) + 1)
    z_start = cython.cast(cython.int, (min_point[2] / voxel_size) - 1)
    z_end = cython.cast(cython.int, (max_point[2] / voxel_size) + 1)

    num_centers = (x_end - x_start) * (y_end - y_start) * (z_end - z_start)
    centers: vector[Tuple[cython.double, cython.double, cython.double]]
    centers.resize(num_centers)

    num_centers = 0
    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            for z in range(z_start, z_end):
                centers[num_centers] = (
                    round_to_digits((x + 0.5) * voxel_size, 6),
                    round_to_digits((y + 0.5) * voxel_size, 6),
                    round_to_digits((z + 0.5) * voxel_size, 6),
                )
                num_centers += 1

    return centers


def triangles_to_voxels(triangles: List[Triangle], voxel_size: float) -> Set[Point]:
    """
    Helper method to compute all the voxels intersecting with a given list of triangles.

    :param triangles: The triangles to compute the intersecting voxels.
    :type triangles: list[tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]]
    :param voxel_size: The voxel edges size.
    :type voxel_size: float

    :return: The centers of the voxels that intersect with the triangles.
    :rtype: set[tuple[float, float, float]]
    """
    voxel_centers = set()

    for triangle in triangles:
        min_point = tuple(min(p[i] for p in triangle) for i in range(3))
        max_point = tuple(max(p[i] for p in triangle) for i in range(3))

        for bbox_center in aabb_intersecting_boxes(
            [min_point[0], min_point[1], min_point[2]],
            [max_point[0], max_point[1], max_point[2]],
            voxel_size,
        ):
            bbox_center = tuple(bbox_center)
            if bbox_center not in voxel_centers:
                if triangle_intersects_voxel(
                    [
                        [triangle[0][0], triangle[0][1], triangle[0][2]],
                        [triangle[1][0], triangle[1][1], triangle[1][2]],
                        [triangle[2][0], triangle[2][1], triangle[2][2]],
                    ],
                    [bbox_center[0], bbox_center[1], bbox_center[2]],
                    [0.5 * voxel_size, 0.5 * voxel_size, 0.5 * voxel_size],
                ):
                    voxel_centers.add(bbox_center)

    return voxel_centers


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
def flood_fill_matrix_c(
    matrix: cython.int[:, :, :], start: cython.int[3], fill_with: cython.int, shape: cython.int[3]
) -> cython.int[:, :, :]:
    dx: cython.int[6] = [0, 0, -1, 1, 0, 0]
    dy: cython.int[6] = [-1, 1, 0, 0, 0, 0]
    dz: cython.int[6] = [0, 0, 0, 0, -1, 1]
    nx: cython.int
    ny: cython.int
    nz: cython.int
    x: cython.int
    y: cython.int
    z: cython.int
    sx: cython.int = shape[0]
    sy: cython.int = shape[1]
    sz: cython.int = shape[2]

    old_value: cython.int = matrix[start[0], start[1], start[2]]

    if old_value == fill_with:
        return matrix

    fill_stack: stack[Tuple[cython.int, cython.int, cython.int]]
    fill_stack.push((start[0], start[1], start[2]))

    while not fill_stack.empty():
        x, y, z = fill_stack.top()
        fill_stack.pop()
        matrix[x, y, z] = fill_with

        for i in range(6):
            nx, ny, nz = x + dx[i], y + dy[i], z + dz[i]

            if 0 <= nx < sx and 0 <= ny < sy and 0 <= nz < sz and matrix[nx, ny, nz] == old_value:
                fill_stack.push((nx, ny, nz))

    return matrix


def flood_fill_matrix(
    matrix: np.ndarray[np.bool_, np.ndim == 3], start: Tuple[int, int, int], fill_with: bool
) -> np.ndarray[np.bool_, np.ndim == 3]:
    # TODO: add docstrings
    return np.asarray(
        flood_fill_matrix_c(
            matrix.astype(np.int32),
            [start[0], start[1], start[2]],
            fill_with,
            [matrix.shape[0], matrix.shape[1], matrix.shape[2]],
        ),
        dtype=np.bool_,
    )


@cython.cfunc
@cython.cdivision(True)
@cython.boundscheck(False)
@cython.wraparound(False)
def line_segment_intersects_pixel_c(
    x1: cython.double,
    y1: cython.double,
    x2: cython.double,
    y2: cython.double,
    pixel_center: cython.double[2],
    pixel_size: cython.double,
) -> cython.bint:
    pixel_center_x = pixel_center[0]
    pixel_center_y = pixel_center[1]

    # Determine the coordinates of lower-left and upper-right of rectangle
    xmin, xmax = pixel_center_x - pixel_size / 2, pixel_center_x + pixel_size / 2
    ymin, ymax = pixel_center_y - pixel_size / 2, pixel_center_y + pixel_size / 2

    # Compute the line equation for a point

    line_eq1 = (y2 - y1) * xmin + (x1 - x2) * ymin + (x2 * y1 - x1 * y2)
    line_eq2 = (y2 - y1) * xmin + (x1 - x2) * ymax + (x2 * y1 - x1 * y2)
    line_eq3 = (y2 - y1) * xmax + (x1 - x2) * ymin + (x2 * y1 - x1 * y2)
    line_eq4 = (y2 - y1) * xmax + (x1 - x2) * ymax + (x2 * y1 - x1 * y2)

    # Check if all corners are on the same side of the line
    miss: cython.bint = (line_eq1 <= 0 and line_eq2 <= 0 and line_eq3 <= 0 and line_eq4 <= 0) or (
        line_eq1 >= 0 and line_eq2 >= 0 and line_eq3 >= 0 and line_eq4 >= 0
    )

    # Does it miss based on the shadow intersection test?
    shadow_miss: cython.bint = (
        (x1 > xmax and x2 > xmax) or (x1 < xmin and x2 < xmin) or (y1 > ymax and y2 > ymax) or (y1 < ymin and y2 < ymin)
    )

    # A hit is if it doesn't miss on both tests!
    return not (miss or shadow_miss)


# def line_segment_intersects_pixel(line_segment, pixel_center, pixel_size):
#     """
#     Check if a line segment intersects with a box.
#
#     :param tuple line_segment: The coordinates of the line segment in the format ((x1, y1), (x2, y2)).
#     :param tuple pixel_center: The coordinates of the pixel's center (box_center_x, box_center_y).
#     :param float pixel_size: The size of the pixel (considering it as a square).
#
#     :return: A boolean indicating whether the line intersects with the pixel.
#     :rtype: bool
#     """
#     return line_segment_intersects_pixel_c(
#         [line_segment[0][0], line_segment[0][1]],
#         [line_segment[1][0], line_segment[1][1]],
#         [pixel_center[0], pixel_center[1]],
#         pixel_size,
#     )


@cython.cfunc
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def line_segments_to_pixels_c(
    line_segments: vector[vector[cython.double[2]]], pixel_size: cython.double
) -> unordered_set[Tuple[cython.double, cython.double]]:
    pixel_centers: unordered_set[Tuple[cython.double, cython.double]]

    for i in range(line_segments.size()):
        line_segment = line_segments[i]
        start: Tuple[cython.double, cython.double] = (line_segment[0][0], line_segment[0][1])
        end: Tuple[cython.double, cython.double] = (line_segment[1][0], line_segment[1][1])

        x1 = start[0]
        y1 = start[1]
        x2 = end[0]
        y2 = end[1]

        # Calculate the bounding box of the line segment
        xmin = min(x1, x2)
        ymin = min(y1, y2)
        xmax = max(x1, x2)
        ymax = max(y1, y2)

        # Calculate the indices of the box that intersect with the bounding box of the line segment
        x_start = cython.cast(cython.int, (xmin / pixel_size) - 1)
        x_end = cython.cast(cython.int, (xmax / pixel_size) + 1)
        y_start = cython.cast(cython.int, (ymin / pixel_size) - 1)
        y_end = cython.cast(cython.int, (ymax / pixel_size) + 1)

        # Create a list of the centers of all the intersecting voxels
        centers: vector[Tuple[cython.double, cython.double]]
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                x_coord: cython.double = (cython.cast(cython.double, x) + 0.5) * pixel_size
                y_coord: cython.double = (cython.cast(cython.double, y) + 0.5) * pixel_size
                center: Tuple[cython.double, cython.double] = (
                    round_to_digits(x_coord, 6),
                    round_to_digits(y_coord, 6),
                )
                centers.push_back(center)

        for j in range(centers.size()):
            if pixel_centers.count(centers[j]) == 0 and line_segment_intersects_pixel_c(
                x1, y1, x2, y2, [centers[j][0], centers[j][1]], pixel_size
            ):
                pixel_centers.insert(centers[j])

    return pixel_centers


# def line_segments_to_pixels(line_segments, pixel_size):
#     pixel_centers = set()
#
#     for line_segment in line_segments:
#         start = line_segment[0]
#         end = line_segment[1]
#
#         x1, y1 = start
#         x2, y2 = end
#
#         # Calculate the bounding box of the line segment
#         xmin = min(x1, x2)
#         ymin = min(y1, y2)
#         xmax = max(x1, x2)
#         ymax = max(y1, y2)
#
#         # Calculate the indices of the box that intersect with the bounding box of the line segment
#         x_indices = range(int(xmin / pixel_size) - 1, int(xmax / pixel_size) + 1)
#         y_indices = range(int(ymin / pixel_size) - 1, int(ymax / pixel_size) + 1)
#
#         # Create a list of the centers of all the intersecting voxels
#         centers = []
#         for x in x_indices:
#             for y in y_indices:
#                 center = tuple(round((_ + 1 / 2) * pixel_size, 6) for _ in [x, y])
#                 centers.append(center)
#
#         for center in centers:
#             if center not in pixel_centers and line_segment_intersects_pixel(line_segment, center, pixel_size):
#                 pixel_centers.add(center)
#
#     return pixel_centers
