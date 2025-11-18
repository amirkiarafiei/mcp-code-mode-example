# Executing MCP Tools as Code: A Better Way for LLM Agents to Use Tools

If you've been working with LLM agents, you've probably run into this frustration: your agent has dozens of tools available, but it only needs two or three for a specific task. Yet, all those tool definitions—names, parameters, descriptions, types—get dumped into the system prompt anyway, eating up precious context window space. Even worse, when tools need to chain together and pass large intermediate results, you're basically paying an expensive autoregressive model to act as a glorified copy-paste machine.

There's a better way. Let's talk about executing MCP tools as code.

## How Traditional Tool Calling Works (And Why It's Problematic)

In the standard approach, when you give an LLM agent a toolkit or MCP server, here's what happens:

1. **Tool Discovery Upfront:** Every single tool's metadata (name, description, parameter schemas, return types) gets injected into the LLM's system prompt before it even starts working
2. **JSON-Based Invocation:** The LLM generates tool calls in a specific JSON format
3. **Host Execution:** Your application parses those JSON calls, executes them, and returns results
4. **Repeat:** The LLM sees the results and decides what to do next

This works, but it has two major problems.

### Problem 1: Context Pollution

Imagine you have two MCP servers: one for Microsoft Teams with 10 tools, and one for Google Drive with another 10 tools. Your user just wants to download a meeting summary and upload it to Drive—that's 2 tools out of 20. But guess what? All 20 tool definitions are sitting there in your system prompt, taking up tokens, reducing your available context for actual reasoning.

When you're working with limited context windows (even "large" ones fill up fast with real-world applications), this is wasteful. You're basically asking the LLM to memorize an entire manual when it only needs to read two pages.

### Problem 2: Expensive Data Transfer

Here's where it gets really dumb. Say your first tool returns a massive meeting summary—8,000 tokens of text. The standard flow forces the LLM to:
1. Receive that entire 8KB result in its context
2. "Decide" to pass it to the next tool
3. Regenerate or reference that same 8KB as input to the next tool call

You're using an expensive autoregressive model—designed for high-variance reasoning tasks—to basically pipe data from one function to another. That's like hiring a PhD to photocopy documents. Operating systems already do this efficiently. Why involve the LLM at all?

## The Solution: Tools as Code

Companies like Anthropic and Cloudflare have pioneered a different approach: represent your tools as executable code in the filesystem, and give the LLM the ability to discover and write code that calls those tools.

Here's how it works:

### Step 1: Organize Tools as a Filesystem

Instead of registering 20 tools upfront, you create a filesystem structure like:

```
agent_filesystem/
  servers/
    teams/
      download_meeting_summary.ts
      list_meetings.ts
      ...
    drive/
      upload_file.ts
      create_folder.ts
      ...
```

Each file is a simple, well-documented function. The LLM doesn't see all of these upfront—they're just sitting there on disk.

### Step 2: Give the LLM Filesystem Access

Instead of 20 tool definitions in the system prompt, you give the LLM just two generic tools:
- A **filesystem tool** to explore and read files
- A **shell tool** to execute TypeScript/Python/whatever

That's it. Two tools instead of 20+.

### Step 3: Let the LLM Discover and Execute

When the user asks to "download the meeting summary and upload it to Drive," the LLM:

1. Uses the filesystem tool to explore: "Let me check what's available in the servers folder"
2. Finds and reads the relevant tool implementations
3. Writes a simple script: 
```typescript
import { download_meeting_summary } from './servers/teams/download_meeting_summary';
import { upload_file } from './servers/drive/upload_file';

const summary = await download_meeting_summary();
await upload_file(summary);
```
4. Executes it with the shell tool

Notice what just happened: the massive meeting summary never touched the LLM's context. It went straight from the Teams tool output to the Drive tool input, mediated by the operating system, not by expensive token generation.

## Why This Works Better

### Benefit 1: Efficient Context Management

The LLM only loads the tool definitions it actually needs. If you have 100 tools available but only use 3, those other 97 don't pollute your context. This is just good context engineering—use your limited token budget for reasoning, not for tool catalogs.

### Benefit 2: Direct Data Flow

Intermediate results flow through code, not through the LLM. A 10MB file? No problem. The LLM just writes `const data = await tool1(); await tool2(data);` and lets the OS handle the actual data movement.

### Benefit 3: Playing to LLM Strengths

Here's something interesting: these models have been trained on vastly more TypeScript/Python code than they have on tool-calling JSON formats. Tool calling as a formalized pattern has only really existed for 2-3 years. TypeScript has been around since 2012, in millions of repositories, tutorials, Stack Overflow answers, documentation sites.

Now, we don't have rigorous empirical studies proving that LLMs are better at generating TypeScript than tool-call JSON (someone should run those experiments!). But theoretically, it makes sense: the training data distribution heavily favors code. You're asking the model to do something it's seen millions more examples of.

## When Does This Matter?

This approach shines when:
- You have many tools but use few per task (high tool count, low utilization)
- Tools need to pass large intermediate results (chaining with big data)
- You want to minimize context usage (who doesn't?)
- You're building agentic systems that need to discover and compose tools dynamically

It's not a silver bullet—if you only have 3-4 tools total and they never chain, the traditional approach works fine. But as your toolkits grow and your use cases get more complex, code execution mode becomes increasingly attractive.

## Is This Something Totally New ?

Absolutely NOT! It is very similar to [CodeAct](https://arxiv.org/abs/2402.01030), an agent that plans and acts in code (python code) instead of natural language, which is different than conventional [ReAct](https://arxiv.org/abs/2210.03629) agent we are used to. The Hugging Face [smolagents](https://github.com/huggingface/smolagents) library already provides first-class support for this type of agents.


## Wrapping Up

The shift from "tools as LLM-visible primitives" to "tools as discoverable code" is fundamentally about better context engineering. We're recognizing that:

1. **Not all tool metadata needs to be in context upfront** - lazy loading is good actually
2. **LLMs should reason about what to do, not move data around** - use the right tool for the job
3. **Code is a lingua franca these models understand deeply** - leverage training distribution

The examples in this repository demonstrate both approaches side-by-side, showing how the same task (download meeting summary, upload to Drive) can be solved with traditional tool calling versus code execution mode. The difference in context usage and efficiency is striking.

As we build more sophisticated AI agents, thinking carefully about how we present tools—and how we let agents discover and compose them—will be just as important as the tools themselves. Code execution mode is one compelling answer to that challenge.

## Example Code

*This article is accompanied by working code examples comparing both approaches. Check out `agent_example_1.py` for traditional tool calling and `agent_example_2.py` for the code execution approach.*

- [Example Code in Github](https://github.com/amirkiarafiei/mcp-code-mode-example)

## References

- [Anthropic's Approach to Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Cloudflare's Code Mode Implementation](https://blog.cloudflare.com/code-mode/)



