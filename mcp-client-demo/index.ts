
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

class MCPClient {

    /**
     * MCP 客户端列表
     */
    private mcps: Client[];
    private tools: any[] = [];

    constructor() {
        this.mcps = [];
    }

    async connectToServer(serverScriptPaths: string[]) {
        try {
            for (const serverScriptPath of serverScriptPaths) {
                const isJs = serverScriptPath.endsWith(".js");
                const isPy = serverScriptPath.endsWith(".py");
                if (!isJs && !isPy) {
                    throw new Error("Server script must be a .js or .py file");
                }
                const command = isPy
                    ? process.platform === "win32"
                        ? "python"
                        : "python3"
                    : process.execPath;

                const mcp = new Client({ name: "mcp-client-cli", version: "1.0.0" });
                this.mcps.push(mcp);

                // 创建 MCP 连接
                mcp.connect(new StdioClientTransport({
                    command,
                    args: [serverScriptPath],
                }));

                const toolsResult = await mcp.listTools();

                // 存储所有工具，交由大模型使用
                this.tools.push(...toolsResult.tools);
                console.log(
                    "Connected to server with tools:",
                    toolsResult.tools.map(({ name }) => name)
                );
            }
        } catch (e) {
            console.log("Failed to connect to MCP server: ", e);
            throw e;
        }
    }

    async cleanup() {
        for (const mcp of this.mcps) {
            await mcp.close();
        }
    }
}

async function main() {
    if (process.argv.length < 3) {
        console.log("Usage: node index.ts <path_to_server_scripts>");
        return;
    }
    const mcpClient = new MCPClient();
    try {
        await mcpClient.connectToServer(process.argv.slice(2));
    } finally {
        await mcpClient.cleanup();
        process.exit(0);
    }
}

main();