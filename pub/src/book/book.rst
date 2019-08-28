.. Automatically generated Sphinx-extended reStructuredText file from DocOnce source
   (https://github.com/hplgit/doconce/)

.. |nbsp| unicode:: 0xA0
   :trim:

.. Note on the Springer T4 style: here we use the modifications

.. introduced in t4do.sty and svmonodo.sty (both are bundled with DocOnce).

.. Document title:

Modeling and Computational Engineering
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

:Authors: Aksel Hiorth, the National IOR Centre & Institute for Energy Resources,
University of Stavanger
:Date: Aug 22, 2019

*Summary.* (Work in Progress) The purpose of this document is to explain how computers solve mathematical models.
Many of the most common numerical methods is presented, we show how to implement them in Python, and discuss the limitations.
The mathemathical formalism is kept to a minimum. All the material is available at
`github <https://github.com/ahiorth/CompEngineering>`__. For each of the chapter there is a Jupyter `notebook <https://github.com/ahiorth/CompEngineering/tree/master/pub/chapters>`__. This makes it possible to run all the codes in this document.
We strongly recommend to install Python from `Anaconda <https://www.anaconda.com/>`__. All documents have been prepared using `doconce <https://github.com/ahiorth/CompEngineering/tree/master/pub/chapters>`__. 

.. !split

.. _ch:preface:

Preface
%%%%%%%

What does computers do better than humans? What is it possible to
compute? These questions have not been fully answered yet, and in the
coming years we will most likely see that the boundaries for what
computers can do will expand significantly. Many of the  fundamental laws in
nature have been known for quite some time, but still it is almost
impossible to predict the behavior of water (H$_2$O) from quantum
mechanics. The most sophisticated super computers runs for days and are
only able to simulate  the behavior of molecules in a couple of
seconds, almost too short to extract meaningful thermodynamic
properties. This leads to another interesting question: What does humans do better
than machines? A large part of
the answer to this question is *modeling*. Modeling is the ability to 
break a complicated, unstructured problem into smaller pieces that can
be solved by computers or by other means. Modeling requires *domain knowledge*, one need to
understand the system well enough to make the correct or the most efficient simplifications. The process usually starts
with some experimental data that one would like to understand, it could be the increasing temperature in the atmosphere or sea, it could 
be changes in the chemical composition of a fluid passing through a rock. The modeler then makes a mental image, which includes a set of 
mechanisms that could be the cause of the observed data. These mechanisms then needs to be formulated mathematically.   
How can we know if a model of a system is good? First of all, a good model is a model that do not break 
any of the fundamental laws of nature, such as mass (assuming non relativistic effects) and energy conservation. Even if you are searching 
for new laws of nature, you have to make sure that your model respect the existing laws, because then a deviation from your model and
the observations could be a hint of the new physics you are searching for.  
Secondly, the model must be able to match the observable data, with a limited set of variables. The variables should 
be determined from data, and then the model should be able to make some predictions that can be tested. Thus, the true
purpose of the model is not only to match experimental data, but serve as a framework where the underlying
mechanisms of the process can be understood. This is done by making model predictions, test them, and improve the model.

In this course our main focus will be on how to use computers to solve models. We will show you through exercises how a mathematical model of
a physical system can be made, and you will have the possibility to explore the model. Computers are extremely useful, they can solve problems that
would be impossible to solve by hand. However, it is extremely important to know about the limitations and strength of various algorithms. One need
to have a toolbox of various algorithms that can be employed depending on the problem one are studying. Sometimes speed is not an issue, and one can use
simpler algorithms, but in many cases *speed is an issue*. Thus it is important to not waste computational time when it is not needed, we will encounter 
examples of this many times in this course. Why should you spend time learning about algorithms that have been implemented already in a software that 
most likely can be downloaded for free? There are many answers to this question, some more practical and some that goes deeper. Lets start with the
practical considerations: Often you encounter a problem that needs to be solved by a computer, it could be as simple as to integrate some production data 
in a spreadsheet to calculate the total production, or it could be to fit a function with more than one variable to some data. Once you have this problem, and 
starting to ask Mr. Google for a solution, you will quickly realize that there are numerous ways of achieving what you want. By educating yourself 
within the most basic numerical methods, presented in this course, you will be able to judge for yourself which method to use in a specific case. 
Another motivation is that development of most of the different numerical methods are *not that difficult*, they usually follow a very similar pattern, but
there are some ''tricks''. It is extremely useful to learn these tricks, they can be adopted to a range of different problems, many are easily implemented
in a spreadsheet. There are some more deeper arguments, and that is that the numerical methods are developed to solve a *general* problem. Most of the 
time we work with *specific* problems, and we would like to have an algorithm that is optimal for our problem that goes beyond only choosing the right one. 
Having understood and learned all the cool tricks that was used in the development of the algorithm in the general case, 
is a starting point for adopting the algorithm to your specific situation. Secondly development of an algorithm is a concrete case of *Computational Thinking*.
Computational thinking is not necessarily related to computers and programming, but it is a way of structuring your work 
into precise statements that are being executed one at a time in a specific order. By learning about algorithmic development, you 
will train yourself in the art of computational thinking, which is a useful skill in all kind of problem solving. 

*Aksel Hiorth, December 2018

.. !split

.. _ch:taylor:

Finite differences
%%%%%%%%%%%%%%%%%%

The mathematics introduced in this chapter is absolutely essential in order to understand the development of numerical algorithms. We strongly advice you to study it carefully, implement python scripts and investigate the results, reproduce the analytical derivations and compare with the numerical solutions.

Numerical derivatives
=====================
The solution to a mathematical model is usually a function. The function could describe the temperature evolution of the earth, it could be growth of cancer cells, the water pressure in an oil reservoir, the list is endless.If we can solve the model analytically, the answer is given in terms of a continuous function. Most of the models cannot be solved analytically, then we have to rely on computers to help us. The computer does not have any concept of continuous functions, a function is always evaluated at some point in space and/or time. Assume for simplicity that the solution to our problem is :math:`f(x)=\sin x`, and we would like to visualize the solution. How many points do we need in our plot to approximate the true function? 
In figure :ref:`fig:taylor:sinx`, there is a plot of :math:`\sin x` on the interval :math:`[-\pi,\pi]`.

.. _fig:taylor:sinx:

.. figure:: fig-taylor/func_plot.png
   :width: 600

   *A plot of :math:`\sin x` for different spacing of the :math:`x`-values*

From the figure we see that in some areas only a couple of points are needed in order to
represent the function well, and in some areas more points are needed. To state it more clearly; between :math:`[-1,1]` a linear function (few points) approximate :math:`\sin x` well, 
whereas in the area where the derivative of the function changes e.g. in :math:`[-2,-1]`, we need the points to be more closely spaced to capture the behavior of the true function.

Why do we care about the number of points? In many cases the function we would like to evaluate can take a very long time to evaluate. Sometimes simulation time is not an issue, then we can use a large number of function
evaluations. However, in many applications simulation time *is an issue*, and it would be good to know where the points needs to be closely spaced, and where we can 
manage with only a few points.

What is a *good representation* representation of the true function? We cannot rely on visual inspection. In the next section we will show how Taylor polynomial representation of a function is a natural starting point to answer this question.

Taylor Polynomial Approximation
===============================
There are many ways of representing a function, but perhaps one of the most widely used is Taylor polynomials. 
Taylor series are the basis for solving ordinary and differential equations, simply because it makes it possible to evaluate any function with a set
of limited operations: *addition, subtraction, and multiplication*. The Taylor polynomial, :math:`P_n(x)` of degree :math:`n` of a function :math:`f(x)` at the point :math:`c` is defined as:

.. admonition:: Taylor polynomial

   
   .. math::
           
            P_n(x) = f(c)+f^\prime(c)(x-c)+\frac{f^{\prime\prime}(c)}{2!}(x-c)^2+\cdots+\frac{f^{(n)}(c)}{n!}(x-c)^n\nonumber
           
   
   .. math::
      :label: eq:taylor:taylori
   
             
           =\sum_{k=0}^n\frac{f^{(n)}}{k!}(x-c)^k.\



If the series is around the point :math:`c=0`, the Taylor polynomial :math:`P_n(x)` is often called a Maclaurin polynomial, more examples can be found 
`here <https://en.wikipedia.org/wiki/Taylor_series>`__. If the series converge (i.e. that the higher order terms approach zero), then we can represent the
function :math:`f(x)` with its corresponding Taylor series around the point :math:`x=c`:

.. math::
   :label: eq:taylor:taylor

        
         f(x) = f(c)+f^\prime(c)(x-c)+\frac{f^{\prime\prime}(c)}{2!}(x-c)^2+\cdots
        =\sum_{k=0}^\infty\frac{f^{(n)}}{k!}(x-c)^k.\
        

The Maclaurin series of :math:`\sin x` is:

.. math::
   :label: sin

        
        \sin x = x-\frac{x^3}{3!}+\frac{x^5}{5!}-\frac{x^7}{7!}+\cdots=\sum_{k=0}^{\infty}\frac{(-1)^n}{(2n+1)!}x^{2n+1}.
        \
        

In figure :ref:`fig:mac_sin`, we show the first nine terms in the Maclaurin series for :math:`\sin x` (all even terms are zero). 

.. _fig:mac_sin:

.. figure:: fig-taylor/mac_sin.png
   :width: 600

   Up to ninth order in the Maclaurin series of :math:`\sin x`

Note that we get a decent representation of :math:`\sin x` on the domain, by *only knowing the function and its derivative in a single point*. 
The error term in Taylors formula, when we represent a function with a finite number of polynomial elements is given by:

.. math::
        
        R_n(x)=f(x)-P_n(x)=\frac{f^{(n+1)}(\eta)}{(n+1)!}(x-c)^{n+1}\nonumber
        

.. math::
   :label: eq:taylor:error

          
              =\frac{1}{n!}\int_c^x(x-\tau)^{n}f^{(n+1)}(\tau)d\tau,\
        

for some :math:`\eta` in the domain :math:`[x,c]`.
If we want to calculate 
:math:`\sin x` to a precision lower than a specified value we can do it as follows:

.. code-block:: python

    import numpy as np
    
    # Sinus implementation using the Maclaurin Serie
    # By setting a value for eps this value will be used
    # if not provided
    def my_sin(x,eps=1e-16):
        f = power = x
        x2 = x*x
        sign = 1
        i=0
        while(power>=eps):
            sign = - sign
            power *= x2/(2*i+2)/(2*i+3)
            f += sign*power
            i += 1
        print('No function evaluations: ', i)
        return f
    
    x=0.8
    eps = 1e-9
    print(my_sin(x,eps), 'error = ', np.sin(x)-my_sin(x,eps))

This implementation needs some explanation:

* The error term is given in equation :eq:`eq:taylor:error`, in this case it reduces to :math:`R_{2n}=(-1)^{n+1}x^{2n+1}\cos\eta/(2n+1)!` for terms up to :math:`k=n-1` in equation :eq:`sin`. Since we do not know
  where to evaluate :math:`\eta` we just replace :math:`\cos\eta` with one (since :math:`\cos\eta\leq1`). We then add the higher order terms and check if the error term is low enough, since we add the error term 
  to the function evaluation our estimate will always be better than the specified accuracy.

* We evaluate the polynomials in the Taylor series by using the previous values too avoid too many multiplications within the loop, we do this by using the following identity:

.. math::
          
          \sin x=\sum_{k=0}^{\infty} (-1)^nt_n, \text{ where: } t_n\equiv\frac{x^{2n+1}}{(2n+1)!}, \text{ hence :}\nonumber
        

.. math::
          
          t_{n+1}=\frac{x^{2(n+1)+1}}{(2(n+1)+1)!}=\frac{x^{2n+1}x^2}{(2n+1)! (2n+2)(2n+3)}\nonumber
        

.. math::
   :label: _auto1

          
          =t_n\frac{x^2}{(2n+2)(2n+3)}
        
        

Evaluation of polynomials
-------------------------
How to evaluate a polynomial of the type: :math:`p_n(x)=a_0+a_1x+a_2x^2+\cdots+a_nx^n`? We already saw a hint in the previous section that it can be done in different ways. One way is simply to 
do:

.. code-block:: python

    pol = a[0]
    for i in range(1,n+1):
    	pol = pol + a[i]*x**i

Note that there are :math:`n` additions, whereas there are :math:`1 + 2 +3+\cdots+n=n(n+1)/2` multiplications for all the iterations. Instead of evaluating the powers all over in 
each loop, we can use the previous calculation to save the number of multiplications:

.. code-block:: python

    pol = a[0] + a[1]*x
    power = x
    for i in range(2,n+1):
    	power  = power*x
    	pol    = pol + a[i]*power

In this case there are still :math:`n` additions, but now there are :math:`2n-1` multiplications. For :math:`n=15`, this amounts to 120 for the first, and 29 for the second method. 
Polynomials can also be evaluated using *nested multiplication*:

.. math::
        
        p_1  = a_0+a_1x\nonumber
        

.. math::
          
        p_2  = a_0+a_1x+a_2x^2=a_0+x(a_1+a_2x)\nonumber
        

.. math::
          
        p_3  = a_0+a_1x+a_2x^2+a_3x^3=a_0+x(a_1+x(a_2+a_3x))\nonumber
        

.. math::
   :label: _auto2

          
        \vdots
        
           

and so on. This can be implemented as:

.. code-block:: python

    pol = a[n]
    for i in range(n-1,1,-1):
    	pol  = a[i] + pol*x

In this case we only have :math:`n` multiplications. So if you know beforehand exactly how many terms is needed to calculate the series, this method would be the preferred method, and is implemented in NumPy as `polyval <https://docs.scipy.org/doc/numpy/reference/generated/numpy.polyval.html#r138ee7027ddf-1>`__. 

.. _ch:taylor:der:

Calculating Derivatives of Functions
====================================

index{forward difference}

The derivative of a function can be calculated using the definition from calculus:

.. math::
   :label: eq:taylor:der1

        
        f^\prime(x)=\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}\simeq \frac{f(x+h)-f(x)}{h}.\
          

