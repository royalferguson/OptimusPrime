from scipy.optimize import rosen as sprosen
import numpy as np


def rosenbrock(x):
    '''
    Rosenbrock Function - non-convex
    global minimum: f(x=1,x2=1,....xn=1) = 0
    bounds: -5 <= Xi <= 10
    '''
    return sprosen(x)


def rosen_ignoredDV(x):
    '''
    Rosenbrock Function that Ignors X0
    non-convex,
    global minimum: f(x=1,x2=1,....xn=1) = 0
    bounds: -5 <= Xi <= 10
    '''
    # ignore x0:
    result = rosenbrock(x[1:])
    return result



def rastrigin(x):
    '''
    Rastrigin Function - non-linear, multi-modal, many local minima
    global minimum: f(x=0,x2=0,....xn=0) = 0
    bounds: -5.12 <= Xi <= 5.12
    '''
    x = np.array(x)
    return 10*len(x) + np.sum(x*x - 10*np.cos(2*np.pi*x))

def ackley(x):
    '''
    Ackley Function - Large Number of local minima
    global minimum: f(x=0,x2=0,....xn=0) = 0
    bounds: -32.768 <= Xi <= 32.768
    '''
    d = len(x)
    return -20.0 * np.exp(-0.2 * np.sqrt((1 / d) * (x ** 2).sum()) ) - np.exp(1/float(d) * np.cos(2 * np.pi * x).sum()) + np.e + 20

def sphere(x):
    '''
    Sphere Function
    global minimum: f(x=0,x2=0,....xn=0) = 0
    bounds: -5.12 <= Xi <= 5.12
    '''
    return np.sum(np.power(np.array(x),2))

def beale(x):
    '''
    Beale Function
    global minimum: f(x=3, y=0.5) = 0
    bounds: -4.5 <= x, y <= 4.5
    '''
    return ( ((1.500 - x[0] + x[0]*x[1])**2) + ((2.250 - x[0] + x[0]*x[1]**2)**2) + ((2.625 - x[0] + x[0]*x[1]**3)**2) )

def goldsteinprice(x):
    '''
    Goldstein-Price Function
    global minimum: f(x=0, y=-1) = 3
    bounds: -2 <= x, y <= 2
    '''
    x,y = x[0],x[1]
    firstPart = 1 + ((x+y+1)**2) * (19 - 14*x + (3*(x**2)) - 14*y + 6*x*y + (3*(y**2)) )
    secondPart = 30 + ((2*x-3*y)**2) * (18 - 32*x + (12*(x**2)) + 48*y - 36*x*y + 27*(y**2) )
    return firstPart * secondPart

def booth(x):
    '''
    Booth Function
    global minimum: f(x=1, y=3) = 0
    bounds: -10 <= x, y <= 10
    '''
    x,y = x[0],x[1]
    return (x+2*y-7)**2 + (2*x+y-5)**2

def bukin6(x):
    '''
    Bukin N.6 Function
    global minimum: f(x=-10, y=1) = 0
    bounds: -15 <= x <= -5
            -3 <= y <= 3
    '''
    x,y = x[0],x[1] 
    return (100 * np.sqrt(np.abs(y - 0.01*(x**2)))) + 0.01*np.abs(x+10)

def matyas(x):
    '''
    Matyas Function
    global minimum: f(x=0, y=0) = 0
    bounds: -10 <= x, y <= 10
    '''
    x,y = x[0],x[1]
    return 0.26*((x**2) + (y**2)) - 0.48*x*y

def levi13(x):
    '''
    Levi N.13 Function 
    global minimum: f(x=1, y=1) = 0
    bounds: -10 <= x, y <= 10
    '''
    x,y = x[0],x[1]
    return (np.sin(3.0*np.pi*x)**2) + ((x-1)**2) * (1+np.sin(3.0*np.pi*y)**2) + ((y-1)**2) * (1+np.sin(2.0*np.pi*y)**2)

def himmelblau(x):
    '''
    Himmelblau Function
    global minimum(s): f(x=3.0, 2.0) = 0
        f(x=-2.805118, y=3.131312) = 0
        f(x=-3.779310, y=-3.283186) = 0
        f(x=3.584428, y=-1.848126) = 0
    bounds: -5 <= x, y <= 5
    '''
    x,y = x[0],x[1]
    return ((x**2)+y-11)**2 + (x+(y**2)-7)**2

def threehumpcamel(x):
    '''
    Three-Hump Camel Function
    global minimum: f(x=0, y=0) = 0
    bounds: -5 <= x, y <= 5
    '''
    x,y = x[0],x[1]
    return 2*(x**2) - (1.05*(x**4)) + ((x**6)/6) + x*y + y**2

def easom(x):
    '''
    Easom Function
    global minimum: f(x=pi, y=pi) = -1
    bounds: -100 <= x, y <= 100
    '''
    x,y = x[0],x[1]
    return -np.cos(x)*np.cos(y)*np.exp(-( (x-np.pi)**2 + (y-np.pi)**2 ))

