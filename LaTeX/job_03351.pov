
////////////////////////////////////////////////////////////////////////
//
//                 Cambridge Crystallographic Data Centre
//                                CCDC 
//
////////////////////////////////////////////////////////////////////////
//
// For information on free software for rendering this file to create very
// high quality bitmap images, please visit the POV-Ray website:
// www.povray.org.
//
// This POV-Ray output mechanism has been tested with POV-Ray version 3.7.
//
// The CCDC is keen to receive feedback on, and suggestions for improvements
// to, this POV-Ray output mechanism. Please visit www.ccdc.cam.ac.uk,
// or e-mail feedback to support@ccdc.cam.ac.uk. Thank you.
//
////////////////////////////////////////////////////////////////////////
//
// If this POVRay file has been generated from an entry in the Cambridge 
// Structural Database, then it will include bibliographic, chemical, crystal, 
// experimental, refinement or atomic coordinate data resulting from the CCDC's 
// data processing and validation procedures.
//
////////////////////////////////////////////////////////////////////////

#version 3.7;
global_settings {
    assumed_gamma 2.2
    max_trace_level 5
}

// -----------------------------------------------------------

#macro rotate_view_for_animation()
    // If using the [filename.pov].ini file, with animation enabled, this will produce
    // a cyclic animation of the scene rotating, otherwise this will not affect the image:
    rotate <0,clock*360,0>
#end

#macro ccdc_perspective_camera( camera_position, field_of_view )
    camera {
        perspective
        location camera_position
        up    <0,1,0>
        right  -x * (image_width/image_height)
        look_at <0,0,-100>
        // Convert the vertical field of view to the horizontal field of view
        angle degrees(2 * atan2(tan(radians(field_of_view / 2)) * image_width, image_height))

        rotate_view_for_animation()
    }
#end

#macro ccdc_directional_light_source( light_position, light_diffuse_colour, light_specular_colour )
    // The scalar multiplier applied to light_position seems to be needed for correct brightness
    light_source {
        5 * light_position
        light_diffuse_colour
        parallel
        shadowless
        rotate_view_for_animation()
    }
    light_source {
        5 * light_position
        light_specular_colour
        parallel
        rotate_view_for_animation()
    }
#end

#macro ccdc_ambient_light_source( light_colour )
    global_settings { ambient_light light_colour * 10 }
#end

#macro ccdc_background_colour( background_colour )
    background { background_colour }
#end

#macro ccdc_background_gradient( top_right_colour, top_left_colour, bottom_left_colour, bottom_right_colour )
    // TODO - adjust to use all four colours
    background { bottom_left_colour }
#end

#macro ccdc_orient_world( world_orientation )
    transform { world_orientation }
#end

#macro ccdc_orient_structure( structure_orientation )
    transform { structure_orientation }
#end

#macro ccdc_set_standard_mercury_solid_material_properties( object_color )
    no_shadow
    texture {
        pigment { object_color }
        finish {
            specular 0.2
            roughness 0.02
        }
    }
#end

#macro ccdc_set_shiny_solid_material_properties( object_color )
    no_shadow
    texture {
        pigment { object_color }
        finish {
            specular 0.8
            roughness 0.02
        }
    }
#end

#macro ccdc_set_matt_solid_material_properties( object_color )
    no_shadow
    texture {
        pigment { object_color }
        finish {
            specular 0.0
            roughness 0.02
        }
    }
#end

#macro ccdc_set_metallic_solid_material_properties( object_color )
    no_shadow
    texture {
        pigment { object_color }
        finish {
            ambient 0.2
            diffuse 0.2
            specular 1.0
            roughness 0.02 
            metallic
            reflection { 0.5, 1.0
               fresnel on
               metallic 0.8
            }
        }
    }
#end

#macro ccdc_set_iridescent_solid_material_properties( object_color )
    no_shadow
    texture {
        pigment { object_color }
        finish {
            ambient 0.1
            diffuse 0.1
            reflection 0.2
            specular 1
            roughness 0.02
            irid {
              0.35
              thickness 0.5
              turbulence 0.5
            }
        }
    }
#end

#macro ccdc_set_solid_material_properties( object_color )
    // change the method call here to select different properties settings
    ccdc_set_standard_mercury_solid_material_properties( object_color )
#end

#macro ccdc_set_wireframe_material_properties( object_color )
    no_shadow
    pigment { object_color }
#end

#macro ccdc_set_point_size( point_size )
    // TODO
#end

#macro ccdc_draw_circle( centre, circle_radius, transformation, circle_color )
    torus {
        circle_radius, 0.03
        transform { transformation }
        translate centre
        ccdc_set_wireframe_material_properties( circle_color )
    }
#end