Not that :math:`h` can be both positive and negative, if :math:`h` is positive equation :eq:`eq:taylor:der1` is termed *forward difference*, because we use the function value on the right (:math:`f(x+|h|)`). If on the other hand :math:`h` is negative equation :eq:`eq:taylor:der1` is termed *backward difference*, because we use the value to the left (:math:`f(x-|h|)`). (:math:`|h|` is the absolute value of :math:`h`).
In the computer we cannot take the limit, :math:`h\to 0`, a natural question is then: What value to use for :math:`h`? 
In figure :ref:`fig:taylor:df`, we have evaluated the numerical derivative of :math:`\sin x`, using the formula in equation :eq:`eq:taylor:der1` for different step sizes :math:`h`. 

.. _fig:taylor:df:

.. figure:: fig-taylor/df.png
   :width: 600

   *Error in the numerical derivative of :math:`\sin x` at :math:`x=0.2` for different step size*

We clearly see that the error depends on the step size, but there is a minimum; choosing a step size too large give a poor estimate and choosing a too low step size give an 
even worse estimate. The explanation for this behavior is two competing effects: *mathematical approximation* and *round off errors*. Let us consider approximation or truncation error
first. By using the Taylor expansion in equation :eq:`eq:taylor:taylor` and expand about :math:`x` and the error formula :eq:`eq:taylor:error`, we get:

.. math::
        
        f(x+h)=f(x)+f^\prime(x)h + \frac{h^2}{2}f^{\prime\prime}(\eta)\text{ , hence:}\nonumber
        

.. math::
   :label: eq:taylor:derr

          
        f^\prime(x)=\frac{f(x+h)-f(x)}{h}-\frac{h}{2}f^{\prime\prime}(\eta),\
        

for some :math:`\eta` in :math:`[x,x+h]`. Thus the error to our approximation is :math:`hf^{\prime\prime}(\eta)/2`, if we reduce the step size by a factor of 10 the error is reduced by a factor of 10. 
Inspecting the graph, we clearly see that this is correct as the step size decreases from :math:`10^{-1}` to :math:`10^{-8}`. When the step size decreases more, there is an increase in the error. This
is due to round off errors, and can be understood by looking into how numbers are stored in a computer.  

Big :math:`\mathcal{O}` notation
--------------------------------
`example <https://rob-bell.net/2009/06/a-beginners-guide-to-big-o-notation/>`__

Round off Errors
----------------
In a computer a floating point number,$x$, is represented as:

.. math::
   :label: _auto3

        
        x=\pm q2^m.
        
        

