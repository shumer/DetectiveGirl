from common import step, write_case, add, T
def variants():
    out = []
    data = [
        dict(rs='16:20', fp=25, br=10, stars=72, poster=18, per=9, cc='11:00', sf='15:10', bd=45, ac='16:00', fe=33, bow=2, runs=3, pz=4),
        dict(rs='16:10', fp=30, br=15, stars=90, poster=20, per=10, cc='10:30', sf='15:00', bd=50, ac='16:10', fe=40, bow=3, runs=3, pz=5),
        dict(rs='16:30', fp=20, br=10, stars=84, poster=24, per=12, cc='11:30', sf='15:20', bd=30, ac='16:00', fe=29, bow=2, runs=4, pz=3),
        dict(rs='16:00', fp=35, br=12, stars=66, poster=22, per=11, cc='10:00', sf='15:05', bd=40, ac='15:50', fe=43, bow=2, runs=3, pz=6),
    ]
    for d in data:
        rem = d['stars'] - d['poster']; g = rem // d['per']; wrong = d['stars'] // d['per']
        assert rem % d['per'] == 0 and d['stars'] % d['per'] == 0 and wrong != g
        f4 = g + 1 if g + 1 != wrong else g - 1
        wrongm = d['fp'] + d['br']
        built = add(d['sf'], d['bd']); assert T(built) <= T(d['ac'])
        scene = d['fe'] - d['fp'] - d['bow']; assert scene > 0
        tot1 = d['runs'] * scene; pauses = d['runs'] - 1; tot2 = pauses * d['pz']; end = add(d['ac'], tot1 + tot2)
        v = dict(rs=d['rs'], fp=d['fp'], br=d['br'], wrongm=wrongm, stars=d['stars'], poster=d['poster'], per=d['per'], rem=rem, g=g, wrong=wrong, f4=f4, cc=d['cc'],
                 sf=d['sf'], bd=d['bd'], built=built, ac=d['ac'], fe=d['fe'], bow=d['bow'], scene=scene, runs=d['runs'], pauses=pauses, pz=d['pz'], tot1=tot1, tot2=tot2, end=end)
        out.append({'values': v, 'answers': [str(d['fp']), 2, 0, end]})
    return out
