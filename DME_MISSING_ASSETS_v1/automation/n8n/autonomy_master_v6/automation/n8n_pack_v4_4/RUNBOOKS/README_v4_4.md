
# DME v4.4 — Wire-in distribution + X multi-segment  • 2025-11-14

This upgrade gives you:
1) **X chunked upload** workflow that splits large videos into 4MB segments, APPENDs all, FINALIZEs, STATUS polls, then tweets.
2) A tiny **wire-in orchestrator** that you can call from the end of your W0 One-Button chain to hit:
   - `/social/fanout` (all networks from v4.2)
   - `/social/li/video` (LinkedIn native from v4.3)
   - `/social/pinterest/video` (Pinterest native from v4.3)
   - `/social/x/video_chunk` (this pack — multi-segment)

## How to connect (2 minutes)
- In **W0_OneButton_Publish_Chain**, add an HTTP Request node at the end:
  - Method: POST
  - URL: `/orchestrate/distribute`
  - JSON body:
  ```json
  {
    "videoUrl": "={$prevNode['ChooseVideoUrl'].json.videoUrl}",
    "title": "={$prevNode['ExtractContent'].json.title}",
    "summary": "={$prevNode['ExtractContent'].json.summary}",
    "linkUrl": "={$prevNode['ComposeArticlePayload'].json.canonical}",
    "tags": "#macro #forex #markets"
  }
  ```
- Import both workflows from this pack first.

## Endpoints created
- `POST /social/x/video_chunk` — chunked X upload + tweet
- `POST /orchestrate/distribute` — calls your fanout + LI native + Pinterest native + X chunk

Chunk size = **4MB**, media category = **tweet_video**.
