"""Shared helpers for case generators: time maths, template rendering and JSON output."""
import json, random, re, os, sys
LANGS = ['ru', 'pl', 'en', 'uk']
def T(hhmm):
    h, m = hhmm.split(':'); return int(h) * 60 + int(m)
def hm(minutes):
    return f"{minutes // 60:02d}:{minutes % 60:02d}"
def add(hhmm, delta):
    return hm(T(hhmm) + delta)
def plural(n, lang, forms):
    if len(forms) == 1: return forms[0]
    a = abs(n); last, last2 = int(a) % 10, int(a) % 100
    if lang == 'en': return forms[0] if a == 1 else forms[-1]
    if len(forms) == 2: return forms[0] if last == 1 and last2 != 11 else forms[1]
    if a != int(a): return forms[1]
    if last == 1 and last2 != 11: return forms[0]
    if 2 <= last <= 4 and not 12 <= last2 <= 14: return forms[1]
    return forms[2]
def fmt(value, lang):
    if isinstance(value, str): return value
    if isinstance(value, float) and value == int(value): value = int(value)
    if isinstance(value, int): return str(value)
    return str(value) if lang == 'en' else str(value).replace('.', ',')
PLACEHOLDER = re.compile(r"\{([a-zA-Z0-9_]+)((?:\|[^{}|]*)*)\}")
INDEXED = re.compile(r"\{([a-zA-Z0-9_]+)#([^{}]*)\}")
def render(template, values, lang):
    def pick(m):
        key, items = m.group(1), m.group(2).split('|')
        if key not in values: raise KeyError(f"missing value {key} in: {template[:60]}")
        idx = int(values[key]); assert 0 <= idx < len(items), (key, idx, template[:60])
        return items[idx]
    template = INDEXED.sub(pick, template)
    def sub(m):
        key, forms = m.group(1), m.group(2)
        if key not in values: raise KeyError(f"missing value {key} in: {template[:60]}")
        if not forms: return fmt(values[key], lang)
        return f"{fmt(values[key], lang)} {plural(float(values[key]), lang, forms[1:].split('|'))}"
    return PLACEHOLDER.sub(sub, template)
def step(title, situation, evidence, question, kind, options, feedback, explanation, outcome, next_, hints, scene):
    return dict(title=title, situation=situation, evidence=evidence, question=question, kind=kind, options=options, feedback=feedback, explanation=explanation, outcome=outcome, next=next_, hints=hints, scene=scene)
def shuffled_orders(case_id, index, steps):
    """Deterministic option order per step for one variant; None for typed answers."""
    orders = []
    for i, st in enumerate(steps):
        if st['kind'] in ('choice', 'multi', 'order'):
            order = list(range(len(st['options'])))
            random.Random(f"{case_id}-{index}-{i}").shuffle(order)
            orders.append(order)
        else:
            orders.append(None)
    return orders
def write_case(case_id, number, locales, variants):
    """Validate templates against every variant and write app/revised/<id>.json."""
    assert len(variants) == 4, 'four variants per case'
    root = os.path.join(os.path.dirname(__file__), '..', '..', 'app', 'revised')
    for lang in LANGS:
        loc = locales[lang]
        assert len(loc['steps']) == 4
        for v, var in enumerate(variants):
            used = set()
            def check(text):
                for m in PLACEHOLDER.finditer(text): used.add(m.group(1))
                for m in INDEXED.finditer(text): used.add(m.group(1))
                out = render(text, var['values'], lang)
                assert '{' not in out and '}' not in out, out
                return out
            for field in ('title', 'intro', 'ending', 'question'): check(loc[field])
            for i, st in enumerate(loc['steps']):
                for field in ('title', 'situation', 'question', 'explanation', 'outcome', 'next'): check(st[field])
                for text in st['evidence'] + st['options'] + st['feedback'] + st['hints']: check(text)
                assert len(st['hints']) == 3
                ans = var['answers'][i]
                if st['kind'] == 'choice':
                    assert len(st['options']) >= 4 and isinstance(ans, int) and 0 <= ans < len(st['options']), (lang, i, ans)
                    assert len(st['feedback']) == len(st['options'])
                    for j, fb in enumerate(st['feedback']): assert bool(fb.strip()) == (j != ans), (lang, i, j, 'feedback must be empty only for the right option')
                elif st['kind'] == 'multi':
                    assert isinstance(ans, list) and 0 < len(ans) < len(st['options'])
                elif st['kind'] == 'order':
                    assert sorted(ans) == list(range(len(st['options'])))
                else:
                    text = str(ans)
                    for h in st['hints']:
                        assert text not in render(h, var['values'], lang), (lang, i, 'hint reveals answer', h)
            if lang == 'ru':
                unused = set(var['values']) - used
                assert not unused, f"unused values in variant {v}: {sorted(unused)}"
    # Variants must actually differ.
    signatures = [json.dumps(v['answers'], ensure_ascii=False) for v in variants]
    assert len(set(signatures)) == 4, 'variants must have different answers'
    steps0 = locales['ru']['steps']
    # Keep the round 1 answer on every step for tooling that reads a single answer.
    for lang in LANGS:
        for i, st in enumerate(locales[lang]['steps']): st['answer'] = variants[0]['answers'][i]
    for i, var in enumerate(variants):
        var.setdefault('orders', shuffled_orders(case_id, i, steps0))
    story = {'id': case_id, 'number': number, 'variants': variants, 'locales': locales}
    path = os.path.join(root, f'{case_id}.json')
    with open(path, 'w') as f:
        json.dump(story, f, ensure_ascii=False, indent=1); f.write('\n')
    print(f'{case_id}: ok, {len(variants)} variants')
