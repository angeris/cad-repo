# %%
import copy
from build123d import *
from ocp_vscode import *

from kinematic_mirror_mount.kinematic_mirror import mirror_mount, stage_mount, mirror_mount_depth
from michelson_interferometer.beam_splitter_mount import beam_splitter_mount
from michelson_interferometer.laser_mount import laser_mount, pole_diameter

set_defaults(reset_camera=Camera.KEEP, helper_scale=5)

# %%
board_side_length = 100.0*MM

with BuildPart() as base_board:
    Box(board_side_length, board_side_length, 5.0*MM)

    top_face = base_board.faces().sort_by(Axis.Z).last
    first_mirror_edge = top_face.edges().filter_by(Axis.X).sort_by(Axis.Y).first
    image_out_edge = top_face.edges().filter_by(Axis.X).sort_by(Axis.Y).last

    # Place the kinematic mirror mount at the center of the first mirror edge
    # with depth buffer
    first_mirror_location = first_mirror_edge @ .5 + (0, mirror_mount_depth/2, 0)
    RigidJoint(
        label="first_mirror",
        joint_location=Location(first_mirror_location)
    )

    second_mirror_edge = top_face.edges().filter_by(Axis.Y).sort_by(Axis.X).first
    laser_mount_edge = top_face.edges().filter_by(Axis.Y).sort_by(Axis.X).last

    second_mirror_location = second_mirror_edge @ .5 + (mirror_mount_depth/2, 0, 0)
    RigidJoint(
        label="second_mirror",
        joint_location=Location(second_mirror_location, (0, 0, 270))
    )

    beam_splitter_location = top_face.center()
    RigidJoint(
        label="beam_splitter_mount",
        joint_location=Location(beam_splitter_location)
    )

    laser_mount_location = laser_mount_edge @ .5 + (-pole_diameter/2, 0, 0)
    RigidJoint(
        label="laser_mount",
        joint_location=Location(laser_mount_location, 180)
    )

show(base_board, render_joints=True)

# %%
# Connect the parts
first_stage = copy.copy(stage_mount.part)
second_stage = copy.copy(stage_mount.part)
first_mirror = copy.copy(mirror_mount.part)
second_mirror = copy.copy(mirror_mount.part)

base_board.joints["first_mirror"].connect_to(first_stage.joints["mount_point"])
base_board.joints["second_mirror"].connect_to(second_stage.joints["mount_point"])

first_stage.joints["mirror_mount"].connect_to(first_mirror.joints["stage_mount_point"])
second_stage.joints["mirror_mount"].connect_to(second_mirror.joints["stage_mount_point"])

beam_splitter_mount_part = copy.copy(beam_splitter_mount.part)
base_board.joints["beam_splitter_mount"].connect_to(beam_splitter_mount_part.joints["beam_splitter_mount_point"])

laser_mount_part = copy.copy(laser_mount.part)
base_board.joints["laser_mount"].connect_to(laser_mount_part.joints["laser_mount_point"])

show([base_board, first_stage, second_stage, first_mirror, second_mirror, beam_splitter_mount_part, laser_mount_part])

complete_assembly = Compound(
    label="michelson_interferometer_assembly",
    children=[
        base_board.part,
        first_stage,
        second_stage,
        first_mirror,
        second_mirror,
        beam_splitter_mount_part,
        laser_mount_part,
    ]
)

# %%

show(complete_assembly, axes=False, grid=False, transparent=False)
save_screenshot("michelson_interferometer/complete_assembly.png")
# %%