L = {}
L['ru'] = {
 "title": "Театр потерянного финала",
 "intro": "Перед спектаклем в папке режиссёра нашлись четыре разных финала: «Мост», «Плавание», «Бал» и «Фонарь». Никто не отметил, какой репетировали вчера, а актёры на уроках до {ac}. В архиве несколько записей репетиций без подписей, и реквизитор принёс список на сегодня, где есть лодка. Помоги найти вчерашнюю запись, определить финал и рассчитать сегодняшнюю репетицию.",
 "ending": "Финал начинается на {fp}-й минуте файла, потому что камера стояла на паузе весь перерыв. Вчерашняя запись это файл 3: {g|гирлянда|гирлянды|гирлянд} из {rem} оставшихся звёзд и новый синий занавес. По декорациям подошёл только «Мост», а лодка из списка реквизита оказалась из первого акта. Мост поставят к {built}, актёры прогонят финал {runs|раз|раза|раз} и закончат в {end}.",
 "question": "У файла 1 тоже {g|гирлянда|гирлянды|гирлянд}. Почему он всё равно не вчерашний?",
 "steps": [
  step("Где в файле начинается финал?", "В архиве режиссёр открывает длинную запись репетиции. Известно, как шла репетиция и как работала камера.",
   ["Репетиция началась в {rs}, запись включили в тот же момент.", "Первая часть длилась {fp} минут, затем был перерыв {br} минут, после него сразу начался финал.", "На перерыв камеру ставили на паузу, и после перерыва запись продолжилась с того же места файла."],
   "На какой минуте файла начинается финал? Введи число.", "number", [], [],
   "Перерыв в файл не попал: камера стояла на паузе. В файле идут {fp} минут первой части и сразу финал, поэтому он начинается на {fp}-й минуте, а не на {wrongm}-й.",
   "На {fp}-й минуте в кадре сцена с гирляндами и мостом. Но в архиве несколько файлов без подписей, и сначала нужно убедиться, что открыт именно вчерашний.", "Сверить записи",
   ["Перерыв в файл не попал: камера стояла на паузе.", "В файле идёт только первая часть, а потом сразу финал.", "Сколько минут длилась первая часть?"], 1),
  step("Какая запись вчерашняя?", "На сцене реквизитор показывает, что осталось от вчерашних украшений, а режиссёр листает файлы без подписей. Вчера утром сменили занавес. Найди файл, у которого совпадает всё.",
   ["Вчера было {stars} звёзд. {poster} из них закрепили на афише, а все остальные распределили поровну на гирлянды, по {per} звёзд на каждую.", "Вчера в {cc} красный занавес заменили новым синим. Все вчерашние репетиции были после этого.", "Файл 1: {g} гирлянд, красный занавес.", "Файл 2: {wrong} гирлянд, синий занавес.", "Файл 3: {g} гирлянд, синий занавес.", "Файл 4: {f4} гирлянд, синий занавес."],
   "Какой файл записан вчера?", "choice", ["Файл 1", "Файл 2", "Файл 3", "Файл 4"],
   ["Гирлянды совпадают, но занавес красный. Его сняли вчера в {cc}, значит запись сделана раньше.", "{wrong} гирлянд получится, если разделить все {stars} звёзд на {per}. Но {poster} звёзд ушли на афишу.", "", "{f4} гирлянд не получается ни при каком счёте: {rem} звёзд на {per} делятся без остатка."],
   "{stars} - {poster} = {rem} звёзд на гирлянды, {rem} : {per} = {g} гирлянд. Синий занавес висит с {cc} вчера. {g} гирлянд и синий занавес только в файле 3.",
   "Вчерашняя запись найдена: файл 3. В кадре финала {g|гирлянда|гирлянды|гирлянд} и мост, лодки и фонаря нет. Теперь сравним это с четырьмя текстами.", "Сравнить четыре финала",
   ["Сначала посчитай, сколько гирлянд сделали вчера: звёзды для афиши в гирлянды не пошли.", "Занавес тоже улика: красный занавес сняли до всех вчерашних репетиций.", "Должны совпасть оба признака: и число гирлянд, и цвет занавеса."], 0),
  step("Какой финал репетировали?", "У реквизита режиссёр раскладывает четыре текста. В каждом указано, что обязательно должно быть на сцене. Реквизитор принёс список на сегодня и в нём есть лодка, но не спеши.",
   ["На вчерашней записи: {g|гирлянда|гирлянды|гирлянд}, мост, в руках у актёров ничего нет.", "«Мост»: {g} гирлянд и мост.", "«Плавание»: {g} гирлянд и лодка.", "«Бал»: {wrong} гирлянд и мост.", "«Фонарь»: {g} гирлянд, мост и фонарь в руках у актёра.", "Список реквизита на сегодня: лодка для первого акта, мост для финала."],
   "Какой текст совпадает со вчерашней записью?", "choice", ["«Мост»", "«Плавание»", "«Бал»", "«Фонарь»"],
   ["", "Лодка есть в списке на сегодня, но для первого акта. В кадре финала лодки нет, там мост.", "На записи {g|гирлянда|гирлянды|гирлянд}, а «Балу» нужно {wrong}.", "Мост и гирлянды совпадают, но фонаря в руках у актёров на записи нет."],
   "«Мост» совпадает по всем признакам: {g|гирлянда|гирлянды|гирлянд}, мост, ничего в руках. У «Плавания» лодка, у «Бала» {wrong} гирлянд, у «Фонаря» лишний предмет. Лодка из списка реквизита относится к первому акту и на финал не указывает.",
   "Финал найден: «Мост». Осталось рассчитать сегодняшнюю репетицию, чтобы актёры успели прогнать финал несколько раз.", "Составить план репетиции",
   ["Сравни каждый текст со всеми признаками на записи, а не с одним.", "Список реквизита на сегодня говорит о сегодняшнем спектакле целиком, а не о финале.", "Лишний предмет на сцене тоже несовпадение."], 2),
  step("Когда закончится репетиция?", "За столом режиссёр составляет план. Сцена освободится после занятий, мост нужно собрать до прихода актёров, а финал прогнать несколько раз с паузами.",
   ["Сцена свободна с {sf}. Сборка моста занимает {bd} минут.", "Актёры приходят в {ac} и сразу начинают первый прогон.", "На вчерашней записи финал шёл с {fp}-й по {fe}-ю минуту файла, включая поклон {bow|минуту|минуты|минут}. Сегодня прогоняют без поклона.", "Прогонов {runs}, между соседними прогонами пауза {pz|минута|минуты|минут}."],
   "Во сколько закончится последний прогон? Введи время ЧЧ:ММ.", "time", [], [],
   "Мост готов к {built}, до прихода актёров. Финал без поклона: {fe} - {fp} - {bow} = {scene} минут. {runs} прогона по {scene} минут это {tot1} минут, между ними {pauses|пауза|паузы|пауз} по {pz|минуте|минуты|минут}, ещё {tot2}. {ac} + {tot1} + {tot2} минут = {end}.",
   "План готов: мост к {built}, актёры в {ac}, последний прогон заканчивается в {end}. Режиссёр убирает три других финала в архив.", "Передать план режиссёру",
   ["Сначала проверь, что сцена будет готова к приходу актёров.", "Прогонов {runs}, а пауз между ними только {pauses}.", "Сложи все прогоны и паузы между ними и прибавь к {ac}."], 3)
 ]}
