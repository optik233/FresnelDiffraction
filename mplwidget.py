# 要在GUI上画图 就得用一个matplotlib
# 然而GUI库里面没有plt小部件 所以得建立一个matplotlib小部件，需要的是界面尺寸管理、界面小部件、还有一个输出布局
from PyQt5.QtWidgets import QSizePolicy, QWidget, QVBoxLayout
# 后台的画布拿出来，准备把后台画布搬到小部件上去
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# 后台的工具条拿出来，准备把后台的工具条搬到小部件上去
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
# 准备图像属性，为画布绘图添加点属性
from matplotlib.figure import Figure
from matplotlib import rcParams # 字体参数管理
import matplotlib.gridspec as gds   # 想在子图2上画子图1的colorbar，未实现过程
# 包含类的py文件

rcParams['font.size'] = 9


class MplCanvas(FigureCanvas):  # 小部件的画布（后台画布）

    def __init__(self):
        self.fig = Figure()  # 建立图像区域
        gs00 = gds.GridSpec(1, 2, width_ratios=[10, 1])
        self.ax = self.fig.add_subplot(111)  # 建立图像的轴
        self.cax = self.fig.add_subplot(gs00[1])
        FigureCanvas.__init__(self, self.fig)  # 把fig放在后台画布上，并且后台画布初始化在mpl画布上，画布上的呈现的是刚建立的fig
        # 改一下尺寸
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 系统更新布局
        FigureCanvas.updateGeometry(self)


class MplWidget(QWidget):  # mpl小部件（全部小部件）；；要添加的类名字
    # mpl的小部件要放在QtDesigner里面
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)  # 继承小部件的所有初始化条件
        # 建立小部件画布
        self.canvas = MplCanvas()
        # 为画布创建一个导航条，创建给窗口自己
        self.navi_toolbar = NavigationToolbar(self.canvas, self)
        # 创建一个垂直布局
        self.vbl = QVBoxLayout()
        self.vbl.addWidget(self.canvas) # 布局上添加画布
        self.vbl.addWidget(self.navi_toolbar)   # 布局下添加工具条
        self.setLayout(self.vbl)    # 设置布局
