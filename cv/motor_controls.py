import math
from skittles import *

'''
see https://github.com/nooseman/robot-arm/blob/master/kinematics_derivation/kinematics.pdf

calculate_positions() takes two lists and a tuple:
    - centers is list of all centers detected
    - radii is list of radii corresponding to each center
    - dimensions is tuple of image size like (height, width)

it returns another list, made of tuples that look like (horizontal_dist, radius)
'''
def calculate_position(centers, radii, dimensions):
    # cut down centers, radii in case one is longer than other
    shortest = len(centers) if len(centers) < len(radii) else len(radii)
    centers = centers[:shortest]
    radii = radii[:shortest]

    positions = []
    for i in range(len(centers)):
        dist_from_y_axis = centers[i][0] - dimensions[1] / 2
        positions.append((dist_from_y_axis, 100 / radii[i]))

    return positions

'''
minify() takes one list:
    - positions is a list of all positions detected (as calculated 
    in calculate_positions())

it returns a integer representing how far arm needs to rotate
    - positive integers mean rightward (and vice versa)
    - if 0 is returned, at least one skittle is centered in FOV
'''
def minify(positions):
    if positions == None:
        return False

    minimum = abs(positions[0])
    for position in positions:
        # if position, radius implies skittle on minimum
        if abs(abs(position[0]) - position[1]) < abs(abs(minimum[0]) - minimum[1]):
            minimum = position

            # if current skittle lies on central axis
            if 0 in [minimum[0] - minimum[1], minimum[0] + minimum[1]]:
                return 0

    return minimum

# approximates distance to skittle based on observed radius
def skittle_distance(radius):
    return 1 / radius

# returns a frame from camera
def frame_grab():
    return None

# rotate base of arm by specific number of degrees
def rotate_base(degrees):
    pass

'''
centralize_skittle() takes no parameters, and returns a radial distance 
once a skittle is centered
'''
def centralize_skittle():
    degrees = 360

    while degrees != 0:
        frame = frame_grab()
        centers, radii = draw_contours(np.copy(frame))[1:]

        positions = calculate_positions(centers, radii, frame.shape)
        theta, radius = minify(positions)

        rotate_base(theta)
        # need to wait here until rotation is complete. how can i implement that?


    return skittle_distance(radius)

    
'''
Control Schemes:
-=-=-=-=-=-=-=-=
* determine positions
    - take single initial picture
* pick skittle
    - want skittle closest to middle of FOV
    - use calculate_position()
* repeat until a skittle lies on center line
'''

'''
General Motion Scheme:
-=-=-=-=-=-=-=-=-=-=-=

1. Survey FOV
    - if no skittles found, rotate by FOV degrees
2. Minify until a skittle lies on middle line
3. Move to skittle's radial position but maintain height
4. Scan again, Minify until skittle in middle of fov
5. Drop down, pick up skittle.
6. Place skittle in bowl?
'''