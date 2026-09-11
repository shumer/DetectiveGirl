from common import step, write_case
def secs(mark):
    m, s = mark.split(':'); return int(m) * 60 + int(s)
NOTES = 4  # MI, SOL, DO, RE as card indices 2, 0, 1, 3
def variants():
    out = []
    data = [
        dict(lt='0:47', st='1:05', w=3, rep=6, bar=8, fr={'mi': '1/4', 'sol': '1/2', 'do': '3/4', 're': '3/8'}, den=1, rp=3, pz=2),
        dict(lt='0:52', st='1:16', w=4, rep=6, bar=12, fr={'mi': '1/3', 'sol': '1/4', 'do': '1/2', 're': '5/12'}, den=2, rp=3, pz=3),
        dict(lt='1:10', st='1:22', w=3, rep=4, bar=8, fr={'mi': '1/2', 'sol': '3/4', 'do': '1/4', 're': '5/8'}, den=1, rp=4, pz=2),
        dict(lt='0:38', st='0:58', w=5, rep=4, bar=8, fr={'mi': '1/8', 'sol': '3/4', 'do': '1/2', 're': '3/8'}, den=1, rp=2, pz=5),
    ]
    from fractions import Fraction
    for d in data:
        delay = secs(d['st']) - secs(d['lt']); assert d['w'] * d['rep'] == delay
        dur = {k: Fraction(v) * d['bar'] for k, v in d['fr'].items()}
        assert all(x.denominator == 1 for x in dur.values()); dur = {k: int(v) for k, v in dur.items()}
        assert len(set(dur.values())) == 4
        names = ['mi', 'sol', 'do', 're']  # Index for {n#МИ|СОЛЬ|ДО|РЕ}.
        order_names = sorted(names, key=lambda k: dur[k])
        cards = ['sol', 'do', 'mi', 're']  # Card order as shown in the options.
        answer = [cards.index(k) for k in order_names]
        greet = sum(dur.values()); pauses = d['rp'] - 1; tot1 = d['rp'] * greet; tot2 = pauses * d['pz']; total = tot1 + tot2
        v = dict(lt=d['lt'], st=d['st'], lsec=secs(d['lt']), ssec=secs(d['st']), delay=delay, w=d['w'], rep=d['rep'], pa=2,
                 bar=d['bar'], fmi=d['fr']['mi'], fsol=d['fr']['sol'], fdo=d['fr']['do'], fre=d['fr']['re'], smi=dur['mi'], ssol=dur['sol'], sdo=dur['do'], sre=dur['re'], den=d['den'],
                 n1=names.index(order_names[0]), n2=names.index(order_names[1]), n3=names.index(order_names[2]), n4=names.index(order_names[3]),
                 s1=dur[order_names[0]], s2=dur[order_names[1]], s3=dur[order_names[2]], s4=dur[order_names[3]],
                 greet=greet, rp=d['rp'], pauses=pauses, pz=d['pz'], tot1=tot1, tot2=tot2, total=total)
        out.append({'values': v, 'answers': [str(delay), 0, answer, str(total)]})
    return out
