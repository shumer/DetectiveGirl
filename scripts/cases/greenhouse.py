from common import step, write_case, add, T
def variants():
    out = []
    data = [
        dict(plan=60, seg=[('9:00', '9:18'), ('9:32', '9:47'), ('10:05', '10:17')], fl='8:50', bl='10:20', cw=80, pw=60, niches=[120, 150, 130, 160], ni=1, n=12, pp=50, plat=[5, 6.5, 7], xs='11:40'),
        dict(plan=60, seg=[('9:00', '9:12'), ('9:30', '9:48'), ('10:03', '10:15')], fl='8:45', bl='10:20', cw=90, pw=70, niches=[170, 140, 150, 180], ni=0, n=15, pp=40, plat=[5.5, 6, 6.5], xs='11:30'),
        dict(plan=50, seg=[('9:00', '9:16'), ('9:28', '9:39'), ('9:52', '10:05')], fl='8:55', bl='10:10', cw=70, pw=60, niches=[120, 125, 140, 150], ni=2, n=16, pp=50, plat=[7, 8, 8.5], xs='11:45'),
        dict(plan=70, seg=[('9:00', '9:20'), ('9:35', '9:52'), ('10:08', '10:22')], fl='8:40', bl='10:30', cw=85, pw=65, niches=[140, 155, 145, 160], ni=1, n=10, pp=60, plat=[4, 6.5, 7], xs='11:20'),
    ]
    for d in data:
        (s1, e1), (s2, e2), (s3, e3) = d['seg']
        lens = [T(b) - T(a) for a, b in d['seg']]; got = sum(lens); miss = d['plan'] - got; assert miss > 0
        lampon = T(e3) - T(s1); dgap = T(e2) - T(e1)
        assert T('0' + d['fl']) < T(s1) and T(d['bl']) > T(e3)
        need = d['cw'] + d['pw']; fits = [i for i, w in enumerate(d['niches']) if w >= need]; assert fits == sorted([d['ni'], 3]) and d['ni'] != 3
        needcm = d['n'] * d['pp']; needm = needcm / 100; needm = int(needm) if needm == int(needm) else needm
        p1, p2, p3 = d['plat']; assert p1 < needm <= p3 and p2 >= needm
        extra = miss * 2; xe = add(d['xs'], extra)
        v = dict(plan=d['plan'], s1=s1, e1=e1, s2=s2, e2=e2, s3=s3, e3=e3, l1=lens[0], l2=lens[1], l3=lens[2], got=got, miss=miss, lampon=lampon, dgap=dgap, fl=d['fl'], bl=d['bl'],
                 cw=d['cw'], pw=d['pw'], need=need, na=d['niches'][0], nb=d['niches'][1], nc=d['niches'][2], nd=d['niches'][3], ni=d['ni'], nw=d['niches'][d['ni']],
                 n=d['n'], pp=d['pp'], needcm=needcm, needm=needm, p1=p1, p2=p2, p3=p3, extra=extra, xs=d['xs'], xe=xe)
        out.append({'values': v, 'answers': [str(miss), 2, [d['ni'], 6], xe]})
    return out