#macro ccdc_draw_wireframe_sphere( centre, sphere_radius, sphere_color )
    union {
        #local transformation = transform { matrix <
            0, -1, 0,
            1, 0, 0,
            0, 0, 1,
            0, 0, 0 > };
        ccdc_draw_circle( centre, sphere_radius, transformation, sphere_color )
        #local transformation = transform { matrix <
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
            0, 0, 0 > };
        ccdc_draw_circle( centre, sphere_radius, transformation, sphere_color )
        #local transformation = transform { matrix <
            1, 0, 0,
            0, 0, 1,
            0, -1, 0,
            0, 0, 0 > };
        ccdc_draw_circle( centre, sphere_radius, transformation, sphere_color )
        #local transformation = transform { matrix <
            1, 0, 0,
            0, 0.707107, 0.707107,
            0, -0.707107, 0.707107,
            0, 0, 0 > };
        ccdc_draw_circle( centre, sphere_radius, transformation, sphere_color )
        #local transformation = transform { matrix <
            0.5, -0.707107, -0.5,
            0.707107, 0, 0.707107,
            -0.5, -0.707107, 0.5,
            0, 0, 0 > };
        ccdc_draw_circle( centre, sphere_radius, transformation, sphere_color )
        #local transformation = transform { matrix <
            0.707107, -0.707107, 0,
            0.707107, 0.707107, 0,
            0, 0, 1,
            0, 0, 0 > };
        ccdc_draw_circle( centre, sphere_radius, transformation, sphere_color )
        #local transformation = transform { matrix <
            1, 0, 0,
            0, -0.707107, 0.707107,
            0, -0.707107, -0.707107,
            0, 0, 0 > };
        ccdc_draw_circle( centre, sphere_radius, transformation, sphere_color )
        #local transformation = transform { matrix <
            0.5, 0.707107, 0.5,
            -0.707107, 0, 0.707107,
            0.5, -0.707107, 0.5,
            0, 0, 0 > };
        ccdc_draw_circle( centre, sphere_radius, transformation, sphere_color )
        #local transformation = transform { matrix <
            0.707107, 0.707107, 0,
            -0.707107, 0.707107, 0,
            0, 0, 1,
            0, 0, 0 > };
        ccdc_draw_circle( centre, sphere_radius, transformation, sphere_color )

    }
#end

#macro ccdc_draw_solid_sphere( position, sphere_radius, sphere_color )
    sphere {
        position, sphere_radius
        ccdc_set_solid_material_properties( sphere_color )
    }
#end

#macro ccdc_draw_solid_polygon( vertices, origin, transformation, polygon_color )
    #local nvertices = dimension_size( vertices, 1 );
    polygon {
        nvertices + 1
        #local i = 0;
        #while ( i < nvertices )
            vertices[ i ]
            #local i = i + 1;
        #end
        // Repeat the first point, to close the polygon:
        vertices[ 0 ]
        translate origin
        transform { transformation inverse }
        ccdc_set_solid_material_properties( polygon_color )
    }
#end

#macro ccdc_draw_solid_torus( centre, ring_radius, torus_radius, transformation, torus_color )
    torus {
        ring_radius, torus_radius
        transform { transformation }
        translate centre
        ccdc_set_solid_material_properties( torus_color )
    }
#end

#macro ccdc_draw_disk( centre, disk_radius, disk_normal, disk_color )
    // TODO
#end

#macro ccdc_draw_line_segment( line_begin, line_end, line_color )
    cylinder {
        line_begin, line_end, 0.03
        ccdc_set_wireframe_material_properties( line_color )
    }
#end

#macro ccdc_draw_stippled_line_segment( line_begin, line_end, stipple, stipple_scale_factor, line_color )
    // TODO - adjust to use stipple and stipple_scale_factor
    /* For example:

        AACRUB delocalised bonds:
        61680 = F0F0
        
        AABHTZ contacts:
        43690 = AAAA
    */
    // The following is approximately correct when drawing contacts
    #declare nsteps = 20;
    #declare increment = 1 / nsteps;
    #declare scalar1 = 0.0;
    #while ( scalar1 < 1.0 )
        #declare point1 = ( scalar1 * line_begin ) + ( 1 - scalar1 ) * line_end;
        #declare scalar2 = scalar1 + ( increment / 2.0 );
        #declare point2 = ( scalar2 * line_begin ) + ( 1 - scalar2 ) * line_end;
        cylinder {
            point1, point2, 0.03
            ccdc_set_wireframe_material_properties( line_color )
        }
        #declare scalar1 = scalar1 + increment;
    #end
#end

#macro ccdc_draw_wireframe_arc( arc_centre, arc_end_1, arc_end_2,
                                stipple, stipple_scale_factor, line_color )
    // TODO
#end