NR = "{n1#МИ|СОЛЬ|ДО|РЕ}, {n2#МИ|СОЛЬ|ДО|РЕ}, {n3#МИ|СОЛЬ|ДО|РЕ}, {n4#МИ|СОЛЬ|ДО|РЕ}"
NP = "{n1#MI|SOL|DO|RE}, {n2#MI|SOL|DO|RE}, {n3#MI|SOL|DO|RE}, {n4#MI|SOL|DO|RE}"
NU = "{n1#МІ|СОЛЬ|ДО|РЕ}, {n2#МІ|СОЛЬ|ДО|РЕ}, {n3#МІ|СОЛЬ|ДО|РЕ}, {n4#МІ|СОЛЬ|ДО|РЕ}"
L = {}
L['ru'] = {
 "title": "Маяк, который забыл мелодию",
 "intro": "Игрушечный маяк встречает гостей огоньком и короткой мелодией. Ася вчера правила программу, а сегодня звук запаздывает и ноты идут не в том порядке. Её брат говорит, что дело в проводе динамика, который он вчера задел. Помоги по видеозаписи и карточке мелодии вернуть приветствие и проверить его по контрольной записи.",
 "ending": "Звук запаздывал на {delay|секунду|секунды|секунд} из-за {rep} тестовых ожиданий по {w|секунде|секунды|секунд}, которые Ася забыла убрать. Провод брата был ни при чём: плохой провод не даёт одну и ту же задержку каждый раз. Ноты вернули в порядок от короткой к длинной: " + NR + ". Одно приветствие длится {greet|секунду|секунды|секунд}, а вся программа из {rp} приветствий и {pauses|паузы|пауз|пауз} {total|секунду|секунды|секунд}, ровно как на контрольной записи.",
 "question": "Брат действительно задел провод. Почему эта версия не объясняла задержку?",
 "steps": [
  step("Насколько запаздывает звук?", "У маяка Ася включает видеозапись сегодняшнего приветствия. На записи есть отметки времени файла, и Ася нашла два момента.",
   ["Огонёк загорается на отметке {lt} файла.", "Первая нота слышна на отметке {st} файла.", "По плану свет и звук должны начинаться одновременно."],
   "На сколько секунд запаздывает звук? Введи число.", "number", [], [],
   "{st} это {ssec} секунд, {lt} это {lsec} секунд. {ssec} - {lsec} = {delay} секунд.",
   "Звук отстаёт ровно на {delay|секунду|секунды|секунд}, и на трёх повторах записи задержка одинаковая. Посмотрим, откуда в программе звука берётся столько секунд.", "Открыть программу звука",
   ["Переведи обе отметки в секунды.", "Отметка вида минуты:секунды. Умножь минуты на 60 и прибавь секунды.", "Вычти момент света из момента звука."], 0),
  step("Где лишнее ожидание?", "На экране программа звука по командам. Световая программа начинает сразу. Брат Аси настаивает на проводе. Проверь, что из этого даёт задержку ровно в {delay|секунду|секунды|секунд}, и каждый раз одинаковую.",
   ["Команда 1: ждать {w|секунду|секунды|секунд}, повторить {rep|раз|раза|раз}.", "Команда 2: сыграть приветствие.", "Команда 3: после приветствия ждать {pa} секунды перед повтором.", "Брат вчера задел провод динамика, провод сидит неплотно.", "На трёх повторах записи задержка каждый раз ровно {delay|секунда|секунды|секунд}."],
   "Что объясняет задержку первого звука?", "choice", ["{rep|ожидание|ожидания|ожиданий} по {w|секунде|секунды|секунд} перед приветствием", "Команда сыграть приветствие", "Пауза {pa} секунды после приветствия", "Неплотный провод динамика"],
   ["", "Эта команда начинает звук, а не задерживает его.", "Эта пауза идёт после приветствия и не может задержать его начало.", "Неплотный провод даёт треск или тишину, но не ровно {delay|секунду|секунды|секунд} каждый раз."],
   "Команда 1 стоит до звука и длится {w} × {rep} = {delay} секунд, ровно как задержка. Команда 2 начинает звук, команда 3 выполняется после него. Провод не даёт одинаковую задержку на каждом повторе.",
   "Ася вспоминает: она вставила тестовое ожидание, чтобы проверять свет, и забыла его убрать. Команду 1 удаляют, свет и звук начинают вместе. Теперь порядок нот.", "Сверить карточку мелодии",
   ["Ищи то, что стоит до первого звука.", "Задержка одинаковая на каждом повторе: сбой провода так не работает.", "Сколько секунд дают все повторы команды 1?"], 1),
  step("В каком порядке звучат ноты?", "На карточке Аси записано правило этого приветствия: звуки идут от самого короткого к самому длинному. Длительности даны в долях одного такта.",
   ["Один такт длится {bar} секунд.", "МИ занимает {fmi} такта, СОЛЬ {fsol} такта, ДО {fdo} такта, РЕ {fre} такта.", "Каждый звук звучит один раз."],
   "Расставь звуки по правилу карточки, от короткого к длинному.", "order", ["СОЛЬ, {fsol} такта", "ДО, {fdo} такта", "МИ, {fmi} такта", "РЕ, {fre} такта"], [],
   "Такт {bar} секунд, значит в секундах: МИ {smi}, СОЛЬ {ssol}, ДО {sdo}, РЕ {sre}. Порядок от короткого к длинному: " + NR + ".",
   "Ася сохраняет порядок " + NR + ". Одно приветствие длится {s1} + {s2} + {s3} + {s4} = {greet} секунд. Осталось проверить всю программу по контрольной записи.", "Рассчитать всю программу",
   ["Приведи все доли к одному знаменателю, например к {den#четвертям|восьмым|двенадцатым|шестнадцатым}.", "Или переведи доли в секунды: один такт это {bar} секунд, умножь каждую долю на {bar}.", "Сравни четыре получившихся числа и расставь звуки по возрастанию."], 2),
  step("Сколько длится всё приветствие?", "Программа повторяет восстановленное приветствие несколько раз. У Аси есть контрольная запись правильной программы, и по длительности можно проверить, всё ли восстановлено.",
   ["Одно приветствие длится {greet|секунду|секунды|секунд}.", "Приветствие звучит {rp|раз|раза|раз}.", "Между соседними приветствиями пауза {pz|секунда|секунды|секунд}. Перед первым и после последнего пауз нет.", "Контрольная запись правильной программы длится {total|секунду|секунды|секунд}."],
   "Сколько секунд займёт восстановленная программа? Введи число.", "number", [], [],
   "{rp} приветствия: {rp} × {greet} = {tot1} секунд. {pauses|пауза|паузы|пауз}: {pauses} × {pz} = {tot2} секунд. Всего {total} секунд, как на контрольной записи.",
   "Длительность совпала с контрольной записью. Ася запускает маяк: свет и звук вместе, ноты по порядку, брат оправдан.", "Запустить приветствие",
   ["Сначала длительность одного приветствия из четырёх звуков.", "Приветствий {rp}, но пауз между ними только {pauses}.", "Сложи звуки и паузы."], 3)
 ]}
