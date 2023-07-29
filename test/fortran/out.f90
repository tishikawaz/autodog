module fortran_programmer_module
    ! module fortran_programmer_module
    !
    ! A module for creating and manipulating Fortran programmer objects.
    !
    ! Todo: None.
    implicit none

    private

    type, public, extends(programmer) :: fortran_programmer_class
        ! One-line abstract: A class representing a Fortran programmer.
        !
        ! Description: This class represents a Fortran programmer and extends the "programmer" class. It has a private attribute "language" which is an allocatable character array. The class provides two public procedures: "initialize" and "who_is".
        !
        ! Attributes:
        ! - language (character(:), allocatable): The programming language used by the Fortran programmer.
        private

        character(:),allocatable :: language

        contains

        procedure, public, pass(self) :: initialize
        procedure, public, pass(self) :: who_is
    end type fortran_programmer_class

    contains

    subroutine initialize(self, language)
        ! Write a one-line abstract of the function here.
        !
        ! This subroutine initializes a Fortran programmer object with an optional language argument.
        !
        ! A description of the function is written here.
        !
        ! This subroutine initializes a Fortran programmer object. It takes an optional language argument, which specifies the programming language the programmer is proficient in. If the language argument is provided, the subroutine allocates memory for the language attribute of the programmer object and assigns the value of the language argument to it. If the language argument is not provided, the subroutine allocates memory for the language attribute and assigns the value 'Fortran' to it.
        !
        ! Args:
        !     self (fortran_programmer_class): The Fortran programmer object to be initialized.
        !     language (character(:), allocatable, optional): The programming language the programmer is proficient in. Default is 'Fortran'.
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
        !     # Example 1: Initialize a Fortran programmer object with a language argument
        !     programmer = fortran_programmer_class()
        !     programmer%initialize(language='C')
        !
        !     # Example 2: Initialize a Fortran programmer object without a language argument
        !     programmer = fortran_programmer_class()
        !     programmer%initialize()
        !
        ! Note:
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
        ! Write a one-line abstract of the function here.
        !
        ! This subroutine prints the language of a Fortran programmer.
        !
        ! A description of the function is written here.
        !
        ! Args:
        !     self (fortran_programmer_class): an instance of the fortran_programmer_class
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
        !     The usage of the function is described here.
        !
        !     ```fortran
        !     type(fortran_programmer_class) :: programmer
        !     programmer%language = 'Fortran'
        !     call who_is(programmer)
        !     ```
        !     Output:
        !     ```
        !     I am Fortran programmer
        !     ```
        !
        ! Note:
        !     None
        class(fortran_programmer_class), intent(inout) :: self

        print *, 'I am '//self%language//' programmer'
    end subroutine who_is
end module fortran_programmer_module

program we_love_fortran
    ! Abstract: This Fortran code demonstrates the usage of a programmer module to initialize and identify a programmer.
    !
    ! Description:
    ! This code utilizes a programmer module to create an instance of a programmer class. The programmer class has two methods: initialize and who_is. The initialize method is called to initialize the programmer object, and the who_is method is called to identify the programmer. The code demonstrates the usage of these methods by calling them in the main program.
    use fortran_programmer_module
    implicit none

    type(fortran_programmer_class) :: programmer

    call programmer%initialize()
    call programmer%who_is()
end program