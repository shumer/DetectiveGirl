from common import step, write_case, add, T
def variants():
    out = []
    data = [
        dict(sec=[5, 7, 6, 8, 4, 6], on='14:20', dur=50, out='15:16', sl='14:50', dcm=4.5, spools=[60, 80, 100], si=2, wo=45, wb=15, packs=[40, 75, 50], pi=1, full=90, fi=0, cs='16:55'),
        dict(sec=[6, 5, 7, 6, 5, 7], on='14:10', dur=55, out='15:12', sl='14:45', dcm=3.5, spools=[50, 80, 60], si=1, wo=40, wb=20, packs=[60, 55, 80], pi=2, full=80, fi=1, cs='16:52'),
        dict(sec=[4, 8, 5, 7, 6, 5], on='14:30', dur=40, out='15:18', sl='14:55', dcm=5.5, spools=[90, 120, 100], si=1, wo=35, wb=15, packs=[65, 45, 50], pi=0, full=120, fi=2, cs='17:20'),
        dict(sec=[5, 6, 7, 8, 5, 8], on='14:05', dur=60, out='15:14', sl='14:40', dcm=2.5, spools=[40, 45, 60], si=2, wo=50, wb=15, packs=[70, 80, 60], pi=1, full=60, fi=3, cs='17:03'),
    ]
    fractions = [('1/3', '2/3', 2, 3), ('1/4', '3/4', 3, 4), ('3/4', '1/4', 1, 4), ('1/6', '5/6', 5, 6)]
    for d in data:
        s = d['sec']; lit = sum(s[:4]); ans1 = s[4] + s[5]
        offt = add(d['on'], d['dur']); assert T(d['out']) - T(offt) >= 3
        gap = T(d['out']) - T(d['sl']); assert gap >= 20
        cart = add(d['out'], -1)
        dm = d['dcm'] * 20; assert dm == int(dm); dm = int(dm)
        spools = d['spools']; assert [x >= dm for x in spools].count(True) == 1 and spools[d['si']] >= dm
        need = 10 + d['wo'] + d['wb']; ret = add('18:10', d['wo'] + d['wb'])
        packs = d['packs']; assert [x >= need for x in packs].count(True) == 1 and packs[d['pi']] >= need
        left = packs[d['pi']] - need; assert left > 0
        have, miss, num, den = fractions[d['fi']]
        missm = d['full'] * num // den; assert d['full'] * num % den == 0
        cdone = add(d['cs'], missm); before = T('18:00') - T(cdone); assert before > 0
        short = [x for i, x in enumerate(spools) if i != d['si']]; others = [i for i in range(3) if i != d['pi']]
        v = dict(s1=s[0], s2=s[1], s3=s[2], s4=s[3], s5=s[4], s6=s[5], total=sum(s), lit=lit, first=lit + 1, ans1=ans1,
                 on=d['on'], dur=d['dur'], offt=offt, out=d['out'], sl=d['sl'], ss=add(d['sl'], -10), gap=gap, cart=cart,
                 dcm=d['dcm'], dm=dm, r1=spools[0], r2=spools[1], r3=spools[2], spool=spools[d['si']], sh1=short[0], sh2=short[1],
                 wo=d['wo'], wb=d['wb'], need=need, ret=ret, pa=packs[0], pb=packs[1], pc=packs[2], pi=d['pi'], pack=packs[d['pi']], o1=others[0], o2=others[1], left=left,
                 full=d['full'], have=have, miss=miss, missm=missm, cs=d['cs'], cdone=cdone, before=before)
        out.append({'values': v, 'answers': [str(ans1), 2, [d['si'], 3 + d['pi']], cdone]})
    return out
