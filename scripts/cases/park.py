from common import step, write_case, add, T
def variants():
    out = []
    data = [
        dict(rng=500, f=[240, 180], b=[280, 250], p=[150, 190, 170], arch=400, old=30, dcm=3.5, nr=18, pa=16, pb=20, extra=60, pd=24, dist=350, spd=25, chk=8),
        dict(rng=600, f=[260, 220], b=[310, 300], p=[200, 190, 230], arch=450, old=40, dcm=4.5, nr=22, pa=20, pb=25, extra=80, pd=30, dist=400, spd=20, chk=10),
        dict(rng=450, f=[200, 180], b=[240, 230], p=[130, 170, 160], arch=350, old=20, dcm=2.5, nr=15, pa=12, pb=18, extra=50, pd=20, dist=300, spd=25, chk=6),
        dict(rng=550, f=[300, 210], b=[290, 280], p=[160, 200, 200], arch=420, old=35, dcm=3, nr=20, pa=18, pb=24, extra=20, pd=28, dist=450, spd=30, chk=9),
    ]
    for d in data:
        fs, bs, ps = sum(d['f']), sum(d['b']), sum(d['p']); assert fs <= d['rng'] < bs and ps > d['rng'] and d['arch'] < d['rng']
        dm = d['dcm'] * 20; assert dm == int(dm); dm = int(dm); new = fs - d['old'] + dm; assert new <= d['rng']; spare = d['rng'] - new
        assert d['pa'] < d['nr'] <= d['pb'] and new + d['extra'] > d['rng'] and d['pd'] > d['nr']
        tr = d['dist'] // d['spd']; assert d['dist'] % d['spd'] == 0; dep = add('15:00', -tr); start = add(dep, -d['chk'])
        v = dict(rng=d['rng'], f1=d['f'][0], f2=d['f'][1], fs=fs, b1=d['b'][0], b2=d['b'][1], bs=bs, p1=d['p'][0], p2=d['p'][1], p3=d['p'][2], ps=ps, pdiff=ps - d['rng'], arch=d['arch'],
                 old=d['old'], dcm=d['dcm'], dm=dm, new=new, spare=spare, nr=d['nr'], pa=d['pa'], pb=d['pb'], extra=d['extra'], withb=new + d['extra'], pd=d['pd'],
                 dist=d['dist'], spd=d['spd'], tr=tr, dep=dep, chk=d['chk'], start=start)
        out.append({'values': v, 'answers': [0, str(new), 2, start]})
    return out
