from common import step, write_case, add, T
def variants():
    out = []
    data = [
        dict(tm=1200, bm=250, pm=150, tl=45, p1len=50, p2len=30, p3len=50, p4len=60, dep='10:25', spd=90, dist=60, fi=0, stop=10, unl=10, mk=12, la='11:20', lb='11:30', db=4, sb=12, lc='11:35', dc=3, sc=6, ld='11:25', dd=5, sd=10, lim=40, back='12:15', tw='13:30', f0='12:00', every=40, fl2=25),
        dict(tm=1100, bm=200, pm=100, tl=40, p1len=45, p2len=35, p3len=50, p4len=60, dep='10:20', spd=60, dist=45, fi=1, stop=5, unl=10, mk=15, la='11:15', lb='11:25', db=5, sb=15, lc='11:30', dc=4, sc=6, ld='11:20', dd=6, sd=12, lim=45, back='12:20', tw='13:15', f0='12:05', every=30, fl2=20),
        dict(tm=1500, bm=300, pm=200, tl=55, p1len=60, p2len=50, p3len=60, p4len=70, dep='10:35', spd=80, dist=40, fi=2, stop=15, unl=10, mk=10, la='11:25', lb='11:35', db=3, sb=12, lc='11:30', dc=6, sc=9, ld='11:30', dd=4, sd=8, lim=50, back='12:25', tw='13:40', f0='12:00', every=45, fl2=30),
        dict(tm=1400, bm=250, pm=150, tl=50, p1len=55, p2len=45, p3len=55, p4len=60, dep='10:50', spd=90, dist=30, fi=3, stop=10, unl=15, mk=8, la='11:30', lb='11:40', db=2, sb=10, lc='11:45', dc=3, sc=6, ld='11:35', dd=4, sd=12, lim=40, back='12:10', tw='13:20', f0='11:50', every=35, fl2=25),
    ]
    fracs = ['2/3', '3/4', '1/2', '1/3']
    kg = lambda g: g / 1000 if g % 1000 else g // 1000
    for d in data:
        tot = d['tm'] + d['bm'] + d['pm']; p4 = tot + d['pm']; p1g = d['tm'] + d['bm']
        assert d['p2len'] < d['tl'] <= d['p3len'] and d['p1len'] >= d['tl']
        fl = d['dist'] * 60 // d['spd']; assert d['dist'] * 60 % d['spd'] == 0
        arr = add(d['dep'], fl + d['stop'] + d['unl']); left = T('12:10') - T(arr); assert left > 0
        latest = add('12:10', -d['mk'])
        assert T(d['la']) < T(arr) <= T(d['lb'])
        tb = d['db'] * 60 // d['sb']; ab = add(d['lb'], tb); assert d['db'] * 60 % d['sb'] == 0 and T(ab) <= T(latest)
        tc = d['dc'] * 60 // d['sc']; ac = add(d['lc'], tc); assert d['dc'] * 60 % d['sc'] == 0 and T(ac) > T(latest) and T(d['lc']) >= T(arr)
        td = d['dd'] * 60 // d['sd']; ad = add(d['ld'], td); assert d['dd'] * 60 % d['sd'] == 0 and T(ad) <= T(latest) and T(d['ld']) >= T(arr) and d['lim'] < d['p3len']
        kmmin = 60 // d['sb']; assert 60 % d['sb'] == 0
        havem = T('12:10') - T(ab); fin = add(ab, d['mk'])
        flights = [add(d['f0'], i * d['every']) for i in range(3)]
        fdep = next(f for f in flights if T(f) > T(d['back'])); tim = add(fdep, d['fl2']); before = T(d['tw']) - T(tim); assert before > 0
        assert T(flights[2]) + d['fl2'] > T(d['tw']) or True
        v = dict(tkg=d['tm'] // 1000, tg=d['tm'] % 1000, tm=d['tm'], bm=d['bm'], pm=d['pm'], tot=tot, totkg=kg(tot), tl=d['tl'],
                 p1=kg(p1g), p1g=p1g, p1len=d['p1len'], p2len=d['p2len'], p3len=d['p3len'], p4kg=p4 // 1000, p4g=p4 % 1000, p4len=d['p4len'],
                 dep=d['dep'], spd=d['spd'], dist=d['dist'], frac=fracs[d['fi']], fi=d['fi'], fl=fl, stop=d['stop'], unl=d['unl'], arr=arr, left=left,
                 mk=d['mk'], latest=latest, la=d['la'], lb=d['lb'], db=d['db'], sb=d['sb'], tb=tb, ab=ab, lc=d['lc'], dc=d['dc'], sc=d['sc'], tc=tc, ac=ac, ld=d['ld'], dd=d['dd'], sd=d['sd'], lim=d['lim'], kmmin=kmmin, havem=havem, fin=fin,
                 back=d['back'], tw=d['tw'], f0=d['f0'], every=d['every'], fl2=d['fl2'], fA=flights[0], fB=flights[1], fC=flights[2], fdep=fdep, tim=tim, before=before)
        out.append({'values': v, 'answers': [2, arr, 1, tim]})
    return out