Most computers are 64-bits, then one bit is reserved for the sign, 52 for the fraction (:math:`q`) and 11 for
the exponent (:math:`m`)  (for a graphic illustration see `Wikipedia <https://en.wikipedia.org/wiki/Double-precision_floating-point_format>`__).
what is the largest *floating point* number the computer can represent? 
Since :math:`m` contains 11 bits, :math:`m` can have the maximal value :math:`m=2^{11}=1024`, and then the largest value is close to :math:`2^{1024}\simeq 10^{308}`.
If you enter ``print(10.1*10**(308))`` in Python the answer will be ``Inf``. If you enter ``print(10*10**(308))``, Python will give an answer. This is because 
the number :math:`10.1\cdot10^{308}` is floating point number, whereas :math:`10^{309}` is an *integer*, and Python does something clever when it comes to representing integers. 
Python has a third numeric type called long int, which can use the available memory to represent an integer. 

:math:`10^{308}` is the largest number, but what is the highest precision we can use, or how many decimal places can we use for a floating point number? 
Since there are 52 bits for the fraction, there are :math:`1/2^{52}\simeq10^{-16}` decimal places. As an example
the value of :math:`\pi` is :math:`3.14159265358979323846264338\ldots`, but in Python it can only be represented by 16 digits: :math:`3.141592653589793`. In principle 
it does not sound so bad to have an answer accurate to 16 digits, and it is much better than most experimental results. 
So what is the problem? One problem that you should be aware of is that round off errors can be a serious problem when we subtract two numbers that 
are very close to one another. If we implement the following program in Python:

.. code-block:: python

    h=1e-16
    x = 2.1 + h
    y = 2.1 - h
    print((x-y)/h)

we expect to get the answer 2, but instead we get zero. By changing :math:`h` to a higher value, the answer will get closer to 2. 

Armed with this knowledge of round off errors, we can continue to analyze
the result in figure :ref:`fig:taylor:df`.
The round off error when we represent a floating point number :math:`x` in the 
machine will be of the order :math:`x/10^{16}` (*not* :math:`10^{-16}`). In general, when we evaluate a function the error will be of the order 
:math:`\epsilon|f(x)|`, where :math:`\epsilon\sim10^{-16}`. Thus equation :eq:`eq:taylor:derr` is modified in the following way when we take into account the round off errors:

.. math::
   :label: eq:taylor:derr2

        
        f^\prime(x)=\frac{f(x+h)-f(x)}{h}\pm\frac{2\epsilon|f(x)|}{h}-\frac{h}{2}f^{\prime\prime}(\eta),\
        

we do not know the sign of the round off error, so the total error :math:`R_2` is:

.. math::
   :label: eq:taylor:derr3

        
        R_2=\frac{2\epsilon|f(x)|}{h}+\frac{h}{2}|f^{\prime\prime}(\eta)|.\
        

We have put absolute values around the function and its derivative to get the maximal error, it might be the case that the round off error cancel part of the 
truncation error. However, the round off error is random in nature and will change from machine to machine, and each time we run the program. 
Note that the round off error increases when :math:`h` decreases, and the approximation error decreases when :math:`h` decreases. This is exactly what we see in the figure above. We can find the 
best step size, by differentiating :math:`R_2` and put it equal to zero:

.. math::
        
        \frac{dR_2}{dh}=-\frac{2\epsilon|f(x)|}{h^2}+\frac{1}{2}f^{\prime\prime}(\eta)=0\nonumber
        

.. math::
   :label: eq:taylor:derr4

          
        h=2\sqrt{\epsilon\left|\frac{f(x)}{f^{\prime\prime}(\eta)}\right|}\simeq 2\cdot10^{-8},\
        

In the last equation we have assumed that :math:`f(x)` and its derivative is :math:` |nbsp| 1`. This step size corresponds to an error of order :math:`R_2\sim10^{-8}`. 
Inspecting 
the result in figure :ref:`fig:taylor:df`.
we see that the minimum is located at :math:`h\sim10^{-8}`.      

Higher Order Derivatives
========================
There are more ways to calculate the derivative of a function, than the formula given in equation :eq:`eq:taylor:derr`. Different formulas can be
derived by using Taylors formula in :eq:`eq:taylor:taylor`, usually one expands about :math:`x\pm h`:

.. math::
        
        f(x+h)=f(x)+f^\prime(x)h + \frac{h^2}{2}f^{\prime\prime}(x)+ \frac{h^3}{3!}f^{(3)}(x)+ \frac{h^4}{4!}f^{(4)}(x)+\cdots\nonumber
        

.. math::
   :label: _auto4

          
        f(x-h)=f(x)-f^\prime(x)h + \frac{h^2}{2}f^{\prime\prime}(x)- \frac{h^3}{3!}f^{(3)}(x)+ \frac{h^4}{4!}f^{(3)}(x)-\cdots.
        
        

If we add these two equations, we get an expression for the second derivative, because the first derivative cancels out. But we also observe that if we subtract these two equations we get 
an expression for the first derivative that is accurate to a higher order than the formula in equation :eq:`eq:taylor:der1`, hence:

.. math::
   :label: eq:taylor:der2

        
        f^\prime(x)=\frac{f(x+h)-f(x-h)}{2h} -\frac{h^2}{6}f^{(3)}(\eta),\
        

.. math::
   :label: eq:taylor:2der

          
        f^{\prime\prime}(x) = \frac{f(x+h)+f(x-h)-2f(x)}{h^2}+ \frac{h^2}{12}f^{(4)}(\eta)\,
        

for some :math:`\eta` in :math:`[x,x+h]`. In figure :ref:`fig:taylor:df2`, we have plotted equation :eq:`eq:taylor:derr`, :eq:`eq:taylor:der2`, and :eq:`eq:taylor:2der` for 
different step sizes. The derivative in equation :eq:`eq:taylor:der2`, gives a higher accuracy than equation :eq:`eq:taylor:derr` for a larger step size,
as can bee seen in figure :ref:`fig:taylor:df2`.

.. _fig:taylor:df2:

.. figure:: fig-taylor/df2.png
   :width: 600

   *Error in the numerical derivative and second derivative of :math:`\sin x` at :math:`x=0.2` for different step size*

We can perform a similar error analysis as we did before, and then we find for equation :eq:`eq:taylor:der2` and :eq:`eq:taylor:2der` that the total
numerical error is:

.. math::
   :label: eq:taylor:derr3b

        
        R_3=\frac{\epsilon|f(x)|}{h}+\frac{h^2}{6}f^{(3)}(\eta),\
        

.. math::
   :label: eq:taylor:derr4b

          
        R_4=\frac{4\epsilon|f(x)|}{h^2}+\frac{h^2}{12}f^{(4)}(\eta),\
        

respectively. Differentiating these two equations with respect to :math:`h`, and set the equations equal to zero, we find an optimal step size of
:math:`h\sim10^{-5}` for equation :eq:`eq:taylor:derr3b`, which gives an error of :math:`R_2\sim 10^{-16}/10^{-5}+(10^{-5})^2/6\simeq10^{-10}`, and :math:`h\sim10^{-4}` for equation
:eq:`eq:taylor:derr4b`, which gives an error of :math:`R_4\sim 4\cdot10^{-16}/(10^{-4})^2+(10^{-4})^2/12\simeq10^{-8}`. Note that we get the surprising result for the first order 
derivative in equation :eq:`eq:taylor:der2`, that a higher step size gives a more accurate result. 

.. !split

.. _ch:nlin:

Linear and nonlinear equations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. !split

.. _ch:numint:

Numerical integration
%%%%%%%%%%%%%%%%%%%%%

Numerical Integration
=====================
Before diving into the details of this section, it is worth pointing out that the derivation of the algorithms in this section follows a general pattern:

1. We start with a mathematical model (in this case an integral)

2. The mathematical model is formulated in discrete form 

3. Then we design an algorithm to solve the model 

4. The numerical solution for a test case is compared with the true solution (could be an analytical solution or data)

5. Error analysis: we investigate the accuracy of the algorithm by changing the number of iterations and/or make changes to the implementation or algorithm

In practice you would not use your own implementation to calculate an integral, but in order to understand which method to use 
in a specific case, it is important to understand the limitation and advantages of the different algorithms. The only way to achieve this is to 
have a basic understanding of the development. There might also be some cases where you would like to adapt an integration scheme to your specific
case if there is a special need  that the integration is fast. 

