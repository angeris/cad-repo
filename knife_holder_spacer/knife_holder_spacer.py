# %%
import copy
from build123d import *
from ocp_vscode import *

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)

# %%
spacer_height = 20.0*MM
spacer_width = 20.0*MM
spacer_depth = 20.0*MM

spacer_thickness = 4.0*MM

extrusion_height = (spacer_height - spacer_thickness)/2

with BuildPart() as knife_holder_spacer:
    spacer_box = Box(spacer_width, spacer_depth, spacer_height)

    top_face = spacer_box.faces().sort_by(Axis.Z).last
    bottom_face = spacer_box.faces().sort_by(Axis.Z).first

    with BuildSketch(top_face) as spacer_cutout:
        cutout_width = spacer_width - 2*spacer_thickness
        cutout_depth = spacer_depth - 2*spacer_thickness
        with Locations((-cutout_width/2, -cutout_depth/2, 0)):
            Rectangle(cutout_width + spacer_thickness, cutout_depth + spacer_thickness, align=(Align.MIN, Align.MIN))

    extrude(amount=-extrusion_height, mode=Mode.SUBTRACT)

    with BuildSketch(bottom_face) as spacer_cutout_bottom:
        add(mirror(spacer_cutout.sketch, about=Plane.XZ))

    extrude(amount=-extrusion_height, mode=Mode.SUBTRACT)

show(knife_holder_spacer)

# %%
show(knife_holder_spacer, reset_camera=Camera.RESET, axes=False, grid=False)
save_screenshot("knife_holder_spacer/knife_holder_spacer.png")

export_step(knife_holder_spacer.part, "knife_holder_spacer/knife_holder_spacer.step")