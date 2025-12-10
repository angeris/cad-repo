# %%
import copy
from build123d import *
from ocp_vscode import *

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)

# %%
width = 200*MM
height = 200*MM
depth = 100*MM

wall_thickness = 5*MM

box = Box(width, height, depth)

box -= offset(box, -wall_thickness)

show(box, reset_camera=Camera.RESET)