L['pl'] = {
 "title": "Latarnia, która zapomniała melodii",
 "intro": "Zabawkowa latarnia morska wita gości światełkiem i krótką melodią. Asia wczoraj poprawiała program, a dziś dźwięk się spóźnia i nuty idą w złej kolejności. Jej brat mówi, że chodzi o przewód głośnika, który wczoraj zaczepił. Pomóż na podstawie nagrania i karty melodii przywrócić powitanie i sprawdzić je z nagraniem kontrolnym.",
 "ending": "Dźwięk spóźniał się o {delay|sekundę|sekundy|sekund} przez {rep} testowych oczekiwań po {w|sekundzie|sekundy|sekund}, których Asia zapomniała usunąć. Przewód brata nie miał z tym nic wspólnego: zły przewód nie daje za każdym razem tego samego opóźnienia. Nuty wróciły do kolejności od krótkiej do długiej: " + NP + ". Jedno powitanie trwa {greet|sekundę|sekundy|sekund}, a cały program z {rp} powitań i {pauses|przerwy|przerw|przerw} {total|sekundę|sekundy|sekund}, dokładnie jak na nagraniu kontrolnym.",
 "question": "Brat naprawdę zaczepił przewód. Dlaczego ta wersja nie wyjaśniała opóźnienia?",
 "steps": [
  step("O ile spóźnia się dźwięk?", "Przy latarni Asia włącza nagranie dzisiejszego powitania. Na nagraniu są znaczniki czasu pliku i Asia znalazła dwa momenty.",
   ["Światełko zapala się na znaczniku {lt} pliku.", "Pierwszą nutę słychać na znaczniku {st} pliku.", "Według planu światło i dźwięk mają zaczynać się jednocześnie."],
   "O ile sekund spóźnia się dźwięk? Wpisz liczbę.", "number", [], [],
   "{st} to {ssec} sekund, {lt} to {lsec} sekund. {ssec} - {lsec} = {delay} sekund.",
   "Dźwięk spóźnia się dokładnie o {delay|sekundę|sekundy|sekund} i na trzech powtórzeniach nagrania opóźnienie jest takie samo. Zobaczmy, skąd w programie dźwięku bierze się tyle sekund.", "Otwórz program dźwięku",
   ["Zamień oba znaczniki na sekundy.", "Znacznik ma postać minuty:sekundy. Pomnóż minuty przez 60 i dodaj sekundy.", "Odejmij moment światła od momentu dźwięku."], 0),
  step("Gdzie jest zbędne oczekiwanie?", "Na ekranie jest program dźwięku po komendach. Program światła zaczyna od razu. Brat Asi upiera się przy przewodzie. Sprawdź, co z tego daje opóźnienie dokładnie {delay|sekundę|sekundy|sekund}, i to za każdym razem takie samo.",
   ["Komenda 1: czekać {w|sekundę|sekundy|sekund}, powtórzyć {rep|raz|razy|razy}.", "Komenda 2: zagrać powitanie.", "Komenda 3: po powitaniu czekać {pa} sekundy przed powtórzeniem.", "Brat wczoraj zaczepił przewód głośnika, przewód siedzi luźno.", "Na trzech powtórzeniach nagrania opóźnienie za każdym razem wynosi dokładnie {delay|sekundę|sekundy|sekund}."],
   "Co wyjaśnia opóźnienie pierwszego dźwięku?", "choice", ["{rep|oczekiwanie|oczekiwania|oczekiwań} po {w|sekundzie|sekundy|sekund} przed powitaniem", "Komenda zagrania powitania", "Przerwa {pa} sekundy po powitaniu", "Luźny przewód głośnika"],
   ["", "Ta komenda zaczyna dźwięk, a nie go opóźnia.", "Ta przerwa jest po powitaniu i nie może opóźnić jego początku.", "Luźny przewód daje trzaski albo ciszę, ale nie dokładnie {delay|sekundę|sekundy|sekund} za każdym razem."],
   "Komenda 1 stoi przed dźwiękiem i trwa {w} × {rep} = {delay} sekund, dokładnie tyle co opóźnienie. Komenda 2 zaczyna dźwięk, komenda 3 wykonuje się po nim. Przewód nie daje takiego samego opóźnienia przy każdym powtórzeniu.",
   "Asia przypomina sobie: wstawiła testowe oczekiwanie, żeby sprawdzać światło, i zapomniała je usunąć. Komenda 1 zostaje usunięta, światło i dźwięk zaczynają razem. Teraz kolejność nut.", "Sprawdź kartę melodii",
   ["Szukaj tego, co stoi przed pierwszym dźwiękiem.", "Opóźnienie jest takie samo przy każdym powtórzeniu: awaria przewodu tak nie działa.", "Ile sekund dają wszystkie powtórzenia komendy 1?"], 1),
  step("W jakiej kolejności brzmią nuty?", "Na karcie Asi zapisano regułę tego powitania: dźwięki idą od najkrótszego do najdłuższego. Długości podano w częściach jednego taktu.",
   ["Jeden takt trwa {bar} sekund.", "MI zajmuje {fmi} taktu, SOL {fsol} taktu, DO {fdo} taktu, RE {fre} taktu.", "Każdy dźwięk brzmi raz."],
   "Ustaw dźwięki według reguły z karty, od krótkiego do długiego.", "order", ["SOL, {fsol} taktu", "DO, {fdo} taktu", "MI, {fmi} taktu", "RE, {fre} taktu"], [],
   "Takt trwa {bar} sekund, więc w sekundach: MI {smi}, SOL {ssol}, DO {sdo}, RE {sre}. Kolejność od krótkiego do długiego: " + NP + ".",
   "Asia zapisuje kolejność " + NP + ". Jedno powitanie trwa {s1} + {s2} + {s3} + {s4} = {greet} sekund. Zostało sprawdzić cały program z nagraniem kontrolnym.", "Oblicz cały program",
   ["Sprowadź wszystkie części do wspólnego mianownika, na przykład do {den#czwartych|ósmych|dwunastych|szesnastych}.", "Albo zamień części na sekundy: jeden takt to {bar} sekund, pomnóż każdą część przez {bar}.", "Porównaj cztery otrzymane liczby i ustaw dźwięki rosnąco."], 2),
  step("Ile trwa całe powitanie?", "Program powtarza przywrócone powitanie kilka razy. Asia ma nagranie kontrolne poprawnego programu i po długości można sprawdzić, czy wszystko zostało przywrócone.",
   ["Jedno powitanie trwa {greet|sekundę|sekundy|sekund}.", "Powitanie brzmi {rp|raz|razy|razy}.", "Między sąsiednimi powitaniami jest przerwa {pz|sekunda|sekundy|sekund}. Przed pierwszym i po ostatnim przerw nie ma.", "Nagranie kontrolne poprawnego programu trwa {total|sekundę|sekundy|sekund}."],
   "Ile sekund zajmie przywrócony program? Wpisz liczbę.", "number", [], [],
   "{rp} powitania: {rp} × {greet} = {tot1} sekund. {pauses|przerwa|przerwy|przerw}: {pauses} × {pz} = {tot2} sekund. Razem {total} sekund, jak na nagraniu kontrolnym.",
   "Długość zgadza się z nagraniem kontrolnym. Asia uruchamia latarnię: światło i dźwięk razem, nuty po kolei, brat uniewinniony.", "Uruchom powitanie",
   ["Najpierw długość jednego powitania z czterech dźwięków.", "Powitań jest {rp}, ale przerw między nimi tylko {pauses}.", "Dodaj dźwięki i przerwy."], 3)
 ]}
