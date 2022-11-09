import math
import unittest

import volmdlr
from volmdlr import faces, edges, wires
from volmdlr.models.plane_faces import face as plane_face


class TestCylindricalSurface3D(unittest.TestCase):
    cylindrical_surface = faces.CylindricalSurface3D(volmdlr.OXYZ, 0.32)

    def test_line_intersections(self):
        line3d = edges.Line3D(volmdlr.O3D, volmdlr.Point3D(0.3, 0.3, .3))
        line_inters = self.cylindrical_surface.line_intersections(line3d)
        self.assertEqual(len(line_inters), 2)
        self.assertEqual(line_inters[0], volmdlr.Point3D(0.22627416, 0.22627416, 0.22627416))
        self.assertEqual(line_inters[1], volmdlr.Point3D(-0.22627416, -0.22627416, -0.22627416))

    def test_plane_intersections(self):
        plane_surface = faces.Plane3D(volmdlr.OZXY)
        parallel_plane_secant_cylinder = plane_surface.frame_mapping(volmdlr.Frame3D(
            volmdlr.O3D, volmdlr.Point3D(.5, 0, 0), volmdlr.Point3D(0, .5, 0), volmdlr.Point3D(0, 0, .2)), 'new')
        cylinder_tanget_plane = plane_surface.frame_mapping(volmdlr.Frame3D(
            volmdlr.Point3D(0, 0.32/2, 0), volmdlr.Point3D(.5, 0, 0),
            volmdlr.Point3D(0, .5, 0), volmdlr.Point3D(0, 0, .2)), 'new')
        not_intersecting_cylinder_parallel_plane = plane_surface.frame_mapping(volmdlr.Frame3D(
            volmdlr.Point3D(0, 0.32, 0), volmdlr.Point3D(.5, 0, 0),
            volmdlr.Point3D(0, .5, 0), volmdlr.Point3D(0, 0, .2)), 'new')
        cylinder_concurrent_plane = plane_surface.rotation(volmdlr.O3D, volmdlr.X3D, math.pi/4)
        cylinder_perpendicular_plane = plane_surface.rotation(volmdlr.O3D, volmdlr.X3D, math.pi/2)

        cylinder_surface_secant_parallel_plane_intersec = self.cylindrical_surface.plane_intersection(
            parallel_plane_secant_cylinder)
        self.assertEqual(len(cylinder_surface_secant_parallel_plane_intersec), 2)
        self.assertTrue(isinstance(cylinder_surface_secant_parallel_plane_intersec[0], edges.Line3D))
        self.assertTrue(isinstance(cylinder_surface_secant_parallel_plane_intersec[1], edges.Line3D))

        cylinder_surface_tangent_plane = self.cylindrical_surface.plane_intersection(
            cylinder_tanget_plane)
        self.assertEqual(len(cylinder_surface_tangent_plane), 1)
        self.assertTrue(isinstance(cylinder_surface_tangent_plane[0], edges.Line3D))

        cylinder_surface_tangent_plane_not_intersecting = self.cylindrical_surface.plane_intersection(
            not_intersecting_cylinder_parallel_plane)
        self.assertEqual(len(cylinder_surface_tangent_plane_not_intersecting), 0)

        cylinder_surface_concurrent_plane_intersec = self.cylindrical_surface.plane_intersection(
            cylinder_concurrent_plane)
        self.assertTrue(isinstance(cylinder_surface_concurrent_plane_intersec[0], wires.Ellipse3D))

        cylinder_surface_perpendicular_plane_intersec = self.cylindrical_surface.plane_intersection(
            cylinder_perpendicular_plane)
        self.assertTrue(isinstance(cylinder_surface_perpendicular_plane_intersec[0], wires.Circle3D))


if __name__ == '__main__':
    unittest.main()
