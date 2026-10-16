"""Create FlexFusionX's "New patient intake" form in Cliniko.

Rebuilt from the Health Intake step of the old Lovable site (old-site/chunks/BookingSection-*.js),
same questions, pain types and red flags, as a Cliniko patient form template.

Dry run by default:   python tools/cliniko_intake.py
Create it:            python tools/cliniko_intake.py --apply
Re-running is safe: it skips creation if a template with the same name exists.
"""
import base64, json, os, sys, urllib.request, urllib.error
from datetime import datetime

APPLY = "--apply" in sys.argv
KEY = open(os.path.expanduser("~/.cliniko")).read().strip()
BASE = f"https://api.{KEY.rsplit('-', 1)[1]}.cliniko.com/v1/"
HEAD = {"Authorization": "Basic " + base64.b64encode((KEY + ":").encode()).decode(),
        "Accept": "application/json", "Content-Type": "application/json",
        "User-Agent": "FlexFusionX site setup (ck@flexfusionx.com.au)"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cliniko-backup")
os.makedirs(OUT, exist_ok=True)
NAME = "New patient intake"

YN = [{"value": "Yes"}, {"value": "No"}, {"value": "Not sure"}]
SCALE = [{"value": str(i)} for i in range(11)]


def text(name, required=False):
    return {"type": "text", "name": name, "required": required}


def para(name, required=False):
    return {"type": "paragraph", "name": name, "required": required}


def radio(name, answers, required=False):
    return {"type": "radiobuttons", "name": name, "required": required, "answers": answers, "other": {"enabled": False}}


def checks(name, answers, required=False, other=False):
    return {"type": "checkboxes", "name": name, "required": required,
            "answers": [{"value": a} for a in answers], "other": {"enabled": other}}


FORM = {
    "name": NAME,
    "restricted_to_practitioner": False,
    "email_to_patient_on_completion": False,
    "content": {"sections": [
        {"name": "Before your first session",
         "description": "This is the same intake your physio would normally go through at the start of your session. "
                        "Answering it ahead saves time, so we can get straight into testing and treatment. "
                        "It takes about 3 minutes. Only the first question about your injury is required.",
         "questions": [
             {"type": "full_name", "name": "Your name", "required": True, "patient_field_connection": "full_name",
              "options": {"title_enabled": False, "preferred_first_name_enabled": True}},
             {"type": "date", "name": "Date of birth", "required": False, "patient_field_connection": "date_of_birth"},
             text("Main sport or activity (if any)"),
         ]},
        {"name": "Your injury",
         "questions": [
             para("What's the problem? (e.g. right shoulder pain when lifting overhead, started 3 weeks ago after a gym session)", True),
             para("How and when did it start? (e.g. suddenly after a fall, gradually over months, no clear cause)"),
             text("Where is the pain? (e.g. front of right shoulder, spreads down the arm)"),
             radio("Pain right now (0 = no pain, 10 = worst imaginable)", SCALE),
             radio("Pain at its worst (0 to 10)", SCALE),
             radio("Pain at its best (0 to 10)", SCALE),
             checks("Type of pain (select all that apply)", ["Sharp", "Dull / ache", "Burning", "Throbbing", "Stabbing", "Stiff"], other=True),
             para("What makes it worse? (e.g. reaching overhead, sleeping on it)"),
             para("What makes it better? (e.g. rest, ice, anti-inflammatories)"),
             para("How does it change over 24 hours? (e.g. worse in the morning, eases through the day, wakes me at night)"),
         ]},
        {"name": "Nerve symptoms",
         "questions": [
             radio("Pins and needles?", YN),
             radio("Numbness?", YN),
             radio("Weakness?", YN),
         ]},
        {"name": "History",
         "questions": [
             radio("Have you had this problem before?", YN),
             para("If yes, when, and how was it managed?"),
             radio("Have you had any imaging (X-ray, MRI, ultrasound)?", YN),
             para("If yes, what did it show?"),
             para("Current medications (optional) (e.g. ibuprofen as needed)"),
         ]},
        {"name": "Health screening",
         "description": "None of these means you can't be treated. They help us check for anything that needs a medical review first.",
         "questions": [
             checks("Have you had any of these in the last few weeks?", [
                 "Unexplained weight loss", "Fever or feeling unwell", "Night pain not relieved by rest",
                 "Bowel or bladder changes", "Numbness in the groin or saddle area", "Recent significant trauma",
                 "None of these"]),
         ]},
        {"name": "Your goals",
         "questions": [
             para("What are your goals for treatment? (e.g. get back to running pain-free in 6 weeks)"),
         ]},
    ]},
}


def call(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, headers=HEAD,
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req) as r:
            code, out = r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        code, out = e.code, e.read().decode()
    return code, (json.loads(out) if out.strip().startswith("{") else out)


_, existing = call("GET", "patient_form_templates")
names = [t["name"] for t in existing.get("patient_form_templates", [])]
qcount = sum(len(s["questions"]) for s in FORM["content"]["sections"])
print(f"{NAME}: {len(FORM['content']['sections'])} sections, {qcount} questions")
if NAME in names:
    print("Already exists, nothing to do.")
elif not APPLY:
    print("Dry run only. Re-run with --apply to create it.")
else:
    code, d = call("POST", "patient_form_templates", FORM)
    with open(os.path.join(OUT, "changes.log"), "a", encoding="utf8") as log:
        log.write(json.dumps({"at": datetime.now().isoformat(), "method": "POST", "path": "patient_form_templates",
                              "code": code, "resp": str(d)[:500]}) + "\n")
    print("POST patient_form_templates ->", code, d.get("id") if isinstance(d, dict) else str(d)[:400])