#macro ccdc_draw_wireframe_ellipsoid( centre, axis1, axis2, axis3, ellipsoid_colour )
    union {
        #local circle_radius = 1.0;
        #local origin = < 0, 0, 0 >;

        #local transformation = transform { matrix <
            0, -1, 0,
            1, 0, 0,
            0, 0, 1,
            0, 0, 0 > };
        ccdc_draw_circle( origin, circle_radius, transformation, ellipsoid_colour )
        #local transformation = transform { matrix <
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
            0, 0, 0 > };
        ccdc_draw_circle( origin, circle_radius, transformation, ellipsoid_colour )
        #local transformation = transform { matrix <
            1, 0, 0,
            0, 0, 1,
            0, -1, 0,
            0, 0, 0 > };
        ccdc_draw_circle( origin, circle_radius, transformation, ellipsoid_colour )
        #local transformation = transform { matrix <
            1, 0, 0,
            0, 0.707107, 0.707107,
            0, -0.707107, 0.707107,
            0, 0, 0 > };
        ccdc_draw_circle( origin, circle_radius, transformation, ellipsoid_colour )
        #local transformation = transform { matrix <
            0.5, -0.707107, -0.5,
            0.707107, 0, 0.707107,
            -0.5, -0.707107, 0.5,
            0, 0, 0 > };
        ccdc_draw_circle( origin, circle_radius, transformation, ellipsoid_colour )
        #local transformation = transform { matrix <
            0.707107, -0.707107, 0,
            0.707107, 0.707107, 0,
            0, 0, 1,
            0, 0, 0 > };
        ccdc_draw_circle( origin, circle_radius, transformation, ellipsoid_colour )
        #local transformation = transform { matrix <
            1, 0, 0,
            0, -0.707107, 0.707107,
            0, -0.707107, -0.707107,
            0, 0, 0 > };
        ccdc_draw_circle( origin, circle_radius, transformation, ellipsoid_colour )
        #local transformation = transform { matrix <
            0.5, 0.707107, 0.5,
            -0.707107, 0, 0.707107,
            0.5, -0.707107, 0.5,
            0, 0, 0 > };
        ccdc_draw_circle( origin, circle_radius, transformation, ellipsoid_colour )
        #local transformation = transform { matrix <
            0.707107, 0.707107, 0,
            -0.707107, 0.707107, 0,
            0, 0, 1,
            0, 0, 0 > };
        ccdc_draw_circle( origin, circle_radius, transformation, ellipsoid_colour )

        scale < vlength( axis1 ), vlength( axis2 ), vlength( axis3 ) >
        #declare axis1_norm = vnormalize( axis1 );
        #declare axis2_norm = vnormalize( axis2 );
        #declare axis3_norm = vnormalize( axis3 );
        matrix < axis1_norm.x,  axis1_norm.y,  axis1_norm.z,
                 axis2_norm.x,  axis2_norm.y,  axis2_norm.z,
                 axis3_norm.x,  axis3_norm.y,  axis3_norm.z,
                 0, 0, 0 >

        translate centre
    }
#end

#macro ccdc_draw_open_cylinder( centre_line_begin, centre_line_end, cylinder_radius, cylinder_color )
    cylinder {
        centre_line_begin, centre_line_end, cylinder_radius
        open
        ccdc_set_solid_material_properties( cylinder_color )
    }
#end

#macro ccdc_draw_closed_cylinder( centre_line_begin, centre_line_end, cylinder_radius, cylinder_color )
    cylinder {
        centre_line_begin, centre_line_end, cylinder_radius
        ccdc_set_solid_material_properties( cylinder_color )
    }
#end

#macro ccdc_draw_solid_ellipsoid( centre, axis1, axis2, axis3, ellipsoid_color )
    sphere {
        < 0, 0, 0 >, 1
        scale < vlength( axis1 ), vlength( axis2 ), vlength( axis3 ) >
        #declare axis1_norm = vnormalize( axis1 );
        #declare axis2_norm = vnormalize( axis2 );
        #declare axis3_norm = vnormalize( axis3 );
        matrix < axis1_norm.x,  axis1_norm.y,  axis1_norm.z,
                 axis2_norm.x,  axis2_norm.y,  axis2_norm.z,
                 axis3_norm.x,  axis3_norm.y,  axis3_norm.z,
                 0, 0, 0 >
        translate centre
        ccdc_set_solid_material_properties( ellipsoid_color )
    }
#end

