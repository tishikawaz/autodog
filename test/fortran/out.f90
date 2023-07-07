module fortran_programmer_module
    ! *******************************************************************************
    ! Module Name: fortran_programmer_module
    !
    ! Description: This module defines a Fortran programmer class that extends the
    ! programmer class. It provides methods to initialize the programmer
    ! object and print the programmer's language.
    !
    ! Public Types:
    ! - fortran_programmer_class: A derived type that extends the programmer class.
    !
    ! Public Procedures:
    ! - initialize: Initializes the programmer object with a specified language.
    ! - who_is: Prints the programmer's language.
    !
    ! Private Types:
    ! - None
    !
    ! Private Procedures:
    ! - None
    !
    ! *******************************************************************************
    implicit none

    private

    type, public, extends(programmer) :: fortran_programmer_class
        ! Fortran Programmer Class
        ! This class represents a Fortran programmer. It extends the `programmer` class.
        ! Attributes:
        ! - language (character(:), allocatable): The programming language used by the
        ! programmer.
        ! Methods:
        ! - initialize(self): Initializes the Fortran programmer object.
        ! - who_is(self): Prints information about the Fortran programmer.
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
        ! It takes an optional `language` argument to set the programming language of the
        ! programmer.
        ! If `language` is provided, it assigns it to `self%language`.
        ! If `language` is not provided, it assigns the default value 'Fortran' to
        ! `self%language`.
        class(fortran_programmer_class), intent(inout) :: self
        character(:), allocatable, intent(in), optional :: language

        if (present(language)) then
            allocate(self%language, source = language)
            return
        end if
        allocate(self%language, source = 'Fortran')
    end subroutine initialize

    subroutine who_is(self)
        ! This subroutine prints the programming language of the given programmer object.
        !
        ! Parameters:
        ! self: The programmer object whose language will be printed.
        !
        ! Output:
        ! None.
        !
        ! Example usage:
        ! call who_is(programmer_object)
        !
        ! Note:
        ! The programmer object must be of type fortran_programmer_class.
        class(fortran_programmer_class), intent(inout) :: self

        print *, 'I am '//self%language//' programmer'
    end subroutine who_is
end module fortran_programmer_module

program we_love_fortran
    ! """
    ! This program demonstrates the usage of the `fortran_programmer_module` module
    ! and the `fortran_programmer_class` type.
    ! The program creates an instance of the `fortran_programmer_class` type named
    ! `programmer` and calls two methods on it: `initialize()` and `who_is()`.
    ! Usage:
    !     - Make sure the `fortran_programmer_module` module is available.
    !     - Compile and run the program.
    ! Author: [Your Name]
    ! Date: [Current Date]
    ! """
    use fortran_programmer_module
    implicit none

    type(fortran_programmer_class) :: programmer

    call programmer%initialize()
    call programmer%who_is()
end program