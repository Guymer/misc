PROGRAM main
    USE ISO_FORTRAN_ENV
    USE mod_safe,           ONLY:   sub_allocate_array

    IMPLICIT NONE

    ! Declare parameters ...
    INTEGER(kind = INT64), PARAMETER                                            :: n = 1024_INT64

    ! Declare variables ...
    REAL(kind = REAL64), ALLOCATABLE, DIMENSION(:, :)                           :: arr

    ! Allocate (8.0 MiB) array and populate it ...
    CALL sub_allocate_array(arr, "arr", n, n, .TRUE._INT8)
    arr = 1.0e0_REAL64

    WRITE(fmt = '(f9.1)', unit = OUTPUT_UNIT) SUM(arr)

    ! Clean up ...
    DEALLOCATE(arr)
END PROGRAM main
