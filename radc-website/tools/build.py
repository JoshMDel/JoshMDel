#!/usr/bin/env python3
"""Static site generator for Ryall's Auto Detailing Centre (RADC), Oudtshoorn.

Run from the radc-website folder:   python3 tools/build.py
It writes clean-URL pages (folder/index.html), sitemap.xml, robots.txt, llms.txt
and site.webmanifest into the radc-website folder, ready for any static host.

Edit the BUSINESS dict below to update NAP details, then rebuild.
"""
import json, os, html
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# ---------------------------------------------------------------------------
# Business facts (single source of truth for NAP + schema). Keep these EXACTLY
# in line with the Google Business Profile.
# ---------------------------------------------------------------------------
BUSINESS = {
    "name": "Ryall's Auto Detailing Centre",
    "short": "RADC",
    "site": "https://www.radc.co.za",          # TODO: replace with the live domain
    "phone_display": "081 087 6539",
    "phone_e164": "+27810876539",
    "wa": "27810876539",
    "email": "rwagenaar398@gmail.com",
    "street": "27 Heunis Street",
    "suburb": "Colridge View",
    "city": "Oudtshoorn",
    "postcode": "6620",                         # Google shows 6620, WhatsApp shows 6625 - confirm
    "region": "Western Cape",
    "country": "ZA",
    "maps": "https://www.google.com/maps/search/?api=1&query=Ryall%27s+Auto+Detailing+Centre%2C+27+Heunis+St%2C+Oudtshoorn",
    "maps_embed": "https://www.google.com/maps?q=27+Heunis+St,+Oudtshoorn,+6620&output=embed",
    "tiktok": "https://www.tiktok.com/@ryall.wagenaar",
    "facebook": "",                             # TODO: paste the Facebook page URL
    "rating": "5.0",
    "reviews": "13",
    "hours_text": "Opens 8am Monday · bookings by WhatsApp",
}
B = BUSINESS
WA_LINK = f"https://wa.me/{B['wa']}?text=" + "Hi%20RADC%2C%20I%27d%20like%20a%20quote%20for%20my%20car."
TODAY = date.today().isoformat()
BIZ_ID = B["site"] + "/#business"

# ---------------------------------------------------------------------------
# Prices (from the RADC WhatsApp Business catalogue)
# ---------------------------------------------------------------------------
PRICES = {
    "washes": [
        ("Basic wash & vacuum", "Pre-wash, hand wash and interior vacuum", 130),
        ("Ceramic treatment wash", "Basic wash & vacuum plus a ceramic gloss enhancer", 260),
        ("Decon wash & clay bar", "Decontamination / acid wash and clay bar to lift bonded grime", 217),
        ("Engine bay detailing", "Engine bay cleaned and dressed", 150),
    ],
    "valets": [
        ("Full valet – sedan or hatch", "Complete interior and exterior valet", 1000),
        ("Full valet – SUV, double cab bakkie or minibus", "Complete valet for larger vehicles", 1399),
    ],
    "polish": [
        ("1-Step polish – sedan / hatch", "Single-stage machine polish for gloss and light swirl removal", 1000),
        ("2-Step polish – sedan / hatch", "Cut and refine for deeper defect correction", 1300),
        ("3-Step polish – sedan / hatch", "Full multi-stage paint correction", 1699.99),
        ("1-Step polish – SUV / minibus", "Single-stage polish for larger vehicles", 1500),
        ("2-Step polish – SUV, minibus, double cab", "Two-stage correction for larger vehicles", 2000),
        ("3-Step polish – SUV, minibus, double cab", "Full multi-stage correction for larger vehicles", 2500),
        ("Flat & polish", "Wet-sanding (flatting) and polish for heavier defects", 1999.99),
    ],
    "ceramic12": [
        ("Ceramic coating application", "Ceramic protection layer on prepared paint", 1000),
        ("1-Step polish + 12-month-plus ceramic", "Sedan / hatch", 1299.99),
        ("2-Step polish + 12-month-plus ceramic", "Sedan / hatch", 1799.99),
        ("SUV 1-Step polish + 12-month-plus ceramic", "SUV / bakkie", 2000),
        ("3-Step polish + 12-month-plus ceramic", "Sedan / hatch", 2500),
    ],
    "ceramic5": [
        ("1-Step polish + 5-year ceramic", "Sedan / hatch", 4299),
        ("2-Step polish + 5-year ceramic", "Sedan / hatch", 4799),
        ("3-Step polish + 5-year ceramic", "Sedan / hatch", 5500),
        ("SUV 1-Step polish + 5-year ceramic", "SUV / bakkie", 5500),
        ("2-Step polish + 5-year ceramic – SUV / bakkie", "SUV / bakkie", 6000),
    ],
    "headlights": [
        ("Headlight repair (inside clean)", "Opening and cleaning headlights from the inside, removing haze and moisture marks", 200),
        ("Headlight restoration", "Sanding, polishing and protecting yellowed, oxidised lenses", 250),
    ],
    "repairs": [
        ("Bumper alignment", "Re-aligning loose or misaligned bumpers", 200),
        ("Scratch & faded-paint removal", "Removing scratches and small dents and reviving faded panels", 300),
        ("Rim repairs", "Kerb-rash and rim restoration", 400),
        ("Dent repairs", "Removing small, minor dents with respray", 1600),
        ("Full body respray", "Full exterior respray, materials included", 13500),
    ],
}

def rand(v):
    if float(v).is_integer():
        return "R" + f"{int(v):,}".replace(",", " ")
    return "R" + f"{v:,.2f}".replace(",", " ")

def esc(s):
    return html.escape(s, quote=True)

# ---------------------------------------------------------------------------
# Icons (inline SVG, no icon font)
# ---------------------------------------------------------------------------
ICONS = {
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.3zM12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2z"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/><path d="M19 17l.8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/></svg>',
    "car": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14M3 13l2-6a2 2 0 0 1 1.9-1.4h10.2A2 2 0 0 1 19 7l2 6v4a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-1H6v1a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><circle cx="7.5" cy="13.5" r="1"/><circle cx="16.5" cy="13.5" r="1"/></svg>',
    "bulb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.7l5.7 5.7a8 8 0 1 1-11.4 0z"/></svg>',
    "wrench": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0 5 5L22 14l-8 8-2.3-2.3a4 4 0 0 0-5-5L2 10l8-8z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13S3 17 3 10a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
    "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8z"/></svg>',
    "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>',
}

def btn_wa(label="WhatsApp us", cls="btn btn-wa", text=None):
    href = WA_LINK if text is None else f"https://wa.me/{B['wa']}?text=" + text
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener">{ICONS["wa"]}{label}</a>'

def btn_call(label=None, cls="btn btn-ghost"):
    return f'<a class="{cls}" href="tel:{B["phone_e164"]}">{ICONS["phone"]}{label or "Call " + B["phone_display"]}</a>'

def picture(name, widths, alt, sizes, w, h, eager=False, cls=""):
    srcset_webp = ", ".join(f"/assets/img/{name}-{x}.webp {x}w" for x in widths)
    srcset_jpg = ", ".join(f"/assets/img/{name}-{x}.jpg {x}w" for x in widths)
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="{srcset_webp}" sizes="{sizes}">'
            f'<img src="/assets/img/{name}-{widths[-1]}.jpg" srcset="{srcset_jpg}" sizes="{sizes}" '
            f'alt="{esc(alt)}" width="{w}" height="{h}" {load} decoding="async"{(" class=" + chr(34) + cls + chr(34)) if cls else ""}></picture>')

# ---------------------------------------------------------------------------
# Site structure
# ---------------------------------------------------------------------------
SERVICES = [
    {"slug": "ceramic-coating", "nav": "Ceramic Coating", "icon": "shield",
     "from": 1000, "teaser": "12-month-plus and 5-year ceramic packages, paired with 1-, 2- or 3-step polishing for a slick, protected finish."},
    {"slug": "paint-correction-polishing", "nav": "Paint Correction & Polishing", "icon": "spark",
     "from": 1000, "teaser": "1-step, 2-step and 3-step machine polishing to remove swirls, oxidation and dullness and bring back deep gloss."},
    {"slug": "car-valet-wash", "nav": "Valets & Washes", "icon": "drop",
     "from": 130, "teaser": "From a quick wash & vacuum to a full valet, decon wash, clay bar and engine-bay detail."},
    {"slug": "headlight-restoration", "nav": "Headlight Restoration", "icon": "bulb",
     "from": 200, "teaser": "Yellow, cloudy headlights sanded, polished and protected — safer night driving and a fresher-looking car."},
    {"slug": "dent-scratch-repair", "nav": "Dents, Scratches & Resprays", "icon": "wrench",
     "from": 200, "teaser": "Scratch and faded-paint removal, minor dent repairs, rim repairs, bumper alignment and full resprays."},
]