L['pl'] = {
 "title": "Teatr zaginionego finału",
 "intro": "Przed spektaklem w teczce reżysera znalazły się cztery różne finały: „Most”, „Rejs”, „Bal” i „Latarnia”. Nikt nie zaznaczył, który próbowano wczoraj, a aktorzy są na lekcjach do {ac}. W archiwum jest kilka nagrań prób bez podpisów, a rekwizytor przyniósł listę na dziś, na której jest łódka. Pomóż znaleźć wczorajsze nagranie, ustalić finał i zaplanować dzisiejszą próbę.",
 "ending": "Finał zaczyna się w {fp}. minucie pliku, bo kamera była zatrzymana przez całą przerwę. Wczorajsze nagranie to plik 3: {g|girlanda|girlandy|girland} z {rem} pozostałych gwiazd i nowa niebieska kurtyna. Do dekoracji pasował tylko „Most”, a łódka z listy rekwizytów okazała się z pierwszego aktu. Most ustawią do {built}, aktorzy przejdą finał {runs|raz|razy|razy} i skończą o {end}.",
 "question": "Plik 1 też ma {g|girlandę|girlandy|girland}. Dlaczego mimo to nie jest wczorajszy?",
 "steps": [
  step("Gdzie w pliku zaczyna się finał?", "W archiwum reżyser otwiera długie nagranie próby. Wiadomo, jak przebiegała próba i jak działała kamera.",
   ["Próba zaczęła się o {rs}, nagranie włączono w tym samym momencie.", "Pierwsza część trwała {fp} minut, potem była przerwa {br} minut, a zaraz po niej zaczął się finał.", "Na przerwę kamerę zatrzymano i po przerwie nagranie ruszyło z tego samego miejsca pliku."],
   "W której minucie pliku zaczyna się finał? Wpisz liczbę.", "number", [], [],
   "Przerwa nie trafiła do pliku: kamera była zatrzymana. W pliku jest {fp} minut pierwszej części i od razu finał, więc zaczyna się on w {fp}. minucie, a nie w {wrongm}.",
   "W {fp}. minucie w kadrze jest scena z girlandami i mostem. Ale w archiwum jest kilka plików bez podpisów i najpierw trzeba się upewnić, że otwarty jest właśnie wczorajszy.", "Porównaj nagrania",
   ["Przerwa nie trafiła do pliku: kamera była zatrzymana.", "W pliku jest tylko pierwsza część, a potem od razu finał.", "Ile minut trwała pierwsza część?"], 1),
  step("Które nagranie jest wczorajsze?", "Na scenie rekwizytor pokazuje, co zostało z wczorajszych dekoracji, a reżyser przegląda pliki bez podpisów. Wczoraj rano wymieniono kurtynę. Znajdź plik, w którym zgadza się wszystko.",
   ["Wczoraj były {stars} gwiazdy. {poster} z nich przypięto do afisza, a wszystkie pozostałe rozdzielono po równo na girlandy, po {per} gwiazd na każdą.", "Wczoraj o {cc} czerwoną kurtynę wymieniono na nową niebieską. Wszystkie wczorajsze próby były po tym.", "Plik 1: {g} girland, czerwona kurtyna.", "Plik 2: {wrong} girland, niebieska kurtyna.", "Plik 3: {g} girland, niebieska kurtyna.", "Plik 4: {f4} girland, niebieska kurtyna."],
   "Który plik nagrano wczoraj?", "choice", ["Plik 1", "Plik 2", "Plik 3", "Plik 4"],
   ["Girlandy się zgadzają, ale kurtyna jest czerwona. Zdjęto ją wczoraj o {cc}, więc nagranie powstało wcześniej.", "{wrong} girland wyjdzie, jeśli podzielić wszystkie {stars} gwiazd przez {per}. Ale {poster} gwiazd poszło na afisz.", "", "{f4} girland nie wychodzi przy żadnym liczeniu: {rem} gwiazd dzieli się przez {per} bez reszty."],
   "{stars} - {poster} = {rem} gwiazd na girlandy, {rem} : {per} = {g} girland. Niebieska kurtyna wisi od wczoraj od {cc}. {g} girland i niebieska kurtyna są tylko w pliku 3.",
   "Wczorajsze nagranie znalezione: plik 3. W kadrze finału jest {g|girlanda|girlandy|girland} i most, nie ma łódki ani latarni. Teraz porównamy to z czterema tekstami.", "Porównaj cztery finały",
   ["Najpierw policz, ile girland zrobiono wczoraj: gwiazdy na afisz nie poszły na girlandy.", "Kurtyna też jest poszlaką: czerwoną kurtynę zdjęto przed wszystkimi wczorajszymi próbami.", "Muszą się zgadzać obie cechy: liczba girland i kolor kurtyny."], 0),
  step("Który finał próbowano?", "Przy rekwizytach reżyser rozkłada cztery teksty. W każdym zapisano, co koniecznie musi być na scenie. Rekwizytor przyniósł listę na dziś i jest na niej łódka, ale nie spiesz się.",
   ["Na wczorajszym nagraniu: {g|girlanda|girlandy|girland}, most, aktorzy nic nie trzymają w rękach.", "„Most”: {g} girland i most.", "„Rejs”: {g} girland i łódka.", "„Bal”: {wrong} girland i most.", "„Latarnia”: {g} girland, most i latarnia w ręku aktora.", "Lista rekwizytów na dziś: łódka do pierwszego aktu, most do finału."],
   "Który tekst zgadza się z wczorajszym nagraniem?", "choice", ["„Most”", "„Rejs”", "„Bal”", "„Latarnia”"],
   ["", "Łódka jest na liście na dziś, ale do pierwszego aktu. W kadrze finału nie ma łódki, jest most.", "Na nagraniu jest {g|girlanda|girlandy|girland}, a „Bal” potrzebuje {wrong}.", "Most i girlandy się zgadzają, ale latarni w rękach aktorów na nagraniu nie ma."],
   "„Most” zgadza się we wszystkim: {g|girlanda|girlandy|girland}, most, nic w rękach. „Rejs” ma łódkę, „Bal” {wrong} girland, „Latarnia” dodatkowy przedmiot. Łódka z listy rekwizytów należy do pierwszego aktu i nie wskazuje na finał.",
   "Finał znaleziony: „Most”. Zostało zaplanować dzisiejszą próbę, żeby aktorzy zdążyli przejść finał kilka razy.", "Ułóż plan próby",
   ["Porównaj każdy tekst ze wszystkimi cechami nagrania, a nie z jedną.", "Lista rekwizytów na dziś mówi o całym dzisiejszym spektaklu, a nie o finale.", "Dodatkowy przedmiot na scenie to też niezgodność."], 2),
  step("Kiedy skończy się próba?", "Przy stole reżyser układa plan. Scena zwolni się po zajęciach, most trzeba złożyć przed przyjściem aktorów, a finał przejść kilka razy z przerwami.",
   ["Scena jest wolna od {sf}. Składanie mostu zajmuje {bd} minut.", "Aktorzy przychodzą o {ac} i od razu zaczynają pierwsze przejście.", "Na wczorajszym nagraniu finał trwał od {fp}. do {fe}. minuty pliku, łącznie z ukłonem {bow|minuta|minuty|minut}. Dziś przechodzą bez ukłonu.", "Przejść jest {runs}, między sąsiednimi przejściami przerwa {pz|minuta|minuty|minut}."],
   "O której skończy się ostatnie przejście? Wpisz czas GG:MM.", "time", [], [],
   "Most gotowy na {built}, przed przyjściem aktorów. Finał bez ukłonu: {fe} - {fp} - {bow} = {scene} minut. {runs} przejścia po {scene} minut to {tot1} minut, między nimi {pauses|przerwa|przerwy|przerw} po {pz|minucie|minuty|minut}, jeszcze {tot2}. {ac} + {tot1} + {tot2} minut = {end}.",
   "Plan gotowy: most na {built}, aktorzy o {ac}, ostatnie przejście kończy się o {end}. Reżyser odkłada trzy pozostałe finały do archiwum.", "Przekaż plan reżyserowi",
   ["Najpierw sprawdź, czy scena będzie gotowa na przyjście aktorów.", "Przejść jest {runs}, a przerw między nimi tylko {pauses}.", "Dodaj wszystkie przejścia i przerwy między nimi, a potem dodaj to do {ac}."], 3)
 ]}