The Midpoint Rule
-----------------
Numerical integration is encountered in numerous applications in physics and engineering sciences. 
Let us first consider the most simple case, a function :math:`f(x)`, which is a function of one variable, :math:`x`. The most straight forward way of calculating the area :math:`\int_a^bf(x)dx` is 
simply to divide the area under the function into :math:`N` equal rectangular slices with size :math:`h=(b-a)/N`, as illustrated in figure :ref:`fig:numint:mid`. The area of one box is:

.. math::
   :label: eq:numint:mid0

        
        M(x_k,x_k+h)=f(x_k+\frac{h}{2}) h,\
        

and the area of all the boxes is:

.. math::
        
        I(a,b)=\int_a^bf(x)dx\simeq\sum_{k=0}^{N-1}M(x_k,x_k+h)\nonumber
        

.. math::
   :label: eq:numint:mid1

          
        =h\sum_{k=0}^{N-1}f(x_k+\frac{h}{2})=h\sum_{k=0}^{N-1}f(a+(k+\frac{1}{2})h).
        \
        

Note that the sum goes from :math:`k=0,1,\ldots,N-1`, a total of :math:`N` elements. We could have chosen to let the sum go from :math:`k=1,2,\ldots,N`. 
In Python, C, C++ and many other programming languages the arrays start by indexing the elements from :math:`0,1,\ldots` to :math:`N-1`, 
therefore we choose the convention of having the first element to start at :math:`k=0`.

.. _fig:numint:mid:

.. figure:: fig-numint/func_sq.png
   :width: 800

   *Integrating a function with the midpoint rule*

Below is a Python code, where this algorithm is implemented for :math:`\int_0^\pi\sin (x)dx`

.. code-block:: python

    import numpy as np
    # Function to be integrated
    def f(x):
        return np.sin(x)
    
    def int_midpoint(func, lower_limit, upper_limit,N):
        """ calculates the area of func over the domain lower_limit
            to upper limit using N integration points """
        h    = (upper_limit-lower_limit)/N # step size 
        area = 0.
        for all integration points do:
            estimate integration midpoint value, xi
            add area under curve: func(xi)*h
        return area


.. note::
   There are many ways to calculate loops in a programming language. If you were coding in a lower level programming language like Fortran, C or C++, you would probably implement the loop like (in Python syntax):
   
   .. code-block:: python
   
       for k in range(0,N): # loop over k=0,1,..,N-1
           val = lower_limit+(k+0.5)*h # midpoint value
           area += func(val)
       return area*h
   
   However, in Python, you would always try to avoid loops because they are generally slow. A more efficient way of implementing the above rule would be to replace the loop with:
   
   .. code-block:: python
   
       val  = [lower_limit+(k+0.5)*h for k in range(N)]
       ff   = func(val)
       area = np.sum(ff)
       return area*h




The Trapezoidal Rule
--------------------
The numerical error in the above example is quite low, only about 2$\%$ for :math:`N=5`. 
However, by just looking at the graph above it seems likely that we can develop a better algorithm by using trapezoids instead of rectangles, 
see figure :ref:`fig:numint:trap`.

.. _fig:numint:trap:

.. figure:: fig-numint/func_tr.png
   :width: 800

   *Integrating a function with the trapezoidal rule*

Earlier we approximated the area using the midpoint value: :math:`f(x_k+h/2)\cdot h`. Now we use :math:`A=A_1+A_2`, where :math:`A_1=f(x_k)\cdot h` 
and :math:`A_2=(f(x_k+h)-f(x_k))\cdot h/2`, hence the area of one trapezoid is:

.. math::
   :label: _auto5

        
        A\equiv T(x_k,x_k+h)=(f(x_k+h)+f(x_k))h/2.
        
        

This is the trapezoidal rule, and for the whole interval we get:

.. math::
        
        I(a,b)=\int_a^bf(x)dx\simeq\frac{1}{2}h\sum_{k=0}^{N-1}\left[f(x_k+k h)+f(x_k)\right] \nonumber 
        

.. math::
          
        =h\left[\frac{1}{2}f(a)+f(a+h) + f(a+2h) +\nonumber\right. 
        

.. math::
          
        \left.\qquad\cdots + f(a+(N-2)h)+\frac{1}{2}f(b)\right]\nonumber 
        

.. math::
   :label: _auto6

          
        =h\left[\frac{1}{2}f(a)+\frac{1}{2}f(b)+\sum_{k=1}^{N-1}f(a+k h)\right].
        
        

Note that this formula was bit more involved to derive, but it requires only one more function evaluations compared to the midpoint rule. 
Below is a python implementation:

.. code-block:: python

    import numpy as np
    # Function to be integrated
    def f(x):
        return np.sin(x)
    
    #In the implementation below the calculation goes faster 
    #when we avoid unnecessary multiplications by h in the loop
    def int_trapez(func, lower_limit, upper_limit,N):
        """ calculates the area of func over the domain lower_limit
            to upper limit using N integration points """
        h       = (upper_limit-lower_limit)/N # step size
        area    = 0.5*(func(lower_limit)+func(upper_limit))
        val     = lower_limit
        for all integration points do:
            estimate integration midpoint value, xi
            add are under curve: func(xi)*h
        return area

In the table below, we have calculated the numerical error for various values of :math:`N`.

=========  =========  ==============  =================  
:math:`N`  :math:`h`  Error Midpoint  Error Trapezoidal  
=========  =========  ==============  =================  
    1         3.14        -57\%             100\%        
    5        0.628       -1.66\%            3.31\%       
    10       0.314       -0.412\%          0.824\%       
   100       0.031      -4.11E-3\%        8.22E-3\%      
=========  =========  ==============  =================  

Note that we get the surprising result that this algorithm performs poorer, a factor of 2 than the midpoint rule.
How can this be explained? By just looking at figure :ref:`fig:numint:mid`, we see that the midpoint rule actually over predicts the area from :math:`[x_k,x_k+h/2]` 
 and under predicts in the interval :math:`[x_k+h/2,x_{k+1}]` or vice versa. The net effect is that for many cases the midpoint rule give a slightly better 
 performance than the trapezoidal rule. In the next section we will investigate this more formally.

Numerical Errors on Integrals
-----------------------------
It is important to know the accuracy of the methods we are using, otherwise we do not know if the
computer produce correct results. In the previous examples we were able to estimate the error because we knew the analytical result. However, if we know the 
analytical result there is no reason to use the computer to calculate the result(!). Thus, we need a general method to estimate the error, and let the computer 
run until a desired accuracy is reached. 

In order to analyze the midpoint rule in more detail we approximate the function by a Taylor 
series at the midpoint between :math:`x_k` and :math:`x_k+h`: 

.. math::
        
        f(x)=f(x_k+h/2)+f^\prime(x_k+h/2)(x-(x_k+h/2))\nonumber
        

.. math::
   :label: _auto7

          
        +\frac{1}{2!}f^{\prime\prime}(x_k+h/2)(x-(x_k+h/2))^2+\mathcal{O}(h^3)
        
        

Since :math:`f(x_k+h/2)` and its derivatives are constants it is straight forward to integrate :math:`f(x)`:

.. math::
        
        I(x_k,x_k+h)=\int_{x_k}^{x_k+h}\left[f(x_k+h/2)+f^\prime(x_k+h/2)(x-(x_k+h/2))\right.\nonumber
        

.. math::
   :label: _auto8

          
        \left.+\frac{1}{2!}f^{\prime\prime}(x_k+h/2)(x-(x_k+h/2))^2+\mathcal{O}(h^3)\right]dx
        
        

The first term is simply the midpoint rule, to evaluate the two other terms we make the substitution: :math:`u=x-x_k`:

.. math::
        
        I(x_k,x_k+h)=f(x_k+h/2)\cdot h+f^\prime(x_k+h/2)\int_0^h(u-h/2)du\nonumber
        

.. math::
          
        +\frac{1}{2}f^{\prime\prime}(x_k+h/2)\int_0^h(u-h/2)^2du+\mathcal{O}(h^4)\nonumber
        

.. math::
   :label: _auto9

          
        =f(x_k+h/2)\cdot h-\frac{h^3}{24}f^{\prime\prime}(x_k+h/2)+\mathcal{O}(h^4).
        
        

