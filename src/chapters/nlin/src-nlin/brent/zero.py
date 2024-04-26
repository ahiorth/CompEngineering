#! /usr/bin/env python
#
def f_01 ( x ):

#*****************************************************************************80
#
## F_01 evaluates sin ( x ) - x / 2.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    03 December 2016
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    Input, real X, the point at which F is to be evaluated.
#
#    Output, real VALUE, the value of the function at X.
#
  import numpy as np

  value = np.sin ( x ) - 0.5 * x

  return value

def f_02 ( x ):

#*****************************************************************************80
#
## F_02 evaluates 2*x-exp(-x).
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    03 December 2016
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    Input, real X, the point at which F is to be evaluated.
#
#    Output, real VALUE, the value of the function at X.
#
  import numpy as np

  value = 2.0 * x - np.exp ( - x )

  return value

def f_03 ( x ):

#*****************************************************************************80
#
## F_03 evaluates x*exp(-x).
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    03 December 2016
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    Input, real X, the point at which F is to be evaluated.
#
#    Output, real VALUE, the value of the function at X.
#
  import numpy as np

  value = x * np.exp ( - x )

  return value

def f_04 ( x ):

#*****************************************************************************80
#
## F_04 evaluates exp(x) - 1 / (100*x*x).
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    03 December 2016
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    Input, real X, the point at which F is to be evaluated.
#
#    Output, real VALUE, the value of the function at X.
#
  import numpy as np

  value = np.exp ( x ) - 1.0 / 100.0 / x / x

  return value

def f_05 ( x ):

#*****************************************************************************80
#
## F_05 evaluates (x+3)*(x-1)*(x-1).
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    03 December 2016
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    Input, real X, the point at which F is to be evaluated.
#
#    Output, real VALUE, the value of the function at X.
#
  value = ( x + 3.0 ) * ( x - 1.0 ) * ( x - 1.0 )

  return value

def zero ( a, b, machep, t, f ):

#*****************************************************************************80
#
## ZERO seeks the root of a function F(X) in an interval [A,B].
#
#  Discussion:
#
#    The interval [A,B] must be a change of sign interval for F.
#    That is, F(A) and F(B) must be of opposite signs.  Then
#    assuming that F is continuous implies the existence of at least
#    one value C between A and B for which F(C) = 0.
#
#    The location of the zero is determined to within an accuracy
#    of 6 * MACHEPS * abs ( C ) + 2 * T.
#
#    Thanks to Thomas Secretin for pointing out a transcription error in the
#    setting of the value of P, 11 February 2013.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    03 December 2016
#
#  Author:
#
#    Original FORTRAN77 version by Richard Brent
#    Python version by John Burkardt
#
#  Reference:
#
#    Richard Brent,
#    Algorithms for Minimization Without Derivatives,
#    Dover, 2002,
#    ISBN: 0-486-41998-3,
#    LC: QA402.5.B74.
#
#  Parameters:
#
#    Input, real A, B, the endpoints of the change of sign interval.
#
#    Input, real MACHEP, an estimate for the relative machine
#    precision.
#
#    Input, real T, a positive error tolerance.
#
#    Input, real value = F ( x ), the name of a user-supplied
#    function which evaluates the function whose zero is being sought.
#
#    Output, real VALUE, the estimated value of a zero of
#    the function F.
#

