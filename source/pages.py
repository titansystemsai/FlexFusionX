"""Policy pages (privacy.html, terms.html) in the site's style.

Text mirrors the reviewed drafts in the Claude Doc "FlexFusionX Privacy Policy & Terms".
Anything still to confirm is written as [[...]] and renders as a dashed TBC chip.
Called from build.py.
"""
import os
import re

PRIVACY = r"""
<p class="meta">Last updated: 16 October 2026</p>

<h2>1. Who we are</h2>
<p>FlexFusionX (ABN 81 239 476 840) is a physiotherapy practice run by Cyriac Kallarakkal, an AHPRA-registered physiotherapist (PHY0004039512). We see clients at 101 Portrush Rd, Evandale SA 5069, which is inside Balance Physiotherapy, as well as at home, at your gym or training ground, and online. Balance Physiotherapy is a separate business, and we do not share your records with them unless you agree.</p>
<p>This policy explains how we handle your personal information, including health information, under the Privacy Act 1988 (Cth) and the Australian Privacy Principles. Health providers must follow these rules whatever their size.</p>

<h2>2. What we collect</h2>
<ul>
<li><b>Contact details:</b> your name, date of birth, address, phone, email and emergency contact.</li>
<li><b>Health information:</b> your medical history, symptoms, injuries, training and activity, assessment findings, treatment notes, exercise programs, goals, and any imaging or reports you share.</li>
<li><b>Funding details:</b> Medicare, private health fund, DVA, WorkCover or CTP claim details, and for NDIS participants your NDIS number, plan management type, and plan manager or support coordinator details.</li>
<li><b>Payment details:</b> what you paid and how. Card details are handled by our payment provider, and we don't store full card numbers.</li>
<li><b>Enquiries:</b> what you tell us when you call, email or message us.</li>
<li><b>Website usage:</b> basic, non-identifying data about how the site is used.</li>
</ul>

<h2>3. How we collect it</h2>
<p>Mostly from you: through our online booking and intake forms, in sessions, and by phone, email, SMS or video call. With your consent, or where the law allows, we may also receive information from your GP or specialist, other health providers, your insurer or claims manager, your NDIS support coordinator, plan manager or guardian, or a coach you ask us to work with.</p>
<p>You can make a general enquiry without giving your name. To assess or treat you, we need to know who you are.</p>

<h2>4. Why we use it</h2>
<ul>
<li>To assess, treat and plan your care, including programs between sessions.</li>
<li>To contact you about appointments, including reminders by SMS or email.</li>
<li>To issue invoices and process claims with Medicare, health funds, DVA, WorkCover, CTP insurers or the NDIS.</li>
<li>To write reports you or your funding body need, such as NDIS progress reports.</li>
<li>To meet our legal and professional obligations, including AHPRA and insurance requirements.</li>
<li>To send occasional updates or offers, only if you've agreed. You can opt out at any time.</li>
</ul>
<p>We do not sell your information.</p>

<h2>5. Who we share it with</h2>
<p>We share only what is needed, and with your consent unless the law allows otherwise:</p>
<ul>
<li>Your GP, specialist or other health providers involved in your care.</li>
<li>Medicare, your health fund, DVA, WorkCover or CTP insurers, to process claims you make.</li>
<li>For NDIS participants: the NDIA, your plan manager and your support coordinator.</li>
<li>Family members, carers, guardians or support workers you nominate.</li>
<li>A coach or trainer, only if you ask us to.</li>
<li>Service providers who help us run the practice: our practice software (Cliniko, which also runs our online bookings, SMS reminders and telehealth video), email (Google Workspace) and website hosting (Cloudflare). They may only use your information to provide their service to us.</li>
<li>Anyone we are legally required to tell, or where needed to lessen a serious threat to someone's life, health or safety.</li>
</ul>

<h2>6. Overseas disclosure</h2>
<p>Our patient records are stored with Cliniko on servers in Australia. Some of our service providers, including parts of Cliniko's, Google's and our website host's services, may process limited information in other countries, mainly the United States. We use providers with strong security and privacy commitments.</p>

<h2>7. How we keep it safe</h2>
<p>Records are kept in Cliniko, a secure, encrypted practice management system. Only Cyriac can access clinical records, and accounts are protected by strong, unique passwords. We don't keep paper records. If we receive any, we scan and securely destroy them. Telehealth sessions use a secure video service and are not recorded without your consent.</p>

<h2>8. How long we keep it</h2>
<p>We keep health records for at least 7 years after your last appointment. If you were under 18 at your last appointment, we keep them until you turn 25. After that, we securely delete or de-identify them. Enquiries that don't lead to an appointment are deleted after 12 months.</p>

<h2>9. Accessing and correcting your information</h2>
<p>You can ask for a copy of your records, or ask us to correct anything that's wrong, by emailing <a href="mailto:ck@flexfusionx.com.au">ck@flexfusionx.com.au</a> or calling <a href="tel:+61449969060">0449 969 060</a>. We will respond within 30 days. There's no charge to make a request, though we may charge a reasonable fee for copying large records, and we will tell you first. If we can't give you access, for example where the law allows us to refuse, we will tell you why in writing.</p>

<h2>10. Our website</h2>
<ul>
<li><b>Enquiries:</b> the site has no contact form. If you call or email us, we use what you tell us only to reply and arrange your care.</li>
<li><b>Online booking:</b> bookings and intake forms are run by Cliniko and covered by this policy and <a href="https://www.cliniko.com/policies/privacy/" target="_blank" rel="noopener">Cliniko's privacy policy</a>.</li>
<li><b>Cookies and analytics:</b> this site doesn't use analytics or advertising cookies. The booking widget is provided by Cliniko and the fonts by Google Fonts, which receive basic technical information such as your IP address.</li>
<li><b>Links:</b> our site links to other sites, such as Instagram and Google Maps, which have their own privacy policies.</li>
</ul>

<h2>11. Automated decisions</h2>
<p>We don't use automated decision-making. Every decision about your care is made by your physiotherapist.</p>

<h2>12. Data breaches</h2>
<p>If a data breach is likely to cause you serious harm, we will tell you and the Office of the Australian Information Commissioner (OAIC), as the Notifiable Data Breaches scheme requires, and explain what you can do.</p>

<h2>13. Complaints</h2>
<p>If you're unhappy with how we've handled your information, please contact us first at <a href="mailto:ck@flexfusionx.com.au">ck@flexfusionx.com.au</a> or <a href="tel:+61449969060">0449 969 060</a>. We will respond within 30 days. If you're not satisfied, you can contact:</p>
<ul>
<li><b>Office of the Australian Information Commissioner:</b> <a href="https://www.oaic.gov.au" target="_blank" rel="noopener">oaic.gov.au</a>, 1300 363 992 (privacy complaints).</li>
<li><b>Health and Community Services Complaints Commissioner (SA):</b> <a href="https://www.hcscc.sa.gov.au" target="_blank" rel="noopener">hcscc.sa.gov.au</a>, 1800 232 007 (complaints about health services).</li>
<li><b>NDIS Quality and Safeguards Commission:</b> <a href="https://www.ndiscommission.gov.au" target="_blank" rel="noopener">ndiscommission.gov.au</a>, 1800 035 544 (NDIS participants).</li>
</ul>

<h2>14. Changes to this policy</h2>
<p>We may update this policy. The current version is always at flexfusionx.com.au/privacy, with the date it was last updated.</p>

<h2>15. Contact</h2>
<p>FlexFusionX · Cyriac Kallarakkal · 101 Portrush Rd, Evandale SA 5069 · <a href="mailto:ck@flexfusionx.com.au">ck@flexfusionx.com.au</a> · <a href="tel:+61449969060">0449 969 060</a></p>
"""