def crossintray(x):
    '''
    Cross-In-Tray Function
    global minimum(s): f(x=1.3491, 1.3491) = -2.06261
        f(x=-1.3491, y=1.3491) = -2.06261
        f(x=1.3491, y=-1.3491) = -2.06261
        f(x=-1.3491, y=-1.3491) = -2.06261
    bounds: -10 <= x, y <= 10
    '''
    x,y = x[0],x[1]
    innerPart = np.exp(np.abs(100- (np.sqrt(x**2 + y**2)/np.pi) ))
    return -0.0001*(np.power(np.abs(np.sin(x) * np.sin(y) * innerPart) + 1,0.1))

def eggholder(x):
    '''
    Eggholder Function
    global minimum: f(x=512, y=404.2319) = -959.6407
    bounds: -512 <= x, y <= 512
    '''
    x,y = x[0],x[1]
    return -(y+47) * np.sin(np.sqrt(np.abs(x/2 + (y+47)))) - x*np.sin(np.sqrt(np.abs(x - (y+47))))

def holdertable(x):
    '''
    Holder Table Function
    global minimum(s): f(x=8.05502, 9.66459) = -19.2085
        f(x=-8.05502, 9.66459) = -19.2085
        f(x=8.05502, -9.66459) = -19.2085
        f(x=-8.05502, -9.66459) = -19.2085
    bounds: -10 <= x, y <= 10
    '''
    x,y = x[0],x[1]
    return -np.abs(np.sin(x) * np.cos(y) * np.exp(np.abs(1 - np.sqrt(x**2 + y**2)/np.pi)))

def mccormick(x):
    '''
    McCormick Function
    global minimum: f(x=-0.54719, y=-1.54719) = -1.9133
    bounds: -1.5 <= x <= 4
            -3 <= y <= 4
    '''
    x,y = x[0],x[1]
    return np.sin(x+y) + (x-y)**2 - 1.5*x + 2.5*y + 1

def schaffer2(x):
    '''
    Schaffer N.2 Function
    global minimum: f(x=0, y=0) = 0
    bounds: -100 <= x, y <= 100
    '''
    x,y = x[0],x[1]
    return 0.5  +  (np.power(np.sin(x**2 - y**2),2) - 0.5)/np.power(1+0.001*(x**2+y**2),2)

def schaffer4(x):
    '''
    Schaffer N.4 Function
    global minimum: f(x=0, y=1.253115) = 0.292579
    bounds: -100 <= x, y <= 100
    '''
    x,y = x[0],x[1]
    return 0.5  +  (np.power(np.cos(np.sin(np.abs(x**2 - y**2))),2) - 0.5)/np.power(1+0.001*(x**2+y**2),2)

def styblinskitang(x):
    '''
    Styblinski-Tang Function
    global minimum: n * -39.16617 <= f(-2.903534,...,-2.903534) <= n * -39.16616
    bounds: -5 <= x_i <= 5
    '''
    return sum([item**4 - 16*item**2 + 5*item for item in x]) / 2.0

def powell(x):
    '''
    Powell Function
    global minimum: f(x=0,x2=0,....xn=0) = 0
    bounds: -4 <= Xi <= 5
    '''
    x = np.array(x)
    xlen = len(x)
    xa = x[np.linspace(0,xlen-4,int(xlen/4)).astype(int)]
    xb = x[np.linspace(1,xlen-3,int(xlen/4)).astype(int)]
    xc = x[np.linspace(2,xlen-2,int(xlen/4)).astype(int)]
    xd = x[np.linspace(3,xlen-1,int(xlen/4)).astype(int)]
    s1 = (xa + 10*xb)**2
    s2 = 5 * (xc - xd)**2
    s3 = (xb - 2*xc)**4
    s4 = 10 * (xa - xd)**4
    return sum(s1 + s2 + s3 + s4)


def sumofdifferentpowers(x):
    '''
    sumOfDifferentPowers Function
    global minimum: f(x=0,x2=0,....xn=0) = 0
    bounds: -1 <= Xi <= 1
    '''
    xpow = np.arange(1,len(x)+1)
    return np.sum(np.power(x,xpow+1))

def schwefel(x):
    '''
    schwefel Function
    global minimum: f(x=420.9687,x2=420.9687,....xn=420.9687) = 0
    bounds: -500 <= Xi <= 500
    '''
    return 418.9829*len(x) - sum([i * np.sin(np.sqrt(np.abs(i))) for i in x])



