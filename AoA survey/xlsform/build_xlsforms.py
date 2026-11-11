#!/usr/bin/env python3
"""
build_xlsforms.py
=================
Builds KoboToolbox / ODK XLSForms (English) for the three SSA EdTech Landscape
Review instruments, plus a question map and a list of review notes.

  python build_xlsforms.py            # writes into /mnt/user-data/outputs

Outputs
  SSA_Teacher_Survey_v1_EN_XLSForm.xlsx
  SSA_Provider_Survey_v1_EN_XLSForm.xlsx
  SSA_Expert_Consultation_R1_v1_EN_XLSForm.xlsx
  SSA_XLSForm_Question_Map_and_Review_Notes.xlsx

Design rules (see the review notes sheet for the reasoning)
  * Explicit primary consent gate (required=yes) terminates survey immediately if declined.
  * Every substantive question is optional, as the survey introductions promise.
  * Location (GPS) capture is explicitly gated by a consent sub-question.
  * PII and contact data are flagged, sanitized, and decoupled for detached storage.
  * "Select up to N" and "do not combine None/No view with others" are enforced
    as constraints, not just printed as text.
  * "Rank your top three" becomes three sequential single-choice questions with
    duplicate prevention (works in every Kobo client, unlike full ranking).
  * Instructions such as "select all that apply" live in the hint.
  * French / Portuguese later: add label::Français (fr) / label::Português (pt)
    columns next to the English ones; no logic changes are needed.

The script also validates each form structurally and runs scenario tests on
the actual skip-logic / constraint expressions it writes into the files.
"""
import re
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

OUT = Path(__file__).resolve().parent
LANG = "English (en)"
LBL, HNT, CMSG = ("label::" + LANG, "hint::" + LANG, "constraint_message::" + LANG)

# ---------------------------------------------------------------- code helpers
SPECIAL = {"don't know": "dont_know", "none": "none", "no view": "no_view",
           "not applicable": "not_applicable", "not sure": "not_sure",
           "i am not sure": "not_sure"}


def norm(s):
    return s.replace("\u2019", "'").strip()


def slug(label, limit=30):
    s = re.sub(r"\([^)]*\)", "", norm(label)).lower().replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    if len(s) > limit:
        s = s[:limit].rsplit("_", 1)[0] or s[:limit]
    return s or "opt"


def code_for(label):
    n = norm(label).lower()
    if n in SPECIAL:
        return SPECIAL[n]
    if re.match(r"^other(\s*[\(,]|$)", n) or n.startswith("other national"):
        return "other"
    return slug(label)


def O(text):
    """'a · b · c' -> ['a', 'b', 'c']"""
    return [p.strip() for p in text.split("\u00b7") if p.strip()]


# ------------------------------------------------------------------ the engine
class Form:
    def __init__(self, fid, title, instrument):
        self.fid, self.title, self.instrument = fid, title, instrument
        self.rows, self.lists, self._lidx = [], {}, {}
        self.names, self.qmap, self.review = set(), [], []
        self.tests = []          # (question, field, answers, dot, expected)

    # -- low level
    def _add(self, **r):
        if r.get("name"):
            assert r["name"] not in self.names, "duplicate name " + r["name"]
            self.names.add(r["name"])
        self.rows.append(r)

    def lst(self, options, hint):
        items, used = [], set()
        for o in options:
            code, label = o if isinstance(o, tuple) else (code_for(o), o)
            base, i = code, 2
            while code in used:
                code, i = "%s_%d" % (base, i), i + 1
            used.add(code)
            items.append((code, label))
        key = tuple(items)
        if key in self._lidx:
            return self._lidx[key]
        name, i = hint, 2
        while name in self.lists:
            name, i = "%s_%d" % (hint, i), i + 1
        self.lists[name] = items
        self._lidx[key] = name
        return name

    def codes(self, listname):
        return [c for c, _ in self.lists[listname]]

    # -- structure
    def begin(self, name, label, appearance=None, relevant=None):
        self._add(type="begin_group", name=name, label=label,
                  appearance=appearance, relevant=relevant)

    def end(self):
        self._add(type="end_group")

    def note(self, name, label, relevant=None):
        self._add(type="note", name=name, label=label, relevant=relevant)

    def calc(self, name, value):
        self._add(type="calculate", name=name, calculation=value)

    # -- questions
    def _log(self, doc, names, qtype, listname="", maxsel=None, excl=None,
             relevant=None, pii=False, note=""):
        self.qmap.append(dict(doc=doc, names=names, type=qtype, list=listname,
                              max=maxsel or "", excl=", ".join(excl or []),
                              relevant=relevant or "", pii="YES" if pii else "",
                              note=note))

    def _specify(self, name, listname, kind, specify):
        codes = self.codes(listname)
        sp = {}
        if specify is None:
            if "other" in codes:
                sp["other"] = "Please specify."
        elif isinstance(specify, dict):
            sp = dict(specify)
        for code, prompt in sp.items():
            assert code in codes, "specify code %s not in list for %s" % (code, name)
            expr = ("selected(${%s}, '%s')" if kind == "multi" else "${%s}='%s'") % (name, code)
            fname = "%s_%s" % (name, code)
            self._add(type="text", name=fname, label=prompt, relevant=expr)
            self._log(self._cur_doc, fname, "text (specify)", relevant=expr,
                      note="Free-text follow-up to '%s'" % code)
            self.tests.append((fname, "relevant", {name: code}, None, True))
            self.tests.append((fname, "relevant", {name: ""}, None, False))

    def select_one(self, name, label, options, doc=None, hint=None, relevant=None,
                   appearance=None, specify=None, note="", required=None,
                   constraint=None, cmsg=None):
        self._cur_doc = doc or name
        ln = self.lst(options, name.lower())
        req_val = "yes" if required in (True, "yes") else None
        self._add(type="select_one " + ln, name=name, label=label, hint=hint,
                  relevant=relevant, appearance=appearance, required=req_val,
                  constraint=constraint, cmsg=cmsg)
        self._log(self._cur_doc, name, "select_one", ln, relevant=relevant, note=note)
        self._specify(name, ln, "one", specify)
        return ln

    def select_multi(self, name, label, options, doc=None, maxsel=None, excl=None,
                     hint=None, relevant=None, appearance=None, specify=None, note="", required=None):
        self._cur_doc = doc or name
        ln = self.lst(options, name.lower())
        codes = self.codes(ln)
        labels = dict(self.lists[ln])
        excl = excl or []
        for e in excl:
            assert e in codes, "exclusive %s not in list %s" % (e, ln)
        parts, msgs = [], []
        if maxsel:
            parts.append("count-selected(.)<=%d" % maxsel)
            msgs.append("Please select no more than %d answers." % maxsel)
        for e in excl:
            parts.append("not(selected(., '%s') and count-selected(.)>1)" % e)
        if excl:
            msgs.append("%s cannot be combined with other answers." %
                        " / ".join("\u201c%s\u201d" % labels[e] for e in excl))
        constraint = " and ".join(parts) or None
        if hint is None:
            hint = ("Select up to %d." % maxsel) if maxsel else "Select all that apply."
        req_val = "yes" if required in (True, "yes") else None
        self._add(type="select_multiple " + ln, name=name, label=label, hint=hint,
                  relevant=relevant, appearance=appearance, constraint=constraint,
                  cmsg=" ".join(msgs) or None, required=req_val)
        self._log(self._cur_doc, name, "select_multiple", ln, maxsel, excl, relevant, note=note)
        if constraint:
            if maxsel:
                self.tests.append((name, "constraint", {}, " ".join(codes[:maxsel]), True))
                self.tests.append((name, "constraint", {}, " ".join(codes[:maxsel + 1]), False))
            for e in excl:
                other = next(c for c in codes if c != e)
                self.tests.append((name, "constraint", {}, e, True))
                self.tests.append((name, "constraint", {}, e + " " + other, False))
        self._specify(name, ln, "multi", specify)
        return ln

    def geopoint(self, name, label, doc=None, hint=None, relevant=None, note="", required=None):
        self._cur_doc = doc or name
        req_val = "yes" if required in (True, "yes") else None
        self._add(type="geopoint", name=name, label=label, hint=hint, relevant=relevant, required=req_val)
        self._log(self._cur_doc, name, "geopoint", relevant=relevant, note=note)

    def text(self, name, label, doc=None, hint=None, relevant=None, pii=False, note="", required=None):
        self._cur_doc = doc or name
        req_val = "yes" if required in (True, "yes") else None
        self._add(type="text", name=name, label=label, hint=hint, relevant=relevant,
                  appearance="multiline", required=req_val)
        self._log(self._cur_doc, name, "text", relevant=relevant, pii=pii, note=note)

    def matrix(self, name, label, rows, options, doc=None, note=""):
        """rows = [(row_name, row_label)]; one select_one per row, shown as a table."""
        self._cur_doc = doc or name
        ln = self.lst(options, name.lower())
        self.begin(name, label, appearance="table-list")
        for rname, rlabel in rows:
            self._add(type="select_one " + ln, name=rname, label=rlabel)
            self._log(self._cur_doc, rname, "select_one (matrix row)", ln, note=rlabel)
        self.end()
        return ln

    def top3(self, name, label, options, doc=None, hint=None, note=""):
        """Rank top three as three sequential single-choice questions."""
        self._cur_doc = doc or name
        ln = self.lst(options, name.lower())
        n1, n2, n3 = ("%s_%d" % (name, i) for i in (1, 2, 3))
        self.begin("g_" + name, label + " Rank your top three.", appearance="field-list")
        self._add(type="select_one " + ln, name=n1, label="1st choice (most important)", hint=hint)
        c2, c3 = ". != ${%s}" % n1, ". != ${%s} and . != ${%s}" % (n1, n2)
        r2, r3 = "${%s} != ''" % n1, "${%s} != ''" % n2
        self._add(type="select_one " + ln, name=n2, label="2nd choice", relevant=r2,
                  constraint=c2, cmsg="Please choose a different answer from your 1st choice.")
        self._add(type="select_one " + ln, name=n3, label="3rd choice", relevant=r3,
                  constraint=c3, cmsg="Please choose an answer different from your 1st and 2nd choices.")
        self.end()
        codes = self.codes(ln)
        self._log(self._cur_doc, "%s, %s, %s" % (n1, n2, n3), "rank top 3 (3 questions)", ln,
                  note="1st/2nd/3rd choice; later ranks appear after the earlier one is answered")
        a, b, c = codes[0], codes[1], codes[2]
        self.tests += [(n2, "constraint", {n1: a}, a, False), (n2, "constraint", {n1: a}, b, True),
                       (n3, "constraint", {n1: a, n2: b}, a, False),
                       (n3, "constraint", {n1: a, n2: b}, b, False),
                       (n3, "constraint", {n1: a, n2: b}, c, True),
                       (n2, "relevant", {n1: ""}, None, False), (n2, "relevant", {n1: a}, None, True),
                       (n3, "relevant", {n2: ""}, None, False), (n3, "relevant", {n2: b}, None, True)]
        if "other" in codes:
            expr = " or ".join("${%s}='other'" % n for n in (n1, n2, n3))
            self._add(type="text", name=name + "_other", label="Please specify.", relevant=expr)
            self._log(self._cur_doc, name + "_other", "text (specify)", relevant=expr)
            self.tests += [(name + "_other", "relevant", {n2: "other"}, None, True),
                           (name + "_other", "relevant", {n1: a, n2: b, n3: c}, None, False)]
        return ln

    def issue(self, doc, kind, text):
        self.review.append((self.title, doc, kind, text))

    # -- output
    def write(self, path):
        wb = Workbook()
        ws = wb.active
        ws.title = "survey"
        cols = [("type", "type"), ("name", "name"), ("label", LBL), ("hint", HNT),
                ("required", "required"), ("relevant", "relevant"),
                ("constraint", "constraint"), ("cmsg", CMSG),
                ("appearance", "appearance"), ("calculation", "calculation")]
        used = [(k, h) for k, h in cols if any(r.get(k) for r in self.rows)]
        ws.append([h for _, h in used])
        for r in self.rows:
            ws.append([r.get(k) or None for k, _ in used])
        wc = wb.create_sheet("choices")
        wc.append(["list_name", "name", LBL])
        for ln, items in self.lists.items():
            for code, label in items:
                wc.append([ln, code, label])
        wsx = wb.create_sheet("settings")
        wsx.append(["form_title", "form_id", "default_language", "style"])
        wsx.append([self.title, self.fid, LANG, "pages"])
        for sh in (ws, wc, wsx):
            for c in sh[1]:
                c.font = Font(name="Arial", bold=True)
            sh.freeze_panes = "A2"
            for col in sh.columns:
                w = max(len(str(c.value or "")) for c in col[:60])
                sh.column_dimensions[col[0].column_letter].width = min(max(w + 2, 10), 70)
        wb.save(path)


# ------------------------------------------------------------ expression tests
def xp(expr, ans, dot=""):
    """Evaluate the small XPath subset used in the forms."""
    e = re.sub(r"\$\{([^}]+)\}", lambda m: "A(%r)" % m.group(1), expr)
    e = re.sub(r"count-selected\(([^)]*)\)", lambda m: "CNT(%s)" % m.group(1).strip(), e)
    e = re.sub(r"selected\(([^,]+),\s*('[^']*')\)", r"SEL(\1,\2)", e)
    e = re.sub(r"(?<![\w'\)])\.(?![\w'])", "DOT", e)
    e = re.sub(r"(?<![!<>=])=(?!=)", "==", e)
    e = e.replace("not(", "not (")
    env = {"A": lambda n: ans.get(n, ""), "SEL": lambda v, c: c in str(v).split(),
           "CNT": lambda v: len(str(v).split()), "DOT": dot}
    return bool(eval(e, {"__builtins__": {}}, env))


