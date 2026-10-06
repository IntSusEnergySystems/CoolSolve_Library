#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sweep.py -- quick, dependency-free sweep of a private collection of EES models.

What it does (all read-only on the source tree, nothing is extracted to disk):
  1. walks the source root and reads every .ees / .lib / .lkt file, plus the .ees/.lib/.lkt
     members of .zip archives (read in memory; byte-identical copies of an already listed
     file are dropped, macOS '._*' resource forks are ignored);
  2. extracts cheap features per file: EES version, #lines, #equations, comment ratio,
     title/description comments, language guess, language features, unit hints, fluids,
     $ID$ licence stamp, authors hints, companion data files ...;
  3. groups exact and near duplicates (hash of normalised code / Jaccard >= 0.6 on the
     normalised code lines), picks one representative per group (best documented, then
     newest EES version / mtime);
  4. applies heuristic classification (category / kind / level / priority / licence) and then
     the manual curation layer 'curation.csv' (same folder; English titles/descriptions and
     overrides decided by a human/LLM review of the sweep);
  5. writes inventory.csv (exact column set below) next to this script.

Usage:
    python3 sweep.py [--root DIR] [--out DIR] [--curation FILE] [--stats]

Binary .ees layout used (verified on the whole collection):
    byte 0 = length of the version string, then the version string (e.g. 'X9.920'),
    uint32 LE at offset 16 = length n of the Equations-window text,
    bytes [20:20+n] = Equations-window text, Windows-1252, lines end with CRLF.
    24 files store RTF instead of plain text -> converted by strip_rtf().
The other binary parts (unit settings, variable records with the stored solution, lookup and
parametric tables) are decoded by CoolSolve's tools/ees_extract.py when the CoolSolve
repository is found next to the library (or via $COOLSOLVE_TOOLS); the columns ees_units,
stored_solution and tables are then filled, otherwise they are left empty.

Privacy: files of student exam submissions (PERSONAL_DIRS) are classified by rule and their
file names are redacted in the output (the source keeps them).

Manual columns: 'decision' and 'library_id' are filled by the library workflow; they are read
back from the existing inventory.csv (by path) and preserved when the sweep is re-run.

Curation file (curation.csv, UTF-8), columns:
    key,scope,title,description,category_guess,kind_guess,level_guess,priority,
    license_status,authors,notes,doc_quality,language
  key   = value of the 'path' column of any member of the duplicate group (or of the file)
  scope = 'group' (default for every member of the key's group; 'priority' only applies to
          the representative, other members get low/skip) or 'file' (this row only)
  empty cells are ignored; 'notes' are appended to the automatic notes.
"""
import argparse
import collections
import csv
import hashlib
import io
import os
import re
import struct
import sys
import time
import unicodedata
import zipfile

DEFAULT_ROOT = os.path.expanduser('~/Nextcloud/thermo_models')
HERE = os.path.dirname(os.path.abspath(__file__))
EXTS = ('.ees', '.lib', '.lkt')
DATA_EXTS = ('.txt', '.csv', '.asc', '.dat', '.xls', '.xlsx', '.xlsm', '.mat')

DS_SNIPPETS = set()   # filled by discover(): .txt files starting with the {$DS.} directive

COLUMNS = ['candidate_id', 'source', 'path', 'companion_files', 'title', 'description',
           'category_guess', 'kind_guess', 'level_guess', 'language', 'format', 'ees_version',
           'n_lines', 'n_equations', 'features', 'unit_hints', 'fluids', 'doc_quality',
           'duplicate_group', 'is_representative', 'priority', 'license_status', 'authors', 'notes',
           'ees_units', 'stored_solution', 'tables', 'decision', 'library_id']

# Folders holding student exam submissions (file names = student names): classified by rule,
# file names redacted in the output.
PERSONAL_DIRS = ('MCI_REMIDICKES/MCI/Examen/MCI_ees_examen_juin_2019/MCI_examen_juin_2019/',
                 'MCI_REMIDICKES/MCI/Examen/MCI_examen_juin_2019/')


def is_personal(rel):
    return rel.startswith(PERSONAL_DIRS)


def redact(rel, cid):
    folder, name = rel.rsplit('/', 1)
    ext = name.rsplit('.', 1)[-1] if '.' in name else ''
    return '%s/[redacted %s].%s' % (folder, cid, ext)


_EE = None


def ees_extract_module():
    """CoolSolve's tools/ees_extract.py (sibling repository), or None."""
    global _EE
    if _EE is None:
        _EE = False
        for d in (os.environ.get('COOLSOLVE_TOOLS'),
                  os.path.join(HERE, '..', '..', '..', 'CoolSolve', 'tools')):
            if d and os.path.isfile(os.path.join(d, 'ees_extract.py')):
                sys.path.insert(0, os.path.abspath(d))
                import ees_extract
                _EE = ees_extract
                break
    return _EE or None


def binary_info(b):
    """Unit system, stored solution and embedded tables decoded by ees_extract.py."""
    E = ees_extract_module()
    if E is None:
        return {}
    try:
        r = E.extract_bytes(b)
    except Exception:
        return {}
    u = E.unit_directive(r['units'])
    stored = sum(v['value'] is not None for v in r['variables'])
    return {
        'ees_units': (u[len('$UnitSystem '):] if u else '?') + (' +decimal-comma' if r['decimal_comma'] else ''),
        'stored_solution': '%d/%d' % (stored, len(r['variables'])),
        'tables': ';'.join('%s:%s(%dx%d)' % (t['kind'], t['name'], t['nrows'], len(t['columns']))
                           for t in r['tables']),
    }

CATEGORIES = ['fundamentals', 'properties', 'heat_transfer', 'heat_exchangers', 'compressors',
              'expanders_turbines', 'pumps_fans', 'valves_nozzles_piping', 'storage',
              'combustion_boilers', 'engines', 'power_cycles_vapour', 'power_cycles_gas',
              'refrigeration_heat_pumps', 'absorption_sorption', 'hvac_psychrometrics',
              'solar_renewables', 'cogeneration_energy_systems', 'buildings', 'misc']
KINDS = ['steady', 'dynamic', 'optimization', 'function', 'unknown']
PRIORITIES = ['wave1', 'high', 'medium', 'low', 'skip']


# ======================================================================================
# low-level readers
# ======================================================================================
def nfc(s):
    return unicodedata.normalize('NFC', s)


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def decode_cp1252(raw):
    try:
        return raw.decode('cp1252')
    except UnicodeDecodeError:
        return raw.decode('cp1252', errors='replace')


def strip_rtf(s):
    """Very small RTF -> text converter (enough for EES equation windows)."""
    out = []
    i, n = 0, len(s)
    stack = []
    skip = False
    while i < n:
        c = s[i]
        if c == '{':
            stack.append(skip)
            i += 1
            if re.match(r'\\(fonttbl|colortbl|stylesheet|info|pict|\*)', s[i:i + 14]):
                skip = True
        elif c == '}':
            skip = stack.pop() if stack else False
            i += 1
        elif c == '\\':
            i += 1
            if i >= n:
                break
            d = s[i]
            if d in '\\{}':
                if not skip:
                    out.append(d)
                i += 1
            elif d == "'":
                h = s[i + 1:i + 3]
                i += 3
                if not skip:
                    try:
                        out.append(bytes([int(h, 16)]).decode('cp1252'))
                    except Exception:
                        pass
            elif d in '~-_':
                if not skip:
                    out.append({'~': ' ', '-': '', '_': '-'}[d])
                i += 1
            elif d in '\r\n':
                if not skip:
                    out.append('\n')
                i += 1
            elif d.isalpha():
                m = re.match(r'([a-zA-Z]+)(-?\d+)? ?', s[i:])
                w, par = m.group(1), m.group(2)
                i += m.end()
                if skip:
                    continue
                if w in ('par', 'line'):
                    out.append('\n')
                elif w == 'tab':
                    out.append('\t')
                elif w == 'u' and par is not None:
                    v = int(par)
                    v = v + 65536 if v < 0 else v
                    out.append(chr(v))
                    if i < n and s[i] == '?':
                        i += 1
                elif w == 'emdash':
                    out.append('\u2014')
                elif w == 'endash':
                    out.append('\u2013')
                elif w == 'bullet':
                    out.append('\u2022')
                elif w in ('lquote', 'rquote'):
                    out.append("'")
                elif w in ('ldblquote', 'rdblquote'):
                    out.append('"')
            else:
                i += 1
        elif c in '\r\n':
            i += 1
        else:
            if not skip:
                out.append(c)
            i += 1
    return ''.join(out)


