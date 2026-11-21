---
name: reel-broll
description: Plan and generate AI b-roll for a reel - turn the edit plan's b-roll cues into video prompts and queue them on your own rented GPU running ComfyUI with open-weight models (Wan 2.2, LTX-2.5), for about $1.39 an hour instead of paying per clip. Use when the user wants AI b-roll, generated clips, or cutaways for a reel, TikTok or Short. Part of the Reel Agent team.
---

# reel-broll

AI b-roll fills the cutaways: the product, the place, the idea. **The creator's face stays real.**
Open-weight video models are weakest on close-up faces, and audiences follow people.

## Inputs

The b-roll cues from `reel-agent/reels/<slug>/edit-plan.md`, or a list from the user.

## 1. Write the shot list

For each cue, write one prompt in English (the models follow English best):

- **subject + action**, **camera move** (slow push-in, orbit, top-down, handheld), **light** (morning
  window light, neon, golden hour), **lens/feel** (shallow depth of field, macro), **style** (photoreal,
  3D render, paper cut-out)
- 5 seconds, **vertical 720×1280**
- no real people's likeness, no brand logos, no text in the image (add text in the edit)

Example: *"Slow push-in on a laptop on a wooden desk at night, a glowing terminal on screen, steam
rising from a coffee cup, warm desk lamp, shallow depth of field, photoreal."*

## 2. The GPU (one-time setup, about 20 minutes)

Rent an RTX 5090 on RunPod with the official ComfyUI template, a network volume for the models,
and the Wan 2.2 / LTX-2.5 templates. Step-by-step guide, Arabic and English:
<https://github.com/alihaidar2950/wan-setup>

Cost checked 2026-11-18: **$1.39 an hour** while the pod runs. Wan 2.2 makes a 5 s clip in about
2 minutes, so 20+ clips an hour. Prices change; check runpod.io. **Stop the pod when you're done**:
an idle pod bills the same as a busy one.

## 3. Queue the clips

In ComfyUI, open the Wan 2.2 or LTX-2.5 text-to-video template, set 720×1280, and export it with
**Workflow → Export (API)**. Save the prompts one per line in `broll-prompts.txt`. Then:

```bash
python ~/.claude/skills/reel-broll/scripts/queue_comfy.py --server https://<pod-id>-8188.proxy.runpod.net --workflow wan_api.json --prompts broll-prompts.txt
```

The script finds the positive prompt node, sets a fresh seed per clip and queues one job per line.
Add `--dry-run` first to check what it will send. The clips land in ComfyUI's output folder.

Without a GPU, give the creator the shot list to use in any video tool they already pay for.

## Output: `reel-agent/reels/<slug>/broll.md`

The shot list (cue, timecode, prompt, model) and the cost estimate (clips × ~2 min ÷ 60 × $1.39).
Remind the creator to switch on the platform's AI label when a reel uses generated clips.
