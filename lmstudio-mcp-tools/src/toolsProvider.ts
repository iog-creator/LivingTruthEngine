import { text, tool, type Tool, type ToolsProviderController } from "@lmstudio/sdk";
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
      try {
        // Call our HTTP bridge
        const response = await fetch("http://127.0.0.1:8756/tools/verify_ssot", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        return {
          status: "success",
          result: result,
          inference_logs: "Check LM Studio developer logs for token accumulation and tool calls"
        };
      } catch (e) {
        return {
          status: "error",
          error: `Failed to call HTTP bridge: ${e}`,
          note: "Make sure the HTTP bridge is running: make lm-tools"
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
      try {
        // Call our HTTP bridge
        const response = await fetch("http://127.0.0.1:8756/tools/read_ssot_report", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        return {
          status: "success",
          result: result,
          inference_logs: "Check LM Studio developer logs for token accumulation and tool calls"
        };
      } catch (e) {
        return {
          status: "error",
          error: `Failed to call HTTP bridge: ${e}`,
          note: "Make sure the HTTP bridge is running: make lm-tools"
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
      try {
        // Call our HTTP bridge
        const response = await fetch("http://127.0.0.1:8756/tools/run_repo_inventory", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();

        return {
          status: "success",
          result: result,
          inference_logs: "Check LM Studio developer logs for token accumulation and tool calls"
        };
      } catch (e) {
        return {
          status: "error",
          error: `Failed to call HTTP bridge: ${e}`,
          note: "Make sure the HTTP bridge is running: make lm-tools"
        };
      }
    },
  });
  tools.push(runHealthChecksTool);

  return tools;
}