def read_ees_bytes(b):
    """-> (version, text, was_rtf). Raises ValueError if not an EES file."""
    if len(b) < 24:
        raise ValueError('too short')
    ln = b[0]
    ver = b[1:1 + ln].decode('latin1')
    n = struct.unpack('<I', b[16:20])[0]
    if n > len(b) - 20:
        raise ValueError('bad text length')
    raw = b[20:20 + n]
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff'):   # one file stores UTF-16 text
        text = raw.decode('utf-16', errors='replace')
    else:
        text = decode_cp1252(raw)
    rtf = text.startswith('{\\rtf')
    if rtf:
        text = strip_rtf(text)
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return ver, text, rtf


def clean_version(v):
    m = re.match(r'^[A-Za-z]?\d+\.\d+', v or '')
    return m.group(0) if m else (v or '').strip()


def split_code_comments(text):
    """Separate EES comments from code.

    EES comments: "..." (may span lines), {...} (nestable) and // to end of line.
    Single-quoted strings are kept in the code. Returns (code, comments) where code has
    every comment replaced by a blank (newlines preserved) and comments is a list of
    (kind, text, line_no) in file order.
    """
    code = []
    comments = []
    i, n, line = 0, len(text), 1
    while i < n:
        c = text[i]
        if c == '"':
            j = text.find('"', i + 1)
            if j < 0:
                j = n
            body = text[i + 1:j]
            comments.append(('"', body, line))
            nl = body.count('\n')
            code.append(' ' + '\n' * nl)
            line += nl
            i = j + 1
        elif c == '{':
            depth, j = 1, i + 1
            while j < n and depth > 0:
                ch = text[j]
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                j += 1
            if depth > 0:  # unbalanced: fall back to first closing brace
                k = text.find('}', i + 1)
                if k < 0:  # a lone '{' -> ordinary char
                    code.append(c)
                    i += 1
                    continue
                j = k + 1
            body = text[i + 1:j - 1]
            comments.append(('{', body, line))
            nl = body.count('\n')
            code.append(' ' + '\n' * nl)
            line += nl
            i = j
        elif c == "'":
            j = text.find("'", i + 1)
            k = text.find('\n', i + 1)
            if j >= 0 and (k < 0 or j < k):
                code.append(text[i:j + 1])
                i = j + 1
            else:
                code.append(c)
                i += 1
        elif c == '/' and text.startswith('//', i):
            j = text.find('\n', i)
            if j < 0:
                j = n
            comments.append(('//', text[i + 2:j], line))
            code.append(' ')
            i = j
        else:
            if c == '\n':
                line += 1
            code.append(c)
            i += 1
    return ''.join(code), comments


# ======================================================================================
# vocabularies
# ======================================================================================
FR_WORDS = set('''le la les des du un une et est pour par dans sur avec au aux qui que ce cette ces
ses sont entre sans ou où plus ne pas il elle on nous vous leur leurs mais donc car sera seront
doit peut être avoir fait calcul calculer rendement débit puissance température pression entrée sortie
échangeur chaleur vapeur eau fluide détente condenseur évaporateur chaudière hypothèse hypothèses
données paramètres résultats exercice énoncé réponse travail énergie masse volume titre surchauffe
sous-refroidissement refroidissement réchauffage soutirage fumées combustible combustion comburant
températures pressions isentropique rendements cycle moteur soupape taux compression admission
échappement cylindre piston ouverture fermeture avance retard trouver déterminer donner donné supposé
supposer valeur valeurs dimensionnement régime nominal débit-masse état résolution calculez
détermination vitesse'''.split())

EN_WORDS = set('''the of and is for with in to from at by on an are this that as be or not input inputs output
outputs heat temperature pressure flow rate mass power efficiency cycle compressor turbine condenser
evaporator exchanger fluid steam water calculate calculation parameters results assumptions assumption
model value values total specific inlet outlet supply exhaust which when where then using given find
determine problem solution what how air gas work energy enthalpy entropy volume ratio isentropic
adiabatic constant coefficient number factor area length diameter velocity state data'''.split())

NL_WORDS = set('''het een van voor met op te dat niet om ook bij naar uit aan als zijn wordt worden deze die dit
temperatuur druk warmte stoom koelmiddel vermogen massastroom debiet verdamper condensor warmtewisselaar
vraag oefening berekening gegevens resultaten lucht nodig bepaal bereken gevraagd opgave enthalpie
rendement toestand ketel pomp ventilator leiding dichtheid soortelijke isentropisch
compressieverhouding stroming'''.split())

_FLUID_NAMES = '''Water Steam Steam_IAPWS Steam_NBS Air Air_ha AirH2O NH3 Ammonia R717 NH3H2O LiBrH2O R718
R134a R22 R12 R11 R113 R114 R123 R124 R125 R141b R142b R143a R152a R218 R227ea R236ea R236fa R245fa R290
R32 R404A R407C R410A R507A R600 R600a R744 R1234yf R1234ze R1233zd R365mfc RC318 R502 R500 R13 R14
R23 R41 R21 R30 R40 R170 R1270 Propane Isobutane Butane n-Butane Pentane n-Pentane Isopentane Hexane
n-Hexane Heptane n-Heptane Octane n-Octane Decane Dodecane Benzene Toluene Methane Ethane Ethylene
Propylene Methanol Ethanol Acetone CO2 CarbonDioxide CO CarbonMonoxide N2 Nitrogen O2 Oxygen H2
Hydrogen He Helium Ar Argon Neon Krypton Xenon SO2 H2S NO NO2 N2O Cl2 H2O D2O HeavyWater CH4 C2H6
C3H8 C4H10 C8H18 C2H4 C2H2 Acetylene MM MDM MD2M D4 D5 D6 SES36 Novec649 HFE7000 Therminol_VP1
Therminol Dowtherm Syltherm800 Glycol EG PG EthyleneGlycol PropyleneGlycol Brine Hydrazine Mercury
Sodium Cyclopentane Cyclohexane Isohexane Gasoline Diesel Ice Syngas'''.split()
KNOWN_FLUIDS = {f.lower(): f for f in _FLUID_NAMES}


# ======================================================================================
# per-file analysis
# ======================================================================================
UNIT_TOKEN_RE = re.compile(r'\[([^\[\]\n]{1,28})\]')
ARRAY_RE = re.compile(r'[A-Za-z_][\w$#]*\[[^\[\]\n]+\]')
SHIFT_RE = re.compile(r'[A-Za-z_][\w$#]*\[\s*[A-Za-z_]\w*\s*[+-]\s*\d+\s*\]')
IDENT_RE = re.compile(r'[A-Za-z_][\w$#]*')
UNIT_OK_RE = re.compile(r'^[A-Za-z\u00b0\u00b5%\u00b2\u00b3\-\*/\^\(\)\.\d\s]+$')
RE_FUNC_DEF = re.compile(r'^\s*(function|procedure|module|subprogram)\b\s*([A-Za-z_][\w$]*)', re.I)
RE_DUP = re.compile(r'^\s*duplicate\b\s*([A-Za-z_]\w*)\s*=\s*([^,;]+?)\s*[,;]\s*([^,;]+?)\s*$', re.I)
RE_END = re.compile(r'^\s*end\b(?:\s+[A-Za-z_][\w$]*)?\s*$', re.I)
RE_CALL = re.compile(r'^\s*call\b\s*([A-Za-z_][\w$]*)', re.I)
RE_EQ = re.compile(r'(?<![<>:=!])=(?!=)')

FEATURE_RES = [
    ('FUNCTION', re.compile(r'^\s*function\b\s*[A-Za-z_]', re.I | re.M)),
    ('PROCEDURE', re.compile(r'^\s*procedure\b\s*[A-Za-z_]', re.I | re.M)),
    ('CALL', re.compile(r'^\s*call\b\s*[A-Za-z_]', re.I | re.M)),
    ('MODULE', re.compile(r'^\s*module\b\s*[A-Za-z_]', re.I | re.M)),
    ('SUBPROGRAM', re.compile(r'^\s*subprogram\b\s*[A-Za-z_]', re.I | re.M)),
    ('DUPLICATE', re.compile(r'^\s*duplicate\b', re.I | re.M)),
    ('INTEGRAL', re.compile(r'\bintegral\s*\(|\$integraltable', re.I)),
    ('LOOKUP', re.compile(r'\b(lookup\w*|interpolate\d?|tablevalue|tablerun)\b\s*[\(\$]|\$lookup', re.I)),
    ('UNITSYSTEM', re.compile(r'\$unitsystem', re.I)),
    ('PSYCH', re.compile(r'\bairh2o\b|\bair_ha\b|\brelhum\b|\bhumrat\b|\bwetbulb\b|\bdewpoint\b|\bpsychro', re.I)),
    ('CONVERT', re.compile(r'\bconverttemp\s*\(|\bconvert\s*\(', re.I)),
    ('FLUIDPROP', re.compile(r'\bfluidprop\w*\s*\(', re.I)),
    ('REFPROP', re.compile(r'\bees_refprop\b|\brefprop\b', re.I)),
    ('INCLUDE', re.compile(r'\$include|\$common', re.I)),
]


