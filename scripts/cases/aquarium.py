from common import step, write_case, add, T, hm
def variants():
    out = []
    data = [
        dict(wf=3, obs=['10:05', '10:11', '10:17'], ic=4, shoff=3, dl=6, until='10:44', ss='11:10', sl=30, f1=5, iv2=6, margin=2),
        dict(wf=4, obs=['10:08', '10:13', '10:18'], ic=3, shoff=2, dl=4, until='10:34', ss='11:00', sl=40, f1=4, iv2=7, margin=3),
        dict(wf=2, obs=['10:04', '10:11', '10:18'], ic=5, shoff=3, dl=7, until='11:05', ss='11:30', sl=35, f1=3, iv2=5, margin=2),
        dict(wf=5, obs=['10:13', '10:21', '10:29'], ic=6, shoff=3, dl=8, until='10:48', ss='12:00', sl=30, f1=6, iv2=8, margin=4),
    ]
    for d in data:
        r = [add(o, -d['wf']) for o in d['obs']]; iv = T(r[1]) - T(r[0]); assert T(r[2]) - T(r[1]) == iv
        nxt = add(r[2], iv); after = add(nxt, iv)
        c2 = add(r[0], d['ic']); assert c2 != r[1]
        sh0 = add(r[0], d['shoff']); sh1, sh2 = add(sh0, iv), add(sh0, 2 * iv); assert sh0 not in r and sh1 not in r
        ch0 = add(r[0], -iv); boff = add(r[2], 1) if iv < 4 else add(r[2], iv // 2); assert T(r[2]) < T(boff) < T(nxt)
        ts = add(ch0, -d['dl']); span = T(d['until']) - T(ch0); assert span % iv == 0; gaps = span // iv; cnt = gaps + 1
        soff = add(nxt, 2)
        send = add(d['ss'], d['sl']); allowed = add(send, -d['margin'])
        rings = []; t = T(d['ss']) + d['f1']
        while t <= T(allowed): rings.append(hm(t)); t += d['iv2']
        nextring = hm(t); cnt2 = len(rings); assert cnt2 >= 3
        v = dict(wf=d['wf'], o1=d['obs'][0], o2=d['obs'][1], o3=d['obs'][2], r1=r[0], r2=r[1], r3=r[2], iv=iv, nxt=nxt, after=after,
                 ic=d['ic'], c2=c2, sh0=sh0, sh1=sh1, sh2=sh2, ch0=ch0, boff=boff, dl=d['dl'], ts=ts, until=d['until'], span=span, gaps=gaps, cnt=cnt, soff=soff,
                 ss=d['ss'], sl=d['sl'], f1=d['f1'], iv2=d['iv2'], margin=d['margin'], send=send, allowed=allowed, ringsList=', '.join(rings), nextring=nextring, cnt2=cnt2, last=rings[-1])
        out.append({'values': v, 'answers': [nxt, 3, str(cnt), str(cnt2)]})
    return out
L = {}
L['ru'] = {
 "title": "Аквариум и загадка пузырьков",
 "intro": "В выставочном аквариуме без экскурсии вдруг пошли ровные кольца пузырьков. Рыб здесь нет, только игрушки с механизмами: замок, лодка, ракушка и сундук. Посетитель уверен, что кольца пускает замок, у него самые толстые трубки. Смотритель записал время колец, но его часы спешат. Помоги найти, какая игрушка работает сама по себе, почему она включилась и как настроить показ для гостей.",
 "ending": "Кольца пускал сундук, а не лодка и не замок. Расписание лодки совпадало с наблюдениями, но смотритель выключил её в {boff}, а кольцо в {nxt} всё равно появилось. Сундук запустила вчерашняя проверочная программа с автозапуском в {ts}. Для сеанса в {ss} смотритель задал {cnt2|кольцо|кольца|колец}, чтобы последнее вышло не позже {allowed}.",
 "question": "Лодка выпускала бы кольца ровно в те же минуты, что и сундук. Что окончательно доказало, что виновата не она?",
 "steps": [
  step("Когда ждать следующее кольцо?", "У аквариума смотритель показывает три записи в блокноте. Он записывал время по своим наручным часам, а механизмы игрушек работают по точному времени.",
   ["По часам смотрителя кольца появились в {o1}, {o2} и {o3}.", "Часы смотрителя спешат на {wf|минуту|минуты|минут}.", "Предположим, что кольца идут через равные промежутки."],
   "Во сколько по точному времени появится следующее кольцо? Введи время ЧЧ:ММ.", "time", [], [],
   "По точному времени кольца были в {r1}, {r2} и {r3}: из каждого наблюдения вычитаем {wf|минуту|минуты|минут}. Промежуток {iv|минута|минуты|минут}, значит следующее в {nxt}.",
   "В {nxt} кольцо действительно появилось. Кольца идут каждые {iv|минуту|минуты|минут}, начиная с {r1} или раньше. Идём к пульту сравнивать программы игрушек.", "Открыть программы игрушек",
   ["Часы смотрителя спешат: настоящее время меньше, чем он записал.", "Переведи все три наблюдения в точное время и найди промежуток между ними.", "Прибавь промежуток к последнему точному времени."], 0),
  step("Какая игрушка пускает кольца?", "На пульте четыре программы, по одной на игрушку. Каждая задаёт, когда игрушка выпускает первое кольцо и как часто следующие. Смотритель успел провести один опыт, а посетитель настаивает на замке.",
   ["Наблюдения по точному времени: {r1}, {r2}, {r3}, {nxt}.", "Замок: первое кольцо в {r1}, затем каждые {ic|минуту|минуты|минут}.", "Лодка: первое кольцо в {r1}, затем каждые {iv|минуту|минуты|минут}.", "Ракушка: первое кольцо в {sh0}, затем каждые {iv|минуту|минуты|минут}.", "Сундук: первое кольцо в {ch0}, затем каждые {iv|минуту|минуты|минут}.", "В {boff} смотритель выключил программу лодки. Кольцо в {nxt} всё равно появилось.", "Посетитель говорит, что кольца пускает замок: у него самые толстые трубки."],
   "Какая игрушка выпускает кольца?", "choice", ["Замок", "Лодка", "Ракушка", "Сундук"],
   ["Замок дал бы второе кольцо в {c2}, а не в {r2}. Толстые трубки не меняют расписание.", "Расписание лодки совпадает со всеми наблюдениями. Но её выключили в {boff}, а кольцо в {nxt} всё равно появилось.", "Ракушка начинает в {sh0} и дальше даёт {sh1}, {sh2}: ни одно время не совпадает.", ""],
   "Замок отпадает по промежутку, ракушка по времени начала. Лодка и сундук дают одинаковые минуты: {r1}, {r2}, {r3}, {nxt}. Разделил их опыт: лодку выключили в {boff}, а кольцо в {nxt} появилось, значит его пустил сундук. Первое кольцо сундука в {ch0} смотритель просто не видел.",
   "Кольца пускает сундук. Смотритель выключает его программу, и в {after} кольца нет. Теперь выясним, почему сундук включился без экскурсии.", "Открыть журнал сундука",
   ["Сначала отбрось программы, у которых не совпадает промежуток или время первого кольца.", "Если две программы дают одни и те же минуты, расписание их не различит. Ищи опыт, который различает.", "Что произошло с кольцами после того, как лодку выключили?"], 1),
  step("Откуда взялся ранний запуск?", "В журнале сундука осталась вчерашняя проверочная программа с автозапуском. Смотритель хочет убедиться, что именно она объясняет кольца, и понять, сколько колец вышло бы без вмешательства.",
   ["Проверочная программа запускается автоматически в {ts} и перед первым кольцом ждёт {dl|минуту|минуты|минут}.", "Дальше она выпускает кольцо каждые {iv|минуту|минуты|минут}, пока её не выключат.", "Смотритель выключил программу в {soff}, но хочет знать, что было бы, если бы она работала до конца утра: до {until} включительно."],
   "Сколько колец выпустил бы сундук с первого кольца до {until} включительно? Введи число.", "number", [], [],
   "Первое кольцо в {ts} + {dl} минут = {ch0}, это совпадает с расписанием сундука. От {ch0} до {until} проходит {span} минут, это {span} : {iv} = {gaps} промежутков. Колец на одно больше, чем промежутков: {cnt}.",
   "Проверочная программа объясняет и первое кольцо, и все следующие. Смотритель удаляет автозапуск и настраивает программу для сеанса.", "Настроить программу показа",
   ["Сначала найди время первого кольца: к моменту запуска прибавь ожидание.", "Посчитай минуты от первого кольца до последнего и раздели на промежуток.", "Первое кольцо тоже считается: колец на одно больше, чем промежутков."], 2),
  step("Сколько колец увидят гости?", "Смотритель готовит показ. Новая программа сундука начнётся вместе с сеансом, а последнее кольцо должно успеть подняться до конца сеанса.",
   ["Сеанс начинается в {ss} и длится {sl} минут.", "Первое кольцо выходит через {f1|минуту|минуты|минут} после начала сеанса, дальше каждые {iv2|минуту|минуты|минут}.", "Последнее кольцо должно выйти не позже чем за {margin|минуту|минуты|минут} до конца сеанса, иначе гости не увидят, как оно поднимется."],
   "Сколько колец нужно задать в программе? Введи число.", "number", [], [],
   "Сеанс заканчивается в {send}, последнее кольцо не позже {allowed}. Кольца: {ringsList}, следующее в {nextring} уже поздно. Итого {cnt2|кольцо|кольца|колец}.",
   "Смотритель задаёт {cnt2|кольцо|кольца|колец}, последнее в {last}. Сундук больше не включается сам, а посетитель узнал, что толстые трубки ничего не доказывают.", "Открыть показ пузырьков",
   ["Выпиши моменты колец по порядку от первого.", "Найди последний разрешённый момент: конец сеанса минус {margin|минута|минуты|минут}.", "Отбрось кольца после этого момента."], 3)
 ]}
L['pl'] = {
 "title": "Akwarium i zagadka bąbelków",
 "intro": "W wystawowym akwarium bez wycieczki nagle poszły równe kręgi bąbelków. Ryb tu nie ma, tylko zabawki z mechanizmami: zamek, łódka, muszla i skrzynia. Zwiedzający jest pewien, że kręgi puszcza zamek, bo ma najgrubsze rurki. Opiekun zapisał czasy kręgów, ale jego zegarek się spieszy. Pomóż ustalić, która zabawka działa sama z siebie, dlaczego się włączyła i jak ustawić pokaz dla gości.",
 "ending": "Kręgi puszczała skrzynia, a nie łódka ani zamek. Rozkład łódki zgadzał się z obserwacjami, ale opiekun wyłączył ją o {boff}, a krąg o {nxt} i tak się pojawił. Skrzynię uruchomił wczorajszy program testowy z autostartem o {ts}. Na seans o {ss} opiekun ustawił {cnt2|krąg|kręgi|kręgów}, żeby ostatni wyszedł najpóźniej o {allowed}.",
 "question": "Łódka wypuszczałaby kręgi dokładnie w tych samych minutach co skrzynia. Co ostatecznie dowiodło, że to nie ona?",
 "steps": [
  step("Kiedy spodziewać się następnego kręgu?", "Przy akwarium opiekun pokazuje trzy zapisy w notesie. Zapisywał czas według swojego zegarka, a mechanizmy zabawek działają według dokładnego czasu.",
   ["Według zegarka opiekuna kręgi pojawiły się o {o1}, {o2} i {o3}.", "Zegarek opiekuna spieszy się o {wf|minutę|minuty|minut}.", "Załóżmy, że kręgi idą w równych odstępach."],
   "O której według dokładnego czasu pojawi się następny krąg? Wpisz czas GG:MM.", "time", [], [],
   "Według dokładnego czasu kręgi były o {r1}, {r2} i {r3}: od każdej obserwacji odejmujemy {wf|minutę|minuty|minut}. Odstęp to {iv|minuta|minuty|minut}, więc następny o {nxt}.",
   "O {nxt} krąg rzeczywiście się pojawił. Kręgi idą co {iv|minutę|minuty|minut}, począwszy od {r1} albo wcześniej. Idziemy do pulpitu porównać programy zabawek.", "Otwórz programy zabawek",
   ["Zegarek opiekuna się spieszy: prawdziwy czas jest wcześniejszy niż zapisał.", "Przelicz wszystkie trzy obserwacje na dokładny czas i znajdź odstęp między nimi.", "Dodaj odstęp do ostatniego dokładnego czasu."], 0),
  step("Która zabawka puszcza kręgi?", "Na pulpicie są cztery programy, po jednym na zabawkę. Każdy określa, kiedy zabawka wypuszcza pierwszy krąg i jak często następne. Opiekun zdążył zrobić jeden eksperyment, a zwiedzający upiera się przy zamku.",
   ["Obserwacje według dokładnego czasu: {r1}, {r2}, {r3}, {nxt}.", "Zamek: pierwszy krąg o {r1}, potem co {ic|minutę|minuty|minut}.", "Łódka: pierwszy krąg o {r1}, potem co {iv|minutę|minuty|minut}.", "Muszla: pierwszy krąg o {sh0}, potem co {iv|minutę|minuty|minut}.", "Skrzynia: pierwszy krąg o {ch0}, potem co {iv|minutę|minuty|minut}.", "O {boff} opiekun wyłączył program łódki. Krąg o {nxt} i tak się pojawił.", "Zwiedzający mówi, że kręgi puszcza zamek: ma najgrubsze rurki."],
   "Która zabawka wypuszcza kręgi?", "choice", ["Zamek", "Łódka", "Muszla", "Skrzynia"],
   ["Zamek dałby drugi krąg o {c2}, a nie o {r2}. Grube rurki nie zmieniają rozkładu.", "Rozkład łódki zgadza się ze wszystkimi obserwacjami. Ale wyłączono ją o {boff}, a krąg o {nxt} i tak się pojawił.", "Muszla zaczyna o {sh0} i dalej daje {sh1}, {sh2}: żaden czas się nie zgadza.", ""],
   "Zamek odpada przez odstęp, muszla przez czas początku. Łódka i skrzynia dają te same minuty: {r1}, {r2}, {r3}, {nxt}. Rozdzielił je eksperyment: łódkę wyłączono o {boff}, a krąg o {nxt} się pojawił, więc puściła go skrzynia. Pierwszego kręgu skrzyni o {ch0} opiekun po prostu nie widział.",
   "Kręgi puszcza skrzynia. Opiekun wyłącza jej program i o {after} kręgu nie ma. Teraz ustalimy, dlaczego skrzynia włączyła się bez wycieczki.", "Otwórz dziennik skrzyni",
   ["Najpierw odrzuć programy, w których nie zgadza się odstęp albo czas pierwszego kręgu.", "Jeśli dwa programy dają te same minuty, rozkład ich nie rozróżni. Szukaj eksperymentu, który rozróżnia.", "Co stało się z kręgami po wyłączeniu łódki?"], 1),
  step("Skąd wziął się wczesny start?", "W dzienniku skrzyni został wczorajszy program testowy z autostartem. Opiekun chce się upewnić, że to właśnie on wyjaśnia kręgi, i zrozumieć, ile kręgów wyszłoby bez interwencji.",
   ["Program testowy uruchamia się automatycznie o {ts} i przed pierwszym kręgiem czeka {dl|minutę|minuty|minut}.", "Dalej wypuszcza krąg co {iv|minutę|minuty|minut}, dopóki się go nie wyłączy.", "Opiekun wyłączył program o {soff}, ale chce wiedzieć, co by było, gdyby działał do końca poranka: do {until} włącznie."],
   "Ile kręgów wypuściłaby skrzynia od pierwszego kręgu do {until} włącznie? Wpisz liczbę.", "number", [], [],
   "Pierwszy krąg o {ts} + {dl} minut = {ch0}, to zgadza się z rozkładem skrzyni. Od {ch0} do {until} mija {span} minut, czyli {span} : {iv} = {gaps} odstępów. Kręgów jest o jeden więcej niż odstępów: {cnt}.",
   "Program testowy wyjaśnia i pierwszy krąg, i wszystkie następne. Opiekun usuwa autostart i ustawia program na seans.", "Ustaw program pokazu",
   ["Najpierw znajdź czas pierwszego kręgu: do momentu startu dodaj oczekiwanie.", "Policz minuty od pierwszego kręgu do ostatniego i podziel przez odstęp.", "Pierwszy krąg też się liczy: kręgów jest o jeden więcej niż odstępów."], 2),
  step("Ile kręgów zobaczą goście?", "Opiekun przygotowuje pokaz. Nowy program skrzyni zacznie się razem z seansem, a ostatni krąg musi zdążyć wypłynąć przed końcem seansu.",
   ["Seans zaczyna się o {ss} i trwa {sl} minut.", "Pierwszy krąg wychodzi {f1|minutę|minuty|minut} po początku seansu, dalej co {iv2|minutę|minuty|minut}.", "Ostatni krąg musi wyjść najpóźniej {margin|minutę|minuty|minut} przed końcem seansu, inaczej goście nie zobaczą, jak wypływa."],
   "Ile kręgów trzeba ustawić w programie? Wpisz liczbę.", "number", [], [],
   "Seans kończy się o {send}, ostatni krąg najpóźniej o {allowed}. Kręgi: {ringsList}, następny o {nextring} jest już za późno. Razem {cnt2|krąg|kręgi|kręgów}.",
   "Opiekun ustawia {cnt2|krąg|kręgi|kręgów}, ostatni o {last}. Skrzynia już nie włącza się sama, a zwiedzający dowiedział się, że grube rurki niczego nie dowodzą.", "Otwórz pokaz bąbelków",
   ["Wypisz momenty kręgów po kolei od pierwszego.", "Znajdź ostatni dozwolony moment: koniec seansu minus {margin|minuta|minuty|minut}.", "Odrzuć kręgi po tym momencie."], 3)
 ]}
L['en'] = {
 "title": "The Aquarium and the Bubble Riddle",
 "intro": "In the display aquarium, neat rings of bubbles have started rising with no tour going on. There are no fish here, only mechanical toys: a castle, a boat, a shell and a chest. A visitor is sure the castle makes the rings, because it has the thickest pipes. The keeper wrote down the ring times, but his watch runs fast. Help find which toy is running on its own, why it switched on, and how to set up the show for the guests.",
 "ending": "The rings came from the chest, not the boat and not the castle. The boat’s schedule matched the observations, but the keeper switched it off at {boff} and the ring at {nxt} still appeared. The chest was started by yesterday’s test program with an auto-start at {ts}. For the {ss} session the keeper set {cnt2} rings, so that the last one rises no later than {allowed}.",
 "question": "The boat would have released rings at exactly the same minutes as the chest. What finally proved it was not the boat?",
 "steps": [
  step("When is the next ring due?", "At the aquarium, the keeper shows three entries in his notebook. He wrote the times by his own wristwatch, while the toy mechanisms run on exact time.",
   ["By the keeper’s watch, rings appeared at {o1}, {o2} and {o3}.", "The keeper’s watch is {wf|minute|minutes} fast.", "Let’s assume the rings come at equal intervals."],
   "At what exact time will the next ring appear? Enter the time as HH:MM.", "time", [], [],
   "In exact time the rings came at {r1}, {r2} and {r3}: subtract {wf|minute|minutes} from each observation. The interval is {iv} minutes, so the next one is at {nxt}.",
   "At {nxt} a ring really did appear. The rings come every {iv} minutes, starting at {r1} or earlier. Let’s go to the control panel and compare the toy programs.", "Open the toy programs",
   ["The keeper’s watch is fast: the real time is earlier than he wrote.", "Convert all three observations to exact time and find the interval between them.", "Add the interval to the last exact time."], 0),
  step("Which toy makes the rings?", "The control panel has four programs, one per toy. Each sets when the toy releases its first ring and how often the next ones come. The keeper managed one experiment, and the visitor insists on the castle.",
   ["Observations in exact time: {r1}, {r2}, {r3}, {nxt}.", "Castle: first ring at {r1}, then every {ic} minutes.", "Boat: first ring at {r1}, then every {iv} minutes.", "Shell: first ring at {sh0}, then every {iv} minutes.", "Chest: first ring at {ch0}, then every {iv} minutes.", "At {boff} the keeper switched off the boat’s program. The ring at {nxt} still appeared.", "The visitor says the castle makes the rings: it has the thickest pipes."],
   "Which toy is releasing the rings?", "choice", ["The castle", "The boat", "The shell", "The chest"],
   ["The castle would give its second ring at {c2}, not {r2}. Thick pipes do not change the schedule.", "The boat’s schedule matches every observation. But it was switched off at {boff}, and the ring at {nxt} still appeared.", "The shell starts at {sh0} and then gives {sh1}, {sh2}: none of the times match.", ""],
   "The castle is out because of the interval, the shell because of its start time. The boat and the chest give the same minutes: {r1}, {r2}, {r3}, {nxt}. The experiment told them apart: the boat was switched off at {boff}, and the ring at {nxt} still came, so the chest released it. The keeper simply did not see the chest’s first ring at {ch0}.",
   "The chest makes the rings. The keeper switches off its program, and at {after} there is no ring. Now let’s find out why the chest switched on without a tour.", "Open the chest’s log",
   ["First rule out the programs whose interval or first-ring time does not match.", "If two programs give the same minutes, the schedule cannot tell them apart. Look for the experiment that does.", "What happened to the rings after the boat was switched off?"], 1),
  step("Where did the early start come from?", "The chest’s log still holds yesterday’s test program with an auto-start. The keeper wants to be sure it really explains the rings, and to know how many rings there would have been without anyone stepping in.",
   ["The test program starts automatically at {ts} and waits {dl} minutes before the first ring.", "After that it releases a ring every {iv} minutes until it is switched off.", "The keeper switched the program off at {soff}, but wants to know what would have happened if it had run until the end of the morning: up to and including {until}."],
   "How many rings would the chest have released from its first ring up to and including {until}? Enter a number.", "number", [], [],
   "The first ring at {ts} + {dl} minutes = {ch0}, which matches the chest’s schedule. From {ch0} to {until} is {span} minutes, which is {span} ÷ {iv} = {gaps} intervals. There is one more ring than there are intervals: {cnt}.",
   "The test program explains both the first ring and all the following ones. The keeper deletes the auto-start and sets up the program for the session.", "Set up the show program",
   ["First find the time of the first ring: add the wait to the start time.", "Count the minutes from the first ring to the last and divide by the interval.", "The first ring counts too: there is one more ring than there are intervals."], 2),
  step("How many rings will the guests see?", "The keeper prepares the show. The chest’s new program will start together with the session, and the last ring must have time to rise before the session ends.",
   ["The session starts at {ss} and lasts {sl} minutes.", "The first ring comes {f1} minutes after the session starts, then every {iv2} minutes.", "The last ring must come no later than {margin} minutes before the end of the session, or the guests will not see it rise."],
   "How many rings should be set in the program? Enter a number.", "number", [], [],
   "The session ends at {send}, so the last ring must be no later than {allowed}. The rings: {ringsList}, and the next at {nextring} is too late. {cnt2} rings in total.",
   "The keeper sets {cnt2} rings, the last at {last}. The chest no longer switches itself on, and the visitor has learned that thick pipes prove nothing.", "Open the bubble show",
   ["Write out the ring times in order from the first.", "Find the last allowed moment: the end of the session minus {margin} minutes.", "Drop the rings after that moment."], 3)
 ]}
L['uk'] = {
 "title": "Акваріум і загадка бульбашок",
 "intro": "У виставковому акваріумі без екскурсії раптом пішли рівні кільця бульбашок. Риб тут немає, лише іграшки з механізмами: замок, човен, мушля і скриня. Відвідувач упевнений, що кільця пускає замок, у нього найтовщі трубки. Доглядач записав час кілець, але його годинник поспішає. Допоможи знайти, яка іграшка працює сама по собі, чому вона увімкнулася і як налаштувати показ для гостей.",
 "ending": "Кільця пускала скриня, а не човен і не замок. Розклад човна збігався зі спостереженнями, але доглядач вимкнув його о {boff}, а кільце о {nxt} усе одно з’явилося. Скриню запустила вчорашня перевірочна програма з автозапуском о {ts}. Для сеансу о {ss} доглядач задав {cnt2|кільце|кільця|кілець}, щоб останнє вийшло не пізніше ніж о {allowed}.",
 "question": "Човен випускав би кільця рівно в ті самі хвилини, що й скриня. Що остаточно довело, що винен не він?",
 "steps": [
  step("Коли чекати наступне кільце?", "Біля акваріума доглядач показує три записи в блокноті. Він записував час за своїм наручним годинником, а механізми іграшок працюють за точним часом.",
   ["За годинником доглядача кільця з’явилися о {o1}, {o2} і {o3}.", "Годинник доглядача поспішає на {wf|хвилину|хвилини|хвилин}.", "Припустімо, що кільця йдуть через рівні проміжки."],
   "О котрій за точним часом з’явиться наступне кільце? Введи час ГГ:ХХ.", "time", [], [],
   "За точним часом кільця були о {r1}, {r2} і {r3}: від кожного спостереження віднімаємо {wf|хвилину|хвилини|хвилин}. Проміжок {iv|хвилина|хвилини|хвилин}, отже наступне о {nxt}.",
   "О {nxt} кільце справді з’явилося. Кільця йдуть кожні {iv|хвилину|хвилини|хвилин}, починаючи з {r1} або раніше. Ідемо до пульта порівнювати програми іграшок.", "Відкрити програми іграшок",
   ["Годинник доглядача поспішає: справжній час менший, ніж він записав.", "Переведи всі три спостереження в точний час і знайди проміжок між ними.", "Додай проміжок до останнього точного часу."], 0),
  step("Яка іграшка пускає кільця?", "На пульті чотири програми, по одній на іграшку. Кожна задає, коли іграшка випускає перше кільце і як часто наступні. Доглядач устиг провести один дослід, а відвідувач наполягає на замку.",
   ["Спостереження за точним часом: {r1}, {r2}, {r3}, {nxt}.", "Замок: перше кільце о {r1}, потім кожні {ic|хвилину|хвилини|хвилин}.", "Човен: перше кільце о {r1}, потім кожні {iv|хвилину|хвилини|хвилин}.", "Мушля: перше кільце о {sh0}, потім кожні {iv|хвилину|хвилини|хвилин}.", "Скриня: перше кільце о {ch0}, потім кожні {iv|хвилину|хвилини|хвилин}.", "О {boff} доглядач вимкнув програму човна. Кільце о {nxt} усе одно з’явилося.", "Відвідувач каже, що кільця пускає замок: у нього найтовщі трубки."],
   "Яка іграшка випускає кільця?", "choice", ["Замок", "Човен", "Мушля", "Скриня"],
   ["Замок дав би друге кільце о {c2}, а не о {r2}. Товсті трубки не змінюють розкладу.", "Розклад човна збігається з усіма спостереженнями. Але його вимкнули о {boff}, а кільце о {nxt} усе одно з’явилося.", "Мушля починає о {sh0} і далі дає {sh1}, {sh2}: жоден час не збігається.", ""],
   "Замок відпадає за проміжком, мушля за часом початку. Човен і скриня дають однакові хвилини: {r1}, {r2}, {r3}, {nxt}. Розділив їх дослід: човен вимкнули о {boff}, а кільце о {nxt} з’явилося, отже його пустила скриня. Першого кільця скрині о {ch0} доглядач просто не бачив.",
   "Кільця пускає скриня. Доглядач вимикає її програму, і о {after} кільця немає. Тепер з’ясуємо, чому скриня увімкнулася без екскурсії.", "Відкрити журнал скрині",
   ["Спершу відкинь програми, у яких не збігається проміжок або час першого кільця.", "Якщо дві програми дають ті самі хвилини, розклад їх не розрізнить. Шукай дослід, який розрізняє.", "Що сталося з кільцями після того, як човен вимкнули?"], 1),
  step("Звідки взявся ранній запуск?", "У журналі скрині залишилася вчорашня перевірочна програма з автозапуском. Доглядач хоче переконатися, що саме вона пояснює кільця, і зрозуміти, скільки кілець вийшло б без втручання.",
   ["Перевірочна програма запускається автоматично о {ts} і перед першим кільцем чекає {dl|хвилину|хвилини|хвилин}.", "Далі вона випускає кільце кожні {iv|хвилину|хвилини|хвилин}, поки її не вимкнуть.", "Доглядач вимкнув програму о {soff}, але хоче знати, що було б, якби вона працювала до кінця ранку: до {until} включно."],
   "Скільки кілець випустила б скриня від першого кільця до {until} включно? Введи число.", "number", [], [],
   "Перше кільце о {ts} + {dl} хвилин = {ch0}, це збігається з розкладом скрині. Від {ch0} до {until} минає {span} хвилин, це {span} : {iv} = {gaps} проміжків. Кілець на одне більше, ніж проміжків: {cnt}.",
   "Перевірочна програма пояснює і перше кільце, і всі наступні. Доглядач видаляє автозапуск і налаштовує програму для сеансу.", "Налаштувати програму показу",
   ["Спершу знайди час першого кільця: до моменту запуску додай очікування.", "Порахуй хвилини від першого кільця до останнього і поділи на проміжок.", "Перше кільце теж рахується: кілець на одне більше, ніж проміжків."], 2),
  step("Скільки кілець побачать гості?", "Доглядач готує показ. Нова програма скрині почнеться разом із сеансом, а останнє кільце має встигнути піднятися до кінця сеансу.",
   ["Сеанс починається о {ss} і триває {sl} хвилин.", "Перше кільце виходить через {f1|хвилину|хвилини|хвилин} після початку сеансу, далі кожні {iv2|хвилину|хвилини|хвилин}.", "Останнє кільце має вийти не пізніше ніж за {margin|хвилину|хвилини|хвилин} до кінця сеансу, інакше гості не побачать, як воно підніметься."],
   "Скільки кілець треба задати в програмі? Введи число.", "number", [], [],
   "Сеанс закінчується о {send}, останнє кільце не пізніше ніж о {allowed}. Кільця: {ringsList}, наступне о {nextring} уже пізно. Разом {cnt2|кільце|кільця|кілець}.",
   "Доглядач задає {cnt2|кільце|кільця|кілець}, останнє о {last}. Скриня більше не вмикається сама, а відвідувач дізнався, що товсті трубки нічого не доводять.", "Відкрити показ бульбашок",
   ["Випиши моменти кілець по порядку від першого.", "Знайди останній дозволений момент: кінець сеансу мінус {margin|хвилина|хвилини|хвилин}.", "Відкинь кільця після цього моменту."], 3)
 ]}
if __name__ == '__main__':
    write_case('aquarium', '007', L, variants())
