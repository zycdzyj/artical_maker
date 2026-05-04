import markdown
import os
import sys
import time
import pickle
from PySide6.QtWidgets import *
from PySide6.QtCore import *
# 引入 Jinja2
from jinja2 import Template 
from bs4 import BeautifulSoup
# 假设这些是你自己的模块
from artcial_ui import Ui_Dialog 
from log import Ui_Dialog as LogDialogUI

def get_script_dir():
    """获取脚本所在目录（兼容打包前后）"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.ui.pushButton_log.clicked.connect(self.open_log_dialog)
        self.ui.label_user_name.setText("NONE")
        self.ui.pushButton_opfile.clicked.connect(self.open_file_dialog)
        self.ui.lineEdit_title.setText("未命名")
    def open_log_dialog(self):
        log_dialog = LogDialog(self)
        log_dialog.exec()

    def open_file_dialog(self):
        # 1. 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "选择Markdown文件", 
            "", 
            "Markdown Files (*.md);;All Files (*)"
        )

        if file_path:
            try:
                # 2. 读取 Markdown 内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_text = f.read()
                
                # 3. 转换为 HTML (保持不变)
                # 使用 'fenced_code' 等扩展支持代码块
                html_content = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])

                # 4. 读取模板文件 (路径保持不变)
                template_path = os.path.join(get_script_dir(), 'artcial', 'model.html')
                
                if not os.path.exists(template_path):
                    QMessageBox.critical(self, "错误", f"找不到模板文件:\n{template_path}")
                    return

                with open(template_path, 'r', encoding='utf-8') as f:
                    template_html = f.read()

                # ==========================================
                # 5. 使用 Jinja2 进行渲染 (核心修改部分)
                # ==========================================
                
                # 创建 Jinja2 模板对象
                jinja_template = Template(template_html)
                
                # 准备上下文数据
                # 我们在模板中可以使用 {{ html_body }} 来接收这个变量
                context = {
                    'html_body': html_content,
                    'user_picture': ("../../user/"+self.ui.label_user_name.text()+".jpg") if self.ui.label_user_name.text() != "NONE" else None,
                    'user_name': self.ui.label_user_name.text() if self.ui.label_user_name.text() != "NONE" else "Guest"
                }
                
                # 渲染模板
                # |safe 过滤器告诉 Jinja2 不要转义 HTML 标签
                final_html = jinja_template.render(context)

                # 6. 构建保存路径 (逻辑保持不变)
                
                # 获取标题
                title = "未命名"
                lines = md_text.strip().split('\n')
                if lines:
                    first_line = lines[0].strip()
                    if first_line.startswith('#'):
                        title = first_line.lstrip('#').strip()
                    else:
                        title = first_line[:20]
                
                # 获取当前登录的用户名
                current_user = self.ui.label_user_name.text()
                if current_user == "NONE" or not current_user:
                    current_user = "Guest"

                # 组合文件夹名称



                base_output_dir = os.path.join(get_script_dir(), 'artcial')
                folder_name = f"{current_user}_{time.strftime('%Y%m%d_%H%M%S')}_{title}"
                base_output_dir = os.path.join(base_output_dir, folder_name)
                
                # 确保目录存在
                os.makedirs(base_output_dir, exist_ok=True)

                # 最终文件路径
                original_filename = os.path.basename(file_path)
                output_filename = os.path.splitext(original_filename)[0] + ".html"
                output_path = os.path.join(base_output_dir, output_filename)

                # 7. 写入文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(final_html)
                
                QMessageBox.information(self, "成功", f"网页已生成:\n{output_path}")
                print(f"✅ 生成成功: {output_path}")
                pkl_file = os.path.join(get_script_dir(), 'data.pkl')
                data_list = []

                # 1. 尝试读取旧数据
                if os.path.exists(pkl_file):
                    try:
                        with open(pkl_file, 'rb') as f:
                            loaded_data = pickle.load(f)
                            # 确保读出来的是列表，防止类型错误
                            if isinstance(loaded_data, list):
                                data_list = loaded_data
                            else:
                                data_list = [loaded_data]
                    except Exception as e:
                        print(f"读取 pickle 文件失败: {e}")
                        data_list = []
                
                # 2. 准备新的文章数据字典
                new_article = {
                    'user_picture': "user/" + self.ui.label_user_name.text() + ".jpg", 
                    'user_name': context['user_name'], 
                    'html_body': self.ui.lineEdit_title.text() + "<br><br>",
                    'href':'artcial/' + folder_name + '/' + output_filename
                }

                # 3. 将新数据追加到列表中
                data_list.append(new_article)

                # 4. 保存回文件
                try:
                    with open(pkl_file, 'wb') as f:
                        pickle.dump(data_list, f)
                    print("✅ 数据列表已更新")
                except Exception as e:
                    print(f"保存 pickle 文件失败: {e}")
                content_html = '<div class="container">\n  <div class="feature-grid">\n'
                for artical in reversed(data_list):
                    content_html += f'''

<div class="feature-item">
    <!-- 1. 头部区域 -->
    <div class="user-info-row" style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
        
        <!-- 左侧：头像容器 -->
        <!-- 修改点：去掉了 class="avatar"，直接在 style 里控制宽高和圆角，防止外部样式干扰 -->
        <p style="margin: 0; width: 50px; height: 50px; border-radius: 50%; overflow: hidden; flex-shrink: 0;">
            <img src="{artical['user_picture']}" alt="用户头像" style="width: 100%; height: 100%; object-fit: cover; display: block;">
        </p>
        
        <!-- 右侧：用户名 -->
        <h3 style="font-size: 24px; margin: 0; font-weight: bold;">
            {artical['user_name']}
        </h3>
    </div>

    <!-- 2. 下方标题 -->
    <p style="font-size: 24px; margin: 0;">
        <a href="{artical['href']}" style="text-decoration: none; color: inherit; cursor: pointer;">
            {artical['html_body']}
        </a>
    </p>
</div>

                    
                    '''
                current_dir = os.path.dirname(os.path.abspath(__file__))
                content_html += '  </div>\n</div>'
                template_file = os.path.join(current_dir, 'news_2.html') 
                output_file = os.path.join(current_dir, 'news.html')

                # 1. 检查模板文件是否存在
                if not os.path.exists(template_file):
                    print(f"❌ 错误：找不到文件 '{template_file}'")
                    print("请确保 build.py 和 template.html 在同一个文件夹里！")
                else:
                    # 2. 读取模板 (这里定义了 template_content)
                    try:
                        with open(template_file, 'r', encoding='utf-8') as f:
                            template_content = f.read()  # <--- 变量在这里定义
        
                            # 3. 替换占位符
                            #    确保你的 template.html 里有这行注释：<!-- CONTENT_PLACEHOLDER -->
                            if '<!-- CONTENT_PLACEHOLDER -->' in template_content:
                                final_html = template_content.replace('<!-- CONTENT_PLACEHOLDER -->', content_html)
            
                                # 4. 写入文件
                                with open(output_file, 'w', encoding='utf-8') as f:
                                    f.write(final_html)
            
                                    print(f"✅ 成功！已生成 {output_file}")
                            else:
                                print("❌ 错误：在 template.html 中找不到 '<!-- CONTENT_PLACEHOLDER -->'")
                                print("请检查模板文件里有没有这行字。")
            
                    except Exception as e:
                        print(f"❌ 发生未知错误: {e}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"处理文件时出错:\n{str(e)}")
                print(f"❌ 错误: {e}")

            

class LogDialog(QDialog):
    def __init__(self, parent=None, folder_path=None):
        super().__init__(parent)
        
        if folder_path is None:
            self.base_path = get_script_dir() 
        else:
            self.base_path = folder_path
            
        self.ui = LogDialogUI()
        self.ui.setupUi(self)
        
        self.user_list = self.get_filenames_without_suffix(self.base_path)
        
        if not self.user_list:
            QMessageBox.warning(self, "提示", "未找到图片！\n请检查路径。")
        else:
            self.ui.comboBox.addItems(self.user_list)
        
        self.ui.comboBox.currentIndexChanged.connect(self.update_log_display)
        self.ui.pushButton_yes.clicked.connect(self.on_yes_clicked)

    def on_yes_clicked(self):
        selected_user = self.ui.comboBox.currentText()
        parent_window = self.parent()
        
        if parent_window and hasattr(parent_window, 'ui'):
            parent_window.ui.label_user_name.setText(selected_user)
        else:
            print("错误：无法找到主窗口")
            
        self.accept() 

    def update_log_display(self):
        pass

    def get_filenames_without_suffix(self, folder_path):
        filenames = []
        user_dir = os.path.join(folder_path, 'user')
        
        if not os.path.exists(user_dir):
            return filenames

        for filename in os.listdir(user_dir):
            file_path = os.path.join(user_dir, filename)
            if os.path.isfile(file_path):
                if filename.lower().endswith(('jpg', 'png', 'jpeg')):
                    name_without_ext = os.path.splitext(filename)[0]
                    filenames.append(name_without_ext)
        return filenames

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())