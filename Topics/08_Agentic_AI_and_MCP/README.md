# Agentic AI and MCP

## What you will learn

Design bounded AI workflows that can select tools, pass structured information, and report their actions predictably.

## Important concepts

- Agent loops, tool selection, and structured tool schemas
- State, planning, observations, and stopping conditions
- MCP concepts: clients, servers, tools, resources, and prompts
- Permissions, least privilege, validation, and human approval
- Tracing, failure handling, and deterministic evaluation

## Practical exercises

- Design a small tool interface with explicit input and output types.
- Trace a bounded workflow and test invalid inputs, timeouts, and tool errors.
- Add an approval step before any consequential or externally visible action.

## Suggested projects

- A read-only research assistant that retrieves sources and returns cited notes.
- A local workflow that coordinates a small number of safe tools with explicit limits.

Begin with read-only, narrow tools. Do not give an agent unrestricted credentials or authority.