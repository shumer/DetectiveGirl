"""Regenerate every case JSON from scripts/cases/*.py and rebuild docs/stories.ru.md."""
import importlib, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, 'cases'))
from common import render
IDS = ['owl', 'forest', 'cloud', 'museum', 'greenhouse', 'theatre', 'aquarium', 'bakery', 'lighthouse', 'library', 'park']
for case_id in IDS:
    mod = importlib.import_module(case_id)
    number = {'owl': '001', 'forest': '002', 'cloud': '003', 'museum': '004', 'greenhouse': '005', 'theatre': '006', 'aquarium': '007', 'bakery': '008', 'lighthouse': '009', 'library': '010', 'park': '011'}[case_id]
    mod.write_case(case_id, number, mod.L, mod.variants())
kinds = {'choice': 'выбор из вариантов', 'multi': 'отметить нескольких', 'order': 'порядок карточек', 'time': 'время', 'number': 'число'}
lines = ["# Игровые сценарии", "", "Одиннадцать дел, доступных в игре на русском, польском, английском и украинском. Уровень: 11 лет. В каждом деле есть вопрос «кто, что или почему», подозреваемые или версии, ложный след и математика 5 класса.", "", "У каждого дела четыре партии: один сюжет и четыре набора чисел с разными ответами. При запуске дела выбирается случайная партия из ещё не пройденных. Ниже показана партия 1; остальные три отличаются только числами и ответами. Файл собран автоматически из `scripts/cases/*.py` командой `python3 scripts/build_cases.py`.", ""]
for case_id in IDS:
    story = json.load(open(os.path.join(here, '..', 'app', 'revised', f'{case_id}.json')))
    t = story['locales']['ru']; var = story['variants'][0]; vals = var['values']; R = lambda s: render(s, vals, 'ru')
    lines += [f"## {story['number']}. {R(t['title'])}", "", R(t['intro']), ""]
    for i, st in enumerate(t['steps'], 1):
        lines += [f"### Шаг {i}. {R(st['title'])}", "", R(st['situation']), ""]
        lines += [f"- {R(e)}" for e in st['evidence']] + [""]
        lines += [f"{R(st['question'])} ({kinds[st['kind']]})", ""]
        if st['options']: lines += [f"{j + 1}. {R(o)}" for j, o in enumerate(st['options'])] + [""]
        ans = var['answers'][i - 1]
        if st['kind'] == 'choice': ans_s = R(st['options'][ans])
        elif st['kind'] in ('multi', 'order'): ans_s = (', ' if st['kind'] == 'multi' else ' → ').join(R(st['options'][k]) for k in ans)
        else: ans_s = str(ans)
        lines += [f"Ответ: {ans_s}.", "", R(st['explanation']), "", f"Вывод: {R(st['outcome'])}", "", f"Переход: {R(st['next'])}", "", "Подсказки:", ""] + [f"- {R(h)}" for h in st['hints']]
        if st['kind'] == 'choice':
            lines += ["", "Обратная связь на неверные варианты:", ""] + [f"- {R(st['options'][j])}: {R(fb)}" for j, fb in enumerate(st['feedback']) if fb]
        lines += [""]
    other = ', '.join(json.dumps([a for a in v['answers'] if not isinstance(a, list)], ensure_ascii=False) for v in story['variants'][1:])
    lines += ["### Развязка", "", R(t['ending']), "", R(t['question']), "", f"Ответы партий 2-4 (без карточек): {other}", ""]
open(os.path.join(here, '..', 'docs', 'stories.ru.md'), 'w').write("\n".join(lines))
print('docs/stories.ru.md rebuilt')
