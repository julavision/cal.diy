// Puts the product wordmark at the top of the desktop sidebar. Cal's own layout
// shows the logo only on tablet widths; on desktop the corner is the account
// menu, so the app had no visible logo at all. Run by apply.sh at build time.
// If upstream changes this file and the anchor is gone, it warns and skips —
// a missing logo is better than a failed build.
import { readFileSync, writeFileSync } from "node:fs";

const FILE = "apps/web/modules/shell/SideBar.tsx";
const ANCHOR = '<div className="flex h-full flex-col justify-between py-3 lg:pt-4">';
const MARK = "data-brand-wordmark";
const INSERT = `
          <Link href="/event-types" ${MARK} className="mb-4 hidden px-2 lg:block" aria-label="Home">
            <Logo />
          </Link>`;

let src = readFileSync(FILE, "utf8");
if (src.includes(MARK)) {
  console.log("sidebar wordmark: already there");
} else if (!src.includes(ANCHOR) || !/import \{ Logo \}/.test(src) || !/import Link from/.test(src)) {
  console.warn("⚠ sidebar wordmark: SideBar.tsx changed upstream — skipped (see branding/README.md)");
} else {
  writeFileSync(FILE, src.replace(ANCHOR, ANCHOR + INSERT));
  console.log("sidebar wordmark: added");
}