def validate(f):
    problems = []
    rows = f.rows
    depth = 0
    for r in rows:
        if r["type"] == "begin_group":
            depth += 1
        elif r["type"] == "end_group":
            depth -= 1
            if depth < 0:
                problems.append("end_group without begin_group")
    if depth != 0:
        problems.append("unbalanced groups (%d)" % depth)
    name_re = re.compile(r"^[A-Za-z_][A-Za-z0-9_.\-]*$")
    seen = {}
    for i, r in enumerate(rows):
        n = r.get("name")
        if n:
            if not name_re.match(n):
                problems.append("bad name " + n)
            seen[n] = i
        t = r["type"]
        if t.startswith("select_") and t.split()[1] not in f.lists:
            problems.append("missing list for " + n)
        if t not in ("end_group", "calculate", "start", "end", "today") and not r.get("label"):
            problems.append("empty label: " + str(n))
    for ln, items in f.lists.items():
        codes = [c for c, _ in items]
        if len(codes) != len(set(codes)):
            problems.append("duplicate codes in list " + ln)
        for c in codes:
            if not re.match(r"^[A-Za-z0-9_\-]+$", c):
                problems.append("bad choice code %s in %s" % (c, ln))
    qlist = {r["name"]: r["type"].split()[1] for r in rows
             if r["type"].startswith("select_") and r.get("name")}
    for i, r in enumerate(rows):
        for field in ("relevant", "constraint"):
            ex = r.get(field)
            if not ex:
                continue
            if ex.count("(") != ex.count(")"):
                problems.append("unbalanced parens in %s of %s" % (field, r.get("name")))
            for ref in re.findall(r"\$\{([^}]+)\}", ex):
                if ref not in seen:
                    problems.append("%s of %s refers to unknown %s" % (field, r["name"], ref))
                elif seen[ref] >= i:
                    problems.append("%s of %s refers forward to %s" % (field, r["name"], ref))
            for ref, code in re.findall(r"\$\{([^}]+)\}\s*!?=\s*'([^']*)'", ex):
                if code and ref in qlist and code not in f.codes(qlist[ref]):
                    problems.append("%s of %s: code %r not in list of %s" % (field, r["name"], code, ref))
            for ref, code in re.findall(r"selected\(\$\{([^}]+)\},\s*'([^']*)'\)", ex):
                if ref in qlist and code not in f.codes(qlist[ref]):
                    problems.append("%s of %s: code %r not in list of %s" % (field, r["name"], code, ref))
    return problems


def run_tests(f, extra):
    byname = {r["name"]: r for r in f.rows if r.get("name")}
    fails, n = [], 0
    for q, field, ans, dot, expected in f.tests + extra:
        r = byname.get(q)
        if r is None or not r.get(field):
            fails.append("no %s on %s" % (field, q))
            continue
        got = xp(r[field], ans, dot or "")
        n += 1
        if got != expected:
            fails.append("%s.%s ans=%s dot=%r expected %s got %s" % (q, field, ans, dot, expected, got))
    return n, fails


# ------------------------------------------------------------------ data lists
SSA48 = [("AGO", "Angola"), ("BEN", "Benin"), ("BWA", "Botswana"), ("BFA", "Burkina Faso"),
         ("BDI", "Burundi"), ("CPV", "Cabo Verde"), ("CMR", "Cameroon"),
         ("CAF", "Central African Republic"), ("TCD", "Chad"), ("COM", "Comoros"),
         ("COD", "Congo, Dem. Rep."), ("COG", "Congo, Rep."), ("CIV", "C\u00f4te d\u2019Ivoire"),
         ("GNQ", "Equatorial Guinea"), ("ERI", "Eritrea"), ("SWZ", "Eswatini"), ("ETH", "Ethiopia"),
         ("GAB", "Gabon"), ("GMB", "The Gambia"), ("GHA", "Ghana"), ("GIN", "Guinea"),
         ("GNB", "Guinea-Bissau"), ("KEN", "Kenya"), ("LSO", "Lesotho"), ("LBR", "Liberia"),
         ("MDG", "Madagascar"), ("MWI", "Malawi"), ("MLI", "Mali"), ("MRT", "Mauritania"),
         ("MUS", "Mauritius"), ("MOZ", "Mozambique"), ("NAM", "Namibia"), ("NER", "Niger"),
         ("NGA", "Nigeria"), ("RWA", "Rwanda"), ("STP", "S\u00e3o Tom\u00e9 and Pr\u00edncipe"),
         ("SEN", "Senegal"), ("SYC", "Seychelles"), ("SLE", "Sierra Leone"), ("SOM", "Somalia"),
         ("ZAF", "South Africa"), ("SSD", "South Sudan"), ("SDN", "Sudan"), ("TZA", "Tanzania"),
         ("TGO", "Togo"), ("UGA", "Uganda"), ("ZMB", "Zambia"), ("ZWE", "Zimbabwe")]
assert len(SSA48) == 48 and len({c for c, _ in SSA48}) == 48

WORLD_RAW = """AFG Afghanistan|ALB Albania|DZA Algeria|AND Andorra|AGO Angola|ATG Antigua and Barbuda|ARG Argentina|ARM Armenia|AUS Australia|AUT Austria|AZE Azerbaijan|BHS Bahamas|BHR Bahrain|BGD Bangladesh|BRB Barbados|BLR Belarus|BEL Belgium|BLZ Belize|BEN Benin|BTN Bhutan|BOL Bolivia|BIH Bosnia and Herzegovina|BWA Botswana|BRA Brazil|BRN Brunei|BGR Bulgaria|BFA Burkina Faso|BDI Burundi|CPV Cabo Verde|KHM Cambodia|CMR Cameroon|CAN Canada|CAF Central African Republic|TCD Chad|CHL Chile|CHN China|COL Colombia|COM Comoros|COD Congo, Dem. Rep.|COG Congo, Rep.|CRI Costa Rica|CIV Côte d’Ivoire|HRV Croatia|CUB Cuba|CYP Cyprus|CZE Czechia|DNK Denmark|DJI Djibouti|DMA Dominica|DOM Dominican Republic|ECU Ecuador|EGY Egypt|SLV El Salvador|GNQ Equatorial Guinea|ERI Eritrea|EST Estonia|SWZ Eswatini|ETH Ethiopia|FJI Fiji|FIN Finland|FRA France|GAB Gabon|GMB The Gambia|GEO Georgia|DEU Germany|GHA Ghana|GRC Greece|GRD Grenada|GTM Guatemala|GIN Guinea|GNB Guinea-Bissau|GUY Guyana|HTI Haiti|HND Honduras|HUN Hungary|ISL Iceland|IND India|IDN Indonesia|IRN Iran|IRQ Iraq|IRL Ireland|ISR Israel|ITA Italy|JAM Jamaica|JPN Japan|JOR Jordan|KAZ Kazakhstan|KEN Kenya|KIR Kiribati|KWT Kuwait|KGZ Kyrgyzstan|LAO Laos|LVA Latvia|LBN Lebanon|LSO Lesotho|LBR Liberia|LBY Libya|LIE Liechtenstein|LTU Lithuania|LUX Luxembourg|MDG Madagascar|MWI Malawi|MYS Malaysia|MDV Maldives|MLI Mali|MLT Malta|MHL Marshall Islands|MRT Mauritania|MUS Mauritius|MEX Mexico|FSM Micronesia|MDA Moldova|MCO Monaco|MNG Mongolia|MNE Montenegro|MAR Morocco|MOZ Mozambique|MMR Myanmar|NAM Namibia|NRU Nauru|NPL Nepal|NLD Netherlands|NZL New Zealand|NIC Nicaragua|NER Niger|NGA Nigeria|PRK North Korea|MKD North Macedonia|NOR Norway|OMN Oman|PAK Pakistan|PLW Palau|PAN Panama|PNG Papua New Guinea|PRY Paraguay|PER Peru|PHL Philippines|POL Poland|PRT Portugal|QAT Qatar|ROU Romania|RUS Russia|RWA Rwanda|KNA Saint Kitts and Nevis|LCA Saint Lucia|VCT Saint Vincent and the Grenadines|WSM Samoa|SMR San Marino|STP São Tomé and Príncipe|SAU Saudi Arabia|SEN Senegal|SRB Serbia|SYC Seychelles|SLE Sierra Leone|SGP Singapore|SVK Slovakia|SVN Slovenia|SLB Solomon Islands|SOM Somalia|ZAF South Africa|KOR South Korea|SSD South Sudan|ESP Spain|LKA Sri Lanka|SDN Sudan|SUR Suriname|SWE Sweden|CHE Switzerland|SYR Syria|TJK Tajikistan|TZA Tanzania|THA Thailand|TLS Timor-Leste|TGO Togo|TON Tonga|TTO Trinidad and Tobago|TUN Tunisia|TUR Türkiye|TKM Turkmenistan|TUV Tuvalu|UGA Uganda|UKR Ukraine|ARE United Arab Emirates|GBR United Kingdom|USA United States|URY Uruguay|UZB Uzbekistan|VUT Vanuatu|VEN Venezuela|VNM Vietnam|YEM Yemen|ZMB Zambia|ZWE Zimbabwe|VAT Holy See|PSE Palestine|TWN Taiwan|XKX Kosovo"""
WORLD = []
for _p in WORLD_RAW.split("|"):
    _c, _n = _p.split(" ", 1)
    WORLD.append((_c, _n))
WORLD.sort(key=lambda t: t[1].replace("\u00c3", "A").lower())
WORLD.append(("OTH", "Other / not listed"))
assert len({c for c, _ in WORLD}) == len(WORLD), "duplicate world codes"
assert all(re.match(r"^[A-Z]{3}$", c) for c, _ in WORLD)
assert {c for c, _ in SSA48} <= {c for c, _ in WORLD}, "SSA code missing from world list"

AGREE5 = ["Strongly disagree", "Disagree", "Neither", "Agree", "Strongly agree"]
CONF = ["Low", "Medium", "High"]


