"""
作者：202128013920003 刘夕铭
机构：中国科学院长春光学精密机械与物理研究所
功能：演示菲涅尔衍射的演化
版本：Version 4
最后更改时间：2022.03.29@14.19
参考：《Understanding Optics with Python》 Vasudevan Lakshminarayanand等著，夫琅禾费衍射的UI设计
"""


from PyQt5.QtWidgets import QApplication, QMainWindow
# QApplication 包含窗口系统和其他来源处理过和发送过的主事件循环，也处理应用程序初始化和收尾。管理对话
# QMainWindow  QMainWindow()可以创建一个应用程序的窗口。MainWindow的结构分为五个部分：菜单栏（Menu Bar）工具栏（Toolbars）、
# 停靠窗口（Dock Widgets）、状态栏（Status Bar）和中央窗口（Central Widget） 中央窗口可以使用任何形式的widget来填充
# 总结来说 QApplication 是控制模块，负责载入QT架构；； QMainWindow 是显示模块，负责把自己的UI显示出来
from PyQt5.QtCore import pyqtSlot  # 槽函数命令
from FresnelDiffractionUI import Ui_MainWindow  # 把QT创建的UI界面导进来
from numpy import pi, linspace, meshgrid, sin
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from ClassFresnelDiffraction import FresnelDiffraction
import matplotlib.colorbar as colorbars
# 创建我自己的UI类，继承于QT自创的Ui_MainWindow
class FresnelDiffractionApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)  # 主窗口初始化在自己的APP窗口上
        self.setupUi(self)  # QT生成的setupUI的函数，是UI_MainWindow里面的方法 在刚生成的主窗口上面进行我们的初始化
        self.fig1() # 建立一个图像

    def fig1(self):

        lmbd = self.SliderLambda.value() * 1e-9    # 接收外部波长，单位：m
        b = self.SliderB.value() * 1e-2    # 矩形孔的宽度，单位：m
        h = self.SliderH.value() * 1e-2    # 矩形孔的高度，单位：m
        z_1 = self.SliderZ1.value()    # 菲涅尔衍射是近场衍射，传播距离，单位：m
        a = self.SliderA.value()   # 平面波振幅，单位：V/m

        X_Mmax = a/2
        X_Mmin = -a/2
        Y_Mmax = X_Mmax
        Y_Mmin = X_Mmin
        N = 10

        a0 = FresnelDiffraction(a=a, lmbd=lmbd, z_1=z_1, b=b, h=h)
        x0, y0, result0 = a0.fresneldif()
        mpl = self.mplwidget.canvas # 在小部件的画布上作图，创建一个小部件对象 部件名称self.mplwidget
        mpl.ax.clear()
        mpl.cax.clear()
        mpl.ax.contourf(x0, y0, result0, cmap='gray')
        mpl.ax.set_xlabel(u'$X(e-2m)$', fontsize=12, fontweight='bold')
        mpl.ax.set_ylabel(u'$Y(e-2m)$', fontsize=12, fontweight='bold')
        mpl.ax.set_xticklabels(linspace(X_Mmin, X_Mmax, N, endpoint=False))
        mpl.ax.set_yticklabels(linspace(Y_Mmin, Y_Mmax, N, endpoint=False))
        mpl.figure.suptitle('Fresnel Diffraction by rectangular aperture', fontsize=10, fontweight='bold')
        mpl.ax.set_title(r'$\lambda = %2fm, b = %2fm, h = %2fm, z_1 = %sm$' % (lmbd, b, h, z_1), fontsize=10)
        mpl.draw()

    @pyqtSlot("int")
    def on_SpinBoxLambda_valueChanged(self, value):
        self.SliderLambda.setValue(value)

    @pyqtSlot("int")
    def on_SpinBoxB_valueChanged(self, value):
        self.SliderB.setValue(value)

    @pyqtSlot("int")
    def on_SpinBoxH_valueChanged(self, value):
        self.SliderH.setValue(value)

    @pyqtSlot("int")
    def on_SpinBoxA_valueChanged(self, value):
        self.SliderA.setValue(value)

    @pyqtSlot("int")
    def on_SpinBoxZ1_valueChanged(self, value):
        self.SliderZ1.setValue(value)

    @pyqtSlot("int")
    def on_SliderLambda_valueChanged(self, value):
        self.SpinBoxLambda.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_SliderB_valueChanged(self, value):
        self.SpinBoxB.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_SliderH_valueChanged(self, value):
        self.SpinBoxH.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_SliderA_valueChanged(self, value):
        self.SpinBoxA.setValue(value)
        self.fig1()

    @pyqtSlot("int")
    def on_SliderZ1_valueChanged(self, value):
        self.SpinBoxZ1.setValue(value)
        self.fig1()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    FresnelDiffractionApplication = FresnelDiffractionApp()
    FresnelDiffractionApplication.show()  # 显示主窗口
    sys.exit(app.exec_())  # 退出