L = {}
L['ru'] = {
 "title": "Сигнал с лунной оранжереи",
 "intro": "Робот Пик ухаживает за ростками в учебной лунной оранжерее под куполом. Утром датчик ряда Б прислал сигнал: ростки недополучили свет, хотя лампа над рядом горела всё утро. Механик говорит, что лампа мигала при включении. Пик подозревает свою тележку. А ещё в оранжерее была экскурсия. Помоги понять, что закрывало свет, куда убрать помеху и как вернуть росткам недостающие минуты.",
 "ending": "Свет закрывали дважды и разные вещи: с {e1} до {s2} тележка Пика с ящиками, с {e2} до {s3} экскурсия у ряда Б. Мигание лампы было до начала плана и ни на что не повлияло. Тележке нашли нишу {ni#А|Б|В|Г}, а группам отвели площадку П3 вне лучей. Дополнительная лампа с половинной силой работала с {xs} до {xe} и восполнила {miss|минуту|минуты|минут}. Ряд Б получил свои {plan} минут.",
 "question": "Лампа ряда Б горела {lampon|минуту|минуты|минут}, а ростки получили {got}. Почему исправная лампа ещё не значит, что освещение в порядке?",
 "steps": [
  step("Сколько света не хватило?", "Под куполом Пик показывает журнал датчика ряда Б. Датчик стоит у самых ростков и записывает только тот свет, который до них доходит. Лампа над рядом пишет свой журнал отдельно.",
   ["По плану на это утро каждый ряд должен получить {plan} минут света.", "Датчик ряда Б записал свет с {s1} до {e1}, с {s2} до {e2} и с {s3} до {e3}.", "Журнал лампы ряда Б: горела с {s1} до {e3} без выключений."],
   "Сколько минут света недополучил ряд Б? Введи число.", "number", [], [],
   "Три отрезка: {l1} + {l2} + {l3} = {got} минут. По плану {plan}, не хватает {plan} - {got} = {miss} минут.",
   "Лампа горела {lampon|минуту|минуты|минут}, а до ростков дошло {got}. Значит, между лампой и рядом что-то было дважды: с {e1} до {s2} и с {e2} до {s3}. Пик открывает журнал перемещений.", "Открыть журнал перемещений",
   ["Сложи три отрезка, в каждом посчитай минуты от начала до конца.", "План {plan} минут. Сравни с тем, что набралось.", "Не хватает ровно разницы между планом и суммой отрезков."], 0),
  step("Что закрывало свет?", "У ряда Б Пик разложил всё, что случилось утром. Два промежутка без света уже известны: с {e1} до {s2} и с {e2} до {s3}. Проверь каждое событие по времени: попадает ли оно в промежуток и может ли закрыть лампу.",
   ["Пик поставил тележку с высокими ящиками у ряда Б в {e1} и увёз её в {s2}.", "По расписанию экскурсия стояла у ряда Б с {e2} до {s3}: {n} человек между лампой и ростками.", "Механик записал: лампа ряда Б мигала в {fl} при включении, потом горела ровно.", "Шторы купола закрываются на обед в {bl} и открываются в 11:00."],
   "Что закрывало свет от ряда Б?", "choice", ["Только тележка Пика", "Только экскурсия", "Тележка в первый промежуток и экскурсия во второй", "Мигание лампы при включении"],
   ["Тележка объясняет промежуток с {e1} до {s2}. Но свет пропадал ещё раз, с {e2} до {s3}, когда тележки уже не было.", "Экскурсия объясняет промежуток с {e2} до {s3}. Но первый промежуток начался в {e1}, за {dgap|минуту|минуты|минут} до экскурсии.", "", "Лампа мигала в {fl}, до начала плана в {s1}. В {s1} датчик уже видел ровный свет."],
   "Первый промежуток совпадает с тележкой: поставили в {e1}, увезли в {s2}. Второй совпадает с экскурсией: с {e2} до {s3}. Мигание было до {s1}, шторы закрылись после {e3}. Причин две, и обе нужно устранить.",
   "Помех две: тележка и люди перед рядом. Тележке нужно постоянное место, а группам площадка вне лучей. Идём к нишам в коридоре.", "Выбрать место для тележки и группы",
   ["Сравни каждое событие с двумя промежутками без света.", "Одно событие не может объяснить оба промежутка, если оно было только в одном из них.", "Событие до {s1} или после {e3} на утренний план не влияет."], 1),
  step("Куда убрать помехи?", "В коридоре четыре ниши для тележки и три площадки для экскурсий. Пик измерил всё рулеткой. Нужно выбрать одну нишу и одну площадку так, чтобы ни то, ни другое не мешало лампам.",
   ["Тележка занимает {cw} см по ширине, и рядом с ней в той же нише нужен проход не уже {pw} см.", "Ниши: А {na} см, Б {nb} см, В {nc} см, Г {nd} см. Ниша Г попадает в луч лампы ряда В.", "На экскурсии {n} человек, каждому нужно {pp} см вдоль перил площадки.", "Площадки: П1 длиной {p1} м, П2 длиной {p2} м перед лампой ряда А, П3 длиной {p3} м вне всех лучей."],
   "Отметь одну нишу для тележки и одну площадку для экскурсий.", "multi", ["Ниша А", "Ниша Б", "Ниша В", "Ниша Г", "Площадка П1", "Площадка П2", "Площадка П3"], [],
   "Тележке с проходом нужно {cw} + {pw} = {need} см. Подходят {ni#А|Б|В|Г} ({nw}) и Г ({nd}), но Г в луче лампы ряда В, остаётся {ni#А|Б|В|Г}. Группе нужно {n} × {pp} см = {needcm} см, то есть {needm} м. П1 коротка, П2 стоит перед лампой ряда А, подходит П3.",
   "Тележка теперь стоит в нише {ni#А|Б|В|Г}, экскурсии ждут на площадке П3. Осталось вернуть ряду Б недостающие {miss|минуту|минуты|минут} света.", "Настроить дополнительную лампу",
   ["Сначала посчитай, сколько сантиметров нужно тележке вместе с проходом, и сколько метров нужно группе.", "Подходящих по размеру мест больше одного. Отбрось те, что стоят в луче какой-нибудь лампы.", "Нужно ровно два ответа: одна ниша и одна площадка."], 2),
  step("Когда выключить подсветку?", "В пульте оранжереи Пик включает дополнительную лампу над рядом Б. Она слабее основной, поэтому время нужно пересчитать.",
   ["Ряду Б не хватает {miss|минуты|минут|минут} света основной лампы.", "Дополнительная лампа даёт вдвое меньше света: чтобы восполнить одну минуту основной, она должна работать две.", "Пик включит дополнительную лампу в {xs}.", "Основная лампа в это время выключена по плану и не считается."],
   "Во сколько выключить дополнительную лампу, чтобы восполнить ровно недостачу? Введи время ЧЧ:ММ.", "time", [], [],
   "{miss|минута|минуты|минут} основной лампы это {miss} × 2 = {extra} минут дополнительной. {xs} + {extra} минут = {xe}.",
   "В {xe} ряд Б получит все {plan} минут по плану. Тележка в нише, площадка выбрана, и утренний сбой больше не повторится.", "Завершить проверку оранжереи",
   ["Каждую недостающую минуту дополнительная лампа восполняет за две.", "Удвой недостачу из первого шага.", "Прибавь это время к {xs}."], 3)
 ]}
