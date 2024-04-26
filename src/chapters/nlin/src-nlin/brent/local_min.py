#! /usr/bin/env python
#
def g_01 ( x ):

#*****************************************************************************80
#
## G_01 evaluates (x-2)^2 + 1.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    14 April 2008
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
  value = ( x - 2.0 ) * ( x - 2.0 ) + 1.0

  return value

def g_02 ( x ):

#*****************************************************************************80
#
## G_02 evaluates x^2 + exp ( - x ).
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    14 April 2008
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

  value = x * x + np.exp ( - x )

  return value

def g_03 ( x ):

#*****************************************************************************80
#
## G_03 evaluates x^4+2x^2+x+3.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    14 April 2008
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
  value = ( ( x * x + 2.0 ) * x + 1.0 ) * x + 3.0

  return value

def g_04 ( x ):

#*****************************************************************************80
#
## G_04 evaluates exp(x)+1/(100X)
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    14 April 2008
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

  value = np.exp ( x ) + 0.01 / x

  return value

def g_05 ( x ):

#*****************************************************************************80
#
## G_05 evaluates exp(x) - 2x + 1/(100x) - 1/(1000000x^2)
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    14 April 2008
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

  value = np.exp ( x ) - 2.0 * x + 0.01 / x - 0.000001 / x / x

  return value

def g_06 ( x ):

#*****************************************************************************80
#
## G_06 evaluates - x * sin(10 pi x ) - 1.0
#
#  Discussion:
#
#    There is a local minimum between 1.80 and 1.90 at about
#    1.850547466.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    19 January 2013
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

  value = - x * np.sin ( 10.0 * np.pi * x ) - 1.0

  return value

def local_min ( a, b, epsi, t, f ):

#*****************************************************************************80
#
## LOCAL_MIN seeks a local minimum of a function F(X) in an interval [A,B].
#
#  Discussion:
#
#    The method used is a combination of golden section search and
#    successive parabolic interpolation.  Convergence is never much slower
#    than that for a Fibonacci search.  If F has a continuous second
#    derivative which is positive at the minimum (which is not at A or
#    B), then convergence is superlinear, and usually of the order of
#    about 1.324....
#
#    The values EPSI and T define a tolerance TOL = EPSI * abs ( X ) + T.
#    F is never evaluated at two points closer than TOL.
#
#    If F is a unimodal function and the computed values of F are always
#    unimodal when separated by at least SQEPS * abs ( X ) + (T/3), then
#    LOCAL_MIN approximates the abscissa of the global minimum of F on the
#    interval [A,B] with an error less than 3*SQEPS*abs(LOCAL_MIN)+T.
#
#    If F is not unimodal, then LOCAL_MIN may approximate a local, but
#    perhaps non-global, minimum to the same accuracy.
#
#    Thanks to Jonathan Eggleston for pointing out a correction to the 
#    golden section step, 01 July 2013.
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
#    Original FORTRAN77 version by Richard Brent.
#    Python version by John Burkardt.
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
#    Input, real A, B, the endpoints of the interval.
#
#    Input, real EPSI, a positive relative error tolerance.
#    EPSI should be no smaller than twice the relative machine precision,
#    and preferably not much less than the square root of the relative
#    machine precision.
#
#    Input, real T, a positive absolute error tolerance.
#
#    Input, function value = F ( x ), the name of a user-supplied
#    function whose local minimum is being sought.
#
#    Output, real X, the estimated value of an abscissa
#    for which F attains a local minimum value in [A,B].
#
#    Output, real FX, the value F(X).
#
  import numpy as np
#
#  C is the square of the inverse of the golden ratio.
#
  c = 0.5 * ( 3.0 - np.sqrt ( 5.0 ) )

  sa = a
  sb = b
  x = sa + c * ( b - a )
  w = x
  v = w
  e = 0.0
  fx = f ( x )
  fw = fx
  fv = fw

  while ( True ):

    m = 0.5 * ( sa + sb )
    tol = epsi * abs ( x ) + t
    t2 = 2.0 * tol
#
#  Check the stopping criterion.
#
    if ( abs ( x - m ) <= t2 - 0.5 * ( sb - sa ) ):
      break
#
#  Fit a parabola.
#
    r = 0.0
    q = r
    p = q

    if ( tol < abs ( e ) ):

      r = ( x - w ) * ( fx - fv )
      q = ( x - v ) * ( fx - fw )
      p = ( x - v ) * q - ( x - w ) * r
      q = 2.0 * ( q - r )

      if ( 0.0 < q ):
        p = - p

      q = abs ( q )

      r = e
      e = d

    if ( abs ( p ) < abs ( 0.5 * q * r ) and \
         q * ( sa - x ) < p and \
         p < q * ( sb - x ) ):
#
#  Take the parabolic interpolation step.
#
      d = p / q
      u = x + d
#
#  F must not be evaluated too close to A or B.
#
      if ( ( u - sa ) < t2 or ( sb - u ) < t2 ):

        if ( x < m ):
          d = tol
        else:
          d = - tol
#
#  A golden-section step.
#
    else:

      if ( x < m ):
        e = sb - x
      else:
        e = sa - x

      d = c * e
#
#  F must not be evaluated too close to X.
#
    if ( tol <= abs ( d ) ):
      u = x + d
    elif ( 0.0 < d ):
      u = x + tol
    else:
      u = x - tol

    fu = f ( u )