def dd6func(X,for_minimize=True,intermixed=False):
    '''
    Define a composite function of a multi-D X vector
    This is for dimension n=6.
    The optimum value is at Xopt = [1,-1,1,-1,1,-1]
    With for_minimize=True the optimum is a minimum of 1e-6;
    for_minimize=False gives a maximum of 1.0 at Xopt.
    '''
    # Keep track of the evaluations count
    global EVALUATION_COUNT
    EVALUATION_COUNT += 1
    X = np.array(X)
    # Inter-mix the parameters? (True), or keep separate? (False)
    # Seems 'easier' to solve when kept separate.
    # In either case, adjust the values so that the maximum happens for
    # the input:  X = [1,-1,1,-1,1,-1]
    if intermixed:
        # Combine parameters in +/- pairs to inter-mix the underlying model parameters.
        xa = 1+(X[0]+X[3])/2
        xb = 2+(X[1]+X[5])/2
        xc = -1+(X[2]+X[4])/2
        xd = -1+(X[0]-X[3])/2
        xe = (X[1]-X[5])/2
        xf = (X[2]-X[4])/2
    else:
        # Keep parameters separate, just adding an offset.
        xa = X[0]+0
        xb = X[1]+2
        xc = X[2]-1
        xd = X[3]+1
        xe = X[4]-1
        xf = X[5]+1
    ##print(xa,xb,xc,xd,xe,xf)
    # This combined function has its maximum of 1.0 at:
    #     [xa,xb,xc,xd,xe,xf] = [1,1,0,0,0,0]
    value = ( rosen_ab([xa,xb],1.0,5.0) +
                       0.1*rastrigin([xc,xd]) )
    # The 0.22 was tuned so that the 2nd-place 
    # the mis-optimized [1,-1,0,-1,0,-1] gives just at/below 0.95
    value = (0.75*np.exp(-0.22*np.sqrt(value)) +
                 0.25*np.exp(-0.07*sphere([xe,xf])))
    # Remove the three sub-function evaluations from the evaluation count:
    EVALUATION_COUNT -= 3
    # Select the range of the function:
    # for_minimize=True is like usual OF, goes from min at 0 to inf
    # for_minimize=False is like an efficiency, 0 to a max at 1.
    if for_minimize:
        return -np.log(value-1.e-6)   # -1.e-6 ensures the log is positive.
    else:
        return value

def dd8func(X,for_minimize=True,intermixed=False):
    '''
    This d=8 composite function is the dd6func with two more Xs:
    one each added to the Rosenbrock and Rastrigin components.
    The optimum is similarly at [1,-1,1,-1,1,-1,1,-1]
    Here, X[0,1,4,5,6,7] map to the previous dd6 values:
          X[0,1,2,3,4,5]
    and X[2] and X[3] are added inputs to the Rosenbrock and Rastrigin
    functions.
    ---
    Define a composite function of a multi-D X vector
    This is for dimension n=6.
    The optimum value is at Xopt = [1,-1,1,-1,1,-1]
    With for_minimize=True the optimum is a minimum of 1e-6;
    for_minimize=False gives a maximum of 1.0 at Xopt.
    '''
    # Keep track of the evaluations count
    global EVALUATION_COUNT
    EVALUATION_COUNT += 1
    X = np.array(X)
    # Inter-mix the parameters? (True), or keep separate? (False)
    # Seems 'easier' to solve when kept separate.
    # In either case, adjust the values so that the maximum happens for
    # the input:  X = [1,-1,1,-1,1,-1,1,-1]
    if intermixed:
        # Combine parameters in +/- pairs to inter-mix the underlying model parameters.
        xa = 1+(X[0]+X[5])/2
        xb = 2+(X[1]+X[7])/2
        xc = -1+(X[4]+X[6])/2
        xd = -1+(X[0]-X[5])/2
        xe = (X[1]-X[7])/2
        xf = (X[4]-X[6])/2
    else:
        # Keep parameters separate, just adding an offset.
        xa = X[0]+0
        xb = X[1]+2
        xc = X[4]-1
        xd = X[5]+1
        xe = X[6]-1
        xf = X[7]+1
    ##print(xa,xb,xc,xd,xe,xf)
    # This combined function has its maximum of 1.0 at:
    #     [xa,xb,X2,X3,xc,xd,xe,xf] = [1,1,1,0,0,0,0,0]
    value = ( rosen_ab([xa,xb,X[2]],1.0,16.0) +     # <-- b=16
                       0.1*rastrigin([X[3]+1,xc,xd]) )
    # (In dd6func) The 0.22 was tuned so that the 2nd-place 
    # the mis-optimized [1,-1,0,-1,0,-1] gives just at/below 0.95
    value = (0.75*np.exp(-0.22*np.sqrt(value)) +
                 0.25*np.exp(-0.07*sphere([xe,xf])))
    # Remove the three sub-function evaluations from the evaluation count:
    EVALUATION_COUNT -= 3
    # Select the range of the returned function:
    #   for_minimize=True is like usual OF, goes from min near 0 to inf,
    #   for_minimize=False is like an efficiency, 0 to a max at 1.
    if for_minimize:
        return -np.log(value-1.e-6)   # -1.e-6 ensures the log is positive.
    else:
        return value


