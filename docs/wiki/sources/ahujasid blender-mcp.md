---
type: source
source_type: github_repo
title: "ahujasid/blender-mcp"
author: "Siddharth Ahuja"
date_published: 2025
url: https://github.com/ahujasid/blender-mcp
confidence: high
tags:
  - source
  - blender
  - mcp
  - claude
related:
  - "[[Blender MCP Architecture]]"
  - "[[minihellboy claude-blender]]"
---

# ahujasid/blender-mcp

The reference Blender MCP server. Sponsored by Warp. Two-component distributed architecture.

## Architecture

1. **Blender Addon (`addon.py`)** — TCP socket server inside Blender, default `localhost:9876`. Configurable via `BLENDER_HOST` / `BLENDER_PORT` env vars.
2. **MCP Server (`src/blender_mcp/server.py`)** — Bridges Claude (or Cursor / VS Code) to the addon via JSON-over-TCP.

Communication: simple JSON protocol, `{type, parameters}` request → `{status, result}` response.

## Tools exposed

- Scene inspection / object queries
- Object create / modify / delete (primitives)
- Material + color
- **`execute_blender_code`** — arbitrary Python in Blender context (powerful, dangerous)
- Asset download via Poly Haven, Hyper3D Rodin, Sketchfab
- Viewport screenshot for scene understanding

## Requirements

- Blender 3.0+
- Python 3.10+
- `uv` package manager
- Current version: 1.5.5

## Security caveats

> The `execute_blender_code` tool allows running arbitrary Python code in Blender, which can be powerful but potentially dangerous.

Telemetry collects anonymized prompts, code, screenshots — disable via addon checkbox or `DISABLE_TELEMETRY=true`.

## Limitations for FDM 3D printing

- **No native print-prep tools** — no manifold check, no orientation optimizer, no support generator
- Complex operations need sequential decomposition by Claude
- First command per session sometimes fails (re-run)
- Hyper3D free-tier daily quota
- Multiple instances will collide on port 9876

## Verdict for parametric printables

Good for **art + scene composition**. Wrong tool for **deterministic FDM-print parts** because Blender's mesh kernel doesn't enforce manifoldness — exactly the "constant battle" Blender is criticized for in CAD comparisons. For printable parts, prefer CadQuery via [[flowful-ai cad-skill]].
