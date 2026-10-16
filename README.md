# FlexFusionX website rebuild

Homepage mockup for flexfusionx.com.au (Cyriac Kallarakkal, Performance Physiotherapy, Evandale SA).
Published preview: https://claude.ai/artifact/5dViSeKfmR4AbJpKoay75m

This is the design mockup, not the production site. The production build (planned: Astro on Vercel, Cliniko booking embed) has not started.

## Folders

| Folder | Contents |
|---|---|
| `mockups/` | Self-contained pages that open in any browser. `flexfusionx-home-latest.html` (also saved as `-v10`) is the current homepage, with `privacy.html` and `terms.html` beside it. `01`–`04` are the earlier concepts and hero studies. |
| `source/` | `home.html` is the editable page with `{{placeholders}}` for images, `pages.py` holds the Privacy Policy and Terms text. `assets.json` holds the processed images. `build.py` builds all three pages into `mockups/`. |
| `images/web-ready/` | Every image used in the mockup, resized and cropped, as plain files (names match the placeholders in `home.html`). |
| `images/originals/` | Full-resolution street runners photo with the baked-in Instagram text removed, and Cyriac's portrait from the old site. |
| `images/from-brief/` | All 18 images extracted from the brief document. |
| `images/from-instagram/` | Posts downloaded from @flex.fusionx. |
| `images/reference-only/` | The old site's hero image. It is AI-generated; do not use it. |
| `brief/` | The original brief (`FLEXFUSION X.docx`) and its extracted text. |
| `old-site/` | The live Lovable site's code, downloaded for analysis. |
| `tools/` | `vp.mjs` measures every section at 11 screen sizes; `review.mjs` screenshots every section (`node tools/review.mjs 1366x768,390x844`); `pageshots.mjs` checks the policy pages. They read `tools/preview.html`. |

## Cliniko booking

- Booking page: https://flexfusionx.au5.cliniko.com/bookings
- `flexfusionx-home-latest.html` contains the live Cliniko embed (works locally and on the real site).
- `flexfusionx-home-artifact.html` is the version published to claude.ai, which blocks third-party iframes, so it shows a card linking to the booking page instead.

## Rebuild the mockup

```
cd source
python build.py
```

Requires Python with Pillow.

## Before launch

- Prices, cancellation policy, hours, phone, parking, ABN, AHPRA number and qualification are still marked TBC on the page.
- Written permission is needed from Mount Barker United, Stride Society (Shaun), Walkerville Physiotherapy and everyone shown in photos.
- Rights to the Instagram photos and the X-rays need confirming.
- NDIS registration status decides the NDIS wording.
