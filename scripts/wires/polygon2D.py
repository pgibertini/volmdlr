#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 17:02:36 2017

"""

import math
import volmdlr as vm
import volmdlr.wires as vmw
import volmdlr.primitives2d as primitives2d
import time


p1 = vm.Point2D(0, 0)
p2 = vm.Point2D(1, 0)
p3 = vm.Point2D(2, 1)
p4 = vm.Point2D(1, 0.5)
p5 = vm.Point2D(-0.5, 1)
polygon1 = vm.wires.ClosedPolygon2D([p1, p2, p3, p4, p5])


r1 = 1.78*0.5
r2 = r1+0.3
theta1 = 12*2*math.pi/360
theta2 = 33*2*math.pi/360
pm1 = vm.Point2D(0, -r1)
pm2 = vm.Point2D(0, -r2)
pc = vm.Point2D(0, 0)
p1 = pm1.rotation(pc, -theta2)
p2 = pm1.rotation(pc, -theta1)
p3 = pm1.rotation(pc, theta1)
p4 = pm1.rotation(pc, theta2)
p8 = pm2.rotation(pc, -theta2)
p7 = pm2.rotation(pc, -theta1)
p6 = pm2.rotation(pc, theta1)
p5 = pm2.rotation(pc, theta2)

polygon2 = vmw.ClosedPolygon2D([p1, p2, p3, p4, p5, p6, p7, p8], name='border')

polygon3 = vmw.ClosedPolygon2D([vm.Point2D(-0.4518626885964, 0.45),
                                vm.Point2D(-0.4518626885964, 0.85),
                                vm.Point2D(-0.9518626885964, 0.85),
                                vm.Point2D(-0.9518626885964, -0.85),
                                vm.Point2D(-0.4518626885964, -0.85),
                                vm.Point2D(-0.4518626885964, -0.45),
                                vm.Point2D(1.5481373114036, -0.15),
                                vm.Point2D(1.5481373114036, 0.15)])

for polygon in [polygon1, polygon2, polygon3]:

    cog = polygon.center_of_mass()
    (xmin, ymin), (xmax, ymax) = polygon.bounding_points()

    # Try inside
    points_inside = []
    points_outside = []

    for i in range(100):

        pt = vm.Point2D.random(xmin, xmax, ymin, ymax)
        if polygon.point_belongs(pt):
            points_inside.append(pt)
        else:
            points_outside.append(pt)

    ax = polygon.plot()
    for point in points_inside:
        point.plot(ax=ax, color='b')
    for point in points_outside:
        point.plot(ax=ax, color='r')

    # Speed test
    t = time.time()
    n = 100000
    for i in range(n):
        pt = vm.Point2D.random(-0.3, 0.7, -0.3, 0.7)
    #    print(p.PointDistance(pt))
        polygon.point_belongs(pt)
    t = time.time() - t
    print('time spent: {}s, {}s/eval'.format(t, t/n))

    ax = polygon.plot()

    projections = []
    for line in polygon.primitives:
        point, _ = line.point_projection(cog)
        if point:
            point.plot(color='b', ax=ax)

    self_intersects, line1, line2 = polygon.self_intersects()
    if self_intersects:
        line1.plot(ax=ax, color='r')
        line2.plot(ax=ax, color='r')
        raise ValueError('Polygon should not interesect itself')

    # cog.plot(ax=ax)
    cog.plot(ax=ax, color='r')

    mesh = polygon.triangulation()
    mesh.plot(ax=ax)
