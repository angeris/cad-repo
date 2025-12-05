# %%
import copy
from build123d import *
from ocp_vscode import *

from michelson_interferometer.beam_splitter_mount import beam_splitter_mount_height

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)

# %%

laser_diameter = 6.0*MM
laser_depth = 10*MM
laser_mount_thickness = 1.0*MM
laser_notch_diameter = 4*MM
laser_notch_depth = 1*MM

pole_height = beam_splitter_mount_height + laser_notch_diameter/2
pole_diameter = 3*MM

# Height above center at which to create notch
split_height = 1*MM

laser_mount_base = Cylinder(pole_diameter/2, pole_height)
laser_mount_base += Pos(0, 0, pole_height/2) * Rot(0, 90, 0) * (Cylinder(laser_diameter/2 + laser_mount_thickness, laser_depth))

with BuildPart() as laser_mount:
    add(laser_mount_base)

    front_face = laser_mount.faces().sort_by(Axis.X).last

    with BuildSketch(front_face):
        Circle(laser_notch_diameter/2)
    extrude(until=Until.FIRST, mode=Mode.SUBTRACT)

    with BuildSketch(front_face) as sk:
        Circle(laser_diameter/2)
    extrude(amount=-(laser_depth - laser_notch_depth), mode=Mode.SUBTRACT)

    split_plane = Plane((0, 0, pole_height/2 + split_height), (1, 0, 0))
    split(bisect_by=split_plane, mode=Mode.SUBTRACT)
    
    joint_location = laser_mount.faces().filter_by(Plane.XY).sort_by(Axis.Z).first.center()
    RigidJoint(
        label="laser_mount_point",
        joint_location=Location(
            joint_location,
            (0, 0, 0)
        )
    )

show(laser_mount, render_joints=True)
