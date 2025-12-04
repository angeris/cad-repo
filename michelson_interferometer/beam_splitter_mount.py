# %%
import copy
from build123d import *
from ocp_vscode import *

from kinematic_mirror_mount.kinematic_mirror import mount_height, mirror_side_length, mirror_margin

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)

# %%
beam_splitter_side_length = 10*MM
beam_splitter_mount_thickness = 2.0*MM
beam_splitter_mount_height = mount_height - mirror_side_length - mirror_margin

with BuildPart() as beam_splitter_mount:
    Box(
        beam_splitter_side_length + beam_splitter_mount_thickness*2,
        beam_splitter_side_length + beam_splitter_mount_thickness*2,
        beam_splitter_mount_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN)
    )

    beam_splitter_mount_top_face = beam_splitter_mount.faces().sort_by(Axis.Z).last

    with BuildSketch(beam_splitter_mount_top_face):
        Rectangle(
            beam_splitter_side_length,
            beam_splitter_side_length,
            align=(Align.CENTER, Align.CENTER)
        )
    extrude(amount=-beam_splitter_mount_thickness, mode=Mode.SUBTRACT)

    RigidJoint(
        label="beam_splitter_mount_point",
        joint_location=Location(
            (0, 0, 0),
            (0, 0, 0)
        )
    )

show(beam_splitter_mount, render_joints=True)