L['pl'] = {
 "title": "Sygnał z księżycowej szklarni",
 "intro": "Robot Pik opiekuje się sadzonkami w szkolnej szklarni na Księżycu pod kopułą. Rano czujnik rzędu B wysłał sygnał: sadzonki dostały za mało światła, choć lampa nad rzędem świeciła cały ranek. Mechanik mówi, że lampa migała przy włączaniu. Pik podejrzewa swój wózek. A w szklarni była jeszcze wycieczka. Pomóż ustalić, co zasłaniało światło, gdzie usunąć przeszkodę i jak oddać sadzonkom brakujące minuty.",
 "ending": "Światło zasłaniały dwa razy różne rzeczy: od {e1} do {s2} wózek Pika ze skrzynkami, od {e2} do {s3} wycieczka przy rzędzie B. Miganie lampy było przed rozpoczęciem planu i na nic nie wpłynęło. Dla wózka znaleziono wnękę {ni#A|B|C|D}, a grupom przydzielono platformę P3 poza smugami światła. Dodatkowa lampa o połowie mocy pracowała od {xs} do {xe} i uzupełniła {miss|minutę|minuty|minut}. Rząd B dostał swoje {plan} minut.",
 "question": "Lampa rzędu B świeciła {lampon|minutę|minuty|minut}, a sadzonki dostały {got}. Dlaczego sprawna lampa nie znaczy jeszcze, że oświetlenie jest w porządku?",
 "steps": [
  step("Ile światła zabrakło?", "Pod kopułą Pik pokazuje dziennik czujnika rzędu B. Czujnik stoi tuż przy sadzonkach i zapisuje tylko to światło, które do nich dociera. Lampa nad rzędem prowadzi osobny dziennik.",
   ["Według planu tego ranka każdy rząd ma dostać {plan} minut światła.", "Czujnik rzędu B zapisał światło od {s1} do {e1}, od {s2} do {e2} i od {s3} do {e3}.", "Dziennik lampy rzędu B: świeciła od {s1} do {e3} bez wyłączeń."],
   "Ilu minut światła zabrakło rzędowi B? Wpisz liczbę.", "number", [], [],
   "Trzy odcinki: {l1} + {l2} + {l3} = {got} minut. Według planu {plan}, brakuje {plan} - {got} = {miss} minut.",
   "Lampa świeciła {lampon|minutę|minuty|minut}, a do sadzonek dotarło {got}. Czyli między lampą a rzędem dwa razy coś było: od {e1} do {s2} i od {e2} do {s3}. Pik otwiera dziennik przemieszczeń.", "Otwórz dziennik przemieszczeń",
   ["Dodaj trzy odcinki, w każdym policz minuty od początku do końca.", "Plan to {plan} minut. Porównaj z tym, co się uzbierało.", "Brakuje dokładnie różnicy między planem a sumą odcinków."], 0),
  step("Co zasłaniało światło?", "Przy rzędzie B Pik rozłożył wszystko, co wydarzyło się rano. Dwie przerwy bez światła są już znane: od {e1} do {s2} i od {e2} do {s3}. Sprawdź każde zdarzenie według czasu: czy mieści się w przerwie i czy może zasłonić lampę.",
   ["Pik postawił wózek z wysokimi skrzynkami przy rzędzie B o {e1} i zabrał go o {s2}.", "Według rozkładu wycieczka stała przy rzędzie B od {e2} do {s3}: {n} osób między lampą a sadzonkami.", "Mechanik zapisał: lampa rzędu B migała o {fl} przy włączaniu, potem świeciła równo.", "Zasłony kopuły zamykają się na obiad o {bl} i otwierają o 11:00."],
   "Co zasłaniało światło rzędowi B?", "choice", ["Tylko wózek Pika", "Tylko wycieczka", "Wózek w pierwszej przerwie i wycieczka w drugiej", "Miganie lampy przy włączaniu"],
   ["Wózek wyjaśnia przerwę od {e1} do {s2}. Ale światło znikło jeszcze raz, od {e2} do {s3}, kiedy wózka już nie było.", "Wycieczka wyjaśnia przerwę od {e2} do {s3}. Ale pierwsza przerwa zaczęła się o {e1}, {dgap|minutę|minuty|minut} przed wycieczką.", "", "Lampa migała o {fl}, przed początkiem planu o {s1}. O {s1} czujnik widział już równe światło."],
   "Pierwsza przerwa zgadza się z wózkiem: postawiony o {e1}, zabrany o {s2}. Druga zgadza się z wycieczką: od {e2} do {s3}. Miganie było przed {s1}, zasłony zamknęły się po {e3}. Przyczyny są dwie i obie trzeba usunąć.",
   "Przeszkody są dwie: wózek i ludzie przed rzędem. Wózek potrzebuje stałego miejsca, a grupy platformy poza smugami światła. Idziemy do wnęk na korytarzu.", "Wybierz miejsce dla wózka i grupy",
   ["Porównaj każde zdarzenie z dwiema przerwami bez światła.", "Jedno zdarzenie nie wyjaśni obu przerw, jeśli było tylko w jednej z nich.", "Zdarzenie przed {s1} albo po {e3} nie wpływa na poranny plan."], 1),
  step("Gdzie usunąć przeszkody?", "Na korytarzu są cztery wnęki na wózek i trzy platformy dla wycieczek. Pik zmierzył wszystko miarką. Trzeba wybrać jedną wnękę i jedną platformę tak, żeby ani jedno, ani drugie nie przeszkadzało lampom.",
   ["Wózek zajmuje {cw} cm szerokości, a obok niego w tej samej wnęce potrzebne jest przejście nie węższe niż {pw} cm.", "Wnęki: A {na} cm, B {nb} cm, C {nc} cm, D {nd} cm. Wnęka D wchodzi w smugę lampy rzędu C.", "Na wycieczce jest {n} osób, każda potrzebuje {pp} cm wzdłuż barierki platformy.", "Platformy: P1 o długości {p1} m, P2 o długości {p2} m przed lampą rzędu A, P3 o długości {p3} m poza wszystkimi smugami."],
   "Zaznacz jedną wnękę dla wózka i jedną platformę dla wycieczek.", "multi", ["Wnęka A", "Wnęka B", "Wnęka C", "Wnęka D", "Platforma P1", "Platforma P2", "Platforma P3"], [],
   "Wózek z przejściem potrzebuje {cw} + {pw} = {need} cm. Pasują {ni#A|B|C|D} ({nw}) i D ({nd}), ale D jest w smudze lampy rzędu C, zostaje {ni#A|B|C|D}. Grupa potrzebuje {n} × {pp} cm = {needcm} cm, czyli {needm} m. P1 jest za krótka, P2 stoi przed lampą rzędu A, pasuje P3.",
   "Wózek stoi teraz we wnęce {ni#A|B|C|D}, wycieczki czekają na platformie P3. Zostało oddać rzędowi B brakujące {miss|minutę|minuty|minut} światła.", "Ustaw dodatkową lampę",
   ["Najpierw policz, ile centymetrów potrzebuje wózek razem z przejściem i ile metrów potrzebuje grupa.", "Pasujących rozmiarem miejsc jest więcej niż jedno. Odrzuć te, które stoją w smudze jakiejś lampy.", "Potrzebne są dokładnie dwie odpowiedzi: jedna wnęka i jedna platforma."], 2),
  step("Kiedy wyłączyć doświetlanie?", "Na pulpicie szklarni Pik włącza dodatkową lampę nad rzędem B. Jest słabsza od głównej, więc czas trzeba przeliczyć.",
   ["Rzędowi B brakuje {miss|minuty|minut|minut} światła głównej lampy.", "Dodatkowa lampa daje dwa razy mniej światła: żeby uzupełnić jedną minutę głównej, musi pracować dwie.", "Pik włączy dodatkową lampę o {xs}.", "Główna lampa jest w tym czasie wyłączona według planu i nie liczy się."],
   "O której wyłączyć dodatkową lampę, żeby uzupełnić dokładnie brak? Wpisz czas GG:MM.", "time", [], [],
   "{miss|minuta|minuty|minut} głównej lampy to {miss} × 2 = {extra} minut dodatkowej. {xs} + {extra} minut = {xe}.",
   "O {xe} rząd B dostanie wszystkie {plan} minut według planu. Wózek jest we wnęce, platforma wybrana i poranna awaria już się nie powtórzy.", "Zakończ kontrolę szklarni",
   ["Każdą brakującą minutę dodatkowa lampa uzupełnia w dwie.", "Podwój brak z pierwszego kroku.", "Dodaj ten czas do {xs}."], 3)
 ]}