BL = {'ru': 'А|Б|В', 'pl': 'A|B|C', 'en': 'A|B|C', 'uk': 'А|Б|В'}
L = {}
L['ru'] = {
 "title": "Лесные фонари",
 "intro": "Лада готовит вечернюю прогулку по тропе с бумажными грибами-фонарями. Днём на проверке фонари в конце тропы погасли все разом, в одну секунду. Мастер Илья клянётся, что блок питания новый. Сторож видел у Круглой поляны незнакомца. Лада хочет знать, почему погас свет, чтобы вечером это не повторилось, и успеть подготовить прогулку к 18:10.",
 "ending": "Свет погас не из-за блока и не из-за незнакомца. Провод от блока 3 лежал через тропу, и в {cart} его перерезала тележка с ящиками. Разряд блока отпал по времени: он бы выключился в {offt}, а свет пропал в {out}. Провод заменили на катушку {spool} м и проложили вдоль тропы, блок {pi#А|Б|В} зарядился к {cdone}. Проверка в 18:00, прогулка с 18:10 до {ret}, у блока останется {left|минута|минуты|минут} запаса.",
 "question": "Незнакомец у поляны был на самом деле. Почему он всё равно ни при чём?",
 "steps": [
  step("Где обрывается свет?", "Лада разворачивает план тропы у склада. Фонари пронумерованы подряд от входа, участки разной длины. Днём Илья прошёл вдоль тропы и записал, какие фонари горят.",
   ["На участках по порядку от входа: {s1}, {s2}, {s3}, {s4}, {s5} и {s6} фонарей, всего {total}.", "На проверке горели фонари с 1 по {lit}. Дальше все тёмные.", "Блок 1 питает участки 1 и 2, блок 2 питает участки 3 и 4, блок 3 питает участки 5 и 6.", "Каждый блок питает только свои фонари."],
   "Сколько фонарей питает блок, из-за которого пропал свет? Введи число.", "number", [], [],
   "{s1} + {s2} + {s3} + {s4} = {lit}: горят ровно первые четыре участка. Фонарь {first} стоит на участке 5. Тёмные участки 5 и 6 питает блок 3: {s5} + {s6} = {ans1} фонарей.",
   "Погасли все {ans1} фонарей блока 3 сразу и ни один другой. Значит, дело в блоке или в его проводе, а не в самих фонарях. Идём к Круглой поляне, где стоит блок 3.", "Идти к блоку 3",
   ["Складывай фонари по участкам от входа, пока не наберёшь {lit}.", "Первый тёмный фонарь номер {first}. Найди, на каком участке он стоит.", "Тёмные участки питает один и тот же блок. Сложи фонари его участков."], 0),
  step("Почему погас свет?", "У Круглой поляны Илья открывает ящик блока 3. Лада собрала все факты, включая рассказ сторожа. Версий три: блок разрядился, кто-то его выключил, повреждён провод. Проверь каждую по времени и по тому, что видно на месте.",
   ["Датчик блока записал: фонари {first}-{total} погасли в {out}.", "Илья включил полностью заряженный блок 3 в {on}. По карточке заряда хватает ровно на {dur} минут, потом блок выключается сам.", "Индикатор заряда блока показывает 2 деления из 5. Выключатель стоит в положении «включено».", "Провод от блока к фонарю {first} лежит поперёк тропы. По журналу склада в {cart} по тропе проехала тележка с ящиками.", "Сторож видел незнакомца у поляны в {ss}. В {sl} тот ушёл в сторону входа."],
   "Какая версия согласуется со всеми фактами?", "choice", ["Блок разрядился, заряда хватило только до {offt}", "Незнакомец выключил блок и ушёл", "Провод поперёк тропы повредила тележка в {cart}", "Все {ans1} фонарей перегорели одновременно"],
   ["Если бы блок разрядился, свет пропал бы в {offt}. А он пропал в {out}, и индикатор до сих пор показывает заряд.", "Выключатель в положении «включено», а незнакомец ушёл в {sl}, за {gap|минуту|минуты|минут} до того, как погас свет.", "", "Фонари не перегорают все в одну секунду, а на первом шаге мы уже поняли, что дело в блоке или проводе."],
   "Разряд не подходит: {on} + {dur} минут = {offt}, а свет пропал в {out}, и заряд в блоке остался. Незнакомец ушёл в {sl} и выключатель не трогал. Провод лежит поперёк тропы, тележка проехала в {cart}, свет пропал через минуту. Илья находит на проводе след колеса и разрыв.",
   "Причина найдена: провод перерезала тележка. Нужен новый провод, который проложат вдоль тропы, и блок на вечер. Идём в мастерскую.", "В мастерскую",
   ["Проверь версию с разрядом по времени: во сколько выключился бы блок, включённый в {on}?", "Сравни время каждого события с {out}, когда погас свет.", "Ищи событие, которое произошло прямо перед {out} и объясняет, почему погасли все фонари блока сразу."], 1),
  step("Что взять из мастерской?", "В мастерской Илья раскладывает катушки провода и запасные блоки. Новый провод проложат вдоль тропы, в обход, чтобы тележки его не задевали. Обход измерен по плану. Блок нужен на всю вечернюю прогулку, включая проверку перед выходом.",
   ["На плане обход провода вдоль тропы измерен: {dcm} см. Масштаб плана: 1 см = 20 м. Сращивать провод из двух кусков нельзя.", "Катушки провода: {r1} м, {r2} м и {r3} м.", "Вечером фонари включают для проверки в 18:00. Группа выходит в 18:10, идёт до павильонов {wo} минут с остановками и возвращается за {wb} минут. Свет нужен до самого возвращения.", "Блоки после полной зарядки работают: А {pa} минут, Б {pb} минут, В {pc} минут."],
   "Отметь, что нужно взять: один провод и один блок.", "multi", ["Катушка {r1} м", "Катушка {r2} м", "Катушка {r3} м", "Блок А: {pa} минут", "Блок Б: {pb} минут", "Блок В: {pc} минут"], [],
   "Обход: {dcm} × 20 = {dm} м. Катушки {sh1} и {sh2} м коротки, подходит {spool} м. Свет нужен с 18:00 до возвращения в {ret}, то есть {need} минут. Блоки {o1#А|Б|В} и {o2#А|Б|В} работают меньше, подходит только блок {pi#А|Б|В} на {pack} минут.",
   "Илья берёт катушку {spool} м и блок {pi#А|Б|В}. Провод проложат вдоль тропы, а блок нужно зарядить до 18:00.", "Зарядить блок",
   ["Провод: переведи сантиметры плана в метры по масштабу.", "Свет нужен с момента проверки в 18:00, а не с выхода группы. Посчитай минуты до возвращения.", "Нужны ровно два предмета: один провод и один блок."], 2),
  step("Успеет ли блок зарядиться?", "У павильонов Илья ставит блок {pi#А|Б|В} на зарядку и прокладывает провод. Лада проверяет, успеет ли всё к проверке в 18:00.",
   ["Проверка фонарей назначена на 18:00.", "Полная зарядка блока {pi#А|Б|В} от нуля занимает {full} минут.", "Когда Илья поставил блок {pi#А|Б|В} на зарядку в {cs}, тот был заряжен на {have}.", "Заряд прибавляется равномерно."],
   "Во сколько блок {pi#А|Б|В} будет заряжен полностью? Введи время ЧЧ:ММ.", "time", [], [],
   "Не хватает {miss} заряда. {miss} от {full} минут это {missm} минут. {cs} + {missm} минут = {cdone}, за {before|минуту|минуты|минут} до проверки.",
   "Блок {pi#А|Б|В} готов к {cdone}, провод лежит вдоль тропы. В 18:00 проверка, в 18:10 группа выходит и вернётся в {ret}. Прогулка состоится.", "Открыть лесную прогулку",
   ["Заряжать нужно не весь блок, а только недостающую часть.", "Какая доля заряда не хватает и сколько это минут из {full}?", "Прибавь эти минуты к {cs}."], 3)
 ]}
