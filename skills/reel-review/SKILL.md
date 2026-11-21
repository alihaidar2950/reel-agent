---
name: reel-review
description: Review how a reel, TikTok or Short performed from its numbers (views, skip rate, average watch time, retention graph, shares, saves, likes, comments, follows), say where viewers left and why, and write the lesson to lessons.md. Use when the user shares Insights or analytics, a screenshot of them, or asks how a video did or why it flopped. Part of the Reel Agent team.
---

# reel-review

## Inputs

The creator's own numbers: screenshots or values from Instagram Insights, TikTok Analytics or
YouTube Studio, plus the reel itself or its script. Compare with the creator's own typical reel
(from `lessons.md`, or ask), never with someone else's account.

Read the numbers off what the creator gives you. Don't guess any that are missing; list them as
missing.

## Where did it go wrong?

| Signal | Meaning | Look at |
|---|---|---|
| High skip rate (Instagram: share of viewers who left in the first ~3 s) | The **opening** lost them | Frame 0, the first line, face or no face, the sound |
| Average watch far below the length; retention drops mid-way | The **middle** lost them | The lines where the graph drops: background, a list with no visuals, a slow beat |
| Good watch, few follows | Nothing to come back for | Is the account's promise clear? |
| Shares and saves high, reach low | Good content, weak opening or timing | The hook and the posting time |
| Comments far below what the CTA should get | The CTA wasn't seen or wasn't clear | When it appears; is the word on screen? |

Change one thing at a time when you can. If two things changed, say the result is confounded.

## Output

1. **A verdict** in 3 lines: what worked, where viewers left, the one change for next time.
2. **Rates per view:** shares, saves, likes, comments, follows, as a %.
3. **Prepend an entry to `reel-agent/lessons.md`:**

```
## <date> <reel slug>
- numbers: views X, skip Y%, avg watch Zs of Ns, shares/saves/likes/comments/follows ...
- hook: formula #, frame 0 = ...
- lost viewers at: ...
- lesson: ...
- next test: ...
```
