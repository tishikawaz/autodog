module fortran_programmer_module
    ! ------------------------------------------------------------------------------
    ! Module: fortran_programmer_module
    ! ------------------------------------------------------------------------------
    ! This module defines a Fortran programmer class that extends the programmer
    ! class.
    ! It contains methods to initialize the programmer and print their language.
    ! 
    ! Public Types:
    ! fortran_programmer_class - A derived type that extends the programmer class.
    ! 
    ! Public Methods:
    ! initialize - Initializes the programmer with a specified language or defaults to
    ! 'Fortran'.
    ! who_is - Prints the programmer's language.
    ! ------------------------------------------------------------------------------
    implicit none

    private

    type, public, extends(programmer) :: fortran_programmer_class
        private

        character(:),allocatable :: language

        contains

        procedure, public, pass(self) :: initialize
        procedure, public, pass(self) :: who_is
    end type fortran_programmer_class

    contains

    subroutine initialize(self, language)
        ! This subroutine initializes the `self` object of type
        ! `fortran_programmer_class`.
        ! It assigns the `language` attribute of the `self` object with the provided
        ! `language` value.
        ! If `language` is not provided, it assigns the `language` attribute with the
        ! default value 'Fortran'.
        ! Parameters:
        ! - self: The `self` object of type `fortran_programmer_class`.
        ! - language: The language to assign to the `language` attribute of the `self`
        ! object (optional).
        class(fortran_programmer_class), intent(inout) :: self
        character(:), allocatable, intent(in), optional :: language

        if (present(language)) then
            allocate(self%language, source = language)
            return
        end if
        allocate(self%language, source = 'Fortran')
    end subroutine initialize

    subroutine who_is(self)
        ! This subroutine prints the type of programmer based on the language attribute of
        ! the fortran_programmer_class object.
        ! 
        ! Parameters:
        ! self: inout, class(fortran_programmer_class)
        ! The object of type fortran_programmer_class whose language attribute will be
        ! used to determine the type of programmer.
        ! 
        ! Output:
        ! None
        ! 
        ! Example usage:
        ! call who_is(my_programmer)
        ! 
        ! where my_programmer is an object of type fortran_programmer_class.
        ! 
        ! This will print the type of programmer based on the language attribute of
        ! my_programmer object.
        ! 
        ! For example, if my_programmer%language is 'Fortran', the output will be 'I am
        ! Fortran programmer'.
        class(fortran_programmer_class), intent(inout) :: self

        print *, 'I am '//self%language//' programmer'
    end subroutine who_is
end module fortran_programmer_module

program we_love_fortran
    use fortran_programmer_module
    implicit none

    type(fortran_programmer_class) :: programmer

    call programmer%initialize()
    call programmer%who_is()
end program