## MCP Server 天气预报的官方代码

这个项目是一个官方实现的基于 MCP (Model Context Protocol) 的天气预报服务器，使用 Node.js 和 TypeScript 开发。服务器通过 MCP 协议暴露天气预报和天气警报工具，可以集成到支持 MCP 协议的 MCP 主机中。

### 功能特点

-   **获取天气警报**: 根据美国州代码获取当前天气警报
-   **获取天气预报**: 根据经纬度坐标获取未来几天的天气预报
-   基于美国国家气象局 (National Weather Service) 的公开 API
-   使用标准 MCP 协议进行通信

### 环境要求

-   Node.js 16+
-   npm

### 项目结构

```
weather-server-node/
├── src/
│ ├── index.ts              # 主程序入口
│ └── services/
│     └── weatherService.ts # 天气服务相关功能
├── tsconfig.json           # TypeScript 配置
└── README.md               # 项目文档
```

### 项目构建

使用以下命令构建项目：

```bash
# 克隆本项目
git clone https://github.com/jinzcdev/mcp-demos.git

# 进入项目目录
cd mcp-demos/weather-server-node

# 安装依赖
npm install

# 构建项目
npm run build
```

编译后将在当前目录下生成 `build/index.js` 文件。

### 使用方法

构建项目后，可以使用支持 MCP 主机（如 Cline、Cursor）连接此服务。以 Cline 为例，将以下命令添加到 Cline 的 MCP Servers 的配置文件中：

```json
{
    "mcpServers": {
        "weather": {
            "command": "node",
            "args": [
                "/ABSOLUTE/PATH/TO/PARENT/mcp-demos/weather-server-node/build/index.js"
            ]
        }
    }
}
```

服务提供的工具：

1. `get-alerts`: 获取指定州的天气警报

    - 参数: `state` - 两字母的州代码（如 CA、NY）

2. `get-forecast`: 获取指定位置的天气预报
    - 参数: `latitude` - 纬度（-90 到 90 之间）
    - 参数: `longitude` - 经度（-180 到 180 之间）
