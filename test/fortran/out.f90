module fortran_programmer_module
    ! <Write a one-line abstract of the module here>
    ! This Fortran module defines a class for a programmer specializing in Fortran programming.
    !
    ! <A description of the module is written here>
    ! The "fortran_programmer_module" module defines a derived type called "fortran_programmer_class" which extends the base type "programmer". This derived type has a private component "language" which is an allocatable character variable. The module also contains two procedures, "initialize" and "who_is", which are public and can be accessed outside the module.
    !
    ! The "initialize" subroutine initializes the "language" component of the "fortran_programmer_class" object. It takes an optional input argument "language" which specifies the programming language. If the "language" argument is present, the subroutine allocates and assigns the value of "language" to the "language" component. If the "language" argument is not present, the subroutine allocates and assigns the default value 'Fortran' to the "language" component.
    !
    ! The "who_is" subroutine prints a message indicating the programming language of the "fortran_programmer_class" object.
    !
    ! Todo:    * Todo is written here.
    !     (If the module doesn't have todo, this item should not be written.)
    !     - None
    implicit none

    private

    type, public, extends(programmer) :: fortran_programmer_class
        ! <Write a one-line abstract of the class here>
        ! This Fortran type represents a programmer who specializes in the Fortran programming language.
        !
        ! <A description of the class is written here>
        ! The `fortran_programmer_class` type is a derived type in Fortran that extends the `programmer` type. It represents a programmer who specializes in the Fortran programming language. The type has a private attribute `language` which is an allocatable character array. It also contains two public procedures: `initialize` and `who_is`.
        !
        ! Attributes:
        !     language (character(:), allocatable): The programming language the programmer specializes in.
        !
        ! Procedures:
        !     initialize: A public procedure that initializes the `fortran_programmer_class` object.
        !     who_is: A public procedure that prints information about the programmer.
        private

        character(:),allocatable :: language

        contains

        procedure, public, pass(self) :: initialize
        procedure, public, pass(self) :: who_is
    end type fortran_programmer_class

    contains

    subroutine initialize(self, language)
        ! <Initialize the Fortran programmer object with an optional language argument>
        !
        ! This subroutine initializes a Fortran programmer object with an optional language argument. If the language argument is provided, the object's language attribute is set to the provided language. Otherwise, the object's language attribute is set to 'Fortran'.
        !
        ! Args:
        !     self (fortran_programmer_class): The Fortran programmer object to be initialized.
        !     language (character(:), allocatable, optional): The language to set as the object's language attribute. Default is 'Fortran'.
        !
        ! Note:
        !     This subroutine assumes that the fortran_programmer_class has a language attribute.
        !
        ! Examples:
        !     # Example 1: Initialize with default language
        !     programmer = fortran_programmer_class()
        !     programmer.initialize()
        !     print(programmer.language)  # Output: 'Fortran'
        !
        !     # Example 2: Initialize with a specific language
        !     programmer = fortran_programmer_class()
        !     programmer.initialize(language='C')
        !     print(programmer.language)  # Output: 'C'
        class(fortran_programmer_class), intent(inout) :: self
        character(:), allocatable, intent(in), optional :: language

        if (present(language)) then
            allocate(self%language, source = language)
            return
        end if
        allocate(self%language, source = 'Fortran')
    end subroutine initialize

    subroutine who_is(self)
        ! <Write a one-line abstract of the function here>
        !
        ! This subroutine prints the programming language of a Fortran programmer.
        !
        ! Args:
        !     self (class(fortran_programmer_class), intent(inout)): An instance of the fortran_programmer_class.
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
        !     ```
        !     program main
        !         type :: fortran_programmer_class
        !             character(len=10) :: language
        !         end type fortran_programmer_class
        !
        !         type(fortran_programmer_class) :: programmer
        !
        !         programmer%language = 'Fortran'
        !         call who_is(programmer) ! Output: "I am Fortran programmer"
        !     end program main
        !     ```
        !
        ! Note:
        !     None
        class(fortran_programmer_class), intent(inout) :: self

        print *, 'I am '//self%language//' programmer'
    end subroutine who_is
end module fortran_programmer_module

program we_love_fortran
    ! <Write a one-line abstract of the application here>
    !
    ! This Fortran code is a simple program that demonstrates the usage of a module and a class. It initializes an instance of the `fortran_programmer_class` and calls the `initialize` and `who_is` methods of the class.
    !
    ! A description of the application, such as description of usage, I/O, and interfaces, is written here.
    use fortran_programmer_module
    implicit none

    type(fortran_programmer_class) :: programmer

    call programmer%initialize()
    call programmer%who_is()
end program