L = {}
L['ru'] = {
 "title": "Парк и новый маршрут парада",
 "intro": "После дождя парковую арку закрыли на ремонт, а в 15:00 маленькие роботы должны привезти флажки к сцене. Тая, которая отвечает за парад, боится, что заряда роботов не хватит на обходной путь. На плане три открытых дороги и одна закрытая, где-то на пути лужа, а до старта роботам нужно ждать под крышей. Помоги выбрать дорогу, обойти лужу, найти павильон и рассчитать время выхода.",
 "ending": "Из открытых дорог в запас хода {rng} м уложилась только дорога через фонтан: {fs} м. С обходом лужи она стала {new} м. Павильон В единственный вместил всех {nr} роботов, не удлинил путь и не протекал. От павильона до сцены {dist} м со скоростью {spd} м в минуту это {tr|минута|минуты|минут}, плюс {chk|минута|минуты|минут} проверки, поэтому проверку начали в {start} и прибыли ровно в 15:00.",
 "question": "Павильон Б вмещал всех роботов и стоял под крышей. Почему он всё равно не подошёл?",
 "steps": [
  step("По какой дороге ехать?", "У входа Тая показывает план парка. Арка закрыта, но её дорога всё ещё нарисована. Роботы едут от входа до сцены без подзарядки.",
   ["В маршрутной карточке роботов запас хода после полной зарядки: {rng} м.", "Через фонтан: {f1} м, затем {f2} м.", "Через мост: {b1} м, затем {b2} м.", "Через пруд: {p1} м, затем {p2} м, затем {p3} м.", "Через арку: {arch} м, но арка закрыта на ремонт."],
   "Какой путь подходит?", "choice", ["Через фонтан", "Через мост", "Через пруд", "Через арку"],
   ["", "{b1} + {b2} = {bs} м, это больше запаса хода.", "{p1} + {p2} + {p3} = {ps} м, на {pdiff} м больше, чем могут проехать роботы.", "Путь короткий, но арка закрыта: проехать по нему нельзя."],
   "Фонтан: {f1} + {f2} = {fs} м, укладывается в {rng}. Мост: {bs} м, пруд: {ps} м, оба длиннее. Арка короче всех, но закрыта.",
   "Выбран путь через фонтан, {fs} м. Тая идёт проверить его и находит лужу на одном участке. Придётся объезжать.", "Проверить обход лужи",
   ["Сложи части каждого пути и сравни с {rng} м.", "Закрытая дорога не подходит, даже если она самая короткая.", "Подходит только путь не длиннее {rng} м, по которому можно проехать."], 0),
  step("Насколько длиннее обход?", "У фонтана Тая нашла сухую дорожку в обход лужи. Её длины нет на карточке, но есть на плане, а у плана известен масштаб.",
   ["Выбранный путь имеет длину {fs} м.", "Из него убираем залитый участок длиной {old} м.", "Вместо него роботы поедут по сухой дорожке. На плане она измерена: {dcm} см.", "Масштаб плана: 1 см = 20 м.", "Запас хода {rng} м."],
   "Какой станет длина всего пути в метрах? Введи число.", "number", [], [],
   "Обход на плане {dcm} см, по масштабу {dcm} × 20 = {dm} м. Путь: {fs} - {old} + {dm} = {new} м. Это не больше {rng}, роботы доедут.",
   "Путь стал {new} м, запас {spare} м. Теперь нужно место под крышей, где {nr} роботов дождутся старта, и чтобы дорога до него не съела остаток запаса.", "Выбрать павильон",
   ["Переведи обход из сантиметров плана в метры.", "Старый участок убираем, новый добавляем.", "Проверь, что путь всё ещё не больше {rng} м."], 1),
  step("Где ждать старта?", "У павильонов Тая сравнивает четыре варианта. В параде {nr} роботов, и до старта все должны стоять под крышей. Некоторые павильоны лежат прямо на маршруте, другие в стороне.",
   ["Исправленный маршрут: {new} м при запасе хода {rng} м.", "Павильон А: {pa} мест, лежит на маршруте.", "Павильон Б: {pb} мест, заезд к нему добавляет к пути {extra} м.", "Павильон В: {nr} мест, лежит на маршруте.", "Павильон Г: {pd} места, лежит на маршруте, но крыша протекает, и внутри лужи."],
   "Какой павильон подходит?", "choice", ["Павильон А", "Павильон Б", "Павильон В", "Павильон Г"],
   ["В павильоне А только {pa} мест, а роботов {nr}.", "Мест хватает, но с заездом путь станет {new} + {extra} = {withb} м, больше запаса.", "", "Мест много и он на маршруте, но крыша протекает: роботы промокнут, как на улице."],
   "А мал: {pa} мест на {nr} роботов. Б вмещает всех, но удлиняет путь до {withb} м. Г на маршруте и большой, но не защищает от дождя. Только В вмещает {nr}, лежит на маршруте и сухой.",
   "Роботы ждут в павильоне В. Осталось рассчитать, когда начинать предстартовую проверку, чтобы прибыть к сцене ровно в 15:00.", "Назначить время проверки",
   ["У каждого павильона проверь три вещи: места, длину пути и крышу.", "Заезд в павильон в стороне прибавляется к {new} м.", "Протекающая крыша это то же самое, что без крыши."], 2),
  step("Когда начинать проверку?", "У сцены Тая измерила оставшийся отрезок. Роботы едут с постоянной скоростью, а перед выездом их проверяют. Прибыть нужно ровно к началу.",
   ["Прибыть к сцене нужно ровно в 15:00.", "От павильона В до сцены {dist} м.", "Роботы едут со скоростью {spd} м в минуту.", "Перед выездом нужна проверка продолжительностью {chk|минута|минуты|минут}. После проверки роботы сразу выезжают."],
   "Во сколько начать проверку? Введи время ЧЧ:ММ.", "time", [], [],
   "Дорога: {dist} : {spd} = {tr} минут, значит выезд в {dep}. Проверка {chk} минут перед выездом: начало в {start}.",
   "План готов: проверка в {start}, выезд в {dep}, прибытие в 15:00 с запасом хода {spare} м. Тая записывает расписание, и парад состоится.", "Передать план парада",
   ["Время в пути: расстояние раздели на скорость.", "Считай назад от 15:00: сначала дорога, потом проверка.", "Проверка начинается раньше выезда."], 3)
 ]}
