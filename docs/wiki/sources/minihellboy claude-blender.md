---
type: source
source_type: github_repo
title: "minihellboy/claude-blender"
author: "minihellboy"
date_published: 2025
url: https://github.com/minihellboy/claude-blender
confidence: high
tags:
  - source
  - blender
  - mcp
  - claude-code
related:
  - "[[ahujasid blender-mcp]]"
  - "[[Blender MCP Architecture]]"
---

# minihellboy/claude-blender

Claude-Code-targeted Blender MCP variant. 20+ tools, local AI features, ComfyUI bridge.

## Three-layer architecture

Claude Code CLI → MCP server (Python) → Blender addon (JSON-RPC over TCP, port 9876).

Key implementation choice: **timer-polled TCP server** rather than threading because "Blender's Python API is NOT thread-safe." All operations execute on Blender's main thread.

## Tools (20+)

- **Scene**: `blender_get_scene` with detail levels (minimal/basic/detailed/full)
- **Objects**: add/modify/delete primitives
- **Rendering**: viewport capture, scene render with custom settings
- **Animation**: keyframes, frame range
- **Materials**: create + assign

## Local AI features (no external API calls)

- **Shap-E** — text-to-3D
- **TripoSR** — image-to-3D
- **ComfyUI bridge** — connects to local Stable Diffusion at `127.0.0.1:8188`
- **Procedural generators** — rocks, terrain, buildings via Blender modifiers (zero deps)

## Requirements

- Blender 4.0+ (tested 4.3)
- Python 3.10+
- Optional AI extras: torch, diffusers, transformers, trimesh, rembg

## Differentiation vs [[ahujasid blender-mcp]]

- No external API calls for AI features (local Shap-E / TripoSR)
- Clean MCP separation — server can restart independently
- Explicit ComfyUI integration

## Verdict for parametric printables

Same limitation as ahujasid version: Blender mesh ≠ manifold-guaranteed. Good for **AI asset generation** (Shap-E for organic shapes) but downstream you still need manifold validation + repair before slicing. Not the right tool for the user's parametric veranda templates.
