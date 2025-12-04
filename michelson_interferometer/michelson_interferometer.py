# %%
import copy
from build123d import *
from ocp_vscode import *

from kinematic_mirror_mount.kinematic_mirror import mirror_mount, stage_mount

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)

# %%

mirror_mount_depth = 5*MM

board_side_length = 100.0*MM

first_mirror = copy.copy(stage_mount)
second_mirror = copy.copy(stage_mount)

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

base_board.joints["first_mirror"].connect_to(first_mirror.joints["mount_point"])
base_board.joints["second_mirror"].connect_to(second_mirror.joints["mount_point"])

show([base_board, first_mirror, second_mirror], render_joints=True)

# %%
show(base_board, reset_camera=Camera.RESET, axes=False, grid=False, transparent=False)
save_screenshot("michelson_interferometer/complete_assembly.png")