L['pl'] = {
 "title": "Leśne latarnie",
 "intro": "Łada przygotowuje wieczorny spacer szlakiem papierowych grzybów-latarni. Po południu podczas próby latarnie na końcu szlaku zgasły wszystkie naraz, w jednej sekundzie. Majster Ilja zarzeka się, że akumulator jest nowy. Stróż widział przy Okrągłej Polanie nieznajomego. Łada chce wiedzieć, dlaczego zgasło światło, żeby wieczorem to się nie powtórzyło, i zdążyć przygotować spacer na 18:10.",
 "ending": "Światło zgasło nie przez akumulator i nie przez nieznajomego. Przewód od akumulatora 3 leżał w poprzek szlaku i o {cart} przeciął go wózek ze skrzynkami. Rozładowanie odpadło ze względu na czas: akumulator wyłączyłby się o {offt}, a światło zgasło o {out}. Przewód wymieniono na szpulę {spool} m i poprowadzono wzdłuż szlaku, akumulator {pi#A|B|C} naładował się do {cdone}. Próba o 18:00, spacer od 18:10 do {ret}, akumulatorowi zostanie {left|minuta|minuty|minut} zapasu.",
 "question": "Nieznajomy przy polanie był naprawdę. Dlaczego mimo to nie ma z tym nic wspólnego?",
 "steps": [
  step("Gdzie urywa się światło?", "Łada rozkłada plan szlaku przy magazynie. Latarnie są ponumerowane po kolei od wejścia, odcinki mają różną długość. Po południu Ilja przeszedł wzdłuż szlaku i zapisał, które latarnie świecą.",
   ["Na odcinkach po kolei od wejścia: {s1}, {s2}, {s3}, {s4}, {s5} i {s6} latarni, razem {total}.", "Podczas próby świeciły latarnie od 1 do {lit}. Dalej wszystkie ciemne.", "Akumulator 1 zasila odcinki 1 i 2, akumulator 2 odcinki 3 i 4, akumulator 3 odcinki 5 i 6.", "Każdy akumulator zasila tylko swoje latarnie."],
   "Ile latarni zasila akumulator, przez który zniknęło światło? Wpisz liczbę.", "number", [], [],
   "{s1} + {s2} + {s3} + {s4} = {lit}: świecą dokładnie pierwsze cztery odcinki. Latarnia {first} stoi na odcinku 5. Ciemne odcinki 5 i 6 zasila akumulator 3: {s5} + {s6} = {ans1} latarni.",
   "Zgasło wszystkie {ans1} latarni akumulatora 3 naraz i żadna inna. Czyli chodzi o akumulator albo jego przewód, a nie o same latarnie. Idziemy na Okrągłą Polanę, gdzie stoi akumulator 3.", "Idź do akumulatora 3",
   ["Dodawaj latarnie po odcinkach od wejścia, aż uzbierasz {lit}.", "Pierwsza ciemna latarnia ma numer {first}. Ustal, na którym odcinku stoi.", "Ciemne odcinki zasila ten sam akumulator. Dodaj latarnie z jego odcinków."], 0),
  step("Dlaczego zgasło światło?", "Przy Okrągłej Polanie Ilja otwiera skrzynkę akumulatora 3. Łada zebrała wszystkie fakty, łącznie z relacją stróża. Wersje są trzy: akumulator się rozładował, ktoś go wyłączył, uszkodzony jest przewód. Sprawdź każdą według czasu i tego, co widać na miejscu.",
   ["Czujnik akumulatora zapisał: latarnie {first}-{total} zgasły o {out}.", "Ilja włączył w pełni naładowany akumulator 3 o {on}. Według karty ładunku wystarcza dokładnie na {dur} minut, potem akumulator sam się wyłącza.", "Wskaźnik ładunku pokazuje 2 kreski z 5. Wyłącznik jest w pozycji „włączone”.", "Przewód od akumulatora do latarni {first} leży w poprzek szlaku. Według dziennika magazynu o {cart} szlakiem przejechał wózek ze skrzynkami.", "Stróż widział nieznajomego przy polanie o {ss}. O {sl} tamten odszedł w stronę wejścia."],
   "Która wersja zgadza się ze wszystkimi faktami?", "choice", ["Akumulator się rozładował, ładunku starczyło tylko do {offt}", "Nieznajomy wyłączył akumulator i odszedł", "Przewód w poprzek szlaku uszkodził wózek o {cart}", "Wszystkie {ans1} latarni przepaliło się jednocześnie"],
   ["Gdyby akumulator się rozładował, światło zgasłoby o {offt}. A zgasło o {out}, a wskaźnik nadal pokazuje ładunek.", "Wyłącznik jest w pozycji „włączone”, a nieznajomy odszedł o {sl}, {gap|minutę|minuty|minut} przed tym, jak zgasło światło.", "", "Latarnie nie przepalają się wszystkie w jednej sekundzie, a w pierwszym kroku ustaliliśmy, że chodzi o akumulator albo przewód."],
   "Rozładowanie nie pasuje: {on} + {dur} minut = {offt}, a światło zgasło o {out} i w akumulatorze został ładunek. Nieznajomy odszedł o {sl} i nie dotykał wyłącznika. Przewód leży w poprzek szlaku, wózek przejechał o {cart}, światło zgasło minutę później. Ilja znajduje na przewodzie ślad koła i przerwanie.",
   "Przyczyna znaleziona: przewód przeciął wózek. Potrzebny jest nowy przewód, który poprowadzą wzdłuż szlaku, i akumulator na wieczór. Idziemy do warsztatu.", "Do warsztatu",
   ["Sprawdź wersję z rozładowaniem według czasu: o której wyłączyłby się akumulator włączony o {on}?", "Porównaj czas każdego zdarzenia z {out}, kiedy zgasło światło.", "Szukaj zdarzenia, które nastąpiło tuż przed {out} i wyjaśnia, dlaczego zgasły wszystkie latarnie akumulatora naraz."], 1),
  step("Co wziąć z warsztatu?", "W warsztacie Ilja rozkłada szpule przewodu i zapasowe akumulatory. Nowy przewód poprowadzą wzdłuż szlaku, okrężną drogą, żeby wózki go nie zaczepiały. Objazd zmierzono na planie. Akumulator jest potrzebny na cały wieczorny spacer, łącznie z próbą przed wyjściem.",
   ["Na planie objazd przewodu wzdłuż szlaku zmierzono: {dcm} cm. Skala planu: 1 cm = 20 m. Nie wolno łączyć przewodu z dwóch kawałków.", "Szpule przewodu: {r1} m, {r2} m i {r3} m.", "Wieczorem latarnie włącza się do próby o 18:00. Grupa wychodzi o 18:10, idzie do pawilonów {wo} minut z postojami i wraca w {wb} minut. Światło jest potrzebne aż do powrotu.", "Akumulatory po pełnym naładowaniu działają: A {pa} minut, B {pb} minut, C {pc} minut."],
   "Zaznacz, co trzeba wziąć: jeden przewód i jeden akumulator.", "multi", ["Szpula {r1} m", "Szpula {r2} m", "Szpula {r3} m", "Akumulator A: {pa} minut", "Akumulator B: {pb} minut", "Akumulator C: {pc} minut"], [],
   "Objazd: {dcm} × 20 = {dm} m. Szpule {sh1} i {sh2} m są za krótkie, pasuje {spool} m. Światło jest potrzebne od 18:00 do powrotu o {ret}, czyli {need} minut. Akumulatory {o1#A|B|C} i {o2#A|B|C} działają krócej, pasuje tylko akumulator {pi#A|B|C} na {pack} minut.",
   "Ilja bierze szpulę {spool} m i akumulator {pi#A|B|C}. Przewód poprowadzą wzdłuż szlaku, a akumulator trzeba naładować do 18:00.", "Naładuj akumulator",
   ["Przewód: przelicz centymetry z planu na metry według skali.", "Światło jest potrzebne od próby o 18:00, a nie od wyjścia grupy. Policz minuty do powrotu.", "Potrzebne są dokładnie dwie rzeczy: jeden przewód i jeden akumulator."], 2),
  step("Czy akumulator zdąży się naładować?", "Przy pawilonach Ilja podłącza akumulator {pi#A|B|C} do ładowania i kładzie przewód. Łada sprawdza, czy wszystko zdąży na próbę o 18:00.",
   ["Próba latarni wyznaczona jest na 18:00.", "Pełne ładowanie akumulatora {pi#A|B|C} od zera zajmuje {full} minut.", "Kiedy Ilja podłączył akumulator {pi#A|B|C} do ładowania o {cs}, był naładowany w {have}.", "Ładunek przybywa równomiernie."],
   "O której akumulator {pi#A|B|C} będzie w pełni naładowany? Wpisz czas GG:MM.", "time", [], [],
   "Brakuje {miss} ładunku. {miss} z {full} minut to {missm} minut. {cs} + {missm} minut = {cdone}, {before|minutę|minuty|minut} przed próbą.",
   "Akumulator {pi#A|B|C} gotowy na {cdone}, przewód leży wzdłuż szlaku. O 18:00 próba, o 18:10 grupa wychodzi i wróci o {ret}. Spacer się odbędzie.", "Rozpocznij leśny spacer",
   ["Ładować trzeba nie cały akumulator, a tylko brakującą część.", "Jakiej części ładunku brakuje i ile to minut z {full}?", "Dodaj te minuty do {cs}."], 3)
 ]}