AREAS = [
    {"slug": "george", "name": "George", "region": "Garden Route",
     "places": ["George", "Blanco", "Wilderness", "Pacaltsdorp", "Herold's Bay"],
     "dist": "about 55 km", "time": "roughly 50–60 minutes", "route": "the N12 over the Outeniqua Pass"},
    {"slug": "mossel-bay", "name": "Mossel Bay", "region": "Garden Route",
     "places": ["Mossel Bay", "Hartenbos", "Great Brak River", "KwaNonqaba", "Dana Bay"],
     "dist": "about 85 km", "time": "roughly 1 hour", "route": "the R328 over the Robinson Pass"},
    {"slug": "knysna-plettenberg-bay", "name": "Knysna & Plettenberg Bay", "region": "Garden Route",
     "places": ["Knysna", "Sedgefield", "Plettenberg Bay", "Brenton-on-Sea", "Keurboomstrand"],
     "dist": "about 120–150 km", "time": "roughly 1 h 45 – 2 hours", "route": "the N12 to George and the N2 east"},
    {"slug": "klein-karoo", "name": "the Klein Karoo", "region": "Klein Karoo",
     "places": ["De Rust", "Dysselsdorp", "Calitzdorp", "Ladismith", "Uniondale", "Van Wyksdorp"],
     "dist": "25–100 km", "time": "20 minutes to about 1 h 15", "route": "the R62 and N12"},
    {"slug": "central-karoo", "name": "the Central Karoo", "region": "Central Karoo",
     "places": ["Prince Albert", "Beaufort West", "Laingsburg", "Klaarstroom", "Leeu-Gamka"],
     "dist": "about 75–230 km", "time": "roughly 1 h 15 – 2 h 45", "route": "Meiringspoort (N12) or the Swartberg Pass"},
]

NAV = [("/", "Home"), ("/services/", "Services"), ("/prices/", "Prices"),
       ("/areas/", "Areas"), ("/about/", "About"), ("/contact/", "Contact")]

PAGES = []  # (path, priority) for sitemap

# ---------------------------------------------------------------------------
# Schema helpers
# ---------------------------------------------------------------------------
def area_served():
    names = ["Oudtshoorn", "George", "Mossel Bay", "Knysna", "Plettenberg Bay", "Wilderness",
             "Sedgefield", "De Rust", "Dysselsdorp", "Calitzdorp", "Ladismith", "Uniondale",
             "Prince Albert", "Beaufort West", "Laingsburg"]
    out = [{"@type": "City", "name": n} for n in names]
    out += [{"@type": "AdministrativeArea", "name": "Garden Route District (Eden)"},
            {"@type": "AdministrativeArea", "name": "Central Karoo District"},
            {"@type": "Place", "name": "Klein Karoo"}]
    return out

def business_schema():
    same = [u for u in (B["tiktok"], B["facebook"]) if u]
    return {
        "@type": ["AutoWash", "AutoBodyShop"],
        "@id": BIZ_ID,
        "name": B["name"],
        "alternateName": B["short"],
        "slogan": "Cleaner | Shinier | Protected",
        "description": ("Car detailing centre in Oudtshoorn offering ceramic coating, 1- to 3-step paint "
                        "correction, full valets, headlight restoration, dent and scratch repair and resprays "
                        "for drivers across the Garden Route, Klein Karoo and Central Karoo."),
        "url": B["site"] + "/",
        "telephone": B["phone_e164"],
        "email": B["email"],
        "image": [B["site"] + "/assets/img/og-radc-car-detailing-oudtshoorn.jpg",
                  B["site"] + "/assets/img/honda-civic-paint-correction-gloss-1080.jpg"],
        "logo": B["site"] + "/assets/img/radc-logo-512.png",
        "priceRange": "R130 – R13 500",
        "currenciesAccepted": "ZAR",
        "address": {"@type": "PostalAddress", "streetAddress": B["street"],
                    "addressLocality": B["city"], "addressRegion": B["region"],
                    "postalCode": B["postcode"], "addressCountry": B["country"]},
        "hasMap": B["maps"],
        "areaServed": area_served(),
        "knowsAbout": ["Car detailing", "Ceramic coating", "Paint correction", "Machine polishing",
                       "Headlight restoration", "Car valeting", "Dent repair", "Vehicle respray"],
        "contactPoint": {"@type": "ContactPoint", "telephone": B["phone_e164"],
                         "contactType": "customer service", "areaServed": "ZA",
                         "availableLanguage": ["English", "Afrikaans"]},
        **({"sameAs": same} if same else {}),
    }

def breadcrumb_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": B["site"] + p}
        for i, (p, n) in enumerate(crumbs)]}

