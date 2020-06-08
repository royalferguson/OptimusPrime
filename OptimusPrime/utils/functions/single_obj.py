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





