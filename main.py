"""
main.py

功能: 桌面控件主程序
时间: 2025/12/01
版本: 1.0
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Callable

from PyQt5.QtCore import Qt, QTimer, QPoint, QEvent
from PyQt5.QtWidgets import QApplication, QWidget, QMenu, QAction
from PyQt5.QtGui import QPainter, QColor, QPixmap, QPainterPath, QPen, QMouseEvent, QPaintEvent


class FloatingBall(QWidget):
    """实现桌面控件的界面及相关函数调用"""

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(60, 60)

        self.setMouseTracking(True)
        self.under_mouse = False

        self.menu_visible = False
        self.dragging = False
        self.drag_position = QPoint()

        self.long_press_timer = QTimer()
        self.long_press_timer.setSingleShot(True)
        self.long_press_timer.timeout.connect(self.start_drag)

        self.menu = QMenu()

        self.menu.setStyleSheet(
            """
            QMenu {
                background-color: white;
                color: black;
                border: 1px solid #ccc;
            }
            QMenu::item {
                padding: 5px 20px;
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: #e6f0ff;
                color: black;
            }
            """
        )

        # 路径和网址
        self.ICON_PATH = "data/icon.png"

        self.BASE_DIR = Path("D:/My Programs")
        self.code_work = self.BASE_DIR / "AutoWork"
        self.code_ui = self.BASE_DIR / "DeskUI"
        self.code_box = self.BASE_DIR / "FaunaBox"
        self.code_folio = self.BASE_DIR / "MyPortfolio"
        self.code_stock = self.BASE_DIR / "Stock Indicators"

        self.url_bilibili = "https://www.bilibili.com"
        self.url_deepseek = "https://chat.deepseek.com"
        self.url_chatgpt = "https://chatgpt.com"

        self.baidu_path = "D:/BaiduNetdiskDownload"

        # 菜单项
        self.add_menu_item("mstsc", lambda: subprocess.Popen("mstsc"))

        # 写代码子菜单
        code_actions = {
            "LeetCode": learn_leetcode,
            "AutoWork": lambda: open_path_in_vscode(self.code_work),
            "FaunaBox": lambda: open_path_in_vscode(self.code_box),
            "DeskUI": lambda: open_path_in_vscode(self.code_ui),
            "Portfolio": lambda: open_path_in_vscode(self.code_folio),
            "Stock": lambda: open_path_in_vscode(self.code_stock),
        }
        self.add_sub_menu_item("代码", code_actions)

        # 网站子菜单
        edge_actions = {
            "bilibili": lambda: open_url_in_edge(self.url_bilibili),
            "DeepSeek": lambda: open_url_in_edge(self.url_deepseek),
            "ChatGPT": lambda: open_url_in_edge(self.url_chatgpt)
        }
        self.add_sub_menu_item("网站", edge_actions)

        # 文档子菜单
        dir_actions = {
            "回收站": lambda: subprocess.Popen("explorer shell:RecycleBinFolder"),
            "下载": lambda: subprocess.Popen("explorer shell:Downloads"),
            "百度云": lambda: os.startfile(self.baidu_path),
        }
        self.add_sub_menu_item("文档", dir_actions)

        self.add_menu_item("退出", QApplication.quit)

    def add_menu_item(self, title: str, callback: Callable[[], None]) -> None:
        """向菜单添加一个新选项"""
        action = QAction(title, self)
        action.triggered.connect(callback)
        self.menu.addAction(action)

    def add_sub_menu_item(self, title: str, actions: dict[str, Callable[[], None]]) -> None:
        """添加子菜单"""
        sub_menu = QMenu(title, self.menu)
        for subtitle, func in actions.items():
            action = QAction(subtitle, self)
            action.triggered.connect(func)
            sub_menu.addAction(action)
        self.menu.addMenu(sub_menu)

    def start_drag(self) -> None:
        """开始拖拽悬浮球"""
        self.dragging = True
        self.setCursor(Qt.ClosedHandCursor)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """处理鼠标按下事件，准备拖拽"""
        if event.button() == Qt.LeftButton:
            self.activateWindow()
            self.raise_()
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.long_press_timer.start(100)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """处理鼠标移动事件，实现拖拽效果"""
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """处理鼠标释放事件，结束拖拽或显示菜单"""
        self.long_press_timer.stop()
        if self.dragging:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)
        else:
            self.activateWindow()
            self.raise_()
            self.show_menu()

    def show_menu(self) -> None:
        """在悬浮球下方显示功能菜单"""
        self.menu.move(self.x(), self.y() + self.height())
        self.menu.show()
        self.menu_visible = True

    def paintEvent(self, event: QPaintEvent) -> None:
        """绘制悬浮球的圆形外观和图标"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. 裁剪为圆形区域
        path = QPainterPath()
        path.addEllipse(0, 0, self.width(), self.height())
        painter.setClipPath(path)

        # 2. 贴图（缩放 + 绘制）
        pixmap = QPixmap(self.ICON_PATH)
        pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        painter.drawPixmap(0, 0, pixmap)

        # 3. 平时边框（默认是深灰）
        border_color = QColor(80, 80, 80)

        # 4. 悬停特效（边框变亮或加发光感）
        if self.under_mouse:
            border_color = QColor(200, 200, 200)

        # 5. 绘制边框
        pen = QPen(border_color)
        pen.setWidth(4)  # 设置边框宽度（比如 4 像素）
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(2, 2, self.width() - 4, self.height() - 4)

    def enterEvent(self, event: QEvent) -> None:
        """鼠标进入悬浮球区域"""
        self.under_mouse = True
        self.update()

    def leaveEvent(self, event: QEvent) -> None:
        """鼠标离开悬浮球区域"""
        self.under_mouse = False
        self.update()


def open_url_in_edge(url: str) -> None:
    """打开网页"""
    subprocess.Popen(f"start msedge {url}", shell=True)


def open_path_in_vscode(project_dir: str, vscode_path: str = "D:/Program Files (x86)/Microsoft VS Code/Code.exe") -> None:
    """打开 VsCode 项目"""
    subprocess.Popen([vscode_path, project_dir])


def learn_leetcode() -> None:
    """学习力扣"""
    open_path_in_vscode("D:/Machine Learning/LeetCode")
    open_url_in_edge("https://leetcode.cn/problemset/")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ball = FloatingBall()
    ball.move(2000, 200)
    ball.show()
    sys.exit(app.exec_())