L = {}
L['ru'] = {
 "title": "Посылка для облачного острова",
 "intro": "На облачном острове к празднику собирают флюгер-петуха. Мастер открыл коробку: вместо хвоста внутри маленький парус. Почтальон Ника уверена, что перепутала две коробки с одинаковым облаком на крышке. На почте четыре невостребованных отправления, у всех размокли ярлыки. Праздник в 12:10, «Ласточка» летает на остров раз в день. Нужно найти хвост, доставить его к мастеру и успеть к празднику. А потом ещё вернуть парус тому, кто его ждёт.",
 "ending": "Хвост нашёлся в третьей коробке: две коробки весили одинаково, и разобраться помогла длина. «Ласточка» долетела за {fl} минут с остановкой, курьер Б привёз хвост в {ab}, и мастер поднял флюгер к 12:10. Парус улетел «Стрижом» в {fdep} и был у лодочника Тима в {tim}. Ника больше не подписывает коробки только рисунком: теперь на каждой адрес и вес.",
 "question": "Две коробки весили ровно {totkg} кг. Почему масса сама по себе не сказала, в какой из них хвост?",
 "steps": [
  step("Какая коробка наша?", "На почте Ника кладёт на весы все четыре отправления и достаёт накладную мастера. Открывать чужие посылки нельзя, поэтому выбрать нужно по накладной, а открыть только одну.",
   ["Накладная мастера: хвост длиной {tl} см, масса {tkg} кг {tg} г. Упакован в коробку массой {bm} г, внутри ещё {pm} г бумаги.", "Отправление №1: {p1} кг, коробка длиной {p1len} см.", "Отправление №2: {totkg} кг, коробка длиной {p2len} см.", "Отправление №3: {totkg} кг, коробка длиной {p3len} см.", "Отправление №4: {p4kg} кг {p4g} г, коробка длиной {p4len} см."],
   "Какое отправление открыть?", "choice", ["Отправление №1", "Отправление №2", "Отправление №3", "Отправление №4"],
   ["{p1} кг это {p1g} г: хвост и коробка без бумаги. Но бумага тоже лежит внутри.", "Масса совпадает, но хвост длиной {tl} см не поместится в коробку длиной {p2len} см.", "", "{p4kg} кг {p4g} г тяжелее нужной массы на {pm} г."],
   "{tm} + {bm} + {pm} = {tot} г, то есть {totkg} кг. Столько весят №2 и №3, но хвост длиной {tl} см поместится только в коробку длиной {p3len} см. Ника открывает №3: внутри хвост петуха.",
   "Хвост найден в отправлении №3. Теперь его нужно отправить на остров «Ласточкой» и понять, сколько времени останется.", "К причалу «Ласточки»",
   ["Переведи всё в граммы и сложи хвост, коробку и бумагу.", "Одинаковую массу могут иметь две коробки. Тогда смотри на размер.", "Хвост длиной {tl} см не согнёшь: коробка должна быть длиннее."], 0),
  step("Когда коробка будет на острове?", "На причале Ника сдаёт коробку на «Ласточку». Капитан показывает маршрут: до острова с одной остановкой на Ветряной башне. Посчитай, когда коробку выдадут курьеру.",
   ["«Ласточка» вылетает в {dep} и летит со скоростью {spd} км/ч.", "До острова {dist} км. По пути одна остановка на Ветряной башне, {stop} минут.", "После прибытия разгрузка занимает {unl} минут, потом коробку выдают курьеру."],
   "Во сколько коробку выдадут курьеру на острове? Введи время ЧЧ:ММ.", "time", [], [],
   "{dist} км при скорости {spd} км/ч это {frac} часа, то есть {fl} минут. Остановка {stop} минут и разгрузка {unl} минут. {dep} + {fl} + {stop} + {unl} минут = {arr}.",
   "Коробку выдадут в {arr}. До праздника в 12:10 остаётся {left} минут, и их надо разделить между дорогой курьера и работой мастера.", "Выбрать курьера",
   ["Сначала узнай, сколько минут займёт сам полёт: за час {spd} км, значит какую часть часа займут {dist} км?", "{dist} из {spd} это {fi#две трети|три четверти|половина|одна треть}. Переведи {fi#две трети|три четверти|половину|одну треть} часа в минуты.", "К полёту прибавь остановку и разгрузку, а потом всё к {dep}."], 1),
  step("Кто довезёт хвост?", "На площади острова четыре курьера, у каждого свой рейс по расписанию: время выезда изменить нельзя. Ника записала для каждого, когда он выезжает, сколько ехать и что он берёт.",
   ["Коробку выдают в {arr}. Праздник в 12:10. Мастеру нужно {mk} минут: установить хвост и проверить флюгер.", "Курьер А: выезжает в {la}, едет 3 км со скоростью 12 км/ч.", "Курьер Б: выезжает в {lb}, едет {db} км со скоростью {sb} км/ч.", "Курьер В: выезжает в {lc}, идёт с тележкой {dc} км со скоростью {sc} км/ч.", "Курьер Г: выезжает в {ld}, едет {dd} км со скоростью {sd} км/ч, но берёт только коробки длиной до {lim} см."],
   "Кто довезёт хвост так, чтобы мастер успел к 12:10?", "choice", ["Курьер А", "Курьер Б", "Курьер В", "Курьер Г"],
   ["Курьер А выезжает в {la}, а коробку выдадут только в {arr}.", "", "{dc} км при {sc} км/ч это {tc} минут: курьер В приедет в {ac}, и мастеру не хватит {mk} минут.", "По времени курьер Г успевает, но наша коробка длиной {p3len} см, а он берёт только до {lim} см."],
   "Мастеру нужно {mk} минут, значит хвост должен быть у него не позже {latest}. Б: {db} км при {sb} км/ч это {tb} минут, приедет в {ab}. А уезжает до выдачи, В приедет в {ac}, Г не берёт такие коробки.",
   "Ника договаривается с курьером Б: он забирает коробку в {lb} и привозит мастеру в {ab}. У мастера {havem} минут на работу, которая занимает {mk}.", "Собрать флюгер",
   ["Сначала посчитай, к какому времени хвост должен быть у мастера.", "Время дороги: расстояние раздели на скорость. При {sb} км/ч один километр занимает {kmmin} минут.", "Проверь у каждого три вещи: время выезда, время прибытия и подходит ли коробка."], 3),
  step("Куда девать парус?", "В трюме «Ласточки» мастер устанавливает хвост: в {fin} флюгер готов, к 12:10 петух на башне. Осталась вторая половина ошибки Ники: коробка с парусом, которую ждёт лодочник Тим на Малом острове.",
   ["Курьер Б привезёт коробку с парусом обратно на площадь к {back}.", "Тим ждёт парус на своём причале на Малом острове до {tw}.", "«Стриж» летает на Малый остров каждые {every} минут, первый рейс в {f0}. Полёт занимает {fl2} минут.", "Коробку грузят только на рейс, который вылетает после того, как её привезли на площадь."],
   "Во сколько самое раннее парус будет у Тима? Введи время ЧЧ:ММ.", "time", [], [],
   "Рейсы «Стрижа»: {fA}, {fB}, {fC}. Коробка на площади только в {back}, значит первый подходящий рейс в {fdep}. {fdep} + {fl2} минут = {tim}, Тим ещё ждёт.",
   "Парус улетает в {fdep} и будет у Тима в {tim}, за {before|минуту|минуты|минут} до того, как он перестанет ждать. Обе коробки нашли своих хозяев.", "Поднять флюгер",
   ["Выпиши рейсы «Стрижа»: первый в {f0}, дальше каждые {every} минут.", "Коробка попадёт только на рейс, который вылетает после {back}.", "Прибавь длительность полёта ко времени вылета."], 2)
 ]}