#macro ccdc_draw_ellipsoid_axes( centre, axis1, axis2, axis3, axes_color )
    union {
        cylinder {
            < 0.05, 0, 0 >, < -0.05, 0, 0 >, 1
        }
        cylinder {
            < 0, 0.05, 0 >, < 0, -0.05, 0 >, 1
        }
        cylinder {
            < 0, 0, 0.05 >, < 0, 0, -0.05 >, 1
        }
        #local axis_height = 0.01;
        scale < vlength( axis1 ) + axis_height, vlength( axis2 ) + axis_height, vlength( axis3 ) + axis_height >
        #declare axis1_norm = vnormalize( axis1 );
        #declare axis2_norm = vnormalize( axis2 );
        #declare axis3_norm = vnormalize( axis3 );
        matrix < axis1_norm.x,  axis1_norm.y,  axis1_norm.z,
                 axis2_norm.x,  axis2_norm.y,  axis2_norm.z,
                 axis3_norm.x,  axis3_norm.y,  axis3_norm.z,
                 0, 0, 0 >
        translate centre
        ccdc_set_solid_material_properties( axes_color )
    }
#end

#macro ccdc_draw_point( point_location, point_color )
    // TODO
#end

#macro ccdc_draw_solid_triangle( corner1, corner2, corner3,
                                 color1, color2, color3,
                                 normal1, normal2, normal3 )
   smooth_triangle {
        corner1, normal1,
        corner2, normal2,
        corner3, normal3
        ccdc_set_solid_material_properties( color1 )
        // TODO POVRay does not appear to support different colours for 
        //      different vertices in a smooth_triangle
        //      See section 3.5.8 of the POVRay help.
   }
#end

#macro ccdc_draw_solid_triangle_without_normals( corner1, corner2, corner3,
                                                 color1, color2, color3 )
   triangle {
        corner1,
        corner2,
        corner3
        ccdc_set_solid_material_properties( color1 )
        // TODO POVRay does not appear to support different colours for 
        //      different vertices in a smooth_triangle
        //      See section 3.5.8 of the POVRay help.
   }
#end

#macro ccdc_draw_text( position, message, text_color, text_offset )
    // TODO - Adjust so that the text orientation is correct
    text { ttf font_name, message, 0.1, 0
        ccdc_set_wireframe_material_properties( color text_color )
        /*
        finish {
            ambient 0.2
            diffuse 0.6
            phong 0.3
            phong_size 100
        }
        */
        scale < font_scale, font_scale, font_scale >
        // rotate so text always faces the camera when animated
        rotate <0,clock*360,0>
        translate text_offset
        transform { world_rotation inverse }
        transform { structure_rotation inverse }
        translate position
    }
#end

#macro ccdc_draw_static_text( message )
    // TODO
#end

// -----------------------------------------------------------

// You can edit the file "ccdc_macro_overrides.inc" in this directory
// to override the implementations of any or all the above POVRay macros:
#include "ccdc_macro_overrides.inc"

#declare font_scale = 0.340306;

#declare font_name = "arial.ttf";