L['en'] = {
 "title": "Forest Lanterns",
 "intro": "Lada is preparing an evening walk along a trail of paper mushroom lanterns. During the afternoon test, the lanterns at the end of the trail all went out at once, in a single second. Ilya the technician swears the battery pack is new. The watchman saw a stranger near Round Clearing. Lada wants to know why the lights went out so it does not happen again in the evening, and to have the walk ready by 18:10.",
 "ending": "The lights did not go out because of the pack or the stranger. The cable from pack 3 lay across the trail, and at {cart} a cart full of crates cut through it. A flat pack was ruled out by timing: it would have switched off at {offt}, but the lights went out at {out}. The cable was replaced with a {spool} m spool laid along the trail, and pack {pi#A|B|C} was charged by {cdone}. Test at 18:00, walk from 18:10 to {ret}, with {left|minute|minutes} of battery to spare.",
 "question": "The stranger near the clearing was real. Why is he still nothing to do with it?",
 "steps": [
  step("Where does the light stop?", "Lada unfolds the trail map by the depot. The lanterns are numbered in order from the entrance, and the sections are different lengths. In the afternoon, Ilya walked the trail and wrote down which lanterns were lit.",
   ["The sections, in order from the entrance, have {s1}, {s2}, {s3}, {s4}, {s5} and {s6} lanterns: {total} in total.", "During the test, lanterns 1 to {lit} were lit. All the rest were dark.", "Pack 1 powers sections 1 and 2, pack 2 powers sections 3 and 4, and pack 3 powers sections 5 and 6.", "Each pack powers only its own lanterns."],
   "How many lanterns are powered by the pack that lost the light? Enter a number.", "number", [], [],
   "{s1} + {s2} + {s3} + {s4} = {lit}: exactly the first four sections are lit. Lantern {first} is on section 5. The dark sections 5 and 6 are powered by pack 3: {s5} + {s6} = {ans1} lanterns.",
   "All {ans1} lanterns of pack 3 went out at once, and no others. So the problem is the pack or its cable, not the lanterns themselves. Let’s go to Round Clearing, where pack 3 stands.", "Go to pack 3",
   ["Add up the lanterns section by section from the entrance until you reach {lit}.", "The first dark lantern is number {first}. Work out which section it stands on.", "The dark sections are powered by the same pack. Add up the lanterns of its sections."], 0),
  step("Why did the lights go out?", "At Round Clearing, Ilya opens the box of pack 3. Lada has gathered all the facts, including the watchman’s story. There are three theories: the pack ran flat, someone switched it off, the cable is damaged. Test each one against the timing and what you can see on the spot.",
   ["The pack’s sensor recorded that lanterns {first}-{total} went out at {out}.", "Ilya switched on fully charged pack 3 at {on}. According to the card, the charge lasts exactly {dur} minutes, then the pack switches itself off.", "The charge indicator shows 2 bars out of 5. The switch is in the “on” position.", "The cable from the pack to lantern {first} lies across the trail. According to the depot log, a cart full of crates drove along the trail at {cart}.", "The watchman saw a stranger near the clearing at {ss}. At {sl} the stranger left towards the entrance."],
   "Which theory fits all the facts?", "choice", ["The pack ran flat; the charge only lasted until {offt}", "The stranger switched the pack off and left", "The cart damaged the cable lying across the trail at {cart}", "All {ans1} lanterns burned out at the same time"],
   ["If the pack had run flat, the lights would have gone out at {offt}. They went out at {out}, and the indicator still shows charge.", "The switch is in the “on” position, and the stranger left at {sl}, {gap|minute|minutes} before the lights went out.", "", "Lanterns do not all burn out in one second, and in step one we already worked out that the problem is the pack or the cable."],
   "A flat pack does not fit: {on} + {dur} minutes = {offt}, but the lights went out at {out} and there is still charge in the pack. The stranger left at {sl} and never touched the switch. The cable lies across the trail, the cart drove past at {cart}, and the lights went out a minute later. Ilya finds a wheel mark and a break on the cable.",
   "The cause is found: the cart cut the cable. We need a new cable, to be laid along the trail, and a pack for the evening. Off to the workshop.", "To the workshop",
   ["Test the flat-pack theory against the timing: when would a pack switched on at {on} have switched off?", "Compare the time of each event with {out}, when the lights went out.", "Look for an event that happened right before {out} and explains why all the pack’s lanterns went out at once."], 1),
  step("What to take from the workshop?", "In the workshop, Ilya lays out cable spools and spare packs. The new cable will run along the trail, on a detour, so that carts cannot catch it. The detour has been measured on the map. The pack has to last the whole evening walk, including the test before setting off.",
   ["On the map, the cable detour along the trail measures {dcm} cm. The map scale is 1 cm = 20 m. The cable cannot be joined from two pieces.", "Cable spools: {r1} m, {r2} m and {r3} m.", "In the evening, the lanterns are switched on for a test at 18:00. The group leaves at 18:10, takes {wo} minutes to reach the pavilions including stops, and returns in {wb} minutes. Light is needed until they are back.", "After a full charge, the packs run for: A {pa} minutes, B {pb} minutes, C {pc} minutes."],
   "Select what to take: one cable and one pack.", "multi", ["{r1} m spool", "{r2} m spool", "{r3} m spool", "Pack A: {pa} minutes", "Pack B: {pb} minutes", "Pack C: {pc} minutes"], [],
   "The detour: {dcm} × 20 = {dm} m. The {sh1} m and {sh2} m spools are too short, so the {spool} m spool fits. Light is needed from 18:00 until the return at {ret}, which is {need} minutes. Packs {o1#A|B|C} and {o2#A|B|C} run for less, so only pack {pi#A|B|C} at {pack} minutes will do.",
   "Ilya takes the {spool} m spool and pack {pi#A|B|C}. The cable will be laid along the trail, and the pack must be charged by 18:00.", "Charge the pack",
   ["Cable: convert the centimetres on the map to metres using the scale.", "Light is needed from the test at 18:00, not from when the group leaves. Count the minutes until the return.", "Exactly two items are needed: one cable and one pack."], 2),
  step("Will the pack charge in time?", "At the pavilions, Ilya puts pack {pi#A|B|C} on charge and lays the cable. Lada checks whether everything will be ready for the test at 18:00.",
   ["The lantern test is set for 18:00.", "A full charge of pack {pi#A|B|C} from empty takes {full} minutes.", "When Ilya put pack {pi#A|B|C} on charge at {cs}, it was {have} charged.", "The charge increases evenly."],
   "What time will pack {pi#A|B|C} be fully charged? Enter the time as HH:MM.", "time", [], [],
   "{miss} of the charge is missing. {miss} of {full} minutes is {missm} minutes. {cs} + {missm} minutes = {cdone}, {before|minute|minutes} before the test.",
   "Pack {pi#A|B|C} is ready by {cdone}, and the cable lies along the trail. Test at 18:00, the group leaves at 18:10 and returns at {ret}. The walk is on.", "Begin the forest walk",
   ["You only need to charge the missing part, not the whole pack.", "What fraction of the charge is missing, and how many minutes out of {full} is that?", "Add those minutes to {cs}."], 3)
 ]}
