# VisCal branding

This fork is Julavision's booking app, **VisCal**, at https://book.julavision.net.
Everything that makes it VisCal instead of Cal.diy lives in this folder and is
applied **at build time** by `apply.sh` — the first step of the Vercel build command:

    cd ../.. && sh branding/apply.sh && yarn db-deploy && yarn workspace @calcom/prisma seed-app-store && NODE_OPTIONS=--max-old-space-size=7168 yarn build

`seed-app-store` is what cal.diy's own Docker image runs on every boot. Without it the
app store is empty — no PayPal, Zoom or Google to connect. It's idempotent and keeps
any keys entered under Settings → Admin → Apps.

Nothing in cal.diy's own files is committed differently, so **Sync fork** from
upstream never conflicts.

| What | How |
|---|---|
| Name, support email, company | Vercel env: `NEXT_PUBLIC_APP_NAME=VisCal` etc. (89 UI strings use it). **apply.sh reads the same variable**, so renaming = change it + rebuild + regenerate the wordmark (`generate-marks.py`, `INK_PART`/`RED_PART`). |
| Hard-coded "Cal.diy" (37 locale files, 27 code files, 66 app-store files) | `apply.sh` rewrites it — case-sensitive, so `cal.diy` URLs stay |
| Logos, icons, favicons, manifest | `public/` — copied over cal.diy's files of the same name |
| Logo in dark mode | `Logo.tsx` — light/dark images instead of `dark:invert`, which turns the red teal |
| Logo in the desktop sidebar | `patch-sidebar.mjs` — Cal shows no logo on desktop (that corner is the account menu); adds the wordmark above it. Skips with a warning if upstream moves `SideBar.tsx` |
| "Powered by" badge | Off in the account's Appearance settings |
| Terms / Privacy links on the booking form | Vercel env `NEXT_PUBLIC_WEBSITE_TERMS_URL` / `…PRIVACY_POLICY_URL` → Julavision's pages (default is cal.com's) |

Marks are Russo One (Julavision's display font) as outlines: **VIS** in ink +
**CAL** in studio red `#e3142b`; icon **V.** with the red dot from "JULAVISION.".
Regenerate with `generate-marks.py` (fontTools); PNGs are rendered from
`favicon-master.svg` with `rsvg-convert`.

**The one thing to watch on upstream syncs:** Cal's `apps/web/vercel.json` ships an
empty `"functions": {}` that Vercel rejects — this fork removes it (commit 4b5932e1ad).
If a sync brings it back, delete it again.
