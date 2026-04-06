# AIE Collector

**Build your deck for [AI Engineer Europe 2026](https://ai.engineer/europe) (London, April 8-10)**

Browse 189 sessions as collector cards, filter by track and type, and save the ones you want to attend.

**[Try it live](https://aie-collector.experimenta.work/)**

## Features

- 189 collector cards with unique AI-generated backgrounds (FLUX)
- Holographic animated borders with 3D tilt on hover
- Filter by track (Context Engineering, MCP, Coding Agents...) and type (keynote, workshop, talk...)
- Save sessions to your personal deck (localStorage)
- Dedicated deck page with day-by-day timeline
- ICS calendar export

## How it's built

Single HTML file. No framework, no build step, no dependencies.

- **Frontend:** Vanilla JS + CSS (one `index.html`)
- **Data:** Open conference data from [ai.engineer](https://ai.engineer/europe)
- **Card art:** 189 images generated with [FLUX](https://docs.bfl.ai/) (Black Forest Labs), each matching the track's color palette
- **Deploy:** Cloudflare Pages (static)

## Run locally

```bash
python3 -m http.server 3000
```

Open `http://localhost:3000`

## Regenerate card images

```bash
export BFL_API_KEY=your_key
python3 scripts/generate-cards.py
```

## Credits

Built with [Claude Code](https://claude.ai/claude-code) as a side project before attending AI Engineer Europe 2026.

Conference data provided by the [AI Engineer](https://ai.engineer) open API.