def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def offer_catalog(name, rows):
    return {"@type": "OfferCatalog", "name": name, "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n, "description": d},
         "priceSpecification": {"@type": "PriceSpecification", "price": f"{p:.2f}",
                                "priceCurrency": "ZAR", "minPrice": f"{p:.2f}"}}
        for n, d, p in rows]}

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
def crumbs_html(crumbs):
    items = []
    for i, (p, n) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            items.append(f'<li aria-current="page">{esc(n)}</li>')
        else:
            items.append(f'<li><a href="{p}">{esc(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(items)}</ol></nav>'

def faq_html(faqs, heading="Frequently asked questions"):
    items = "".join(f'<details><summary>{esc(q)}</summary><div class="answer"><p>{a}</p></div></details>' for q, a in faqs)
    return f'<div class="faq"><h2>{heading}</h2>{items}</div>'

def cta_band(title="Ready for that showroom shine?", text=None):
    text = text or ("Send us a WhatsApp with your car, a couple of photos and what you'd like done. "
                    "We'll reply with a quote and the next open slot.")
    return f'''<section class="block"><div class="wrap"><div class="cta-band">
  <div><h2>{title}</h2><p class="lead" style="margin:0">{text}</p></div>
  <div class="btn-row" style="margin:0;justify-content:flex-start">{btn_wa("WhatsApp for a quote")}{btn_call()}</div>
</div></div></section>'''

def header(path):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if (href == path or (href != "/" and path.startswith(href))) else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
  <a class="brand" href="/" aria-label="{esc(B['name'])} – home">
    <picture><source type="image/webp" srcset="/assets/img/radc-logo-white-240.webp 1x, /assets/img/radc-logo-white-480.webp 2x">
    <img src="/assets/img/radc-logo-white-240.png" alt="RADC – Ryall's Auto Detailing Centre logo" width="118" height="48"></picture>
  </a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav">Menu</button>
  <nav id="site-nav" class="nav" aria-label="Main">{"".join(links)}{btn_wa("Book", "btn btn-primary")}</nav>
</div></header>'''

def footer():
    svc = "".join(f'<li><a href="/services/{s["slug"]}/">{s["nav"]}</a></li>' for s in SERVICES)
    areas = "".join(f'<li><a href="/areas/{a["slug"]}/">Detailing for {a["name"].replace("the ", "")}</a></li>' for a in AREAS)
    social = f'<li><a href="{B["tiktok"]}" rel="noopener" target="_blank">TikTok @ryall.wagenaar</a></li>'
    if B["facebook"]:
        social += f'<li><a href="{B["facebook"]}" rel="noopener" target="_blank">Facebook</a></li>'
    return f'''<footer class="site-footer"><div class="wrap">
  <div class="cols">
    <div>
      <img src="/assets/img/radc-logo-white-240.png" alt="RADC logo" width="140" height="57" loading="lazy" style="margin-bottom:16px">
      <address><strong style="color:var(--text)">{B["name"]}</strong><br>
      {B["street"]}, {B["suburb"]}<br>{B["city"]}, {B["postcode"]}, {B["region"]}<br>
      <a href="tel:{B["phone_e164"]}">{B["phone_display"]}</a><br>
      <a href="mailto:{B["email"]}">{B["email"]}</a></address>
      <p class="small" style="margin-top:12px">{B["hours_text"]}</p>
    </div>
    <div><h3>Services</h3><ul>{svc}<li><a href="/prices/">Full price list</a></li></ul></div>
    <div><h3>Areas we serve</h3><ul><li><a href="/">Oudtshoorn car detailing</a></li>{areas}</ul></div>
    <div><h3>RADC</h3><ul><li><a href="/about/">About us</a></li><li><a href="/contact/">Contact &amp; directions</a></li>
      <li><a href="{B["maps"]}" rel="noopener" target="_blank">Google reviews ({B["rating"]}★)</a></li>{social}</ul></div>
  </div>
  <div class="legal"><span>© {date.today().year} {B["name"]} (RADC), Oudtshoorn. All rights reserved.</span>
  <span class="verse">“Everything through Christ our Lord.” – Philippians 4:13</span></div>
</div></footer>
<div class="mobile-cta">{btn_call("Call")}{btn_wa("WhatsApp")}</div>'''

def render(path, title, description, body, schema_extra=None, crumbs=None, priority="0.7",
           og_image="/assets/img/og-radc-car-detailing-oudtshoorn.jpg", noindex=False):
    graph = [business_schema(),
             {"@type": "WebPage", "@id": B["site"] + path + "#webpage", "url": B["site"] + path,
              "name": title, "description": description, "inLanguage": "en-ZA",
              "isPartOf": {"@id": B["site"] + "/#website"}, "about": {"@id": BIZ_ID},
              "dateModified": TODAY}]
    if path == "/":
        graph.append({"@type": "WebSite", "@id": B["site"] + "/#website", "url": B["site"] + "/",
                      "name": B["name"], "alternateName": "RADC", "inLanguage": "en-ZA",
                      "publisher": {"@id": BIZ_ID}})
    if crumbs:
        graph.append(breadcrumb_schema(crumbs))
    graph += schema_extra or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    canonical = B["site"] + path
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    page = f'''<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#06080d">
<meta name="geo.region" content="ZA-WC">
<meta name="geo.placename" content="Oudtshoorn">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_ZA">
<meta property="og:site_name" content="{esc(B['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{B['site']}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/img/radc-logo-192.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/main.js" defer></script>
</body>
</html>
'''
    if path == "/404.html":
        out_dir, fname = ROOT, "404.html"
    else:
        out_dir, fname = os.path.join(ROOT, path.strip("/")), "index.html"
        os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
        f.write(page)
    if not noindex:
        PAGES.append((path, priority))

def page_hero(crumbs, eyebrow, h1, lead, ctas=True):
    btns = f'<div class="btn-row">{btn_wa("WhatsApp for a quote")}{btn_call()}</div>' if ctas else ""
    return f'''<section class="page-hero"><div class="wrap">
{crumbs_html(crumbs)}
<span class="eyebrow">{eyebrow}</span>
<h1>{h1}</h1>
<p class="lead">{lead}</p>{btns}
</div></section>'''

def price_table(rows, caption=None):
    cap = f"<caption class='sr-only' style='position:absolute;left:-9999px'>{esc(caption)}</caption>" if caption else ""
    trs = "".join(f"<tr><td>{esc(n)}<small>{esc(d)}</small></td><td>{rand(p)}</td></tr>" for n, d, p in rows)
    return f'<table class="price-table">{cap}<thead><tr><th scope="col">Package</th><th scope="col">From</th></tr></thead><tbody>{trs}</tbody></table>'

def service_cards(exclude=None):
    out = []
    for s in SERVICES:
        if s["slug"] == exclude:
            continue
        out.append(f'''<a class="card" href="/services/{s["slug"]}/"><div class="icon">{ICONS[s["icon"]]}</div>
<h3>{s["nav"]}</h3><p class="muted">{s["teaser"]}</p><span class="price">From {rand(s["from"])}</span><br><span class="more">View details →</span></a>''')
    return "".join(out)

FACTS = f'''<div class="facts"><h2 style="font-size:1.4rem">RADC at a glance</h2><dl>
<dt>Business</dt><dd>{B["name"]} (RADC)</dd>
<dt>What we do</dt><dd>Car detailing, ceramic coating, paint correction, valets, headlight restoration, dent &amp; scratch repair, resprays</dd>
<dt>Address</dt><dd>{B["street"]}, {B["suburb"]}, {B["city"]}, {B["postcode"]}</dd>
<dt>Phone / WhatsApp</dt><dd><a href="tel:{B["phone_e164"]}">{B["phone_display"]}</a></dd>
<dt>Prices</dt><dd>From R130 (wash &amp; vacuum) to R6 000 (SUV 5-year ceramic package)</dd>
<dt>Google rating</dt><dd>{B["rating"]} ★ from {B["reviews"]} reviews</dd>
<dt>Serving</dt><dd>Oudtshoorn, the Klein Karoo, Garden Route (George, Mossel Bay, Knysna, Plett) and Central Karoo</dd>
</dl></div>'''

# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
def build_home():
    faqs = [
        ("Where is Ryall's Auto Detailing Centre in Oudtshoorn?",
         f"RADC is at {B['street']}, {B['suburb']}, {B['city']} {B['postcode']}, just off the R62 / 5th Avenue near the Toekomsrus Community Centre. Use the Google Maps link on our <a href=\"/contact/\">contact page</a> for directions."),
        ("How much does car detailing cost in Oudtshoorn?",
         "At RADC a basic wash and vacuum starts at R130, a full valet from R1 000 (sedan/hatch), machine polishing from R1 000 and polish-plus-ceramic packages from R1 299.99. See the <a href=\"/prices/\">full price list</a>; final quotes depend on vehicle size and condition."),
        ("Do you do ceramic coating?",
         "Yes. We offer 12-month-plus and 5-year ceramic packages, each combined with a 1-, 2- or 3-step polish so the coating locks in corrected, glossy paint. <a href=\"/services/ceramic-coating/\">Read about ceramic coating</a>."),
        ("How do I book?",
         f"The quickest way is WhatsApp on {B['phone_display']}. Send your vehicle make and model, a couple of photos and the service you're interested in, and we'll confirm a price and date."),
        ("I live in George, Mossel Bay or the Karoo. Is it worth the drive?",
         "Many of our services, like paint correction and ceramic coating, are once-off investments that last months or years, so a single trip to Oudtshoorn is well worth it. See our <a href=\"/areas/\">areas we serve</a> page for routes and planning tips."),
        ("Can you fix yellow, cloudy headlights?",
         "Yes. Headlight restoration (from R250) sands away the oxidised layer, polishes the lens clear and protects it. If there is haze or moisture inside the lamp, our headlight repair (from R200) cleans them from the inside."),
    ]
    body = f'''<section class="hero">
  <div class="hero-media">{picture("radc-hero-civic-gloss", (640, 1080), "Deep-gloss Bordeaux Honda Civic detailed by RADC in Oudtshoorn", "100vw", 1080, 808, eager=True)}</div>
  <div class="wrap">
    <p class="tagline">Cleaner <span>|</span> Shinier <span>|</span> Protected</p>
    <h1>Car Detailing &amp; <span class="accent">Ceramic Coating</span> in Oudtshoorn</h1>
    <p class="lead">Ryall's Auto Detailing Centre (RADC) restores showroom shine to cars, bakkies and SUVs across the Klein Karoo and Garden Route — from a R130 wash to multi-step paint correction and 5-year ceramic protection.</p>
    <div class="btn-row">{btn_wa("Get a quote on WhatsApp")}<a class="btn btn-ghost" href="/prices/">{ICONS["tag"]}View prices</a></div>
    <ul class="trust">
      <li><span class="stars" aria-hidden="true">★★★★★</span> <a href="{B["maps"]}" target="_blank" rel="noopener">{B["rating"]} on Google ({B["reviews"]} reviews)</a></li>
      <li>{ICONS["pin"]} {B["suburb"]}, Oudtshoorn</li>
      <li>{ICONS["tag"]} Transparent, published prices</li>
    </ul>
  </div>
</section>

<section class="block"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What we do</span>
  <h2>Detailing services in Oudtshoorn</h2>
  <p class="lead">Every job is done by hand with machine-polishing equipment and proper decontamination — we don't just wash cars, we detail and polish every surface for a deeper, richer gloss.</p></div>
  <div class="grid g3">{service_cards()}
    <a class="card" href="/prices/" style="border-color:#1d3b6b;background:linear-gradient(180deg,#0b2347,#081428)"><div class="icon">{ICONS["tag"]}</div>
    <h3>See every price</h3><p class="muted">30+ packages for sedans, hatches, SUVs, bakkies and minibuses — all listed upfront.</p><span class="more">Full price list →</span></a>
  </div>
</div></section>

<section class="block alt"><div class="wrap split">
  <div>
    <span class="eyebrow">Why drivers choose RADC</span>
    <h2>Built for Karoo sun, dust and Garden Route salt air</h2>
    <p>Oudtshoorn summers regularly push past 35 °C, and the Klein Karoo sun is relentless on clear coats, plastics and headlights. Gravel roads coat paint in fine dust, and coastal trips leave salt behind. That combination is exactly what causes faded, chalky paint and yellow headlights.</p>
    <ul class="checklist">
      <li><strong>Correction before protection</strong> — we polish out swirls and oxidation first, so ceramic coatings seal in a perfect finish, not the damage.</li>
      <li><strong>Packages for every vehicle</strong> — separate pricing for hatches, sedans, SUVs, double cabs and minibuses, so you only pay for your size.</li>
      <li><strong>Upfront prices</strong> — our full catalogue is published on this site and on WhatsApp.</li>
      <li><strong>Local and owner-run</strong> — you deal directly with the person detailing your car.</li>
    </ul>
    <div class="btn-row">{btn_wa("Ask about your car")}<a class="btn btn-ghost" href="/about/">About RADC</a></div>
  </div>
  <figure class="photo">{picture("honda-civic-headlight-detail-oudtshoorn", (480, 800, 1080), "Close-up of a glossy red Honda Civic headlight and bonnet after detailing at RADC", "(max-width:860px) 100vw, 480px", 1080, 1620)}</figure>
</div></section>

<section class="block"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How it works</span><h2>Booking in four easy steps</h2></div>
  <ol class="steps">
    <li><strong>WhatsApp us</strong>Send your make, model and a few photos to {B["phone_display"]}.</li>
    <li><strong>Get a clear quote</strong>We recommend the right package and confirm the price.</li>
    <li><strong>Drop off in Oudtshoorn</strong>Bring your vehicle to {B["street"]} on your booked day.</li>
    <li><strong>Collect the shine</strong>We walk you through the result and aftercare tips.</li>
  </ol>
</div></section>

<section class="block alt"><div class="wrap split">
  <figure class="photo">{picture("honda-civic-paint-correction-gloss", (480, 800, 1080), "Bordeaux red Honda Civic with mirror-like paint reflections under night lighting", "(max-width:860px) 100vw, 520px", 1080, 1440)}<figcaption>Deep, wet-look gloss on older single-stage red paint — the kind of result multi-step polishing and ceramic protection are designed for.</figcaption></figure>
  <div>
    <span class="eyebrow">Areas we serve</span>
    <h2>Oudtshoorn, the Klein Karoo &amp; the Garden Route</h2>
    <p>Our centre is in Oudtshoorn, the heart of the Klein Karoo — within an hour of George and Mossel Bay and an easy drive from De Rust, Calitzdorp, Dysselsdorp and Prince Albert.</p>
    <ul class="area-list">
      <li><a href="/">Oudtshoorn &amp; Bongolethu</a></li>
      <li><a href="/areas/george/">George &amp; Wilderness</a></li>
      <li><a href="/areas/mossel-bay/">Mossel Bay &amp; Hartenbos</a></li>
      <li><a href="/areas/knysna-plettenberg-bay/">Knysna &amp; Plett</a></li>
      <li><a href="/areas/klein-karoo/">De Rust, Calitzdorp, Ladismith</a></li>
      <li><a href="/areas/central-karoo/">Prince Albert &amp; Beaufort West</a></li>
    </ul>
    <a class="btn btn-ghost" href="/areas/">All areas →</a>
  </div>
</div></section>

<section class="block"><div class="wrap split" style="align-items:start">
  {faq_html(faqs)}
  {FACTS}
</div></section>
{cta_band()}'''
    render("/", "Car Detailing Oudtshoorn | Ceramic Coating & Polishing | RADC",
           "Ryall's Auto Detailing Centre (RADC) in Oudtshoorn: ceramic coating, paint correction, full valets, headlight restoration & dent repair. 5.0★ on Google. WhatsApp 081 087 6539.",
           body, [faq_schema([(q, html.unescape(strip_tags(a))) for q, a in faqs])], priority="1.0")

def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)

# ---------------------------------------------------------------------------
# SERVICES
# ---------------------------------------------------------------------------
SERVICE_CONTENT = {
"ceramic-coating": {
  "title": "Ceramic Coating Oudtshoorn | 12-Month & 5-Year Packages | RADC",
  "desc": "Ceramic coating in Oudtshoorn from R1 299.99 incl. machine polish. 12-month-plus and 5-year packages for cars, SUVs & bakkies. Serving George, Mossel Bay & the Karoo.",
  "h1": "Ceramic Coating in Oudtshoorn",
  "lead": "Lock in a deep gloss and protect your paint from Karoo UV, dust, bird droppings and road grime. Every RADC ceramic package starts with machine polishing so the coating seals in a corrected finish.",
  "price_keys": [("12-month-plus ceramic packages", "ceramic12"), ("5-year ceramic packages", "ceramic5")],
  "body": f'''
<h2>What is a ceramic coating?</h2>
<p>A ceramic coating is a liquid protective layer that bonds to your car's clear coat and cures into a hard, glossy, water-repellent shell. Compared with a traditional wax, it lasts far longer, makes washing much easier (dirt and water slide off), and adds a layer of defence against UV fading, light chemical etching and environmental fallout.</p>
<p>A coating is <strong>not</strong> a force-field — it won't stop stone chips or deep scratches — but on a well-maintained car it keeps the paint looking freshly polished for a long time.</p>

<h2>Why every package includes a polish</h2>
<p>A coating locks in whatever is underneath it — including swirl marks, water spots and oxidation. That's why RADC pairs every ceramic package with a 1-step, 2-step or 3-step machine polish:</p>
<ul class="checklist">
  <li><strong>1-Step + ceramic</strong> — for newer cars or paint in good condition that needs a gloss boost before coating.</li>
  <li><strong>2-Step + ceramic</strong> — a cutting stage plus a refining stage for moderate swirls and dullness.</li>
  <li><strong>3-Step + ceramic</strong> — full paint correction for older, faded or heavily swirled paint before protection.</li>
</ul>

<h2>12-month-plus vs 5-year ceramic: which should you choose?</h2>
<p>Choose a <strong>12-month-plus</strong> package if you want an affordable gloss and protection boost, are planning to sell the car, or simply want to try a coating. Choose a <strong>5-year</strong> package if you plan to keep the vehicle, park outside a lot, or regularly drive gravel and coastal roads — the longer-life coating spreads the cost over years of easier maintenance.</p>

<h2>Why ceramic protection makes sense in the Klein Karoo</h2>
<p>Oudtshoorn's long, hot summers and high UV levels slowly oxidise unprotected paint, especially reds, blacks and older single-stage finishes. Add fine Karoo dust and the salt air you pick up on trips to Mossel Bay or George, and paint ages quickly. A coating keeps contamination from bonding, so a simple wash restores the shine.</p>

<h2>Ceramic coating aftercare</h2>
<ul class="checklist">
  <li>Avoid washing the car for the first few days while the coating fully cures.</li>
  <li>Hand wash with a pH-neutral shampoo and clean microfibre — avoid brush-type car washes.</li>
  <li>Remove bird droppings and bugs promptly.</li>
  <li>Book a <a href="/services/car-valet-wash/">ceramic treatment wash</a> periodically to top up the hydrophobic layer.</li>
</ul>''',
  "faqs": [
    ("How much is ceramic coating in Oudtshoorn?", "RADC ceramic packages start at R1 299.99 for a 1-step polish plus 12-month-plus ceramic on a sedan or hatch. 5-year packages run from R4 299 (sedan/hatch) to R6 000 (SUV/bakkie with 2-step polish)."),
    ("How long does a ceramic coating take?", "Plan to leave your car with us for the day. Larger vehicles and 3-step correction packages can take longer — we'll confirm timing when you book."),
    ("Can you ceramic coat a bakkie or SUV?", "Yes. We have dedicated SUV, double-cab bakkie and minibus ceramic packages priced for the larger surface area."),
    ("Does ceramic coating protect against stone chips?", "No. A ceramic coating protects against UV, contamination and light marring and makes washing easier, but it does not stop stone chips. Consider paint protection film for high-impact areas."),
  ],
},
"paint-correction-polishing": {
  "title": "Paint Correction & Car Polishing Oudtshoorn | 1-3 Step | RADC",
  "desc": "Machine polishing & paint correction in Oudtshoorn from R1 000. Remove swirls, oxidation & faded paint with 1-, 2- or 3-step polishing. Cars, SUVs, bakkies & minibuses.",
  "h1": "Paint Correction &amp; Machine Polishing in Oudtshoorn",
  "lead": "Faded, swirled or chalky paint? Our 1-, 2- and 3-step machine polishing removes a fine layer of damaged clear coat to reveal the deep colour and gloss underneath.",
  "price_keys": [("Polishing packages", "polish")],
  "body": '''
<h2>What is paint correction?</h2>
<p>Paint correction is the process of machine-polishing your car's paint to remove defects such as swirl marks, holograms, light scratches, water-spot etching and oxidation. Instead of hiding marks with fillers, correction levels the clear coat so light reflects evenly — which is what creates that wet, mirror-like gloss.</p>

<h2>1-step, 2-step or 3-step: what's the difference?</h2>
<ul class="checklist">
  <li><strong>1-Step polish</strong> — a single all-in-one polish. Ideal for newer cars, or paint that's dull but not badly damaged. Big gloss improvement for the price.</li>
  <li><strong>2-Step polish</strong> — a cutting stage to remove moderate defects, followed by a finishing polish to restore clarity.</li>
  <li><strong>3-Step polish</strong> — our most thorough correction: heavier cut, refine and jewel finish. Best for older vehicles, dark colours and show cars.</li>
  <li><strong>Flat &amp; polish</strong> — wet-sanding (flatting) to level deeper defects, orange peel or runs, followed by polishing.</li>
</ul>
<p>Not sure which you need? Send us photos on WhatsApp in direct sunlight — swirls show up clearly — and we'll recommend the right level.</p>

<h2>What's included</h2>
<ul class="checklist">
  <li>Pre-wash and hand wash</li>
  <li>Decontamination to remove bonded grime before any polishing</li>
  <li>Machine polishing stages according to your package</li>
  <li>Final wipe-down to inspect the finish</li>
</ul>

<h2>Why paint fades so fast in Oudtshoorn</h2>
<p>Intense Klein Karoo sun breaks down clear coat over time, leaving reds pink, blacks grey and older single-stage paint chalky. Dust wiped off dry, rough car-wash brushes and gravel roads add swirls. The good news: most of this damage sits in the top layer and can be polished out.</p>

<h2>Protect your corrected paint</h2>
<p>Once your paint is corrected, protect it. Upgrading to a <a href="/services/ceramic-coating/">polish + ceramic package</a> costs less than doing the two separately and keeps the finish looking fresh for months or years.</p>''',
  "faqs": [
    ("How much does car polishing cost in Oudtshoorn?", "At RADC a 1-step polish starts at R1 000 for a sedan or hatch, 2-step at R1 300 and 3-step at R1 699.99. SUVs, minibuses and double cabs start at R1 500, R2 000 and R2 500 respectively."),
    ("Will polishing remove all scratches?", "Polishing removes swirls and scratches in the clear coat. A scratch you can catch with your fingernail has likely gone through the clear coat and may need touch-up or a repair — see our dent & scratch repair service."),
    ("Is machine polishing safe for my paint?", "Yes, when done properly. Correction removes only a tiny amount of clear coat, and we choose the least aggressive method that achieves the result."),
    ("Can you polish a minibus or double-cab bakkie?", "Yes — we have dedicated SUV, minibus and double-cab polishing packages."),
  ],
},
"car-valet-wash": {
  "title": "Car Valet & Car Wash Oudtshoorn | Full Valet from R1 000 | RADC",
  "desc": "Car wash & full valet in Oudtshoorn. Wash & vacuum from R130, decon wash & clay bar R217, engine detailing R150, full valet from R1 000. Book on WhatsApp.",
  "h1": "Car Valet &amp; Wash Services in Oudtshoorn",
  "lead": "From a quick wash and vacuum to a full inside-and-out valet, RADC gets your car, bakkie or SUV properly clean — not just rinsed.",
  "price_keys": [("Washes & add-ons", "washes"), ("Full valets", "valets")],
  "body": '''
<h2>Choose the right clean</h2>
<ul class="checklist">
  <li><strong>Basic wash &amp; vacuum (R130)</strong> — pre-wash, hand wash and interior vacuum for regular upkeep.</li>
  <li><strong>Ceramic treatment wash (R260)</strong> — our basic wash plus a ceramic gloss enhancer that leaves paint slick and water-repellent. Great for maintaining coated cars.</li>
  <li><strong>Decon wash &amp; clay bar (R217)</strong> — a decontamination/acid wash and clay bar to pull out bonded grime, rail dust and overspray that a normal wash leaves behind. Paint feels smooth as glass afterwards.</li>
  <li><strong>Engine bay detailing (R150)</strong> — engine bay cleaned and dressed. Ideal before a sale or service.</li>
  <li><strong>Full valet (from R1 000)</strong> — a complete interior and exterior valet for sedans and hatches, from R1 399 for SUVs, double cabs and minibuses.</li>
</ul>

<h2>Why a proper hand wash matters</h2>
<p>Automatic brushes and dirty sponges drag Karoo dust across your paint and cause the swirl marks that make cars look dull. A careful hand wash with a pre-wash stage loosens grit first, so far less of it gets rubbed into the clear coat.</p>

<h2>Full valet: ideal for</h2>
<ul class="checklist">
  <li>Selling your car — a valeted car photographs better and sells faster.</li>
  <li>After a family holiday to the coast, or a season of farm and gravel roads.</li>
  <li>Taxis, shuttles and minibuses that need a regular deep clean.</li>
  <li>Spotless interiors — a "spotless interior" is something our Google reviewers mention.</li>
</ul>''',
  "faqs": [
    ("How much is a car wash at RADC in Oudtshoorn?", "A basic wash and vacuum is R130. A ceramic treatment wash is R260 and a decon wash with clay bar is R217."),
    ("How much is a full valet?", "A full valet is R1 000 for a sedan or hatch and R1 399 for SUVs, double-cab bakkies and minibuses."),
    ("What does a clay bar do?", "A clay bar lifts contaminants bonded to the paint surface that washing can't remove, leaving it smooth. It's also the essential first step before polishing or coating."),
    ("Do you clean minibuses and taxis?", "Yes. We have valet pricing for SUVs, double cabs and minibuses — WhatsApp us for regular or fleet bookings."),
  ],
},
"headlight-restoration": {
  "title": "Headlight Restoration Oudtshoorn | Yellow Headlights Fixed | RADC",
  "desc": "Headlight restoration in Oudtshoorn from R250. Yellow, foggy or oxidised headlights sanded, polished & protected. Inside headlight cleaning from R200. WhatsApp 081 087 6539.",
  "h1": "Headlight Restoration in Oudtshoorn",
  "lead": "Yellow, cloudy headlights make any car look older — and they cut your light output at night. RADC restores the lenses to clear for a fraction of the cost of new units.",
  "price_keys": [("Headlight services", "headlights")],
  "body": f'''
<div class="split" style="margin-bottom:28px">
<div>
<h2>Why headlights turn yellow</h2>
<p>Modern headlights are polycarbonate plastic with a factory UV coating. Over time, sun exposure breaks that coating down and the plastic oxidises, turning yellow and hazy. In the Klein Karoo, with hot summers and strong UV, this happens faster than in milder climates.</p>
</div>
<figure class="photo">{picture("oxidised-headlight-before-restoration", (430, 860), "Yellow, oxidised car headlight before restoration at RADC Oudtshoorn", "(max-width:860px) 100vw, 430px", 860, 460)}<figcaption>Typical oxidised lens before restoration.</figcaption></figure>
</div>

<h2>Our headlight restoration process</h2>
<ol class="steps">
  <li><strong>Mask &amp; prep</strong>Surrounding paint and trim is taped off and protected.</li>
  <li><strong>Wet-sand</strong>The damaged, oxidised layer is sanded away through progressively finer grits.</li>
  <li><strong>Polish</strong>The lens is machine-polished back to optical clarity.</li>
  <li><strong>Protect</strong>A protective layer is applied to slow future yellowing.</li>
</ol>

<h2>Headlight repair: haze on the inside</h2>
<p>If the haze or moisture marks are <em>inside</em> the lamp, polishing the outside won't fix it. Our headlight repair service (from R200) cleans the headlights from the inside to remove the film and marks.</p>

<h2>Is it a roadworthy issue?</h2>
<p>Badly oxidised headlights scatter and reduce light, which makes night driving on unlit Karoo roads and mountain passes like the Outeniqua and Swartberg less safe. Clear lenses can also help when you're preparing a car for a roadworthy test or sale.</p>''',
  "faqs": [
    ("How much does headlight restoration cost in Oudtshoorn?", "Headlight restoration at RADC is from R250. Inside headlight cleaning (headlight repair) is from R200."),
    ("How long does headlight restoration last?", "With the protective layer applied and sensible care, results can last well over a year. Parking in shade and regular washing help the lenses stay clear for longer."),
    ("Is restoration cheaper than new headlights?", "In most cases, by a wide margin. Replacement units can cost thousands of rand per side, while restoration starts at R250."),
    ("Can you fix moisture inside the headlight?", "Yes — our headlight repair service cleans the lens from the inside to remove haze and moisture marks."),
  ],
},
"dent-scratch-repair": {
  "title": "Dent & Scratch Repair Oudtshoorn | Rim Repair & Respray | RADC",
  "desc": "Scratch & faded paint removal from R300, minor dent repair, rim repairs from R400, bumper alignment R200 and full resprays in Oudtshoorn. Get a WhatsApp quote today.",
  "h1": "Dent, Scratch &amp; Rim Repair in Oudtshoorn",
  "lead": "Car-park scrapes, faded panels, kerbed rims or a bumper that's popped loose — RADC repairs the small things that make a car look tired, right up to full exterior resprays.",
  "price_keys": [("Repair services", "repairs")],
  "body": '''
<h2>Repairs we handle</h2>
<ul class="checklist">
  <li><strong>Scratch &amp; faded-paint removal (from R300)</strong> — removing light scratches and small dents and reviving faded or chalky panels.</li>
  <li><strong>Minor dent repairs (from R1 600)</strong> — removing small dents with a respray of the affected area.</li>
  <li><strong>Rim repairs (from R400)</strong> — kerb rash and rim restoration to make wheels look right again.</li>
  <li><strong>Bumper alignment (R200)</strong> — re-seating and aligning loose or misaligned bumpers after a bump.</li>
  <li><strong>Full body respray (from R13 500)</strong> — a full exterior respray with materials included.</li>
</ul>

<h2>Get an accurate quote fast</h2>
<p>Every repair is different, so the quickest way to a firm price is to WhatsApp us clear photos:</p>
<ul class="checklist">
  <li>One photo from about 2 m away so we can see the panel.</li>
  <li>One close-up of the damage, ideally in daylight.</li>
  <li>Your vehicle's make, model and colour.</li>
</ul>

<h2>Repair, then protect</h2>
<p>After paintwork, ask about combining your repair with a <a href="/services/paint-correction-polishing/">machine polish</a> so the repaired area blends with the rest of the car, or a <a href="/services/ceramic-coating/">ceramic package</a> to keep it looking new.</p>''',
  "faqs": [
    ("How much does scratch removal cost in Oudtshoorn?", "Scratch and faded-paint removal starts at R300. Deeper scratches that need paintwork are quoted from photos."),
    ("Do you repair rims?", "Yes, rim repairs start at R400 per job depending on the damage."),
    ("How much is a full respray?", "A full exterior respray starts at R13 500 including materials. Colour changes and extensive bodywork are quoted separately."),
    ("Can you fix a loose bumper?", "Yes — bumper alignment is R200 where clips and brackets are intact."),
  ],
},
}