#
#  Update A, B, V, W, and X.
#
    if ( fu <= fx ):

      if ( u < x ):
        sb = x
      else:
        sa = x

      v = w
      fv = fw
      w = x
      fw = fx
      x = u
      fx = fu

    else:

      if ( u < x ):
        sa = u
      else:
        sb = u

      if ( fu <= fw or w == x ):
        v = w
        fv = fw
        w = u
        fw = fu
      elif ( fu <= fv or v == x or v == w ):
        v = u
        fv = fu

  return x, fx

def local_min_test ( ):

#*****************************************************************************80
#
## LOCAL_MIN_TEST tests LOCAL_MIN.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    30 November 2016
#
#  Author:
#
#    John Burkardt
#
  import numpy as np
  import platform

  print ( '' )
  print ( 'LOCAL_MIN_TEST' )
  print ( '  Python version: %s' % ( platform.python_version ( ) ) )
  print ( '  LOCAL_MIN seeks a local minimizer of a function F(X)' )
  print ( '  in an interval [A,B].' )

  eps = 2.220446049250313E-016

  epsi = np.sqrt ( eps )
  t = 10.0 * np.sqrt ( eps )

  a = 0.0
  b = 3.141592653589793
  x, fx = local_min ( a, b, epsi, t, g_01 )
  print ( '' )
  print ( '  g_01(x) = ( x - 2 ) * ( x - 2 ) + 1' )
  print ( '  g_01(%g) = %g' % ( x, fx ) )

  a = 0.0
  b = 1.0
  x, fx = local_min ( a, b, epsi, t, g_02 )
  print ( '' )
  print ( '  g_02(x) = x * x + exp ( - x )' )
  print ( '  g_02(%g) = %g' % ( x, fx ) )

  a = -2.0
  b =  2.0
  x, fx = local_min ( a, b, epsi, t, g_03 )
  print ( '' )
  print ( '  g_03(x) = x^4 + 2x^2 + x + 3' )
  print ( '  g_03(%g) = %g' % ( x, fx ) )

  a =  0.0001
  b =  1.0
  x, fx = local_min ( a, b, epsi, t, g_04 )
  print ( '' )
  print ( '  g_04(x) = exp ( x ) + 1 / ( 100 x )' )
  print ( '  g_04(%g) = %g' % ( x, fx ) )

  a =  0.0002
  b = 2.0
  x, fx = local_min ( a, b, epsi, t, g_05 )
  print ( '' )
  print ( '  g_05(x) = exp ( x ) - 2x + 1/(100x) - 1/(1000000x^2)' )
  print ( '  g_05(%g) = %g' % ( x, fx ) )

  a = 1.8
  b = 1.9
  x, fx = local_min ( a, b, epsi, t, g_06 )
  print ( '' )
  print ( '  g_06(x) = - x sin ( 10 pi x ) - 1' )
  print ( '  g_06(%g) = %g' % ( x, fx ) )
#
#  Terminate.
#
  print ( '' )
  print ( 'LOCAL_MIN_TEST' )
  print ( '  Normal end of execution.' )
  return

def test_example ( a, b, t, f, title ):

#*****************************************************************************80
#
## TEST_EXAMPLE tests LOCAL_MIN on one test function.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    30 November 2016
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    Input, real A, B, the endpoints of the interval.
#
#    Input, real T, a positive absolute error tolerance.
#
#    Input, real value = F ( x ), the name of a user-supplied
#    function whose local minimum is being sought.
#
#    Input, string TITLE, a title for the problem.
#
  print ( '' )
  print ( '  %s' % ( title ) )
  print ( '' )
  print ( '  Step      X                          F(X)' )
  print ( '' )

  value = f ( arg )
  print ( '  %4d  %24.16e  %24.16e' % ( a, value ) )

  value = f ( arg )
  print ( '  %4d  %24.16e  %24.16e' % ( b, value ) )

  x, fx = local_min ( a2, b2, status, value )

  return

def r8_sign ( x ):

#*****************************************************************************80
#
## R8_SIGN returns the sign of an R8.
#
#  Discussion:
#
#    The value is +1 if the number is positive or zero, and it is -1 otherwise.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    03 June 2013
#
#  Author:
#
#    John Burkardt
#
#  Parameters:
#
#    Input, real X, the number whose sign is desired.
#
#    Output, real VALUE, the sign of X.
#
  if ( x < 0.0 ):
    value = -1.0
  else:
    value = +1.0
 
  return value

def r8_sign_test ( ):

#*****************************************************************************80
#
## R8_SIGN_TEST tests R8_SIGN.
#
#  Licensing:
#
#    This code is distributed under the GNU LGPL license.
#
#  Modified:
#
#    28 September 2014
#
#  Author:
#
#    John Burkardt
#
  import numpy as np
  import platform

  test_num = 5

  r8_test = np.array ( [ -1.25, -0.25, 0.0, +0.5, +9.0 ] )

  print ( '' )
  print ( 'R8_SIGN_TEST' )
  print ( '  Python version: %s' % ( platform.python_version ( ) ) )
  print ( '  R8_SIGN returns the sign of an R8.' )
  print ( '' )
  print ( '     R8     R8_SIGN(R8)' )
  print ( '' )

  for test in range ( 0, test_num ):
    r8 = r8_test[test]
    s = r8_sign ( r8 )
    print ( '  %8.4f  %8.0f' % ( r8, s ) )
#
#  Terminate.
#
  print ( '' )
  print ( 'R8_SIGN_TEST' )
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
  local_min_test ( )
  timestamp ( )