# ============================================================ TEACHER SURVEY
def build_teacher():
    f = Form("ssa_teacher_survey_v1_en", "SSA EdTech Landscape Review - Teacher survey (EN, draft v1)",
             "teacher_survey_v1_en")
    f._add(type="start", name="start")
    f._add(type="end", name="end")
    f._add(type="today", name="today")
    f.calc("instrument_version", "'teacher_survey_v1_en'")
    f.begin("intro", "Teacher survey")
    f.note("intro_1", "**Sub-Saharan Africa EdTech Landscape Review: Teacher survey**")
    f.note("intro_2", "Thank you for taking the time to share your experience. This short survey is part of the Sub-Saharan Africa EdTech Landscape Review, an independent study of how digital tools are being used in education, carried out under the Global EdTech Alliance of Alliances, incubated within UNESCO\u2019s Global Education Coalition.")
    f.note("intro_3", "We would be grateful for your view as a teacher. You see every day what works in your classroom and what does not, and that is exactly what this review aims to understand. We want to hear from you whether you use digital tools a lot, a little or not at all.")
    f.note("intro_4", "The survey takes about ten minutes. Your answers are anonymous: we do not ask for your name or your school\u2019s name, and nothing you say will be attributed to you. Every substantive question is optional; please skip anything you would prefer not to answer. Participation is completely voluntary.")
    f.select_one("consent_agreed",
                 "Do you agree to take part in this survey under the terms described above?",
                 [("yes", "Yes, I agree to take part"),
                  ("no", "No, I do not wish to take part")],
                 doc="Consent Gate",
                 hint="Participation is voluntary. You may withdraw or stop at any time.",
                 required=True,
                 constraint=". = 'yes'",
                 cmsg="Submission is disabled because consent was declined. Please close your browser window without submitting.")
    f.note("consent_declined",
           "**Thank you for your time.** You have chosen not to participate, so no survey questions will be shown. Please close this browser window without submitting (blank submissions are disabled).",
           relevant="${consent_agreed}='no'")
    f.end()

    f.begin("sec_A", "A. A little about you and where you teach", relevant="${consent_agreed}='yes'")
    f.select_one("A1_country", "In which country do you teach?",
                 SSA48 + [("OTH", "Other")], doc="A1", appearance="minimal", specify=False)
    f.text("A1_region", "If you can, please specify region, state or province:", doc="A1",
           hint="Please state province, state, or district only (do not include school or town name).",
           relevant="${A1_country} != ''")
    f.select_one("A2_school_type", "Which best describes your school?", [
        ("public", "Public / government"), ("low_fee_private", "Low-fee private"),
        ("other_private", "Other private (fee-paying)"), ("faith_based", "Faith-based or mission school"),
        ("community", "Community school"), ("international", "International school"),
        ("refugee_displaced", "School in a refugee camp or serving displaced learners"), "Other"], doc="A2")
    f.select_multi("A3_levels", "Which levels do you currently teach?", [
        ("early_years", "Early years / pre-primary (about ages 3 to 5)"), ("primary", "Primary (about ages 6 to 12)"),
        ("lower_secondary", "Lower secondary (about ages 12 to 15)"),
        ("upper_secondary", "Upper secondary (about ages 15 to 18)"),
        "Other (e.g. adult or non-formal learning, technical and vocational)"], doc="A3")
    f.select_multi("A4_languages", "In which language(s) do you normally give your lessons?", [
        "English", "French", "Portuguese", "Kiswahili", "Arabic",
        ("local_language", "A national or local language (please name)"), "Spanish"], doc="A4",
        specify={"local_language": "Please name the language(s)."})
    f.select_one("A5_understand", "How well do most of your students understand the language you give lessons in?", [
        "Well", "Partly", ("hardly", "Hardly at all, it\u2019s a new language for them"),
        ("varies", "It varies a lot between students"), "I am not sure"], doc="A5")
    f.select_one("A6_subject", "Which subject area do you mainly teach?", [
        ("languages_literacy", "Languages and literacy"), ("maths_science", "Maths and science"),
        ("humanities", "Humanities and social studies"),
        ("all_subjects", "All subjects (e.g. early years or primary class teacher)"), "Other"], doc="A6")
    f.select_one("A7_experience", "How long have you been teaching?", [
        ("lt3", "Less than 3 years"), ("3_10", "3\u201310 years"), ("gt10", "More than 10 years")], doc="A7")
    f.select_multi("A8_training", "What training have you had for teaching?", [
        ("college_programme", "A teacher-education programme at a college or university (certificate, diploma or degree)"),
        ("other_degree", "A university degree in another subject"),
        ("in_service", "Training while already teaching (e.g. an in-service or distance programme)"),
        ("short_course", "A short induction or training course (e.g. from the ministry, an NGO or a programme)"),
        ("studying_now", "I am currently studying for a teaching qualification"),
        ("on_the_job", "I learned mainly on the job")], doc="A8")
    f.select_one("A9_location", "Where is your school located?", [
        ("major_city", "A major city"), ("smaller_town", "A smaller town"), ("rural", "A rural area")], doc="A9")
    f.select_one("A10_class_size", "How many students are usually in your class?", [
        ("lt30", "Fewer than 30"), ("30_50", "30\u201350"), ("51_80", "51\u201380"), ("gt80", "More than 80")], doc="A10")
    f.select_one("A11_gps_consent",
                 "Are you willing to share your school's approximate GPS coordinates to help map regional educational infrastructure?",
                 [("yes", "Yes, record school GPS coordinates"),
                  ("no", "No, skip GPS recording")],
                 doc="A11 (GPS Consent)",
                 hint="Optional. Coordinates are aggregated at district level to prevent school identification.")
    f.geopoint("A11_gps_location", "School GPS location (optional)", doc="A11",
               hint="If at school, record GPS location to help map school infrastructure. In KoboCollect on Android, tap 'Record Location' (works offline with device GPS).",
               relevant="${A11_gps_consent}='yes'",
               note="Captures coordinates for spatial mapping against school registries (Giga/OpenStreetMap)")
    f.end()

    f.begin("sec_B", "B. Digital tools in your classroom", relevant="${consent_agreed}=\'yes\'")
    f.note("B_intro", "This section asks about your use (or non-use) of technology in your classroom. Technology is broad and by \u201cdigital tools\u201d we mean anything electronic you use for your teaching, including your own mobile phone (for example to look things up, or WhatsApp with students or parents), radio or TV lessons, a computer, tablet or projector, and apps or websites.")
    f.select_one("B1_use_digital", "Do you use any digital tools (phone, tablet, TV, computer, laptop) in your teaching, even occasionally?",
                 [("yes", "Yes"), ("no", "No, not at present")], doc="B1")
    f.select_multi("B1_why_no", "What are the main reasons?", [
        ("no_devices", "No devices at school"), ("no_electricity", "No electricity"), ("no_internet", "No internet"),
        ("not_allowed", "Not expected or not allowed"), ("no_training", "No training"),
        ("not_useful", "Not useful for my students"), ("cost", "Cost"), "Other"],
        doc="B1 (follow-up)", maxsel=3, relevant="${B1_use_digital}='no'")
    f.select_multi("B2_tools", "Which kinds of digital tools do you typically use in your teaching, whether in class, for homework, or for feedback and communication?", [
        ("apps", "Learning or subject apps"), ("video_platforms", "Content or video platforms"),
        ("lms", "A learning-management system (assignments, grades)"),
        ("messaging", "Messaging groups with students or parents (e.g. WhatsApp)"),
        ("sms", "SMS or basic-phone services"), ("radio_tv", "Radio or TV lessons"),
        ("teacher_guides", "Tablet or phone with lesson guides for teachers"),
        ("assessment_tools", "Assessment or quiz tools"), ("ai_tools", "AI tools (e.g. chatbots, AI tutors)"),
        ("projector", "Projector or interactive whiteboard"),
        ("gov_platform", "A government or ministry platform"), "None", "Other, please specify"],
        doc="B2", excl=["none"])
    f.matrix("B3_frequency", "In a typical school week, how often do you use digital tools for each of the following?", [
        ("B3_prep", "Preparing lessons (planning, making materials)"),
        ("B3_present", "Presenting in class (e.g. slides, video, projector, radio)"),
        ("B3_student_activities", "Activities students do themselves (apps, exercises, research)"),
        ("B3_assessment", "Assessment (quizzes, marking, feedback)"),
        ("B3_comm_admin", "Communication and admin (with students, parents, records)")],
        ["Never", "Occasionally", "Most days", ("every_lesson", "Every lesson / daily")], doc="B3")
    f.select_multi("B4_who_decides", "Who mainly decides which digital tools you use in class?", [
        ("ministry", "The ministry / government"), ("school_leadership", "My school leadership"),
        ("i_choose", "I choose myself"), ("ngo_donor", "An NGO or donor programme"),
        ("students_parents", "Students or parents bring their own"), ("mix", "A mix")],
        doc="B4", maxsel=2, excl=["mix"])
    f.select_multi("B5_student_devices", "What devices do your students mainly use for digital learning?", [
        ("school_computers", "School-provided computers or tablets"), ("own_smartphones", "Their own smartphones"),
        ("basic_phones", "Basic (non-smart) phones"), ("shared_school", "Shared devices at school"),
        ("family_phone", "A family member\u2019s phone"), ("own_home_computers", "Their own computers or tablets at home"),
        ("no_access", "Most students have no access to devices"), "Not applicable"],
        doc="B5", excl=["no_access", "not_applicable"])
    f.select_one("B6_electricity", "Does your school have reliable electricity?", [
        ("reliable_mains", "Yes, reliable mains power"), ("mains_cuts", "Mains power, but with frequent cuts"),
        ("solar_generator", "Solar or generator only"), ("none", "No electricity"), "Don't know"], doc="B6")
    f.select_one("B7_internet", "How reliable is internet access where you teach?", [
        ("no_access", "No access"), "Unreliable", "Mostly reliable", "Fully reliable"], doc="B7")
    f.select_one("B8_approved_tools", "Does your school or ministry recommend or approve specific digital tools for teaching?", [
        ("official_list", "Yes, there is an official list or platform"),
        ("informal", "Some tools are recommended informally"), "No", "Don't know"], doc="B8")
    f.end()

    f.begin("sec_C", "C. How well the tools fit your classroom", relevant="${consent_agreed}=\'yes\'")
    f.matrix("C1_fit", "Thinking about the digital tools you use, how much do you agree with each statement?", [
        ("C1_lang_teach", "The tools are available in the language I teach in."),
        ("C1_lang_home", "The tools work well in the language most of my students speak at home."),
        ("C1_curriculum", "The tools fit our national curriculum."),
        ("C1_assessment", "The tools fit the way students are assessed and examined."),
        ("C1_teaching_style", "The tools suit the way I teach."),
        ("C1_infrastructure", "The tools work with the devices, power and internet we actually have."),
        ("C1_context", "The examples and content assume a context that fits my students."),
        ("C1_control", "I can adjust or switch off what a tool does when I need to.")],
        AGREE5 + ["Not applicable"], doc="C1")
    f.select_multi("C2_misfit_reason", "When a tool does not fit your classroom well, what is usually the biggest reason?", [
        "Language", "Curriculum mismatch", "Assessment mismatch", "Cultural fit",
        ("infrastructure", "Power, internet or devices"), ("too_difficult", "Too difficult to use"), "Cost",
        ("fits_well", "They fit well / no problem"), "Other"], doc="C2", maxsel=2, excl=["fits_well"])
    f.select_multi("C3_trust", "When you decide whether a digital tool is worth using with your students, what makes you trust it most?", [
        ("ministry_approved", "It is recommended or approved by the ministry or my school"),
        ("peer_recommended", "Other teachers I know use it and recommend it"),
        ("seen_it_work", "I have tried it and seen it work with my students"),
        ("research_evidence", "Research or an evaluation shows it improves learning"),
        ("known_organisation", "It comes from a well-known company or organisation"),
        ("training_support", "It comes with training or support"), "Other"], doc="C3", maxsel=2)
    f.end()

    f.begin("sec_D", "D. Pressures in your teaching", relevant="${consent_agreed}=\'yes\'")
    f.select_multi("D1_pressures", "Which pressures in your teaching are most difficult right now?", [
        ("class_size", "Large class sizes"), ("workload_admin", "Heavy workload or admin"),
        ("mixed_levels", "A wide range of student levels in one class"),
        ("resources", "Limited resources or materials"), ("attendance", "Student attendance"),
        ("wellbeing_behaviour", "Student wellbeing or behaviour"), ("exam_prep", "Preparing students for exams"),
        "Other"], doc="D1", maxsel=2)
    f.select_one("D2_private_tutoring", "In your experience, roughly how many of your students also receive paid private tutoring or extra lessons outside school hours?",
                 ["Almost none", "Some", "About half", "Most", "Almost all", "Don't know"], doc="D2")
    f.select_one("D3_workload_effect", "Overall, do digital tools reduce or add to your workload?", [
        "Reduce it a lot", "Reduce it a little", "No difference", "Add a little", "Add a lot"], doc="D3")
    f.select_multi("D4_workload_parts", "Which parts of your workload are most affected by the use of digital tools?", [
        ("lesson_prep", "Lesson preparation"), ("marking", "Marking and feedback"),
        ("comm_admin", "Communication and admin"),
        ("learning_tools", "Learning to use the tools / technical problems"),
        ("required_platforms", "Keeping up with required platforms or reporting"),
        ("not_affected", "My workload is not substantially affected by digital technology")],
        doc="D4", excl=["not_affected"])
    f.end()

    f.begin("sec_E", "E. AI and your readiness to use digital tools", relevant="${consent_agreed}=\'yes\'")
    f.select_one("E1_ai_use", "Do you use AI tools such as ChatGPT, Gemini or Meta AI (for example in WhatsApp), or other AI tools made for teachers, in your teaching or preparation?",
                 ["Regularly", "Sometimes", "Tried once or twice", "Never"], doc="E1")
    f.select_one("E2_edu_ai_safer", "Some teachers feel AI tools made for education are safer or more appropriate for school than general ones like ChatGPT. How much do you agree?",
                 AGREE5 + ["Not sure"], doc="E2")
    f.select_one("E3_student_ai", "As far as you know, do your students use AI tools for their schoolwork?", [
        "Regularly", "Sometimes", "Rarely", ("not_that_i_know", "Not that I know of"), "Don't know"], doc="E3")
    f.select_one("E4_ai_languages", "When students use AI tools in a national or local language, how well do the tools handle it?", [
        "Well", "Adequately", "Poorly", ("use_major_language", "Students mostly use them in English, French or Portuguese instead"),
        "Don't know"], doc="E4")
    f.select_one("E5_confidence", "How confident do you personally feel using digital and AI tools in teaching?", [
        "Not at all", "A little", "Fairly confident", "Very confident"], doc="E5")
    f.select_one("E6_training", "Have you received any training or guidance on using digital or AI tools?", [
        ("yes_good", "Yes, good support"), ("yes_limited", "Yes, but limited"), ("no", "No")], doc="E6")
    f.select_multi("E6_who", "If yes, who provided it?", [
        ("ministry_school", "Ministry or school"), ("ngo_donor", "An NGO or donor programme"),
        ("tool_company", "The company that makes the tool"),
        ("self_taught", "I found it myself (online courses, videos)"), "Colleagues"],
        doc="E6 (follow-up)", relevant="${E6_training}='yes_good' or ${E6_training}='yes_limited'")
    f.select_one("E7_ai_rules", "Does your school or ministry have rules or guidance on using AI in the classroom?", [
        ("yes_clear", "Yes, and they are clear and followed"),
        ("yes_unclear", "Yes, but unclear or not followed in practice"), "No", "Don't know"], doc="E7")
    f.end()

    f.begin("sec_F", "F. Wellbeing and online safety", relevant="${consent_agreed}=\'yes\'")
    f.matrix("F1_observations", "Thinking about your students in general, how often do you observe the following?", [
        ("F1_tiredness", "Tiredness in class"), ("F1_concentration", "Difficulty concentrating or staying on task"),
        ("F1_anxiety", "Students seeming anxious or stressed"), ("F1_bullying", "Bullying between students (of any kind)")],
        ["Never", "Rarely", "Sometimes", "Often"], doc="F1")
    f.select_one("F2_phone_use", "As far as you know, how many of your students use a mobile phone or other device outside school on most days?",
                 ["Almost none", "Some", "About half", "Most", "Almost all", "Don't know"], doc="F2")
    f.select_one("F2_online_problems", "How often do problems that started online come up at school, for example bullying, or harmful or inappropriate content being shared?",
                 ["Never", "Rarely", "Sometimes", "Often", "Don't know"], doc="F2 (follow-up)",
                 relevant="${F2_phone_use} != '' and ${F2_phone_use} != 'almost_none'")
    f.select_one("F3_phone_wellbeing", "In your view, how do students\u2019 phones and other devices affect their wellbeing overall?", [
        ("mostly_positive", "Mostly positively"), ("both", "Both positively and negatively"),
        ("mostly_negative", "Mostly negatively"), ("no_effect", "No noticeable effect"), "Don't know"], doc="F3")
    f.select_one("F4_phone_rules", "Does your school have rules about phones or personal devices during the school day?", [
        ("not_allowed", "Phones not allowed at all"), ("certain_times", "Allowed only at certain times"),
        ("no_rules", "No rules"), "Don't know"], doc="F4")
    f.select_one("F5_restriction_effect", "If your school restricts phones, have you noticed a difference?", [
        ("positive", "Yes, a positive difference"), ("no_difference", "No difference"),
        ("harder", "It made things harder"), "Not applicable"], doc="F5")
    f.select_one("F6_wellbeing_considered", "When digital tools are chosen at your school, is students\u2019 wellbeing considered?",
                 ["Yes", "Sometimes", "No", "Don't know"], doc="F6")
    f.select_one("F7_report_harm", "If a student had a harmful experience linked to a digital tool (for example inappropriate content, bullying, or contact from a stranger), would you know how to report it?", [
        ("yes_procedure", "Yes, there is a school procedure"),
        ("yes_informal", "Yes, informally (e.g. I would tell the head teacher)"), "No", "Not applicable"], doc="F7")
    f.end()

    f.begin("sec_G", "G. Anything else", relevant="${consent_agreed}='yes'")
    f.text("G1_anything_else", "Is there anything about digital tools in your classroom that you think this review should understand?",
           doc="G1", hint="Optional. Please do not include your name, school name, or names of colleagues or students.",
           note="Free text; review and scrub any identifying details before sharing")
    f.select_one("G2_followup_optin",
                 "Would you be open to participating in future teacher focus groups or receiving a summary of this study's findings?",
                 [("yes", "Yes, I am open to follow-up"),
                  ("no", "No, keep this submission 100% anonymous without follow-up")],
                 doc="G2 (Opt-in)",
                 hint="Optional. If 'Yes', contact details are kept strictly detached from your classroom responses.")
    f.text("G2_contact_info",
           "Contact phone / WhatsApp or email (optional; kept separate from your answers)",
           doc="G2 (Contact)",
           relevant="${G2_followup_optin}='yes'",
           hint="Optional. Phone or email. Stored in a separate protected registry and never linked to survey data.",
           pii=True,
           note="Personal data; detached follow-up registry")
    f.note("thanks", "**Thank you. Your experience makes this review possible.**", relevant="${consent_agreed}='yes'")
    f.end()

    f.tests += [
        ("sec_A", "relevant", {"consent_agreed": "yes"}, None, True),
        ("sec_A", "relevant", {"consent_agreed": "no"}, None, False),
        ("sec_A", "relevant", {"consent_agreed": ""}, None, False),
        ("consent_declined", "relevant", {"consent_agreed": "no"}, None, True),
        ("consent_declined", "relevant", {"consent_agreed": "yes"}, None, False),
        ("consent_agreed", "constraint", {}, "yes", True),
        ("consent_agreed", "constraint", {}, "no", False),
        ("consent_agreed", "constraint", {}, "yes", True),
        ("consent_agreed", "constraint", {}, "no", False),
        ("consent_agreed", "constraint", {}, "yes", True),
        ("consent_agreed", "constraint", {}, "no", False),
        ("A11_gps_location", "relevant", {"A11_gps_consent": "yes"}, None, True),
        ("A11_gps_location", "relevant", {"A11_gps_consent": "no"}, None, False),
        ("G2_contact_info", "relevant", {"G2_followup_optin": "yes"}, None, True),
        ("G2_contact_info", "relevant", {"G2_followup_optin": "no"}, None, False),
        ("A1_region", "relevant", {"A1_country": "KEN"}, None, True),
        ("A1_region", "relevant", {"A1_country": ""}, None, False),
        ("B1_why_no", "relevant", {"B1_use_digital": "no"}, None, True),
        ("B1_why_no", "relevant", {"B1_use_digital": "yes"}, None, False),
        ("B1_why_no", "relevant", {"B1_use_digital": ""}, None, False),
        ("E6_who", "relevant", {"E6_training": "yes_good"}, None, True),
        ("E6_who", "relevant", {"E6_training": "yes_limited"}, None, True),
        ("E6_who", "relevant", {"E6_training": "no"}, None, False),
        ("E6_who", "relevant", {"E6_training": ""}, None, False),
        ("F2_online_problems", "relevant", {"F2_phone_use": "almost_none"}, None, False),
        ("F2_online_problems", "relevant", {"F2_phone_use": "some"}, None, True),
        ("F2_online_problems", "relevant", {"F2_phone_use": "dont_know"}, None, True),
        ("F2_online_problems", "relevant", {"F2_phone_use": ""}, None, False),
        ("B2_tools", "constraint", {}, "messaging sms", True),
        ("B2_tools", "constraint", {}, "none messaging", False),
    ]

    # review notes
    f.issue("Header", "Inconsistency", "The page header says 'Draft v1 \u00b7 25 Sept 2026' but the opening line says 'Draft v1 (28 September 2026)'. Align the dates.")
    f.issue("Intro", "Design decision", "The 'Language selector' line is not built as a question. Kobo lets respondents switch language from the form menu once translations exist (French and Portuguese later).")
    f.issue("Intro", "Implemented", "Explicit primary consent gate ('consent_agreed') added with required=yes. If declined, the survey terminates immediately to an exit note; all subsequent sections are skipped.")
    f.issue("A11", "Implemented", "GPS location capture is gated by an explicit sub-gate question ('A11_gps_consent'). If declined, geopoint widget is hidden. Coordinates are marked for meso-level administrative aggregation.")
    f.issue("G2", "Implemented", "Added optional follow-up opt-in ('G2_followup_optin' and 'G2_contact_info') with pii=True. Documented for decoupled storage away from classroom responses.")
    f.issue("A1", "Design decision", "Country list uses ISO3 codes as the stored values (e.g. KEN) so exports join directly to your dashboards. 'Other' is kept for respondents outside the 48 countries; filter these out in analysis if needed.")
    f.issue("B1\u2013B3", "Needs confirmation", "No skip logic from B1 'No' to B2/B3 (B2 has a 'None' option and B3 a 'Never' option, so they appear to be asked of everyone). If B2/B3 should be hidden for non-users, say so; it is a one-line change.")
    f.issue("F4\u2013F5", "Needs confirmation", "F5 ('If your school restricts phones...') is not gated by F4 because F5 has its own 'Not applicable' option. Say if you want it hidden when F4 = 'No rules'.")
    f.issue("D4", "Typo fixed", "'techology' corrected to 'technology' in the last D4 option.")
    f.issue("A4", "Needs confirmation", "'Spanish' appears in the lesson-language list but not in the survey's stated languages (English, French, Portuguese). Kept as written (relevant for Equatorial Guinea); confirm.")
    f.issue("All 'Other' options", "Design decision", "A 'Please specify' text box appears whenever 'Other' (or a named-language option) is selected. This was not in the Word version.")
    f.issue("Multi-selects", "Design decision", "Limits such as 'select up to two' are enforced, and 'None' / 'No access' / 'A mix' / 'They fit well' / 'Not applicable' cannot be combined with other answers. These were not enforced in the Word version.")
    f.issue("G1", "Privacy", "Free text may contain names or school details despite the anonymity promise. Review before publishing any quotes.")
    return f