def clean_comment(t):
    t = t.strip()
    t = re.sub(r'^[\s!*=#~\-_\.]+', '', t)
    t = re.sub(r'[\s*=#~\-_]+$', '', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()


def looks_like_code(t):
    """True for commented-out equations such as 'T_1=300' or 'P=Pressure(R134a;T=T1;x=1)'."""
    if '=' not in t:
        return False
    spaced = len(re.findall(r'[A-Za-z\u00c0-\u00ff]{3,}\s+[A-Za-z\u00c0-\u00ff]{3,}', t))
    if spaced >= 2 and len(t) > 40:
        return False
    return bool(re.match(r"^[\w$\[\]\.#'\s\*/\+\-\^\(\),;:=<>]+$", t)) and spaced < 2


def word_list(text):
    return re.findall(r"[A-Za-z\u00c0-\u00ff][A-Za-z\u00c0-\u00ff'\-]*", text)


def guess_language(texts):
    blob = ' '.join(texts).lower()
    toks = [w.strip("'-") for w in word_list(blob)]
    toks = [w for w in toks if len(w) >= 2]
    if len(toks) < 4:
        return 'none' if len(toks) == 0 else 'unknown'
    fr = en = nl = 0.0
    for w in toks:
        w2 = w.split("'")[-1] if "'" in w else w
        if w in FR_WORDS or w2 in FR_WORDS:
            fr += 1
        if w in EN_WORDS:
            en += 1
        if w in NL_WORDS:
            nl += 1
    fr += len(re.findall(r"[\u00e9\u00e8\u00ea\u00e0\u00e7\u00f9\u00f4\u00e2]", blob)) * 0.5
    nl += len(re.findall(r'\b\w*(?:ij|ooi|oek|uur|ijk)\w*\b', blob)) * 0.2
    if blob.count("l'") + blob.count("d'") >= 2:
        fr += 2
    order = sorted([(fr, 'fr'), (en, 'en'), (nl, 'nl')], reverse=True)
    if order[0][0] < 1.5:
        return 'unknown'
    if order[1][0] > 0 and order[1][0] >= 0.7 * order[0][0]:
        return '+'.join(sorted([order[0][1], order[1][1]]))
    return order[0][1]


def normalise_line(l, euro):
    l = l.lower()
    if euro:
        l = re.sub(r'(?<=\d),(?=\d)', '.', l)
    l = l.replace(';', ',')
    l = re.sub(r'(?<![\w$#\]])(\d[\d\.]*(?:e[+-]?\d+)?)\s*\[[^\[\]]*\]', r'\1', l)
    l = re.sub(r'\)\s*\[[^\[\]]*\]', ')', l)
    l = re.sub(r'\s+', '', l)
    return l


def parse_version(v):
    m = re.match(r'[A-Za-z]*(\d+)\.?(\d*)', v or '')
    if not m:
        return (0, 0)
    return (int(m.group(1)), int(m.group(2) or 0))


def eval_bound(expr, consts):
    e2 = re.sub(r'[A-Za-z_]\w*', lambda m: str(consts.get(m.group(0).lower(), 'None')), expr.strip())
    if re.match(r'^[\d\.\+\-\*/\(\)\s]+$', e2):
        try:
            return int(round(eval(e2, {'__builtins__': {}})))
        except Exception:
            return None
    return None


def analyse_code(code):
    """Structural analysis of comment-free code text."""
    lines = code.split('\n')
    consts = {}
    for l in lines:
        m = re.match(r"^\s*([A-Za-z_]\w*)\s*=\s*([-+]?\d+(?:\.\d+)?)\s*(\[[^\]]*\])?\s*$", l)
        if m:
            try:
                consts[m.group(1).lower()] = float(m.group(2))
            except ValueError:
                pass
    stack = []  # entries: ('alg'|'blk'|'dup', multiplier)
    n_eq = n_alg = n_dup = expanded = max_loop = unresolved = 0
    calls = collections.Counter()
    defs = collections.defaultdict(list)
    directives = []
    code_lines = []
    for raw in lines:
        s = raw.strip()
        if not s:
            continue
        low = s.lower()
        if s.startswith('$'):
            directives.append(s)
            continue
        m = RE_FUNC_DEF.match(s)
        if m:
            kind = m.group(1).lower()
            defs[kind].append(m.group(2))
            stack.append(('alg' if kind in ('function', 'procedure') else 'blk', 1))
            code_lines.append(s)
            continue
        m = RE_DUP.match(s)
        if m:
            n_dup += 1
            lo, hi = eval_bound(m.group(2), consts), eval_bound(m.group(3), consts)
            if lo is None or hi is None:
                cnt, unresolved = 10, unresolved + 1
            else:
                cnt = max(1, hi - lo + 1)
            max_loop = max(max_loop, cnt)
            stack.append(('dup', cnt))
            code_lines.append(s)
            continue
        if RE_END.match(s):
            if stack:
                stack.pop()
            continue
        mc = RE_CALL.match(s)
        if mc:
            calls[mc.group(1).lower()] += 1
            code_lines.append(s)
            continue
        if any(k == 'alg' for k, _ in stack):
            n_alg += 1
            code_lines.append(s)
            continue
        s_nostr = re.sub(r"'[^'\n]*'", "''", s)
        if RE_EQ.search(s_nostr):
            n_eq += 1
            mult = 1
            for k, mu in stack:
                if k == 'dup':
                    mult *= mu
            expanded += mult
            code_lines.append(s)
        elif not re.match(r'^\s*(endif|else)\b', low):
            code_lines.append(s)
    return {'n_eq': n_eq, 'n_alg': n_alg, 'n_dup': n_dup, 'expanded': expanded, 'max_loop': max_loop,
            'calls': calls, 'defs': defs, 'directives': directives, 'code_lines': code_lines,
            'unresolved_loops': unresolved, 'consts': consts}


def strings_by_variable(code):
    d = collections.defaultdict(list)
    for m in re.finditer(r"([A-Za-z_][\w#]*\$)\s*=\s*'([^'\n]*)'", code):
        d[m.group(1).lower()].append(m.group(2))
    return d


def canon_fluid(v):
    v = v.strip()
    return KNOWN_FLUIDS.get(v.lower(), v)


def extract_fluids(code, sbv):
    found = collections.OrderedDict()
    for line in code.split('\n'):
        ls = line.strip()
        if re.match(r'^call\s+(?!ees_refprop)', ls, re.I) or RE_FUNC_DEF.match(ls):
            continue
        for m in re.finditer(r"([A-Za-z_][\w$#]*)\s*\(\s*([A-Za-z_][\w$#\-\.]*)\s*[,;]", ls):
            a = m.group(2)
            al = a.lower()
            if re.match(r'^(lookup|interpolate|tablerun|tablevalue|string|copy|concat|call)', m.group(1), re.I):
                continue
            if al.endswith('$'):
                for v in sbv.get(al, []):
                    v = v.strip()
                    mm = re.search(r'refprop\w*[\\/]([^\\/]+)$', v, re.I)
                    if mm:
                        found.setdefault('%s (REFPROP)' % mm.group(1), 1)
                    elif v and ' ' not in v and len(v) <= 40 and not re.match(r'^(freeze|density|spechea|thermalc|viscosity|dynvisc)', v, re.I):
                        found.setdefault(canon_fluid(v), 1)
            elif al in KNOWN_FLUIDS:
                found.setdefault(KNOWN_FLUIDS[al], 1)
    for m in re.finditer(r"'([^'\n]{1,40})'", code):
        v = m.group(1).strip()
        if v.lower() in KNOWN_FLUIDS:
            found.setdefault(KNOWN_FLUIDS[v.lower()], 1)
    return list(found.keys())


def extract_units(full_text):
    counts = collections.Counter()
    for m in UNIT_TOKEN_RE.finditer(full_text):
        start = m.start()
        prev = full_text[start - 1] if start > 0 else ' '
        if prev.isalpha() or prev in '_$#':
            continue  # array reference like x[i]
        tok = m.group(1).strip()
        if not tok or not UNIT_OK_RE.match(tok) or re.match(r'^\d+$', tok):
            continue
        t = tok.replace('\u00b0', '').replace(' ', '')
        if t.lower() in ('i', 'j', 'k', 'n', 'ii', 'jj', 'nn'):
            continue
        if t.lower() in ('c', 'celsius', 'degc'):
            t = 'C'
        elif t.lower() == 'kelvin':
            t = 'K'
        counts[t] += 1
    return counts


def infer_units(code):
    """Weak magnitude-based hints from literal assignments to T_*/p_* variables."""
    temps, press = [], []
    for m in re.finditer(r"^\s*([A-Za-z_][\w$#]*)\s*=\s*([-+]?\d+(?:[.,]\d+)?(?:[eE][-+]?\d+)?)\s*(\[[^\]]*\])?\s*$", code, re.M):
        name, val = m.group(1), m.group(2).replace(',', '.')
        if m.group(3):
            continue
        try:
            v = float(val)
        except ValueError:
            continue
        if re.match(r'^[Tt](_|\d)', name) or name.lower() == 't':
            temps.append(v)
        elif re.match(r'^[Pp](_|\d)', name) or name.lower() == 'p':
            press.append(v)
    hints = []
    if len(temps) >= 3:
        low = sum(1 for v in temps if v < 130) / len(temps)
        hints.append('~T:C' if low > 0.5 else '~T:K')
    if len(press) >= 3:
        press.sort()
        med = press[len(press) // 2]
        if med >= 1e4:
            hints.append('~p:Pa')
        elif med >= 20:
            hints.append('~p:kPa')
        elif med > 0:
            hints.append('~p:bar|MPa')
    return hints


def meaningful_comments(comments):
    out = []
    for kind, body, line in comments:
        if '$ID$' in body or body.strip().startswith('$'):
            continue
        heading = body.lstrip().startswith('!')
        t = clean_comment(body)
        if len(t) < 3 or not re.search(r'[A-Za-z\u00c0-\u00ff]{2,}', t):
            continue
        out.append({'text': t, 'kind': kind, 'line': line, 'heading': heading, 'code': looks_like_code(t)})
    return out


ID_LICENSES = {
    '1206': 'J. Lebrun lab licence (ULiege)',
    '202': 'ULiege Thermodynamics Lab licence',
    '0202': 'ULiege Thermodynamics Lab student/staff licence',
    '3804': 'P. Ngendakumana licence (ULiege Thermotechnics)',
    '434': 'K. Kim / Samsung Electronics licence (third party)',
    '1564': 'Solar Energy Lab, U. Wisconsin licence (third party)',
}


def parse_id_tag(tag):
    m = re.match(r'#\s*(\d+)\s*:\s*(.*)$', tag or '')
    if not m:
        return ('', '')
    num = m.group(1)
    return (num, ID_LICENSES.get(num, 'EES licence #%s: %s' % (num, m.group(2)[:60])))


AUTHOR_CANON = [
    (r'quoilin', 'Sylvain Quoilin'), (r'bertagnolio', 'St\u00e9phane Bertagnolio'), (r'lebrun', 'Jean Lebrun'),
    (r'lemort', 'Vincent Lemort'), (r'cuevas', 'Cristian Cuevas'), (r'rodr[i\u00ed]guez', 'Andr\u00e9s Rodr\u00edguez'),
    (r'teodorese', 'Vlad Teodorese'), (r'da silva', 'Cleide Da Silva'), (r'ngendakumana', 'Philippe Ngendakumana'),
    (r'dickes', 'R\u00e9mi Dickes'), (r'borguet', 'S. Borguet'), (r'masy', 'G. Masy'),
]


def canon_author(name):
    n = strip_accents(name).lower()
    for rx, full in AUTHOR_CANON:
        if re.search(strip_accents(rx), n):
            return full
    return name.strip()


def find_authors(prose, rel, id_tag):
    """Explicit 'Author(s): ...' lines in the comments (canonical names, reviewers flagged)."""
    names = []
    for c in prose[:60]:
        m = re.match(r'^(authors?|auteurs?|reviewed by|written by|made by|created by)\s*[:\-]\s*(.+)$', c['text'], re.I)
        if m:
            tag = ' (reviewer)' if m.group(1).lower().startswith('reviewed') else ''
            for part in re.split(r'\s*(?:,|;|&|\band\b|\bet\b)\s*', m.group(2)):
                part = part.strip(' .')
                if 3 <= len(part) <= 40 and not re.search(r'universit|faculty|laborator|^author\d', part, re.I):
                    nm = canon_author(part) + tag
                    if nm not in names:
                        names.append(nm)
    return names


INITIALS = {'SQ': 'Sylvain Quoilin', 'SB': 'St\u00e9phane Bertagnolio', 'JL': 'Jean Lebrun', 'VL': 'Vincent Lemort',
            'CC': 'Cristian Cuevas', 'AR': 'Andr\u00e9s Rodr\u00edguez', 'VT': 'Vlad Teodorese', 'PNG': 'Philippe Ngendakumana',
            'RD': 'R\u00e9mi Dickes', 'CAS': 'Cleide Da Silva'}


def initials_from_name(fname):
    out = []
    for m in re.finditer(r'(?<![A-Za-z])([A-Z]{2,8})(\d{6})(?!\d)', fname):
        sfx = m.group(1)
        i, toks = 0, []
        while i < len(sfx):
            for ln in (3, 2):
                if sfx[i:i + ln] in INITIALS:
                    toks.append(sfx[i:i + ln])
                    i += ln
                    break
            else:
                toks = []
                break
        for t in toks:
            if INITIALS[t] not in out:
                out.append(INITIALS[t])
    return out


def analyse_text(text, fmt='ees'):
    code, comments = split_code_comments(text)
    ca = analyse_code(code)
    lines = text.split('\n') if text else []
    mc = meaningful_comments(comments)
    prose = [c for c in mc if not c['code']]
    comment_chars = sum(len(c['text']) for c in prose)
    code_chars = len(re.sub(r'\s+', '', code))
    words = sum(len(word_list(c['text'])) for c in prose)
    n_head = sum(1 for c in prose if c['heading'])
    title, desc_parts = '', []
    for c in prose:
        t = c['text']
        t = re.sub(r'^(title|titre)\s*:\s*', '', t, flags=re.I)
        if not title:
            if len(t) >= 4:
                title = t
            continue
        if len(desc_parts) < 4 and t != title:
            desc_parts.append(t)
    m = re.search(r'\$ID\$([^\n}]*)', text)
    id_tag = m.group(1).strip() if m else ''
    feats = [name for name, rx in FEATURE_RES if rx.search(code)]
    if ARRAY_RE.search(code):
        feats.append('ARRAYS')
    if SHIFT_RE.search(code):
        feats.append('INDEX_SHIFT')
        if 'INTEGRAL' not in feats and re.search(r'\b(dt|d_t|deltat|delta_t|dtau|time|timestep|t_step)\b', code, re.I):
            feats.append('TIME_STEPPING')
    sbv = strings_by_variable(code)
    refs = set()
    for m in re.finditer(r"([A-Za-z0-9_\- \.]+\.(?:lkt|lib|txt|csv|asc|dat|xls|xlsx|xlsm|mat))", code, re.I):
        refs.add(m.group(1).strip().lower())
    for m in re.finditer(r"\b(?:lookup\w*|interpolate\d?|tablerun)\s*\(\s*'([^']+)'", code, re.I):
        refs.add(m.group(1).strip().lower())
    for m in re.finditer(r"\blookup\$row\s*\(\s*'([^']+)'", code, re.I):
        refs.add(m.group(1).strip().lower())
    euro = (';' in code) and bool(re.search(r'\d,\d', code))
    lines_norm = [normalise_line(l, euro) for l in ca['code_lines']]
    lines_norm = [l for l in lines_norm if l and l not in ('end', 'endif', 'else')]
    full_units = extract_units(text)
    return {
        'n_lines': len(lines), 'code': code, 'comments': comments, 'prose': prose, 'title': title,
        'description': ' | '.join(desc_parts), 'id_tag': id_tag, 'comment_chars': comment_chars,
        'code_chars': code_chars, 'words': words, 'n_head': n_head,
        'comment_ratio': comment_chars / max(1, comment_chars + code_chars), 'features': feats,
        'fluids': extract_fluids(code, sbv), 'units': full_units, 'unit_infer': infer_units(code),
        'idents': set(w.lower() for w in IDENT_RE.findall(code)), 'refs': refs, 'norm_lines': lines_norm,
        'ca': ca, 'euro': euro, 'uses_273': bool(re.search(r'273[\.,]15|\b273\b', code)),
        'language': guess_language([c['text'] for c in prose]),
        'authors_explicit': find_authors(prose, '', id_tag),
    }


def doc_quality_score(a, fmt):
    w, r, h = a['words'], a['comment_ratio'], a['n_head']
    if fmt == 'lkt':
        return 0
    if w < 8:
        return 0
    if (w >= 300 and r >= 0.15) or (w >= 150 and r >= 0.15 and h >= 4):
        return 3
    if (w >= 60 and r >= 0.05) or w >= 120:
        return 2
    return 1


def lkt_strings(b):
    out = []
    for m in re.finditer(rb'[\x20-\x7e\xb0-\xff]{4,}', b):
        s = m.group().decode('cp1252', errors='replace').strip()
        if re.search(r'[A-Za-z]{3,}', s) and not re.match(r'^[\W\d_]+$', s):
            out.append(s)
    return out


# ======================================================================================
# discovery
# ======================================================================================
def fix_zip_name(info):
    n = info.filename
    if not (info.flag_bits & 0x800):
        try:
            n = info.filename.encode('cp437').decode('cp1252')
        except Exception:
            pass
    return n


def is_junk(name):
    base = name.rsplit('/', 1)[-1]
    return base.startswith('._') or name.startswith('__MACOSX/') or '/__MACOSX/' in name


def iter_zip(data, label, depth=0):
    """yield dict(kind='model'|'data', label=..., name=..., bytes=..., mtime=...) for zip members."""
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
    except Exception:
        return
    for info in z.infolist():
        if info.is_dir():
            continue
        name = fix_zip_name(info)
        low = name.lower()
        if is_junk(name):
            yield {'kind': 'junk', 'label': label + '!/' + name}
            continue
        try:
            mt = time.mktime(tuple(info.date_time) + (0, 0, -1))
        except Exception:
            mt = 0
        try:
            if low.endswith(EXTS):
                yield {'kind': 'model', 'label': label + '!/' + name, 'bytes': z.read(info), 'mtime': mt}
            elif low.endswith(DATA_EXTS):
                yield {'kind': 'data', 'label': label + '!/' + name}
            elif low.endswith('.zip') and depth < 2:
                for x in iter_zip(z.read(info), label + '!/' + name, depth + 1):
                    yield x
        except Exception:
            continue


def discover(root):
    disk, zipped, data, junk = [], [], [], []
    global DS_SNIPPETS
    DS_SNIPPETS = set()
    for dp, dns, fns in os.walk(root):
        dns.sort(key=lambda s: nfc(s).lower())
        for fn in sorted(fns, key=lambda s: nfc(s).lower()):
            ap = os.path.join(dp, fn)
            rel = nfc(os.path.relpath(ap, root)).replace(os.sep, '/')
            low = fn.lower()
            if low.endswith(EXTS):
                disk.append({'rel': rel, 'abs': ap, 'zip': False, 'mtime': os.stat(ap).st_mtime})
            elif low.endswith(DATA_EXTS):
                data.append(rel)
                if low.endswith('.txt'):
                    try:
                        with open(ap, 'rb') as f:
                            if f.read(8).startswith(b'{$DS.}'):   # equation snippet of an EES Diagram Window model
                                DS_SNIPPETS.add(rel)
                    except OSError:
                        pass
            elif low.endswith('.zip'):
                try:
                    with open(ap, 'rb') as f:
                        blob = f.read()
                except OSError:
                    continue
                for x in iter_zip(blob, rel):
                    if x['kind'] == 'model':
                        zipped.append({'rel': nfc(x['label']), 'abs': None, 'zip': True,
                                       'bytes': x['bytes'], 'mtime': x['mtime']})
                    elif x['kind'] == 'data':
                        data.append(nfc(x['label']))
                    else:
                        junk.append(nfc(x['label']))
    disk.sort(key=lambda d: (d['rel'].lower(), d['rel']))
    zipped.sort(key=lambda d: (d['rel'].lower(), d['rel']))
    return disk, zipped, data, junk


def analyse_item(it):
    rel = it['rel']
    low = rel.lower()
    b = it['bytes'] if it['zip'] else open(it['abs'], 'rb').read()
    rec = dict(it)
    rec['size'] = len(b)
    rec['raw_hash'] = hashlib.sha1(b).hexdigest()
    rec['error'] = ''
    rec['lkt_strings'] = []
    rec['bin_opt_hint'] = False
    rec['bin'] = {}
    if low.endswith('.ees'):
        rec['format'] = 'ees'
        rec['bin'] = binary_info(b)
        try:
            ver, text, rtf = read_ees_bytes(b)
        except Exception as e:
            ver, text, rtf = '', '', False
            rec['error'] = 'unreadable: %s' % e
        rec.update({'ees_version': clean_version(ver), 'rtf': rtf, 'text': text})
        try:   # weak optimisation hint: Minimize/Maximize strings in the (unreliable) binary tail
            tail = b[20 + struct.unpack('<I', b[16:20])[0]:]
            rec['bin_opt_hint'] = bool(re.search(rb'Minimi[sz]e|Maximi[sz]e', tail))
        except Exception:
            pass
    elif low.endswith('.lib'):
        rec['format'] = 'lib'
        try:
            text = b.decode('cp1252')
        except UnicodeDecodeError:
            text = b.decode('latin1')
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        if '$SB1' in text[:20]:   # compiled-style library: binary header before the first PROCEDURE/FUNCTION
            m = re.search(r'(procedure|function|module|subprogram)\s+[A-Za-z_]', text, re.I)
            if m:
                text = text[m.start():]
        rec.update({'ees_version': '', 'rtf': False, 'text': text})
    else:
        rec['format'] = 'lkt'
        ver = b[1:1 + b[0]].decode('latin1') if b and b[0] < 20 else ''
        rec.update({'ees_version': clean_version(ver), 'rtf': False, 'text': '', 'lkt_strings': lkt_strings(b)})
    rec['a'] = analyse_text(rec['text'], rec['format'])
    rec['text_hash'] = hashlib.sha1(rec['text'].encode('utf-8')).hexdigest() if rec['text'] else rec['raw_hash']
    rec['doc_quality'] = doc_quality_score(rec['a'], rec['format'])
    return rec


# ======================================================================================
# duplicates
# ======================================================================================
class UF:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[max(ra, rb)] = min(ra, rb)


def group_duplicates(recs, thr=0.6, min_lines=4):
    uf = UF(len(recs))
    sets, hashes = [], []
    for r in recs:
        lines = r['a']['norm_lines']
        sets.append(frozenset(lines))
        if r['format'] == 'lkt':
            hashes.append('lkt:' + r['raw_hash'])
        else:
            hashes.append(hashlib.sha1('\n'.join(lines).encode('utf-8')).hexdigest() if lines else None)
        r['norm_hash'] = hashes[-1]
    by_hash = collections.defaultdict(list)
    for i, h in enumerate(hashes):
        if h is not None:
            by_hash[h].append(i)
    for idxs in by_hash.values():
        for j in idxs[1:]:
            uf.union(idxs[0], j)
    inv = collections.defaultdict(list)
    for i, s in enumerate(sets):
        if len(s) >= min_lines:
            for l in s:
                inv[l].append(i)
    cand = collections.Counter()
    for l, idxs in inv.items():
        if len(idxs) > 40:
            continue
        for x in range(len(idxs)):
            for y in range(x + 1, len(idxs)):
                cand[(idxs[x], idxs[y])] += 1
    near = []
    for (a, b), c in cand.items():
        A, B = sets[a], sets[b]
        un = len(A | B)
        j = len(A & B) / un if un else 0.0
        if j >= thr:
            uf.union(a, b)
        elif j >= 0.45:
            near.append((j, a, b))
    comps = collections.defaultdict(list)
    for i in range(len(recs)):
        comps[uf.find(i)].append(i)
    return list(comps.values()), sets, hashes, near


STUDENT_AUTH_RE = re.compile(r'MCI_REMIDICKES/MCI/Examen/MCI_[^/]*juin_2019/|MCI_REMIDICKES/MCI/Labo 2/rapport/')
COPYLIKE_RE = re.compile(r'copie|copy|(^|/)old/|(^|/)save/|backup|(^|/)tmp|sans titre|untitled|\(\d\)|(^|/)~', re.I)
STUDENT_RE = re.compile(r'(^|/)examen?/|examen_|rapport|groupe|student|etudiant|(^|/)exam', re.I)


def rep_key(r):
    a = r['a']
    penalty = (1 if COPYLIKE_RE.search(r['rel']) else 0) + (1 if r['zip'] else 0) + (2 if STUDENT_RE.search(strip_accents(r['rel'])) else 0)
    return (-r['doc_quality'], penalty, -min(a['words'], 800), [-x for x in parse_version(r['ees_version'])],
            -r['mtime'], len(r['rel']), r['rel'])


def jaccard(A, B):
    un = len(A | B)
    return len(A & B) / un if un else 0.0


# ======================================================================================
# heuristic classification (defaults; the curation layer overrides)
# ======================================================================================
CAT_RULES = [
    ('absorption_sorption', r'absorption|libr\b|libr[_-]?h2o|nh3h2o|sorption|desiccant|lithium|brine to|absorbeur'),
    ('hvac_psychrometrics', r'psychro|humid|air humide|moist air|airh2o|air_ha|wet.?bulb|dew.?point|relhum|cooling tower|tour de refroid|cooling coil|heating coil|batterie|\bahu\b|saturation adiabatique|recovery loop|degre de saturation'),
    ('refrigeration_heat_pumps', r'refriger|frigori|heat pump|pompe a chaleur|\bpac\b|chiller|\bcop\b|r134a|r22\b|r410a|r407c|r12\b|r113\b|climatis|air.?cond|machine frigo|koel|warmtepomp|q_dot_ev|t_ev\b'),
    ('power_cycles_vapour', r'rankine|\borc\b|organic|vapeur|steam|kalina|soutirage|centrale|reheat|resurchauffe|feedwater'),
    ('power_cycles_gas', r'brayton|gas turbine|turbine a gaz|turbo.?reacteur|turbojet|jet engine|combined cycle|cycle combine|stirling|ericsson'),
    ('engines', r'otto|diesel|moteur|engine|\bmci\b|cylindree|soupape|suralimentation|turbocompress|detarage|injection|knock|piston engine'),
    ('combustion_boilers', r'combustion|chaudiere|boiler|bruleur|burner|fuel|excess air|exces d.air|pouvoir calorifique|stoichio|flamme|dissociation|cpbar'),
    ('compressors', r'compress|scroll|screw|\bvis\b|reciprocating|piston compressor|roots?\b'),
    ('expanders_turbines', r'expander|expandeur|expanseur|turbin|detente|laval|turbo.?expan'),
    ('pumps_fans', r'\bpump|pompe|\bfan\b|ventilateur|blower|centrifugal|affinity'),
    ('heat_exchangers', r'exchanger|echangeur|\bhx\b|\bntu\b|\blmtd\b|effectiveness|plate heat|recuperat|economiser|regenerat|counterflow|contre.?courant|crossflow|condenser three zones'),
    ('valves_nozzles_piping', r'tuyere|nozzle|\bvalve|vanne|diffuser|diffuseur|\bpipe|tuyau|conduite|perte de charge|pressure drop|\bduct|iso ?5167|orifice|throttl|laminage|venturi'),
    ('storage', r'storage|stockage|ballon|thermal storage|accumul|ice storage|\bpcm\b'),
    ('solar_renewables', r'solar|solaire|photovolta|\bpv\b|wind|eolien|geotherm|ground|collector|capteur'),
    ('buildings', r'building|batiment|thermal conf|confort|\bpmv\b|\bppd\b|envelope|residential|bizone|radiator|cooling ceiling'),
    ('cogeneration_energy_systems', r'cogeneration|\bchp\b|trigeneration|energy system|district|economic|\bnpv\b|rentabilit|investissement|payback|pay-back'),
    ('heat_transfer', r'conduction|convection|rayonnement|radiation|ailette|\bfin\b|nusselt|fourier|resistance thermique|lumped'),
    ('properties', r'propert|proprietes|fluidprop|refprop|equation of state|equation d.etat|van der waals|saturation properties'),
    ('fundamentals', r'first law|premier principe|second law|second principe|entropie|entropy|exergy|exergie|ideal gas|gaz parfait|piston.?cylind|energy balance|bilan d.energie|carnot'),
]


def classify_category(rec):
    a = rec['a']
    blob = strip_accents(' '.join([rec['rel'], a['title'], a['description'], ' '.join(c['text'] for c in a['prose'][:25]),
                                   ' '.join(sorted(a['idents']))])).lower()
    best, bscore = 'misc', 0
    for cat, rx in CAT_RULES:
        n = len(re.findall(rx, blob))
        if n > bscore:
            best, bscore = cat, n
    return best


OPT_RE = re.compile(r'optim|maximi[sz]|minimi[sz]|maximum de|minimum de|best exponent', re.I)


def classify_kind(rec):
    a = rec['a']
    ca = a['ca']
    if rec['format'] == 'lib':
        return 'function'
    if rec['format'] == 'lkt' or (rec['format'] == 'ees' and not rec['text'].strip()):
        return 'unknown'
    if ca['n_eq'] == 0 and (ca['defs'].get('function') or ca['defs'].get('procedure') or ca['defs'].get('module')):
        return 'function'
    if ca['n_eq'] == 0:
        return 'unknown'
    blob = a['title'] + ' ' + a['description']
    if re.search(r'\$integraltable\s+(tau|t|time)\b', rec['text'], re.I) or 'TIME_STEPPING' in a['features']:
        return 'dynamic'
    if OPT_RE.search(blob) and re.search(r'optim', blob, re.I):
        return 'optimization'
    return 'steady'


def classify_level(rec):
    a = rec['a']
    ca = a['ca']
    if rec['format'] == 'lkt':
        return 1
    n = ca['n_eq']
    exp = ca['expanded']
    if rec['format'] == 'lib':
        nd = sum(len(v) for v in ca['defs'].values())
        return 3 if nd >= 6 else 2
    if n >= 500 or exp >= 1000:
        lvl = 4 if n >= 500 else 3
    elif n >= 200:
        lvl = 3
    elif n > 40:
        lvl = 2
    else:
        lvl = 1
    proc = ca['defs'].get('procedure') or ca['defs'].get('function') or ca['defs'].get('module') or ca['defs'].get('subprogram')
    if proc and n + ca['n_alg'] >= 60:
        lvl = max(lvl, 3)
    elif proc and n >= 20:
        lvl = max(lvl, 2)
    return min(lvl, 4)


# Maintainer decision (2026-10-04): every file of this collection comes from the maintainer's
# laboratory and is published under the library license (MIT).  These rules now only give
# authorship hints (credits); the license_status column is always 'own'.
LICENSE_RULES = [
    (r'^thermo_kuleuven/', 'own', 'S. Quoilin (KU Leuven course)'),
    (r'^MCI_REMIDICKES/', 'own', 'P. Ngendakumana; R. Dickes'),
    (r'^Model data bank/', 'own', 'ULiege Thermodynamics Lab (J. Lebrun et al.)'),
    (r'^modeles/LABORELEC_2002/', 'own', 'Felipe Trebilcock (ULiege Thermodynamics Lab, Dec 2002, for Laborelec; reviewers J. Lebrun, E. Winandy)'),
    (r'^modeles/', 'own', 'ULiege Thermodynamics Lab'),
    (r'^machines et systemes thermiques/', 'own', 'ULiege MSTh course (J. Lebrun, V. Lemort, S. Bertagnolio)'),
    (r'^thermodynamique appliquee/2017-2018', 'own', 'ULiege THD course (S. Bertagnolio, S. Borguet)'),
    (r'^thermodynamique appliquee/(2022-2023|Aout 2022)', 'own', 'ULiege course MECA0002 (S. Quoilin; repetition assistants N. Paulus, B. Dechesne per companion Python/Word metadata)'),
    (r'^thermodynamique appliquee/', 'own', 'ULiege Thermodynamics Lab course material'),
]


def default_license(rel):
    for rx, lic, who in LICENSE_RULES:
        if re.search(rx, rel):
            return lic, who
    return 'own', ''


# ======================================================================================
# curation layer
# ======================================================================================
CUR_COLS = ['key', 'scope', 'title', 'description', 'category_guess', 'kind_guess', 'level_guess',
            'priority', 'license_status', 'authors', 'notes', 'doc_quality', 'language']


def load_curation(path):
    rows = []
    if path and os.path.exists(path):
        with open(path, encoding='utf-8', newline='') as f:
            for r in csv.DictReader(f):
                rows.append(r)
    return rows


# ======================================================================================
# main pipeline
# ======================================================================================
PREV = []      # rows of the previous inventory.csv (set by main): keeps the TM-/DG- IDs stable


def assign_ids(recs, dropped=()):
    """A path already in the inventory keeps its TM ID (personal files, whose path is redacted: the k-th
    file of a folder takes the k-th redacted ID of that folder); new files get the next free numbers."""
    by_path = {' '.join(p['path'].split()): p['candidate_id'] for p in PREV if '[redacted ' not in p['path']}
    red = collections.defaultdict(list)
    for p in PREV:
        if '[redacted ' in p['path']:
            red[(p['path'].rsplit('/', 1)[0], p['path'].rsplit('.', 1)[-1])].append(p['candidate_id'])
    for v in red.values():
        v.sort()
    used = set()
    for r in recs:
        if is_personal(r['rel']):
            folder, name = r['rel'].rsplit('/', 1)
            q = red.get((folder, name.rsplit('.', 1)[-1] if '.' in name else ''))
            cid = q.pop(0) if q else None
        else:
            cid = by_path.get(' '.join(r['rel'].split()))     # write_csv collapses blanks
        r['cid'] = cid if cid and cid not in used else None
        if r['cid']:
            used.add(cid)
    keeper = {' '.join(k.split()): r for r in recs for k in [r['rel']] if r['cid'] is None}
    for gone, kept in dropped:           # an inventoried zip member now dropped as a copy of a new file
        cid = by_path.get(' '.join(gone.split()))
        r = keeper.get(' '.join(kept.split()))
        if cid and r is not None and r['cid'] is None and cid not in used:
            r['cid'] = cid
            used.add(cid)
    nxt = max([int(p['candidate_id'][3:]) for p in PREV] + [0]) + 1
    for r in recs:
        if r['cid'] is None:
            r['cid'] = 'TM-%04d' % nxt
            nxt += 1
    lost = sorted({p['candidate_id'] for p in PREV} - used)
    if lost:
        sys.stderr.write('WARNING: %d previous IDs no longer found on disk: %s\n' % (len(lost), ' '.join(lost[:20])))


def build(root, curation_path):
    disk, zipped, datafiles, junk = discover(root)
    recs, dropped = [], []
    seen = {}
    for it in disk:
        r = analyse_item(it)
        recs.append(r)
        seen.setdefault(r['text_hash'], r['rel'])
    for it in zipped:
        r = analyse_item(it)
        if r['text_hash'] in seen:
            dropped.append((r['rel'], seen[r['text_hash']]))
            continue
        seen[r['text_hash']] = r['rel']
        recs.append(r)
    n_disk = len(disk)
    assign_ids(recs, dropped)
    by_rel = {r['rel']: r for r in recs}

    # ---- duplicate groups ----
    comps, sets, hashes, near = group_duplicates(recs)
    comps = [sorted(c) for c in comps]
    comps.sort(key=lambda c: c[0])
    gcount = 0
    old_dg = {p['candidate_id']: p['duplicate_group'] for p in PREV if p.get('duplicate_group')}
    old_rep = {p['candidate_id'] for p in PREV if p.get('is_representative') == 'yes'}
    dg_next = max([int(g[3:]) for g in old_dg.values()] + [0]) + 1
    used_dg = set()
    for comp in comps:
        members = [recs[i] for i in comp]
        was_rep = [r for r in members if r['cid'] in old_rep]     # keep the previous representative
        rep = sorted(was_rep or members, key=rep_key)[0]
        for r in members:
            r['group_size'] = len(comp)
            r['is_rep'] = (r is rep)
            r['rep'] = rep
        if len(comp) > 1:
            prev = collections.Counter(old_dg[r['cid']] for r in members if r['cid'] in old_dg)
            prev = [g for g, _ in prev.most_common() if g not in used_dg]
            if len(prev) > 1:
                sys.stderr.write('note: duplicate groups %s now joined as %s\n' % (', '.join(prev), prev[0]))
            if prev: gid = prev[0]
            else: gid = 'DG-%04d' % dg_next; dg_next += 1
            used_dg.add(gid)
            for r in members:
                r['dgroup'] = gid
                r['jac'] = jaccard(sets[recs.index(r)], sets[recs.index(rep)]) if r is not rep else 1.0
                r['exact'] = (r is not rep and r['norm_hash'] is not None and r['norm_hash'] == rep['norm_hash'])
        else:
            members[0]['dgroup'] = ''
            members[0]['jac'] = 1.0
            members[0]['exact'] = False
    for r in recs:
        r['related'] = []
    for j, a, b in sorted(near, reverse=True):
        if recs[a]['rep'] is recs[b]['rep']:
            continue
        for x, y in ((a, b), (b, a)):
            if len(recs[x]['related']) < 2 and recs[y]['cid'] not in [c for c, _ in recs[x]['related']]:
                recs[x]['related'].append((recs[y]['cid'], j))

    # ---- library function index (for companion / notes) ----
    libidx = {}
    for r in recs:
        if r['format'] == 'lib':
            for kind, names in r['a']['ca']['defs'].items():
                for nme in names:
                    libidx.setdefault(nme.lower(), r)

    def container_of(rel):
        return rel.split('!/', 1)[0] if '!/' in rel else rel.rsplit('/', 1)[0]

    data_by_container = collections.defaultdict(list)
    for d in datafiles:
        data_by_container[container_of(d)].append(d)
    models_by_container = collections.defaultdict(list)
    for r in recs:
        models_by_container[container_of(r['rel'])].append(r)

    for r in recs:
        comp = []
        needs = []
        a = r['a']
        defined = set(n.lower() for v in a['ca']['defs'].values() for n in v)
        used_calls = set(a['ca']['calls'])
        refs = a['refs']
        cont = container_of(r['rel'])
        for o in models_by_container[cont]:
            if o is r or o['format'] not in ('lib', 'lkt'):
                continue
            base = o['rel'].rsplit('/', 1)[-1].lower()
            stem = base.rsplit('.', 1)[0]
            hit = base in refs or stem in refs or any(stem == x.rsplit('.', 1)[0] for x in refs)
            if o['format'] == 'lib' and (used_calls & set(n.lower() for v in o['a']['ca']['defs'].values() for n in v)):
                hit = True
            if o['format'] == 'lkt' and 'LOOKUP' in a['features'] and ('!/' in o['rel'] or cont == container_of(o['rel'])):
                hit = hit or (len([x for x in models_by_container[cont] if x['format'] == 'lkt']) <= 3)
            if hit:
                comp.append(o['rel'].rsplit('/', 1)[-1])
        for d in data_by_container[cont]:
            base = d.rsplit('/', 1)[-1].lower()
            stem = base.rsplit('.', 1)[0]
            if base in refs or stem in refs or (r['format'] == 'ees' and d in DS_SNIPPETS):
                comp.append(d.rsplit('/', 1)[-1])
        r['companions'] = sorted(set(comp))
        unresolved = []
        for c in sorted(used_calls):
            if c in defined:
                continue
            if c in libidx and libidx[c]['rel'] != r['rel']:
                lr = libidx[c]
                if container_of(lr['rel']) != cont:
                    needs.append('%s -> %s (%s)' % (c, lr['rel'].rsplit('/', 1)[-1], lr['cid']))
            else:
                unresolved.append(c)
        r['needs_lib'] = needs
        r['undefined_calls'] = unresolved

    # ---- curation ----
    cur = load_curation(curation_path)
    group_rows = collections.defaultdict(list)   # rep-cid -> rows
    file_rows = {}
    for row in cur:
        key = nfc(row['key'])
        r = by_rel.get(key)
        if r is None:
            print('WARNING: curation key not found: %r' % key, file=sys.stderr)
            continue
        if (row.get('scope') or 'group').strip() == 'file':
            file_rows[r['rel']] = row
        else:
            group_rows[id(r['rep'])].append(row)

    out = []
    for i, r in enumerate(recs):
        a, ca = r['a'], r['a']['ca']
        rep = r['rep']
        gl = group_rows.get(id(rep), [])
        fl = file_rows.get(r['rel'])

        def pick(field, default=''):
            if fl and (fl.get(field) or '').strip():
                return fl[field].strip()
            for row in gl:
                if (row.get(field) or '').strip():
                    return row[field].strip()
            return default

        lic0, who0 = default_license(r['rel'])
        auth_auto = list(a['authors_explicit'])
        have = [x.replace(' (reviewer)', '') for x in auth_auto]
        for nme in initials_from_name(r['rel'].rsplit('/', 1)[-1]):
            if nme not in have:
                auth_auto.append(nme)
        if STUDENT_AUTH_RE.search(r['rel']):
            auth_auto = ['student submission (MCI course)']
        authors = pick('authors', '; '.join(auth_auto) if auth_auto else who0)
        category = pick('category_guess', classify_category(r))
        kind = pick('kind_guess', classify_kind(r))
        level = pick('level_guess', str(classify_level(r)))
        lang = pick('language', a['language'])
        dq = pick('doc_quality', str(r['doc_quality']))
        lic = pick('license_status', lic0)
        lic = 'own'                  # maintainer decision 2026-10-04 (see LICENSE_RULES)
        title = pick('title', '')
        desc = pick('description', '')
        auto_notes = []
        if not title:
            title = a['title'] or os.path.splitext(r['rel'].rsplit('/', 1)[-1])[0]
            auto_notes.append('title/description auto-extracted (not curated)')
            if not desc:
                desc = a['description']
        # priority
        prio = None
        if fl and (fl.get('priority') or '').strip():
            prio = fl['priority'].strip()
        elif r['is_rep']:
            for row in gl:
                if (row.get('priority') or '').strip():
                    prio = row['priority'].strip()
                    break
        if prio is None:
            if not r['is_rep']:
                prio = 'skip' if r.get('exact') else 'low'
            else:
                if r['format'] == 'ees' and (ca['n_eq'] == 0 and not ca['defs']):
                    prio = 'skip'
                elif int(dq) >= 2 and 12 <= ca['n_eq'] <= 400:
                    prio = 'medium'
                else:
                    prio = 'low'
        # auto notes
        if r['zip']:
            auto_notes.append('inside zip archive (not extracted): ' + r['rel'].split('!/')[0].rsplit('/', 1)[-1])
        if r['rtf']:
            auto_notes.append('stored as RTF')
        if r['error']:
            auto_notes.append(r['error'])
        if r['group_size'] > 1:
            if r['is_rep']:
                nex = sum(1 for x in recs if x['rep'] is r and x is not r and x.get('exact'))
                auto_notes.append('representative of %d-file duplicate group%s' % (r['group_size'], ' (%d with identical equations)' % nex if nex else ''))
            elif r.get('exact'):
                auto_notes.append('identical equations to %s' % rep['cid'])
            else:
                auto_notes.append('near-duplicate/variant of %s (Jaccard %.2f)' % (rep['cid'], r['jac']))
        if ca['expanded'] > 1.5 * max(1, ca['n_eq']) and ca['n_dup']:
            auto_notes.append('~%d equations after DUPLICATE expansion' % ca['expanded'])
        if r['related']:
            auto_notes.append('similar but not grouped: ' + ', '.join('%s (J=%.2f)' % (c, j) for c, j in r['related']))
        if r['needs_lib']:
            auto_notes.append('needs library: ' + ', '.join(r['needs_lib']))
        if r['undefined_calls']:
            auto_notes.append('calls external/built-in procedures: ' + ', '.join(r['undefined_calls'][:6]))
        if re.search(r'freely distributed and may not be sold', r['text'], re.I):
            auto_notes.append("carries the lab disclaimer 'freely distributed, may not be sold, cite origin'")
        elif re.search(r'freely used and reproduced as long as', r['text'], re.I):
            auto_notes.append('contains a permissive-use statement (free use/reproduction with credit)')
        if r['bin_opt_hint']:
            auto_notes.append('binary contains Minimize/Maximize strings (weak optimisation hint)')
        num, idlic = parse_id_tag(a['id_tag'])
        if idlic:
            auto_notes.append('EES ID stamp: ' + idlic)
        if r['format'] == 'lkt' and r['lkt_strings']:
            auto_notes.append('binary lookup table; strings: ' + ' / '.join(r['lkt_strings'][:4])[:120])
        notes = '; '.join(auto_notes)
        extra = pick('notes', '')
        if extra:
            notes = extra + ('; ' + notes if notes else '')
        # units & features & fluids
        units = [u for u, _ in a['units'].most_common(8)]
        hints = list(units)
        if a['uses_273']:
            hints.append('+273.15')
        hints.extend(a['unit_infer'] if not units else [])
        feats = [f for f in a['features'] if f not in ('INDEX_SHIFT',)]
        if 'INDEX_SHIFT' in a['features'] and 'DUPLICATE' not in feats:
            feats.append('INDEX_SHIFT')
        if is_personal(r['rel']):
            title, desc = 'Student exam submission (MCI exam, June 2019)', ''
            prio, lic, authors = 'skip', 'own', ''
            notes = ('student answers to the June 2019 MCI exam (duplicates of the exam solution); '
                     'file name redacted (personal data)')
        row = {
            'candidate_id': r['cid'], 'source': 'thermo_models',
            'path': redact(r['rel'], r['cid']) if is_personal(r['rel']) else r['rel'],
            'companion_files': ';'.join(r['companions']), 'title': title, 'description': desc,
            'category_guess': category, 'kind_guess': kind, 'level_guess': level, 'language': lang,
            'format': r['format'], 'ees_version': r['ees_version'], 'n_lines': a['n_lines'],
            'n_equations': ca['n_eq'], 'features': ';'.join(feats), 'unit_hints': ';'.join(hints),
            'fluids': ';'.join(a['fluids'][:8]), 'doc_quality': dq, 'duplicate_group': r['dgroup'],
            'is_representative': 'yes' if r['is_rep'] else 'no', 'priority': prio,
            'license_status': lic, 'authors': authors, 'notes': notes,
            'ees_units': r['bin'].get('ees_units', ''), 'stored_solution': r['bin'].get('stored_solution', ''),
            'tables': r['bin'].get('tables', ''),
            'decision': 'discarded' if is_personal(r['rel']) else 'todo', 'library_id': '',
        }
        if is_personal(r['rel']):
            row['companion_files'] = ''
        for k in row:
            if isinstance(row[k], str):
                row[k] = re.sub(r'\s+', ' ', row[k].replace('\n', ' ')).strip()
        out.append(row)
    return out, recs, dropped, junk, n_disk


def write_csv(rows, path):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow(r)


def print_stats(rows, recs, dropped, junk, n_disk):
    top = lambda p: p.split('/')[0]
    print('rows: %d (on disk: %d, zip members kept: %d); redundant zip members dropped: %d; junk ignored: %d' % (
        len(rows), n_disk, len(rows) - n_disk, len(dropped), len(junk)))
    for col in ('format', 'category_guess', 'kind_guess', 'level_guess', 'priority', 'license_status', 'language',
                'doc_quality', 'is_representative'):
        print('\n== %s' % col)
        for k, v in collections.Counter(r[col] for r in rows).most_common():
            print('  %-32s %d' % (k, v))
    print('\n== by top folder')
    for k, v in sorted(collections.Counter(top(r['path']) for r in rows).items()):
        print('  %-36s %d' % (k, v))
    groups = collections.Counter(r['duplicate_group'] for r in rows if r['duplicate_group'])
    print('\nduplicate groups (>=2 files): %d covering %d files; singletons: %d' % (
        len(groups), sum(groups.values()), sum(1 for r in rows if not r['duplicate_group'])))
    print('representatives: %d' % sum(1 for r in rows if r['is_representative'] == 'yes'))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', default=DEFAULT_ROOT)
    ap.add_argument('--out', default=HERE)
    ap.add_argument('--curation', default=os.path.join(HERE, 'curation.csv'))
    ap.add_argument('--stats', action='store_true')
    args = ap.parse_args()
    previous = os.path.join(args.out, 'inventory.csv')
    old = {}
    if os.path.exists(previous):                       # keep the IDs and the workflow's manual columns
        with open(previous, encoding='utf-8', newline='') as f:
            PREV.extend(csv.DictReader(f))
        old = {' '.join(r['path'].split()): r for r in PREV}
    rows, recs, dropped, junk, n_disk = build(args.root, args.curation)
    rows.sort(key=lambda r: r['candidate_id'])          # previous rows first, new files appended
    prev_by_id = {p['candidate_id']: p for p in PREV}
    for i, r in enumerate(rows):          # a row already inventoried is kept as it is (workers' notes and
        p = prev_by_id.get(r['candidate_id'])                # decisions); only a group change is recorded
        if not p:
            continue
        if ' '.join(p['path'].split()) != ' '.join(r['path'].split()):
            r['decision'], r['library_id'] = p['decision'], p['library_id']
            r['notes'] = (r['notes'] + '; ' if r['notes'] else '') + 'sweep %s: file now at this path (was %s)' % (
                time.strftime('%Y-%m-%d'), p['path'])
            continue
        keep = dict(p)
        if p['duplicate_group'] != r['duplicate_group']:
            keep['duplicate_group'] = r['duplicate_group']
            keep['notes'] = (p['notes'] + '; ' if p['notes'] else '') + 'sweep %s: duplicate group %s -> %s' % (
                time.strftime('%Y-%m-%d'), p['duplicate_group'] or '-', r['duplicate_group'] or '-')
        rows[i] = keep
    os.makedirs(args.out, exist_ok=True)
    if old:
        for r in rows:
            o = old.get(' '.join(r['path'].split()))
            if o and o.get('decision'):
                r['decision'], r['library_id'] = o['decision'], o.get('library_id', '')
    write_csv(rows, os.path.join(args.out, 'inventory.csv'))
    print('wrote %s (%d rows)' % (os.path.join(args.out, 'inventory.csv'), len(rows)))
    if args.stats:
        print_stats(rows, recs, dropped, junk, n_disk)


if __name__ == '__main__':
    main()