L['pl'] = {
 "title": "Park i nowa trasa parady",
 "intro": "Po deszczu parkową bramę zamknięto do remontu, a o 15:00 małe roboty mają przywieźć chorągiewki na scenę. Taja, która odpowiada za paradę, boi się, że ładunku robotów nie starczy na objazd. Na planie są trzy otwarte drogi i jedna zamknięta, gdzieś na trasie jest kałuża, a do startu roboty muszą czekać pod dachem. Pomóż wybrać drogę, ominąć kałużę, znaleźć pawilon i obliczyć czas wyjazdu.",
 "ending": "Z otwartych dróg w zasięgu {rng} m zmieściła się tylko droga przez fontannę: {fs} m. Z objazdem kałuży wydłużyła się do {new} m. Pawilon C jako jedyny pomieścił wszystkie {nr} robotów, nie wydłużył trasy i nie przeciekał. Z pawilonu do sceny {dist} m z prędkością {spd} m na minutę to {tr|minuta|minuty|minut}, plus {chk|minuta|minuty|minut} kontroli, więc kontrolę zaczęto o {start} i przyjechano dokładnie o 15:00.",
 "question": "Pawilon B mieścił wszystkie roboty i miał dach. Dlaczego mimo to nie pasował?",
 "steps": [
  step("Którą drogą jechać?", "Przy wejściu Taja pokazuje plan parku. Brama jest zamknięta, ale jej droga nadal jest narysowana. Roboty jadą od wejścia do sceny bez doładowania.",
   ["W karcie trasy robotów zasięg po pełnym naładowaniu: {rng} m.", "Przez fontannę: {f1} m, potem {f2} m.", "Przez most: {b1} m, potem {b2} m.", "Przez staw: {p1} m, potem {p2} m, potem {p3} m.", "Przez bramę: {arch} m, ale brama jest zamknięta do remontu."],
   "Która trasa pasuje?", "choice", ["Przez fontannę", "Przez most", "Przez staw", "Przez bramę"],
   ["", "{b1} + {b2} = {bs} m, to więcej niż zasięg.", "{p1} + {p2} + {p3} = {ps} m, o {pdiff} m więcej, niż roboty mogą przejechać.", "Trasa jest krótka, ale brama jest zamknięta: nie da się nią przejechać."],
   "Fontanna: {f1} + {f2} = {fs} m, mieści się w {rng}. Most: {bs} m, staw: {ps} m, obie za długie. Brama jest najkrótsza, ale zamknięta.",
   "Wybrano trasę przez fontannę, {fs} m. Taja idzie ją sprawdzić i znajduje kałużę na jednym odcinku. Trzeba będzie objechać.", "Sprawdź objazd kałuży",
   ["Dodaj części każdej trasy i porównaj z {rng} m.", "Zamknięta droga nie pasuje, nawet jeśli jest najkrótsza.", "Pasuje tylko trasa nie dłuższa niż {rng} m, którą da się przejechać."], 0),
  step("O ile dłuższy jest objazd?", "Przy fontannie Taja znalazła suchą ścieżkę omijającą kałużę. Jej długości nie ma na karcie, ale jest na planie, a plan ma znaną skalę.",
   ["Wybrana trasa ma długość {fs} m.", "Usuwamy z niej zalany odcinek o długości {old} m.", "Zamiast niego roboty pojadą suchą ścieżką. Na planie zmierzono ją: {dcm} cm.", "Skala planu: 1 cm = 20 m.", "Zasięg {rng} m."],
   "Jaka będzie długość całej trasy w metrach? Wpisz liczbę.", "number", [], [],
   "Objazd na planie ma {dcm} cm, według skali {dcm} × 20 = {dm} m. Trasa: {fs} - {old} + {dm} = {new} m. To nie więcej niż {rng}, roboty dojadą.",
   "Trasa ma teraz {new} m, zapas {spare} m. Teraz potrzebne jest miejsce pod dachem, gdzie {nr} robotów doczeka startu, i żeby droga do niego nie zjadła reszty zapasu.", "Wybierz pawilon",
   ["Przelicz objazd z centymetrów planu na metry.", "Stary odcinek usuwamy, nowy dodajemy.", "Sprawdź, czy trasa nadal nie jest dłuższa niż {rng} m."], 1),
  step("Gdzie czekać na start?", "Przy pawilonach Taja porównuje cztery warianty. W paradzie jest {nr} robotów i do startu wszystkie muszą stać pod dachem. Niektóre pawilony leżą wprost na trasie, inne na uboczu.",
   ["Poprawiona trasa: {new} m przy zasięgu {rng} m.", "Pawilon A: {pa} miejsc, leży na trasie.", "Pawilon B: {pb} miejsc, dojazd do niego dodaje do trasy {extra} m.", "Pawilon C: {nr} miejsc, leży na trasie.", "Pawilon D: {pd} miejsc, leży na trasie, ale dach przecieka i w środku są kałuże."],
   "Który pawilon pasuje?", "choice", ["Pawilon A", "Pawilon B", "Pawilon C", "Pawilon D"],
   ["W pawilonie A jest tylko {pa} miejsc, a robotów jest {nr}.", "Miejsc starcza, ale z dojazdem trasa będzie miała {new} + {extra} = {withb} m, więcej niż zasięg.", "", "Miejsc jest dużo i leży na trasie, ale dach przecieka: roboty zmokną jak na dworze."],
   "A jest za mały: {pa} miejsc na {nr} robotów. B mieści wszystkie, ale wydłuża trasę do {withb} m. D jest na trasie i duży, ale nie chroni przed deszczem. Tylko C mieści {nr}, leży na trasie i jest suchy.",
   "Roboty czekają w pawilonie C. Zostało obliczyć, kiedy zacząć kontrolę przed startem, żeby dojechać do sceny dokładnie o 15:00.", "Ustal czas kontroli",
   ["Przy każdym pawilonie sprawdź trzy rzeczy: miejsca, długość trasy i dach.", "Dojazd do pawilonu na uboczu dodaje się do {new} m.", "Przeciekający dach to to samo, co brak dachu."], 2),
  step("Kiedy zacząć kontrolę?", "Przy scenie Taja zmierzyła pozostały odcinek. Roboty jadą ze stałą prędkością, a przed wyjazdem są sprawdzane. Dojechać trzeba dokładnie na początek.",
   ["Dojechać do sceny trzeba dokładnie o 15:00.", "Z pawilonu C do sceny jest {dist} m.", "Roboty jadą z prędkością {spd} m na minutę.", "Przed wyjazdem potrzebna jest kontrola trwająca {chk|minutę|minuty|minut}. Po kontroli roboty od razu wyjeżdżają."],
   "O której zacząć kontrolę? Wpisz czas GG:MM.", "time", [], [],
   "Droga: {dist} : {spd} = {tr} minut, więc wyjazd o {dep}. Kontrola {chk} minut przed wyjazdem: początek o {start}.",
   "Plan gotowy: kontrola o {start}, wyjazd o {dep}, przyjazd o 15:00 z zapasem {spare} m. Taja zapisuje rozkład i parada się odbędzie.", "Przekaż plan parady",
   ["Czas jazdy: odległość podziel przez prędkość.", "Licz wstecz od 15:00: najpierw droga, potem kontrola.", "Kontrola zaczyna się przed wyjazdem."], 3)
 ]}