Note that all the odd terms cancels out, i.e :math:`\int_0^h(u-h/2)^m=0` for :math:`m=1,3,5\ldots`. Thus the error for the midpoint rule, :math:`E_{M,k}`, on this particular interval is:

.. math::
   :label: _auto10

        
        E_{M,k}=I(x_k,x_k+h)-f(x_k+h/2)\cdot h=-\frac{h^3}{24}f^{\prime\prime}(x_k+h/2),
        
        

where we have ignored higher order terms. We can easily sum up the error on all the intervals, but clearly :math:`f^{\prime\prime}(x_k+h/2)` will 
not, in general, have the same value on all intervals. However, an upper bound for the error can be found by replacing :math:`f^{\prime\prime}(x_k+h/2)` 
with the maximal value on the interval :math:`[a,b]`, :math:`f^{\prime\prime}(\eta)`:

.. math::
   :label: eq:numint:em

        
        E_{M}=\sum_{k=0}^{N-1}E_{M,k}=-\frac{h^3}{24}\sum_{k=0}^{N-1}f^{\prime\prime}(x_k+h/2)\leq-\frac{Nh^3}{24}f^{\prime\prime}(\eta),\
        

.. math::
   :label: _auto11

          
        E_{M}\leq-\frac{(b-a)^3}{24N^2}f^{\prime\prime}(\eta),
        
        

where we have used :math:`h=(b-a)/N`. We can do the exact same analysis for the trapezoidal rule, but then we expand the function around :math:`x_k-h` instead of the midpoint. 
The error term is then:

.. math::
   :label: _auto12

        
        E_T=\frac{(b-a)^3}{12N^2}f^{\prime\prime}(\overline{\eta}).
        
        

At the first glance it might look like the midpoint rule always is better than the trapezoidal rule, but note that the second derivative is 
evaluated in different points (:math:`\eta` and :math:`\overline{\eta}`). Thus it is possible to construct examples where the midpoint rule performs poorer 
than the trapezoidal rule.

Before we end this section we will rewrite the error terms in a more useful form as it is not so easy to evaluate 
:math:`f^{\prime\prime}(\eta)` (since we do not know which value of :math:`\eta` to use). By taking a closer look at equation :eq:`eq:numint:em`, 
we see that it is closely related to the midpoint rule for :math:`\int_a^bf^{\prime\prime}(x)dx`, hence:

.. math::
   :label: _auto13

        
        E_{M}=-\frac{h^2}{24}h
        \sum_{k=0}^{N-1}f^{\prime\prime}(x_k+h/2)\simeq-\frac{h^2}{24}\int_a^b
        f^{\prime\prime}(x)dx
        
        

.. math::
   :label: _auto14

          
        E_M\simeq\frac{h^2}{24}\left[f^\prime(b)-f^\prime(a)\right]=-\frac{(b-a)^2}{24N^2}\left[f^\prime(b)-f^\prime(a)\right]
        
        

The corresponding formula for the trapezoid formula is:

.. math::
   :label: _auto15

        
        E_T\simeq \frac{h^2}{12}\left[f^\prime(b)-f^\prime(a)\right]=\frac{(b-a)^2}{12N^2}\left[f^\prime(b)-f^\prime(a)\right]
        
        

Now, we can make an algorithm that automatically choose the number of steps to reach (at least) a predefined accuracy:

.. code-block:: python

    import numpy as np
    # Function to be integrated
    def f(x):
        return np.sin(x)
    #Numerical derivative of function
    def df(x,func):
        dh=1e-5 # some low step size
        return (func(x+dh)-func(x))/dh 
    #Adaptive midpoint rule, "adaptive" because the number of 
    #function evaluations depends on the integrand
    def int_adaptive_midpoint(func, lower_limit, upper_limit, tol):
        """ calculates the area of func over the domain lower_limit
            to upper limit for the specified tolerance tol """
        dfa  = df(lower_limit,func) # derivative in point a 
        dfb  = df(upper_limit,func) # derivative in point b
        h    = np.sqrt(abs(24*tol/(dfb-dfa)))
        print('Number of intervals = ', (upper_limit-lower_limit)/h)
        for all integration points do:
            estimate integration midpoint value, xi
            add area under curve: func(xi)*h
        return area


.. note::
   In Python it is sometimes convenient to enter default values for the arguments in a function. In the above example, we could also have written the function definition as\\ ``def int_adaptive_midpoint(func, lower_limit, upper_limit,`` \\ ``tol=1e-8):``. If the ``tol`` parameter is not given the code will assume an accuracy of :math:`10^{-8}`.



.. _sec:numint:parct:

Practical Estimation of Errors on Integrals
-------------------------------------------
From the example above we were able to estimate the number of steps needed to reach (at least) a certain precision. 
In many practical cases we do not deal with functions, but with data and it can be difficult to evaluate the derivative. 
We also saw from the example above that the algorithm gives a higher precision than what we asked for. 
How can we avoid doing too many iterations? A very simple solution to this question is to double the number of intervals until 
a desired accuracy is reached. The following analysis holds for both the trapezoid and midpoint method, because in both cases 
the error scale as :math:`h^2`. 

Assume that we have evaluated the integral with a step size :math:`h_1`, and the computed result is :math:`I_1`. 
Then we know that the true integral is :math:`I=I_1+c h_1^2`, where :math:`c` is a constant that is unknown. If we now half the step size: :math:`h_2=h_1/2`, 
then we get a new (better) estimate of the integral, :math:`I_2`, which is related to the true integral :math:`I` as: :math:`I=I_2+c h_2^2`. 
Taking the difference between :math:`I_2` and :math:`I_1` give us an estimation of the error:

.. math::
   :label: _auto16

        
        I_2-I_1=I-c h_2^2-(I-ch_1^2)=3c h_2^2,
        
        

where we have used the fact that :math:`h_1=2h_2`, Thus the error term is:

.. math::
   :label: _auto17

        
        E(a,b)=c h_2^2=\frac{1}{3}(I_2-I_1).
        
        

This might seem like we need to evaluate the integral twice as many times as needed. This is not the case, by choosing to exactly 
half the spacing we only need to evaluate for the values that lies halfway between the original points. We will demonstrate how 
to do this by using the trapezoidal rule, because it operates directly on the :math:`x_k` values and not the midpoint values. 
The trapezoidal rule can now be written as:

.. math::
   :label: _auto18

        
        I_2(a,b)=h_2\left[\frac{1}{2}f(a)+\frac{1}{2}f(b)+\sum_{k=1}^{N_2-1}f(a+k h_2)\right],
        
        

.. math::
          
        =h_2\left[\frac{1}{2}f(a)+\frac{1}{2}f(b)+\sum_{k=\text{even values}}^{N_2-1}f(a+k h_2)\right.\nonumber
        

.. math::
   :label: _auto19

          
        \left.\qquad+\sum_{k=\text{odd values}}^{N_2-1}f(a+k h_2)\right],
        
        

in the last equation we have split the sum into odd an even values. The sum over the even values can be rewritten:

.. math::
   :label: _auto20

        
        \sum_{k=\text{even values}}^{N_2-1}f(a+k h_2)=\sum_{k=0}^{N_1-1}f(a+2k h_2)=\sum_{k=0}^{N_1-1}f(a+k h_1),
        
        

note that :math:`N_2` is replaced with :math:`N_1=N_2/2`, we can now rewrite :math:`I_2` as:

.. math::
        
        I_2(a,b)=h_2\left[\frac{1}{2}f(a)+\frac{1}{2}f(b)+\sum_{k=0}^{N_1-1}f(a+k h_1)\right.\nonumber
        

.. math::
   :label: _auto21

          
        \left.+\sum_{k=\text{odd values}}^{N_2-1}f(a+k h_2)\right]
        
        

Note that the first terms are actually the trapezoidal rule for :math:`I_1`, hence:

.. math::
   :label: _auto22

        
        I_2(a,b)=\frac{1}{2}I_1(a,b)+h_2\sum_{k=\text{odd values}}^{N_2-1}f(a+k h_2)
        
        

A possible algorithm is then:
1. Choose a low number of steps to evaluate the integral, :math:`I_0`, the first time, e.g. :math:`N_0=10`

2. Double the number of steps, :math:`N_1=2N_0` 

3. Calculate the missing values by summing over the odd number of steps :math:`\sum_{k=\text{odd values}}^{N_1-1}f(a+k h_1)`

