import random
from shapely.geometry import Point, Polygon
from shapely.prepared import prep
import numpy as np

import matplotlib.pyplot as plt 

# Define polygon
poly = Polygon([(0, 0), (4, 0), (4, 4), (0, 4)])
poly = Polygon([[-125.8424167,49.25715], [-125.8416333,49.25745],[-125.8404833,49.2562],[-125.8413,49.25588333]]);

def create_grid_in_polygon(polygon, step_size):
    """
    Generates a regular grid of points inside a given shapely Polygon.
    
    :param polygon: shapely.geometry.Polygon object
    :param step_size: Distance between grid points (in the polygon's CRS units)
    :return: List of shapely.geometry.Point objects inside the polygon
    """
    # 1. Get the bounding box of the polygon
    xmin, ymin, xmax, ymax = polygon.bounds
    
    # 2. Generate regular ranges for X and Y coordinates
    x_coords = np.arange(xmin, xmax, step_size)
    y_coords = np.arange(ymin, ymax, step_size)
    
    # 3. Create a 2D grid mesh from the ranges
    grid_x, grid_y = np.meshgrid(x_coords, y_coords)
    
    # 4. Flatten the grid into a list of (x, y) coordinate tuples
    potential_points = np.vstack([grid_x.ravel(), grid_y.ravel()]).T
    
    # 5. Optimize point-in-polygon checks using shapely.prepared
    # This significantly speeds up the filtering loop
    prep_polygon = prep(polygon)
    
    # 6. Filter points to keep only those inside the polygon
    inside_points = []
    for x, y in potential_points:
        p = Point(x, y)
        if prep_polygon.contains(p):
            inside_points.append(p)
            
    return inside_points


# Generate random points inside polygon
def random_points_in_polygon(polygon, num_points):
    points = []
    minx, miny, maxx, maxy = polygon.bounds
    while len(points) < num_points:
        p = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if polygon.contains(p):
            points.append(p)
    return points

# points = random_points_in_polygon(poly, 50)
points = create_grid_in_polygon(polygon=poly, step_size=0.0001)
# print("Generated points:", points_inside)

x, y = poly.boundary.xy
plt.plot(x, y)
for p in points:
    plt.scatter(p.x, p.y,c='r')

plt.axis('equal')
plt.savefig('tmp_regular_grid.png')