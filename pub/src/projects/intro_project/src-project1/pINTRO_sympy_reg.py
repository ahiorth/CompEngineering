import sympy as sym
sym.init_printing(use_latex=True)

##from pINTRO_linear_regression import OLSR

if __name__ == "__main__":

    # Approximate function g(x,y)=sqrt(x^2+y^2) as a linear function in a
    # square region, assuming x to always be less than y.
    #
    # Then, the least squares problem can be solved analytically using
    # double integrals.
    #
    # We find that g(x,y) ~ 0.43x + 0.93y, i.e., that the hypotenuse of a
    # right triangle is approximately equal to 0.43 times the shortest side,
    # plus 0.93 times the second shortest side.
    #
    # Example: x=3, y=4 --> z ~ 0.43*x+0.93*4 = 5.01 ~ 5.
    #
    # For an equilateral triangle, z ~ 1.36*x.

    x, y, u = sym.symbols('x y u', positive=True)
    a, b, c = sym.symbols('a b c')

    # ----------------------------------------------------------------------
    # No constant coefficient, x < y:
    integrand = (sym.sqrt(x*x+y*y)-a*x-b*y)**2  # c?
    int_x = sym.integrate(integrand, (x, 0, y))
    chi_sq = sym.integrate(int_x, (y, 0, u))
    dchi_da = sym.diff(chi_sq, a)
    dchi_db = sym.diff(chi_sq, b)

    sol = sym.solve([dchi_da, dchi_db], a, b)
    a_optimal = sol[a].evalf()
    b_optimal = sol[b].evalf()
    print('a=', a_optimal, ', b=', b_optimal)
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # No constant coefficient, x < y:
    integrand = (sym.sqrt(x*x+y*y)-a*x-b*y-c)**2  # c?
    int_x = sym.integrate(integrand, (x, 0, y))
    chi_sq = sym.integrate(int_x, (y, 0, u))
    dchi_da = sym.diff(chi_sq, a)
    dchi_db = sym.diff(chi_sq, b)
    dchi_dc = sym.diff(chi_sq, c)

    sol = sym.solve([dchi_da, dchi_db, dchi_dc], a, b, c)
    a_optimal = sol[a].evalf()
    b_optimal = sol[b].evalf()
    c_optimal = sol[c].evalf()
    print('a=', a_optimal, ', b=', b_optimal, ', c=', c_optimal)
    # ----------------------------------------------------------------------




