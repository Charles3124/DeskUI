# DeskUI - 悬浮球快捷工具
## 功能概述

一个桌面悬浮球工具，提供快速访问常用程序、代码项目和网站的便捷菜单。

## 主要特性

- **悬浮球交互**：
  - 点击显示功能菜单
  - 长按拖动可移动位置
  - 鼠标悬停时有视觉反馈

- **快捷功能**：
  - 快速打开常用程序 (如远程桌面)
  - 一键访问代码项目 (在 VSCode 中打开)
  - 快速打开常用网站
  - 便捷访问系统文件夹

## 功能菜单说明

### 主菜单项

- **mstsc**：打开远程桌面连接
- **代码**：子菜单，包含各种代码项目
- **网站**：子菜单，快速访问常用网站
- **文档**：子菜单，快速访问系统文件夹
- **退出**：关闭悬浮球程序

### 代码子菜单

- LeetCode：打开 LeetCode 学习项目和网站
- AutoWork：打开 AutoWork 项目
- FaunaBox：打开 FaunaBox 项目
- DeskUI：打开 DeskUI 项目
- Portfolio：打开个人作品网站项目
- Stock：打开股票指标量化项目

### 网站子菜单

- bilibili：打开 B 站
- DeepSeek：打开 DeepSeek
- ChatGPT：打开 ChatGPT

### 文档子菜单

- 回收站：打开系统回收站
- 下载：打开下载文件夹
- 百度云：打开百度网盘目录

## 自定义配置

修改代码中的以下路径以适应您的系统环境：

```python
# 项目路径
self.BASE_DIR = Path("D:/My Programs")
self.code_work = self.BASE_DIR / "AutoWork"
self.code_ui = self.BASE_DIR / "Desk UI"
self.code_box = self.BASE_DIR / "FaunaBox"
self.code_folio = self.BASE_DIR / "MyPortfolio"
self.code_stock = self.BASE_DIR / "Stock Indicators"

# 网址
self.url_bilibili = "https://www.bilibili.com"
self.url_deepseek = "https://chat.deepseek.com"
self.url_chatgpt = "https://chatgpt.com"

# 其他路径
self.baidu_path = "D:/BaiduNetdiskDownload"
```

## 已知问题

- 程序启动时悬浮球位置固定为 (2000, 200)，可能需要根据屏幕分辨率调整

## 安装与使用

### 依赖安装

```bash
pip install PyQt5
```

### 运行程序

```bash
python main.py
```
