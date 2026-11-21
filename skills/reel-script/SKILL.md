---
name: reel-script
description: Write a short-form video script in the creator's own dialect from a chosen hook, with platform cuts (Instagram, TikTok, YouTube Shorts), the post caption and three cover texts. Use when the user has a hook or topic and wants the script, caption or cover text for a reel, TikTok or Short. Part of the Reel Agent team.
---

# reel-script

## Inputs

- The chosen hook (from `reel-agent/reels/<slug>/hook.md`, or the user).
- The topic, the payoff, and any real proof the creator has (a screen recording, a number, a result).
- `reel-agent/profile.md` (dialect, audience) and `reel-agent/lessons.md`.

## Shape (aim for 30-45 seconds)

1. **Hook** (0-3 s): the line as chosen, plus the promise in plain words by second 3.
2. **What it is** (1 line): name it, and say if it's free.
3. **The payoff list** (3-6 lines): one concrete thing per line, each one something the viewer can
   picture or copy. No background lines ("so basically AI has been evolving…"); they're where
   viewers leave.
4. **Re-hook at ~70%:** "But the best one?" / «بس أقوى واحد؟», then the strongest item.
5. **How to start** (1 line): the smallest first step.
6. **CTA** (1 line): Instagram, a keyword ("comment WORD and I'll DM you…"); TikTok and YouTube,
   a follow line.

## Writing rules

- **Write the way the creator talks,** in their dialect, with the English words they really use.
  Read it aloud in your head: if it sounds like a textbook, rewrite it.
- **Length:** count words. Spoken Arabic runs about 2-2.5 words a second, English about 3. Give the
  estimated length.
- **Every claim is true** and matches what the creator can show. Numbers come from real things.
- One idea per line, so the editor can give each line its own visual.

## Output: `reel-agent/reels/<slug>/script.md`

- The script as a numbered table: line, estimated seconds, and a one-line visual idea per line.
- **Platform cuts:** what changes for TikTok and YouTube (the hook if it names a platform, and the CTA).
- **Caption** (Instagram): the CTA first, 2-3 short lines on what it is and its honest limits, the
  CTA again, 3-5 hashtags.
- **Three cover texts:** at most 5 words each, readable at thumbnail size.
- **A filming note:** framing, takes (hook alone, then the body in one go), what to hold or show.
