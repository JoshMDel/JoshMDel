# RADC – Ryall's Auto Detailing Centre website

Static, SEO-focused website for Ryall's Auto Detailing Centre, 27 Heunis St, Colridge View, Oudtshoorn.

## Structure
- `/` – Home page, targeting Oudtshoorn car detailing searches
- `/services/` plus 5 service pages (ceramic coating, paint correction, valets & washes, headlight restoration, dents/scratches/resprays)
- `/prices/` – full catalogue price list (OfferCatalog schema)
- Areas served are listed as plain text on the home page and in the footer (plus `areaServed` schema)
- `/about/`, `/contact/` (form → pre-filled WhatsApp message), `404.html`
- `sitemap.xml`, `robots.txt`, `llms.txt`, `site.webmanifest`

## Client preview (GitHub Pages)
`.github/workflows/radc-preview.yml` builds a **noindex** preview (`RADC_PREVIEW=1`) and publishes it to
https://joshmdel.github.io/JoshMDel/ on every push that touches `radc-website/`.
One-time setup: repo **Settings → Pages → Source: GitHub Actions**.

## Editing
All business details (NAP, domain, prices, copy) live in `tools/build.py`. Edit, then rebuild:

```bash
cd radc-website
python3 tools/build.py            # regenerates all pages + sitemap
python3 tools/prepare_images.py <photo_dir>   # only when replacing source photos
```

## Before launch – TODO
1. Set `site` in `tools/build.py` to the live domain, then rebuild (canonicals, schema and sitemap all use it).
2. Change the WhatsApp Business address postcode from 6625 to 6620 so it matches Google and the site.
3. Add the Facebook page URL.
4. Replace the Maps search link with the Google Business Profile share link.
5. Deploy the `radc-website` folder to Netlify, Cloudflare Pages or GitHub Pages; add the site to Search Console and submit `sitemap.xml`.