ccdc_perspective_camera( < 0, 0, 19498.1 >, 0.05 )
ccdc_directional_light_source( < 1, 1, 1 >, rgb < 0.701961, 0.701961, 0.701961 >, rgb < 1, 1, 1 > )
ccdc_directional_light_source( < -1, 0.2, 1 >, rgb < 0.501961, 0.501961, 0.501961 >, rgb < 0.501961, 0.501961, 0.501961 > )
ccdc_ambient_light_source( rgb < 0.301961, 0.301961, 0.301961 > )
union {
    #declare world_orientation = transform { matrix <
        0.608118, -0.751754, -0.255065,
        0.210924, 0.462762, -0.861024,
        0.765313, 0.469805, 0.439977,
        -0.528357, -0.9017, 0 > };
    #declare world_rotation = transform { matrix <
        0.608118, -0.751754, -0.255065,
        0.210924, 0.462762, -0.861024,
        0.765313, 0.469805, 0.439977,
        0, 0, 0 > };
    union {
        // job_03351
        #declare structure_orientation = transform { matrix <
            -0.276386, -0.931822, 0.235198,
            -0.0668817, -0.225488, -0.971947,
            0.958717, -0.284363, 0,
            -1.27887, 5.40223, 7.71717 > };
        #declare structure_rotation = transform { matrix <
            -0.276386, -0.931822, 0.235198,
            -0.0668817, -0.225488, -0.971947,
            0.958717, -0.284363, 0,
            0, 0, 0 > };
        // job_03351 atoms
        // atom C1
        ccdc_draw_solid_sphere( < 1.60498, 8.90418, 2.7625 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C2
        ccdc_draw_solid_sphere( < 2.03285, 8.09251, 3.9805 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C3
        ccdc_draw_solid_sphere( < 1.19862, 7.6674, 5.00483 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C4
        ccdc_draw_solid_sphere( < 1.7826, 6.93606, 6.03047 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C5
        ccdc_draw_solid_sphere( < 2.23873, 5.72127, 7.92222 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C6
        ccdc_draw_solid_sphere( < 2.47684, 10.1553, 2.76262 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C7
        ccdc_draw_solid_sphere( < 2.01598, 11.4645, 2.76262 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C8
        ccdc_draw_solid_sphere( < 2.97389, 12.4695, 2.76274 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C9
        ccdc_draw_solid_sphere( < 4.11936, 14.4572, 2.76262 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C10
        ccdc_draw_solid_sphere( < 2.03265, 8.09292, 1.54415 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C11
        ccdc_draw_solid_sphere( < 1.19843, 7.66819, 0.519578 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C12
        ccdc_draw_solid_sphere( < 1.78244, 6.93715, -0.506295 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C13
        ccdc_draw_solid_sphere( < 2.23826, 5.72265, -2.39817 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C14
        ccdc_draw_solid_sphere( < 4.12551, 8.36149, 2.76226 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C15
        ccdc_draw_solid_sphere( < 3.40191, 7.79789, 3.98038 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C16
        ccdc_draw_solid_sphere( < 3.98732, 7.06692, 5.0046 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C17
        ccdc_draw_solid_sphere( < 3.15414, 6.64078, 6.03035 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C18
        ccdc_draw_solid_sphere( < 3.84586, 9.86061, 2.7625 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C19
        ccdc_draw_solid_sphere( < 4.80468, 10.864, 2.76238 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C20
        ccdc_draw_solid_sphere( < 4.34543, 12.1742, 2.76262 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C21
        ccdc_draw_solid_sphere( < 3.40176, 7.79811, 1.54403 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C22
        ccdc_draw_solid_sphere( < 3.98717, 7.06772, 0.519459 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom C23
        ccdc_draw_solid_sphere( < 3.15396, 6.64196, -0.506413 >, 0.425, rgb < 0.568627, 0.568627, 0.568627 > )
        // atom H24
        ccdc_draw_solid_sphere( < 0.539194, 9.13372, 2.7625 >, 0.3, rgb < 1, 1, 1 > )
        // atom H25
        ccdc_draw_solid_sphere( < 0.139147, 7.89582, 5.00471 >, 0.3, rgb < 1, 1, 1 > )
        // atom H26
        ccdc_draw_solid_sphere( < 0.956485, 11.6922, 2.76262 >, 0.3, rgb < 1, 1, 1 > )
        // atom H27
        ccdc_draw_solid_sphere( < 0.139018, 7.89652, 0.520052 >, 0.3, rgb < 1, 1, 1 > )
        // atom H28
        ccdc_draw_solid_sphere( < 0.29965, 6.39377, 7.49065 >, 0.3, rgb < 1, 1, 1 > )
        // atom H29
        ccdc_draw_solid_sphere( < 2.02283, 14.3987, 2.76286 >, 0.3, rgb < 1, 1, 1 > )
        // atom H30
        ccdc_draw_solid_sphere( < 0.299146, 6.39473, -1.96624 >, 0.3, rgb < 1, 1, 1 > )
        // atom H31
        ccdc_draw_solid_sphere( < 5.19146, 8.13203, 2.76215 >, 0.3, rgb < 1, 1, 1 > )
        // atom H32
        ccdc_draw_solid_sphere( < 5.0468, 6.83906, 5.00424 >, 0.3, rgb < 1, 1, 1 > )
        // atom H33
        ccdc_draw_solid_sphere( < 5.86403, 10.6355, 2.76226 >, 0.3, rgb < 1, 1, 1 > )
        // atom H34
        ccdc_draw_solid_sphere( < 5.04661, 6.83985, 0.519696 >, 0.3, rgb < 1, 1, 1 > )
        // atom H35
        ccdc_draw_solid_sphere( < 4.28283, 5.53607, 7.49041 >, 0.3, rgb < 1, 1, 1 > )
        // atom H36
        ccdc_draw_solid_sphere( < 6.00602, 13.541, 2.7625 >, 0.3, rgb < 1, 1, 1 > )
        // atom H37
        ccdc_draw_solid_sphere( < 4.28237, 5.53712, -1.96647 >, 0.3, rgb < 1, 1, 1 > )
        // atom O38
        ccdc_draw_solid_sphere( < 2.11219, 5.13281, 8.96577 >, 0.38, rgb < 0.941176, 0, 0 > )
        // atom O39
        ccdc_draw_solid_sphere( < 4.37292, 15.6349, 2.76262 >, 0.38, rgb < 0.941176, 0, 0 > )
        // atom O40
        ccdc_draw_solid_sphere( < 2.11149, 5.13392, -3.44159 >, 0.38, rgb < 0.941176, 0, 0 > )
        // atom N41
        ccdc_draw_solid_sphere( < 1.25684, 6.3691, 7.18277 >, 0.3875, rgb < 0.560784, 0.560784, 1 > )
        // atom N42
        ccdc_draw_solid_sphere( < 2.86796, 13.8533, 2.76274 >, 0.3875, rgb < 0.560784, 0.560784, 1 > )
        // atom N43
        ccdc_draw_solid_sphere( < 1.2565, 6.37059, -1.65871 >, 0.3875, rgb < 0.560784, 0.560784, 1 > )
        // atom N44
        ccdc_draw_solid_sphere( < 3.40019, 5.90757, 7.18265 >, 0.3875, rgb < 0.560784, 0.560784, 1 > )
        // atom N45
        ccdc_draw_solid_sphere( < 5.01128, 13.3917, 2.7625 >, 0.3875, rgb < 0.560784, 0.560784, 1 > )
        // atom N46
        ccdc_draw_solid_sphere( < 3.39985, 5.90906, -1.65883 >, 0.3875, rgb < 0.560784, 0.560784, 1 > )
        // job_03351 bonds
        // bond C1-C2
        ccdc_draw_closed_cylinder( < 1.60498, 8.90418, 2.7625 >, < 2.03285, 8.09251, 3.9805 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C1-C6
        ccdc_draw_closed_cylinder( < 1.60498, 8.90418, 2.7625 >, < 2.47684, 10.1553, 2.76262 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C1-C10
        ccdc_draw_closed_cylinder( < 1.60498, 8.90418, 2.7625 >, < 2.03265, 8.09292, 1.54415 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C1-H24
        ccdc_draw_closed_cylinder( < 1.60498, 8.90418, 2.7625 >, < 1.07209, 9.01895, 2.7625 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 1.07209, 9.01895, 2.7625 >, < 0.539194, 9.13372, 2.7625 >, 0.1, rgb < 1, 1, 1 > )
        // bond C2-C3
        ccdc_draw_closed_cylinder( < 2.03285, 8.09251, 3.9805 >, < 1.19862, 7.6674, 5.00483 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C2-C15
        ccdc_draw_closed_cylinder( < 2.03285, 8.09251, 3.9805 >, < 3.40191, 7.79789, 3.98038 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C3-C4
        ccdc_draw_closed_cylinder( < 1.19862, 7.6674, 5.00483 >, < 1.7826, 6.93606, 6.03047 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C3-H25
        ccdc_draw_closed_cylinder( < 1.19862, 7.6674, 5.00483 >, < 0.668884, 7.78161, 5.00477 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 0.668884, 7.78161, 5.00477 >, < 0.139147, 7.89582, 5.00471 >, 0.1, rgb < 1, 1, 1 > )
        // bond C4-C17
        ccdc_draw_closed_cylinder( < 1.7826, 6.93606, 6.03047 >, < 3.15414, 6.64078, 6.03035 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C4-N41
        ccdc_draw_closed_cylinder( < 1.7826, 6.93606, 6.03047 >, < 1.51972, 6.65258, 6.60662 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 1.51972, 6.65258, 6.60662 >, < 1.25684, 6.3691, 7.18277 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C5-O38
        ccdc_draw_closed_cylinder( < 2.23873, 5.72127, 7.92222 >, < 2.17546, 5.42704, 8.444 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 2.17546, 5.42704, 8.444 >, < 2.11219, 5.13281, 8.96577 >, 0.1, rgb < 0.941176, 0, 0 > )
        // bond C5-N41
        ccdc_draw_closed_cylinder( < 2.23873, 5.72127, 7.92222 >, < 1.74778, 6.04519, 7.5525 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 1.74778, 6.04519, 7.5525 >, < 1.25684, 6.3691, 7.18277 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C5-N44
        ccdc_draw_closed_cylinder( < 2.23873, 5.72127, 7.92222 >, < 2.81946, 5.81442, 7.55244 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 2.81946, 5.81442, 7.55244 >, < 3.40019, 5.90757, 7.18265 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C6-C7
        ccdc_draw_closed_cylinder( < 2.47684, 10.1553, 2.76262 >, < 2.01598, 11.4645, 2.76262 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C6-C18
        ccdc_draw_closed_cylinder( < 2.47684, 10.1553, 2.76262 >, < 3.84586, 9.86061, 2.7625 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C7-C8
        ccdc_draw_closed_cylinder( < 2.01598, 11.4645, 2.76262 >, < 2.97389, 12.4695, 2.76274 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C7-H26
        ccdc_draw_closed_cylinder( < 2.01598, 11.4645, 2.76262 >, < 1.48623, 11.5783, 2.76262 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 1.48623, 11.5783, 2.76262 >, < 0.956485, 11.6922, 2.76262 >, 0.1, rgb < 1, 1, 1 > )
        // bond C8-C20
        ccdc_draw_closed_cylinder( < 2.97389, 12.4695, 2.76274 >, < 4.34543, 12.1742, 2.76262 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C8-N42
        ccdc_draw_closed_cylinder( < 2.97389, 12.4695, 2.76274 >, < 2.92093, 13.1614, 2.76274 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 2.92093, 13.1614, 2.76274 >, < 2.86796, 13.8533, 2.76274 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C9-O39
        ccdc_draw_closed_cylinder( < 4.11936, 14.4572, 2.76262 >, < 4.24614, 15.0461, 2.76262 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 4.24614, 15.0461, 2.76262 >, < 4.37292, 15.6349, 2.76262 >, 0.1, rgb < 0.941176, 0, 0 > )
        // bond C9-N42
        ccdc_draw_closed_cylinder( < 4.11936, 14.4572, 2.76262 >, < 3.49366, 14.1552, 2.76268 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 3.49366, 14.1552, 2.76268 >, < 2.86796, 13.8533, 2.76274 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C9-N45
        ccdc_draw_closed_cylinder( < 4.11936, 14.4572, 2.76262 >, < 4.56532, 13.9245, 2.76256 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 4.56532, 13.9245, 2.76256 >, < 5.01128, 13.3917, 2.7625 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C10-C11
        ccdc_draw_closed_cylinder( < 2.03265, 8.09292, 1.54415 >, < 1.19843, 7.66819, 0.519578 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C10-C21
        ccdc_draw_closed_cylinder( < 2.03265, 8.09292, 1.54415 >, < 3.40176, 7.79811, 1.54403 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C11-C12
        ccdc_draw_closed_cylinder( < 1.19843, 7.66819, 0.519578 >, < 1.78244, 6.93715, -0.506295 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C11-H27
        ccdc_draw_closed_cylinder( < 1.19843, 7.66819, 0.519578 >, < 0.668725, 7.78236, 0.519815 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 0.668725, 7.78236, 0.519815 >, < 0.139018, 7.89652, 0.520052 >, 0.1, rgb < 1, 1, 1 > )
        // bond C12-C23
        ccdc_draw_closed_cylinder( < 1.78244, 6.93715, -0.506295 >, < 3.15396, 6.64196, -0.506413 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C12-N43
        ccdc_draw_closed_cylinder( < 1.78244, 6.93715, -0.506295 >, < 1.51947, 6.65387, -1.0825 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 1.51947, 6.65387, -1.0825 >, < 1.2565, 6.37059, -1.65871 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C13-O40
        ccdc_draw_closed_cylinder( < 2.23826, 5.72265, -2.39817 >, < 2.17487, 5.42829, -2.91988 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 2.17487, 5.42829, -2.91988 >, < 2.11149, 5.13392, -3.44159 >, 0.1, rgb < 0.941176, 0, 0 > )
        // bond C13-N43
        ccdc_draw_closed_cylinder( < 2.23826, 5.72265, -2.39817 >, < 1.74738, 6.04662, -2.02844 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 1.74738, 6.04662, -2.02844 >, < 1.2565, 6.37059, -1.65871 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C13-N46
        ccdc_draw_closed_cylinder( < 2.23826, 5.72265, -2.39817 >, < 2.81905, 5.81586, -2.0285 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 2.81905, 5.81586, -2.0285 >, < 3.39985, 5.90906, -1.65883 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C14-C15
        ccdc_draw_closed_cylinder( < 4.12551, 8.36149, 2.76226 >, < 3.40191, 7.79789, 3.98038 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C14-C18
        ccdc_draw_closed_cylinder( < 4.12551, 8.36149, 2.76226 >, < 3.84586, 9.86061, 2.7625 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C14-C21
        ccdc_draw_closed_cylinder( < 4.12551, 8.36149, 2.76226 >, < 3.40176, 7.79811, 1.54403 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C14-H31
        ccdc_draw_closed_cylinder( < 4.12551, 8.36149, 2.76226 >, < 4.65849, 8.24676, 2.76221 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 4.65849, 8.24676, 2.76221 >, < 5.19146, 8.13203, 2.76215 >, 0.1, rgb < 1, 1, 1 > )
        // bond C15-C16
        ccdc_draw_closed_cylinder( < 3.40191, 7.79789, 3.98038 >, < 3.98732, 7.06692, 5.0046 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C16-C17
        ccdc_draw_closed_cylinder( < 3.98732, 7.06692, 5.0046 >, < 3.15414, 6.64078, 6.03035 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C16-H32
        ccdc_draw_closed_cylinder( < 3.98732, 7.06692, 5.0046 >, < 4.51706, 6.95299, 5.00442 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 4.51706, 6.95299, 5.00442 >, < 5.0468, 6.83906, 5.00424 >, 0.1, rgb < 1, 1, 1 > )
        // bond C17-N44
        ccdc_draw_closed_cylinder( < 3.15414, 6.64078, 6.03035 >, < 3.27717, 6.27418, 6.6065 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 3.27717, 6.27418, 6.6065 >, < 3.40019, 5.90757, 7.18265 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C18-C19
        ccdc_draw_closed_cylinder( < 3.84586, 9.86061, 2.7625 >, < 4.80468, 10.864, 2.76238 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C19-C20
        ccdc_draw_closed_cylinder( < 4.80468, 10.864, 2.76238 >, < 4.34543, 12.1742, 2.76262 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C19-H33
        ccdc_draw_closed_cylinder( < 4.80468, 10.864, 2.76238 >, < 5.33436, 10.7497, 2.76232 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 5.33436, 10.7497, 2.76232 >, < 5.86403, 10.6355, 2.76226 >, 0.1, rgb < 1, 1, 1 > )
        // bond C20-N45
        ccdc_draw_closed_cylinder( < 4.34543, 12.1742, 2.76262 >, < 4.67836, 12.783, 2.76256 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 4.67836, 12.783, 2.76256 >, < 5.01128, 13.3917, 2.7625 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond C21-C22
        ccdc_draw_closed_cylinder( < 3.40176, 7.79811, 1.54403 >, < 3.98717, 7.06772, 0.519459 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C22-C23
        ccdc_draw_closed_cylinder( < 3.98717, 7.06772, 0.519459 >, < 3.15396, 6.64196, -0.506413 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        // bond C22-H34
        ccdc_draw_closed_cylinder( < 3.98717, 7.06772, 0.519459 >, < 4.51689, 6.95379, 0.519578 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 4.51689, 6.95379, 0.519578 >, < 5.04661, 6.83985, 0.519696 >, 0.1, rgb < 1, 1, 1 > )
        // bond C23-N46
        ccdc_draw_closed_cylinder( < 3.15396, 6.64196, -0.506413 >, < 3.2769, 6.27551, -1.08262 >, 0.1, rgb < 0.568627, 0.568627, 0.568627 > )
        ccdc_draw_closed_cylinder( < 3.2769, 6.27551, -1.08262 >, < 3.39985, 5.90906, -1.65883 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond H28-N41
        ccdc_draw_closed_cylinder( < 0.29965, 6.39377, 7.49065 >, < 0.778245, 6.38143, 7.33671 >, 0.1, rgb < 1, 1, 1 > )
        ccdc_draw_closed_cylinder( < 0.778245, 6.38143, 7.33671 >, < 1.25684, 6.3691, 7.18277 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond H29-N42
        ccdc_draw_closed_cylinder( < 2.02283, 14.3987, 2.76286 >, < 2.4454, 14.126, 2.7628 >, 0.1, rgb < 1, 1, 1 > )
        ccdc_draw_closed_cylinder( < 2.4454, 14.126, 2.7628 >, < 2.86796, 13.8533, 2.76274 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond H30-N43
        ccdc_draw_closed_cylinder( < 0.299146, 6.39473, -1.96624 >, < 0.77782, 6.38266, -1.81247 >, 0.1, rgb < 1, 1, 1 > )
        ccdc_draw_closed_cylinder( < 0.77782, 6.38266, -1.81247 >, < 1.2565, 6.37059, -1.65871 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond H35-N44
        ccdc_draw_closed_cylinder( < 4.28283, 5.53607, 7.49041 >, < 3.84151, 5.72182, 7.33653 >, 0.1, rgb < 1, 1, 1 > )
        ccdc_draw_closed_cylinder( < 3.84151, 5.72182, 7.33653 >, < 3.40019, 5.90757, 7.18265 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond H36-N45
        ccdc_draw_closed_cylinder( < 6.00602, 13.541, 2.7625 >, < 5.50865, 13.4664, 2.7625 >, 0.1, rgb < 1, 1, 1 > )
        ccdc_draw_closed_cylinder( < 5.50865, 13.4664, 2.7625 >, < 5.01128, 13.3917, 2.7625 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        // bond H37-N46
        ccdc_draw_closed_cylinder( < 4.28237, 5.53712, -1.96647 >, < 3.84111, 5.72309, -1.81265 >, 0.1, rgb < 1, 1, 1 > )
        ccdc_draw_closed_cylinder( < 3.84111, 5.72309, -1.81265 >, < 3.39985, 5.90906, -1.65883 >, 0.1, rgb < 0.560784, 0.560784, 1 > )
        ccdc_orient_structure( structure_orientation )
        #declare structure_orientation = transform { matrix <
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
            0, 0, 0 > };
        #declare structure_rotation = transform { matrix <
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
            0, 0, 0 > };
    }
    // job_03351 finished
    ccdc_orient_world( world_orientation )
}
