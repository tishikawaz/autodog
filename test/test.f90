module class_weno5_js
    !**
    !* NOTE: If you use a grid that has curvature, variables are not interpolated by 5th order.
    !* Efficient Implementation of Weighted ENO Schemes (https://www.sciencedirect.com/science/article/pii/S0021999196901308)
    !*

    use typedef_module
    use abstract_reconstructor
    use abstract_configuration
    use weno_utils
    use stdio_module

    implicit none

    private

    type, public, extends(reconstructor) :: weno5_js
        private

        real(real_kind) :: epsilon_

        contains

        procedure, public, pass(self) :: initialize
        procedure, public, pass(self) :: reconstruct_lhc
        procedure, public, pass(self) :: reconstruct_rhc
    end type weno5_js

    contains

    subroutine initialize(self, config, a_reconstructor_generator)
        class(weno5_js               ),           intent(inout) :: self
        class(configuration          ),           intent(inout) :: config
        class(reconstructor_generator), optional, intent(inout) :: a_reconstructor_generator

        logical :: found

        call config%get_real("Reconstructor.WENO5-JS.Epsilon", self%epsilon_, found, 1.d-6)
        if(.not. found) call write_warring("'Reconstructor.WENO5-JS.Epsilon' is not found in configration you set. To be set dafault value.")
    end subroutine initialize

    pure function reconstruct_lhc( &
        self                     , &
        primitive_variables_set  , &
        face_to_cell_index       , &
        cell_centor_positions    , &
        face_centor_positions    , &
        face_index               , &
        num_local_cells          , &
        num_primitive_variables      ) result(reconstructed_primitive_variables)

        class  (weno5_js ), intent(in) :: self
        integer(int_kind ), intent(in) :: face_index
        real   (real_kind), intent(in) :: primitive_variables_set          (:, :)
        integer(int_kind ), intent(in) :: face_to_cell_index               (:, :)
        real   (real_kind), intent(in) :: cell_centor_positions            (:, :)
        real   (real_kind), intent(in) :: face_centor_positions            (:, :)
        integer(int_kind ), intent(in) :: num_local_cells
        integer(int_kind ), intent(in) :: num_primitive_variables
        real   (real_kind)             :: reconstructed_primitive_variables(num_primitive_variables)

        integer(int_kind ) :: i
        real   (real_kind) :: w(3), p(3)
        real   (real_kind) :: ideal_w(3), b_coef(3,3), p_coef(3,2)

        associate(                                                                                  &
            p_m3 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells-2, face_index)), &
            p_m2 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells-1, face_index)), &
            p_m1 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells+0, face_index)), &
            p_0  => cell_centor_positions(1:3, face_to_cell_index(num_local_cells+1, face_index)), &
            p_p1 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells+2, face_index)), &
            p_p2 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells+3, face_index))  &
        )
            ideal_w(:  ) = compute_ideal_weights_left_side            (p_m3, p_m2, p_m1, p_0, p_p1, p_p2)
            b_coef (:,:) = compute_js_indicator_coefficients_left_side(p_m3, p_m2, p_m1, p_0, p_p1, p_p2)
            p_coef (:,:) = compute_polynomials_coefficients_left_side (p_m3, p_m2, p_m1, p_0, p_p1, p_p2)
        end associate

        do i = 1, num_primitive_variables, 1
            associate(                                                                                 &
                v_m2 => primitive_variables_set(i, face_to_cell_index(num_local_cells-2, face_index)), &
                v_m1 => primitive_variables_set(i, face_to_cell_index(num_local_cells-1, face_index)), &
                v    => primitive_variables_set(i, face_to_cell_index(num_local_cells+0, face_index)), &
                v_p1 => primitive_variables_set(i, face_to_cell_index(num_local_cells+1, face_index)), &
                v_p2 => primitive_variables_set(i, face_to_cell_index(num_local_cells+2, face_index))  &
            )
                w(1:3) = compute_weights_left_side    (v_m2, v_m1, v, v_p1, v_p2, ideal_w, b_coef, self%epsilon_)
                p(1:3) = compute_polynomials_left_side(v_m2, v_m1, v, v_p1, v_p2, p_coef)
                reconstructed_primitive_variables(i) = w(1) * p(1) + w(2) * p(2) + w(3) * p(3)
            end associate
        end do
    end function reconstruct_lhc

    pure function reconstruct_rhc( &
        self                     , &
        primitive_variables_set  , &
        face_to_cell_index       , &
        cell_centor_positions    , &
        face_centor_positions    , &
        face_index               , &
        num_local_cells          , &
        num_primitive_variables      ) result(reconstructed_primitive_variables)

        class  (weno5_js ), intent(in) :: self
        integer(int_kind ), intent(in) :: face_index
        real   (real_kind), intent(in) :: primitive_variables_set          (:, :)
        integer(int_kind ), intent(in) :: face_to_cell_index               (:, :)
        real   (real_kind), intent(in) :: cell_centor_positions            (:, :)
        real   (real_kind), intent(in) :: face_centor_positions            (:, :)
        integer(int_kind ), intent(in) :: num_local_cells
        integer(int_kind ), intent(in) :: num_primitive_variables
        real   (real_kind)             :: reconstructed_primitive_variables(num_primitive_variables)

        integer(int_kind ) :: i
        real   (real_kind) :: w(3), p(3)
        real   (real_kind) :: ideal_w(3), b_coef(3,3), p_coef(3,2)

        associate(                                                                                  &
            p_m3 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells-2, face_index)), &
            p_m2 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells-1, face_index)), &
            p_m1 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells+0, face_index)), &
            p_0  => cell_centor_positions(1:3, face_to_cell_index(num_local_cells+1, face_index)), &
            p_p1 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells+2, face_index)), &
            p_p2 => cell_centor_positions(1:3, face_to_cell_index(num_local_cells+3, face_index))  &
        )
            ideal_w(:  ) = compute_ideal_weights_right_side            (p_m3, p_m2, p_m1, p_0, p_p1, p_p2)
            b_coef (:,:) = compute_js_indicator_coefficients_right_side(p_m3, p_m2, p_m1, p_0, p_p1, p_p2)
            p_coef (:,:) = compute_polynomials_coefficients_right_side (p_m3, p_m2, p_m1, p_0, p_p1, p_p2)
        end associate

        do i = 1, num_primitive_variables, 1
            associate(                                                                                 &
                v_m2 => primitive_variables_set(i, face_to_cell_index(num_local_cells-1, face_index)), &
                v_m1 => primitive_variables_set(i, face_to_cell_index(num_local_cells+0, face_index)), &
                v    => primitive_variables_set(i, face_to_cell_index(num_local_cells+1, face_index)), &
                v_p1 => primitive_variables_set(i, face_to_cell_index(num_local_cells+2, face_index)), &
                v_p2 => primitive_variables_set(i, face_to_cell_index(num_local_cells+3, face_index))  &
            )
                w(1:3) = compute_weights_right_side    (v_m2, v_m1, v, v_p1, v_p2, ideal_w, b_coef, self%epsilon_)
                p(1:3) = compute_polynomials_right_side(v_m2, v_m1, v, v_p1, v_p2, p_coef)
                reconstructed_primitive_variables(i) = w(1) * p(1) + w(2) * p(2) + w(3) * p(3)
            end associate
        end do
    end function reconstruct_rhc

end module class_weno5_js