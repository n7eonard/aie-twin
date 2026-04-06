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

## Card gallery

Each track has its own color palette. Every card background is unique, generated from the session title.

| Context Engineering | MCP | Coding Agents | Harness Engineering |
|:---:|:---:|:---:|:---:|
| ![Context Engineering](data/card-images/043_QXByaWwgOTExOjE1.webp) | ![MCP](data/card-images/099_TGVzc29ucyBmcm9t.webp) | ![Coding Agents](data/card-images/097_UmVwbGFjaW5nIDEy.webp) | ![Harness Engineering](data/card-images/040_SGFybmVzcyBFbmdp.webp) |

| Evals & Observability | Voice & Vision | Claws & Personal Agents | AI Architects |
|:---:|:---:|:---:|:---:|
| ![Evals](data/card-images/042_V2h5IGJ1aWxkaW5n.webp) | ![Voice & Vision](data/card-images/041_QmV5b25kIFRyYW5z.webp) | ![Claws](data/card-images/039_T3BlbkNsYXcgQU1B.webp) | ![AI Architects](data/card-images/052_VGhlIERvbWFpbi1O.webp) |

| GPUs & LLM Infra | Generative Media | Google DeepMind/Gemini | Keynote |
|:---:|:---:|:---:|:---:|
| ![GPUs](data/card-images/101_T25lIExvZ2luIHRv.webp) | ![Generative Media](data/card-images/079_VGhpbmsgWW91IENh.webp) | ![DeepMind](data/card-images/082_VGhlIGFnZW50LXJl.webp) | ![Keynote](data/card-images/033_T3BlbmluZyBBZGRy.webp) |

## Credits

Built with [Claude Code](https://claude.ai/claude-code) as a side project before attending AI Engineer Europe 2026.

Conference data provided by the [AI Engineer](https://ai.engineer) open API.