L['en'] = {
 "title": "The Park and the New Parade Route",
 "intro": "After the rain, the park arch was closed for repairs, and at 15:00 the little robots have to bring the flags to the stage. Taya, who is in charge of the parade, is afraid the robots’ charge will not last the detour. The map shows three open routes and one closed one, there is a puddle somewhere along the way, and the robots need to wait under a roof before the start. Help choose the route, get round the puddle, find a pavilion and work out the departure time.",
 "ending": "Of the open routes, only the one past the fountain fitted the {rng} m range: {fs} m. With the puddle detour it became {new} m. Pavilion C was the only one that held all {nr} robots, did not lengthen the route and did not leak. From the pavilion to the stage is {dist} m at {spd} m per minute, which is {tr} minutes, plus {chk} minutes of checks, so the check started at {start} and the robots arrived at exactly 15:00.",
 "question": "Pavilion B held all the robots and had a roof. Why was it still no good?",
 "steps": [
  step("Which route to take?", "At the entrance, Taya shows the park map. The arch is closed, but its route is still drawn. The robots travel from the entrance to the stage without recharging.",
   ["The robots’ route card gives their range after a full charge: {rng} m.", "Past the fountain: {f1} m, then {f2} m.", "Over the bridge: {b1} m, then {b2} m.", "Past the pond: {p1} m, then {p2} m, then {p3} m.", "Through the arch: {arch} m, but the arch is closed for repairs."],
   "Which route works?", "choice", ["Past the fountain", "Over the bridge", "Past the pond", "Through the arch"],
   ["", "{b1} + {b2} = {bs} m, which is more than the range.", "{p1} + {p2} + {p3} = {ps} m, {pdiff} m more than the robots can travel.", "The route is short, but the arch is closed: you cannot go that way."],
   "Fountain: {f1} + {f2} = {fs} m, within {rng}. Bridge: {bs} m, pond: {ps} m, both too long. The arch is the shortest of all, but closed.",
   "The fountain route is chosen, {fs} m. Taya goes to check it and finds a puddle on one section. A detour will be needed.", "Check the puddle detour",
   ["Add up the parts of each route and compare with {rng} m.", "A closed route does not work, even if it is the shortest.", "Only a route no longer than {rng} m that can actually be travelled will do."], 0),
  step("How much longer is the detour?", "At the fountain, Taya has found a dry path around the puddle. Its length is not on the card, but it is on the map, and the map’s scale is known.",
   ["The chosen route is {fs} m long.", "We remove the flooded section, {old} m long.", "Instead, the robots will take the dry path. On the map it measures {dcm} cm.", "Map scale: 1 cm = 20 m.", "The range is {rng} m."],
   "How long will the whole route be, in metres? Enter a number.", "number", [], [],
   "The detour on the map is {dcm} cm, which by the scale is {dcm} × 20 = {dm} m. The route: {fs} - {old} + {dm} = {new} m. That is no more than {rng}, so the robots will make it.",
   "The route is now {new} m, with {spare} m to spare. Now we need a place under a roof where {nr} robots can wait for the start, without the way there eating up what is left of the range.", "Choose a pavilion",
   ["Convert the detour from map centimetres to metres.", "Remove the old section, add the new one.", "Check that the route is still no more than {rng} m."], 1),
  step("Where to wait for the start?", "At the pavilions, Taya compares four options. There are {nr} robots in the parade, and all of them must be under a roof before the start. Some pavilions lie right on the route, others off to the side.",
   ["The corrected route: {new} m with a range of {rng} m.", "Pavilion A: {pa} places, on the route.", "Pavilion B: {pb} places, but the detour to it adds {extra} m to the route.", "Pavilion C: {nr} places, on the route.", "Pavilion D: {pd} places, on the route, but the roof leaks and there are puddles inside."],
   "Which pavilion works?", "choice", ["Pavilion A", "Pavilion B", "Pavilion C", "Pavilion D"],
   ["Pavilion A has only {pa} places, and there are {nr} robots.", "There are enough places, but with the detour the route becomes {new} + {extra} = {withb} m, more than the range.", "", "Plenty of places and on the route, but the roof leaks: the robots would get as wet as outside."],
   "A is too small: {pa} places for {nr} robots. B holds them all but stretches the route to {withb} m. D is on the route and big, but does not keep the rain out. Only C holds {nr}, lies on the route and is dry.",
   "The robots wait in pavilion C. All that remains is to work out when to start the pre-departure check so they reach the stage at exactly 15:00.", "Set the check time",
   ["For each pavilion check three things: places, route length and roof.", "The detour to a pavilion off the route is added to the {new} m.", "A leaking roof is the same as no roof."], 2),
  step("When to start the check?", "At the stage, Taya has measured the remaining stretch. The robots travel at a constant speed, and they are checked before departure. They must arrive exactly at the start.",
   ["The robots must reach the stage at exactly 15:00.", "From pavilion C to the stage is {dist} m.", "The robots travel at {spd} m per minute.", "Before departure they need a check lasting {chk} minutes. After the check the robots leave at once."],
   "What time should the check start? Enter the time as HH:MM.", "time", [], [],
   "Travel: {dist} ÷ {spd} = {tr} minutes, so departure at {dep}. A {chk}-minute check before departure: start at {start}.",
   "The plan is ready: check at {start}, departure at {dep}, arrival at 15:00 with {spare} m of range to spare. Taya writes down the timetable, and the parade is on.", "Hand over the parade plan",
   ["Travel time: divide the distance by the speed.", "Count back from 15:00: first the journey, then the check.", "The check starts before the departure."], 3)
 ]}
