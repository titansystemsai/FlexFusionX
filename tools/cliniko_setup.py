"""Set up FlexFusionX's Cliniko for online booking, to match the website.

Dry run by default (prints the plan, writes nothing):
    python tools/cliniko_setup.py
Apply the changes:
    python tools/cliniko_setup.py --apply

Reads the API key from ~/.cliniko. Snapshots the current business and appointment
types to tools/cliniko-backup/ and logs every call there, so changes can be reversed.
Cliniko is used for booking only: no prices or billing are set here.
Old appointment types are hidden from online booking, never deleted.

Not possible through the API (do these in Cliniko by hand):
  - Regular weekly hours (Settings > Practitioners > Cyriac > Availability)
  - Account/practice name, email "from" address, online booking rules
"""
import base64, json, os, sys, urllib.request, urllib.error
from datetime import datetime

APPLY = "--apply" in sys.argv
KEY = open(os.path.expanduser("~/.cliniko")).read().strip()
SHARD = KEY.rsplit("-", 1)[1]
BASE = f"https://api.{SHARD}.cliniko.com/v1/"
HEAD = {
    "Authorization": "Basic " + base64.b64encode((KEY + ":").encode()).decode(),
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "FlexFusionX site setup (ck@flexfusionx.com.au)",
}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cliniko-backup")
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, "changes.log"), "a", encoding="utf8")

PRACTITIONER = "1996016389709638948"
BUSINESS = "1996016392184278309"
OLD_TYPES = ["1996016391571910543", "1996016391907454864", "2020182783736950485"]  # Standard, First, NDIS Consult


def call(method, path, body=None):
    if method != "GET" and not APPLY:
        print(f"  [dry run] {method} {path} {json.dumps(body) if body else ''}")
        return 0, {"id": f"<new {path}>"}
    req = urllib.request.Request(BASE + path, method=method, headers=HEAD,
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req) as r:
            code, text = r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        code, text = e.code, e.read().decode()
    if method != "GET":
        LOG.write(json.dumps({"at": datetime.now().isoformat(), "method": method, "path": path,
                              "body": body, "code": code, "resp": text[:500]}) + "\n")
        print(f"  {method} {path} -> {code}")
        if code >= 300:
            print("   ", text[:300])
    return code, (json.loads(text) if text.strip().startswith("{") else text)


# --- snapshot first
for path in ["businesses/" + BUSINESS, "appointment_types"]:
    _, data = call("GET", path)
    name = path.split("?")[0].replace("/", "_")
    json.dump(data, open(os.path.join(OUT, f"before_{name}.json"), "w"), indent=1)

# --- 1. location details
print("1. Location details")
call("PATCH", "businesses/" + BUSINESS, {
    "business_name": "FlexFusionX", "display_name": "FlexFusionX",
    "address_1": "101 Portrush Road", "address_2": "Inside Balance Physiotherapy",
    "city": "Evandale", "state": "SA", "post_code": "5069", "country_code": "AU",
    "contact_information": "0449 969 060 · ck@flexfusionx.com.au",
    "email_reply_to": "ck@flexfusionx.com.au",
    "website_address": "https://flexfusionx.com.au/",
    "additional_information": "FlexFusionX is inside Balance Physiotherapy. Free on-site parking.",
})

# --- 2. bookable appointment types
print("2. Appointment types")
TYPES = [
    ("Initial assessment", 60, None, "#E3262D", {},
     "Your first visit: a full assessment, movement analysis and a written plan you leave with."),
    ("Follow-up (30 min)", 30, None, "#5B5F64", {},
     "Treatment, load adjustments and an updated program."),
    ("Follow-up (20 min)", 20, None, "#8A8E93", {},
     "A shorter check-in and progression of your program."),
    ("Manual therapy / massage (30 min)", 30, None, "#C77D2E", {}, "Performance manual therapy and massage."),
    ("Manual therapy / massage (45 min)", 45, None, "#C77D2E", {}, "Performance manual therapy and massage."),
    ("Manual therapy / massage (60 min)", 60, None, "#C77D2E", {}, "Performance manual therapy and massage."),
    ("Manual therapy / massage (90 min)", 90, None, "#C77D2E", {}, "Performance manual therapy and massage."),
    ("Telehealth consult (40 min)", 40, None, "#2E9E6B", {"telehealth_enabled": True},
     "A video consult from home. Assessment, advice and a program you can start straight away."),
    ("Telehealth follow-up (20 min)", 20, None, "#5DB88E", {"telehealth_enabled": True},
     "A video check-in to review progress and update your program."),
    ("NDIS session", 60, None, "#7B4FD0", {},
     "For NDIS participants, at home or in the clinic. Support workers welcome. Invoices can go to your plan manager."),
]
_, cur = call("GET", "appointment_types?per_page=100")
cur_names = {t["name"]: t["id"] for t in cur.get("appointment_types", [])}
for name, mins, item, color, extra, desc in TYPES:
    if name in cur_names:
        continue
    body = {"name": name, "duration_in_minutes": mins, "color": color, "description": desc,
            "show_in_online_bookings": True, "max_attendees": 1,
            "practitioner_ids": [PRACTITIONER], "business_ids": [BUSINESS], **extra}
    call("POST", "appointment_types", body)

# --- 3. hide old types from online booking (kept for existing appointments)
print("3. Hide old appointment types from online booking")
for t in OLD_TYPES:
    call("PATCH", "appointment_types/" + t, {"show_in_online_bookings": False})

# --- 4. switch the location on for online bookings
print("4. Turn on online bookings for the location")
call("PATCH", "businesses/" + BUSINESS, {"show_in_online_bookings": True})

print("Done." if APPLY else "Dry run only. Re-run with --apply to make these changes.")