L['pl'] = {
 "title": "Paczka dla Wyspy Chmur",
 "intro": "Na Wyspie Chmur na święto składają wiatrowskaz w kształcie koguta. Majster otworzył pudełko: zamiast ogona w środku był mały żagiel. Listonoszka Nika jest pewna, że pomyliła dwa pudełka z taką samą chmurką na wieczku. Na poczcie są cztery nieodebrane przesyłki, wszystkie z rozmokłymi etykietami. Święto jest o 12:10, „Jaskółka” lata na wyspę raz dziennie. Trzeba znaleźć ogon, dostarczyć go do majstra i zdążyć na święto. A potem jeszcze oddać żagiel temu, kto na niego czeka.",
 "ending": "Ogon znalazł się w trzecim pudełku: dwa pudełka ważyły tyle samo i pomogła długość. „Jaskółka” doleciała w {fl} minut z postojem, kurier B przywiózł ogon o {ab}, a majster ustawił wiatrowskaz na 12:10. Żagiel odleciał „Jerzykiem” o {fdep} i był u szkutnika Tima o {tim}. Nika nie podpisuje już pudełek samym rysunkiem: teraz na każdym jest adres i masa.",
 "question": "Dwa pudełka ważyły dokładnie {totkg} kg. Dlaczego sama masa nie powiedziała, w którym jest ogon?",
 "steps": [
  step("Które pudełko jest nasze?", "Na poczcie Nika kładzie na wadze wszystkie cztery przesyłki i wyjmuje list przewozowy majstra. Cudzych paczek nie wolno otwierać, więc trzeba wybrać według listu, a otworzyć tylko jedną.",
   ["List przewozowy majstra: ogon o długości {tl} cm, masa {tkg} kg {tg} g. Zapakowany w pudełko o masie {bm} g, w środku jeszcze {pm} g papieru.", "Przesyłka nr 1: {p1} kg, pudełko o długości {p1len} cm.", "Przesyłka nr 2: {totkg} kg, pudełko o długości {p2len} cm.", "Przesyłka nr 3: {totkg} kg, pudełko o długości {p3len} cm.", "Przesyłka nr 4: {p4kg} kg {p4g} g, pudełko o długości {p4len} cm."],
   "Którą przesyłkę otworzyć?", "choice", ["Przesyłka nr 1", "Przesyłka nr 2", "Przesyłka nr 3", "Przesyłka nr 4"],
   ["{p1} kg to {p1g} g: ogon i pudełko bez papieru. Ale papier też jest w środku.", "Masa się zgadza, ale ogon o długości {tl} cm nie zmieści się w pudełku o długości {p2len} cm.", "", "{p4kg} kg {p4g} g jest o {pm} g cięższe niż potrzebna masa."],
   "{tm} + {bm} + {pm} = {tot} g, czyli {totkg} kg. Tyle ważą nr 2 i nr 3, ale ogon o długości {tl} cm zmieści się tylko w pudełku o długości {p3len} cm. Nika otwiera nr 3: w środku jest ogon koguta.",
   "Ogon znalazł się w przesyłce nr 3. Teraz trzeba wysłać go na wyspę „Jaskółką” i policzyć, ile czasu zostanie.", "Do przystani „Jaskółki”",
   ["Zamień wszystko na gramy i dodaj ogon, pudełko i papier.", "Dwa pudełka mogą mieć tę samą masę. Wtedy patrz na rozmiar.", "Ogona o długości {tl} cm nie da się zgiąć: pudełko musi być dłuższe."], 0),
  step("Kiedy pudełko będzie na wyspie?", "Na przystani Nika oddaje pudełko na „Jaskółkę”. Kapitan pokazuje trasę: do wyspy z jednym postojem na Wietrznej Wieży. Policz, kiedy pudełko zostanie wydane kurierowi.",
   ["„Jaskółka” wylatuje o {dep} i leci z prędkością {spd} km/h.", "Do wyspy jest {dist} km. Po drodze jeden postój na Wietrznej Wieży, {stop} minut.", "Po przylocie rozładunek zajmuje {unl} minut, potem pudełko wydaje się kurierowi."],
   "O której pudełko zostanie wydane kurierowi na wyspie? Wpisz czas GG:MM.", "time", [], [],
   "{dist} km przy prędkości {spd} km/h to {frac} godziny, czyli {fl} minut. Postój {stop} minut i rozładunek {unl} minut. {dep} + {fl} + {stop} + {unl} minut = {arr}.",
   "Pudełko zostanie wydane o {arr}. Do święta o 12:10 zostaje {left} minut i trzeba je podzielić między drogę kuriera i pracę majstra.", "Wybierz kuriera",
   ["Najpierw ustal, ile minut zajmie sam lot: w godzinę {spd} km, więc jaką część godziny zajmie {dist} km?", "{dist} z {spd} to {fi#dwie trzecie|trzy czwarte|połowa|jedna trzecia}. Zamień {fi#dwie trzecie|trzy czwarte|połowę|jedną trzecią} godziny na minuty.", "Do lotu dodaj postój i rozładunek, a potem wszystko do {dep}."], 1),
  step("Kto dowiezie ogon?", "Na placu wyspy jest czterech kurierów, każdy ma swój kurs według rozkładu: godziny odjazdu nie można zmienić. Nika zapisała dla każdego, kiedy odjeżdża, jak długo jedzie i co bierze.",
   ["Pudełko wydają o {arr}. Święto jest o 12:10. Majster potrzebuje {mk} minut: zamontować ogon i sprawdzić wiatrowskaz.", "Kurier A: odjeżdża o {la}, jedzie 3 km z prędkością 12 km/h.", "Kurier B: odjeżdża o {lb}, jedzie {db} km z prędkością {sb} km/h.", "Kurier C: odjeżdża o {lc}, idzie z wózkiem {dc} km z prędkością {sc} km/h.", "Kurier D: odjeżdża o {ld}, jedzie {dd} km z prędkością {sd} km/h, ale bierze tylko pudełka o długości do {lim} cm."],
   "Kto dowiezie ogon tak, żeby majster zdążył na 12:10?", "choice", ["Kurier A", "Kurier B", "Kurier C", "Kurier D"],
   ["Kurier A odjeżdża o {la}, a pudełko wydadzą dopiero o {arr}.", "", "{dc} km przy {sc} km/h to {tc} minut: kurier C dojedzie o {ac} i majstrowi zabraknie {mk} minut.", "Czasowo kurier D zdąży, ale nasze pudełko ma {p3len} cm długości, a on bierze tylko do {lim} cm."],
   "Majster potrzebuje {mk} minut, więc ogon musi być u niego najpóźniej o {latest}. B: {db} km przy {sb} km/h to {tb} minut, dojedzie o {ab}. A odjeżdża przed wydaniem, C dojedzie o {ac}, D nie bierze takich pudełek.",
   "Nika umawia się z kurierem B: odbiera pudełko o {lb} i przywozi majstrowi o {ab}. Majster ma {havem} minut na pracę, która zajmuje {mk}.", "Złóż wiatrowskaz",
   ["Najpierw policz, do której ogon musi być u majstra.", "Czas drogi: odległość podziel przez prędkość. Przy {sb} km/h jeden kilometr zajmuje {kmmin} minut.", "Sprawdź u każdego trzy rzeczy: godzinę odjazdu, godzinę przyjazdu i czy pudełko pasuje."], 3),
  step("Co zrobić z żaglem?", "W ładowni „Jaskółki” majster montuje ogon: o {fin} wiatrowskaz jest gotowy, na 12:10 kogut jest na wieży. Została druga połowa pomyłki Niki: pudełko z żaglem, na które czeka szkutnik Tim na Małej Wyspie.",
   ["Kurier B przywiezie pudełko z żaglem z powrotem na plac na {back}.", "Tim czeka na żagiel na swojej przystani na Małej Wyspie do {tw}.", "„Jerzyk” lata na Małą Wyspę co {every} minut, pierwszy kurs o {f0}. Lot trwa {fl2} minut.", "Pudełko ładuje się tylko na kurs, który wylatuje po tym, jak przywieziono je na plac."],
   "O której najwcześniej żagiel będzie u Tima? Wpisz czas GG:MM.", "time", [], [],
   "Kursy „Jerzyka”: {fA}, {fB}, {fC}. Pudełko jest na placu dopiero o {back}, więc pierwszy pasujący kurs jest o {fdep}. {fdep} + {fl2} minut = {tim}, Tim jeszcze czeka.",
   "Żagiel odlatuje o {fdep} i będzie u Tima o {tim}, {before|minutę|minuty|minut} przed tym, jak przestanie czekać. Oba pudełka trafiły do właścicieli.", "Ustaw wiatrowskaz",
   ["Wypisz kursy „Jerzyka”: pierwszy o {f0}, dalej co {every} minut.", "Pudełko trafi tylko na kurs, który wylatuje po {back}.", "Dodaj czas lotu do godziny wylotu."], 2)
 ]}