4. Check if :math:`E_1(a,b)=\frac{1}{3}(I_1-I_0)` is lower than a specific tolerance

5. If yes quit, if not, return to 2, and continue until :math:`E_i(a,b)=\frac{1}{3}(I_{i+1}-I_{i})` is lower than the tolerance  

Below is a Python implementation:

.. code-block:: python

    import numpy as np
    # Function to be integrated
    def f(x):
        return np.sin(x)
    # step size is chosen automatically to reach the specified tolerance 
    def int_adaptive_trapez(func, lower_limit, upper_limit, tol):
        """ calculates the area of func over the domain lower_limit
            to upper limit for the specified tolerance tol """
        h       = (upper_limit-lower_limit)
        area    = 0.5*(func(lower_limit)+func(upper_limit))
        calc_tol = tol + 1 # just larger than tol to enter the while loop 
        while(calc_tol>tol):
            half the step size h /= 2
            for all odd integration points in the domain:
                sum up all the odd function values in odd_terms
            new_area = 0.5*area + h*odd_terms
            calc_tol = abs(new_area-area)/3 
            area     = new_area # store new values for next iteration
        print('Number of intervals = ', (upper_limit-lower_limit)/h)
        return area #while loop ended and we can return the area

If you compare the number of terms used in the adaptive trapezoidal rule, which was developed by halving the step size, and the adaptive midpoint rule that was derived on the basis of the theoretical error term, you will find the adaptive midpoint rule is more efficient. So why go through all this trouble? In the next section we will see that the development we did for the adaptive trapezoidal rule is closely related to Romberg integration, which is *much* more effective.