L['en'] = {
 "title": "Signal from the Moon Greenhouse",
 "intro": "Pik the robot looks after seedlings in a school greenhouse under a dome on the Moon. This morning the sensor in row B sent a signal: the seedlings got too little light, even though the lamp above the row was on all morning. The mechanic says the lamp flickered when it was switched on. Pik suspects his own cart. And there was a school trip in the greenhouse too. Help work out what blocked the light, where to move the obstacle, and how to give the seedlings back their missing minutes.",
 "ending": "The light was blocked twice, by different things: from {e1} to {s2} by Pik’s cart of crates, and from {e2} to {s3} by the school trip standing at row B. The lamp’s flicker happened before the plan began and changed nothing. The cart got niche {ni#A|B|C|D}, and groups now wait on platform P3, outside every beam. The half-power extra lamp ran from {xs} to {xe} and made up the {miss} minutes. Row B received its {plan} minutes.",
 "question": "The lamp in row B was on for {lampon} minutes, but the seedlings received {got}. Why does a working lamp not yet mean the lighting is fine?",
 "steps": [
  step("How much light was missing?", "Under the dome, Pik shows the log of the row B sensor. The sensor stands right beside the seedlings and records only the light that actually reaches them. The lamp above the row keeps its own separate log.",
   ["According to the plan, every row should receive {plan} minutes of light this morning.", "The row B sensor recorded light from {s1} to {e1}, from {s2} to {e2} and from {s3} to {e3}.", "The row B lamp log: on from {s1} to {e3} without being switched off."],
   "How many minutes of light did row B miss? Enter a number.", "number", [], [],
   "Three stretches: {l1} + {l2} + {l3} = {got} minutes. The plan says {plan}, so {plan} - {got} = {miss} minutes are missing.",
   "The lamp was on for {lampon} minutes, but only {got} reached the seedlings. So something was between the lamp and the row twice: from {e1} to {s2} and from {e2} to {s3}. Pik opens the movement log.", "Open the movement log",
   ["Add up the three stretches, counting the minutes from start to end in each.", "The plan is {plan} minutes. Compare it with what was collected.", "Exactly the difference between the plan and the sum of the stretches is missing."], 0),
  step("What blocked the light?", "At row B, Pik has laid out everything that happened this morning. The two gaps without light are already known: from {e1} to {s2} and from {e2} to {s3}. Check each event by time: does it fall inside a gap, and could it block the lamp?",
   ["Pik parked the cart with tall crates at row B at {e1} and took it away at {s2}.", "According to the timetable, the school trip stood at row B from {e2} to {s3}: {n} people between the lamp and the seedlings.", "The mechanic noted that the row B lamp flickered at {fl} when switched on, then shone steadily.", "The dome blinds close for lunch at {bl} and open again at 11:00."],
   "What blocked the light from row B?", "choice", ["Only Pik’s cart", "Only the school trip", "The cart in the first gap and the school trip in the second", "The lamp flickering when switched on"],
   ["The cart explains the gap from {e1} to {s2}. But the light disappeared again from {e2} to {s3}, when the cart was already gone.", "The school trip explains the gap from {e2} to {s3}. But the first gap began at {e1}, {dgap|minute|minutes} before the trip.", "", "The lamp flickered at {fl}, before the plan started at {s1}. At {s1} the sensor already saw steady light."],
   "The first gap matches the cart: parked at {e1}, removed at {s2}. The second matches the school trip: from {e2} to {s3}. The flicker was before {s1}, and the blinds closed after {e3}. There are two causes, and both need fixing.",
   "Two obstacles: the cart and people in front of the row. The cart needs a permanent place, and groups need a platform outside the beams. Let’s go to the niches in the corridor.", "Choose places for the cart and the group",
   ["Compare each event with the two gaps without light.", "One event cannot explain both gaps if it happened during only one of them.", "An event before {s1} or after {e3} does not affect the morning plan."], 1),
  step("Where to put the obstacles?", "The corridor has four niches for the cart and three platforms for school trips. Pik has measured everything with a tape. You need to choose one niche and one platform so that neither gets in the way of the lamps.",
   ["The cart is {cw} cm wide, and beside it in the same niche there must be a passage at least {pw} cm wide.", "Niches: A {na} cm, B {nb} cm, C {nc} cm, D {nd} cm. Niche D is in the beam of the row C lamp.", "There are {n} people on a school trip, and each needs {pp} cm along the platform rail.", "Platforms: P1 is {p1} m long, P2 is {p2} m long and in front of the row A lamp, P3 is {p3} m long and outside every beam."],
   "Select one niche for the cart and one platform for school trips.", "multi", ["Niche A", "Niche B", "Niche C", "Niche D", "Platform P1", "Platform P2", "Platform P3"], [],
   "The cart plus passage needs {cw} + {pw} = {need} cm. {ni#A|B|C|D} ({nw}) and D ({nd}) fit, but D is in the beam of the row C lamp, so {ni#A|B|C|D} remains. The group needs {n} × {pp} cm = {needcm} cm, which is {needm} m. P1 is too short, P2 stands in front of the row A lamp, so P3 fits.",
   "The cart now stands in niche {ni#A|B|C|D}, and school trips wait on platform P3. All that remains is to give row B its missing {miss} minutes of light.", "Set up the extra lamp",
   ["First work out how many centimetres the cart needs together with the passage, and how many metres the group needs.", "More than one place fits by size. Rule out the ones that stand in some lamp’s beam.", "Exactly two answers are needed: one niche and one platform."], 2),
  step("When to switch off the extra light?", "At the greenhouse control panel, Pik switches on an extra lamp above row B. It is weaker than the main one, so the time has to be recalculated.",
   ["Row B is missing {miss} minutes of light from the main lamp.", "The extra lamp gives half as much light: to make up one minute of the main lamp, it has to run for two.", "Pik will switch on the extra lamp at {xs}.", "The main lamp is off at that time according to the plan and does not count."],
   "What time should the extra lamp be switched off to make up exactly the shortfall? Enter the time as HH:MM.", "time", [], [],
   "{miss} minutes of the main lamp is {miss} × 2 = {extra} minutes of the extra lamp. {xs} + {extra} minutes = {xe}.",
   "At {xe} row B will have received all {plan} minutes of the plan. The cart is in its niche, the platform is chosen, and this morning’s failure will not happen again.", "Finish the greenhouse check",
   ["The extra lamp makes up each missing minute in two.", "Double the shortfall from the first step.", "Add that time to {xs}."], 3)
 ]}
