"pointcload utils"
from math import pi, sin ,cos
import random
from pathlib import Path
import open3d as o3d

def down_sample(filename, fileout):
    "downsamle the current file to 1 mm"
    filename = "chess.ply"
    file = filename
    pcl =o3d.io.read_point_cloud(str(file))
    outfile = Path(fileout)
    #pcl2jpg(pcl, outfile)
    print("Number of points: ", len(pcl.points))
    print("Downsample the point cloud with a voxel of 0.05")
    downpcd = pcl.voxel_down_sample(voxel_size=0.5)
    #pcl2jpg(downpcd, Path(folder) / "pic2.jpg")
    #outfile = Path(folder) / "pic2.ply"
    print("Number of downsampled points: ", len(downpcd.points))
    o3d.io.write_point_cloud(str(outfile), downpcd)

def rx_matrix(vx):
    "create the rotation matrix about x"
    v= vx/180*pi
    matrix = [(1,0,0), (0,cos(v),-sin(v)), (0,sin(v),cos(v))]
    return matrix

def ry_matrix(vy):
    "create the rotation matrix y"
    v= vy/180*pi
    matrix = [(cos(v),-sin(v),0), (sin(v), cos(v),0),(0,0,1)]
    return matrix

def rz_matrix(vz):
    "create the rotation matrix z "
    v= vz/180*pi
    matrix = [(cos(v),0,sin(v)), (0,1,0), (-sin(v),0, cos(v))]
    return matrix

def rotate_pcl(pcl, mat):
    "rotate according to matrix"
    respcl = pcl.rotate(mat)
    return respcl

def split_pcl(file, outpath, splitsize=10):
    "split a pcl in a number files for stitching"
    xrange = range(-30,30,splitsize)
    yrange = range(-30,30,splitsize)
    zrange = range(-30,30,splitsize)
    size = int(splitsize * 1.5)
    outpath = Path(outpath)
    pcl = o3d.io.read_point_cloud(str(file))
    print("points", len(pcl.points))
    center = pcl.get_center()
    print ("center", center)
    print("get_axis_aligned_bounding_box", pcl.get_axis_aligned_bounding_box())
    print("get_max_bound", pcl.get_max_bound())

    sumpoint = 0
    number = 0
    for x in xrange:
        for y in yrange:
            for z in zrange:
                minc = (x,y,z)
                maxc = (x+size,y+size,z+size)
                box = o3d.geometry.AxisAlignedBoundingBox(minc,maxc)
                cube = pcl.crop(box)
                nopoints = len(cube.points)
                if nopoints>0:
                    sumpoint += len(cube.points)
                    outfile = outpath / f"file{number}.ply"
                    o3d.io.write_point_cloud(str(outfile), cube)
                    number +=1
                    print("file:", number, "center", cube.get_center(), "points", len(cube.points))
    print("points", len(pcl.points))
    print ("center", center)
    print("get_axis_aligned_bounding_box", pcl.get_axis_aligned_bounding_box())
    print("get_max_bound", pcl.get_max_bound())
    print("Sumpoints", sumpoint)

def random_split(file, outpath, splitsize=10):
    "split a pcl in a number files for stitching and random rotate"
    xrange = range(-30,30,splitsize)
    yrange = range(-30,30,splitsize)
    zrange = range(-30,30,splitsize)
    size = int(splitsize * 1.5)
    outpath = Path(outpath)
    pcl = o3d.io.read_point_cloud(str(file))
    sumpoint = 0
    number = 0

    for x in xrange:
        for y in yrange:
            for z in zrange:
                minc = (x,y,z)
                maxc = (x+size,y+size,z+size)
                box = o3d.geometry.AxisAlignedBoundingBox(minc,maxc)
                cube = pcl.crop(box)
                nopoints = len(cube.points)
                if nopoints>0:
                    sumpoint += len(cube.points)
                    print ("Points in box", len(cube.points ))
                    randomv = random.randint(0,50)
                    resrot  = rotate_pcl(cube, rx_matrix(randomv))
                    outfile = outpath / f"file{number}.ply"
                    o3d.io.write_point_cloud(str(outfile), resrot)
                    number +=1
if __name__ == "__main__":
    infile = Path(__file__).parent / 'stl' / 'LJ3.ply'
    split_pcl(infile, "out", splitsize=20)

    random_split(infile, "out3", splitsize=20)


    # mypcl = o3d.io.read_point_cloud("out2/file0.ply")
    # m = rx_matrix(20)
    # res  = rotate_pcl(mypcl, m)
    # o3d.io.write_point_cloud("out2/file0_20x.ply", res)
    # res  = rotate_pcl(mypcl, ry_matrix(20))
    # o3d.io.write_point_cloud("out2/file0_20y.ply", res)
    # res  = rotate_pcl(mypcl, rz_matrix(20))
    # o3d.io.write_point_cloud("out2/file0_20z.ply", res)
