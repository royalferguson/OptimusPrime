import numpy as np

#  utils.get_random_x0(((popsize * #dv),#dv),min_value,max_value)
#dv=5
#popsize=2
# utils.get_random_x0(10,5),min_value,max_value)


# with 5 Decision Variables and a popsize of 2
count=(10,5)
x0 = np.random.uniform(-5, 10, (count[0], count[1]))
print(x0)
print(x0.shape)

len_x0=x0.shape[1]
print(len_x0)


print("==================================")

x0 = [1.3, 0.7, 0.8, 1.9, 1.1]
popsize = 2
print("x0 before array build:  ", len(x0))
print(x0)

print("==================================")

x1 = np.array([np.array(x0) for i in range(popsize*len(x0))])
len_x1=x1.shape[1]
print("x1: ", len_x1)
print(x1)

print("==================================")

#np.array(n * a).reshape(n, -1)
x2=np.array(10 * x0)
print(x2.shape)
print(x2)

x3=x2.reshape(10,-1)
print(x3)
x3=x2.reshape(-1,5)
print(x3)

print("==================================")
shape=20
seed=3
x4=np.full(shape, seed)
print("length of shape: ", len(x4.shape))
print(x4.shape)
print(x4)

