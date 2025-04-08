## MCP Server 简易文件系统

这个项目是一个基于 MCP (Model Context Protocol) 的简易文件系统服务器，使用 Python 开发。服务器通过 MCP 协议暴露多种文件系统操作工具，可以集成到支持 MCP 协议的 MCP 主机中。

### 功能特点

-   **文件操作**：读取、写入、编辑、移动文件
-   **目录操作**：列出目录内容、创建目录
-   **批量操作**：批量读取多个文件
-   **安全限制**：仅允许访问指定目录
-   **元数据获取**：获取文件详细信息和属性

### 项目结构

```
simple-filesystem-server-python/
├── simple_filesystem.py  # 主程序入口
├── pyproject.toml        # 项目依赖配置
└── README.md             # 项目文档
```

### 项目构建

使用以下命令构建并运行项目：

```bash
# 克隆本项目
git clone https://github.com/jinzcdev/mcp-demos.git

# 进入项目目录
cd mcp-demos/simple-filesystem-server-python

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# On Windows:
# .venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -e .
```

### 使用方法

可以使用支持 MCP 的主机（如 Cline、Cursor）连接此服务。以 Cline 为例，将以下命令添加到 Cline 的 MCP Servers 配置文件中：

```json
{
    "mcpServers": {
        "filesystem": {
            "command": "python",
            "args": [
                "/ABSOLUTE/PATH/TO/PARENT/mcp-demos/simple-filesystem-server-python/simple_filesystem.py",
                "/path/to/allowed/directory1",
                "/path/to/allowed/directory2"
            ]
        }
    }
}
```

注意：需要在参数中指定允许访问的目录路径。

### 提供的工具

1. `list_directory`: 列出指定目录中的所有文件和目录

    - 参数: `dir_path` - 要列出内容的目录路径

2. `read_file`: 读取指定文件的完整内容

    - 参数: `file_path` - 要读取的文件路径

3. `write_file`: 创建新文件或覆盖现有文件

    - 参数: `file_path` - 要写入的文件路径
    - 参数: `content` - 要写入的文本内容

4. `read_multiple_files`: 同时读取多个文件的内容

    - 参数: `file_paths` - 要读取的文件路径列表

5. `edit_file`: 对文本文件进行基于行的编辑

    - 参数: `file_path` - 要编辑的文件路径
    - 参数: `edits` - 包含 'oldText' 和 'newText' 的编辑列表
    - 参数: `dry_run` - 如果为 True，仅显示变更而不实际修改

6. `create_directory`: 创建新目录或确保目录存在

    - 参数: `dir_path` - 要创建的目录路径

7. `move_file`: 移动或重命名文件和目录

    - 参数: `source_path` - 源文件或目录路径
    - 参数: `destination_path` - 目标路径

8. `get_file_info`: 获取文件或目录的详细元数据

    - 参数: `file_path` - 文件或目录路径

9. `list_allowed_directories`: 列出服务器允许访问的所有目录
    - 无参数
