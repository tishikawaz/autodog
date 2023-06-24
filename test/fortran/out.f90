module fortran_programmer_module
    ! This Fortran code defines a module named `fortran_programmer_module`
    ! that contains a derived type named `fortran_programmer_class`. This
    ! derived type extends another derived type named `programmer`. The
    ! `fortran_programmer_class` contains a character variable named
    ! `language` and two procedures named `initialize` and `who_is`.
    ! 
    ! The `initialize` procedure initializes the `language` variable of the
    ! `fortran_programmer_class`. It takes two arguments, `self` and
    ! `language`. The `self` argument is of the `fortran_programmer_class`
    ! type and is passed by reference. The `language` argument is an optional
    ! character variable that is passed by value. If the `language` argument
    ! is present, the `language` variable of the `fortran_programmer_class` is
    ! allocated and initialized with the value of the `language` argument. If
    ! the `language` argument is not present, the `language` variable of the
    ! `fortran_programmer_class` is allocated and initialized with the value
    ! `'Fortran'`.
    ! 
    ! The `who_is` procedure prints a message to the standard output that
    ! indicates the language of the programmer. It takes one argument, `self`,
    ! which is of the `fortran_programmer_class` type and is passed by
    ! reference. The message printed to the standard output is `'I am
    ! '//self%language//' programmer'`.
    ! 
    ! Overall, this code defines a derived type that represents a Fortran
    ! programmer and provides procedures to initialize and print information
    ! about the programmer.
    implicit none

    private

    type, public, extends(programmer) :: fortran_programmer_class
        ! Fortran Programmer Class
        ! 
        ! This class is a subclass of the Programmer class and represents a
        ! programmer who specializes in the Fortran programming language. It has
        ! two public methods:
        ! 
        ! Methods:
        ! ---------
        ! initialize(self)
        !     Initializes the Fortran programmer object by setting the language
        !     attribute to 'Fortran'.
        ! 
        ! who_is(self)
        !     Prints out the name and language of the Fortran programmer object.
        ! 
        ! Attributes:
        ! -----------
        ! language : str
        !     The programming language that the Fortran programmer specializes in.
        ! 
        private

        character(:),allocatable :: language

        contains

        procedure, public, pass(self) :: initialize
        procedure, public, pass(self) :: who_is
    end type fortran_programmer_class

    contains

    subroutine initialize(self, language)
        ! Initializes the Fortran programmer object with a specified language or
        ! defaults to 'Fortran'.
        ! 
        ! Parameters:
        !     self (fortran_programmer_class): The Fortran programmer object to be
        !     initialized.
        !     language (optional, str): The language to initialize the object
        !     with. Defaults to 'Fortran' if not provided.
        ! 
        ! Returns:
        !     None
        ! 
        ! Example:
        !     >>> programmer = fortran_programmer_class()
        !     >>> programmer.initialize('Python')
        !     >>> print(programmer.language)
        !     Python
        class(fortran_programmer_class), intent(inout) :: self
        character(:), allocatable, intent(in), optional :: language

        if (present(language)) then
            allocate(self%language, source = language)
            return
        end if
        allocate(self%language, source = 'Fortran')
    end subroutine initialize

    subroutine who_is(self)
        ! Prints the programming language of the Fortran programmer.
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
    ! This program demonstrates the use of a Fortran module and class to
    ! create a programmer object and call its methods.
    ! 
    ! The program imports the "fortran_programmer_module" module and creates
    ! an instance of the "fortran_programmer_class" class named "programmer".
    ! The "initialize" method of the class is called to initialize the
    ! programmer object. The "who_is" method of the class is then called to
    ! print out the name of the programmer.
    ! 
    ! This program can be used as a template for creating and using Fortran
    ! modules and classes in other programs.
    use fortran_programmer_module
    implicit none

    type(fortran_programmer_class) :: programmer

    call programmer%initialize()
    call programmer%who_is()
end program