# ============================================================ PROVIDER SURVEY
def build_provider():
    f = Form("ssa_provider_survey_v1_en", "SSA EdTech Landscape Review - Provider survey (EN, draft v1)",
             "provider_survey_v1_en")
    f._add(type="start", name="start")
    f._add(type="end", name="end")
    f._add(type="today", name="today")
    f.calc("instrument_version", "'provider_survey_v1_en'")
    f.begin("intro", "EdTech provider survey")
    f.note("intro_1", "**Sub-Saharan Africa EdTech Landscape Review: EdTech provider survey**")
    f.note("intro_2", "Thank you for taking part. This survey is part of the Sub-Saharan Africa EdTech Landscape Review, an independent study of how educational technology is meeting education needs across the region, carried out under the Global EdTech Alliance of Alliances.")
    f.note("intro_3", "We are inviting organisations that build, sell or deliver digital learning tools or services in Sub-Saharan Africa: companies, social enterprises, NGOs and public bodies alike. We want to understand how your products reach learners, what helps and what gets in the way, and what it would take to meet growing expectations on safety, data and evidence.")
    f.note("intro_4", "This is not an evaluation or a rating of your organisation. Your answers will be reported only in aggregate, and nothing will be attributed to your organisation. At the end you can choose, separately, whether we may contact you about a possible future directory of EdTech providers in the region; saying \u2018no\u2019 does not affect your participation.")
    f.note("intro_5", "The survey takes about 15 minutes. Every substantive question is optional. If you offer several products, please answer for your main product or service. Participation is completely voluntary.")
    f.select_one("consent_agreed",
                 "Do you agree to take part in this survey on behalf of your organisation under the terms described above?",
                 [("yes", "Yes, I agree to take part"),
                  ("no", "No, I do not wish to take part")],
                 doc="Consent Gate",
                 hint="Participation is voluntary. Answers are reported in aggregate only.",
                 required=True,
                 constraint=". = 'yes'",
                 cmsg="Submission is disabled because consent was declined. Please close your browser window without submitting.")
    f.note("consent_declined",
           "**Thank you for your time.** You have chosen not to participate, so no further survey questions will be shown. Please close this browser window without submitting (blank submissions are disabled).",
           relevant="${consent_agreed}='no'")
    f.end()

    f.begin("sec_A", "A. Your organisation", relevant="${consent_agreed}='yes'")
    f.text("A1_org_name", "Organisation name", doc="A1",
           hint="Optional. If provided, organisation name is stored in a separate directory index and decoupled from sensitive survey metrics.", pii=True,
           note="Identifies the organisation: strip before analytical dataset release")
    f.select_one("A2_hq_country", "In which country is your organisation headquartered?", WORLD,
                 doc="A2", appearance="autocomplete")
    f.select_one("A2_office_gps_consent",
                 "Are you willing to record your organisation's headquarters or regional office GPS coordinates?",
                 [("yes", "Yes, record office GPS coordinates"),
                  ("no", "No, skip GPS recording")],
                 doc="A2 (GPS Consent)",
                 hint="Optional. Used for regional EdTech ecosystem cluster mapping.")
    f.geopoint("A2_office_gps", "Organisation HQ or regional office GPS location (optional)", doc="A2 (GPS)",
               hint="Optional: Record office or hub GPS coordinates.",
               relevant="${A2_office_gps_consent}='yes'",
               note="Captures office/hub location")
    f.select_multi("A3_operate_countries", "In which Sub-Saharan African countries do you currently operate?",
                   SSA48, doc="A3")
    f.select_one("A4_org_type", "What type of organisation are you?", [
        ("for_profit", "For-profit company"), "Social enterprise", ("ngo", "NGO or non-profit"),
        ("public_body", "Public body or state-owned organisation"),
        ("university_research", "University or research institution"), "Other"], doc="A4")
    f.select_one("A5_origin_ownership", "Which best describes where your organisation was founded and who owns it?", [
        ("ssa_local", "Founded in Sub-Saharan Africa, mainly locally owned"),
        ("ssa_foreign_investment", "Founded in Sub-Saharan Africa, with significant foreign investment"),
        ("foreign_subsidiary", "Subsidiary or branch of an organisation based outside Sub-Saharan Africa"), "Other"], doc="A5")
    f.select_one("A6_founded", "When was your organisation founded?", [
        ("before_2010", "Before 2010"), ("2010_2015", "2010\u20132015"), ("2016_2020", "2016\u20132020"),
        ("2021_later", "2021 or later")], doc="A6")
    f.select_one("A7_staff", "Roughly how many people work for your organisation?", [
        ("1_10", "1\u201310"), ("11_50", "11\u201350"), ("51_200", "51\u2013200"), ("gt200", "More than 200")], doc="A7")
    f.end()

    f.begin("sec_B", "B. Your main product or service", relevant="${consent_agreed}=\'yes\'")
    f.select_multi("B1_main_function", "What does your main product or service mainly do?", [
        ("learner_content", "Learning content or apps for learners"), ("tutoring", "Tutoring or exam preparation"),
        ("teacher_tools", "Tools for teachers (lesson plans, coaching, classroom assessment)"),
        ("school_lms", "School or learning-management systems"), ("assessment_data", "Assessment, data or analytics"),
        ("skills_training", "Skills, vocational or workforce training"),
        ("hardware_connectivity", "Hardware, devices or connectivity"),
        ("radio_tv_media", "Content through radio, TV or recorded media"), "Other (please specify)"],
        doc="B1", maxsel=2)
    f.select_multi("B2_users", "Who are the main users?", [
        "Learners", "Teachers", ("school_leaders", "School leaders or administrators"),
        ("parents", "Parents or caregivers"), ("ministries", "Ministries or government"), "Other"], doc="B2")
    f.select_multi("B3_levels", "Which levels of education?", [
        ("early_years", "Early years (ages about 3 to 5)"), ("primary", "Primary (ages about 6 to 12)"),
        ("secondary", "Secondary (ages about 12 to 18)"), ("tvet", "Technical and vocational"),
        ("higher_ed", "Higher education"), ("adult_nonformal", "Adult or non-formal learning")], doc="B3")
    f.select_one("B4_active_users", "Roughly how many learners or users were active on your product in Sub-Saharan Africa in the past 12 months?", [
        ("lt1k", "Fewer than 1,000"), ("1k_10k", "1,000\u201310,000"), ("10k_100k", "10,001\u2013100,000"),
        ("100k_1m", "100,001\u20131 million"), ("gt1m", "More than 1 million"),
        ("dk_prefer_not", "Don't know / prefer not to say")], doc="B4")
    f.end()

    f.begin("sec_C", "C. How your product reaches users", relevant="${consent_agreed}=\'yes\'")
    f.select_multi("C1_channels", "Through which channels is your product delivered?", [
        ("smartphone_app", "Smartphone app"), ("web", "Web browser"), ("basic_phone", "Basic phone (SMS, USSD, voice)"),
        ("messaging_apps", "Messaging apps (e.g. WhatsApp, Telegram)"), ("radio_tv", "Radio or TV"),
        ("preloaded_offline", "Preloaded devices or offline servers"),
        ("print_plus_digital", "Printed materials combined with digital"), "Other"], doc="C1")
    f.select_one("C2_offline", "Can the core product be used without an internet connection?", [
        ("fully_offline", "Yes, fully offline"), ("partly", "Partly (it syncs when connected)"),
        ("needs_connection", "No, it needs a connection")], doc="C2")
    f.select_one("C3_min_device", "What is the minimum device a user needs?", [
        ("basic_phone", "A basic phone"), ("low_cost_smartphone", "A low-cost smartphone"),
        ("tablet_computer", "A tablet or computer"), ("supplied_device", "A dedicated device that we supply"),
        ("no_personal_device", "No personal device (e.g. radio or TV)")], doc="C3")
    f.select_one("C4_data_payer", "Who usually pays for the mobile data needed to use your product?", [
        ("users_pay", "Users pay"), ("zero_rated", "Free to users through a mobile operator arrangement (zero-rated)"),
        ("we_or_programme", "Covered by us or by a programme"),
        ("not_applicable", "Not applicable (offline or no data needed)")], doc="C4")
    f.select_multi("C5_mno", "Do you work with mobile network operators?", [
        ("commercial", "Yes, as commercial partners"), ("free_discounted", "Yes, for free or discounted access"),
        ("distribution_payment", "Yes, as a distribution or payment channel"), "No"], doc="C5", excl=["no"])
    f.end()

    f.begin("sec_D", "D. Languages and local fit", relevant="${consent_agreed}=\'yes\'")
    f.select_multi("D1_languages", "In which languages is your product available?", [
        "English", "French", "Portuguese", "Arabic", "Kiswahili", "Spanish",
        ("other", "Other national or local languages (please list)")], doc="D1",
        specify={"other": "Please list the other languages."})
    f.select_one("D2_curriculum", "Is your content aligned with national curricula?", [
        ("yes", "Yes (please name the countries)"), "Partly", ("not_specific", "Not curriculum-specific")], doc="D2",
        specify={"yes": "Please name the countries."})
    f.select_one("D3_adaptation", "When you enter a new country or language, who adapts the content?", [
        ("own_team", "Our own team"), ("local_partners", "Local partners"),
        ("government_schools", "The government or schools"), ("no_adaptation", "We do not adapt content"),
        "Not applicable"], doc="D3")
    f.end()

    f.begin("sec_E", "E. Business model and continuity", relevant="${consent_agreed}=\'yes\'")
    f.select_multi("E1_revenue", "What are your main sources of revenue or funding?", [
        ("families_pay", "Families or individual learners pay"), ("schools_pay", "Schools pay"),
        ("government_contracts", "Government contracts"), ("donor_grants", "Donor or philanthropic grants"),
        ("investors", "Investors (not yet generating revenue)"),
        ("corporate_sponsorship", "Corporate partners or sponsorship"), "Other"], doc="E1", maxsel=2)
    f.select_one("E2_route", "What is your main route to learners?", [
        ("direct_families", "Directly to families or learners"), ("selling_schools", "Selling to schools"),
        ("government", "Government procurement or partnership"), ("donor_ngo", "Through donor or NGO programmes"),
        ("mno_companies", "Through mobile operators or other companies"), ("not_school_focused", "Not school-focused")], doc="E2")
    f.select_one("E3_funding_ends", "If your main source of funding ended within the next year, what would most likely happen to your product?", [
        ("unchanged", "Continue largely unchanged"), ("reduced", "Continue in reduced form"),
        ("hand_over", "Hand over to a government or partner"), ("close_pause", "Close or pause"), "Don't know"], doc="E3")
    f.select_one("E4_data_portability", "If a school or ministry stopped using your product, could they take their data with them?", [
        ("yes_standard", "Yes, in a standard format"), ("yes_request", "Yes, on request"),
        ("no", "No, not currently"), ("no_data", "We hold no such data")], doc="E4")
    f.select_one("E5_support", "Do you provide training or ongoing support for teachers or schools using your product?", [
        ("included", "Yes, included"), ("extra_cost", "Yes, at extra cost"), ("guides_only", "Online guides only"),
        "No", "Not applicable"], doc="E5")
    f.end()

    f.begin("sec_F", "F. Data, safety and AI", relevant="${consent_agreed}=\'yes\'")
    f.select_one("F1_childrens_data", "Does your product collect personal data (for example, names, phone numbers, photos or voice recordings, location, device identifiers, or learning and assessment records linked to a named or numbered learner) about children (under 18)?",
                 ["Yes", "No", "Not sure"], doc="F1")
    f.select_one("F2_data_location", "Where is user data mainly stored?", [
        ("in_country", "In the country where the users are"), ("elsewhere_africa", "Elsewhere in Africa"),
        ("outside_africa", "Outside Africa"), ("no_personal_data", "We do not store personal data"), "Don't know"], doc="F2")
    f.select_one("F3_permission", "How do you obtain permission to collect children\u2019s data?", [
        ("parent_consent", "Consent from parents or guardians"),
        ("school_ministry_agreement", "Through an agreement with the school or ministry"),
        ("learner_consent", "The learner\u2019s own consent"), ("no_childrens_data", "We do not collect children\u2019s data"),
        ("other_or_not_sure", "Other or not sure")], doc="F3")
    f.select_one("F4_reporting", "Can users report harmful content, contact or behaviour in your product?", [
        ("in_product_team", "Yes, within the product, with a named team responding"),
        ("general_support", "Yes, through general customer support"), "No",
        ("not_applicable", "Not applicable (no user interaction)")], doc="F4")
    f.select_one("F5_ai_use", "Does your product use artificial intelligence (AI)?", [
        "No", ("planning", "Planning to"), ("yes_api", "Yes, using models from other companies (e.g. through an API)"),
        ("yes_adapted", "Yes, using models we have adapted or fine-tuned"), ("yes_own", "Yes, using our own models")], doc="F5")
    ai_rel = "${F5_ai_use}='yes_api' or ${F5_ai_use}='yes_adapted' or ${F5_ai_use}='yes_own'"
    f.select_multi("F5_ai_types", "If yes, which of the following does your product use?", [
        ("generative", "Generative AI: produces text, images, audio or conversational responses (e.g. a chatbot or content generator)"),
        ("other_ml", "Other AI or machine learning: e.g. predicting performance, recommending content, speech recognition, automated marking"),
        ("rule_based", "Rule-based adaptation: content adjusts by pre-set rules, without machine learning"),
        ("none_of_these", "None of these")], doc="F5 (follow-up)", relevant=ai_rel, excl=["none_of_these"])
    f.select_multi("F5_ai_role", "If AI is used, what does the AI do?", [
        ("generates_content", "Generates content"), ("tutors_chats", "Tutors or chats with learners"),
        ("marks_feedback", "Marks work or gives feedback"),
        ("recommends_paths", "Recommends or personalises learning paths"),
        ("supports_teachers", "Supports teachers (e.g. planning)"), ("translation_speech", "Translation or speech"),
        ("admin_analytics", "Administration or analytics"), "Other", "Don\u2019t know"],
        doc="F5 (follow-up)", relevant=ai_rel, excl=["dont_know"])
    f.select_one("F5_learner_interaction", "Do learners interact directly with the AI?", [
        "Yes", ("teacher_supervised", "Only under teacher supervision"), "No"], doc="F5 (follow-up)", relevant=ai_rel)
    f.end()

    f.begin("sec_G", "G. Evidence and recognition", relevant="${consent_agreed}=\'yes\'")
    f.select_multi("G1_evidence", "What evidence do you have that your product achieves what it aims to?", [
        ("usage_data", "Usage and engagement data"), ("user_feedback", "User feedback or surveys"),
        ("own_outcome_study", "Our own study of learning outcomes"), ("independent_evaluation", "An independent evaluation"),
        ("rct_comparison", "A randomised or comparison-group impact study"), ("none_yet", "None yet"), "Other"],
        doc="G1", excl=["none_yet"])
    f.select_one("G2_government", "Have you worked with a government education authority in Sub-Saharan Africa (e.g. a pilot, contract or endorsement)?", [
        ("yes_national", "Yes, at national level"), ("yes_regional", "Yes, at regional or local level"),
        ("pilot_only", "Pilot only"), "No"], doc="G2")
    f.select_one("G3_disability_testing", "Has your product been tested with users with disabilities?",
                 ["Yes", "Partly", "No", "Don't know"], doc="G3")
    f.select_one("G4_certification", "Do you hold any external certification or recognition related to education quality, data protection, accessibility or public-good status (e.g. Digital Public Good)?", [
        ("yes", "Yes (please name)"), "No", "Don't know"], doc="G4", specify={"yes": "Please name the certification or recognition."})
    f.end()

    f.begin("sec_H", "H. Standards and requirements", relevant="${consent_agreed}=\'yes\'")
    f.begin("H1_familiarity", "How familiar are you with the following?", appearance="field-list")
    fam = ["Never heard of it", "Heard of it", "Have looked at it", "Have applied or been assessed"]
    f._cur_doc = "H1"
    ln = f.lst(fam, "h1_framework")
    f._add(type="select_one " + ln, name="H1_framework", label="UNICEF\u2019s EdTech for Good Framework: a published framework for assessing whether digital learning tools are safe, effective and appropriate")
    f._log("H1", "H1_framework", "select_one", ln)
    ln2 = f.lst(fam + [("listed", "Our product is listed")], "h1_cabinet")
    f._add(type="select_one " + ln2, name="H1_cabinet", label="The Learning Cabinet: an online catalogue, hosted by UNICEF with partners, of EdTech tools that have been through that assessment")
    f._log("H1", "H1_cabinet", "select_one", ln2, note="Extra option 'Our product is listed' applies to the Learning Cabinet only")
    f.end()
    f.select_multi("H2_hardest", "If governments or funders asked you to meet international requirements for safe and effective EdTech, which would be hardest for your organisation?", [
        ("learning_evidence", "Independent evidence of learning impact"),
        ("data_protection_docs", "Documenting data-protection practices"),
        ("safeguarding", "Safeguarding and reporting processes"), ("accessibility", "Accessibility testing"),
        ("ai_documentation", "Documenting how AI features work and their limits"),
        ("none_difficult", "None of this would be difficult"), "I am not sure"],
        doc="H2", maxsel=3, excl=["none_difficult", "not_sure"])
    f.select_multi("H3_reasons", "If you feel these may be difficult, what are the main reasons?", [
        ("cost", "The cost of assessment or application"), ("staff_capacity", "Staff time and capacity"),
        ("language", "Application processes only in English or another language we do not work in"),
        ("none_difficult", "None would be difficult"), "Don't know"],
        doc="H3", maxsel=2, excl=["none_difficult", "dont_know"],
        relevant="${H2_hardest} != '' and not(selected(${H2_hardest}, 'none_difficult')) and not(selected(${H2_hardest}, 'not_sure'))",
        note="Numbered H3 in the Word file; the next question is also numbered H3 (here H4)")
    f.select_one("H4_requirements_bias", "How much do you agree: \u201cInternational quality requirements for EdTech are designed with large international providers in mind.\u201d",
                 AGREE5 + ["No view"], doc="H3 (second)", note="Second question numbered H3 in the Word file")
    f.end()

    f.begin("sec_I", "I. Barriers to growth", relevant="${consent_agreed}=\'yes\'")
    f.top3("I1_barriers", "What are the biggest barriers to your product reaching more learners in Sub-Saharan Africa?", [
        ("finance", "Access to finance"), ("procurement", "Government procurement processes"),
        ("infrastructure", "Infrastructure (power, connectivity, devices)"),
        ("families_pay", "Families\u2019 ability to pay"), ("schools_pay", "Schools\u2019 ability to pay"),
        ("evidence_reqs", "Evidence requirements"), ("regulation", "Regulation or licensing"),
        ("localisation_cost", "Cost of language and local adaptation"),
        ("free_global_tools", "Competition from free global tools"), ("skilled_staff", "Finding skilled staff"),
        "Other (please specify)"], doc="I1")
    f.end()

    f.begin("sec_J", "J. Final questions", relevant="${consent_agreed}='yes'")
    f.text("J1_anything_else", "Is there anything else about EdTech in Sub-Saharan Africa that you think this review should understand?",
           doc="J1", hint="Optional. Please do not include sensitive proprietary secrets or identifiable personal names.")
    f.select_one("J2_directory_contact", "We may later develop a public directory of EdTech providers in the region. May we contact you about listing your organisation? Your answers to this survey will not be published in any directory.",
                 ["Yes", "No"], doc="J2")
    f.text("J2_contact_email", "Contact email", doc="J2", relevant="${J2_directory_contact}='yes'", pii=True,
           hint="Corporate or representative email address. Stored in directory vault separately from responses.",
           note="Personal data")
    f.select_one("J3_interview", "Would you be willing to take part in a short interview or focus group?",
                 ["Yes", "No"], doc="J3")
    f.text("J3_contact", "Contact", doc="J3", relevant="${J3_interview}='yes'", pii=True,
           hint="Name and email/phone. Kept strictly detached from survey data.",
           note="Personal data")
    f.note("thanks", "**Thank you for contributing to this review.**", relevant="${consent_agreed}='yes'")
    f.end()

    f.tests += [
        ("sec_A", "relevant", {"consent_agreed": "yes"}, None, True),
        ("sec_A", "relevant", {"consent_agreed": "no"}, None, False),
        ("consent_declined", "relevant", {"consent_agreed": "no"}, None, True),
        ("consent_declined", "relevant", {"consent_agreed": "yes"}, None, False),
        ("A2_office_gps", "relevant", {"A2_office_gps_consent": "yes"}, None, True),
        ("A2_office_gps", "relevant", {"A2_office_gps_consent": "no"}, None, False),
        ("F5_ai_types", "relevant", {"F5_ai_use": "no"}, None, False),
        ("F5_ai_types", "relevant", {"F5_ai_use": "planning"}, None, False),
        ("F5_ai_types", "relevant", {"F5_ai_use": "yes_api"}, None, True),
        ("F5_ai_role", "relevant", {"F5_ai_use": "yes_own"}, None, True),
        ("F5_ai_role", "relevant", {"F5_ai_use": ""}, None, False),
        ("F5_learner_interaction", "relevant", {"F5_ai_use": "yes_adapted"}, None, True),
        ("H3_reasons", "relevant", {"H2_hardest": "learning_evidence"}, None, True),
        ("H3_reasons", "relevant", {"H2_hardest": "learning_evidence accessibility"}, None, True),
        ("H3_reasons", "relevant", {"H2_hardest": "none_difficult"}, None, False),
        ("H3_reasons", "relevant", {"H2_hardest": "not_sure"}, None, False),
        ("H3_reasons", "relevant", {"H2_hardest": ""}, None, False),
        ("J2_contact_email", "relevant", {"J2_directory_contact": "yes"}, None, True),
        ("J2_contact_email", "relevant", {"J2_directory_contact": "no"}, None, False),
        ("J3_contact", "relevant", {"J3_interview": "yes"}, None, True),
        ("J3_contact", "relevant", {"J3_interview": ""}, None, False),
    ]

    f.issue("Header", "Inconsistency", "Header says 'Draft v1 \u00b7 25 Sept 2026' but the opening line says 28 September 2026. Align the dates.")
    f.issue("H3", "Numbering error", "Two questions are numbered H3 in the Word file (the 'difficult reasons' question and the 'international requirements' agreement statement). Built as H3 (reasons) and H4 (agreement); please renumber the Word version to match.")
    f.issue("H3", "Logic", "H3 (reasons) is shown only if H2 includes a real difficulty (not 'None of this would be difficult' or 'I am not sure'), so its own 'None would be difficult' option is redundant. Confirm whether to keep it.")
    f.issue("H1", "Design decision", "Split into two questions because the 'Our product is listed' answer applies to the Learning Cabinet only.")
    f.issue("F5", "Design decision", "'Planning to' is treated as not currently using AI, so the three AI follow-ups appear only for the three 'Yes' answers.")
    f.issue("I1", "Design decision", "Ranking is three sequential questions (1st/2nd/3rd) with duplicate prevention. Analysis columns: I1_barriers_1, _2, _3.")
    f.issue("Intro", "Implemented", "Explicit primary consent gate ('consent_agreed') added with required=yes. Gating sections A through J.")
    f.issue("A2 (GPS)", "Implemented", "Organisation office GPS capture is gated by explicit consent ('A2_office_gps_consent').")
    f.issue("A1, J2, J3", "Privacy & Decoupling", "Organisation name ('A1_org_name') and contact fields ('J2_contact_email', 'J3_contact') are flagged with pii=True. Maintained in the decoupled contact directory protocol to ensure survey responses remain aggregate-only.")
    f.issue("A2", "Design decision", "The 'all countries' dropdown is a typed 193-country UN list plus four additions (Holy See, Palestine, Taiwan, Kosovo) and 'Other / not listed'. Check it against your preferred country list.")
    f.issue("A4/D1", "Needs confirmation", "'Spanish' appears among product languages as in the Word file; confirm it is intended.")
    f.issue("All 'Other' options", "Design decision", "A 'Please specify' text box appears when 'Other' is selected, and where the Word file said 'please name/list' (D1, D2, G4).")
    return f


