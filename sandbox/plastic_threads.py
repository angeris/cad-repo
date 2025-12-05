# %%
import copy
from build123d import *
from ocp_vscode import *

from bd_warehouse.thread import PlasticBottleThread

set_defaults(reset_camera=Camera.KEEP, helper_scale=5)

# %%
thread_size = "M38SP444"

external_threads = PlasticBottleThread(thread_size, external=True)
neck_radius = external_threads.root_radius

external_cylinder = Cylinder(neck_radius+0.001*MM, external_threads.length + 2*MM, align=(Align.CENTER, Align.CENTER, Align.MIN))
male_thread = Rot(0, 0, 180) * Rot(180, 0, 0) * (external_cylinder + external_threads)

internal_threads = PlasticBottleThread(thread_size, external=False)

neck_radius = internal_threads.root_radius
outer_wall = 1*MM

with BuildPart() as female_thread:
    Cylinder(neck_radius + outer_wall, internal_threads.length + outer_wall, align=(Align.CENTER, Align.CENTER, Align.MIN))

    with BuildSketch(female_thread.faces().sort_by(Axis.Z).first) as cap_profile:
        Circle(neck_radius-.001*MM)
    extrude(amount=-internal_threads.length, mode=Mode.SUBTRACT)

    add(internal_threads)

show(female_thread.part, Pos(0, 0, -10)* male_thread)

export_step(female_thread.part, "sandbox/female_threads.step")
export_step(male_thread, "sandbox/male_threads.step")