def build_services():
    # hub
    crumbs = [("/", "Home"), ("/services/", "Services")]
    body = page_hero(crumbs, "Services", "Car Detailing Services in Oudtshoorn",
        "Five specialist service areas, each with packages for hatches, sedans, SUVs, bakkies and minibuses. Click a service for what's included, prices and FAQs.")
    body += f'<section class="block"><div class="wrap"><div class="grid g3">{service_cards()}</div></div></section>'
    body += f'''<section class="block alt"><div class="wrap split" style="align-items:start">
<div><h2>Not sure what your car needs?</h2>
<p>Most cars fall into one of three categories:</p>
<ul class="checklist">
<li><strong>"It just needs a good clean"</strong> — a <a href="/services/car-valet-wash/">wash or full valet</a>.</li>
<li><strong>"It's clean but looks dull or swirly"</strong> — <a href="/services/paint-correction-polishing/">paint correction</a>.</li>
<li><strong>"I want it to stay looking new"</strong> — <a href="/services/ceramic-coating/">polish + ceramic coating</a>.</li>
</ul>
<p>Send a few photos on WhatsApp and we'll point you to the right package.</p></div>
{FACTS}</div></section>'''
    body += cta_band()
    render("/services/", "Car Detailing Services Oudtshoorn | Polishing, Ceramic & Valets | RADC",
           "All RADC detailing services in Oudtshoorn: ceramic coating, paint correction, valets & washes, headlight restoration, dent, scratch & rim repair. Prices from R130.",
           body, [{"@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "url": f'{B["site"]}/services/{s["slug"]}/', "name": s["nav"]}
               for i, s in enumerate(SERVICES)]}], crumbs, priority="0.9")

    for s in SERVICES:
        c = SERVICE_CONTENT[s["slug"]]
        path = f'/services/{s["slug"]}/'
        crumbs = [("/", "Home"), ("/services/", "Services"), (path, s["nav"])]
        tables = "".join(f'<div class="price-group"><h3>{t}</h3>{price_table(PRICES[k], t)}</div>' for t, k in c["price_keys"])
        all_rows = [r for _, k in c["price_keys"] for r in PRICES[k]]
        body = page_hero(crumbs, f'From {rand(s["from"])} · Oudtshoorn', c["h1"], c["lead"])
        body += f'''<section class="block"><div class="wrap split" style="align-items:start">
<article>{c["body"]}</article>
<aside>
  <div class="card" style="position:sticky;top:90px">
    <h2 style="font-size:1.6rem">Prices</h2>
    {tables}
    <p class="small muted">Prices from the RADC catalogue. Final quote depends on vehicle size and condition.</p>
    <div class="btn-row">{btn_wa("Get a quote")}{btn_call("Call")}</div>
  </div>
</aside>
</div></section>
<section class="block alt"><div class="wrap">{faq_html(c["faqs"])}</div></section>
<section class="block"><div class="wrap"><div class="section-head"><h2>Related services</h2></div><div class="grid g4">{service_cards(exclude=s["slug"])}</div>
<p style="margin-top:28px" class="muted">Driving in from out of town? See our guides for <a href="/areas/george/">George</a>, <a href="/areas/mossel-bay/">Mossel Bay</a>, <a href="/areas/knysna-plettenberg-bay/">Knysna &amp; Plett</a>, the <a href="/areas/klein-karoo/">Klein Karoo</a> and the <a href="/areas/central-karoo/">Central Karoo</a>.</p></div></section>
{cta_band()}'''
        svc_schema = {"@type": "Service", "@id": B["site"] + path + "#service",
                      "name": strip_tags(html.unescape(c["h1"])), "serviceType": s["nav"],
                      "description": strip_tags(c["lead"]), "provider": {"@id": BIZ_ID},
                      "areaServed": area_served(), "url": B["site"] + path,
                      "hasOfferCatalog": offer_catalog(s["nav"] + " packages", all_rows),
                      "offers": {"@type": "AggregateOffer", "priceCurrency": "ZAR",
                                 "lowPrice": f"{min(r[2] for r in all_rows):.2f}",
                                 "highPrice": f"{max(r[2] for r in all_rows):.2f}",
                                 "offerCount": len(all_rows)}}
        render(path, c["title"], c["desc"], body, [svc_schema, faq_schema(c["faqs"])], crumbs, priority="0.9")