# ============================================================ EXPERT CONSULTATION
def build_expert():
    f = Form("ssa_expert_consultation_r1_v1_en",
             "SSA EdTech Landscape Review - Expert consultation, Round 1 (EN, draft v1)",
             "expert_consultation_r1_v1_en")
    f._add(type="start", name="start")
    f._add(type="end", name="end")
    f._add(type="today", name="today")
    f.calc("instrument_version", "'expert_consultation_r1_v1_en'")
    f.begin("intro", "Expert Consultation, Round 1")
    f.note("intro_1", "**Sub-Saharan Africa EdTech Landscape Review: Expert Consultation, Round 1**")
    f.note("intro_2", "This short consultation is the first round of a two-round expert exercise informing the Sub-Saharan Africa EdTech Landscape Review, a scoping study of how educational technology (EdTech) is meeting education needs across the region. It is part of a series of regional reviews carried out under the Global EdTech Alliance of Alliances.")
    f.note("intro_3", "A good deal is already documented about EdTech in Sub-Saharan Africa: evidence on what improves learning, gaps in electricity and connectivity, and which countries have national strategies. We are not asking you to repeat that. We are asking for your judgement where the evidence seems to be thinner, uneven or possibly disputed: how decisions about EdTech are actually made, what lasts, and what it would take to use technology safely and responsibly in the systems you know.")
    f.note("intro_4", "Please answer for one national education system only, the one you know best. This can be a country, or a region or state within it. You may add a second system if you wish. Every question has a \u201cno view\u201d option and skipping is fine. Your answers are anonymous. In Round 2 you will see how the panel responded, including anonymised reasons behind strongly divergent views, and you can reconsider your answers. The aim is not to force agreement: where experts continue to disagree, that disagreement is a valuable finding.")
    f.note("intro_5", "The value of this review rests on the judgement of a relatively small number of people who truly know these systems and your insight would make a real difference. This round takes about 25\u201330 minutes.")
    f.select_one("consent_agreed",
                 "Do you agree to participate in this expert consultation panel under the terms outlined above?",
                 [("yes", "Yes, I agree to participate"),
                  ("no", "No, I do not wish to participate")],
                 doc="Consent Gate",
                 hint="Participation is voluntary. Expert responses are anonymised prior to Round 2 Delphi sharing.",
                 required=True,
                 constraint=". = 'yes'",
                 cmsg="Submission is disabled because consent was declined. Please close your browser window without submitting.")
    f.note("consent_declined",
           "**Thank you for your time.** You have chosen not to participate, so no further consultation questions will be shown. Please close this browser window without submitting (blank submissions are disabled).",
           relevant="${consent_agreed}='no'")
    f.end()

    conf = lambda n, doc: f.select_one(n, "Confidence", CONF, doc=doc)

    f.begin("sec_A", "Section A. About you", relevant="${consent_agreed}='yes'")
    f.note("A_intro", "Answers in this section are used only to group responses and are fully anonymised.")
    f.select_one("A1_system", "Which education system will you answer for? Please choose the one you know best.",
                 SSA48, doc="A1", appearance="minimal")
    f.text("A1_region", "If your answers apply mainly to one region, state or province, please name it (optional):",
           doc="A1", hint="Provide province, state, or county name only (optional). Avoid specific village or personal details.",
           relevant="${A1_system} != ''")
    f.select_one("A1_expert_gps_consent",
                 "Are you willing to share your current office or institutional GPS coordinates?",
                 [("yes", "Yes, record GPS coordinates"),
                  ("no", "No, skip GPS recording")],
                 doc="A1 (GPS Consent)",
                 hint="Optional. Used to evaluate geographic coverage of the expert panel across SSA.")
    f.geopoint("A1_expert_gps", "Current location / office GPS (optional)", doc="A1 (GPS)",
               hint="Optional: Record your current location.",
               relevant="${A1_expert_gps_consent}='yes'",
               note="Geographic location of expert respondent")
    f.select_one("A2_second_system", "Is there a second system you know well and would like to comment on? (optional)",
                 SSA48 + [("NONE", "No second system")], doc="A2", appearance="minimal")
    f.select_one("A3_based", "Where are you mainly based?", [
        ("in_country", "In the country I am answering for"), ("elsewhere_africa", "Elsewhere in Africa"),
        ("outside_africa", "Outside Africa")], doc="A3")
    f.select_one("A3_work_type", "If you are not based in that country, how would you describe your work in that system?", [
        ("sustained", "Sustained work on the ground (several years, or ongoing)"),
        ("periodic", "Periodic projects or visits"), ("documents", "Mainly through research or documents")],
        doc="A3 (follow-up)", relevant="${A3_based}='elsewhere_africa' or ${A3_based}='outside_africa'")
    f.select_multi("A4_perspective", "Which perspective best describes your vantage point?", [
        ("policy", "Policy / ministry / regulator"), ("provision", "EdTech provision (building or selling tools)"),
        ("mno", "Mobile network or telecoms operator"), ("research", "Research / academia"),
        ("ngo_delivery", "NGO or agency delivery (incl. education in emergencies)"),
        ("donor", "Donor, funder or development partner"), ("ecosystem", "Ecosystem (accelerator, hub, association)"),
        ("school", "School leadership or teaching"), "Other (please specify)"], doc="A4")
    f.select_one("A5_years", "Roughly how many years have you worked on education and/or EdTech in this system?", [
        ("lt2", "Less than 2"), ("2_5", "2\u20135"), ("6_10", "6\u201310"), ("gt10", "More than 10")], doc="A5")
    f.end()

    f.begin("sec_B", "Section B. What counts as EdTech, and how it is adopted", relevant="${consent_agreed}=\'yes\'")
    f.select_multi("B1_definition", "There is no agreed definition of \u201cEdTech\u201d. Which of the following should a review like this count as EdTech in the system you answer for?", [
        ("lms", "Learning or school management systems (e.g. a learning platform, a school information system)"),
        ("digital_content", "Digital content from publishers or the ministry"),
        ("family_apps", "Learning apps that families use directly"), ("radio_tv", "Radio, TV or recorded lessons"),
        ("sms_voice", "SMS, USSD, voice or other basic-phone services"),
        ("messaging", "Learning through messaging apps (e.g. WhatsApp groups or chatbots)"),
        ("teacher_tools", "Tools for teachers (e.g. tablets or phones with lesson guides, coaching apps)"),
        ("tutoring", "Private tutoring or exam-preparation platforms"),
        ("skills", "Skills or upskilling platforms for young people and adults"),
        ("general_productivity", "General productivity tools used in schools but not built for education (e.g. Google Workspace, Microsoft Teams, Zoom)"),
        ("general_ai", "General AI tools (e.g. ChatGPT, Gemini, Meta AI)"),
        ("hardware_connectivity", "Hardware and connectivity programmes (devices, solar power, school connectivity)"),
        "Other (please name)"], doc="B1")
    f.top3("B2_decision_drivers", "In the system you answer for, who in practice drives decisions about which EdTech reaches public schools?", [
        ("ministry", "Ministry of education or national agency"),
        ("other_gov", "Other government bodies (e.g. ICT ministry, regulator)"),
        ("regional_local_gov", "Regional or local government"), ("schools_heads", "Schools and head teachers"),
        ("donors", "Donors, development banks or international agencies"),
        ("ngos", "NGOs and implementing organisations"), ("edtech_companies", "EdTech companies"),
        ("mno_bigtech", "Mobile network operators or large technology companies"),
        ("parents", "Parents and households"), "Other (please specify)"], doc="B2")
    f.select_multi("B2_who_pays", "And whose money mainly pays for it?", [
        ("national_gov", "National government"), ("regional_local_gov", "Regional or local government"),
        ("school_budgets", "Schools\u2019 own budgets (incl. grants, fees or parent contributions)"),
        ("donors", "Donors, development banks or international agencies"),
        ("companies_mno", "Companies or mobile operators (e.g. free or sponsored provision)"),
        ("families", "Families directly")], doc="B2 (follow-up)", maxsel=2)
    conf("B2_confidence", "B2 (follow-up)")
    f.text("B2_private_schools", "Is this different for private or low-fee private schools? If so, how?",
           doc="B2 (follow-up)", hint="Optional.")
    f.select_one("B3_after_pilots", "When donor- or pilot-funded EdTech initiatives come to an end in the system you answer for, what typically happens?", [
        ("sustained", "Absorbed and sustained by the system"), ("reduced", "Continues in reduced form"),
        ("taken_over", "Taken over by a company or another funder"), "Stops", "Varies widely", "No view"], doc="B3")
    f.select_multi("B3_end_causes", "Apart from funding ending, what most often brings initiatives to an end?", [
        ("change_government", "A change of government or minister"),
        ("lost_champion", "Loss of a key champion in the ministry"),
        ("turnover_training", "Staff turnover, or training not sustained"),
        ("equipment_not_replaced", "Equipment breaks down and is not replaced"),
        ("running_costs", "Running costs (data, electricity, licences) not budgeted"),
        ("policy_curriculum_change", "A policy or curriculum change"), "Other (please specify)", "No view"],
        doc="B3 (follow-up)", maxsel=2, excl=["no_view"])
    f.text("B3_what_lasts", "What distinguishes the initiatives that do last?", doc="B3 (follow-up)", hint="Optional.")
    f.select_multi("B4_procurement", "Where public bodies buy or adopt EdTech in the system you answer for, where does the process most often break down?", [
        ("needs_undefined", "Needs are not clearly defined before buying"),
        ("procurement_expertise", "Limited procurement expertise, or unclear rules"),
        ("supplier_transparency", "Supplier selection lacks transparency"),
        ("delays", "Long delays in approval or payment"),
        ("no_school_testing", "Decisions are made centrally without testing in schools"),
        ("no_running_budget", "No budget for maintenance, training or running costs"),
        ("no_evaluation", "Little or no evaluation after adoption"),
        ("outside_government", "Most purchasing happens outside government (donors, NGOs)"), "No view"],
        doc="B4", maxsel=3, excl=["no_view"])
    f.end()

    f.begin("sec_C", "Section C. Fit with languages, curricula and classrooms", relevant="${consent_agreed}=\'yes\'")
    f.select_multi("C1_misfit", "Where is the sharpest misfit between the tools in use and local classrooms?", [
        ("language_instruction", "Language of instruction"), ("home_languages", "Learners\u2019 home languages"),
        ("curriculum_exam", "Curriculum and exam alignment"),
        ("infrastructure_assumptions", "Assumptions about devices, power or connectivity"),
        ("teaching_approach", "The teaching approach built into the tool"),
        ("cultural_fit", "Cultural fit of content and examples"), ("cost", "Cost to schools or families"),
        "Other (please specify)"], doc="C1")
    f.select_one("C2_adaptation", "How much genuine local adaptation of tools is happening?", [
        "Almost none", ("superficial", "Mostly superficial (translation only)"), ("some", "Some genuine adaptation"),
        "Substantial", "No view"], doc="C2")
    f.text("C2_example", "Can you give an example of real adaptation and what made it possible, or of problems caused by a tool that was not adapted?",
           doc="C2 (follow-up)", hint="Optional.")
    f.matrix("C3_ai_readiness", "For use in education, how close are AI tools to being genuinely usable in each of the following?", [
        ("C3_official_language", "The main official language of instruction in your system"),
        ("C3_early_grade_languages", "The national or local languages used in the early grades"),
        ("C3_home_languages", "Learners\u2019 home languages more widely"),
        ("C3_classrooms", "Actual classrooms in your system (working and in use, not just technically capable)")],
        ["Far off", "Some way off", "Nearly there", "Already adequate", "No view"], doc="C3")
    f.text("C3_obstacle", "What is the main obstacle to getting from capable AI models to tools that work in classrooms?",
           doc="C3 (follow-up)", hint="Optional.")
    c4_list = [
        ("supporting_teachers", "Supporting existing teachers (e.g. lesson guides, coaching, professional development)"),
        ("training_new", "Helping train or qualify new teachers"),
        ("enabling_less_qualified", "Enabling less-qualified or community teachers to teach (e.g. scripted lessons)"),
        ("reaching_no_teacher", "Reaching learners who have no teacher available (e.g. radio, self-study apps, AI tutors)"),
        ("adding_workload", "Adding to teachers\u2019 workload without easing the shortage"),
        ("drawing_funding", "Drawing funding or attention away from recruiting and paying teachers"),
        ("little_or_no_role", "Little or no role"), "No view"]
    f.select_multi("C4_teacher_shortage", "Many education systems face serious shortages of qualified teachers. In the system you answer for, what role is EdTech actually playing in relation to this?",
                   c4_list, doc="C4", excl=["little_or_no_role", "no_view"])
    f.select_one("C4_main_role", "And which of these should be EdTech\u2019s main role in your system?", [
        ("supporting_teachers", "Supporting existing teachers (e.g. lesson guides, coaching, professional development)"),
        ("training_new", "Helping train or qualify new teachers"),
        ("enabling_less_qualified", "Enabling less-qualified or community teachers to teach (e.g. scripted lessons)"),
        ("reaching_no_teacher", "Reaching learners who have no teacher available (e.g. radio, self-study apps, AI tutors)"),
        "No view"], doc="C4 (follow-up)", hint="Select one.",
        note="Answer options not given in the Word file: assumed to be the four supportive roles + No view")
    conf("C4_confidence", "C4 (follow-up)")
    f.end()

    f.begin("sec_D", "Section D. Conditions for safe and responsible use", relevant="${consent_agreed}=\'yes\'")
    f.note("D_intro", "International frameworks now describe what responsible EdTech should look like: how children\u2019s data are handled, how learners are kept safe, what evidence of learning is needed, and who might be excluded. The questions below ask something different: in the system you know, could these things actually be checked today and if so by whom?")
    areas = [
        ("a", "How the product collects, stores and shares children\u2019s data"),
        ("b", "Whether there is a working way to report and follow up harm linked to a digital tool (e.g. through the school, a helpline or child-protection services)"),
        ("c", "Whether the product\u2019s claims about improving learning are backed by evidence"),
        ("d", "How any AI features work, where they fail and whether people can oversee and correct them"),
        ("e", "Whether the product fits the national curriculum and the languages of instruction"),
        ("f", "Whether the product works with local power, connectivity, devices and existing systems"),
        ("g", "Whether learners with disabilities can use it and who else might be excluded"),
        ("h", "Whether teachers will get the training and support the product needs"),
        ("i", "Who is behind the product (ownership, funding) and what happens to schools and their data if it ends")]
    f.matrix("D1_checkable", "In the system you answer for, could each of the following be checked for an EdTech product today?",
             [("D1_" + k, "%s. %s" % (k, t)) for k, t in areas],
             ["Routinely", ("some", "For some products or parts of the system"),
              ("outside_support", "Only with outside support"), ("not_at_present", "Not at present"), "Don't know"],
             doc="D1")
    f.begin("D2_checkers", "For the same list (a\u2013i), who would realistically do the checking?", appearance=None)
    f._cur_doc = "D2"
    who = [("provider_self", "The provider itself (self-declaration only)"),
           ("ministry", "Ministry or government agency"),
           ("regulator", "Independent regulator (e.g. data protection authority)"),
           ("university", "University or research body"), ("schools_local", "Schools or local education offices"),
           ("donor_intl", "Donor or international organisation"), ("no_one", "No one at present")]
    for k, t in areas:
        f.select_multi("D2_" + k, "%s. %s" % (k, t), who, doc="D2", excl=["no_one"],
                       hint="Select all that apply for this row.")
    f.end()
    gap_rel = " or ".join("${D1_%s}='outside_support' or ${D1_%s}='not_at_present'" % (k, k) for k, _ in areas)
    f.select_multi("D3_constraints", "Where you answered \u201conly with outside support\u201d or \u201cnot at present\u201d in D1, what are the main constraints?", [
        ("no_mandate", "No legal mandate or rules"), ("no_body", "No body responsible"),
        ("no_expertise", "Lack of technical expertise"), ("no_funding", "No funding"),
        ("not_priority", "Not a political priority"), ("changes_government_staff", "Changes of government or staff"),
        ("language_capacity", "Language or translation capacity"),
        ("info_abroad", "Information is held by providers abroad"), "Other (please specify)"],
        doc="D3", maxsel=3, relevant=gap_rel)
    f.select_one("D3_most_urgent", "Which one of the areas a\u2013i is the most urgent gap in your system?",
                 [(k, "%s. %s" % (k, t)) for k, t in areas], doc="D3 (follow-up)", hint="Select one.", relevant=gap_rel)
    f.select_one("D4_evidence_level", "If the ministry required evidence before adopting an EdTech product, which level would be realistic without shutting out local providers?", [
        ("description", "A clear description of what the product does and why it should work"),
        ("use_evidence", "Evidence from use (e.g. usage data, teacher feedback, a pilot report)"),
        ("independent_eval", "An independent evaluation in comparable settings"),
        ("rigorous_impact", "A rigorous impact study (e.g. a randomised trial)"), "No view"], doc="D4")
    f.matrix("D4_agree", "How much do you agree with each statement?", [
        ("D4_agree_i", "(i) Strict international evidence requirements would favour large international providers over local ones."),
        ("D4_agree_iii", "(iii) Evidence produced in other countries is usually enough to judge whether a product will work here.")],
        AGREE5 + ["No view"], doc="D4 (follow-up)",
        note="Word file labels the statements (i) and (iii); there is no (ii)")
    f.select_one("D5_ai_oversight", "Think about how AI is currently used in schools in the system you answer for: by teachers, by learners, or built into products. Which best describes oversight at present?", [
        ("no_guidance", "There is no specific guidance or oversight yet"),
        ("guidance_unused", "Guidance exists but is not applied in practice"),
        ("guidance_inconsistent", "Guidance is not applied consistently"),
        ("broadly_covered", "Oversight broadly covers the ways AI is used in schools"),
        ("ai_not_used_enough", "AI is not yet used enough in schools for this to matter"), "No view"],
        doc="D5", hint="Choose one.")
    f.select_one("D5_biggest_gap", "If there are gaps, where is the biggest one?", [
        ("no_one_responsible", "No one is responsible for it"),
        ("no_expertise", "Those responsible lack technical expertise"),
        ("personal_phones", "Most AI use happens on personal phones, outside school systems"),
        ("built_in_unreviewed", "AI is built into products that are bought or donated without review"), "Other"],
        doc="D5 (follow-up)", hint="Select one.",
        relevant="${D5_ai_oversight}='no_guidance' or ${D5_ai_oversight}='guidance_unused' or ${D5_ai_oversight}='guidance_inconsistent'")
    conf("D5_confidence", "D5 (follow-up)")
    f.matrix("D6_familiarity", "How familiar are you with the following?", [
        ("D6_framework", "UNICEF\u2019s EdTech for Good Framework: a published framework for assessing whether digital learning tools are safe, effective and appropriate"),
        ("D6_cabinet", "The Learning Cabinet: an online catalogue, hosted by UNICEF with partners, of EdTech tools that have been through that assessment")],
        ["Never heard of it", "Heard of it", "Have looked at it", ("used", "Have used it in a decision or project")], doc="D6")
    f.select_one("D6_own_list", "Does the system you answer for have its own list, standard or approval process for EdTech?", [
        ("yes_formal", "Yes, formal and used"), ("yes_unused", "Yes, but not used in practice"),
        ("informal", "Informal practices only"), "No", "Don't know"], doc="D6 (follow-up)")
    f.text("D6_name", "If yes, please name it:", doc="D6 (follow-up)",
           relevant="${D6_own_list}='yes_formal' or ${D6_own_list}='yes_unused'")
    f.end()

    f.begin("sec_E", "Section E. Learner wellbeing", relevant="${consent_agreed}=\'yes\'")
    f.select_one("E1_wellbeing_design", "How much do you agree that EdTech providers active in your system meaningfully design for learner wellbeing (e.g. avoiding addictive features, protecting learners from harmful content or contact), rather than only claiming to?",
                 AGREE5 + ["No view", ("cant_evidence", "Can\u2019t be evidenced either way")], doc="E1")
    conf("E1_confidence", "E1 (follow-up)")
    f.text("E1_comment", "Please comment or give examples:", doc="E1 (follow-up)", hint="Optional.")
    f.select_one("E2_agenda", "How prominent are concerns about screen time, online harm or phone use in education debates in your system?", [
        ("not_on_agenda", "Not on the agenda"), ("discussed_not_acted", "Discussed but not acted on"),
        ("some_action", "Some policy or school action (e.g. rules on phones)"),
        ("major_priority", "A major policy priority"), "No view"], doc="E2")
    f.text("E2_examples", "Examples you are aware of:", doc="E2 (follow-up)", hint="Optional.")
    f.end()

    f.begin("sec_F", "Section F. Specific questions", relevant="${consent_agreed}=\'yes\'")
    f.top3("F1_constraints", "What are the biggest constraints on EdTech reaching learners in public schools in your system?", [
        "Electricity", ("connectivity", "Internet connectivity"), ("data_cost", "Cost of data"), "Devices",
        ("maintenance", "Maintenance and repair"), ("security_theft", "Security or theft of equipment"),
        ("teacher_capacity", "Teacher capacity"), ("language_content", "Content in the right language"),
        "Other (please specify)"], doc="F1")
    f.matrix("F2_lesson_guides", "Tools that give teachers structured lesson guides (e.g. on tablets or phones), sometimes combined with coaching and monitoring, are now used at scale in some countries and regions. How much do you agree with each statement?", [
        ("F2_judgement", "They reduce teachers\u2019 professional judgement more than is acceptable."),
        ("F2_conditions", "They depend on conditions (monitoring, pay, supervision) that public systems can maintain."),
        ("F2_sustainable", "They can be sustained without external funding."),
        ("F2_scale_up", "They would be suitable for scale-up in the system I answer for.")],
        AGREE5 + ["No view"], doc="F2")
    f.select_one("F3_family_edtech", "How significant is EdTech that families buy or use directly (e.g. learning apps or exam-preparation services, often paid for with mobile money or airtime)?", [
        "Negligible", ("small_urban", "Small, mainly urban and better-off families"),
        ("significant_growing", "Significant and growing"), ("larger_than_school", "Larger than school-based use"),
        "No view"], doc="F3")
    f.select_one("F3_gaps", "Does this widen or narrow gaps between learners?", [
        ("widens_lot", "Widens a lot"), ("widens_little", "Widens a little"), ("no_difference", "No difference"),
        "Narrows", "No view"], doc="F3 (follow-up)")
    f.top3("F4_evidence_weight", "When decisions about EdTech are made in your system, which kinds of evidence carry most weight?", [
        ("international_research", "International research (e.g. trials from other countries)"),
        ("national_evaluations", "Evaluations carried out in this country"),
        ("donor_pilots", "Results from pilots run by donors or NGOs"),
        ("provider_claims", "Providers\u2019 claims and marketing"),
        ("agency_recommendations", "Recommendations from international agencies"),
        ("teacher_feedback", "Feedback from teachers and schools"),
        ("political_visibility", "Political or public visibility"), "Other (please specify)"], doc="F4")
    f.select_one("F4_local_evidence", "How much do you agree: \u201cEvidence generated in this country is given enough weight in decisions.\u201d",
                 AGREE5 + ["No view"], doc="F4 (follow-up)")
    f.select_multi("F5_mno_role", "What role do mobile network operators play in EdTech in your system?", [
        ("free_discounted", "Free or discounted access to learning content"), ("school_connectivity", "Connectivity for schools"),
        ("own_platforms", "Their own learning platforms or services"),
        ("programme_partners", "Partners in government or donor programmes"),
        ("payment_channels", "Payment channels (mobile money, airtime) for learning services"),
        ("little_or_no_role", "Little or no role"), "No view"], doc="F5", excl=["little_or_no_role", "no_view"])
    f.select_one("F5_influence", "How much influence do they have over which EdTech reaches learners?", [
        "None", "Some", "Considerable", "Substantial", "No view"], doc="F5 (follow-up)")
    f.top3("F6_crisis_constraints", "For refugee, displaced or crisis-affected learners, rank the biggest constraints on EdTech actually helping.", [
        ("accreditation", "Recognition or accreditation of learning"), ("connectivity_devices", "Connectivity and devices"),
        "Power", ("language_content", "Content in the right language"), ("teacher_capacity", "Teacher capacity"),
        ("safety_protection", "Safety and protection risks"), ("funding_sustainability", "Funding sustainability"),
        ("coordination", "Coordination among agencies"), "Other (please specify)"], doc="F6",
        hint="Please answer only if you have experience of education in displacement or crisis settings.")
    f.end()

    f.begin("sec_G", "Section G. Equity and the review itself", relevant="${consent_agreed}='yes'")
    f.top3("G1_equity", "Across everything above, which equity dimension is most consequential in your system and most at risk of being missed?", [
        "Gender", ("rural_remote", "Rural or remote location"), "Disability", ("income", "Household income"),
        ("minority_languages", "Language / speakers of minority languages"),
        ("displacement", "Displacement or refugee status"), ("conflict_area", "Living in a conflict-affected area"),
        "Other (please specify)"], doc="G1")
    f.text("G2_missing_question", "What important question about EdTech in your system does this consultation miss?", doc="G2",
           hint="Optional. Please do not include personal names or identifiable individual details.")
    f.text("G3_suggested_experts",
           "Would you like to suggest other experts for this panel, especially people working in the system you answered for? If so, please give their name, organisation, institutional role, or public profile link.",
           doc="G3",
           hint="Optional. Please do not submit private phone numbers or private email addresses without their prior consent.",
           pii=True,
           note="Third-party referral: store in administrative panel roster, detached from survey responses")
    f.begin("G4_panel", "Would you be willing to take part in Round 2 (a short follow-up later this year), and/or a brief interview/focus group?", appearance="field-list")
    f.select_one("G4_round2", "Round 2", ["Yes", "No"], doc="G4")
    f.select_one("G4_interview", "Interview / focus group", ["Yes", "No"], doc="G4")
    f.text("G4_delphi_code",
           "Anonymous Expert Token / Delphi Pseudonym",
           doc="G4 (Delphi Code)",
           relevant="${G4_round2}='yes'",
           hint="To link your Round 1 and Round 2 answers without sharing an email address, enter your anonymous Expert Token (e.g. EXP-042 from your email) or a memorable personal pseudonym (e.g. BLUEZEBRA42). Entering the same code in Round 2 re-links your responses with zero identity exposure.",
           pii=False,
           note="Anonymous panel Token or memorable pseudonym for zero-knowledge Delphi linkage")
    f.text("G4_contact", "Contact email or phone (optional; kept separate from your answers)", doc="G4",
           relevant="${G4_round2}='yes' or ${G4_interview}='yes'",
           hint="Optional. Kept in a detached panel key registry to notify you when Round 2 opens.",
           pii=True,
           note="Personal data; stored in detached Delphi key vault")
    f.end()
    f.note("thanks", "**Thank you. Your judgement makes this review possible.**", relevant="${consent_agreed}='yes'")
    f.end()

    f.tests += [
        ("sec_A", "relevant", {"consent_agreed": "yes"}, None, True),
        ("sec_A", "relevant", {"consent_agreed": "no"}, None, False),
        ("consent_declined", "relevant", {"consent_agreed": "no"}, None, True),
        ("consent_declined", "relevant", {"consent_agreed": "yes"}, None, False),
        ("consent_agreed", "constraint", {}, "yes", True),
        ("consent_agreed", "constraint", {}, "no", False),
        ("G4_delphi_code", "relevant", {"G4_round2": "yes"}, None, True),
        ("G4_delphi_code", "relevant", {"G4_round2": "no"}, None, False),
        ("A1_expert_gps", "relevant", {"A1_expert_gps_consent": "yes"}, None, True),
        ("A1_expert_gps", "relevant", {"A1_expert_gps_consent": "no"}, None, False),
        ("G4_contact", "relevant", {"G4_round2": "yes", "G4_interview": "no"}, None, True),
        ("G4_contact", "relevant", {"G4_round2": "no", "G4_interview": "yes"}, None, True),
        ("G4_contact", "relevant", {"G4_round2": "yes", "G4_interview": "yes"}, None, True),
        ("G4_contact", "relevant", {"G4_round2": "no", "G4_interview": "no"}, None, False),
        ("D3_constraints", "relevant", {"D1_a": "routinely", "D1_b": "some"}, None, False),
        ("D3_constraints", "relevant", {"D1_c": "not_at_present"}, None, True),
        ("D3_constraints", "relevant", {"D1_i": "outside_support"}, None, True),
        ("D3_constraints", "relevant", {}, None, False),
        ("D3_most_urgent", "relevant", {"D1_g": "outside_support"}, None, True),
        ("D3_most_urgent", "relevant", {"D1_g": "dont_know"}, None, False),
        ("A3_work_type", "relevant", {"A3_based": "in_country"}, None, False),
        ("A3_work_type", "relevant", {"A3_based": "outside_africa"}, None, True),
        ("D5_biggest_gap", "relevant", {"D5_ai_oversight": "broadly_covered"}, None, False),
        ("D5_biggest_gap", "relevant", {"D5_ai_oversight": "guidance_unused"}, None, True),
        ("D5_biggest_gap", "relevant", {"D5_ai_oversight": "no_view"}, None, False),
        ("D6_name", "relevant", {"D6_own_list": "yes_formal"}, None, True),
        ("D6_name", "relevant", {"D6_own_list": "informal"}, None, False),
    ]

    f.issue("Header", "Inconsistency", "Header says 'Draft v1 \u00b7 25 Sept 2026' (consistent with the opening line for this document). The teacher and provider files say 28 September in the opening line; align all three.")
    f.issue("D4", "Numbering error", "The two agreement statements are labelled (i) and (iii); there is no (ii). Built as D4_agree_i and D4_agree_iii. Please check whether a statement was dropped.")
    f.issue("C4", "Needs confirmation", "'Which of these should be EdTech\u2019s main role (select one)' has no option list in the Word file. Assumed: the four supportive roles plus 'No view'. Confirm or send the intended list.")
    f.issue("D5", "Needs confirmation", "Two options overlap: 'Guidance exists but is not applied in practice' and 'Guidance is not applied consistently'. Both are kept, and both open the 'biggest gap' follow-up. Confirm they should stay separate.")
    f.issue("D2/D3", "Design decision", "D2 is asked for every row a\u2013i regardless of the D1 answer. In D3 the 'most urgent gap' list shows all nine areas, not only those flagged in D1.")
    f.issue("F6", "Needs confirmation", "'Answer only if you have experience of displacement or crisis settings' is a hint, not a gate (no screening question). Add one if you want it enforced.")
    f.issue("Intro", "Implemented", "Explicit primary consent gate ('consent_agreed') added with required=yes. Rounds are strictly gated on consent.")
    f.issue("A1 (GPS)", "Implemented", "Expert location GPS capture is gated by explicit consent ('A1_expert_gps_consent').")
    f.issue("G3, G4", "Privacy & Ethical Compliance", "G3 (suggested peers) now explicitly instructs respondents to provide public institutional affiliations and avoid sharing unconsented private phone/email. G4 (contact) is now conditionally gated only when Round 2 or interview is selected ('yes'), flagged pii=True, and designated for the detached Delphi panel key registry.")
    f.issue("B2, F1, F4, F6, G1", "Design decision", "Ranking is three sequential questions (1st/2nd/3rd) with duplicate prevention. Analysis columns end _1, _2, _3.")
    f.issue("Round 2", "Needs confirmation", "Round 2 feedback requires linking a respondent's Round 1 answers to Round 2 without names. Kobo has no built-in anonymous panel ID; decide how respondents will be linked (for example a respondent-chosen code entered in both rounds).")
    return f




