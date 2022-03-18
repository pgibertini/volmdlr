import os
import volmdlr.cloud as vmc
import volmdlr.wires as vmw
import volmdlr.faces as vmf

current_path = os.getcwd()
dir_to_clouds = os.path.abspath(current_path + '/cloud2d')

clouds = []
# for file_cloud in os.listdir(dir_to_clouds):
#     path_cloud = os.path.abspath(dir_to_clouds + '/' + file_cloud)
#     clouds.append(vmc.PointCloud2D.load_from_file(path_cloud))

clouds.append(vmc.PointCloud2D.load_from_file(current_path + '\\cloud_gear0.json')) 
clouds.append(vmc.PointCloud2D.load_from_file(current_path + '\\cloud_gear1.json')) 
clouds.append(vmc.PointCloud2D.load_from_file(current_path + '\\cloud_gear2.json')) 

   
polys = []
polys_conv = []
for cloud in clouds :
    polygon = vmw.ClosedPolygon2D.concave_hull(cloud.points, -0.2, 0.000005)
    polys.append(polygon)
    polys_conv.append(vmw.ClosedPolygon2D.points_convex_hull(cloud.points))
    
    
# =============================================================================
# New Simplify -- test
# =============================================================================

import volmdlr
import math

def simplify_test(polygon, min_distance = 1e-3, angle_precision = 5):
    new_polygon_points = []
    pos1, pos2, pos3 = 0, 1, 2
    
    rad_precision = math.radians(angle_precision)
    
    while pos1 < len(polygon.points) :
        
        p1, p2, p3 = polygon.points[pos1], polygon.points[pos2], polygon.points[pos3]
        check_distance = True
        if pos1 != 0 :
            if p1.point_distance(new_polygon_points[-1]) < min_distance:
                check_distance = False
                
        if check_distance :
            v1, v2 = p2 - p1, p3 - p2
            cos = v1.dot(v2) / (v1.norm() * v2.norm())
            angle_v1_v2 = math.acos(round(cos, 6))
            # if abs(angle_v1_v2) <= angle_precision :
                
            # if p3 == polygon.points[0] :
            #     ax = polygon.plot(color='r')
            #     for pt in polygon.points :
            #         pt.plot(ax=ax)
                    
            #     p1.plot(ax=ax, color='b')
            #     p2.plot(ax=ax, color='g')
            #     p3.plot(ax=ax, color='c')
                    
                
                
            if math.isclose(angle_v1_v2, 0, abs_tol=rad_precision) or \
                math.isclose(angle_v1_v2, math.pi, abs_tol=rad_precision) or \
                math.isclose(angle_v1_v2, 2*math.pi, abs_tol=rad_precision):
                pos2 = pos3
                pos3 += 1
                
            else :
                new_polygon_points.append(p1)
                if pos1 > pos2 :
                    break
                
                pos1, pos2 = pos2, pos3
                pos3 += 1
                
        else :
            pos1 += 1
            pos2, pos3 = pos1+1, pos1+2
            
        if pos2 > len(polygon.points) -1 :
            pos2 -= len(polygon.points)

        if pos3 > len(polygon.points) -1  :
            pos3 -= len(polygon.points)

    # ax = polygon.plot(color='r')
    
    # for pt in polygon.points :
    #     pt.plot(ax=ax)
    
    # for pt in new_polygon_points:
    #     pt.plot(ax=ax, color='m')
        
    print('v2',len(new_polygon_points))
    
    return new_polygon_points

polys_simplified =[]
for poly in polys :
    print()
    ax = poly.plot(color='r')
    for pt in poly.points :
        pt.plot(ax=ax)
        
        
    new_polygon_points2 = simplify_test(poly, angle_precision = 20)
    for pt in new_polygon_points2 :
        pt.plot(ax=ax, color = 'b')
        
    new_poly2 = vmw.ClosedPolygon2D(new_polygon_points2)
    new_poly2.plot(ax=ax, color = 'b')
    
    polys_simplified.append(new_poly2)