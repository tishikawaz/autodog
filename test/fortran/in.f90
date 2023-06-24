module fortran_programmer_module
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
        class(fortran_programmer_class), intent(inout) :: self
        character(:), allocatable, intent(in), optional :: language

        if (present(language)) then
            allocate(self%language, source = language)
            return
        end if
        allocate(self%language, source = 'Fortran')
    end subroutine initialize

    subroutine who_is(self)
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