# ---------------------------------------------------------------------------
# PRICES
# ---------------------------------------------------------------------------
def build_prices():
    path = "/prices/"
    crumbs = [("/", "Home"), (path, "Prices")]
    groups = [
        ("Washes &amp; add-ons", "washes", "/services/car-valet-wash/"),
        ("Full valets", "valets", "/services/car-valet-wash/"),
        ("Machine polishing &amp; paint correction", "polish", "/services/paint-correction-polishing/"),
        ("Polish + 12-month-plus ceramic", "ceramic12", "/services/ceramic-coating/"),
        ("Polish + 5-year ceramic", "ceramic5", "/services/ceramic-coating/"),
        ("Headlights", "headlights", "/services/headlight-restoration/"),
        ("Repairs &amp; paintwork", "repairs", "/services/dent-scratch-repair/"),
    ]
    tables = "".join(f'<div class="price-group"><h2 style="font-size:1.7rem">{t}</h2>{price_table(PRICES[k], strip_tags(t))}<p class="small" style="margin-top:8px"><a href="{u}">What\'s included →</a></p></div>' for t, k, u in groups)
    body = page_hero(crumbs, "Price list", "Car Detailing Prices in Oudtshoorn",
        "Every RADC package with upfront starting prices — for hatches, sedans, SUVs, double-cab bakkies and minibuses.")
    body += f'''<section class="block"><div class="wrap split" style="align-items:start">
<div>{tables}
<p class="muted small">Prices in South African rand (ZAR) as listed in the RADC WhatsApp catalogue, last updated {date.today().strftime("%B %Y")}. Prices are starting prices; vehicles in very poor condition, oversized vehicles or special requests are quoted individually.</p></div>
<aside><div class="card" style="position:sticky;top:90px"><h2 style="font-size:1.6rem">Get an exact quote</h2>
<p>WhatsApp your make, model and two or three photos. We'll confirm the right package and price, usually the same day.</p>
<div class="btn-row">{btn_wa("WhatsApp for a quote")}{btn_call("Call")}</div>
<hr style="border-color:var(--line);margin:24px 0">
<h3>Popular picks</h3>
<ul class="checklist small">
<li>Regular upkeep: <strong>Wash &amp; vacuum – R130</strong></li>
<li>Selling your car: <strong>Full valet – R1 000</strong></li>
<li>Dull paint: <strong>2-Step polish – R1 300</strong></li>
<li>Best value protection: <strong>2-Step + 12-month-plus ceramic – R1 799.99</strong></li>
<li>Yellow lights: <strong>Headlight restoration – R250</strong></li>
</ul></div></aside>
</div></section>{cta_band()}'''
    all_rows = [r for _, k, _ in groups for r in PRICES[k]]
    render(path, "Car Detailing Prices Oudtshoorn 2026 | Full RADC Price List",
           "Full RADC price list: wash & vacuum R130, full valet R1 000, polishing from R1 000, ceramic coating packages from R1 299.99, headlight restoration R250 & more.",
           body, [offer_catalog("RADC car detailing price list", all_rows) | {"provider": {"@id": BIZ_ID}}], crumbs, priority="0.9")

