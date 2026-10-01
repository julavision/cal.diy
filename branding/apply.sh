#!/bin/sh
# Product branding (VisCal), applied at BUILD time — first step of the Vercel build
# command. Nothing in cal.diy's own files is committed differently, so
# "Sync fork" from upstream never conflicts. Upstream changes to the files
# touched below are simply re-branded on the next build.
set -e
cd "$(dirname "$0")/.."

# The name comes from the same Vercel env var the app uses, so renaming is one
# setting. Letters and digits only — it goes into sed replacements below.
NAME="${NEXT_PUBLIC_APP_NAME:-VisCal}"
case "$NAME" in *[!A-Za-z0-9]*) echo "NEXT_PUBLIC_APP_NAME must be letters/digits only" >&2; exit 1;; esac

# 1. logos, icons, favicons, manifest — the same filenames cal.diy already serves
cp -R branding/public/. apps/web/public/

# 2. logo component: light/dark images instead of dark:invert (which turns the red teal)
cp branding/Logo.tsx packages/ui/components/logo/Logo.tsx
sed -i.vcbak "s/__APP_NAME__/$NAME/g" packages/ui/components/logo/Logo.tsx && rm -f packages/ui/components/logo/Logo.tsx.vcbak

# 3a. app-store cards, BEFORE the name swap below: descriptions are raw markdown
#     ("Paypal payment app by [Cal.diy](https://cal.com)") shown unrendered, and
#     Cal-built apps list cal.com as their website and support contact.
appfix() { while IFS= read -r f; do sed -E -i.vcbak \
  -e "s#\\[(Cal\\.diy|Cal\\.com)\\]\\(https://cal\\.(com|diy)/?\\)#$NAME#g" \
  -e 's#"email": ?"(support|help)@cal\.(com|diy)"#"email": "hello@julavision.net"#g' \
  -e 's#"url": ?"https://cal\.(com|diy)/?"#"url": "https://julavision.net"#g' \
  "$f" && rm -f "$f.vcbak"; done; }
grep -rlE --include='config.json' --include='*.md' --exclude-dir=node_modules \
     '\]\(https://cal\.(com|diy)/?\)|"(support|help)@cal\.(com|diy)"|"url": ?"https://cal\.(com|diy)/?"' packages/app-store | appfix

# 3. the product name wherever cal.diy hard-codes it. Case-sensitive on purpose:
#    lowercase cal.diy web addresses are left alone. Tests are skipped.
# portable across GNU sed (Vercel) and BSD sed (a Mac): -i with a suffix, then drop the backup
rebrand() { while IFS= read -r f; do sed -i.vcbak "s/Cal\\.diy/$NAME/g" "$f" && rm -f "$f.vcbak"; done; }
grep -rlF --include='*.json' 'Cal.diy' packages/i18n/locales | rebrand
grep -rlF --include='*.ts' --include='*.tsx' --exclude-dir=node_modules --exclude-dir=.next \
     'Cal.diy' apps/web packages/ui packages/features packages/emails packages/lib packages/app-store \
  | grep -v -e '\.test\.' -e '__tests__' -e '/playwright/' -e '\.spec\.' | rebrand
# app-store cards: publisher names and descriptions ("Published by Cal.diy")
grep -rlF --include='config.json' --include='*.md' --exclude-dir=node_modules 'Cal.diy' packages/app-store | rebrand

# 4. the wordmark at the top of the desktop sidebar (Cal shows no logo there)
node branding/patch-sidebar.mjs

echo "✓ $NAME branding applied"
