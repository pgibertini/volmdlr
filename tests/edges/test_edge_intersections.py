import unittest
from itertools import product

import volmdlr
from volmdlr.models.edges import bspline1, lineseg, arc, arc_ellipse2d


class TestEdge2DIntersections(unittest.TestCase):

    def test_edge_intersections(self):
        expected_results = [[volmdlr.Point2D(0.2154767869546837, 0.17126976173937553),
                             volmdlr.Point2D(1.5, 0.0),
                             volmdlr.Point2D(2.7845232130453157, -0.17126976173937541)],
                            [volmdlr.Point2D(0.1393336862079807, 0.12052092182042828),
                             volmdlr.Point2D(1.7686123664970617, -0.12999927610326556)],
                            [volmdlr.Point2D(1.3169499683004458, 0.09016185257330922)],
                            [volmdlr.Point2D(0.2154767869546837, 0.17126976173937553),
                             volmdlr.Point2D(1.5, 0.0),
                             volmdlr.Point2D(2.7845232130453157, -0.17126976173937541)],
                            [volmdlr.Point2D(1.8893801268948387, -0.05191735025264532),
                             volmdlr.Point2D(0.07997689764965754, 0.18933641364671217)],
                            [volmdlr.Point2D(1.2821273688601553, 0.029049684151979283)],
                            [volmdlr.Point2D(0.1393336862079807, 0.12052092182042828),
                             volmdlr.Point2D(1.7686123664970617, -0.12999927610326556)],
                            [volmdlr.Point2D(1.8893801268948387, -0.05191735025264532),
                             volmdlr.Point2D(0.07997689764965754, 0.18933641364671217)],
                            [volmdlr.Point2D(1.0591670432729172, -0.3036620132923239)],
                            [volmdlr.Point2D(1.3169499683004458, 0.09016185257330922)],
                            [volmdlr.Point2D(1.2821273688601553, 0.029049684151979283)],
                            [volmdlr.Point2D(1.0591670432729172, -0.3036620132923239)]]

        intersection_results = []
        for edge1, edge2 in product([bspline1, lineseg, arc, arc_ellipse2d], repeat=2):
            if edge1 == edge2:
                continue
            intersections = edge1.intersections(edge2)
            intersection_results.append(intersections)
        for intersections, expected_intersections in zip(intersection_results, expected_results):
            for intersection, expected_intersection in zip(intersections, expected_intersections):
                self.assertTrue(intersection.is_close(expected_intersection))


if __name__ == '__main__':
    unittest.main()