# ---------------------------------------------------------------------------
# AREAS
# ---------------------------------------------------------------------------
AREA_CONTENT = {
"george": {
  "title": "Car Detailing near George | Ceramic Coating & Polishing | RADC",
  "desc": "Detailing for George, Wilderness & Blanco drivers at RADC Oudtshoorn — ceramic coating, paint correction, valets & headlight restoration. ~55 km over the Outeniqua Pass.",
  "intro": "George is the Garden Route's biggest town, and plenty of George drivers make the scenic trip over the Outeniqua Pass to have their cars detailed at RADC in Oudtshoorn.",
  "local": "George's frequent rain and humidity mean water spots and road film build up quickly, while the N2 and N12 throw up tar and grime. Cars that commute daily on the N2 also pick up stone-chip and swirl damage from regular washing. A <a href=\"/services/paint-correction-polishing/\">machine polish</a> followed by a <a href=\"/services/ceramic-coating/\">ceramic coating</a> makes wet-weather washing far easier — water beads and sheets off instead of drying into spots.",
  "plan": "Leave George on the N12 and enjoy the Outeniqua Pass — you'll be in Oudtshoorn in under an hour. Drop your car off in the morning and, if you have a lift, spend the day in town: the Cango Caves, ostrich farms and Baron van Reede Street's restaurants are all close by.",
  "recommend": ["2-Step polish + 12-month-plus ceramic", "Full valet before selling", "Headlight restoration for N2 night commutes"],
  "faq": [("How far is RADC from George?", "RADC in Oudtshoorn is about 55 km from George via the N12 and Outeniqua Pass — roughly 50 to 60 minutes' drive."),
          ("Why drive from George to Oudtshoorn for detailing?", "For once-off, high-value services like paint correction and ceramic coating, a single trip gives months to years of protection, with clear, published prices.")],
},
"mossel-bay": {
  "title": "Car Detailing near Mossel Bay | Ceramic & Polishing | RADC",
  "desc": "Mossel Bay, Hartenbos & Great Brak drivers: protect your paint from salt air with ceramic coating, polishing & valets at RADC Oudtshoorn — about 1 hour via Robinson Pass.",
  "intro": "Mossel Bay sits right on the ocean — wonderful for weekends, tough on paint. RADC helps Mossel Bay, Hartenbos and Great Brak River drivers fight salt and sun damage.",
  "local": "Salt-laden sea air settles on paint, chrome and rims, and once it bonds it accelerates oxidation and corrosion. Combine that with the reflected glare of beach days and paint dulls fast. A <a href=\"/services/car-valet-wash/\">decon wash and clay bar</a> removes bonded salt and fallout, and a <a href=\"/services/ceramic-coating/\">ceramic coating</a> stops it bonding again so a simple rinse keeps the car clean.",
  "plan": "Take the R328 over the Robinson Pass — about an hour of scenic driving to Oudtshoorn. It's an easy round trip for a drop-off and collection on the same day.",
  "recommend": ["Decon wash & clay bar (R217)", "1-Step or 2-Step polish + 5-year ceramic", "Rim repairs for kerb rash"],
  "faq": [("How far is RADC from Mossel Bay?", "About 85 km via the R328 Robinson Pass — roughly an hour's drive."),
          ("Does ceramic coating help with sea air?", "Yes. A coating creates a slick barrier that keeps salt and fallout from bonding to the clear coat, making it much easier to wash off. Regular rinsing is still important.")],
},
"knysna-plettenberg-bay": {
  "title": "Car Detailing for Knysna & Plettenberg Bay | RADC Oudtshoorn",
  "desc": "Knysna, Sedgefield & Plett drivers: book a ceramic coating, paint correction or full valet at RADC in Oudtshoorn. Worth the drive for long-lasting protection.",
  "intro": "From Knysna and Sedgefield to Plettenberg Bay, coastal Garden Route cars deal with salt air, forest sap and lots of holiday kilometres. RADC's Oudtshoorn centre is a worthwhile day trip for serious paint care.",
  "local": "Tree sap and bird droppings under the Knysna forests can etch clear coat within days in the sun, and coastal humidity keeps grime on the paint. Holiday-season traffic, gravel roads to the beaches and trailer towing all take their toll. Book a <a href=\"/services/paint-correction-polishing/\">2- or 3-step polish</a> to remove etching, then a <a href=\"/services/ceramic-coating/\">5-year ceramic coating</a> so the next season's contamination washes off.",
  "plan": "From Knysna take the N2 to George and the N12 over the Outeniqua Pass (about 1 h 45). From Plett, allow about 2 hours. Combine your drop-off with a Klein Karoo day out — or ask us on WhatsApp about the best timing for out-of-town bookings.",
  "recommend": ["3-Step polish + 5-year ceramic", "Full valet SUV / double cab after the holidays", "Headlight restoration"],
  "faq": [("How long is the drive from Knysna or Plett to RADC?", "Roughly 1 h 45 from Knysna and about 2 hours from Plettenberg Bay via George and the Outeniqua Pass."),
          ("Can I get a quote before driving through?", f"Yes — WhatsApp photos of your vehicle to {B['phone_display']} and we'll quote before you book, so there are no surprises.")],
},
"klein-karoo": {
  "title": "Car Detailing Klein Karoo | De Rust, Calitzdorp, Ladismith | RADC",
  "desc": "Car detailing for the Klein Karoo: De Rust, Dysselsdorp, Calitzdorp, Ladismith & Uniondale. Ceramic coating, polishing, valets & headlight restoration at RADC Oudtshoorn.",
  "intro": "Oudtshoorn is the hub of the Klein Karoo, which makes RADC the closest specialist detailer for De Rust, Dysselsdorp, Calitzdorp, Ladismith, Uniondale and the farms in between.",
  "local": "Klein Karoo vehicles work hard: gravel farm roads, fine red dust, summer heat over 35 °C and intense UV. The result is faded paint, chalky plastics, yellow headlights and dust-packed interiors. A <a href=\"/services/car-valet-wash/\">full valet</a> takes care of the dust; a <a href=\"/services/headlight-restoration/\">headlight restoration</a> restores night visibility on dark country roads; and a <a href=\"/services/ceramic-coating/\">ceramic package</a> protects the paint from the sun.",
  "plan": "Dysselsdorp is about 20 minutes away, De Rust about 30 minutes on the N12, Calitzdorp about 40 minutes on the R62, and Ladismith and Uniondale a little over an hour. Combine your drop-off with shopping or appointments in Oudtshoorn.",
  "recommend": ["Full valet SUV / double cab – R1 399", "SUV 1-Step polish + 12-month-plus ceramic – R2 000", "Engine bay detailing – R150"],
  "faq": [("Do you detail farm bakkies?", "Yes. Our SUV and double-cab packages are priced for bakkies, and an engine-bay detail is a popular add-on for vehicles used on gravel roads."),
          ("Which towns in the Klein Karoo do you serve?", "Customers come from Oudtshoorn, Bongolethu, De Rust, Dysselsdorp, Calitzdorp, Ladismith, Van Wyksdorp, Uniondale and surrounding farms.")],
},
"central-karoo": {
  "title": "Car Detailing Central Karoo | Prince Albert & Beaufort West | RADC",
  "desc": "Prince Albert, Beaufort West & Laingsburg drivers: ceramic coating, paint correction, valets & headlight restoration at RADC Oudtshoorn — via Meiringspoort or Swartberg Pass.",
  "intro": "There are few specialist detailers in the Central Karoo, so drivers from Prince Albert, Beaufort West and Laingsburg often make the trip south to RADC in Oudtshoorn.",
  "local": "The Central Karoo has some of the harshest conditions in the country for paint: extreme summer heat, very high UV, long N1 and N12 kilometres and dusty gravel roads. Long-haul vehicles pick up bug splatter and tar that bake onto the paint. A <a href=\"/services/car-valet-wash/\">decon wash and clay bar</a>, followed by <a href=\"/services/paint-correction-polishing/\">polishing</a> and a <a href=\"/services/ceramic-coating/\">5-year ceramic coating</a>, is the most cost-effective way to keep a Karoo vehicle looking good for years.",
  "plan": "From Prince Albert, drive through spectacular Meiringspoort on the N12 (tar) or over the Swartberg Pass (gravel — not ideal right before a detail!). From Beaufort West, the N12 south via Klaarstroom and Meiringspoort takes around 2 h 30 – 2 h 45. Book ahead on WhatsApp so your car can be done in one visit.",
  "recommend": ["Decon wash & clay bar", "SUV 1-Step polish + 5-year ceramic – R5 500", "Headlight restoration for long night drives"],
  "faq": [("How far is RADC from Prince Albert?", "About 75 km via the Swartberg Pass (gravel) or around 120 km via Meiringspoort on the tarred N12."),
          ("Is it worth driving from Beaufort West?", "For one-day, long-lasting services like polishing and ceramic coating, yes — the protection lasts long after the trip. WhatsApp us first to confirm a date.")],
},
}

