module fortran_programmer_module
    ! Fortran Programmer Module
    !
    ! This module defines a Fortran programmer class that extends the "programmer" class. It includes methods to initialize the programmer object and to print the programmer's language.
    !
    ! Todo: None
    implicit none

    private

    type, public, extends(programmer) :: fortran_programmer_class
        ! Fortran Programmer Class
        !
        ! This class represents a Fortran programmer.
        !
        ! Attributes:
        !     language (character(:), allocatable): The programming language the programmer is proficient in.
        !
        ! Methods:
        !     initialize(self): Initializes the Fortran programmer object.
        !     who_is(self): Prints information about the Fortran programmer.
        private

        character(:),allocatable :: language

        contains

        procedure, public, pass(self) :: initialize
        procedure, public, pass(self) :: who_is
    end type fortran_programmer_class

    contains

    subroutine initialize(self, language)
        ! ```
        ! initialize(self, language)
        !
        ! This subroutine initializes the language attribute of a Fortran programmer object.
        !
        ! Args:
        !     self (fortran_programmer_class): The Fortran programmer object to be initialized.
        !     language (character(:), allocatable, optional): The language to be assigned to the language attribute. If not provided, the default value is 'Fortran'.
        !
        ! Note:
        !     This subroutine assumes that the fortran_programmer_class has a language attribute.
        !
        ! Examples:
        !     # Create a Fortran programmer object
        !     programmer = fortran_programmer_class()
        !
        !     # Initialize the language attribute with 'Fortran'
        !     programmer%initialize()
        !
        !     # Initialize the language attribute with 'Python'
        !     programmer%initialize('Python')
        ! ```
        class(fortran_programmer_class), intent(inout) :: self
        character(:), allocatable, intent(in), optional :: language

        if (present(language)) then
            allocate(self%language, source = language)
            return
        end if
        allocate(self%language, source = 'Fortran')
    end subroutine initialize

    subroutine who_is(self)
        ! one-line description:
        ! This subroutine prints the programming language of a Fortran programmer.
        !
        ! Description:
        ! The subroutine "who_is" prints the programming language of a Fortran programmer. It takes a "self" argument of type "fortran_programmer_class" which is a class representing a Fortran programmer. The subroutine prints the message "I am [language] programmer" where [language] is the value of the "language" attribute of the "self" object.
        !
        ! Args:
        !     self (fortran_programmer_class): The Fortran programmer object.
        !
        ! Returns:
        !     None
        !
        ! Raises:
        !     None
        !
        ! Yields:
        !     None
        !
        ! Examples:
        !     Example usage of the "who_is" subroutine:
        !
        !     ```
        !     type(fortran_programmer_class) :: programmer
        !     programmer%language = 'Fortran'
        !     call who_is(programmer)
        !     ```
        !
        !     Output:
        !     I am Fortran programmer
        !
        ! Note:
        !     None
        class(fortran_programmer_class), intent(inout) :: self

        print *, 'I am '//self%language//' programmer'
    end subroutine who_is
end module fortran_programmer_module

program we_love_fortran
    ! one-line description:
    ! This Fortran code demonstrates the usage of a programmer class from a custom module.
    !
    ! description:
    ! The code begins by declaring a program called "we_love_fortran". It then uses a custom module called "fortran_programmer_module" and sets the implicit none directive.
    !
    ! Next, a variable of type "fortran_programmer_class" called "programmer" is declared.
    !
    ! The code then calls the "initialize" subroutine of the "programmer" object to initialize it.
    !
    ! Finally, the code calls the "who_is" subroutine of the "programmer" object to display information about the programmer.
    !
    ! Overall, this code showcases the usage of a programmer class from a custom module in Fortran.
    use fortran_programmer_module
    implicit none

    type(fortran_programmer_class) :: programmer

    call programmer%initialize()
    call programmer%who_is()
end program