L['uk'] = {
 "title": "Лісові ліхтарі",
 "intro": "Лада готує вечірню прогулянку стежкою з паперовими грибами-ліхтарями. Удень на перевірці ліхтарі в кінці стежки згасли всі разом, за одну секунду. Майстер Ілля присягається, що блок живлення новий. Сторож бачив біля Круглої галявини незнайомця. Лада хоче знати, чому згасло світло, щоб увечері це не повторилося, і встигнути підготувати прогулянку до 18:10.",
 "ending": "Світло згасло не через блок і не через незнайомця. Провід від блока 3 лежав поперек стежки, і о {cart} його перерізав візок із ящиками. Розряд блока відпав за часом: він би вимкнувся о {offt}, а світло зникло о {out}. Провід замінили на котушку {spool} м і проклали вздовж стежки, блок {pi#А|Б|В} зарядився до {cdone}. Перевірка о 18:00, прогулянка з 18:10 до {ret}, у блока залишиться {left|хвилина|хвилини|хвилин} запасу.",
 "question": "Незнайомець біля галявини був насправді. Чому він усе одно ні до чого?",
 "steps": [
  step("Де обривається світло?", "Лада розгортає план стежки біля складу. Ліхтарі пронумеровані підряд від входу, ділянки різної довжини. Удень Ілля пройшов уздовж стежки і записав, які ліхтарі горять.",
   ["На ділянках по порядку від входу: {s1}, {s2}, {s3}, {s4}, {s5} і {s6} ліхтарів, разом {total}.", "На перевірці горіли ліхтарі з 1 по {lit}. Далі всі темні.", "Блок 1 живить ділянки 1 і 2, блок 2 живить ділянки 3 і 4, блок 3 живить ділянки 5 і 6.", "Кожен блок живить лише свої ліхтарі."],
   "Скільки ліхтарів живить блок, через який зникло світло? Введи число.", "number", [], [],
   "{s1} + {s2} + {s3} + {s4} = {lit}: горять рівно перші чотири ділянки. Ліхтар {first} стоїть на ділянці 5. Темні ділянки 5 і 6 живить блок 3: {s5} + {s6} = {ans1} ліхтарів.",
   "Згасли всі {ans1} ліхтарів блока 3 одразу і жоден інший. Отже, річ у блоці або в його проводі, а не в самих ліхтарях. Ідемо до Круглої галявини, де стоїть блок 3.", "Іти до блока 3",
   ["Додавай ліхтарі по ділянках від входу, поки не набереш {lit}.", "Перший темний ліхтар номер {first}. Знайди, на якій ділянці він стоїть.", "Темні ділянки живить той самий блок. Додай ліхтарі його ділянок."], 0),
  step("Чому згасло світло?", "Біля Круглої галявини Ілля відкриває ящик блока 3. Лада зібрала всі факти, разом із розповіддю сторожа. Версій три: блок розрядився, хтось його вимкнув, пошкоджено провід. Перевір кожну за часом і за тим, що видно на місці.",
   ["Датчик блока записав: ліхтарі {first}-{total} згасли о {out}.", "Ілля увімкнув повністю заряджений блок 3 о {on}. За карткою заряду вистачає рівно на {dur} хвилин, потім блок вимикається сам.", "Індикатор заряду блока показує 2 поділки з 5. Вимикач стоїть у положенні «увімкнено».", "Провід від блока до ліхтаря {first} лежить поперек стежки. За журналом складу о {cart} стежкою проїхав візок із ящиками.", "Сторож бачив незнайомця біля галявини о {ss}. О {sl} той пішов у бік входу."],
   "Яка версія узгоджується з усіма фактами?", "choice", ["Блок розрядився, заряду вистачило лише до {offt}", "Незнайомець вимкнув блок і пішов", "Провід поперек стежки пошкодив візок о {cart}", "Усі {ans1} ліхтарів перегоріли одночасно"],
   ["Якби блок розрядився, світло зникло б о {offt}. А воно зникло о {out}, і індикатор досі показує заряд.", "Вимикач у положенні «увімкнено», а незнайомець пішов о {sl}, за {gap|хвилину|хвилини|хвилин} до того, як згасло світло.", "", "Ліхтарі не перегорають усі за одну секунду, а на першому кроці ми вже зрозуміли, що річ у блоці або проводі."],
   "Розряд не підходить: {on} + {dur} хвилин = {offt}, а світло зникло о {out}, і заряд у блоці залишився. Незнайомець пішов о {sl} і вимикача не торкався. Провід лежить поперек стежки, візок проїхав о {cart}, світло зникло за хвилину. Ілля знаходить на проводі слід колеса і розрив.",
   "Причину знайдено: провід перерізав візок. Потрібен новий провід, який прокладуть уздовж стежки, і блок на вечір. Ідемо в майстерню.", "У майстерню",
   ["Перевір версію з розрядом за часом: о котрій вимкнувся б блок, увімкнений о {on}?", "Порівняй час кожної події з {out}, коли згасло світло.", "Шукай подію, яка сталася прямо перед {out} і пояснює, чому згасли всі ліхтарі блока одразу."], 1),
  step("Що взяти з майстерні?", "У майстерні Ілля розкладає котушки проводу і запасні блоки. Новий провід прокладуть уздовж стежки, в обхід, щоб візки його не чіпляли. Обхід виміряно за планом. Блок потрібен на всю вечірню прогулянку, разом із перевіркою перед виходом.",
   ["На плані обхід проводу вздовж стежки виміряно: {dcm} см. Масштаб плану: 1 см = 20 м. Зрощувати провід із двох шматків не можна.", "Котушки проводу: {r1} м, {r2} м і {r3} м.", "Увечері ліхтарі вмикають для перевірки о 18:00. Група виходить о 18:10, іде до павільйонів {wo} хвилин із зупинками і повертається за {wb} хвилин. Світло потрібне до самого повернення.", "Блоки після повної зарядки працюють: А {pa} хвилин, Б {pb} хвилин, В {pc} хвилин."],
   "Познач, що треба взяти: один провід і один блок.", "multi", ["Котушка {r1} м", "Котушка {r2} м", "Котушка {r3} м", "Блок А: {pa} хвилин", "Блок Б: {pb} хвилин", "Блок В: {pc} хвилин"], [],
   "Обхід: {dcm} × 20 = {dm} м. Котушки {sh1} і {sh2} м закороткі, підходить {spool} м. Світло потрібне з 18:00 до повернення о {ret}, тобто {need} хвилин. Блоки {o1#А|Б|В} і {o2#А|Б|В} працюють менше, підходить лише блок {pi#А|Б|В} на {pack} хвилин.",
   "Ілля бере котушку {spool} м і блок {pi#А|Б|В}. Провід прокладуть уздовж стежки, а блок треба зарядити до 18:00.", "Зарядити блок",
   ["Провід: переведи сантиметри плану в метри за масштабом.", "Світло потрібне з моменту перевірки о 18:00, а не з виходу групи. Порахуй хвилини до повернення.", "Потрібні рівно два предмети: один провід і один блок."], 2),
  step("Чи встигне блок зарядитися?", "Біля павільйонів Ілля ставить блок {pi#А|Б|В} на зарядку і прокладає провід. Лада перевіряє, чи все встигне до перевірки о 18:00.",
   ["Перевірку ліхтарів призначено на 18:00.", "Повна зарядка блока {pi#А|Б|В} від нуля займає {full} хвилин.", "Коли Ілля поставив блок {pi#А|Б|В} на зарядку о {cs}, той був заряджений на {have}.", "Заряд додається рівномірно."],
   "О котрій блок {pi#А|Б|В} буде заряджений повністю? Введи час ГГ:ХХ.", "time", [], [],
   "Бракує {miss} заряду. {miss} від {full} хвилин це {missm} хвилин. {cs} + {missm} хвилин = {cdone}, за {before|хвилину|хвилини|хвилин} до перевірки.",
   "Блок {pi#А|Б|В} готовий до {cdone}, провід лежить уздовж стежки. О 18:00 перевірка, о 18:10 група виходить і повернеться о {ret}. Прогулянка відбудеться.", "Відкрити лісову прогулянку",
   ["Заряджати треба не весь блок, а лише частину, якої бракує.", "Якої частки заряду бракує і скільки це хвилин із {full}?", "Додай ці хвилини до {cs}."], 3)
 ]}
if __name__ == '__main__':
    write_case('forest', '002', L, variants())
