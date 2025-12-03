# %%
import copy
from build123d import *
from ocp_vscode import *

set_defaults(reset_camera=Camera.CENTER, helper_scale=5)

# %%

mirror_mount_depth = 5*MM
mount_width = 35*MM
mount_height = 35*MM

mirror_side_length = 25.5*MM
mirror_depth = 1.8*MM

mirror_margin = 2.0*MM

spring_hole_width = 4.0*MM
spring_hole_length = 12.0*MM
spring_hole_through_length = 8.0*MM

rod_diameter = 2.0*MM

spring_hole_margin_bottom = 2.0*MM
spring_hole_margin_left = 8.0*MM
spring_hole_margin_right = 8.0*MM

screw_hole_margin_side = 4.0*MM
screw_hole_margin_bottom = spring_hole_margin_bottom + spring_hole_width/2
screw_hole_diameter = 3.6*MM
screw_hole_depth = 1.00*MM

fillet_radius_outside = 5.0*MM


with BuildPart() as mirror_mount:
    mount_box = Box(mount_width, mount_height, mirror_mount_depth)

    top_face = mount_box.faces().sort_by(Axis.Z).last
    bottom_face = mount_box.faces().sort_by(Axis.Z).first

    with BuildSketch(top_face) as mirror_hole:
        # Get top left vertex of the top face
        top_left_vertex = top_face.vertices().group_by(Axis.Y)[-1][0]
        top_left_vertex_margin = top_left_vertex + (mirror_margin, -mirror_margin, 0)
        with Locations(top_left_vertex_margin):
            mirror_hole_rect = Rectangle(mirror_side_length, mirror_side_length, align=(Align.MIN, Align.MAX))

    extrude(amount=-mirror_depth, mode=Mode.SUBTRACT)

    with BuildSketch(top_face) as rod_holders:
        bottom_left_vertex = top_face.vertices().group_by(Axis.Y)[0][0]
        bottom_right_vertex = top_face.vertices().group_by(Axis.Y)[0][-1]

        midpoint_bottom = ShapeList([bottom_left_vertex, bottom_right_vertex]).center()

        with Locations(midpoint_bottom + (0, spring_hole_margin_bottom, 0)):
            Rectangle(spring_hole_length, spring_hole_width, align=(Align.CENTER, Align.MIN))
    
        # with Locations(bottom_right_vertex + (-spring_hole_margin_right, spring_hole_margin_bottom, 0)):
        #     Rectangle(spring_hole_length, spring_hole_width, align=(Align.MAX, Align.MIN))

        # Create diagonal plane from top left to bottom right
        diagonal_plane = Plane(
            origin=(0,0,0),
            z_dir=Vector(1,1,0),
        )
        mirror(about=diagonal_plane)
        fillet(rod_holders.vertices(), radius=spring_hole_width/2.01)

    rod_holders_extrusion = extrude(amount=-rod_diameter, mode=Mode.SUBTRACT)

    with BuildSketch(top_face) as spring_through_holes:
        with Locations(rod_holders.sketch.faces()):
            Rectangle(spring_hole_through_length, spring_hole_width, align=(Align.CENTER, Align.CENTER))
        
    extrude(amount=-mirror_mount_depth, mode=Mode.SUBTRACT)

    top_right_vertex = top_face.vertices().group_by(Axis.Y)[-1][-1]
    with BuildSketch(bottom_face) as screw_holes:
        with Locations([top_left_vertex + (screw_hole_margin_side, -screw_hole_margin_bottom, 0),
                        bottom_right_vertex + (-screw_hole_margin_side, screw_hole_margin_bottom, 0),
                        top_right_vertex + (-screw_hole_margin_side, -screw_hole_margin_bottom, 0)]):
            Circle(screw_hole_diameter/2)
        
    extrude(amount=-screw_hole_depth, mode=Mode.SUBTRACT)

    bottom_face_screw_holes = mirror_mount.faces().sort_by(Axis.Z).first.edges().filter_by(GeomType.CIRCLE)
    chamfer(bottom_face_screw_holes, length=.8*MM)

    z_edges = mount_box.edges().filter_by(Axis.Z)
    top_left_edge = z_edges.filter_by(Axis.Z).group_by(Axis.Y)[-1][0]
    z_edges.remove(top_left_edge)
    fillet(z_edges, radius=fillet_radius_outside)

show(mirror_mount)

# %%

stage_mount_depth = 5.0*MM
m3_nut_radius = 3.2*MM
m3_nut_depth = 2*MM
stage_mount_bottom_size = 8*MM
stage_mount_right_size = 8*MM
fillet_radius_inside = 2*MM

with BuildPart() as stage_mount:
    stage_box = Box(mount_width, mount_height, stage_mount_depth)

    top_face = stage_mount.faces().sort_by(Axis.Z).last
    with BuildSketch(top_face) as stage_spring_through_holes:
        add(spring_through_holes.sketch)
    extrude(amount=-stage_mount_depth, mode=Mode.SUBTRACT)

    bottom_face = stage_box.faces().sort_by(Axis.Z).first
    with BuildSketch(bottom_face) as stage_rod_holders:
        add(rod_holders.sketch, rotation=90)
    extrude(amount=-rod_diameter, mode=Mode.SUBTRACT)

    with BuildSketch(bottom_face) as stage_screw_holes:
        add(screw_holes.sketch)
    extrude(amount=-stage_mount_depth, mode=Mode.SUBTRACT)

    with BuildSketch(top_face) as m3_nut_holes:
        with Locations(mirror(stage_screw_holes.sketch, about=Plane.ZX).faces()):
            RegularPolygon(m3_nut_radius, side_count=6)

    extrude(amount=-m3_nut_depth, mode=Mode.SUBTRACT)

    top_left_vertex = top_face.vertices().group_by(Axis.Y)[-1][0]
    bottom_right_vertex = top_face.vertices().group_by(Axis.Y)[0][-1]
    with BuildSketch(top_face) as cutout:
        with Locations(top_left_vertex):
            rect = Rectangle(mount_width - stage_mount_right_size, mount_height - stage_mount_bottom_size, align=(Align.MIN, Align.MAX))
    
    bottom_right_cutout_vertex = rect.vertices().group_by(Axis.X)[-1][0]

    extrude(amount=-stage_mount_depth, mode=Mode.SUBTRACT)

    z_edges = stage_box.edges().filter_by(Axis.Z)
    fillet(z_edges, radius=fillet_radius_outside)

    bottom_right_cutout_edge = stage_mount.edges().filter_by(Axis.Z).sort_by_distance(bottom_right_cutout_vertex)[0]
    fillet(bottom_right_cutout_edge, radius=fillet_radius_outside)

    bottom_left_cutout_edge = stage_mount.edges().filter_by(Axis.Z).group_by(Axis.X)[0][0]
    top_right_cutout_edge = stage_mount.edges().filter_by(Axis.Z).group_by(Axis.Y)[-1][0]
    fillet([bottom_left_cutout_edge, top_right_cutout_edge], radius=fillet_radius_inside)

show(stage_mount)

# %%
export_step(mirror_mount.part, "step/kinematic_mirror_mount/mirror_mount.step")
export_step(stage_mount.part, "step/kinematic_mirror_mount/stage_mount.step")