TERMS = r"""
<p class="meta">Last updated: 16 October 2026</p>
<p>These terms apply when you book or receive services from FlexFusionX (ABN 81 239 476 840) or use flexfusionx.com.au. By booking, you agree to them. Nothing here limits your rights under the Australian Consumer Law.</p>

<h2>1. Our services</h2>
<p>FlexFusionX provides physiotherapy assessment, treatment and rehabilitation through Cyriac Kallarakkal, an AHPRA-registered physiotherapist (PHY0004039512). Sessions run at our Evandale clinic (inside Balance Physiotherapy), at your home, gym or training ground, or online.</p>
<p>We are not an emergency service. In an emergency, call 000.</p>

<h2>2. Booking</h2>
<ul>
<li>Book online, by phone on <a href="tel:+61449969060">0449 969 060</a>, or by email at <a href="mailto:ck@flexfusionx.com.au">ck@flexfusionx.com.au</a>.</li>
<li>You don't need a referral. You do need one to claim through Medicare (a GP chronic condition management plan), DVA, WorkCover or CTP. Please bring or send it before your first session.</li>
<li>Please complete the online intake form before your first appointment. It means more of your session goes on assessment and treatment.</li>
<li>Please give us accurate details, and tell us about any change in your health.</li>
</ul>

<h2>3. Fees and payment</h2>
<ul>
<li>We'll tell you the fee for your appointment before your visit, or any time you ask. We'll give you notice before any price change applies to you.</li>
<li>Payment is due within 14 days of your invoice, by bank transfer (EFT).</li>
<li>If you claim from a private health fund, Medicare or DVA, you pay any gap between our fee and your rebate.</li>
<li><b>WorkCover and CTP:</b> we'll bill your insurer once your claim is accepted. If it's declined, or a service isn't approved, you're responsible for the fee.</li>
<li><b>NDIS:</b> we'll agree the supports, prices and invoicing arrangements with you in a written service agreement, and charge no more than the NDIS price limits.</li>
<li><b>Home visits</b> include a call-out fee based on drive time, added to the session fee. We'll confirm it before your visit.</li>
</ul>

<h2>4. Cancellations and late arrivals</h2>
<p>When you book, that time is held just for you. If you can't make it, please give at least <b>24 hours' notice</b> so someone else can use the time. We don't charge cancellation or missed-appointment fees.</p>
<ul>
<li><b>Running late?</b> Let us know. Your session will still finish on time so the next client isn't kept waiting.</li>
<li><b>NDIS participants:</b> cancellation arrangements are set out in your service agreement, in line with the NDIS Pricing Arrangements in force at the time.</li>
<li>If we need to cancel or reschedule, we'll tell you as early as possible.</li>
<li>If missed appointments become frequent, we may introduce a fee. We'll update these terms first, and any change applies only to bookings made after it.</li>
</ul>
<p>To cancel or reschedule, use the link in your confirmation, call <a href="tel:+61449969060">0449 969 060</a>, or email <a href="mailto:ck@flexfusionx.com.au">ck@flexfusionx.com.au</a>.</p>

<h2>5. Home and mobile visits</h2>
<p>We visit homes, gyms and training grounds across metro Adelaide and the eastern suburbs. Please make sure there is safe access and enough space to move, and that pets are secured. For clients under 18, a parent or guardian must be present. We may end or reschedule a visit if the environment isn't safe.</p>

<h2>6. Online sessions</h2>
<p>Online sessions suit many assessments, reviews and programs, but not every condition. We may recommend an in-person visit. Please join from a private, well-lit space with a stable connection. Sessions are not recorded without your consent.</p>

<h2>7. Your care</h2>
<ul>
<li>Before any treatment, we'll explain what we recommend and why, and ask for your consent. You can decline or stop any treatment at any time.</li>
<li>Exercise programs are written for you. Follow them as advised, and tell us if anything gets worse.</li>
<li>Results differ from person to person, and we can't guarantee a particular outcome.</li>
<li>Clients under 18 need consent from a parent or guardian.</li>
</ul>

<h2>8. Respect and safety</h2>
<p>We treat every client with respect and ask the same in return. We may decline or stop services if behaviour is abusive or unsafe.</p>

<h2>9. Using our website</h2>
<p>Information on this website is general and not a substitute for an individual assessment. We aim to keep it accurate, but it may change without notice. The FlexFusionX name, logo, text and photos belong to FlexFusionX or are used with permission, and may not be copied without our consent. To the extent the law allows, we're not liable for any loss arising from use of this website.</p>

<h2>10. Privacy</h2>
<p>We handle your personal and health information as set out in our <a href="privacy.html">Privacy Policy</a>.</p>

<h2>11. Feedback and complaints</h2>
<p>Please tell us first at <a href="mailto:ck@flexfusionx.com.au">ck@flexfusionx.com.au</a> or <a href="tel:+61449969060">0449 969 060</a>, and we'll respond within 30 days. If you're not satisfied, you can contact the Health and Community Services Complaints Commissioner (SA) on 1800 232 007, or Ahpra about a practitioner's professional conduct. NDIS participants can also contact the NDIS Quality and Safeguards Commission on 1800 035 544.</p>

<h2>12. General</h2>
<p>We may update these terms. The version on this page at the time you book applies to that booking. These terms are governed by the laws of South Australia.</p>
"""