Romberg Integration
===================
The adaptive algorithm for the trapezoidal rule in the previous section can be easily improved by remembering 
that the true integral was given by [#romerr]_ : :math:`I=I_i+ch_i^2+\mathcal{O}(h^4)`. The error term was in the previous example only used to 
check if the desired tolerance was achieved, but we could also have added it to our estimate of the integral to reach an accuracy to fourth order:

.. [#romerr] Note that all odd powers of :math:`h` is equal to zero, thus the corrections are always in even powers.  

.. math::
   :label: _auto23

        
        I=I_{i+1}+ch^2+\mathcal{O}(h^4)=I_{i+1}+\frac{1}{3}\left[I_{i+1}-I_{i}\right]+\mathcal{O}(h^4).
        
        

As before the error term :math:`\mathcal{O}(h^4)`, can be written as: :math:`ch^4`. Now we can proceed as in the previous section: First we estimate the 
integral by one step size :math:`I_i=I+ch_i^4`, next we half the step size :math:`I_{i+1}=I+ch_{i+1}^4` and use these two estimates to calculate the error term:

.. math::
        
        I_{i+1}-I_{i}=I-c h_{i+1}^4-(I-ch_i^4)=-c h_{i+1}^4+c(2h_{i+1})^4=15c h_{i+1}^4,\nonumber
        

.. math::
   :label: _auto24

          
        ch_{i+1}^4=\frac{1}{15}\left[I_{i+1}-I_{i}\right]+\mathcal{O}(h^6).
        
        

but now we are in the exact situation as before, we have not only the error term but the correction up to order :math:`h^4` for this integral:

.. math::
   :label: eq:numint:rom

        
        I=I_{i+1}+\frac{1}{15}\left[I_{i+1}-I_{i}\right]+\mathcal{O}(h^6).\
        

Each time we half the step size we also gain a higher order accuracy in our numerical algorithm. Thus, there are two iterations going on at the same time; 
one is the iteration that half the step size (:math:`i`), and the other one is the increasing number of higher order terms added (which we will denote :math:`m`). 
We need to improve our notation, and replace the approximation of the integral (:math:`I_i`) with :math:`R_{i,m}`. Equation :eq:`eq:numint:rom`, can now 
be written:

.. math::
   :label: _auto25

        
        I=R_{i+1,2}+\frac{1}{15}\left[R_{i+1,2}-R_{i,2}\right]+\mathcal{O}(h^6).
        
        

A general formula valid for any :math:`m` can be found by realizing:

.. math::
   :label: eq:numint:rom0

        
        I=R_{i+1,m+1}+c_mh_i^{2m+2}+\mathcal{O}(h_i^{2m+4})\
        

.. math::
          
        I=R_{i,m+1}+c_mh_{i-1}^{2m+2}+\mathcal{O}(h_{i-1}^{2m+4})\nonumber
        

.. math::
   :label: eq:numint:rom1

          
        =R_{i,m+1}+2^{2m+2}c_mh_{i}^{2m+2}+\mathcal{O}(h_{i-1}^{2m+4}),\
        

where, as before :math:`h_{i-1}=2h_i`. Subtracting equation :eq:`eq:numint:rom0` and :eq:`eq:numint:rom1`, we find an expression for the error term:

.. math::
   :label: eq:numint:rom2

        
        c_mh_{i}^{2m+2}=\frac{1}{4^{m+1}-1}(R_{i,m}-R_{i-1,m})\
        

Then the estimate for the integral in equation :eq:`eq:numint:rom1` is:

.. math::
   :label: _auto26

        
        I=R_{i,m+1}+\mathcal{O}(h_i^{2m+2})
        
        

.. math::
   :label: _auto27

          
        R_{i,m+1}=R_{i,m}+\frac{1}{4^{m+1}-1}(R_{i+1,m}-R_{i,m}).
        
        

A possible algorithm is then:

1. Evaluate :math:`R_{0,0}=\frac{1}{2}\left[f(a)+f(b)\right](b-a)` as the first estimate

2. Double the number of steps, :math:`N_{i+1}=2N_i` or half the step size :math:`h_{i+1}=h_i/2` 

3. Calculate the missing values by summing over the odd number of steps :math:`\sum_{k=\text{odd values}}^{N_1-1}f(a+k h_{i+1})`

4. Correct the estimate by adding *all* the higher order error term :math:`R_{i,m+1}=R_{i,m}+\frac{1}{4^m-1}(R_{i+1,m+1}-R_{i,m+1})`

5. Check if the error term is lower than a specific tolerance :math:`E_{i,m}(a,b)=\frac{1}{4^{m+1}-1}(R_{i,m}-R_{i-1,m})`, if yes quit, if no goto 2, increase :math:`i` and :math:`m` by one

The algorithm is illustrated in figure :ref:`fig:numint:romberg`.

.. _fig:numint:romberg:

.. figure:: fig-numint/romberg.png
   :width: 400

   Illustration of the Romberg algorithm. Note that for each new evaluation of the integral :math:`R_{i,0}`, all the correction terms :math:`R_{i,m}` (for :math:`m>0`) must be evaluated again

Note that the tolerance term is not the correct one as it uses the error estimate for the current step, 
which we also use correct the integral in the current step to reach a higher accuracy. 
Thus the error on the integral will always be lower than the user specified tolerance.
Below is a Python implementation:

.. code-block:: python

    import numpy as np
    # Function to be integrated
    def f(x):
        return np.sin(x)
    # step size is choosen automatically to reach (at least) 
    # the specified tolerance 
    def int_romberg(func, lower_limit, upper_limit,tol,show=False):
        """ calculates the area of func over the domain lower_limit
            to upper limit for the given tol, if show=True the triangular
            array of intermediate results are printed """
        Nmax = 100
        R = np.empty([Nmax,Nmax]) # storage buffer
        h = (upper_limit-lower_limit) # step size
        R[0,0]    =.5*(func(lower_limit)+func(upper_limit))*h
        N = 1
        for i in range(1,Nmax):
            h /= 2
            N *= 2
            odd_terms=0
            for all odd terms 1, 3, ..., N-1 do:
                evaulate function values at odd points,
                sum them and store in odd_terms
            R[i,0]   = 0.5*R[i-1,0] + h*odd_terms
    
            for all m in 0, 1, ..., i-1:
                R[i,m+1]   = R[i,m] + (R[i,m]-R[i-1,m])/(4**(m+1)-1)                  
    	# check tolerance, best guess			
            calc_tol = abs(R[i,i]-R[i-1,i-1])       
            if estimated tolerance calc_tol is lower than tol:
                break  # estimated precision reached
            if max number of iterations are reached (i == Nmax-1):
                print('Romberg routine did not converge after ',
                  Nmax, 'iterations!')
                
        if(show==True):
            print out all triangualar elements in R[i,m]
    
        return R[i,i] #return the best estimate

Note that the Romberg integration only uses 32 function evaluations to reach a precision of :math:`10^{-8}`, whereas the adaptive midpoint and trapezoidal rule in the previous
section uses 20480 and 9069 function evaluations, respectively. 

Gaussian Quadrature
-------------------
Many of the methods we have looked into are of the type:

.. math::
   :label: eq:numint:qq1

        
        	\int_a^b f(x) dx = \sum_{k=0}^{N-1} \omega_k f(x_k),\
        

where the function is evaluated at fixed interval. For the midpoint rule :math:`\omega_k=h` for all values of :math:`k`, for the trapezoid rule 
:math:`\omega_k=h/2` for the endpoints and :math:`h` for all the interior points. 
For the Simpsons rule (see exercise) :math:`\omega_k=h/3, 4h/3,2h/3,4h/3,\ldots,4h/3,h/3`. 
Note that all the methods we have looked at so far samples the function in equal spaced points, :math:`f(a+k h)`, 
for :math:`k=0, 1, 2\ldots, N-1`. If we now allow for the function to be evaluated at unevenly spaced points, we can do a lot better. 
This realization is the basis for Gaussian Quadrature. We will explore this in the following, 
but to make the development easier and less cumbersome, we transform the integral from the domain :math:`[a,b]` to :math:`[-1,1]`:

.. math::
   :label: _auto28

        
        \int_a^bf(t)dt=\frac{b-a}{2}\int_{-1}^{1}f(x)dx\text{ , where:}
        
        

.. math::
   :label: _auto29

          
        x=\frac{2}{b-a}t-\frac{b+a}{b-a}.
        
        

The factor in front comes from the fact that :math:`dt=(b-a)dx/2`, thus we can develop our algorithms on the domain :math:`[-1,1]`, 
and then do the transformation back using: :math:`t=(b-a)x/2+(b+a)/2`.


.. note::
   The idea we will explore is as follows:
   If we can approximate the function to be integrated on the domain :math:`[-1,1]` (or on :math:`[a,b]`) as a 
   polynomial of as *large a degree as possible*, then the numerical integral of this polynomial will be very close to the integral of the 
   function we are seeking.



This idea is best understood by a couple of examples. Assume that we want to use :math:`N=1` in equation :eq:`eq:numint:qq1`:

.. math::
   :label: _auto30

        
        \int_{-1}^{1}f(x)\,dx\simeq\omega_0f(x_0).
        
        

We now choose :math:`f(x)` to be a polynomial of as large a degree as possible, but with the requirement that the integral is exact. If :math:`f(x)=1`, we get:

.. math::
   :label: _auto31

        
        \int_{-1}^{1}f(x)\,dx=\int_{-1}^{1}1\,dx=2=\omega_0,
        
        

hence :math:`\omega_0=2`. If we choose :math:`f(x)=x`, we get:

.. math::
   :label: _auto32

        
        \int_{-1}^{1}f(x)\,dx=\int_{-1}^{1}x\,dx=0=\omega_0f(x_0)=2x_0,
        
        

hence :math:`x_0=0`. 
The Gaussian integration rule for :math:`N=1` is:

.. math::
        
        \int_{-1}^{1}f(x)\,dx\simeq 2f(0)\text{, or: }\nonumber
        

.. math::
   :label: _auto33

          
        \int_{a}^{b}f(t)\,dt\simeq\frac{b-a}{2}\,2f(\frac{b+a}{2})=(b-a)f(\frac{b+a}{2}).
        
        

This equation is equal to the midpoint rule, by choosing :math:`b=a+h` we reproduce equation :eq:`eq:numint:mid0`. If we choose :math:`N=2`:

.. math::
   :label: _auto34

        
        \int_{-1}^{1}f(x)\,dx\simeq\omega_0f(x_0)+\omega_1f(x_1),
        
        

we can show that now $ f(x)=1,\,x,\,x^2\,x^3$ can be integrated exact:

.. math::
   :label: _auto35

        
        \int_{-1}^{1}1\,dx=2=\omega_0f(x_0)+\omega_1f(x_1)=\omega_0+\omega_1\,,
        
        

.. math::
   :label: _auto36

          
        \int_{-1}^{1}x\,dx=0=\omega_0f(x_0)+\omega_1f(x_1)=\omega_0x_0+\omega_1x_1\,,
        
        

.. math::
   :label: _auto37

          
        \int_{-1}^{1}x^2\,dx=\frac{2}{3}=\omega_0f(x_0)+\omega_1f(x_1)=\omega_0x_0^2+\omega_1x_1^2\,,
        
        

.. math::
   :label: _auto38

          
        \int_{-1}^{1}x^3\,dx=0=\omega_0f(x_0)+\omega_1f(x_1)=\omega_0x_0^3+\omega_1x_1^3\,,
        
        

hence there are four unknowns and four equations. The solution is: :math:`\omega_0=\omega_1=1` and :math:`x_0=-x_1=1/\sqrt{3}`.
The Gaussian integration rule for :math:`N=2` is:

.. math::
   :label: _auto39

        
        \int_{-1}^{1}f(x)\,dx\simeq f(-\frac{1}{\sqrt{3}})+f(\frac{1}{\sqrt{3}})\, \text{, or:}
        
        

.. math::
   :label: _auto40

          
        \int_{a}^{b}f(x)\,dx\simeq \frac{b-a}{2}\left[f(-\frac{b-a}{2}\frac{1}{\sqrt{3}}+\frac{b+a}{2})
        +f(\frac{b-a}{2}\frac{1}{\sqrt{3}}+\frac{b+a}{2})\right].
        
        

.. code-block:: python

    def int_gaussquad2(func, lower_limit, upper_limit):
        x   = np.array([-1/np.sqrt(3.),1/np.sqrt(3)])
        w   = np.array([1, 1])
        xp  = 0.5*(upper_limit-lower_limit)*x
        xp += 0.5*(upper_limit+lower_limit)
        area = np.sum(w*func(xp))
        return area*0.5*(upper_limit-lower_limit)

The case N=3
~~~~~~~~~~~~

For the case :math:`N=3`, we find that :math:`f(x)=1,x,x^2,x^3,x^4,x^5` can be integrated exactly:

.. math::
   :label: _auto41

        
        \int_{-1}^{1}1\,dx=2=\omega_0+\omega_1+\omega_2\,,
        
        

.. math::
   :label: _auto42

          
        \int_{-1}^{1}x\,dx=0=\omega_0x_0+\omega_1x_1+\omega_2x_2\,,
        
        

.. math::
   :label: _auto43

          
        \int_{-1}^{1}x^2\,dx=\frac{2}{3}=\omega_0x_0^2+\omega_1x_1^2+\omega_2x_2^2\,,
        
        

.. math::
   :label: _auto44

          
        \int_{-1}^{1}x^3\,dx=0=\omega_0x_0^3+\omega_1x_1^3+\omega_2x_2^3\,,
        
        

.. math::
   :label: _auto45

          
        \int_{-1}^{1}x^4\,dx=\frac{2}{5}=\omega_0x_0^4+\omega_1x_1^4+\omega_2x_2^4\,,
        
        

.. math::
   :label: _auto46

          
        \int_{-1}^{1}x^5\,dx=0=\omega_0x_0^5+\omega_1x_1^5+\omega_2x_2^5\,,
        
        

the solution to these equations are :math:`\omega_{0,1,2}=5/9, 8/9, 5/9` and :math:`x_{1,2,3}=-\sqrt{3/5},0,\sqrt{3/5}`. Below is a Python implementation:

.. code-block:: python

    def int_gaussquad2(lower_limit, upper_limit,func):
        x  = np.array([-np.sqrt(3./5.),0.,np.sqrt(3./5.)])
        w  = np.array([5./9., 8./9., 5./9.])
        xp = 0.5*(upper_limit-lower_limit)*x
        xp += 0.5*(upper_limit+lower_limit)
        area = np.sum(w*func(xp))
        return area*0.5*(upper_limit-lower_limit)

Note that the Gaussian quadrature converges very fast. From :math:`N=2` to :math:`N=3` function evaluation we reduce the error (in this specific case) 
from 6.5% to 0.1%. Our standard trapezoidal formula needs more than 20 function evaluations to achieve this, the Romberg method uses 4-5 function
evaluations. How can this be? If we use the standard Taylor formula for the function to be integrated, we know that for :math:`N=2` the Taylor 
formula must be integrated up to :math:`x^3`, so the error term is proportional to :math:`h^4f^{(4)}(\xi)` (where :math:`\xi` is some x-value in :math:`[a,b]`). 
:math:`h` is the step size, and we can replace it with :math:`h\sim (b-a)/N`, thus the error scale as :math:`c_N/N^4` (where :math:`c_N` is a constant). 
Following the same argument, we find for :math:`N=3` that the error term is :math:`h^6f^{(6)}(\xi)` or that the error term scale as :math:`c_N/N^6`. 
Each time we increase :math:`N` by a factor of one, the error term reduces by :math:`N^2`. Thus if we evaluate the integral for :math:`N=10`, 
increasing to :math:`N=11` will reduce the error by a factor of :math:`11^2=121`.

Error term on Gaussian Integration
----------------------------------
The Gaussian integration rule of order :math:`N` integrates exactly a polynomial of order :math:`2N-1`. 
From Taylors error formula, see equation :eq:`eq:taylor:error` in the chapter :ref:`ch:taylor`,
we can easily see that the error term must be of order :math:`2N`, and be proportional to :math:`f^{(2N)}(\eta)`, see [Ref1]_ for more details on the derivation of error terms. The drawback with an analytical error term derived from series expansion is that it involves the derivative of the function. As we have already explained, this is very unpractical and it is much more practical to use the methods described in the section :ref:`sec:numint:parct`. Let us consider this in more detail, assume that we evaluate the integral using first a Gaussian integration rule with :math:`N` points, and then :math:`N+1` points. Our estimates of the "exact" integral, :math:`I`,  would then be:

.. math::
   :label: eq:numint:gerr1

        
         I=I_N+ch_{N}^{2N},
        

.. math::
   :label: eq:numint:gerr2

          
         I=I_{N+1}+ch_{N+1}^{2N+1}.
        
        

In principle :math:`h_{N+1}\neq h_{N}`, but in the following we will assume that :math:`h_N\simeq h_{N+1}`, and :math:`h\ll 1`. Subtracting equation :eq:`eq:numint:gerr1` and :eq:`eq:numint:gerr2` we can show that a reasonable estimate for the error term :math:`ch^{2N}` would be:

.. math::
   :label: _auto47

        
        ch^N= I_{N+1}-I_N.
        
        

If this estimate is lower than a given tolerance we can be quite confident that the higher order estimate :math:`I_{N+1}` approximate the true integral within our error estimate. This is the method implemented in SciPy, `integrate.quadrature <https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.integrate.quadrature.html>`__
Common Weight functions for Classical Gaussian Quadratures
----------------------------------------------------------
Which method to use in a specific case?
---------------------------------------
There are no general answers to this question, and one need to decide from case to case. If computational speed is not an issue, 
and the function to be integrated can be evaluated at any points all the methods above can be used. If the function to be integrated 
is a set of observations at different times, that might be unevenly spaced, I would use the midpoint rule:

.. math::
   :label: _auto48

        
        I(a,b)=\int_a^bf(x)dx\simeq\sum_{k=0}^{N-1}M(x_k,x_k+h)=\sum_{k=0}^{N-1}h_if(x_k+\frac{h_i}{2})
        
        

This is because we do not know anything about the function between the points, only when it is observed, and the formula uses only 
the information at the observation points. There is a second more subtle reason, and that is the fact that in many cases the 
observations a different times are the {\it average} value of the observable quantity and it those cases the midpoint 
rule would be the exact answer. 

.. --- begin exercise ---

Exercise 3.1: Numerical Integration
-----------------------------------

**a)**
Show that for a linear function, :math:`y=a\cdot x+b` both the trapezoidal rule and the rectangular rule are exact

**b)**
Consider :math:`I(a,b)=\int_a^bf(x)dx` for :math:`f(x)=x^2`. The analytical result is :math:`I(a,b)=\frac{b^3-a^3}{3}`. Use the Trapezoidal and 
  Midpoint rule to evaluate these integrals and show that the error for the Trapezoidal rule is exactly twice as big as the Midpoint rule.

