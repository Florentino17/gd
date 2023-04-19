import torch
data = torch.tensor([
    [4.2589,4.1893],
    [4.6232,3.0388],
    [1.5079,-1.2669],
    [4.6535,5.9372],
    [3.5294,2.5478],
    [1.3902,-1.1850],
    [2.1140,-0.0451],
    [3.1875,1.0716],
    [4.8300,4.9539],
    [4.8596,3.9318],
    [1.6305,-0.8507],
    [4.8824,3.6177],
    [4.8287,3.5885],
    [2.9415,0.0735],
    [4.2011,0.4580],
    [1.5675,-0.4265],
    [2.6870,0.6993],
    [4.6629,3.5710],
    [4.1688,4.7080],
    [4.8380,2.9644]])
import matplotlib.pyplot as plt
def f(x):
    # return 3*(x[0]-1)**2 + 2*(x[1]-2)**2  #原函数定义式
    sum=0
    for i in range(0,data.size()[0]):
        sum+=(x[0]*data[i][0]+x[1]-data[i][1])**2
        # print((x[0]*data[i][0]-data[i][1])**2)
    return sum
def f_grad(x):
    # return torch.tensor([6*(x[0]-1),4*(x[1]-2)])  #求导后的式子
    sum1=0
    sum2=0
    for i in range(0,data.size()[0]):
        sum1+=2*data[i][0]*(x[0]*data[i][0]+x[1]-data[i][1])
        sum2+=2*(x[0]*data[i][0]+x[1]-data[i][1])
    sum1/=20
    sum2/=20
    return torch.tensor([sum1,sum2])
x0 = torch.tensor([10,10])   #初始x1,x2
eta = 0.001               #初始学习率
f0 = f(x0)                  #计算初始y

x_record = [x0]             #记录，为了画图
f_record = [f0]

num_steps = 50000              #十次迭代
for i in range(num_steps):      
    x_new = x0 - eta*f_grad(x0)  #计算eta*f_grad(x0)，即向梯度反向传播
    f_new = f(x_new)        #计算新的y值
    if (i%1000==0):
        print(f_new)
    x0 = x_new
    f0 = f_new
    x_record.append(x0)             #画图
    f_record.append(f0)
##20.3718

## 远程1m20s
## 本地3m04s