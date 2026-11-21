---
name: reel-edit-plan
description: Turn a short-form video script into a shot-by-shot edit plan - layout per line (face, split panel, full panel), word-by-word caption chunks, on-screen graphics, b-roll and sound cues, at a pace that changes every 1-2 seconds. Use when the user has a script or a filmed take and wants to know how to edit it, or wants an edit plan for CapCut, Premiere or an editor. Part of the Reel Agent team.
---

# reel-edit-plan

This skill plans the edit; it doesn't render video. Hand the plan to whoever edits (you, CapCut,
an editor or a video-code tool).

## Inputs

`reel-agent/reels/<slug>/script.md`, and the transcript with timestamps if the take is filmed
(otherwise estimate from word counts).

## The default style: panel + caption band + face

This style keeps the face on screen most of the time and still changes something every 1-2 seconds:

- **1080×1920 in three bands:**
  - top panel (0-618 px): light grey-white with a faint grid, for the graphics
  - caption band (618-724 px): near-black
  - the creator's face (724-1920)
- **Captions:** 2-4 words at a time in the band. White, with the word being spoken in one accent
  colour, word by word.
- **Graphics:** simple white UI cards, small mono labels, rounded icon tiles in the accent colour.
  Each one pops in on the word that names it. Mock-ups carry a small "illustrative" mark.
- **Full-panel moments:** the graphic takes the whole screen 2-3 times. Use them for the reveal
  (~15%), the re-hook (~70%) and the how-to (~85%).
- **The face layer doesn't zoom.** The motion lives in the panel.

Use another style if the creator asks or `lessons.md` says this one isn't working.

## Rules

- **Frame 0 carries the hook in full,** with no fade-in. It often becomes the cover.
- **Something changes every 1-2 s:** a new card, a tick, a typed word, a layout switch.
- **One visual per script line,** showing that line's payoff.
- **Cut silences and breaths** longer than ~0.3 s in the face take.
- **Sound:** voice first; soft pop or click on each graphic; music, if any, well under the voice.

## Output: `reel-agent/reels/<slug>/edit-plan.md`

A table, one row per caption chunk or beat:

| # | time | layout | caption chunk (highlight word in **bold**) | panel graphic / animation | b-roll cue | sound |

Then:

- a list of every graphic to build, so the editor can make them once and reuse them
- the b-roll cues, for `reel-broll`
- a 3-second check: describe frame 0 and the first 3 s with the sound off. Would a stranger know
  what they get?