L['en'] = {
 "title": "The Theatre of the Lost Finale",
 "intro": "Before the play, four different finales turned up in the director’s folder: “The Bridge”, “The Voyage”, “The Ball” and “The Lantern”. Nobody marked which one was rehearsed yesterday, and the actors are in lessons until {ac}. The archive holds several unlabelled rehearsal recordings, and the props manager has brought today’s list, which includes a boat. Help find yesterday’s recording, identify the finale and plan today’s rehearsal.",
 "ending": "The finale starts at minute {fp} of the file, because the camera was paused for the whole break. Yesterday’s recording is file 3: {g} garlands made from the {rem} remaining stars, and the new blue curtain. Only “The Bridge” matched the set, and the boat on the props list turned out to belong to act one. The bridge will be built by {built}, the actors will run the finale {runs} times and finish at {end}.",
 "question": "File 1 also has {g} garlands. Why is it still not yesterday’s recording?",
 "steps": [
  step("Where in the file does the finale start?", "In the archive, the director opens a long rehearsal recording. We know how the rehearsal went and how the camera worked.",
   ["The rehearsal began at {rs}, and the recording was started at the same moment.", "The first part lasted {fp} minutes, then there was a {br}-minute break, and the finale began straight after it.", "The camera was paused for the break, and after the break the recording continued from the same point in the file."],
   "At what minute of the file does the finale start? Enter a number.", "number", [], [],
   "The break did not make it into the file: the camera was paused. The file holds {fp} minutes of the first part and then the finale immediately, so it starts at minute {fp}, not {wrongm}.",
   "At minute {fp} the frame shows a stage with garlands and a bridge. But there are several unlabelled files in the archive, and first we need to be sure this one is yesterday’s.", "Compare the recordings",
   ["The break did not make it into the file: the camera was paused.", "The file holds only the first part, and then the finale straight away.", "How many minutes did the first part last?"], 1),
  step("Which recording is yesterday’s?", "On stage, the props manager shows what is left of yesterday’s decorations while the director flicks through the unlabelled files. The curtain was replaced yesterday morning. Find the file where everything matches.",
   ["Yesterday there were {stars} stars. {poster} of them were fixed to the poster, and all the rest were shared equally between garlands, {per} stars each.", "Yesterday at {cc} the red curtain was replaced with a new blue one. All of yesterday’s rehearsals came after that.", "File 1: {g} garlands, red curtain.", "File 2: {wrong} garlands, blue curtain.", "File 3: {g} garlands, blue curtain.", "File 4: {f4} garlands, blue curtain."],
   "Which file was recorded yesterday?", "choice", ["File 1", "File 2", "File 3", "File 4"],
   ["The garlands match, but the curtain is red. It was taken down yesterday at {cc}, so this recording was made earlier.", "You get {wrong} garlands if you divide all {stars} stars by {per}. But {poster} stars went on the poster.", "", "{f4} garlands do not come out of any calculation: {rem} stars divide by {per} exactly."],
   "{stars} - {poster} = {rem} stars for garlands, {rem} ÷ {per} = {g} garlands. The blue curtain has been up since {cc} yesterday. {g} garlands and a blue curtain appear only in file 3.",
   "Yesterday’s recording is found: file 3. The finale frame shows {g} garlands and a bridge, with no boat and no lantern. Now let’s compare that with the four scripts.", "Compare the four finales",
   ["First work out how many garlands were made yesterday: the poster stars did not go into garlands.", "The curtain is a clue too: the red curtain came down before all of yesterday’s rehearsals.", "Both features must match: the number of garlands and the colour of the curtain."], 0),
  step("Which finale was rehearsed?", "By the props, the director lays out four scripts. Each one lists what must be on stage. The props manager has brought today’s list and it includes a boat, but do not rush.",
   ["In yesterday’s recording: {g} garlands, a bridge, and the actors hold nothing.", "“The Bridge”: {g} garlands and a bridge.", "“The Voyage”: {g} garlands and a boat.", "“The Ball”: {wrong} garlands and a bridge.", "“The Lantern”: {g} garlands, a bridge and a lantern in an actor’s hand.", "Today’s props list: a boat for act one, a bridge for the finale."],
   "Which script matches yesterday’s recording?", "choice", ["“The Bridge”", "“The Voyage”", "“The Ball”", "“The Lantern”"],
   ["", "The boat is on today’s list, but for act one. There is no boat in the finale frame, there is a bridge.", "The recording shows {g} garlands, and “The Ball” needs {wrong}.", "The bridge and the garlands match, but there is no lantern in the actors’ hands in the recording."],
   "“The Bridge” matches on every point: {g} garlands, a bridge, nothing in hand. “The Voyage” has a boat, “The Ball” has {wrong} garlands, “The Lantern” has an extra object. The boat on the props list belongs to act one and says nothing about the finale.",
   "The finale is found: “The Bridge”. All that remains is to plan today’s rehearsal so the actors can run the finale several times.", "Plan the rehearsal",
   ["Compare each script with all the features of the recording, not just one.", "Today’s props list describes the whole of today’s play, not the finale.", "An extra object on stage is a mismatch too."], 2),
  step("When will the rehearsal end?", "At the table, the director draws up a plan. The stage will be free after lessons, the bridge must be built before the actors arrive, and the finale has to be run several times with breaks.",
   ["The stage is free from {sf}. Building the bridge takes {bd} minutes.", "The actors arrive at {ac} and start the first run straight away.", "In yesterday’s recording the finale ran from minute {fp} to minute {fe} of the file, including a {bow}-minute bow. Today they run it without the bow.", "There are {runs} runs, with a {pz}-minute break between neighbouring runs."],
   "What time will the last run end? Enter the time as HH:MM.", "time", [], [],
   "The bridge is ready by {built}, before the actors arrive. The finale without the bow: {fe} - {fp} - {bow} = {scene} minutes. {runs} runs of {scene} minutes make {tot1} minutes, with {pauses} {pz}-minute breaks between them, another {tot2}. {ac} + {tot1} + {tot2} minutes = {end}.",
   "The plan is ready: bridge by {built}, actors at {ac}, last run ending at {end}. The director files the other three finales away in the archive.", "Hand the plan to the director",
   ["First check that the stage will be ready when the actors arrive.", "There are {runs} runs, but only {pauses} breaks between them.", "Add up all the runs and the breaks between them, then add that to {ac}."], 3)
 ]}