#
#  Make local copies of A and B.
#
  sa = a
  sb = b
  fa = f ( sa )
  fb = f ( sb )

  c = sa
  fc = fa
  e = sb - sa
  d = e

  while ( True ):

    if ( abs ( fc ) < abs ( fb ) ):

      sa = sb
      sb = c
      c = sa
      fa = fb
      fb = fc
      fc = fa

    tol = 2.0 * machep * abs ( sb ) + t
    m = 0.5 * ( c - sb )

    if ( abs ( m ) <= tol or fb == 0.0 ):
      break

    if ( abs ( e ) < tol or abs ( fa ) <= abs ( fb ) ):

      e = m
      d = e

    else:

      s = fb / fa

      if ( sa == c ):

        p = 2.0 * m * s
        q = 1.0 - s

      else:

        q = fa / fc
        r = fb / fc
        p = s * ( 2.0 * m * q * ( q - r ) - ( sb - sa ) * ( r - 1.0 ) )
        q = ( q - 1.0 ) * ( r - 1.0 ) * ( s - 1.0 )

      if ( 0.0 < p ):
        q = - q
      else:
        p = - p

      s = e
      e = d

      if ( 2.0 * p < 3.0 * m * q - abs ( tol * q ) and p < abs ( 0.5 * s * q ) ):
        d = p / q
      else:
        e = m
        d = e

    sa = sb
    fa = fb

    if ( tol < abs ( d ) ):
      sb = sb + d
    elif ( 0.0 < m ):
      sb = sb + tol
    else:
      sb = sb - tol

    fb = f ( sb )

    if ( ( 0.0 < fb and 0.0 < fc ) or ( fb <= 0.0 and fc <= 0.0 ) ):
      c = sa
      fc = fa
      e = sb - sa
      d = e

  value = sb

  return value

def zero_test ( ):

#*****************************************************************************80
#
## ZERO_TEST tests the Brent zero finding routine on all test functions.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    03 December 2016
#
#  Author:
#
#    John Burkardt
#
  import numpy as np

  print ( '' )
  print ( 'ZERO_TEST' )
  print ( '  ZERO seeks a root X of a function F()' )
  print ( '  in an interval [A,B].' )

  eps = 2.220446049250313E-016

  machep = np.sqrt ( eps )
  t = 10.0 * np.sqrt ( eps )

  a = 1.0
  b = 2.0
  x = zero ( a, b, machep, t, f_01 )
  print ( '' )
  print ( '  f_01(x) = sin ( x ) - x / 2' )
  print ( '  f_01(%g) = %g' % ( x, f_01 ( x ) ) )

  a = 0.0
  b = 1.0
  x = zero ( a, b, machep, t, f_02 )
  print ( '' )
  print ( '  f_02(x) = 2 * x - exp ( - x )' )
  print ( '  f_02(%g) = %g' % ( x, f_02 ( x ) ) )

  a = -1.0
  b =  0.5
  x = zero ( a, b, machep, t, f_03 )
  print ( '' )
  print ( '  f_03(x) = x * exp ( - x )' )
  print ( '  f_03(%g) = %g' % ( x, f_03 ( x ) ) )

  a =  0.0001
  b =  20.0
  x = zero ( a, b, machep, t, f_04 )
  print ( '' )
  print ( '  f_04(x) = exp ( x ) - 1 / ( 100 * x * x )' )
  print ( '  f_04(%g) = %g' % ( x, f_04 ( x ) ) )

  a = -5.0
  b =  2.0
  x = zero ( a, b, machep, t, f_05 )
  print ( '' )
  print ( '  f_05(x) = (x+3) * (x-1) * (x-1)' )
  print ( '  f_05(%g) = %g' % ( x, f_05 ( x ) ) )
#
#  Terminate.
#
  print ( '' )
  print ( 'ZERO_TEST' )
  print ( '  Normal end of execution.' )
  return

def timestamp ( ):

#*****************************************************************************80
#
## TIMESTAMP prints the date as a timestamp.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license. 
#
#  Modified:
#
#    06 April 2013
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    None
#
  import time

  t = time.time ( )
  print ( time.ctime ( t ) )

  return None

def timestamp_test ( ):

#*****************************************************************************80
#
## TIMESTAMP_TEST tests TIMESTAMP.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license. 
#
#  Modified:
#
#    03 December 2014
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    None
#
  import platform

  print ( '' )
  print ( 'TIMESTAMP_TEST:' )
  print ( '  Python version: %s' % ( platform.python_version ( ) ) )
  print ( '  TIMESTAMP prints a timestamp of the current date and time.' )
  print ( '' )

  timestamp ( )
#
#  Terminate.
#
  print ( '' )
  print ( 'TIMESTAMP_TEST:' )
  print ( '  Normal end of execution.' )
  return

if ( __name__ == '__main__' ):
  timestamp ( )
  zero_test ( )
  timestamp ( )

