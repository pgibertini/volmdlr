import os
import volmdlr.cloud as vmc
import volmdlr.wires as vmw

current_path = os.getcwd()
dir_to_clouds = os.path.abspath(current_path + '/cloud2d')

clouds = []
for file_cloud in os.listdir(dir_to_clouds):
    path_cloud = os.path.abspath(dir_to_clouds + '/' + file_cloud)
    clouds.append(vmc.PointCloud2D.load_from_file(path_cloud))
    
polys = []
polys_conv = []
for cloud in clouds[:1] :
    polygon = vmw.ClosedPolygon2D.concave_hull(cloud.points, 0, 0.000005)
    polys.append(polygon)
    polys_conv.append(vmw.ClosedPolygon2D.points_convex_hull(cloud.points))
    
    
# for poly, cloud in zip(polys, clouds):
# for k, cloud in enumerate(clouds[:1]):
#     ax = polys[k].plot(color='r')
#     cloud.plot(ax=ax)
#     polys_conv[k].plot(ax=ax, color='g')
    
    
for poly in polys :
    ax = poly.plot(color='r')
    for pt in poly.points :
        pt.plot(ax=ax)
        
    poly_simplify = poly.simplify()
    poly_simplify.plot(ax=ax, color='g')
    for pt in poly_simplify.points :
        pt.plot(ax=ax, color='b')
        
    print(len(poly.points), len(poly_simplify.points))