L['en'] = {
 "title": "The Lighthouse That Forgot Its Tune",
 "intro": "A toy lighthouse greets visitors with a light and a short tune. Asya edited the program yesterday, and today the sound comes late and the notes play in the wrong order. Her brother says the problem is the speaker cable he knocked yesterday. Help restore the greeting from the video recording and the melody card, and check it against the reference recording.",
 "ending": "The sound was {delay} seconds late because of {rep} {w}-second test waits that Asya forgot to remove. Her brother’s cable had nothing to do with it: a faulty cable does not give the same delay every time. The notes went back into order from shortest to longest: " + NP + ". One greeting lasts {greet} seconds, and the whole program of {rp} greetings and {pauses} pauses lasts {total} seconds, exactly like the reference recording.",
 "question": "The brother really did knock the cable. Why did that theory not explain the delay?",
 "steps": [
  step("How late is the sound?", "At the lighthouse, Asya plays the video of today’s greeting. The recording has file time marks, and Asya has found two moments.",
   ["The light comes on at the {lt} mark of the file.", "The first note is heard at the {st} mark of the file.", "According to the plan, the light and the sound should start at the same time."],
   "How many seconds late is the sound? Enter a number.", "number", [], [],
   "{st} is {ssec} seconds, {lt} is {lsec} seconds. {ssec} - {lsec} = {delay} seconds.",
   "The sound is exactly {delay} seconds behind, and the delay is the same on all three repeats in the recording. Let’s see where that many seconds come from in the sound program.", "Open the sound program",
   ["Convert both marks to seconds.", "A mark reads minutes:seconds. Multiply the minutes by 60 and add the seconds.", "Subtract the light moment from the sound moment."], 0),
  step("Where is the extra wait?", "The screen shows the sound program command by command. The light program starts immediately. Asya’s brother insists on the cable. Check which of these gives a delay of exactly {delay} seconds, the same every time.",
   ["Command 1: wait {w} seconds, repeat {rep} times.", "Command 2: play the greeting.", "Command 3: after the greeting, wait {pa} seconds before repeating.", "Yesterday the brother knocked the speaker cable, and it sits loosely.", "On all three repeats in the recording the delay is exactly {delay} seconds every time."],
   "What explains the delay of the first sound?", "choice", ["{rep} {w}-second waits before the greeting", "The command to play the greeting", "The {pa}-second pause after the greeting", "The loose speaker cable"],
   ["", "This command starts the sound; it does not delay it.", "This pause comes after the greeting and cannot delay its start.", "A loose cable gives crackle or silence, not exactly {delay} seconds every time."],
   "Command 1 comes before the sound and lasts {w} × {rep} = {delay} seconds, exactly the delay. Command 2 starts the sound, and command 3 runs after it. A cable does not give an identical delay on every repeat.",
   "Asya remembers: she inserted a test wait to check the light and forgot to remove it. Command 1 is deleted, and the light and sound start together. Now for the order of the notes.", "Check the melody card",
   ["Look for whatever comes before the first sound.", "The delay is identical on every repeat: a cable fault does not behave like that.", "How many seconds do all the repeats of command 1 add up to?"], 1),
  step("In what order do the notes play?", "Asya’s card states the rule for this greeting: the notes go from the shortest to the longest. The lengths are given as fractions of one bar.",
   ["One bar lasts {bar} seconds.", "MI takes {fmi} of a bar, SOL {fsol} of a bar, DO {fdo} of a bar, RE {fre} of a bar.", "Each note plays once."],
   "Arrange the notes by the card’s rule, from shortest to longest.", "order", ["SOL, {fsol} bar", "DO, {fdo} bar", "MI, {fmi} bar", "RE, {fre} bar"], [],
   "A bar is {bar} seconds, so in seconds: MI {smi}, SOL {ssol}, DO {sdo}, RE {sre}. The order from shortest to longest is " + NP + ".",
   "Asya saves the order " + NP + ". One greeting lasts {s1} + {s2} + {s3} + {s4} = {greet} seconds. All that remains is to check the whole program against the reference recording.", "Work out the whole program",
   ["Bring all the fractions to a common denominator, for example {den#quarters|eighths|twelfths|sixteenths}.", "Or convert the fractions to seconds: one bar is {bar} seconds, so multiply each fraction by {bar}.", "Compare the four numbers you get and arrange the notes in increasing order."], 2),
  step("How long is the whole greeting?", "The program repeats the restored greeting several times. Asya has a reference recording of the correct program, and the length will show whether everything has been restored.",
   ["One greeting lasts {greet} seconds.", "The greeting plays {rp} times.", "There is a {pz}-second pause between neighbouring greetings. There is no pause before the first or after the last.", "The reference recording of the correct program lasts {total} seconds."],
   "How many seconds will the restored program take? Enter a number.", "number", [], [],
   "{rp} greetings: {rp} × {greet} = {tot1} seconds. {pauses} pauses: {pauses} × {pz} = {tot2} seconds. {total} seconds in total, just like the reference recording.",
   "The length matches the reference recording. Asya starts the lighthouse: light and sound together, notes in order, and her brother is cleared.", "Start the greeting",
   ["First find the length of one greeting made of four notes.", "There are {rp} greetings, but only {pauses} pauses between them.", "Add up the notes and the pauses."], 3)
 ]}
