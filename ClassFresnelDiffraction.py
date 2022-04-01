# coding:UTF-8
"""
功能：模拟菲涅尔衍射光场演化过程
参数：振幅a，波长lmbd，距离z_1，衍射孔尺度width
输出：光强分布
作者：202128013920003刘夕铭
时间：2022.03.22@14.22
说明：以二维平面波进行模拟，突出振幅与空间的分布，其中u = x/(lmbd*z_1),v = y/(lmbd*z_1)
    E（x,y）=exp(i*k*z_1)/(i*lmbd*z_1)  *exp(jk/2*z_1*(x^2+y^2))  *fft2(a*exp(jk/2z*(x1^2+y1^2)))
      e    =          e_1               *              e_2             *            e_3
    参考资料：《物理光学》第四版.梁铨廷著、《应用光学》第二版.王文生著
    日用200W钨丝灯 光强为8e+6（cd）
    2cm的圆孔，波长600nm平行光，菲涅尔衍射区 z_1 >> 25cm 夫琅禾费衍射区 z_1 >> 160m
    100W灯泡，10m处，振幅A = 7.74（V/m），光强I为54.3（cd）
结论：根据不同的z_1值的输入，光强colorbar最大值呈现出随z_1的增加，先增加后减小再增加然后区域定值的样貌
思考：平行光首先通过矩形孔，光强大约A^2，分散在矩形孔内，但随着传播距离z_1的增加，光强越来越集中，随后趋于夫琅禾费衍射极限
类包：为菲涅尔衍射演化UI作基础
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


class FresnelDiffraction:
    epsilon = 8.85e-12  # 真空介电常数，单位:F/m
    miu = 4e-7 * np.pi  # 真空磁导率，单位:H/m

    @classmethod  # cls（类对象） 参数,为了以后可以修改参数的有效数字，FresnelDiffraction.epsilon = 8.8541878e-12
    def modify_parameter(cls, epsilon, miu):
        cls.epsilon = epsilon
        cls.miu = miu

    def __init__(self, a=7, lmbd=632.8e-9, z_1=10, b=0.02, h=0.04):
        self.a = a  # 平面波振幅，单位：V/m
        self.lmbd = lmbd  # 接收外部波长，单位：m
        self.k = 2 * np.pi / self.lmbd  # 波矢
        self.z_1 = z_1  # 菲涅尔衍射是近场衍射，传播距离，单位：m
        self.b = b  # 矩形孔的宽度，单位：m
        self.h = h  # 矩形孔的高度，单位：m
        self.step = 100  # 分割数量
        self.meshvectorx = np.linspace(-2 * self.b, 2 * self.b, self.step)  # 对指定区域指定数量进行分割
        self.meshvectory = np.linspace(-2 * self.h, 2 * self.h, self.step)

    def fresneldif(self):
        # 准备FFT的第一项
        meshx, meshy = np.meshgrid(self.meshvectorx, self.meshvectory)  # 创建网格
        fft_1 = self.a * self.rect(meshx, meshy, self.b, self.h)  # 对网格进行函数计算

        # 创建FFT的第二项
        fft_2 = np.exp(1j * self.k / (2 * self.z_1) * (meshx ** 2 + meshy ** 2))  # 将fft第二项作为打扰项Interrupt
        e_notshift = np.fft.fft2(fft_1 * fft_2)
        e_3 = np.fft.fftshift(e_notshift)

        # 准备E的第一第二项
        e_1 = np.exp(1j * self.k * self.z_1) / (1j * self.lmbd * self.z_1)
        e_2 = np.exp(1j * self.k / (2 * self.z_1) * (meshx ** 2 + meshy ** 2))
        e = e_1 * e_2 * e_3

        # 得到光强单位的量,由于u和v对应的x和y的关系，所以换算
        z_result = np.abs(e) ** 2
        z_result_inter = z_result * self.z_1 * self.lmbd * self.z_1 * self.lmbd
        z_result_final = 0.5 * np.sqrt(self.epsilon / self.miu) * z_result_inter
        return meshx, meshy, z_result_final

    # 类内测试代码
    def plotshow(self, plot_x, plot_y, plot_result):
        # 创建画布对象
        fig2 = plt.figure()
        fig2.canvas.manager.set_window_title('FresnelDiffractionEvolution')  # 画布对象标题

        # 画布方法创建轴
        ax2 = fig2.add_subplot()
        ax2.set_title('FresnelDiffraction,Z=%s(m)' % self.z_1)  # 轴对象设置标题
        ax2.set_xlabel('xDirection-Units:(m)')  # 轴对象坐标标识
        ax2.set_ylabel('yDirection-Units:(m)')

        # 画布轴绘图，建立强度等值线,使用'jet'颜色
        cont = plt.contourf(plot_x, plot_y, plot_result, cmap=cm.gray)
        cbar = plt.colorbar(cont)  # 建立等值线对象的颜色条
        cbar.set_label('Intensity-Units:(cd)')  # 建立coloerbar的标题

        # 显示图像
        plt.show()

    @staticmethod  # 静态方法不需要self（实例对象）以及cls（类对象）
    def rect(x_extent, y_extent, rect_b, rect_h):  # 创建rect函数
        threshold_b = rect_b / 2
        threshold_h = rect_h / 2
        r = np.zeros((x_extent.shape[0], x_extent.shape[1]))  # 在此一定记住np.zeros（）的参数是一个元组
        for i in range(1, x_extent.shape[0], 1):  # 要记得对应matlab for i = 1：size（x）[0]，需要用range（）创生表列，参数是 ‘起始，终止，步长’
            for j in range(1, x_extent.shape[1], 1):
                if (x_extent[i][j] < threshold_b) & (x_extent[i][j] > -threshold_b) & (y_extent[i][j] < threshold_h) & (
                        y_extent[i][j] > -threshold_h):  # 记住列表操作的x(i,j)是x[i][j]
                    r[i][j] = 1
        return r

    @staticmethod
    def circle(x_extent, y_extent, circle_radius):  # 创建circle函数
        r = np.zeros((x_extent.shape[1], x_extent.shape[0]))  # 在此一定记住np.zeros（）的参数是一个元组
        cr2 = circle_radius ** 2
        for i in range(1, x_extent.shape[1], 1):  # 要记得对应matlab for i = 1：size（x）[0]，需要用range（）创生表列，参数是 ‘起始，终止，步长’
            for j in range(1, x_extent.shape[0], 1):
                if (x_extent[i][j] ** 2 + y_extent[i][j] ** 2) < cr2:
                    r[i][j] = 1
        return r


if __name__ == '__main__':
    # 创建个实例
    a0 = FresnelDiffraction(z_1=10)  # 10m处看一看
    x0, y0, result0 = a0.fresneldif()
    a0.plotshow(x0, y0, result0)

