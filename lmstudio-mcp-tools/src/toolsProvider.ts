import { text, tool, type Tool, type ToolsProviderController } from "@lmstudio/sdk";
import { spawn } from "child_process";
import { z } from "zod";

export async function toolsProvider(ctl: ToolsProviderController) {
  const tools: Tool[] = [];

  // Tool to validate cursor rules
  const validateCursorRulesTool = tool({
    name: "validate_cursor_rules",
    description: text`
      Validate all cursor rules (.mdc files) for proper frontmatter and structure.
      This will show inference happening in LM Studio developer logs.
    `,
    parameters: {},
    implementation: async () => {
      const workingDirectory = ctl.getWorkingDirectory();
      
      // Call our MCP server via subprocess
      const childProcess = spawn(
        "python",
        ["src/mcp_servers/phase9_mcp_server.py"],
        {
          cwd: workingDirectory,
          timeout: 30000, // 30 seconds
          stdio: "pipe",
        }
      );

      // Send MCP request to validate cursor rules
      const mcpRequest = {
        jsonrpc: "2.0",
        id: 1,
        method: "tools/call",
        params: {
          name: "validate_cursor_rules",
          arguments: {}
        }
      };

      childProcess.stdin.write(JSON.stringify(mcpRequest) + "\n");
      childProcess.stdin.end();

      let stdout = "";
      let stderr = "";

      childProcess.stdout.setEncoding("utf-8");
      childProcess.stderr.setEncoding("utf-8");

      childProcess.stdout.on("data", data => {
        stdout += data;
      });
      childProcess.stderr.on("data", data => {
        stderr += data;
      });

      await new Promise<void>((resolve, reject) => {
        childProcess.on("close", code => {
          if (code === 0) {
            resolve();
          } else {
            reject(new Error(`MCP server exited with code ${code}. Stderr: ${stderr}`));
          }
        });

        childProcess.on("error", err => {
          reject(err);
        });
      });

      try {
        const response = JSON.parse(stdout);
        return {
          status: "success",
          result: response.result,
          inference_logs: "Check LM Studio developer logs for token accumulation and tool calls"
        };
      } catch (e) {
        return {
          status: "error",
          error: `Failed to parse MCP response: ${e}`,
          raw_output: stdout,
          stderr: stderr
        };
      }
    },
  });
  tools.push(validateCursorRulesTool);

  // Tool to validate SSOT bundle
  const validateSSOTBundleTool = tool({
    name: "validate_ssot_bundle",
    description: text`
      Validate the SSOT (Single Source of Truth) bundle files.
      This will show inference happening in LM Studio developer logs.
    `,
    parameters: {},
    implementation: async () => {
      const workingDirectory = ctl.getWorkingDirectory();
      
      // Call our MCP server via subprocess
      const childProcess = spawn(
        "python",
        ["src/mcp_servers/phase9_mcp_server.py"],
        {
          cwd: workingDirectory,
          timeout: 30000, // 30 seconds
          stdio: "pipe",
        }
      );

      // Send MCP request to validate SSOT bundle
      const mcpRequest = {
        jsonrpc: "2.0",
        id: 2,
        method: "tools/call",
        params: {
          name: "validate_ssot_bundle",
          arguments: {}
        }
      };

      childProcess.stdin.write(JSON.stringify(mcpRequest) + "\n");
      childProcess.stdin.end();

      let stdout = "";
      let stderr = "";

      childProcess.stdout.setEncoding("utf-8");
      childProcess.stderr.setEncoding("utf-8");

      childProcess.stdout.on("data", data => {
        stdout += data;
      });
      childProcess.stderr.on("data", data => {
        stderr += data;
      });

      await new Promise<void>((resolve, reject) => {
        childProcess.on("close", code => {
          if (code === 0) {
            resolve();
          } else {
            reject(new Error(`MCP server exited with code ${code}. Stderr: ${stderr}`));
          }
        });

        childProcess.on("error", err => {
          reject(err);
        });
      });

      try {
        const response = JSON.parse(stdout);
        return {
          status: "success",
          result: response.result,
          inference_logs: "Check LM Studio developer logs for token accumulation and tool calls"
        };
      } catch (e) {
        return {
          status: "error",
          error: `Failed to parse MCP response: ${e}`,
          raw_output: stdout,
          stderr: stderr
        };
      }
    },
  });
  tools.push(validateSSOTBundleTool);

  // Tool to run health checks
  const runHealthChecksTool = tool({
    name: "run_health_checks",
    description: text`
      Run comprehensive health checks on the Living Truth Engine system.
      This will show inference happening in LM Studio developer logs.
    `,
    parameters: {},
    implementation: async () => {
      const workingDirectory = ctl.getWorkingDirectory();
      
      // Call our MCP server via subprocess
      const childProcess = spawn(
        "python",
        ["src/mcp_servers/phase9_mcp_server.py"],
        {
          cwd: workingDirectory,
          timeout: 30000, // 30 seconds
          stdio: "pipe",
        }
      );

      // Send MCP request to run health checks
      const mcpRequest = {
        jsonrpc: "2.0",
        id: 3,
        method: "tools/call",
        params: {
          name: "run_health_checks",
          arguments: {}
        }
      };

      childProcess.stdin.write(JSON.stringify(mcpRequest) + "\n");
      childProcess.stdin.end();

      let stdout = "";
      let stderr = "";

      childProcess.stdout.setEncoding("utf-8");
      childProcess.stderr.setEncoding("utf-8");

      childProcess.stdout.on("data", data => {
        stdout += data;
      });
      childProcess.stderr.on("data", data => {
        stderr += data;
      });

      await new Promise<void>((resolve, reject) => {
        childProcess.on("close", code => {
          if (code === 0) {
            resolve();
          } else {
            reject(new Error(`MCP server exited with code ${code}. Stderr: ${stderr}`));
          }
        });

        childProcess.on("error", err => {
          reject(err);
        });
      });

      try {
        const response = JSON.parse(stdout);
        return {
          status: "success",
          result: response.result,
          inference_logs: "Check LM Studio developer logs for token accumulation and tool calls"
        };
      } catch (e) {
        return {
          status: "error",
          error: `Failed to parse MCP response: ${e}`,
          raw_output: stdout,
          stderr: stderr
        };
      }
    },
  });
  tools.push(runHealthChecksTool);

  return tools;
}
