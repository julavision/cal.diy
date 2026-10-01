// Fixes the guest's cancellation subject, which upstream renders as
// "Canceled: Vision Call between Julavision and Ana between Julavision and Ana at …".
// sendCancelledEmailsAndSMS rebuilds each attendee's title with getEventName(),
// passing the booking title — already "X between host and guest" — as the event
// type, so the "between" clause is added twice. With no custom event name set,
// the booking title is already the right text, so use it as-is. Run by apply.sh
// at build time; warns and skips if upstream changes the code.
import { readFileSync, writeFileSync } from "node:fs";

const FILE = "packages/emails/email-manager.ts";
const ANCHOR = `              {
                ...calendarEvent,
                title: getEventName({`;
const MARK = "/* brand: cancel-subject */";
const REPLACE = `              {
                ...calendarEvent,
                title: ${MARK} !eventNameObject.eventName ? calendarEvent.title : getEventName({`;

const src = readFileSync(FILE, "utf8");
const hits = src.split(ANCHOR).length - 1;
if (src.includes(MARK)) {
  console.log("cancel subject: already patched");
} else if (hits !== 1) {
  console.warn(`⚠ cancel subject: email-manager.ts changed upstream (${hits} matches) — skipped (see branding/README.md)`);
} else {
  writeFileSync(FILE, src.replace(ANCHOR, REPLACE));
  console.log("cancel subject: patched");
}