PAGE = r"""<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · FlexFusionX</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@125,600;125,700&family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,900&display=swap">
<style>
:root{{color-scheme:dark;--ink:#0A0A0B;--fg:#FFFFFF;--soft:#C9CCD0;--muted:#A3A7AC;--line:rgba(255,255,255,.12);--signal:#E3262D;
  --sans:"Inter",system-ui,-apple-system,"Segoe UI",Arial,sans-serif;--wide:"Archivo","Arial Black",system-ui,sans-serif;--gut:clamp(16px,4vw,7rem)}}
*{{box-sizing:border-box}}
html{{font-size:clamp(16px,calc(7.4px + .6vw),21px)}}
body{{margin:0;background:var(--ink);color:var(--fg);font:400 1.0625rem/1.65 var(--sans);-webkit-font-smoothing:antialiased}}
a{{color:inherit}}
:focus-visible{{outline:2px solid var(--signal);outline-offset:3px}}
.nav{{position:sticky;top:env(safe-area-inset-top,0px);z-index:10;background:rgba(10,10,11,.92);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.08)}}
.nav .in{{display:flex;align-items:center;gap:1.5rem;height:4.5rem;padding-inline:var(--gut)}}
.brand{{display:flex;align-items:center;gap:.75rem;text-decoration:none}}
.brand .mk{{height:1.5rem;filter:invert(1)}}.brand .wm{{height:.6875rem;filter:invert(1)}}
.back{{margin-left:auto;text-decoration:none;color:var(--soft);font:700 .65rem/1 var(--wide);font-stretch:125%;letter-spacing:.16em;text-transform:uppercase}}
.back:hover{{color:var(--fg)}}
.btn{{display:inline-flex;align-items:center;gap:.6rem;padding:.75rem 1rem;font:700 .75rem/1 var(--wide);font-stretch:125%;letter-spacing:.16em;text-transform:uppercase;text-decoration:none;background:var(--fg);color:var(--ink);border:1.5px solid var(--fg)}}
.btn:hover{{background:transparent;color:var(--fg)}}
@media (max-width:420px){{.brand .wm{{display:none}}}}
main{{padding:clamp(48px,9vh,110px) var(--gut) clamp(56px,10vh,120px)}}
.doc{{max-width:44rem}}
.eyebrow{{display:block;font:700 .6875rem/1.3 var(--wide);font-stretch:125%;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}}
h1{{margin:.9rem 0 .4rem;font:900 clamp(2.4rem,6vw,4.75rem)/.92 var(--sans);text-transform:uppercase;letter-spacing:-.035em}}
.meta{{color:var(--muted);font-size:.9rem;margin:0 0 2rem}}
h2{{margin:2.6rem 0 .8rem;padding-top:1.4rem;border-top:1px solid var(--line);font:900 1.15rem/1.1 var(--sans);text-transform:uppercase;letter-spacing:-.015em}}
p,li{{color:#D9DBDE}}
p{{margin:0 0 1rem}}
ul{{margin:0 0 1rem;padding-left:1.1rem}}
li{{margin:.35rem 0}}
li::marker{{color:var(--signal)}}
b{{color:var(--fg);font-weight:600}}
.tbc{{display:inline-block;padding:0 .4rem;border:1px dashed currentColor;color:var(--muted);font:600 .7rem/1.6 var(--sans);letter-spacing:.03em;vertical-align:.1em}}
.toc{{display:flex;flex-wrap:wrap;gap:.5rem 1.4rem;margin:0 0 1rem}}
.toc a{{text-decoration:none;color:var(--soft);font:700 .65rem/1.4 var(--wide);font-stretch:125%;letter-spacing:.14em;text-transform:uppercase}}
.toc a[aria-current]{{color:var(--fg);border-bottom:1.5px solid var(--signal)}}
footer{{border-top:1px solid rgba(255,255,255,.08);padding:2rem var(--gut) calc(2rem + env(safe-area-inset-bottom,0px));color:var(--muted);font-size:.8rem;display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;justify-content:space-between}}
footer a{{text-decoration:none}}footer a:hover{{text-decoration:underline}}
</style>
</head>
<body>
<header class="nav"><div class="in">
  <a class="brand" href="./" aria-label="FlexFusionX home"><img class="mk" src="{mark}" alt="FX"><img class="wm" src="{word}" alt="FlexFusionX"></a>
  <a class="back" href="./">← Back to site</a>
  <a class="btn" href="./#book">Book →</a>
</div></header>
<main><div class="doc">
  <nav class="toc" aria-label="Policies"><a href="privacy.html"{cur_p}>Privacy policy</a><a href="terms.html"{cur_t}>Terms &amp; cancellations</a></nav>
  <span class="eyebrow">FlexFusionX · Performance Physiotherapy</span>
  <h1>{title}</h1>
  {body}
</div></main>
<footer><span>FlexFusionX · ABN 81 239 476 840 · AHPRA PHY0004039512</span><span><a href="tel:+61449969060">0449 969 060</a> · <a href="mailto:ck@flexfusionx.com.au">ck@flexfusionx.com.au</a></span></footer>
</body>
</html>
"""


def _chips(html):
    return re.sub(r"\[\[(.+?)\]\]", r'<span class="tbc">\1</span>', html)


def build(out_dir, assets):
    pages = [
        ("privacy.html", "Privacy policy", "How FlexFusionX collects, uses and protects your personal and health information.", PRIVACY, True),
        ("terms.html", "Terms & cancellations", "Booking, fees, cancellation and website terms for FlexFusionX Performance Physiotherapy.", TERMS, False),
    ]
    written = []
    for name, title, desc, body, is_privacy in pages:
        html = PAGE.format(title=title.replace("&", "&amp;"), desc=desc, body=_chips(body), mark=assets["mark"], word=assets["word"],
                           cur_p=' aria-current="page"' if is_privacy else "", cur_t="" if is_privacy else ' aria-current="page"')
        path = os.path.join(out_dir, name)
        open(path, "w", encoding="utf8").write(html)
        written.append(path)
    return written