# ============================================================ DETACHED FOLLOW-UP & DIRECTORY
def build_followup_contact():
    f = Form("ssa_followup_contact_optin_v1_en",
             "SSA EdTech Review - Detached Participant Re-Contact & Directory Registry (EN, v1)",
             "followup_contact_optin_v1_en")
    f._add(type="start", name="start")
    f._add(type="end", name="end")
    f._add(type="today", name="today")
    f.calc("instrument_version", "'followup_contact_optin_v1_en'")

    f.begin("intro", "Detached Re-Contact & Directory Registry")
    f.note("intro_1", "**Sub-Saharan Africa EdTech Landscape Review: Detached Re-Contact & Directory Registry**")
    f.note("intro_2", "This standalone registry is completely detached from the anonymous landscape review surveys. Submitting your contact information here is never linked to your survey responses, guaranteeing 100% confidentiality.")
    f.note("intro_3", "Use this form to opt into Delphi Round 2 consultations, request inclusion in the Public SSA EdTech Provider Directory, volunteer for qualitative interviews, or request the final research synthesis.")

    f.select_one("stakeholder_role", "Which stakeholder group best describes your role?", [
        ("teacher", "Teacher / School Educator"),
        ("provider", "EdTech Solution Provider / Entrepreneur"),
        ("expert", "Education Expert / Researcher / Policy Specialist"),
        ("other", "Other Ecosystem Stakeholder")], doc="Role", required=True)

    f.select_multi("optin_purposes", "How would you like to stay engaged?", [
        ("delphi_round2", "Participate in Expert Delphi Consultation Round 2"),
        ("provider_directory", "Be listed or contacted for the Public SSA EdTech Solution Directory"),
        ("qualitative_interview", "Participate in an in-depth qualitative interview or focus group"),
        ("findings_report", "Receive the final published research report and macro observatory findings")],
        doc="Purposes", hint="Select all that apply.", required=True)
    f.end()

    f.begin("contact_details", "Contact Details", appearance="field-list")
    f.text("full_name", "Full Name / Preferred Title", doc="Name", hint="Your name", pii=True, required=True)
    f.text("organisation_name", "Organisation, Institution, or School Name (optional)", doc="Org", hint="Optional", pii=True)
    f.select_one("country", "Primary Country of Operation / Residence",
                 SSA48 + [("OTH", "Other / International")], doc="Country", appearance="minimal")
    f.text("email_address", "Email Address", doc="Email", hint="Primary email address for follow-up", pii=True, required=True)
    f.text("phone_whatsapp", "Phone / WhatsApp (optional)", doc="Phone", hint="Optional: include country code", pii=True)
    f.text("delphi_anon_code", "Anonymous Expert Token / Delphi Pseudonym (optional)", doc="Delphi Code",
           relevant="${stakeholder_role}='expert' and selected(${optin_purposes}, 'delphi_round2')",
           hint="For Expert Delphi Round 2 only: Enter your anonymous Expert Token from your invitation (e.g. EXP-042) or a memorable pseudonym (e.g. BLUEZEBRA42) to match your Round 1 and Round 2 responses without revealing your identity.",
           pii=False, note="Anonymous token / pseudonym for zero-knowledge Delphi panel linkage")
    f.end()

    f.note("thanks", "**Thank you for your engagement with the Sub-Saharan Africa EdTech Landscape Review.** Your details are held securely and will never be joined with anonymous survey datasets.")

    f.tests += [
        ("delphi_anon_code", "relevant", {"stakeholder_role": "expert", "optin_purposes": "delphi_round2"}, None, True),
        ("delphi_anon_code", "relevant", {"stakeholder_role": "teacher", "optin_purposes": "delphi_round2"}, None, False),
        ("delphi_anon_code", "relevant", {"stakeholder_role": "expert", "optin_purposes": "provider_directory"}, None, False),
    ]
    f.issue("Architecture", "Privacy by Design",
            "This detached form physically decouples respondent identities from survey microdata. "
            "In Kobo/ODK, this is deployed as a distinct project asset with a separate database URL, "
            "satisfying GDPR Art. 25 (Data Protection by Design) and AU Malabo Convention standards.")
    return f

