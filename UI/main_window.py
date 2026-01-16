import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
                             QGridLayout, QTextEdit, QGroupBox, QCheckBox,
                             QSpinBox, QComboBox)
from PyQt6.QtCore import Qt


class SettingsManager:
    def __init__(self):
        # 获取当前脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.settings_file = os.path.join(script_dir, "ui_settings.json")
        self.settings = self.load_settings()
    
    def load_settings(self):
        """加载设置文件"""
        default_settings = {
            "last_tab": "Setting",  # 默认打开Setting标签页
            "language": "中文",
            "theme": "浅色主题",
            "baudrate": "9600",
            "port": 8080
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default_settings
        return default_settings
    
    def save_settings(self):
        """保存设置到文件"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False
    
    def get_last_tab(self):
        """获取最后打开的标签页"""
        return self.settings.get("last_tab", "Setting")
    
    def set_last_tab(self, tab_name):
        """设置最后打开的标签页"""
        self.settings["last_tab"] = tab_name
        if self.save_settings():
            print(f"设置文件已更新: {tab_name}")
        else:
            print("保存设置文件失败")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P2 IO Framework - Control Panel")
        self.setFixedSize(1024, 768)
        
        # 初始化设置管理器
        self.settings_manager = SettingsManager()
        
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页控件
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        main_layout.addWidget(self.tab_widget)
        
        # 创建各个标签页
        self.create_monitor_tab()
        self.create_functions_tab()
        self.create_io_tab()
        self.create_setting_tab()
        
        # 恢复上次打开的标签页
        self.restore_last_tab()
    
    def create_monitor_tab(self):
        """创建监控标签页"""
        monitor_tab = QWidget()
        layout = QVBoxLayout(monitor_tab)
        
        # 状态监控区域
        status_group = QGroupBox("系统状态监控")
        status_layout = QGridLayout(status_group)
        
        # 添加状态监控组件
        status_layout.addWidget(QLabel("CPU使用率:"), 0, 0)
        status_layout.addWidget(QLabel("75%"), 0, 1)
        status_layout.addWidget(QLabel("内存使用:"), 1, 0)
        status_layout.addWidget(QLabel("62%"), 1, 1)
        status_layout.addWidget(QLabel("网络状态:"), 2, 0)
        status_layout.addWidget(QLabel("正常"), 2, 1)
        status_layout.addWidget(QLabel("设备连接:"), 3, 0)
        status_layout.addWidget(QLabel("3/5"), 3, 1)
        
        # 日志显示区域
        log_group = QGroupBox("系统日志")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        # 添加到主布局
        layout.addWidget(status_group)
        layout.addWidget(log_group)
        
        self.tab_widget.addTab(monitor_tab, "Monitor")
    
    def create_functions_tab(self):
        """创建功能标签页"""
        functions_tab = QWidget()
        layout = QVBoxLayout(functions_tab)
        
        # 功能控制区域
        control_group = QGroupBox("功能控制")
        control_layout = QGridLayout(control_group)
        
        # 添加功能按钮
        buttons = [
            ("启动服务", 0, 0), ("停止服务", 0, 1),
            ("数据采集", 1, 0), ("数据处理", 1, 1),
            ("报表生成", 2, 0), ("系统诊断", 2, 1)
        ]
        
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedHeight(40)
            control_layout.addWidget(button, row, col)
        
        # 参数设置区域
        param_group = QGroupBox("参数设置")
        param_layout = QGridLayout(param_group)
        
        param_layout.addWidget(QLabel("采样频率:"), 0, 0)
        self.sample_freq = QSpinBox()
        self.sample_freq.setRange(1, 1000)
        self.sample_freq.setValue(100)
        param_layout.addWidget(self.sample_freq, 0, 1)
        
        param_layout.addWidget(QLabel("工作模式:"), 1, 0)
        self.work_mode = QComboBox()
        self.work_mode.addItems(["自动模式", "手动模式", "调试模式"])
        param_layout.addWidget(self.work_mode, 1, 1)
        
        # 添加到主布局
        layout.addWidget(control_group)
        layout.addWidget(param_group)
        layout.addStretch()
        
        self.tab_widget.addTab(functions_tab, "Functions")
    
    def create_io_tab(self):
        """创建IO标签页"""
        io_tab = QWidget()
        layout = QVBoxLayout(io_tab)
        
        # IO状态监控
        io_status_group = QGroupBox("IO状态监控")
        io_layout = QGridLayout(io_status_group)
        
        # 添加IO状态显示
        io_ports = [
            ("DI0", "输入", "高电平"), ("DI1", "输入", "低电平"),
            ("DO0", "输出", "激活"), ("DO1", "输出", "未激活"),
            ("AI0", "模拟输入", "2.5V"), ("AO0", "模拟输出", "0V")
        ]
        
        for i, (port, type_, status) in enumerate(io_ports):
            io_layout.addWidget(QLabel(f"{port}:"), i, 0)
            io_layout.addWidget(QLabel(type_), i, 1)
            io_layout.addWidget(QLabel(status), i, 2)
        
        # IO控制区域
        io_control_group = QGroupBox("IO控制")
        control_layout = QGridLayout(io_control_group)
        
        # 添加IO控制组件
        control_layout.addWidget(QLabel("数字输出:"), 0, 0)
        self.do0_check = QCheckBox("DO0")
        self.do1_check = QCheckBox("DO1")
        control_layout.addWidget(self.do0_check, 0, 1)
        control_layout.addWidget(self.do1_check, 0, 2)
        
        control_layout.addWidget(QLabel("模拟输出:"), 1, 0)
        self.ao_value = QSpinBox()
        self.ao_value.setRange(0, 10)
        self.ao_value.setSuffix(" V")
        control_layout.addWidget(self.ao_value, 1, 1)
        
        # 添加到主布局
        layout.addWidget(io_status_group)
        layout.addWidget(io_control_group)
        layout.addStretch()
        
        self.tab_widget.addTab(io_tab, "IO")
    
    def create_setting_tab(self):
        """创建设置标签页"""
        setting_tab = QWidget()
        layout = QVBoxLayout(setting_tab)
        
        # 系统设置区域
        system_group = QGroupBox("系统设置")
        system_layout = QGridLayout(system_group)
        
        system_layout.addWidget(QLabel("语言设置:"), 0, 0)
        self.language_combo = QComboBox()
        self.language_combo.addItems(["中文", "English", "日本語"])
        system_layout.addWidget(self.language_combo, 0, 1)
        
        system_layout.addWidget(QLabel("主题设置:"), 1, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["浅色主题", "深色主题", "自动"])
        system_layout.addWidget(self.theme_combo, 1, 1)
        
        # 通信设置区域
        comm_group = QGroupBox("通信设置")
        comm_layout = QGridLayout(comm_group)
        
        comm_layout.addWidget(QLabel("串口波特率:"), 0, 0)
        self.baudrate_combo = QComboBox()
        self.baudrate_combo.addItems(["9600", "19200", "38400", "115200"])
        comm_layout.addWidget(self.baudrate_combo, 0, 1)
        
        comm_layout.addWidget(QLabel("网络端口:"), 1, 0)
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1000, 65535)
        self.port_spin.setValue(8080)
        comm_layout.addWidget(self.port_spin, 1, 1)
        
        # 保存/重置按钮
        button_layout = QHBoxLayout()
        save_btn = QPushButton("保存设置")
        reset_btn = QPushButton("恢复默认")
        button_layout.addWidget(save_btn)
        button_layout.addWidget(reset_btn)
        
        # 添加到主布局
        layout.addWidget(system_group)
        layout.addWidget(comm_group)
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.tab_widget.addTab(setting_tab, "Setting")
    
    def on_tab_changed(self, index):
        """标签页切换时保存当前标签页"""
        if index >= 0:
            tab_name = self.tab_widget.tabText(index)
            print(f"切换到标签页: {tab_name}")  # 调试信息
            self.settings_manager.set_last_tab(tab_name)
            print(f"已保存标签页: {tab_name}")  # 确认保存成功
    
    def restore_last_tab(self):
        """恢复上次打开的标签页"""
        last_tab = self.settings_manager.get_last_tab()
        print(f"恢复标签页: {last_tab}")  # 调试信息
        
        # 直接使用标签页索引，避免名称匹配问题
        tab_mapping = {
            "Monitor": 0,
            "Functions": 1,
            "IO": 2,
            "Setting": 3
        }
        
        tab_index = tab_mapping.get(last_tab, 0)  # 默认为Monitor
        self.tab_widget.setCurrentIndex(tab_index)


def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()