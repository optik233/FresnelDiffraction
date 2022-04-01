"""
功能：模拟菲涅尔衍射光场演化过程
参数：波矢k，位矢r
输出：光场分布
作者：202128013920003刘夕铭
时间：2022.03.22@14.22
说明：以二维平面波进行模拟，突出振幅与空间的分布
    E（x,y）=exp(i*k*z_1)/(i*lambda*z_1)*fft(E(x1,y1)*exp(jk/2z*(x1^2+y1^2)))
"""
import matplotlib.pyplot as plt
import numpy as np


def rect(x_extent, y_extent, rect_width):  # 创建rect函数，記住条件和定义后面都要有：表示开始
    threshold = rect_width / 2
    r = np.zeros((x_extent.shape[1], x_extent.shape[0]))  # 在此一定记住np.zeros（）的参数是一个元组

    for i in range(1, x_extent.shape[1], 1):  # 要记得对应matlab for i = 1：size（x）[0]，需要用range（）创生表列，参数是 ‘起始，终止，步长’
        for j in range(1, x_extent.shape[0], 1):
            if (x_extent[i][j] < threshold) & (x_extent[i][j] > -threshold) & (y_extent[i][j] < threshold) & (
                    y_extent[i][j] > -threshold):  # 记住列表操作的x(i,j)是x[i][j]
                r[i][j] = 1
    return r


# 孔径平面的初始参数
A = 1e-9  # 平面波振幅
lmbd = 632.8e-9  # 632.8nm
k = 2 * np.pi / lmbd  # 波矢
z_1 = 2e-7  # 菲涅尔衍射是近场衍射，传播距离，单位：m
width = 600e-9  # 衍射效果明显时，孔径尺度要与波长相近
step = 100  # 分割数量
meshvector = np.linspace(-2 * width, 2 * width, step)  # 对指定区域指定数量进行分割

# 准备FFT的第一项
x, y = np.meshgrid(meshvector, meshvector)  # 创建网格
FFT_1 = A * rect(x, y, width)  # 对网格进行函数计算

# 创建FFT的第二项
FFT_2 = np.exp(1j * k / (2 * z_1) * (x ** 2 + y ** 2))  # 将fft第二项作为打扰项Interrupt
E_notshift = np.fft.fft2(FFT_1 * FFT_2)
E_3 = np.fft.fftshift(E_notshift)

# 准备E的第一第二项
E_1 = np.exp(1j * k * z_1) / (1j * lmbd * z_1)
E_2 = np.exp(1j * k / (2 * z_1) * (x ** 2 + y ** 2))
E = E_1 * E_2 * E_3

# 得到光强单位的量
result = np.abs(E) ** 2

# 创建画布对象
fig2 = plt.figure()
fig2.canvas.manager.set_window_title('FresnelDiffraction')  # 画布对象标题

# 画布方法创建轴
ax2 = fig2.add_subplot()
ax2.set_title('FresnelDiffraction')  # 轴对象设置标题
ax2.set_xlabel('xDirection-Units:(m)')  # 轴对象坐标标识
ax2.set_ylabel('yDirection-Units:(m)')

# 画布轴绘图
cont = plt.contourf(x / lmbd / z_1, y / lmbd / z_1, result)  # 建立强度等值线
cbar = plt.colorbar(cont)  # 建立等值线对象的颜色条
cbar.set_label('Intensity-Units:(cd)')  # 建立coloerbar的标题

# 显示图像
plt.show()
