module fortran_programmer_module
    implicit none

    private

    type, public :: fortran_programmer_class
        ! Fortran Programmer Class
        !
        ! This class defines a Fortran programmer with the following attributes:
        ! - language: a character string representing the programming language used by the
        ! programmer
        !
        ! The class has the following methods:
        ! - initialize: initializes the language attribute
        ! - who_is: prints a message identifying the programmer and their language
        !
        ! Usage:
        !     programmer = fortran_programmer_class()
        !     programmer%initialize("Fortran")
        !     programmer%who_is()
        !
        ! Author: [Your Name]
        ! Date: [Date]
        private

        character(:),allocatable :: language

        contains

        procedure, public, pass(self) :: initialize
        procedure, public, pass(self) :: who_is
    end type fortran_programmer_class

    contains

    subroutine initialize(self, language)
        ! Initializes the Fortran programmer object with a specified language or defaults to
        ! 'Fortran'.
        !
        ! Parameters:
        !     - self: an instance of the fortran_programmer_class
        !     - language (optional): a character string specifying the language to initialize the
        ! object with
        !
        ! Returns:
        !     None
        class(fortran_programmer_class), intent(inout) :: self
        character(:), allocatable, intent(in), optional :: language

        if (present(language)) then
            allocate(self%language, source = language)
            return
        end if
        allocate(self%language, source = 'Fortran')
    end subroutine initialize

    subroutine who_is(self)
        ! Prints a message indicating the programming language of the Fortran programmer.
        !
        ! Parameters:
        ! -----------
        ! self : object
        !     An instance of the fortran_programmer_class.
        !
        ! Returns:
        ! --------
        ! None
        !
        ! Example:
        ! --------
        ! >>> programmer = fortran_programmer_class()
        ! >>> programmer%language = 'Fortran'
        ! >>> programmer%who_is()
        ! I am Fortran programmer
        class(fortran_programmer_class), intent(inout) :: self

        print *, 'I am '//self%language//' programmer'
    end subroutine who_is
end module fortran_programmer_module

program we_love_fortran
    ! This program demonstrates the use of the Fortran Programmer Module to create an instance
    ! of the Fortran Programmer Class and call its methods.
    !
    ! The Fortran Programmer Module is imported and used to create an instance of the Fortran
    ! Programmer Class. The programmer object is then initialized using the initialize()
    ! method and the who_is() method is called to print the name of the programmer.
    !
    ! Args:
    !     None
    !
    ! Returns:
    !     None
    use fortran_programmer_module
    implicit none

    type(fortran_programmer_class) :: programmer

    call programmer%initialize()
    call programmer%who_is()
end program