L['en'] = {
 "title": "A Parcel for Cloud Island",
 "intro": "On Cloud Island, a rooster weather vane is being assembled for the festival. The maker opened the box: instead of the tail, there was a little sail inside. Nika the postwoman is sure she mixed up two boxes with the same cloud on the lid. There are four unclaimed parcels at the post office, all with soggy labels. The festival is at 12:10, and the Swallow flies to the island once a day. You need to find the tail, get it to the maker and make it in time for the festival. And then return the sail to whoever is waiting for it.",
 "ending": "The tail was in the third box: two boxes weighed the same, and it was the length that settled it. The Swallow flew there in {fl} minutes plus a stop, courier B brought the tail at {ab}, and the maker raised the vane by 12:10. The sail left on the Swift at {fdep} and reached Tim the boatman at {tim}. Nika no longer labels boxes with just a picture: now every one carries an address and a weight.",
 "question": "Two boxes weighed exactly {totkg} kg. Why did the weight alone not tell you which one held the tail?",
 "steps": [
  step("Which box is ours?", "At the post office, Nika puts all four parcels on the scales and takes out the maker’s packing note. Other people’s parcels must not be opened, so you have to choose by the note and open only one.",
   ["The maker’s note: the tail is {tl} cm long and weighs {tkg} kg {tg} g. It is packed in a box weighing {bm} g, with another {pm} g of paper inside.", "Parcel 1: {p1} kg, box {p1len} cm long.", "Parcel 2: {totkg} kg, box {p2len} cm long.", "Parcel 3: {totkg} kg, box {p3len} cm long.", "Parcel 4: {p4kg} kg {p4g} g, box {p4len} cm long."],
   "Which parcel should be opened?", "choice", ["Parcel 1", "Parcel 2", "Parcel 3", "Parcel 4"],
   ["{p1} kg is {p1g} g: the tail and box without the paper. But the paper is inside too.", "The weight matches, but a {tl} cm tail will not fit in a {p2len} cm box.", "", "{p4kg} kg {p4g} g is {pm} g heavier than the weight we need."],
   "{tm} + {bm} + {pm} = {tot} g, which is {totkg} kg. Parcels 2 and 3 both weigh that, but a {tl} cm tail only fits in the {p3len} cm box. Nika opens parcel 3: the rooster’s tail is inside.",
   "The tail is in parcel 3. Now it has to be sent to the island on the Swallow, and we need to work out how much time will be left.", "To the Swallow’s dock",
   ["Convert everything to grams and add the tail, the box and the paper.", "Two boxes can have the same weight. Then look at the size.", "A {tl} cm tail cannot be bent: the box has to be longer."], 0),
  step("When will the box reach the island?", "At the dock, Nika hands the box over to the Swallow. The captain shows the route: to the island with one stop at Windmill Tower. Work out when the box will be handed to a courier.",
   ["The Swallow departs at {dep} and flies at {spd} km/h.", "It is {dist} km to the island. There is one stop on the way at Windmill Tower, lasting {stop} minutes.", "After arrival, unloading takes {unl} minutes, and then the box is handed to a courier."],
   "What time will the box be handed to a courier on the island? Enter the time as HH:MM.", "time", [], [],
   "{dist} km at {spd} km/h is {frac} of an hour, which is {fl} minutes. A {stop}-minute stop and {unl} minutes of unloading. {dep} + {fl} + {stop} + {unl} minutes = {arr}.",
   "The box will be handed over at {arr}. There are {left} minutes until the festival at 12:10, to be shared between the courier’s journey and the maker’s work.", "Choose a courier",
   ["First work out how many minutes the flight itself takes: {spd} km in an hour, so what fraction of an hour does {dist} km take?", "{dist} out of {spd} is {fi#two thirds|three quarters|a half|one third}. Convert {fi#two thirds|three quarters|half|one third} of an hour into minutes.", "Add the stop and the unloading to the flight, then add it all to {dep}."], 1),
  step("Who will deliver the tail?", "In the island square there are four couriers, each with a scheduled run: departure times cannot be changed. Nika has noted for each one when they leave, how far they travel and what they carry.",
   ["The box is handed over at {arr}. The festival is at 12:10. The maker needs {mk} minutes to fit the tail and check the vane.", "Courier A: leaves at {la}, rides 3 km at 12 km/h.", "Courier B: leaves at {lb}, rides {db} km at {sb} km/h.", "Courier C: leaves at {lc}, walks {dc} km with a cart at {sc} km/h.", "Courier D: leaves at {ld}, rides {dd} km at {sd} km/h, but only takes boxes up to {lim} cm long."],
   "Who can deliver the tail so that the maker finishes by 12:10?", "choice", ["Courier A", "Courier B", "Courier C", "Courier D"],
   ["Courier A leaves at {la}, but the box is only handed over at {arr}.", "", "{dc} km at {sc} km/h is {tc} minutes: courier C arrives at {ac}, and the maker would not have {mk} minutes.", "Courier D is fine on time, but our box is {p3len} cm long and D only takes boxes up to {lim} cm."],
   "The maker needs {mk} minutes, so the tail must reach them by {latest} at the latest. B: {db} km at {sb} km/h is {tb} minutes, arriving at {ab}. A leaves before the handover, C arrives at {ac}, and D does not take boxes this size.",
   "Nika books courier B: the box is collected at {lb} and delivered to the maker at {ab}. The maker has {havem} minutes for a job that takes {mk}.", "Assemble the weather vane",
   ["First work out by what time the tail must reach the maker.", "Travel time: divide the distance by the speed. At {sb} km/h, one kilometre takes {kmmin} minutes.", "Check three things for each courier: departure time, arrival time and whether the box fits."], 3),
  step("What about the sail?", "In the Swallow’s hold, the maker fits the tail: the vane is ready at {fin}, and the rooster is on the tower by 12:10. The second half of Nika’s mistake remains: the box with the sail, which Tim the boatman is waiting for on Little Island.",
   ["Courier B will bring the box with the sail back to the square by {back}.", "Tim is waiting for the sail at his dock on Little Island until {tw}.", "The Swift flies to Little Island every {every} minutes, with the first flight at {f0}. The flight takes {fl2} minutes.", "A box is only loaded onto a flight that departs after the box has reached the square."],
   "What is the earliest time the sail can reach Tim? Enter the time as HH:MM.", "time", [], [],
   "The Swift’s flights: {fA}, {fB}, {fC}. The box is only in the square at {back}, so the first suitable flight is at {fdep}. {fdep} + {fl2} minutes = {tim}, and Tim is still waiting.",
   "The sail leaves at {fdep} and reaches Tim at {tim}, {before|minute|minutes} before he stops waiting. Both boxes have found their owners.", "Raise the weather vane",
   ["Write out the Swift’s flights: the first at {f0}, then every {every} minutes.", "The box can only go on a flight that departs after {back}.", "Add the flight time to the departure time."], 2)
 ]}
