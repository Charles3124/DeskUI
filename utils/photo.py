import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QScrollArea, QGridLayout, QPushButton, QFileDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ImageViewer(QWidget):

    def __init__(self, root_path: str) -> None:
        super().__init__()
        self.root_path = root_path
        self.setWindowTitle("图片浏览器")

        self.is_dark_mode = True  # 默认夜间模式

        self.init_ui()
        self.load_folders()
        self.apply_dark_mode()  # 初始应用夜间模式

        self.showMaximized()

    def init_ui(self):
        """设置主界面布局，包括文件夹列表、图片展示区域和切换按钮"""
        main_layout = QVBoxLayout(self)
        
        # 顶部按钮布局
        btn_layout = QHBoxLayout()
        self.toggle_mode_btn = QPushButton("切换到日间模式")
        self.toggle_mode_btn.clicked.connect(self.toggle_mode)
        btn_layout.addWidget(self.toggle_mode_btn)
        btn_layout.addStretch()

        # 主体布局（文件夹列表 + 图片区域）
        body_layout = QHBoxLayout()

        # 文件夹列表
        self.folder_list = QListWidget()
        self.folder_list.itemClicked.connect(self.display_images)
        body_layout.addWidget(self.folder_list, 1)

        # 图片显示区（带滚动条）
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.image_container = QWidget()
        self.grid = QGridLayout(self.image_container)
        self.scroll.setWidget(self.image_container)
        body_layout.addWidget(self.scroll, 4)

        # 全屏显示标签（点击退出全屏）
        self.fullscreen_label = QLabel(self)
        self.fullscreen_label.setAlignment(Qt.AlignCenter)
        self.fullscreen_label.hide()
        self.fullscreen_label.mousePressEvent = self.exit_fullscreen
        self.fullscreen_label.setCursor(Qt.PointingHandCursor)

        # 组合布局
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(body_layout)

        # 初始化变量
        self.current_images = []
        self.current_index = 0
        self.setFocusPolicy(Qt.StrongFocus)

    def load_folders(self):
        """加载根目录下的所有子文件夹并显示在列表中"""
        folders = [f for f in os.listdir(self.root_path) if os.path.isdir(os.path.join(self.root_path, f))]
        self.folder_list.addItems(folders)

    def display_images(self, item):
        """根据选中的文件夹显示其中所有图片的缩略图"""
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        folder = item.text()
        folder_path = os.path.join(self.root_path, folder)
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        self.current_images = [os.path.join(folder_path, img) for img in images]

        for i, img_path in enumerate(self.current_images):
            pixmap = QPixmap(img_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            label.setCursor(Qt.PointingHandCursor)
            label.mousePressEvent = lambda event, i=i: self.show_fullscreen(i)
            self.grid.addWidget(label, i // 4, i % 4)

    def show_fullscreen(self, index):
        """将选中的图片以全屏模式显示，隐藏其他所有控件，背景为黑色"""
        self.current_index = index

        # 隐藏其他控件（除了 fullscreen_label）
        self.folder_list.hide()
        self.scroll.hide()
        self.toggle_mode_btn.hide()

        # 设置fullscreen_label覆盖整个窗口并显示黑色背景
        self.fullscreen_label.setGeometry(self.rect())
        self.fullscreen_label.setStyleSheet("background-color: black;")  # 黑背景
        pixmap = QPixmap(self.current_images[self.current_index]).scaled(
            self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.fullscreen_label.setPixmap(pixmap)
        self.fullscreen_label.show()
        self.fullscreen_label.raise_()
        self.setFocus()

    def exit_fullscreen(self, event):
        """退出全屏模式，隐藏图片，恢复其他控件显示"""
        self.fullscreen_label.hide()
        self.folder_list.show()
        self.scroll.show()
        self.toggle_mode_btn.show()

    def resizeEvent(self, event):
        """窗口大小变化时自动调整全屏图像的大小"""
        if self.fullscreen_label.isVisible() and self.current_images:
            pixmap = QPixmap(self.current_images[self.current_index]).scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.fullscreen_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        """在全屏模式中通过左右方向键切换图片"""
        if not self.fullscreen_label.isVisible():
            return

        if event.key() == Qt.Key_Right:
            self.current_index = (self.current_index + 1) % len(self.current_images)
        elif event.key() == Qt.Key_Left:
            self.current_index = (self.current_index - 1) % len(self.current_images)
        else:
            return

        pixmap = QPixmap(self.current_images[self.current_index]).scaled(
            self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.fullscreen_label.setPixmap(pixmap)

    def toggle_mode(self):
        """切换日间/夜间模式"""
        if self.is_dark_mode:
            self.apply_light_mode()
            self.toggle_mode_btn.setText("切换到夜间模式")
            self.is_dark_mode = False
        else:
            self.apply_dark_mode()
            self.toggle_mode_btn.setText("切换到日间模式")
            self.is_dark_mode = True

    def apply_dark_mode(self):
        """应用夜间模式样式"""
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-size: 20px;
            }
            QListWidget {
                background-color: #1e1e1e;
                border: none;
            }
            QScrollArea {
                background-color: #121212;
            }
            QLabel {
                background-color: transparent;
            }
            QListWidget::item:selected {
                background-color: #2a82da;
                color: white;
            }
            QPushButton {
                background-color: #2a82da;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #5599ee;
            }
        """)

    def apply_light_mode(self):
        """应用日间模式样式"""
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
                font-size: 20px;
            }
            QListWidget {
                background-color: #f0f0f0;
                border: none;
            }
            QScrollArea {
                background-color: white;
            }
            QLabel {
                background-color: transparent;
            }
            QListWidget::item:selected {
                background-color: #3399ff;
                color: black;
            }
            QPushButton {
                background-color: #3399ff;
                color: white;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #66b3ff;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    root_path = QFileDialog.getExistingDirectory(None, "选择根目录", "D:/")
    if root_path:
        viewer = ImageViewer(root_path)
        viewer.show()
        sys.exit(app.exec_())