L['uk'] = {
 "title": "Сигнал з місячної оранжереї",
 "intro": "Робот Пік доглядає за паростками в навчальній місячній оранжереї під куполом. Уранці датчик ряду Б надіслав сигнал: паростки недоотримали світло, хоча лампа над рядом горіла весь ранок. Механік каже, що лампа блимала при увімкненні. Пік підозрює свій візок. А ще в оранжереї була екскурсія. Допоможи зрозуміти, що закривало світло, куди прибрати перешкоду і як повернути паросткам хвилини, яких бракує.",
 "ending": "Світло закривали двічі і різні речі: з {e1} до {s2} візок Піка з ящиками, з {e2} до {s3} екскурсія біля ряду Б. Блимання лампи було до початку плану і ні на що не вплинуло. Візку знайшли нішу {ni#А|Б|В|Г}, а групам відвели майданчик П3 поза променями. Додаткова лампа з половинною силою працювала з {xs} до {xe} і надолужила {miss|хвилину|хвилини|хвилин}. Ряд Б отримав свої {plan} хвилин.",
 "question": "Лампа ряду Б горіла {lampon|хвилину|хвилини|хвилин}, а паростки отримали {got}. Чому справна лампа ще не означає, що освітлення в порядку?",
 "steps": [
  step("Скільки світла не вистачило?", "Під куполом Пік показує журнал датчика ряду Б. Датчик стоїть біля самих паростків і записує лише те світло, яке до них доходить. Лампа над рядом пише свій журнал окремо.",
   ["За планом цього ранку кожен ряд має отримати {plan} хвилин світла.", "Датчик ряду Б записав світло з {s1} до {e1}, з {s2} до {e2} і з {s3} до {e3}.", "Журнал лампи ряду Б: горіла з {s1} до {e3} без вимкнень."],
   "Скільки хвилин світла недоотримав ряд Б? Введи число.", "number", [], [],
   "Три відрізки: {l1} + {l2} + {l3} = {got} хвилин. За планом {plan}, бракує {plan} - {got} = {miss} хвилин.",
   "Лампа горіла {lampon|хвилину|хвилини|хвилин}, а до паростків дійшло {got}. Отже, між лампою і рядом щось було двічі: з {e1} до {s2} і з {e2} до {s3}. Пік відкриває журнал переміщень.", "Відкрити журнал переміщень",
   ["Додай три відрізки, у кожному порахуй хвилини від початку до кінця.", "План {plan} хвилин. Порівняй з тим, що набралося.", "Бракує рівно різниці між планом і сумою відрізків."], 0),
  step("Що закривало світло?", "Біля ряду Б Пік розклав усе, що сталося вранці. Два проміжки без світла вже відомі: з {e1} до {s2} і з {e2} до {s3}. Перевір кожну подію за часом: чи потрапляє вона в проміжок і чи може закрити лампу.",
   ["Пік поставив візок із високими ящиками біля ряду Б о {e1} і забрав його о {s2}.", "За розкладом екскурсія стояла біля ряду Б з {e2} до {s3}: {n} людей між лампою і паростками.", "Механік записав: лампа ряду Б блимала о {fl} при увімкненні, потім горіла рівно.", "Штори купола зачиняються на обід о {bl} і відчиняються об 11:00."],
   "Що закривало світло від ряду Б?", "choice", ["Лише візок Піка", "Лише екскурсія", "Візок у перший проміжок і екскурсія в другий", "Блимання лампи при увімкненні"],
   ["Візок пояснює проміжок з {e1} до {s2}. Але світло зникало ще раз, з {e2} до {s3}, коли візка вже не було.", "Екскурсія пояснює проміжок з {e2} до {s3}. Але перший проміжок почався о {e1}, за {dgap|хвилину|хвилини|хвилин} до екскурсії.", "", "Лампа блимала о {fl}, до початку плану о {s1}. О {s1} датчик уже бачив рівне світло."],
   "Перший проміжок збігається з візком: поставили о {e1}, забрали о {s2}. Другий збігається з екскурсією: з {e2} до {s3}. Блимання було до {s1}, штори зачинилися після {e3}. Причин дві, і обидві треба усунути.",
   "Перешкод дві: візок і люди перед рядом. Візку потрібне постійне місце, а групам майданчик поза променями. Ідемо до ніш у коридорі.", "Вибрати місце для візка і групи",
   ["Порівняй кожну подію з двома проміжками без світла.", "Одна подія не може пояснити обидва проміжки, якщо вона була лише в одному з них.", "Подія до {s1} або після {e3} на ранковий план не впливає."], 1),
  step("Куди прибрати перешкоди?", "У коридорі чотири ніші для візка і три майданчики для екскурсій. Пік виміряв усе рулеткою. Треба вибрати одну нішу і один майданчик так, щоб ні те, ні інше не заважало лампам.",
   ["Візок займає {cw} см завширшки, і поруч із ним у тій самій ніші потрібен прохід не вужчий за {pw} см.", "Ніші: А {na} см, Б {nb} см, В {nc} см, Г {nd} см. Ніша Г потрапляє в промінь лампи ряду В.", "На екскурсії {n} людей, кожному потрібно {pp} см уздовж поручнів майданчика.", "Майданчики: П1 завдовжки {p1} м, П2 завдовжки {p2} м перед лампою ряду А, П3 завдовжки {p3} м поза всіма променями."],
   "Познач одну нішу для візка і один майданчик для екскурсій.", "multi", ["Ніша А", "Ніша Б", "Ніша В", "Ніша Г", "Майданчик П1", "Майданчик П2", "Майданчик П3"], [],
   "Візку з проходом потрібно {cw} + {pw} = {need} см. Підходять {ni#А|Б|В|Г} ({nw}) і Г ({nd}), але Г у промені лампи ряду В, залишається {ni#А|Б|В|Г}. Групі потрібно {n} × {pp} см = {needcm} см, тобто {needm} м. П1 закоротка, П2 стоїть перед лампою ряду А, підходить П3.",
   "Візок тепер стоїть у ніші {ni#А|Б|В|Г}, екскурсії чекають на майданчику П3. Залишилося повернути ряду Б {miss|хвилину|хвилини|хвилин} світла, яких бракує.", "Налаштувати додаткову лампу",
   ["Спершу порахуй, скільки сантиметрів потрібно візку разом із проходом і скільки метрів потрібно групі.", "Підхожих за розміром місць більше ніж одне. Відкинь ті, що стоять у промені якоїсь лампи.", "Потрібно рівно дві відповіді: одна ніша і один майданчик."], 2),
  step("Коли вимкнути підсвітку?", "На пульті оранжереї Пік вмикає додаткову лампу над рядом Б. Вона слабша за основну, тому час треба перерахувати.",
   ["Ряду Б бракує {miss|хвилини|хвилин|хвилин} світла основної лампи.", "Додаткова лампа дає вдвічі менше світла: щоб надолужити одну хвилину основної, вона має працювати дві.", "Пік увімкне додаткову лампу о {xs}.", "Основна лампа в цей час вимкнена за планом і не рахується."],
   "О котрій вимкнути додаткову лампу, щоб надолужити рівно нестачу? Введи час ГГ:ХХ.", "time", [], [],
   "{miss|хвилина|хвилини|хвилин} основної лампи це {miss} × 2 = {extra} хвилин додаткової. {xs} + {extra} хвилин = {xe}.",
   "О {xe} ряд Б отримає всі {plan} хвилин за планом. Візок у ніші, майданчик вибрано, і ранковий збій більше не повториться.", "Завершити перевірку оранжереї",
   ["Кожну хвилину, якої бракує, додаткова лампа надолужує за дві.", "Подвой нестачу з першого кроку.", "Додай цей час до {xs}."], 3)
 ]}
if __name__ == '__main__':
    write_case('greenhouse', '005', L, variants())