L['uk'] = {
 "title": "Посилка для Хмарного острова",
 "intro": "На Хмарному острові до свята збирають флюгер-півня. Майстер відкрив коробку: замість хвоста всередині маленьке вітрило. Листоноша Ніка впевнена, що переплутала дві коробки з однаковою хмаринкою на кришці. На пошті чотири незатребувані відправлення, у всіх розмокли ярлики. Свято о 12:10, «Ластівка» літає на острів раз на день. Треба знайти хвіст, доставити його майстрові і встигнути до свята. А потім ще повернути вітрило тому, хто на нього чекає.",
 "ending": "Хвіст знайшовся в третій коробці: дві коробки важили однаково, і розібратися допомогла довжина. «Ластівка» долетіла за {fl} хвилин із зупинкою, кур’єр Б привіз хвіст о {ab}, і майстер підняв флюгер до 12:10. Вітрило полетіло «Серпокрильцем» о {fdep} і було в човняра Тіма о {tim}. Ніка більше не підписує коробки лише малюнком: тепер на кожній адреса і маса.",
 "question": "Дві коробки важили рівно {totkg} кг. Чому маса сама по собі не сказала, у якій із них хвіст?",
 "steps": [
  step("Яка коробка наша?", "На пошті Ніка кладе на ваги всі чотири відправлення і дістає накладну майстра. Відкривати чужі посилки не можна, тому вибрати треба за накладною, а відкрити лише одну.",
   ["Накладна майстра: хвіст завдовжки {tl} см, маса {tkg} кг {tg} г. Запакований у коробку масою {bm} г, усередині ще {pm} г паперу.", "Відправлення №1: {p1} кг, коробка завдовжки {p1len} см.", "Відправлення №2: {totkg} кг, коробка завдовжки {p2len} см.", "Відправлення №3: {totkg} кг, коробка завдовжки {p3len} см.", "Відправлення №4: {p4kg} кг {p4g} г, коробка завдовжки {p4len} см."],
   "Яке відправлення відкрити?", "choice", ["Відправлення №1", "Відправлення №2", "Відправлення №3", "Відправлення №4"],
   ["{p1} кг це {p1g} г: хвіст і коробка без паперу. Але папір теж лежить усередині.", "Маса збігається, але хвіст завдовжки {tl} см не поміститься в коробку завдовжки {p2len} см.", "", "{p4kg} кг {p4g} г важче за потрібну масу на {pm} г."],
   "{tm} + {bm} + {pm} = {tot} г, тобто {totkg} кг. Стільки важать №2 і №3, але хвіст завдовжки {tl} см поміститься лише в коробку завдовжки {p3len} см. Ніка відкриває №3: усередині хвіст півня.",
   "Хвіст знайдено у відправленні №3. Тепер його треба відправити на острів «Ластівкою» і зрозуміти, скільки часу залишиться.", "До причалу «Ластівки»",
   ["Переведи все в грами і додай хвіст, коробку і папір.", "Однакову масу можуть мати дві коробки. Тоді дивися на розмір.", "Хвіст завдовжки {tl} см не зігнеш: коробка має бути довшою."], 0),
  step("Коли коробка буде на острові?", "На причалі Ніка здає коробку на «Ластівку». Капітан показує маршрут: до острова з однією зупинкою на Вітряній вежі. Порахуй, коли коробку видадуть кур’єрові.",
   ["«Ластівка» вилітає о {dep} і летить зі швидкістю {spd} км/год.", "До острова {dist} км. Дорогою одна зупинка на Вітряній вежі, {stop} хвилин.", "Після прибуття розвантаження займає {unl} хвилин, потім коробку видають кур’єрові."],
   "О котрій коробку видадуть кур’єрові на острові? Введи час ГГ:ХХ.", "time", [], [],
   "{dist} км зі швидкістю {spd} км/год це {frac} години, тобто {fl} хвилин. Зупинка {stop} хвилин і розвантаження {unl} хвилин. {dep} + {fl} + {stop} + {unl} хвилин = {arr}.",
   "Коробку видадуть о {arr}. До свята о 12:10 залишається {left} хвилин, і їх треба розділити між дорогою кур’єра і роботою майстра.", "Вибрати кур’єра",
   ["Спершу дізнайся, скільки хвилин займе сам політ: за годину {spd} км, отже яку частину години займуть {dist} км?", "{dist} із {spd} це {fi#дві третини|три чверті|половина|одна третина}. Переведи {fi#дві третини|три чверті|половину|одну третину} години у хвилини.", "До польоту додай зупинку і розвантаження, а потім усе до {dep}."], 1),
  step("Хто довезе хвіст?", "На площі острова чотири кур’єри, у кожного свій рейс за розкладом: час виїзду змінити не можна. Ніка записала для кожного, коли він виїжджає, скільки їхати і що він бере.",
   ["Коробку видають о {arr}. Свято о 12:10. Майстрові потрібно {mk} хвилин: установити хвіст і перевірити флюгер.", "Кур’єр А: виїжджає о {la}, їде 3 км зі швидкістю 12 км/год.", "Кур’єр Б: виїжджає о {lb}, їде {db} км зі швидкістю {sb} км/год.", "Кур’єр В: виїжджає о {lc}, іде з візком {dc} км зі швидкістю {sc} км/год.", "Кур’єр Г: виїжджає о {ld}, їде {dd} км зі швидкістю {sd} км/год, але бере лише коробки завдовжки до {lim} см."],
   "Хто довезе хвіст так, щоб майстер устиг до 12:10?", "choice", ["Кур’єр А", "Кур’єр Б", "Кур’єр В", "Кур’єр Г"],
   ["Кур’єр А виїжджає о {la}, а коробку видадуть лише о {arr}.", "", "{dc} км при {sc} км/год це {tc} хвилин: кур’єр В приїде о {ac}, і майстрові не вистачить {mk} хвилин.", "За часом кур’єр Г встигає, але наша коробка завдовжки {p3len} см, а він бере лише до {lim} см."],
   "Майстрові потрібно {mk} хвилин, отже хвіст має бути в нього не пізніше ніж о {latest}. Б: {db} км при {sb} км/год це {tb} хвилин, приїде о {ab}. А їде до видачі, В приїде о {ac}, Г не бере таких коробок.",
   "Ніка домовляється з кур’єром Б: він забирає коробку о {lb} і привозить майстрові о {ab}. У майстра {havem} хвилин на роботу, яка займає {mk}.", "Зібрати флюгер",
   ["Спершу порахуй, до котрої години хвіст має бути в майстра.", "Час дороги: відстань поділи на швидкість. При {sb} км/год один кілометр займає {kmmin} хвилин.", "Перевір у кожного три речі: час виїзду, час прибуття і чи підходить коробка."], 3),
  step("Куди подіти вітрило?", "У трюмі «Ластівки» майстер установлює хвіст: о {fin} флюгер готовий, до 12:10 півень на вежі. Залишилася друга половина помилки Ніки: коробка з вітрилом, на яку чекає човняр Тім на Малому острові.",
   ["Кур’єр Б привезе коробку з вітрилом назад на площу до {back}.", "Тім чекає на вітрило на своєму причалі на Малому острові до {tw}.", "«Серпокрилець» літає на Малий острів кожні {every} хвилин, перший рейс о {f0}. Політ триває {fl2} хвилин.", "Коробку вантажать лише на рейс, який вилітає після того, як її привезли на площу."],
   "О котрій найраніше вітрило буде в Тіма? Введи час ГГ:ХХ.", "time", [], [],
   "Рейси «Серпокрильця»: {fA}, {fB}, {fC}. Коробка на площі лише о {back}, отже перший підхожий рейс о {fdep}. {fdep} + {fl2} хвилин = {tim}, Тім ще чекає.",
   "Вітрило відлітає о {fdep} і буде в Тіма о {tim}, за {before|хвилину|хвилини|хвилин} до того, як він перестане чекати. Обидві коробки знайшли своїх господарів.", "Підняти флюгер",
   ["Випиши рейси «Серпокрильця»: перший о {f0}, далі кожні {every} хвилин.", "Коробка потрапить лише на рейс, який вилітає після {back}.", "Додай тривалість польоту до часу вильоту."], 2)
 ]}
if __name__ == '__main__':
    write_case('cloud', '003', L, variants())
