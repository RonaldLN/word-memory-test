# 单词记忆训练系统

> [!NOTE]
> 以下内容借助Github Copilot生成，(仅供参考)`

这是一个帮助用户记忆单词的应用程序，通过记忆反馈机制，系统会优先展示用户经常忘记的单词，提高学习效率。

## 功能特点

- 智能单词展示：根据用户记忆情况调整单词出现频率
- 双模式支持：命令行界面和Web界面
- 学习进度追踪：自动保存用户学习历史
- 密码保护：Web界面设有密码保护功能

## 安装说明

1. 克隆项目到本地
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置环境变量（可选）
   - 复制`.env.example`文件为`.env`（项目中已有`.env`文件）
   - 修改`.env`中的密码和密钥

## 使用方法

### 初始化单词库（首次使用）

```bash
python python_program/create_history.py
```

### 命令行模式

```bash
python python_program/main.py
```

命令行界面操作：
- `y`: 表示记住了这个单词
- `n`: 表示忘记了这个单词
- `q`: 退出程序并保存进度

### Web界面模式

```bash
python app.py
```

然后在浏览器中访问：`http://localhost:5000`

- 使用`.env`文件中设置的密码登录
- 点击"记得"或"忘记"按钮反馈学习情况
- 点击"退出"按钮退出系统

## 项目结构

```
├── app.py                 # Flask Web应用主程序
├── config.py              # 配置文件
├── history.json           # 学习历史记录
├── requirements.txt       # 项目依赖
├── python_program/        # 命令行程序
│   ├── create_history.py  # 初始化历史记录
│   ├── main.py            # 命令行主程序
│   └── words.txt          # 单词列表
└── templates/             # HTML模板
    ├── index.html         # 主界面
    └── login.html         # 登录界面
```

## 自定义单词列表

可以通过修改 words.txt 文件来自定义要学习的单词，然后运行 create_history.py 重新初始化历史记录。

## 技术栈

- Python 3
- Flask (Web框架)
- JavaScript (前端交互)
- JSON (数据存储)

## 注意事项

- 学习历史保存在`history.json`文件中
- Web模式需要登录后才能使用
- 两种模式使用相同的历史记录文件，可以交替使用