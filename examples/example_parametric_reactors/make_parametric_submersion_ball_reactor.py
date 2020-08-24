"""
This example creates a submersion ball reactor using the SubmersionBallReactor
parametric shape
"""

import paramak


def main():

    my_reactor = paramak.SubmersionTokamak(
        inner_bore_radial_thickness=10,
        inboard_tf_leg_radial_thickness=30,
        center_column_shield_radial_thickness=60,
        divertor_radial_thickness=50,
        inner_plasma_gap_radial_thickness=30,
        plasma_radial_thickness=300,
        outer_plasma_gap_radial_thickness=30,
        firstwall_radial_thickness=30,
        blanket_rear_wall_radial_thickness=30,
        number_of_tf_coils=16,
        rotation_angle=180,
        support_radial_thickness=20,
        inboard_blanket_radial_thickness=20,
        outboard_blanket_radial_thickness=20,
        plasma_high_point=(200, 200),
        pf_coil_radial_thicknesses=[50, 50, 50, 50],
        pf_coil_vertical_thicknesses=[50, 50, 50, 50],
        pf_coil_to_tf_coil_radial_gap=50,
        outboard_tf_coil_radial_thickness=100,
        tf_coil_poloidal_thickness=50,
        tf_coil_to_rear_blanket_radial_gap=20
)

    my_reactor.export_stp()

    my_reactor.export_neutronics_description()


if __name__ == "__main__":
    main()
