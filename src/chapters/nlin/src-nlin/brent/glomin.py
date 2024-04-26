#! /usr/bin/env python
#
def h_01 ( x ):

#*****************************************************************************80
#
## H_01 evaluates 2 - x.
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
  value = 2.0 - x

  return value

def h_02 ( x ):

#*****************************************************************************80
#
## H_02 evaluates x^2.
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
  value = x * x

  return value

def h_03 ( x ):

#*****************************************************************************80
#
## H_03 evaluates x^3+x^2.
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
  value = x * x * ( x + 1.0 )

  return value

def h_04 ( x ):

#*****************************************************************************80
#
## H_04 evaluates ( x + sin ( x ) ) * exp ( - x * x ).
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

  value = ( x + np.sin ( x ) ) * np.exp ( - x * x )

  return value

def h_05 ( x ):

#*****************************************************************************80
#
## H_05 evaluates ( x - sin ( x ) ) * exp ( - x * x ).
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

  value = ( x - np.sin ( x ) ) * np.exp ( - x * x )

  return value

def glomin ( a, b, c, m, machep, e, t, f ):

#*****************************************************************************80
#
## GLOMIN seeks a global minimum of a function F(X) in an interval [A,B].
#
#  Discussion:
#
#    This function assumes that F(X) is twice continuously differentiable
#    over [A,B] and that F''(X) <= M for all X in [A,B].
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
#    It must be the case that A < B.
#
#    Input, real C, an initial guess for the global
#    minimizer.  If no good guess is known, C = A or B is acceptable.
#
#    Input, real M, the bound on the second derivative.
#
#    Input, real MACHEP, an estimate for the relative machine
#    precision.
#
#    Input, real E, a positive tolerance, a bound for the
#    absolute error in the evaluation of F(X) for any X in [A,B].
#
#    Input, real T, a positive error tolerance.
#
#    Input, function value = F ( x ), the name of a user-supplied
#    function whose global minimum is being sought.
#
#    Output, real X, the estimated value of the abscissa
#    for which F attains its global minimum value in [A,B].
#
#    Output, real FX, the value F(X).
#
  import numpy as np

  a0 = b
  x = a0
  a2 = a
  y0 = f ( b )
  yb = y0
  y2 = f ( a )
  y = y2

  if ( y0 < y ):
    y = y0
  else:
    x = a

  if ( m <= 0.0 or b <= a ):
    fx = y
    return x, fx

  m2 = 0.5 * ( 1.0 + 16.0 * machep ) * m

  if ( c <= a or b <= c ):
    sc = 0.5 * ( a + b )
  else:
    sc = c

  y1 = f ( sc )
  k = 3
  d0 = a2 - sc
  h = 9.0 / 11.0

  if ( y1 < y ):
    x = sc
    y = y1

  while ( True ):

    d1 = a2 - a0
    d2 = sc - a0
    z2 = b - a2
    z0 = y2 - y1
    z1 = y2 - y0
    r = d1 * d1 * z0 - d0 * d0 * z1
    p = r
    qs = 2.0 * ( d0 * z1 - d1 * z0 )
    q = qs

    if ( k < 1000000 or y2 <= y ):

      while ( True ):

        if ( q * ( r * ( yb - y2 ) + z2 * q * ( ( y2 - y ) + t ) ) < \
          z2 * m2 * r * ( z2 * q - r ) ):
          a3 = a2 + r / q
          y3 = f ( a3 )

          if ( y3 < y ):
            x = a3
            y = y3

        k = ( ( 1611 * k ) % 1048576 )
        q = 1.0
        r = ( b - a ) * 0.00001 * float ( k )

        if ( z2 <= r ):
          break

    else:

      k = ( ( 1611 * k ) % 1048576 )
      q = 1.0
      r = ( b - a ) * 0.00001 * float ( k )

      while ( r < z2 ):

        if ( q * ( r * ( yb - y2 ) + z2 * q * ( ( y2 - y ) + t ) ) < \
          z2 * m2 * r * ( z2 * q - r ) ):
          a3 = a2 + r / q
          y3 = f ( a3 )

          if ( y3 < y ):
            x = a3
            y = y3

        k = ( ( 1611 * k ) % 1048576 )
        q = 1.0
        r = ( b - a ) * 0.00001 * float ( k )

    r = m2 * d0 * d1 * d2
    s = np.sqrt ( ( ( y2 - y ) + t ) / m2 )
    h = 0.5 * ( 1.0 + h )
    p = h * ( p + 2.0 * r * s )
    q = q + 0.5 * qs
    r = - 0.5 * ( d0 + ( z0 + 2.01 * e ) / ( d0 * m2 ) )

    if ( r < s or d0 < 0.0 ):
      r = a2 + s
    else:
      r = a2 + r

    if ( 0.0 < p * q ):
      a3 = a2 + p / q
    else:
      a3 = r

    while ( True ):

      a3 = max ( a3, r )

      if ( b <= a3 ):
        a3 = b
        y3 = yb
      else:
        y3 = f ( a3 )

      if ( y3 < y ):
        x = a3
        y = y3

      d0 = a3 - a2

      if ( a3 <= r ):
        break

      p = 2.0 * ( y2 - y3 ) / ( m * d0 )

      if ( ( 1.0 + 9.0 * machep ) * d0 <= abs ( p ) ):
        break

      if ( 0.5 * m2 * ( d0 * d0 + p * p ) <= ( y2 - y ) + ( y3 - y ) + 2.0 * t ):
        break

      a3 = 0.5 * ( a2 + a3 )
      h = 0.9 * h

    if ( b <= a3 ):
      break

    a0 = sc
    sc = a2
    a2 = a3
    y0 = y1
    y1 = y2
    y2 = y3

  fx = y
 
  return x, fx