def build_areas():
    crumbs = [("/", "Home"), ("/areas/", "Areas we serve")]
    cards = "".join(f'''<a class="card" href="/areas/{a["slug"]}/"><div class="icon">{ICONS["pin"]}</div><h3>{a["name"][0].upper() + a["name"][1:]}</h3>
<p class="muted">{", ".join(a["places"])}</p><p class="small">{a["dist"]} · {a["time"]}</p><span class="more">Plan your visit →</span></a>''' for a in AREAS)
    body = page_hero(crumbs, "Areas we serve", "Car Detailing across the Garden Route &amp; Karoo",
        "RADC is based in Oudtshoorn — perfectly placed between the Garden Route coast, the Klein Karoo and the Central Karoo.")
    body += f'''<section class="block"><div class="wrap">
<div class="grid g3"><a class="card" href="/" style="border-color:#1d3b6b"><div class="icon">{ICONS["pin"]}</div><h3>Oudtshoorn</h3><p class="muted">Oudtshoorn, Bongolethu, Colridge View, Toekomsrus, Bridgton, West Bank</p><p class="small">Our home base</p><span class="more">Home page →</span></a>{cards}</div>
</div></section>
<section class="block alt"><div class="wrap split" style="align-items:start"><div>
<h2>Why Oudtshoorn is the ideal hub</h2>
<p>Oudtshoorn lies in the Garden Route District (previously the Eden District Municipality) at the heart of the Klein Karoo. Three mountain passes — Outeniqua, Robinson and Meiringspoort/Swartberg — link it to George, Mossel Bay and the Central Karoo, so most of the region is within an easy drive.</p>
<p>Because services like <a href="/services/paint-correction-polishing/">paint correction</a> and <a href="/services/ceramic-coating/">ceramic coating</a> are long-lasting investments, one trip to RADC gives you months or years of results.</p></div>
{FACTS}</div></section>{cta_band()}'''
    render("/areas/", "Areas We Serve | Car Detailing Garden Route & Karoo | RADC",
           "RADC in Oudtshoorn serves George, Mossel Bay, Knysna, Plett, De Rust, Calitzdorp, Ladismith, Prince Albert, Beaufort West and the wider Garden Route & Karoo.",
           body, None, crumbs, priority="0.8")

    for a in AREAS:
        c = AREA_CONTENT[a["slug"]]
        path = f'/areas/{a["slug"]}/'
        disp = a["name"][0].upper() + a["name"][1:]
        crumbs = [("/", "Home"), ("/areas/", "Areas we serve"), (path, disp)]
        h1 = f'Car Detailing for {a["name"].replace("the ", "")} Drivers'
        body = page_hero(crumbs, f'{a["region"]} · {a["dist"]} from Oudtshoorn', h1, c["intro"])
        rec = "".join(f"<li>{esc(r)}</li>" for r in c["recommend"])
        places = "".join(f"<li>{esc(p)}</li>" for p in a["places"])
        body += f'''<section class="block"><div class="wrap split" style="align-items:start">
<article>
<h2>Paint care challenges in {a["name"].replace("the ", "the ")}</h2>
<p>{c["local"]}</p>
<h2>Planning your trip to RADC</h2>
<p>{c["plan"]}</p>
<div class="facts" style="margin:22px 0"><dl>
<dt>Distance</dt><dd>{a["dist"]} to Oudtshoorn</dd>
<dt>Drive time</dt><dd>{a["time"]}</dd>
<dt>Route</dt><dd>{a["route"]}</dd>
<dt>Our address</dt><dd>{B["street"]}, {B["suburb"]}, {B["city"]} {B["postcode"]}</dd>
</dl></div>
<p>Please WhatsApp us before you travel so we can confirm your quote and booking date — and ask whether any mobile or collection options are available for your area.</p>
<h2>Popular with {a["name"].replace("the ", "")} customers</h2>
<ul class="checklist">{rec}</ul>
<p>See the <a href="/prices/">full price list</a> for every package.</p>
</article>
<aside><div class="card" style="position:sticky;top:90px"><h2 style="font-size:1.5rem">Towns covered</h2><ul class="area-list" style="columns:1">{places}</ul>
<div class="btn-row">{btn_wa("WhatsApp for a quote")}<a class="btn btn-ghost" href="{B["maps"]}" target="_blank" rel="noopener">{ICONS["pin"]}Directions</a></div></div></aside>
</div></section>
<section class="block alt"><div class="wrap"><div class="section-head"><h2>Our services</h2></div><div class="grid g3">{service_cards()}</div></div></section>
<section class="block"><div class="wrap">{faq_html(c["faq"])}</div></section>
{cta_band(f"Driving in from {a['name'].replace('the ', '')}?")}'''
        extra = [faq_schema(c["faq"]),
                 {"@type": "Service", "name": f"Car detailing for {a['name'].replace('the ', '')}",
                  "serviceType": "Car detailing", "provider": {"@id": BIZ_ID},
                  "areaServed": [{"@type": "City", "name": p} for p in a["places"]]}]
        render(path, c["title"], c["desc"], body, extra, crumbs, priority="0.7")