L['uk'] = {
 "title": "Театр загубленого фіналу",
 "intro": "Перед виставою в теці режисера знайшлися чотири різні фінали: «Міст», «Плавання», «Бал» і «Ліхтар». Ніхто не позначив, який репетирували вчора, а актори на уроках до {ac}. В архіві кілька записів репетицій без підписів, і реквізитор приніс список на сьогодні, де є човен. Допоможи знайти вчорашній запис, визначити фінал і розрахувати сьогоднішню репетицію.",
 "ending": "Фінал починається на {fp}-й хвилині файлу, бо камера стояла на паузі всю перерву. Вчорашній запис це файл 3: {g|гірлянда|гірлянди|гірлянд} із {rem} зірок, що залишилися, і нова синя завіса. За декораціями підійшов лише «Міст», а човен зі списку реквізиту виявився з першої дії. Міст поставлять до {built}, актори проженуть фінал {runs|раз|рази|разів} і закінчать о {end}.",
 "question": "У файлу 1 теж {g|гірлянда|гірлянди|гірлянд}. Чому він усе одно не вчорашній?",
 "steps": [
  step("Де у файлі починається фінал?", "В архіві режисер відкриває довгий запис репетиції. Відомо, як ішла репетиція і як працювала камера.",
   ["Репетиція почалася о {rs}, запис увімкнули в той самий момент.", "Перша частина тривала {fp} хвилин, потім була перерва {br} хвилин, після неї одразу почався фінал.", "На перерву камеру ставили на паузу, і після перерви запис продовжився з того самого місця файлу."],
   "На якій хвилині файлу починається фінал? Введи число.", "number", [], [],
   "Перерва у файл не потрапила: камера стояла на паузі. У файлі йдуть {fp} хвилин першої частини і одразу фінал, тому він починається на {fp}-й хвилині, а не на {wrongm}-й.",
   "На {fp}-й хвилині в кадрі сцена з гірляндами і мостом. Але в архіві кілька файлів без підписів, і спершу треба переконатися, що відкрито саме вчорашній.", "Звірити записи",
   ["Перерва у файл не потрапила: камера стояла на паузі.", "У файлі йде лише перша частина, а потім одразу фінал.", "Скільки хвилин тривала перша частина?"], 1),
  step("Який запис учорашній?", "На сцені реквізитор показує, що залишилося від учорашніх прикрас, а режисер гортає файли без підписів. Учора вранці змінили завісу. Знайди файл, у якого збігається все.",
   ["Учора було {stars} зірок. {poster} із них закріпили на афіші, а всі інші розподілили порівну на гірлянди, по {per} зірок на кожну.", "Учора о {cc} червону завісу замінили новою синьою. Усі вчорашні репетиції були після цього.", "Файл 1: {g} гірлянд, червона завіса.", "Файл 2: {wrong} гірлянд, синя завіса.", "Файл 3: {g} гірлянд, синя завіса.", "Файл 4: {f4} гірлянд, синя завіса."],
   "Який файл записано вчора?", "choice", ["Файл 1", "Файл 2", "Файл 3", "Файл 4"],
   ["Гірлянди збігаються, але завіса червона. Її зняли вчора о {cc}, отже запис зроблено раніше.", "{wrong} гірлянд вийде, якщо поділити всі {stars} зірок на {per}. Але {poster} зірок пішли на афішу.", "", "{f4} гірлянд не виходить за жодного рахунку: {rem} зірок діляться на {per} без остачі."],
   "{stars} - {poster} = {rem} зірок на гірлянди, {rem} : {per} = {g} гірлянд. Синя завіса висить з {cc} учора. {g} гірлянд і синя завіса лише у файлі 3.",
   "Учорашній запис знайдено: файл 3. У кадрі фіналу {g|гірлянда|гірлянди|гірлянд} і міст, човна і ліхтаря немає. Тепер порівняємо це з чотирма текстами.", "Порівняти чотири фінали",
   ["Спершу порахуй, скільки гірлянд зробили вчора: зірки для афіші в гірлянди не пішли.", "Завіса теж доказ: червону завісу зняли до всіх учорашніх репетицій.", "Мають збігтися обидві ознаки: і кількість гірлянд, і колір завіси."], 0),
  step("Який фінал репетирували?", "Біля реквізиту режисер розкладає чотири тексти. У кожному вказано, що обов’язково має бути на сцені. Реквізитор приніс список на сьогодні, і в ньому є човен, але не поспішай.",
   ["На вчорашньому записі: {g|гірлянда|гірлянди|гірлянд}, міст, у руках в акторів нічого немає.", "«Міст»: {g} гірлянд і міст.", "«Плавання»: {g} гірлянд і човен.", "«Бал»: {wrong} гірлянд і міст.", "«Ліхтар»: {g} гірлянд, міст і ліхтар у руках в актора.", "Список реквізиту на сьогодні: човен для першої дії, міст для фіналу."],
   "Який текст збігається з учорашнім записом?", "choice", ["«Міст»", "«Плавання»", "«Бал»", "«Ліхтар»"],
   ["", "Човен є у списку на сьогодні, але для першої дії. У кадрі фіналу човна немає, там міст.", "На записі {g|гірлянда|гірлянди|гірлянд}, а «Балу» потрібно {wrong}.", "Міст і гірлянди збігаються, але ліхтаря в руках в акторів на записі немає."],
   "«Міст» збігається за всіма ознаками: {g|гірлянда|гірлянди|гірлянд}, міст, нічого в руках. У «Плавання» човен, у «Балу» {wrong} гірлянд, у «Ліхтаря» зайвий предмет. Човен зі списку реквізиту стосується першої дії і на фінал не вказує.",
   "Фінал знайдено: «Міст». Залишилося розрахувати сьогоднішню репетицію, щоб актори встигли прогнати фінал кілька разів.", "Скласти план репетиції",
   ["Порівняй кожен текст з усіма ознаками на записі, а не з однією.", "Список реквізиту на сьогодні говорить про сьогоднішню виставу цілком, а не про фінал.", "Зайвий предмет на сцені теж незбіг."], 2),
  step("Коли закінчиться репетиція?", "За столом режисер складає план. Сцена звільниться після занять, міст треба зібрати до приходу акторів, а фінал прогнати кілька разів із паузами.",
   ["Сцена вільна з {sf}. Збирання моста займає {bd} хвилин.", "Актори приходять о {ac} і одразу починають перший прогін.", "На вчорашньому записі фінал ішов з {fp}-ї по {fe}-ту хвилину файлу, разом із поклоном {bow|хвилина|хвилини|хвилин}. Сьогодні проганяють без поклону.", "Прогонів {runs}, між сусідніми прогонами пауза {pz|хвилина|хвилини|хвилин}."],
   "О котрій закінчиться останній прогін? Введи час ГГ:ХХ.", "time", [], [],
   "Міст готовий до {built}, до приходу акторів. Фінал без поклону: {fe} - {fp} - {bow} = {scene} хвилин. {runs} прогони по {scene} хвилин це {tot1} хвилин, між ними {pauses|пауза|паузи|пауз} по {pz|хвилині|хвилини|хвилин}, ще {tot2}. {ac} + {tot1} + {tot2} хвилин = {end}.",
   "План готовий: міст до {built}, актори о {ac}, останній прогін закінчується о {end}. Режисер прибирає три інші фінали в архів.", "Передати план режисерові",
   ["Спершу перевір, що сцена буде готова до приходу акторів.", "Прогонів {runs}, а пауз між ними лише {pauses}.", "Додай усі прогони і паузи між ними і додай до {ac}."], 3)
 ]}
if __name__ == '__main__':
    write_case('theatre', '006', L, variants())
