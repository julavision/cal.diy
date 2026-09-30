# VisionCal branding

This fork is Julavision's booking app, **VisionCal**, at https://book.julavision.net.
Everything that makes it VisionCal instead of Cal.diy lives in this folder and is
applied **at build time** by `apply.sh` — the first step of the Vercel build command:

    cd ../.. && sh branding/apply.sh && yarn db-deploy && NODE_OPTIONS=--max-old-space-size=7168 yarn build

Nothing in cal.diy's own files is committed differently, so **Sync fork** from
upstream never conflicts.

| What | How |
|---|---|
| Name, support email, company | Vercel env: `NEXT_PUBLIC_APP_NAME=VisionCal` etc. (89 UI strings use it) |
| Hard-coded "Cal.diy" (37 locale files, 27 code files) | `apply.sh` rewrites it — case-sensitive, so `cal.diy` URLs stay |
| Logos, icons, favicons, manifest | `public/` — copied over cal.diy's files of the same name |
| Logo in dark mode | `Logo.tsx` — light/dark images instead of `dark:invert`, which turns the red teal |
| "Powered by" badge | Off in the account's Appearance settings |

Marks are Russo One (Julavision's display font) as outlines: **VISION** in ink +
**CAL** in studio red `#e3142b`; icon **V.** with the red dot from "JULAVISION.".
Regenerate with `generate-marks.py` (fontTools); PNGs are rendered from
`favicon-master.svg` with `rsvg-convert`.

**The one thing to watch on upstream syncs:** Cal's `apps/web/vercel.json` ships an
empty `"functions": {}` that Vercel rejects — this fork removes it (commit 4b5932e1ad).
If a sync brings it back, delete it again.