def glomin_test ( ):

#*****************************************************************************80
#
## GLOMIN_TEST tests the Brent global minimizer on all test functions.
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
  print ( 'GLOMIN_TEST' )
  print ( '  Test the Brent GLOMIN routine, which seeks' )
  print ( '  a global minimizer of a function F(X)' )
  print ( '  in an interval [A,B],' )
  print ( '  given some upper bound M for F".' )

  machep = 2.220446049250313E-016
  e = np.sqrt ( machep )
  t = np.sqrt ( machep )

  a = 7.0
  b = 9.0
  c = ( a + b ) / 2.0
  m = 0.0

  example_test ( a, b, c, m, machep, e, t, h_01, 'h_01(x) = 2 - x' )

  a = 7.0
  b = 9.0
  c = ( a + b ) / 2.0
  m = 100.0

  example_test ( a, b, c, m, machep, e, t, h_01, 'h_01(x) = 2 - x' )

  a = -1.0
  b = +2.0
  c = ( a + b ) / 2.0
  m = 2.0

  example_test ( a, b, c, m, machep, e, t, h_02, 'h_02(x) = x * x' )

  a = -1.0
  b = +2.0
  c = ( a + b ) / 2.0
  m = 2.1

  example_test ( a, b, c, m, machep, e, t, h_02, 'h_02(x) = x * x' )

  a = -0.5
  b =  +2.0
  c = ( a + b ) / 2.0
  m = 14.0

  example_test ( a, b, c, m, machep, e, t, h_03, 'h_03(x) = x^3 + x^2' )

  a = -0.5
  b =  +2.0
  c = ( a + b ) / 2.0
  m = 28.0

  example_test ( a, b, c, m, machep, e, t, h_03, 'h_03(x) = x^3 + x^2' )

  a = -10.0
  b = +10.0
  c = ( a + b ) / 2.0
  m = 72.0

  example_test ( a, b, c, m, machep, e, t, h_04, 'h_04(x) = ( x + sin(x) ) * exp(-x*x)' )

  a = -10.0
  b = +10.0
  c = ( a + b ) / 2.0
  m = 72.0

  example_test ( a, b, c, m, machep, e, t, h_05, 'h_05(x) = ( x - sin(x) ) * exp(-x*x)' )
#
#  Terminate.
#
  print ( '' )
  print ( 'GLOMIN_TEST' )
  print ( '  Normal end of execution.' )
  return

def example_test ( a, b, c, m, machep, e, t, f, title ):

#*****************************************************************************80
#
## EXAMPLE_TEST tests the Brent global minimizer on one test function.
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
#    Input, real A, B, the endpoints of the interval.
#
#    Input, real C, an initial guess for the global
#    minimizer.  If no good guess is known, C = A or B is acceptable.
#
#    Input, real M, the bound on the second derivative.
#
#    Input, real MACHEP, an estimate for the relative machine
#    precision.
#
#    Input, real E, a positive tolerance, a bound for the
#    absolute error in the evaluation of F(X) for any X in [A,B].
#
#    Input, real T, a positive absolute error tolerance.
#
#    Input, function value = F ( X ), the name of a user-supplied
#    function whose global minimum is being sought.
#
#    Input, string TITLE, a title for the problem.
#
  x, fx = glomin ( a, b, c, m, machep, e, t, f )
  fa = f ( a )
  fb = f ( b )

  print ( '' )
  print ( '  %s' % ( title ) )
  print ( '' )
  print ( '      A                 X             B' )
  print ( '    F(A)              F(X)          F(B)' )
  print ( '' )
  print ( '  %14f  %14f  %14f' % ( a,  x,  b ) )
  print ( '  %14e  %14e  %14e' % ( fa, fx, fb ) )

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
  glomin_test ( )
  timestamp ( )