# ----------------------------------------------------------------------- main
def write_map(forms, path):
    wb = Workbook()
    ws0 = wb.active
    ws0.title = "Review notes"
    ws0.append(["Form", "Doc ID", "Type", "Detail"])
    for f in forms:
        for row in f.review:
            ws0.append(list(row))
    for f in forms:
        ws = wb.create_sheet(f.instrument[:28])
        ws.append(["Doc ID", "XLSForm name(s)", "Type", "Choice list", "Max select", "Exclusive options",
                   "Skip logic (relevant)", "Personal data", "Notes"])
        for q in f.qmap:
            ws.append([q["doc"], q["names"], q["type"], q["list"], q["max"], q["excl"],
                       q["relevant"], q["pii"], q["note"]])
    for sh in wb.worksheets:
        for c in sh[1]:
            c.font = Font(name="Arial", bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="0F5C5A")
        for row in sh.iter_rows(min_row=2):
            for c in row:
                c.font = Font(name="Arial")
                c.alignment = Alignment(wrap_text=True, vertical="top")
        sh.freeze_panes = "A2"
        for col in sh.columns:
            w = max(len(str(c.value or "")) for c in col[:80])
            sh.column_dimensions[col[0].column_letter].width = min(max(w + 2, 12), 60)
    wb.save(path)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    forms = [("SSA_Teacher_Survey_v1_EN_XLSForm.xlsx", build_teacher()),
             ("SSA_Provider_Survey_v1_EN_XLSForm.xlsx", build_provider()),
             ("SSA_Expert_Consultation_R1_v1_EN_XLSForm.xlsx", build_expert()),
             ("SSA_Followup_Contact_Optin_v1_EN_XLSForm.xlsx", build_followup_contact())]
    bad = False
    for fname, f in forms:
        problems = validate(f)
        n, fails = run_tests(f, [])
        questions = [r for r in f.rows if r["type"].split()[0] in ("select_one", "select_multiple", "text")]
        docs = {re.match(r"^[A-Z]\d+", q["doc"]).group(0) for q in f.qmap if re.match(r"^[A-Z]\d+", q["doc"])}
        print("%-52s rows=%d lists=%d doc-items=%d tests=%d" % (fname, len(f.rows), len(f.lists), len(docs), n))
        for p in problems:
            print("   VALIDATION:", p)
        for p in fails:
            print("   TEST FAIL:", p)
        bad = bad or bool(problems or fails)
        f.write(OUT / fname)
    write_map([x for _, x in forms], OUT / "SSA_XLSForm_Question_Map_and_Review_Notes.xlsx")
    print("FAILED" if bad else "ALL CHECKS PASSED")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
