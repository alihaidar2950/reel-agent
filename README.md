# Reel Agent

**9 Claude skills that work as a team on your Reels, TikToks and Shorts. Free and open source.**
**٩ skills لـClaude بيشتغلوا سوا متل team عَ الريلز، التيك توك والـShorts تبعك. ببلاش وopen source.**

From the reel by [@alihaidar.dev](https://www.instagram.com/alihaidar.dev/).

It does the work around the video: hooks, script, caption, cover text, edit plan, AI b-roll,
comment replies, the week's plan, research on what's going viral in your niche, and a review of
every reel's numbers. **It doesn't film you, and it doesn't post for you.** Your face and your voice
stay yours, and nothing goes out without your yes.

بيعمل كل الشغل اللي حول الفيديو: الـhook، الـscript، الـcaption، الـcover، خطة الـedit، الـb-roll بالـAI،
الردود عَ الـcomments، خطة الأسبوع، شو عم يضرب بمجالك، وتقييم كل ريل. **ما بيصوّرك وما بينشر عنك.**
وجّك وصوتك إلك، وما بيطلع شي من دون موافقتك.

---

## The team · الـteam

| Skill | What it does · شو بيعمل |
|---|---|
| `reel-agent` | The lead: sets up your profile, runs the others, keeps the shared notes · الـlead: بيدير الباقيين |
| `reel-hooks` | 8-10 hooks from **21 hook formulas**, scored · hooks من ٢١ formula مع علامة |
| `reel-script` | Script in your dialect, platform cuts, caption, cover text · الـscript بلهجتك، والـcaption والـcover |
| `reel-edit-plan` | Shot-by-shot edit plan: layout, captions, graphics, cues · خطة الـedit لقطة بلقطة |
| `reel-broll` | AI b-roll on your own GPU, Wan 2.2 / LTX-2.5, ~$1.39/hour · b-roll بالـAI عَ GPU تبعك |
| `reel-comments` | Drafts a reply to every comment (never sends) · بيكتبلك ردّ عَ كل comment |
| `reel-week` | The week's plan: what to post, when · خطة الأسبوع: شو تنزّل وإيمتى |
| `reel-viral-finder` | Videos beating their own creator's average in your niche, and your take · الفيديوهات اللي ضاربة بمجالك |
| `reel-review` | Reads your numbers, says where viewers left, writes the lesson · بيقرا الأرقام وبيقلّك شو تغيّر |

They share one folder, `reel-agent/` (your profile, lessons, plan and one folder per reel), so each
one builds on the others' work.

---

## Install · التركيب

You need [Claude Code](https://claude.com/claude-code) (the terminal app, or the Code tab in the Claude desktop app).
بدك Claude Code.

**The easy way · الطريقة السهلة:** open Claude Code and paste:

```text
Install the skills from https://github.com/alihaidar2950/reel-agent into my ~/.claude/skills folder
```

**By hand · يدوي:**

```bash
git clone https://github.com/alihaidar2950/reel-agent
cp -r reel-agent/skills/* ~/.claude/skills/
```

Windows (PowerShell):

```powershell
git clone https://github.com/alihaidar2950/reel-agent
Copy-Item -Recurse reel-agent\skills\* $HOME\.claude\skills\
```

Then start a new Claude Code session in a folder for your content. For the viral finder you also
need Python 3.9+ and `pip install yt-dlp`.

## Use · الاستعمال

```text
/reel-agent set me up
/reel-agent make a reel about <topic>
/reel-agent plan my week
/reel-agent what's going viral in my niche?
/reel-agent reply to these comments: <paste>
/reel-agent here are my Insights for yesterday's reel: <screenshot>
```

بتقدر تحكيه بالعربي: «/reel-agent ساعدني اعمل ريل عن …»

## Honest limits · الحدود

- **Instagram doesn't show view counts publicly,** so for Instagram the viral finder compares likes
  and comments of the reel links you give it. TikTok and YouTube Shorts use real view counts.
- **AI b-roll needs a GPU you rent** (setup guide: [wan-setup](https://github.com/alihaidar2950/wan-setup)).
  Prices were checked on 2026-11-18 and change; stop the pod when you're done.
- **It plans the edit; it doesn't render the video.** Use CapCut, Premiere or an editor with the plan.
- The hook formulas are common short-form formats, not guarantees. `reel-review` checks them
  against your own numbers.

## Safety · الأمان

Scanned with [NVIDIA SkillSpector](https://github.com/NVIDIA/skillspector) v2.12.0 on 2026-11-20:
**9/100, LOW, "SAFE"** for the whole repo, with no high or critical findings. Skill by skill: seven score 0,
`reel-broll` 7 and `reel-viral-finder` 16, all LOW. The remaining notes, and why they're fine:

- `reel-viral-finder` runs yt-dlp (a subprocess). It uses no shell, accepts only plain handles and
  instagram.com links, puts `--` before every link and turns off yt-dlp's `--exec`.
- No skill pre-approves any tool (`allowed-tools`), so Claude Code asks you before every command
  and every network call. That's on purpose.
- Nothing is posted, sent or paid for by these skills. Text from videos, comments and pages is
  treated as data, never as instructions.

Scan it yourself before installing: `skillspector scan reel-agent/skills --recursive`.

MIT licence.

---

### What next? · شو بعد؟

- ⭐ Star this repo if it helped, so more people find it.
- Follow [@alihaidar.dev](https://www.instagram.com/alihaidar.dev/) on Instagram or [TikTok](https://www.tiktok.com/@alihaidar.dev) for the next free guide.
- All my free guides: [github.com/alihaidar2950](https://github.com/alihaidar2950?tab=repositories)

<div dir="rtl">

إذا فادك، حطّ ⭐ عالـrepo، وتابعني عَ [إنستغرام](https://www.instagram.com/alihaidar.dev/) أو [تيك توك](https://www.tiktok.com/@alihaidar.dev) لتوصلك الأداة الجاية ببلاش.

</div>