# ---------------------------------------------------------------------------
# ABOUT / CONTACT / 404
# ---------------------------------------------------------------------------
def build_about():
    path = "/about/"
    crumbs = [("/", "Home"), (path, "About")]
    body = page_hero(crumbs, "About RADC", "About Ryall's Auto Detailing Centre",
        "A local, owner-run detailing centre in Colridge View, Oudtshoorn — built on passion for cars, honest pricing and the support of our community.", ctas=False)
    body += f'''<section class="block"><div class="wrap split">
<div>
<h2>Cleaner. Shinier. Protected.</h2>
<p>Ryall's Auto Detailing Centre — RADC for short — was started by Oudtshoorn local Ryall Wagenaar out of a genuine love for cars and for making them look their best. You can see that passion in the Bordeaux Honda Civic that features across our social media.</p>
<p>We're a premium vehicle detailing service that specialises in restoring showroom shine. From minor scratch removal to complete paint restoration, we use proper machine-polishing techniques and equipment to bring out the best in your vehicle's paintwork. We don't just wash cars — we meticulously detail and polish every surface to reveal a deeper, richer gloss.</p>
<h2>What we stand for</h2>
<ul class="checklist">
<li><strong>Your support matters</strong> — RADC has grown thanks to the loyalty and word-of-mouth of local customers.</li>
<li><strong>Clean cars, happier people</strong> — we treat every vehicle as if it were our own.</li>
<li><strong>Honest, upfront pricing</strong> — every package is <a href="/prices/">published</a>.</li>
<li><strong>From our family to yours</strong> — a local business serving local families, with faith at its core: “Everything through Christ our Lord.” (Philippians 4:13)</li>
</ul>
<div class="btn-row">{btn_wa("Say hi on WhatsApp")}<a class="btn btn-ghost" href="{B["tiktok"]}" target="_blank" rel="noopener">Follow on TikTok</a></div>
</div>
<figure class="photo">{picture("honda-civic-headlight-detail-oudtshoorn", (480, 800, 1080), "Detailed Bordeaux Honda Civic, the RADC signature car", "(max-width:860px) 100vw, 480px", 1080, 1620)}<figcaption>The RADC signature Civic.</figcaption></figure>
</div></section>
<section class="block alt"><div class="wrap split" style="align-items:start">
<div><h2>What our customers say</h2>
<p>RADC holds a <strong>{B["rating"]}-star rating on Google from {B["reviews"]} reviews</strong>. Reviewers mention <em>spotless interiors</em>, <em>friendly staff</em> and long-lasting results.</p>
<a class="btn btn-ghost" href="{B["maps"]}" target="_blank" rel="noopener">{ICONS["star"]}Read our Google reviews</a></div>
{FACTS}</div></section>{cta_band()}'''
    person = {"@type": "Person", "name": "Ryall Wagenaar", "jobTitle": "Owner & detailer",
              "worksFor": {"@id": BIZ_ID}, "sameAs": [B["tiktok"]]}
    render(path, "About RADC | Ryall's Auto Detailing Centre, Oudtshoorn",
           "Meet Ryall's Auto Detailing Centre (RADC): a local, owner-run car detailing business in Colridge View, Oudtshoorn. Cleaner, shinier, protected.",
           body, [person, {"@type": "AboutPage", "url": B["site"] + path}], crumbs, priority="0.6")

def build_contact():
    path = "/contact/"
    crumbs = [("/", "Home"), (path, "Contact")]
    options = "".join(f"<option>{esc(s['nav'])}</option>" for s in SERVICES)
    body = page_hero(crumbs, "Contact &amp; bookings", "Book Car Detailing in Oudtshoorn",
        f"WhatsApp is the fastest way to reach us. Send a few photos of your vehicle and we'll reply with a quote and the next available date.", ctas=False)
    body += f'''<section class="block"><div class="wrap split" style="align-items:start">
<div class="card">
<h2 style="font-size:1.7rem">Request a quote</h2>
<p class="muted small">This form opens WhatsApp with your details filled in — just hit send and attach photos.</p>
<form id="booking-form" class="form" data-wa="{B["wa"]}">
  <div class="row"><div><label for="bf-name">Your name</label><input id="bf-name" autocomplete="name" required></div>
  <div><label for="bf-vehicle">Vehicle (make &amp; model)</label><input id="bf-vehicle" placeholder="e.g. VW Polo, Toyota Hilux" required></div></div>
  <div class="row"><div><label for="bf-service">Service</label><select id="bf-service"><option value="">Not sure – please advise</option>{options}<option>Full valet</option><option>Wash &amp; vacuum</option></select></div>
  <div><label for="bf-town">Your town</label><input id="bf-town" placeholder="e.g. Oudtshoorn, George"></div></div>
  <div><label for="bf-date">Preferred date</label><input id="bf-date" type="date"></div>
  <div><label for="bf-msg">Anything else?</label><textarea id="bf-msg" rows="3" placeholder="Condition, scratches, colour, etc."></textarea></div>
  <button class="btn btn-wa" type="submit">{ICONS["wa"]}Send via WhatsApp</button>
</form>
</div>
<div>
<div class="facts"><h2 style="font-size:1.5rem">Contact details</h2><dl>
<dt>Phone</dt><dd><a href="tel:{B["phone_e164"]}">{B["phone_display"]}</a></dd>
<dt>WhatsApp</dt><dd><a href="{WA_LINK}" target="_blank" rel="noopener">{B["phone_display"]}</a></dd>
<dt>Email</dt><dd><a href="mailto:{B["email"]}">{B["email"]}</a></dd>
<dt>Address</dt><dd>{B["street"]}, {B["suburb"]}<br>{B["city"]}, {B["postcode"]}, {B["region"]}</dd>
<dt>Hours</dt><dd>{B["hours_text"]}</dd>
</dl></div>
<p style="margin-top:18px">We're on Heunis Street just south of 5th Avenue (R62) and near the Toekomsrus Community Centre.</p>
<iframe class="map" title="Map to Ryall's Auto Detailing Centre, 27 Heunis St, Oudtshoorn" src="{B["maps_embed"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
<div class="btn-row"><a class="btn btn-primary" href="{B["maps"]}" target="_blank" rel="noopener">{ICONS["pin"]}Get directions</a>{btn_call()}</div>
</div>
</div></section>'''
    render(path, "Contact RADC | Book Car Detailing in Oudtshoorn | 081 087 6539",
           "Book with Ryall's Auto Detailing Centre: 27 Heunis St, Colridge View, Oudtshoorn. Call or WhatsApp 081 087 6539 for a quote. Directions & map.",
           body, [{"@type": "ContactPage", "url": B["site"] + path}], crumbs, priority="0.8")

def build_404():
    body = f'''<section class="page-hero"><div class="wrap" style="padding:90px 20px">
<span class="eyebrow">Error 404</span><h1>This page took a wrong turn</h1>
<p class="lead">The page you're looking for doesn't exist. Try one of these instead:</p>
<div class="btn-row"><a class="btn btn-primary" href="/">Home</a><a class="btn btn-ghost" href="/services/">Services</a><a class="btn btn-ghost" href="/prices/">Prices</a>{btn_wa()}</div>
</div></section>'''
    render("/404.html", "Page not found | RADC Oudtshoorn", "Page not found.", body, noindex=True)

# ---------------------------------------------------------------------------
# Supporting files
# ---------------------------------------------------------------------------
def write(name, content):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(content)

def build_support():
    urls = "".join(f"  <url><loc>{B['site']}{p}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for p, pr in PAGES)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /tools/\n\n# AI search & answer engines are welcome\nUser-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {B['site']}/sitemap.xml\n")
    price_lines = "\n".join(f"- {n}: from {rand(p)}" for k in PRICES for n, _, p in PRICES[k])
    svc_lines = "\n".join(f"- [{s['nav']}]({B['site']}/services/{s['slug']}/): {s['teaser']}" for s in SERVICES)
    area_lines = "\n".join(f"- [{a['name'][0].upper() + a['name'][1:]}]({B['site']}/areas/{a['slug']}/): {', '.join(a['places'])} ({a['dist']} from Oudtshoorn)" for a in AREAS)
    write("llms.txt", f"""# {B['name']} (RADC)

> Car detailing centre in Oudtshoorn, Western Cape, South Africa. Ceramic coating, 1- to 3-step paint correction, full valets, washes, headlight restoration, dent, scratch and rim repair and resprays. Serves Oudtshoorn, the Klein Karoo, the Garden Route (George, Mossel Bay, Knysna, Plettenberg Bay) and the Central Karoo (Prince Albert, Beaufort West).

## Key facts
- Name: {B['name']} (RADC)
- Slogan: Cleaner | Shinier | Protected
- Address: {B['street']}, {B['suburb']}, {B['city']}, {B['postcode']}, {B['region']}, South Africa
- Phone & WhatsApp: {B['phone_display']} ({B['phone_e164']})
- Email: {B['email']}
- Owner: Ryall Wagenaar
- Google rating: {B['rating']} stars ({B['reviews']} reviews)
- Bookings: via WhatsApp

## Services
{svc_lines}

## Prices (ZAR, starting prices)
{price_lines}

## Areas served
- [Oudtshoorn]({B['site']}/): home base
{area_lines}

## Pages
- [Full price list]({B['site']}/prices/)
- [About]({B['site']}/about/)
- [Contact & directions]({B['site']}/contact/)
""")
    write("site.webmanifest", json.dumps({
        "name": B["name"], "short_name": "RADC", "start_url": "/", "display": "standalone",
        "background_color": "#06080d", "theme_color": "#06080d",
        "icons": [{"src": "/assets/img/radc-logo-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/radc-logo-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))

if __name__ == "__main__":
    build_home(); build_services(); build_prices(); build_areas(); build_about(); build_contact(); build_404()
    build_support()
    print(f"Built {len(PAGES)} indexable pages into {ROOT}")