**c)**
Use the fact that the error term on the trapezoidal rule is twice as big as the midpoint rule to derive Simpsons formula: :math:`I(a,b)=\sum_{k=0}^{N-1}I(x_k,x_k+h)=\frac{h}{6}\left[f(a)+ 4f(a+\frac{h}{2})+2f(a+h)+4f(a+3\frac{h}{2})+2f(a+2h)+\cdots+f(b)\right]` Hint: :math:`I(x_k,x_k+h)=M(x_k,x_k+h)+E_M` (midpoint rule) and :math:`I(x_k,x_k+h)=T(x_k,x_k+h)+E_T=T(x_k,x_k+h)-2E_M` (trapezoidal rule).

.. --- begin solution of exercise ---

**Solution.**
Simpsons rule is an improvement over the midpoint and trapezoidal rule. It can be derived in different ways, we will make use of 
the results in the previous section. If we assume that the second derivative is reasonably well behaved on the interval :math:`x_k` 
and :math:`x_k+h` and fairly constant we can assume that :math:`f^{\prime\prime}(\eta)\simeq f^{\prime\prime}(\overline{\eta})`, hence :math:`E_T=-2E_M`.

.. math::
   :label: _auto49

        
        I(x_k,x_k+h)=M(x_k,x_k+h)+E_M\text{ (midpoint rule)}
        
        

.. math::
          
        I(x_k,x_k+h)=T(x_k,x_k+h)+E_T\nonumber
        

.. math::
   :label: _auto50

          
        =T(x_k,x_k+h)-2E_M\text{ (trapezoidal rule)},
        
        

we can now cancel out the error term by multiplying the first equation with 2 and adding the equations:

.. math::
   :label: _auto51

        
        3I(x_k,x_k+h)=2M(x_k,x_k+h)+T(x_k,x_k+h)
        
        

.. math::
   :label: _auto52

          
        =2f(x_k+\frac{h}{2}) h+\left[f(x_k+h)+f(x_k)\right] \frac{h}{2}
        
        

.. math::
   :label: _auto53

          
        I(x_k,x_k+h)=\frac{h}{6}\left[f(x_k)+4f(x_k+\frac{h}{2})+f(x_k+h)\right].
        
        

Now we can do as we did in the case of the trapezoidal rule, sum over all the elements:

.. math::
        
        I(a,b)=\sum_{k=0}^{N-1}I(x_k,x_k+h)\nonumber
        

.. math::
          
        =\frac{h}{6}\left[f(a)+ 4f(a+\frac{h}{2})+2f(a+h)+4f(a+3\frac{h}{2})\right.\nonumber
        

.. math::
   :label: _auto54

          
        \left.\qquad+2f(a+2h)+\cdots+f(b)\right]
        
        

.. math::
   :label: _auto55

          
        =\frac{h^\prime}{3}\left[f(a)+ f(b) + 4\sum_{k= \text{odd}}^{N-2}f(a+k h^\prime)+2\sum_{k= \text{even}}^{N-2}f(a+k h^\prime)\right],
        
        

note that in the last equation we have changed the step size :math:`h=2h^\prime`.

.. --- end solution of exercise ---

**d)**
Show that for :math:`N=2` (:math:`f(x)=1,x,x^3`), the points and Gaussian quadrature rule for :math:`\int_{0}^{1}x^{1/2}f(x)\,dx`
is :math:`\omega_{0,1}=-\sqrt{70}{150} + 1/3, \sqrt{70}{150} + 1/3`
and :math:`x_{0,1}=-2\sqrt{70}{63} + 5/9, 2\sqrt{70}{63} + 5/9`
1. Integrate :math:`\int_0^1x^{1/2}\cos x\,dx` using the rule derived in the exercise above and compare with the standard Gaussian quadrature rule for (:math:`N=2`, and :math:`N=3`).

**e)**
Make a Python program that uses the Midpoint rule to integrate experimental data that are unevenly spaced and given in the form of two arrays.

.. --- end exercise ---

.. !split

.. _ch:ode:

Ordinary differential equations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. !split

.. _ch:mc:

Monte Carlo Methods
%%%%%%%%%%%%%%%%%%%

.. !split

References
==========

.. [Ref1]
   **J. Stoer and R. Bulirsch**. *Introduction to Numerical Analysis*,
   Springer Science \& Business Media,
   2013.

