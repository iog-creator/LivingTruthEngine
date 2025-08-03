# Langflow Node Index

## Overview
This document provides a comprehensive index of Langflow nodes with their proper JSON structure for programmatic workflow creation.

## Node Categories

### 1. Input/Output Nodes

#### TextNode
```json
{
  "id": "text_node_1",
  "type": "TextNode",
  "position": {"x": 100, "y": 100},
  "data": {
    "node": {
      "template": {
        "text": {
          "type": "str",
          "value": "Your text here",
          "required": true,
          "show": true,
          "multiline": true
        }
      },
      "description": "Simple text input/output node",
      "base_classes": ["TextNode"],
      "display_name": "Text",
      "documentation": "Simple text input/output"
    }
  }
}
```

#### InputNode
```json
{
  "id": "input_node_1",
  "type": "InputNode",
  "position": {"x": 100, "y": 100},
  "data": {
    "node": {
      "template": {
        "input_value": {
          "type": "str",
          "value": "Enter input here",
          "required": true,
          "show": true,
          "multiline": true
        }
      },
      "description": "Input node for user data",
      "base_classes": ["InputNode"],
      "display_name": "Input",
      "documentation": "Input node for user data"
    }
  }
}
```

#### OutputNode
```json
{
  "id": "output_node_1",
  "type": "OutputNode",
  "position": {"x": 300, "y": 100},
  "data": {
    "node": {
      "template": {
        "output_value": {
          "type": "str",
          "value": "Output will appear here",
          "required": true,
          "show": true,
          "multiline": true
        }
      },
      "description": "Output node for results",
      "base_classes": ["OutputNode"],
      "display_name": "Output",
      "documentation": "Output node for results"
    }
  }
}
```

### 2. LLM Nodes

#### ChatOpenAI
```json
{
  "id": "chat_openai_1",
  "type": "ChatOpenAI",
  "position": {"x": 200, "y": 100},
  "data": {
    "node": {
      "template": {
        "model_name": {
          "type": "str",
          "value": "gpt-3.5-turbo",
          "required": true,
          "show": true
        },
        "temperature": {
          "type": "float",
          "value": 0.7,
          "required": true,
          "show": true
        },
        "openai_api_key": {
          "type": "str",
          "value": "",
          "required": true,
          "show": true,
          "password": true
        }
      },
      "description": "OpenAI chat model",
      "base_classes": ["ChatOpenAI"],
      "display_name": "ChatOpenAI",
      "documentation": "OpenAI chat model"
    }
  }
}
```

#### LLMChain
```json
{
  "id": "llm_chain_1",
  "type": "LLMChain",
  "position": {"x": 200, "y": 100},
  "data": {
    "node": {
      "template": {
        "llm": {
          "type": "BaseLLM",
          "value": "ChatOpenAI",
          "required": true,
          "show": true
        },
        "prompt": {
          "type": "BasePromptTemplate",
          "value": "PromptTemplate",
          "required": true,
          "show": true
        }
      },
      "description": "LLM Chain for processing",
      "base_classes": ["LLMChain"],
      "display_name": "LLM Chain",
      "documentation": "LLM Chain for processing"
    }
  }
}
```

### 3. Prompt Nodes

#### PromptTemplate
```json
{
  "id": "prompt_template_1",
  "type": "PromptTemplate",
  "position": {"x": 150, "y": 100},
  "data": {
    "node": {
      "template": {
        "template": {
          "type": "str",
          "value": "You are a helpful assistant. Answer: {question}",
          "required": true,
          "show": true,
          "multiline": true
        },
        "input_variables": {
          "type": "list",
          "value": ["question"],
          "required": true,
          "show": true
        }
      },
      "description": "Template for creating prompts",
      "base_classes": ["PromptTemplate"],
      "display_name": "Prompt Template",
      "documentation": "Template for creating prompts"
    }
  }
}
```

#### HumanInputPrompt
```json
{
  "id": "human_input_1",
  "type": "HumanInputPrompt",
  "position": {"x": 100, "y": 100},
  "data": {
    "node": {
      "template": {
        "prompt": {
          "type": "str",
          "value": "Enter your input:",
          "required": true,
          "show": true,
          "multiline": true
        }
      },
      "description": "Human input prompt",
      "base_classes": ["HumanInputPrompt"],
      "display_name": "Human Input",
      "documentation": "Node for human input"
    }
  }
}
```