L['uk'] = {
 "title": "Маяк, який забув мелодію",
 "intro": "Іграшковий маяк зустрічає гостей вогником і короткою мелодією. Ася вчора правила програму, а сьогодні звук запізнюється і ноти йдуть не в тому порядку. Її брат каже, що річ у проводі динаміка, який він учора зачепив. Допоможи за відеозаписом і карткою мелодії повернути привітання і перевірити його за контрольним записом.",
 "ending": "Звук запізнювався на {delay|секунду|секунди|секунд} через {rep} тестових очікувань по {w|секунді|секунди|секунд}, які Ася забула прибрати. Провід брата був ні до чого: поганий провід не дає ту саму затримку щоразу. Ноти повернули в порядок від короткої до довгої: " + NU + ". Одне привітання триває {greet|секунду|секунди|секунд}, а вся програма з {rp} привітань і {pauses|паузи|пауз|пауз} {total|секунду|секунди|секунд}, рівно як на контрольному записі.",
 "question": "Брат справді зачепив провід. Чому ця версія не пояснювала затримку?",
 "steps": [
  step("Наскільки запізнюється звук?", "Біля маяка Ася вмикає відеозапис сьогоднішнього привітання. На записі є позначки часу файлу, і Ася знайшла два моменти.",
   ["Вогник загоряється на позначці {lt} файлу.", "Першу ноту чути на позначці {st} файлу.", "За планом світло і звук мають починатися одночасно."],
   "На скільки секунд запізнюється звук? Введи число.", "number", [], [],
   "{st} це {ssec} секунд, {lt} це {lsec} секунд. {ssec} - {lsec} = {delay} секунд.",
   "Звук відстає рівно на {delay|секунду|секунди|секунд}, і на трьох повторах запису затримка однакова. Подивимося, звідки в програмі звуку береться стільки секунд.", "Відкрити програму звуку",
   ["Переведи обидві позначки в секунди.", "Позначка виду хвилини:секунди. Помнож хвилини на 60 і додай секунди.", "Відніми момент світла від моменту звуку."], 0),
  step("Де зайве очікування?", "На екрані програма звуку за командами. Світлова програма починає одразу. Брат Асі наполягає на проводі. Перевір, що з цього дає затримку рівно у {delay|секунду|секунди|секунд}, і щоразу однакову.",
   ["Команда 1: чекати {w|секунду|секунди|секунд}, повторити {rep|раз|рази|разів}.", "Команда 2: зіграти привітання.", "Команда 3: після привітання чекати {pa} секунди перед повтором.", "Брат учора зачепив провід динаміка, провід сидить нещільно.", "На трьох повторах запису затримка щоразу рівно {delay|секунда|секунди|секунд}."],
   "Що пояснює затримку першого звуку?", "choice", ["{rep|очікування|очікування|очікувань} по {w|секунді|секунди|секунд} перед привітанням", "Команда зіграти привітання", "Пауза {pa} секунди після привітання", "Нещільний провід динаміка"],
   ["", "Ця команда починає звук, а не затримує його.", "Ця пауза йде після привітання і не може затримати його початок.", "Нещільний провід дає тріск або тишу, але не рівно {delay|секунду|секунди|секунд} щоразу."],
   "Команда 1 стоїть до звуку і триває {w} × {rep} = {delay} секунд, рівно як затримка. Команда 2 починає звук, команда 3 виконується після нього. Провід не дає однакову затримку на кожному повторі.",
   "Ася згадує: вона вставила тестове очікування, щоб перевіряти світло, і забула його прибрати. Команду 1 видаляють, світло і звук починають разом. Тепер порядок нот.", "Звірити картку мелодії",
   ["Шукай те, що стоїть до першого звуку.", "Затримка однакова на кожному повторі: збій проводу так не працює.", "Скільки секунд дають усі повтори команди 1?"], 1),
  step("У якому порядку звучать ноти?", "На картці Асі записано правило цього привітання: звуки йдуть від найкоротшого до найдовшого. Тривалості дано в частках одного такту.",
   ["Один такт триває {bar} секунд.", "МІ займає {fmi} такту, СОЛЬ {fsol} такту, ДО {fdo} такту, РЕ {fre} такту.", "Кожен звук звучить один раз."],
   "Розстав звуки за правилом картки, від короткого до довгого.", "order", ["СОЛЬ, {fsol} такту", "ДО, {fdo} такту", "МІ, {fmi} такту", "РЕ, {fre} такту"], [],
   "Такт {bar} секунд, отже в секундах: МІ {smi}, СОЛЬ {ssol}, ДО {sdo}, РЕ {sre}. Порядок від короткого до довгого: " + NU + ".",
   "Ася зберігає порядок " + NU + ". Одне привітання триває {s1} + {s2} + {s3} + {s4} = {greet} секунд. Залишилося перевірити всю програму за контрольним записом.", "Розрахувати всю програму",
   ["Зведи всі частки до одного знаменника, наприклад до {den#четвертих|восьмих|дванадцятих|шістнадцятих}.", "Або переведи частки в секунди: один такт це {bar} секунд, помнож кожну частку на {bar}.", "Порівняй чотири отримані числа і розстав звуки за зростанням."], 2),
  step("Скільки триває все привітання?", "Програма повторює відновлене привітання кілька разів. В Асі є контрольний запис правильної програми, і за тривалістю можна перевірити, чи все відновлено.",
   ["Одне привітання триває {greet|секунду|секунди|секунд}.", "Привітання звучить {rp|раз|рази|разів}.", "Між сусідніми привітаннями пауза {pz|секунда|секунди|секунд}. Перед першим і після останнього пауз немає.", "Контрольний запис правильної програми триває {total|секунду|секунди|секунд}."],
   "Скільки секунд займе відновлена програма? Введи число.", "number", [], [],
   "{rp} привітання: {rp} × {greet} = {tot1} секунд. {pauses|пауза|паузи|пауз}: {pauses} × {pz} = {tot2} секунд. Разом {total} секунд, як на контрольному записі.",
   "Тривалість збіглася з контрольним записом. Ася запускає маяк: світло і звук разом, ноти по порядку, брата виправдано.", "Запустити привітання",
   ["Спершу тривалість одного привітання з чотирьох звуків.", "Привітань {rp}, але пауз між ними лише {pauses}.", "Додай звуки і паузи."], 3)
 ]}
if __name__ == '__main__':
    write_case('lighthouse', '009', L, variants())
