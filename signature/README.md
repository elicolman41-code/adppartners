# Eli Colman — Email Signature

A professional, animated HTML email signature for Eli Colman (ADP, District Manager — Brooklyn).
The **RUN Powered by ADP** logo slides in (animated GIF), and every line is real,
clickable text with `tel:` / `mailto:` / Bookings links.

| File | What it is |
|------|------------|
| `signature.html` | **The signature to install.** Production HTML — table layout, all-inline CSS, hosted https images. |
| `preview.html` | Open in a browser to see it and watch the logo slide in. Uses the local `/assets` images. |
| `../assets/` | The images (headshot, logo, slide-in GIF) + the generator script. |

---

## 1. Add your real photo (one step — important)

Email clients can only show images from a public `https://` URL — they can't read a
pasted image or a file on your computer. These images are hosted **in this repo**, which
GitHub serves over https for free. Right now the headshot is a placeholder (the "EC" circle).

To use your real headshot:

1. Save your photo as a **square** image named `headshot.png` (≈ 240×240 px works well).
   A circular crop looks best — the signature rounds it, but Outlook ignores rounding, so a
   pre-cropped circle is safest.
2. Replace `assets/headshot.png` with your file.
3. Commit and push. The signature picks it up automatically — no HTML edits needed.

> The RUN logo (`assets/run-adp-logo.png`) is a clean text recreation used as a placeholder.
> To use ADP's official artwork, drop the official PNG in at that path and run
> `python3 assets/make_assets.py` to rebuild the slide-in GIF.

**Two things to know about the image hosting:**

- **The repo must be public** for the images to load in your recipients' inboxes
  (GitHub blocks `raw.githubusercontent.com` for private repos).
- The image URLs in `signature.html` point at the **`claude/eli-colman-contact-1ltb2n`
  branch**. If you merge this work and delete that branch, every already-sent signature
  loses its images. Before sending widely, move the three images to a **stable** location —
  a permanent branch (e.g. `main`), GitHub Pages, or a CDN — and update the `src="..."` URLs.

If you'd rather not make the repo public at all, host the three images anywhere with an
https URL (your website, a CDN, Cloudflare Images) and update the `src="..."` URLs.

---

## 2. Install the signature

### Gmail
1. Open `signature.html` in a browser.
2. Select the whole signature block (from the headshot to the button) and copy it.
3. Gmail → ⚙ **Settings** → **See all settings** → **General** → **Signature** → **Create new**.
4. Paste into the box → **Save changes**.
   *(If pasting strips the layout, use a "paste as HTML" signature add-on, or paste into
   Apple Mail / Outlook which preserve HTML better.)*

### Outlook (New Outlook / Web — what ADP uses)
1. **Settings** → **Mail** → **Compose and reply** → **Email signature**.
2. Open `signature.html` in a browser, select the signature, copy, and paste into the box.
3. Set it as default for new messages and replies → **Save**.

### Outlook (Classic desktop)
1. **File → Options → Mail → Signatures…**
2. Create a new signature, then paste the copied signature block.
   *(Classic Outlook shows only the first frame of the GIF — which is the finished logo,
   so it still looks correct, just without the slide.)*

### Apple Mail / iPhone
- Apple Mail and iOS Mail render the GIF animation and the layout faithfully. Paste the
  signature into **Settings → Mail → Signature** (iOS) or **Mail → Settings → Signatures** (Mac).

---

## What works where (the honest version)

| Client | Layout | Logo slide-in |
|--------|--------|---------------|
| Gmail (web/mobile) | ✅ | ✅ animates |
| New Outlook / Outlook web | ✅ | ✅ animates |
| Apple Mail / iOS Mail | ✅ | ✅ animates |
| Outlook Classic (Word engine) | ✅ | ▫️ shows finished logo, no motion |

The signature is built so the **resting state always looks complete** — the animation is a
bonus where the client supports it, never required for the signature to read correctly.

---

## Regenerating the images

```bash
pip install pillow
python3 assets/make_assets.py
```

Produces `run-adp-logo.png`, `run-adp-logo-slide.gif`, and the placeholder `headshot.png`.