### 4. Memory Nodes

#### ConversationBufferMemory
```json
{
  "id": "memory_1",
  "type": "ConversationBufferMemory",
  "position": {"x": 250, "y": 100},
  "data": {
    "node": {
      "template": {
        "memory_key": {
          "type": "str",
          "value": "chat_history",
          "required": true,
          "show": true
        },
        "return_messages": {
          "type": "bool",
          "value": true,
          "required": true,
          "show": true
        }
      },
      "description": "Conversation memory buffer",
      "base_classes": ["ConversationBufferMemory"],
      "display_name": "Conversation Buffer Memory",
      "documentation": "Memory for conversation history"
    }
  }
}
```

### 5. Tool Nodes

#### ToolNode
```json
{
  "id": "tool_1",
  "type": "ToolNode",
  "position": {"x": 200, "y": 100},
  "data": {
    "node": {
      "template": {
        "tool_name": {
          "type": "str",
          "value": "search",
          "required": true,
          "show": true
        }
      },
      "description": "Tool execution node",
      "base_classes": ["ToolNode"],
      "display_name": "Tool",
      "documentation": "Node for tool execution"
    }
  }
}
```

### 6. Chain Nodes

#### ConversationChain
```json
{
  "id": "conversation_chain_1",
  "type": "ConversationChain",
  "position": {"x": 200, "y": 100},
  "data": {
    "node": {
      "template": {
        "llm": {
          "type": "BaseLLM",
          "value": "ChatOpenAI",
          "required": true,
          "show": true
        },
        "memory": {
          "type": "BaseMemory",
          "value": "ConversationBufferMemory",
          "required": false,
          "show": true
        }
      },
      "description": "Conversation chain with memory",
      "base_classes": ["ConversationChain"],
      "display_name": "Conversation Chain",
      "documentation": "Chain for conversations with memory"
    }
  }
}
```

## Edge Structure

### Standard Edge
```json
{
  "id": "edge_1",
  "source": "source_node_id",
  "target": "target_node_id",
  "sourceHandle": "output",
  "targetHandle": "input"
}
```

## Complete Workflow Example

### Simple Text Processing Workflow
```json
{
  "name": "Simple Text Processing",
  "description": "A simple workflow for text processing",
  "data": {
    "nodes": [
      {
        "id": "input_1",
        "type": "TextNode",
        "position": {"x": 100, "y": 100},
        "data": {
          "node": {
            "template": {
              "text": {
                "type": "str",
                "value": "Enter text to process",
                "required": true,
                "show": true,
                "multiline": true
              }
            },
            "description": "Input text node",
            "base_classes": ["TextNode"],
            "display_name": "Text",
            "documentation": "Simple text input/output"
          }
        }
      },
      {
        "id": "output_1",
        "type": "TextNode",
        "position": {"x": 300, "y": 100},
        "data": {
          "node": {
            "template": {
              "text": {
                "type": "str",
                "value": "Processed text will appear here",
                "required": true,
                "show": true,
                "multiline": true
              }
            },
            "description": "Output text node",
            "base_classes": ["TextNode"],
            "display_name": "Text",
            "documentation": "Simple text input/output"
          }
        }
      }
    ],
    "edges": [
      {
        "id": "edge_1",
        "source": "input_1",
        "target": "output_1",
        "sourceHandle": "output",
        "targetHandle": "input"
      }
    ]
  }
}
```

## Usage Notes

1. **Node IDs**: Must be unique within the workflow
2. **Position**: x,y coordinates for node placement in the UI
3. **Template Values**: Default values that appear in the node configuration
4. **Base Classes**: Must match the actual Langflow node class names
5. **Edges**: Connect nodes using their IDs and proper handle names

## Import Process

1. Create workflow JSON using the structures above
2. Use the `create_langflow` API endpoint to import
3. The workflow will appear in the Langflow UI with proper node rendering
4. Nodes can be configured and connected as needed

## Common Issues

1. **Blank Nodes**: Usually caused by incorrect `type` or `base_classes`
2. **Missing Connections**: Check `sourceHandle` and `targetHandle` values
3. **Rendering Issues**: Ensure all required template fields are present
4. **Import Errors**: Validate JSON structure before importing 