L['uk'] = {
 "title": "Парк і новий маршрут параду",
 "intro": "Після дощу паркову арку зачинили на ремонт, а о 15:00 маленькі роботи мають привезти прапорці до сцени. Тая, яка відповідає за парад, боїться, що заряду роботів не вистачить на обхідний шлях. На плані три відкриті дороги й одна зачинена, десь на шляху калюжа, а до старту роботам треба чекати під дахом. Допоможи вибрати дорогу, обійти калюжу, знайти павільйон і розрахувати час виїзду.",
 "ending": "З відкритих доріг у запас ходу {rng} м уклалася лише дорога через фонтан: {fs} м. З обходом калюжі вона стала {new} м. Павільйон В єдиний умістив усіх {nr} роботів, не подовжив шлях і не протікав. Від павільйону до сцени {dist} м зі швидкістю {spd} м за хвилину це {tr|хвилина|хвилини|хвилин}, плюс {chk|хвилина|хвилини|хвилин} перевірки, тому перевірку почали о {start} і прибули рівно о 15:00.",
 "question": "Павільйон Б уміщав усіх роботів і стояв під дахом. Чому він усе одно не підійшов?",
 "steps": [
  step("Якою дорогою їхати?", "Біля входу Тая показує план парку. Арка зачинена, але її дорога досі намальована. Роботи їдуть від входу до сцени без підзарядки.",
   ["У маршрутній картці роботів запас ходу після повної зарядки: {rng} м.", "Через фонтан: {f1} м, потім {f2} м.", "Через міст: {b1} м, потім {b2} м.", "Через ставок: {p1} м, потім {p2} м, потім {p3} м.", "Через арку: {arch} м, але арка зачинена на ремонт."],
   "Який шлях підходить?", "choice", ["Через фонтан", "Через міст", "Через ставок", "Через арку"],
   ["", "{b1} + {b2} = {bs} м, це більше за запас ходу.", "{p1} + {p2} + {p3} = {ps} м, на {pdiff} м більше, ніж можуть проїхати роботи.", "Шлях короткий, але арка зачинена: проїхати ним не можна."],
   "Фонтан: {f1} + {f2} = {fs} м, укладається в {rng}. Міст: {bs} м, ставок: {ps} м, обидва довші. Арка найкоротша, але зачинена.",
   "Вибрано шлях через фонтан, {fs} м. Тая йде перевірити його і знаходить калюжу на одній ділянці. Доведеться об’їжджати.", "Перевірити обхід калюжі",
   ["Додай частини кожного шляху і порівняй із {rng} м.", "Зачинена дорога не підходить, навіть якщо вона найкоротша.", "Підходить лише шлях не довший за {rng} м, яким можна проїхати."], 0),
  step("Наскільки довший обхід?", "Біля фонтана Тая знайшла суху доріжку в обхід калюжі. Її довжини немає на картці, але є на плані, а в плану відомий масштаб.",
   ["Вибраний шлях має довжину {fs} м.", "З нього прибираємо залиту ділянку завдовжки {old} м.", "Замість неї роботи поїдуть сухою доріжкою. На плані її виміряно: {dcm} см.", "Масштаб плану: 1 см = 20 м.", "Запас ходу {rng} м."],
   "Якою стане довжина всього шляху в метрах? Введи число.", "number", [], [],
   "Обхід на плані {dcm} см, за масштабом {dcm} × 20 = {dm} м. Шлях: {fs} - {old} + {dm} = {new} м. Це не більше за {rng}, роботи доїдуть.",
   "Шлях став {new} м, запас {spare} м. Тепер потрібне місце під дахом, де {nr} роботів дочекаються старту, і щоб дорога до нього не з’їла решту запасу.", "Вибрати павільйон",
   ["Переведи обхід із сантиметрів плану в метри.", "Стару ділянку прибираємо, нову додаємо.", "Перевір, що шлях усе ще не більший за {rng} м."], 1),
  step("Де чекати старту?", "Біля павільйонів Тая порівнює чотири варіанти. У параді {nr} роботів, і до старту всі мають стояти під дахом. Деякі павільйони лежать просто на маршруті, інші осторонь.",
   ["Виправлений маршрут: {new} м при запасі ходу {rng} м.", "Павільйон А: {pa} місць, лежить на маршруті.", "Павільйон Б: {pb} місць, заїзд до нього додає до шляху {extra} м.", "Павільйон В: {nr} місць, лежить на маршруті.", "Павільйон Г: {pd} місць, лежить на маршруті, але дах протікає, і всередині калюжі."],
   "Який павільйон підходить?", "choice", ["Павільйон А", "Павільйон Б", "Павільйон В", "Павільйон Г"],
   ["У павільйоні А лише {pa} місць, а роботів {nr}.", "Місць вистачає, але із заїздом шлях стане {new} + {extra} = {withb} м, більше за запас.", "", "Місць багато і він на маршруті, але дах протікає: роботи промокнуть, як на вулиці."],
   "А малий: {pa} місць на {nr} роботів. Б уміщає всіх, але подовжує шлях до {withb} м. Г на маршруті і великий, але не захищає від дощу. Лише В уміщає {nr}, лежить на маршруті і сухий.",
   "Роботи чекають у павільйоні В. Залишилося розрахувати, коли починати передстартову перевірку, щоб прибути до сцени рівно о 15:00.", "Призначити час перевірки",
   ["У кожного павільйону перевір три речі: місця, довжину шляху і дах.", "Заїзд у павільйон осторонь додається до {new} м.", "Дах, що протікає, це те саме, що без даху."], 2),
  step("Коли починати перевірку?", "Біля сцени Тая виміряла відрізок, що залишився. Роботи їдуть зі сталою швидкістю, а перед виїздом їх перевіряють. Прибути треба рівно до початку.",
   ["Прибути до сцени треба рівно о 15:00.", "Від павільйону В до сцени {dist} м.", "Роботи їдуть зі швидкістю {spd} м за хвилину.", "Перед виїздом потрібна перевірка тривалістю {chk|хвилина|хвилини|хвилин}. Після перевірки роботи одразу виїжджають."],
   "О котрій почати перевірку? Введи час ГГ:ХХ.", "time", [], [],
   "Дорога: {dist} : {spd} = {tr} хвилин, отже виїзд о {dep}. Перевірка {chk} хвилин перед виїздом: початок о {start}.",
   "План готовий: перевірка о {start}, виїзд о {dep}, прибуття о 15:00 із запасом ходу {spare} м. Тая записує розклад, і парад відбудеться.", "Передати план параду",
   ["Час у дорозі: відстань поділи на швидкість.", "Рахуй назад від 15:00: спершу дорога, потім перевірка.", "Перевірка починається раніше за виїзд."], 3)
 ]}
if __name__ == '__main__':
    write_case('park', '011', L, variants())
