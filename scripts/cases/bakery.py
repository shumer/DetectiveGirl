from common import step, write_case, add, T
def variants():
    out = []
    data = [
        dict(tr=4, tp=12, br=6, bp=7, bk=2, tn=3, te=2, dg=200, pm=30, now='14:40', cut=5, ob='14:50', bake=15, cool=10, cr='15:10', wait=10),
        dict(tr=5, tp=10, br=7, bp=6, bk=3, tn=3, te=2, dg=330, pm=40, now='15:00', cut=6, ob='15:12', bake=18, cool=8, cr='15:30', wait=10),
        dict(tr=3, tp=15, br=5, bp=8, bk=2, tn=2, te=2, dg=170, pm=30, now='13:50', cut=4, ob='14:05', bake=12, cool=12, cr='14:25', wait=5),
        dict(tr=4, tp=14, br=8, bp=6, bk=2, tn=3, te=3, dg=280, pm=30, now='16:10', cut=5, ob='16:18', bake=20, cool=10, cr='16:40', wait=10),
    ]
    for d in data:
        baked = d['tr'] * d['tp']; inbox = d['br'] * d['bp']; missing = baked - inbox - d['bk']; assert missing > 0
        samples = d['tn'] * d['te']; assert samples != missing; fake = baked - missing
        cnt = d['dg'] // d['pm']; rest = d['dg'] % d['pm']; assert cnt >= missing and rest > 0; spare = cnt - missing
        cutdone = add(d['now'], d['cut']); assert T(cutdone) < T(d['ob'])
        bakedt = add(d['ob'], d['bake']); ready = add(bakedt, d['cool']); crmax = add(d['cr'], d['wait']); assert T(d['cr']) <= T(ready) <= T(crmax)
        naive = add(d['now'], d['cut'] + d['bake'] + d['cool']); assert naive != ready
        v = dict(tr=d['tr'], tp=d['tp'], baked=baked, br=d['br'], bp=d['bp'], inbox=inbox, bk=d['bk'], missing=missing, tn=d['tn'], te=d['te'], samples=samples, fake=fake,
                 dg=d['dg'], pm=d['pm'], cnt=cnt, rest=rest, spare=spare, now=d['now'], cut=d['cut'], cutdone=cutdone, ob=d['ob'], bake=d['bake'], bakedt=bakedt, cool=d['cool'], ready=ready, cr=d['cr'], wait=d['wait'], crmax=crmax)
        out.append({'values': v, 'answers': [str(missing), 2, str(cnt), ready]})
    return out
L = {}
L['ru'] = {
 "title": "Пекарня лунных пряников",
 "intro": "Для ярмарки заказали {baked} пряников в форме луны. Коробка стоит на прилавке, но в ней заметно пустое место, а сама пекарь Вера была весь день у печи и ничего не заметила. Утром в пекарне были дегустаторы, курьер Петя и помощница Маша. Помоги выяснить, сколько лун не хватает, куда они делись, хватит ли теста и когда коробку можно отдавать.",
 "ending": "Не хватало {missing|луны|лун|лун}: {baked} испекли, {inbox} в коробке, {bk|разбитая|разбитые|разбитых} лежали отдельно. Дегустаторы получили звёзды, а {missing|луну|луны|лун} увёз на стенд ярмарки курьер Петя по накладной, которую Вера не прочитала. Из {dg} г теста вышло {cnt|луна|луны|лун}: {missing} в коробку и {spare} про запас. Печь была занята звёздами до {ob}, поэтому луны остыли к {ready}, и курьер их дождался.",
 "question": "Дегустаторы получили ровно {samples|пряник|пряника|пряников}, а не хватало {missing}. Почему сразу было видно, что дело не в них?",
 "steps": [
  step("Сколько лун не хватает?", "У прилавка Вера показывает два снимка: полные противни перед упаковкой и открытую коробку. Рядом с коробкой тарелка с разбитыми лунами: их отложили, потому что на ярмарку такие не годятся.",
   ["Испекли {tr} полных противня по {tp} лун.", "В коробке {br} полных рядов по {bp} лун.", "{bk|разбитая луна лежит|разбитые луны лежат|разбитых лун лежат} отдельно на тарелке и в коробку не попали."],
   "Сколько лун не хватает, не считая разбитых? Введи число.", "number", [], [],
   "Испекли {tr} × {tp} = {baked}. В коробке {br} × {bp} = {inbox}. Разбитые не пропали, они на тарелке: {baked} - {inbox} - {bk} = {missing|луна|луны|лун} неизвестно где.",
   "{missing|луна исчезла|луны исчезли|лун исчезли} между противнем и коробкой. Вера открывает журнал утра: дегустация, курьер, помощница.", "Проверить журнал утра",
   ["Посчитай испечённые и посчитай в коробке.", "Разбитые не пропали, они лежат отдельно.", "Вычти из испечённых и коробку, и разбитые."], 0),
  step("Куда делись луны?", "В журнале записано всё, что выносили из пекарни утром, а к записям есть фотографии. Проверь каждую версию и по числу, и по форме пряников.",
   ["09:20: {tn} дегустатора получили по {te} пряника. На фото дегустации {samples|звезда|звезды|звёзд}.", "09:40: Вера отложила {bk|разбитую луну|разбитые луны|разбитых лун} на тарелку.", "09:50: курьер Петя взял пакет по накладной «{missing} шт., образцы для стенда ярмарки». На фото стенда {missing|луна|луны|лун}.", "Помощница Маша приходила в 10:00, но только за фартуком, и к пряникам не подходила.", "Фото противней сделано в 09:10: на них {baked} лун."],
   "Где недостающие луны?", "choice", ["Их съели дегустаторы", "Их не было: испекли только {fake|луну|луны|лун}", "Их увёз Петя на стенд ярмарки по накладной", "Это и есть разбитые луны"],
   ["Дегустаторы получили {samples|пряник|пряника|пряников}, а не {missing}, и на фото у них звёзды.", "На фото противней в 09:10 ровно {baked} лун.", "", "Разбитых {bk}, а не хватает {missing}. К тому же разбитые лежат на тарелке, они никуда не делись."],
   "У дегустаторов {samples|звезда|звезды|звёзд}: не то число и не та форма. Противни полные. Разбитых только {bk}. А накладная Пети говорит ровно о {missing} образцах, и на фото стенда {missing|луна|луны|лун}. Луны не пропали, они на ярмарке.",
   "Вера вспоминает: она подписала накладную не глядя. Стенду луны нужны, значит для коробки надо допечь {missing}. Идём проверять тесто.", "Проверить оставшееся тесто",
   ["У каждой версии проверь число пряников и форму на фотографии.", "Разбитые луны никуда не делись, их {bk}.", "Сравни число в накладной Пети с недостачей."], 1),
  step("Хватит ли теста?", "На столе Вера взвешивает оставшееся тесто. Для коробки нужно {missing|луна|луны|лун}, но она хочет ещё несколько про запас, если тесто позволит.",
   ["Осталось {dg} г теста.", "На одну луну уходит {pm} г теста.", "Из остатка теста, которого не хватает на целую луну, луну не делают."],
   "Сколько всего лун можно вырезать из оставшегося теста? Введи число.", "number", [], [],
   "{dg} : {pm} = {cnt} и {rest} г в остатке. {cnt|луна|луны|лун}: {missing} в коробку и {spare} про запас, {rest} г теста останется.",
   "Теста хватает на {cnt|луну|луны|лун}: {missing} для коробки и {spare} запасные. Осталось узнать, когда луны будут готовы: печь сейчас занята.", "Рассчитать время выдачи",
   ["Раздели запас теста на расход одной луны.", "Остаток, которого не хватает на целую луну, не считается.", "Лун получится целое число."], 2),
  step("Когда забирать заказ?", "У печи Вера смотрит на часы. В печи сейчас звёзды для другого заказа, и достать их раньше нельзя. Курьер ярмарки уже в пути.",
   ["Сейчас {now}. Вера начинает вырезать луны прямо сейчас, это занимает {cut|минуту|минуты|минут}.", "Печь занята звёздами до {ob}. Луны можно поставить в печь только после этого.", "Выпечка лун занимает {bake|минуту|минуты|минут}, потом они остывают {cool|минуту|минуты|минут}. Курьеру отдают только остывшие.", "Курьер приедет в {cr} и может подождать не больше {wait|минуты|минут|минут}."],
   "Во сколько луны будут готовы к выдаче? Введи время ЧЧ:ММ.", "time", [], [],
   "Вырезание закончится в {cutdone}, но печь освободится только в {ob}. Выпечка до {bakedt}, остывание до {ready}. Курьер ждёт до {crmax}, значит успеваем.",
   "Луны готовы в {ready}, курьер их дождётся. Коробка снова полная, а Вера с этого дня читает накладные перед подписью.", "Передать заказ на ярмарку",
   ["Вырезать можно, пока печь занята звёздами.", "Печь освободится только в {ob}, раньше выпечка не начнётся.", "После выпечки ещё остывание."], 3)
 ]}
L['pl'] = {
 "title": "Piekarnia księżycowych pierników",
 "intro": "Na jarmark zamówiono {baked} pierników w kształcie księżyca. Pudełko stoi na ladzie, ale widać w nim puste miejsce, a piekarka Wiera cały dzień była przy piecu i niczego nie zauważyła. Rano w piekarni byli degustatorzy, kurier Petia i pomocnica Masza. Pomóż ustalić, ilu księżyców brakuje, gdzie się podziały, czy wystarczy ciasta i kiedy pudełko można wydać.",
 "ending": "Brakowało {missing|księżyca|księżyców|księżyców}: {baked} upieczono, {inbox} jest w pudełku, {bk|połamany leżał|połamane leżały|połamanych leżało} osobno. Degustatorzy dostali gwiazdki, a {missing|księżyc|księżyce|księżyców} zawiózł na stoisko jarmarku kurier Petia według listu przewozowego, którego Wiera nie przeczytała. Z {dg} g ciasta wyszło {cnt|księżyc|księżyce|księżyców}: {missing} do pudełka i {spare} na zapas. Piec był zajęty gwiazdkami do {ob}, więc księżyce ostygły na {ready} i kurier na nie zaczekał.",
 "question": "Degustatorzy dostali dokładnie {samples|piernik|pierniki|pierników}, a brakowało {missing}. Dlaczego od razu było widać, że to nie oni?",
 "steps": [
  step("Ilu księżyców brakuje?", "Przy ladzie Wiera pokazuje dwa zdjęcia: pełne blachy przed pakowaniem i otwarte pudełko. Obok pudełka stoi talerz z połamanymi księżycami: odłożono je, bo takie na jarmark się nie nadają.",
   ["Upieczono {tr} pełne blachy po {tp} księżyców.", "W pudełku jest {br} pełnych rzędów po {bp} księżyców.", "{bk|połamany księżyc leży|połamane księżyce leżą|połamanych księżyców leży} osobno na talerzu i do pudełka nie trafiły."],
   "Ilu księżyców brakuje, nie licząc połamanych? Wpisz liczbę.", "number", [], [],
   "Upieczono {tr} × {tp} = {baked}. W pudełku {br} × {bp} = {inbox}. Połamane nie zniknęły, są na talerzu: {baked} - {inbox} - {bk} = {missing|księżyc|księżyce|księżyców} nie wiadomo gdzie.",
   "{missing|księżyc zniknął|księżyce zniknęły|księżyców zniknęło} między blachą a pudełkiem. Wiera otwiera dziennik poranka: degustacja, kurier, pomocnica.", "Sprawdź dziennik poranka",
   ["Policz upieczone i policz te w pudełku.", "Połamane nie zniknęły, leżą osobno.", "Od upieczonych odejmij i pudełko, i połamane."], 0),
  step("Gdzie się podziały księżyce?", "W dzienniku zapisano wszystko, co rano wynoszono z piekarni, a do zapisów są zdjęcia. Sprawdź każdą wersję i pod względem liczby, i kształtu pierników.",
   ["09:20: {tn} degustatorów dostało po {te} pierniki. Na zdjęciu z degustacji {samples|gwiazdka|gwiazdki|gwiazdek}.", "09:40: Wiera odłożyła {bk|połamany księżyc|połamane księżyce|połamanych księżyców} na talerz.", "09:50: kurier Petia wziął paczkę według listu przewozowego „{missing} szt., próbki na stoisko jarmarku”. Na zdjęciu stoiska {missing|księżyc|księżyce|księżyców}.", "Pomocnica Masza przyszła o 10:00, ale tylko po fartuch, i do pierników nie podchodziła.", "Zdjęcie blach zrobiono o 09:10: jest na nich {baked} księżyców."],
   "Gdzie są brakujące księżyce?", "choice", ["Zjedli je degustatorzy", "Nie było ich: upieczono tylko {fake|księżyc|księżyce|księżyców}", "Zawiózł je Petia na stoisko jarmarku według listu przewozowego", "To właśnie te połamane księżyce"],
   ["Degustatorzy dostali {samples|piernik|pierniki|pierników}, a nie {missing}, i na zdjęciu mają gwiazdki.", "Na zdjęciu blach o 09:10 jest dokładnie {baked} księżyców.", "", "Połamanych jest {bk}, a brakuje {missing}. Poza tym połamane leżą na talerzu, nigdzie nie zniknęły."],
   "Degustatorzy mają {samples|gwiazdkę|gwiazdki|gwiazdek}: nie ta liczba i nie ten kształt. Blachy są pełne. Połamanych jest tylko {bk}. A list przewozowy Petii mówi dokładnie o {missing} próbkach i na zdjęciu stoiska jest {missing|księżyc|księżyce|księżyców}. Księżyce nie zniknęły, są na jarmarku.",
   "Wiera przypomina sobie: podpisała list przewozowy bez czytania. Stoisko potrzebuje księżyców, więc do pudełka trzeba dopiec {missing}. Idziemy sprawdzić ciasto.", "Sprawdź pozostałe ciasto",
   ["Przy każdej wersji sprawdź liczbę pierników i kształt na zdjęciu.", "Połamane księżyce nigdzie nie zniknęły, jest ich {bk}.", "Porównaj liczbę z listu przewozowego Petii z brakiem."], 1),
  step("Czy wystarczy ciasta?", "Na stole Wiera waży pozostałe ciasto. Do pudełka potrzeba {missing|księżyca|księżyców|księżyców}, ale chce jeszcze kilka na zapas, jeśli ciasto pozwoli.",
   ["Zostało {dg} g ciasta.", "Na jeden księżyc idzie {pm} g ciasta.", "Z resztki ciasta, której nie starcza na cały księżyc, księżyca się nie robi."],
   "Ile księżyców łącznie można wyciąć z pozostałego ciasta? Wpisz liczbę.", "number", [], [],
   "{dg} : {pm} = {cnt} i {rest} g reszty. {cnt|księżyc|księżyce|księżyców}: {missing} do pudełka i {spare} na zapas, zostanie {rest} g ciasta.",
   "Ciasta starcza na {cnt|księżyc|księżyce|księżyców}: {missing} do pudełka i {spare} zapasowe. Zostało ustalić, kiedy księżyce będą gotowe: piec jest teraz zajęty.", "Oblicz czas wydania",
   ["Podziel zapas ciasta przez zużycie na jeden księżyc.", "Reszta, której nie starcza na cały księżyc, się nie liczy.", "Księżyców wyjdzie liczba całkowita."], 2),
  step("Kiedy odebrać zamówienie?", "Przy piecu Wiera patrzy na zegar. W piecu są teraz gwiazdki do innego zamówienia i nie można ich wyjąć wcześniej. Kurier z jarmarku jest już w drodze.",
   ["Jest {now}. Wiera zaczyna wycinać księżyce od razu, zajmuje to {cut|minutę|minuty|minut}.", "Piec jest zajęty gwiazdkami do {ob}. Księżyce można włożyć do pieca dopiero potem.", "Pieczenie księżyców trwa {bake|minutę|minuty|minut}, potem stygną {cool|minutę|minuty|minut}. Kurierowi wydaje się tylko ostygnięte.", "Kurier przyjedzie o {cr} i może zaczekać najwyżej {wait|minutę|minuty|minut}."],
   "O której księżyce będą gotowe do wydania? Wpisz czas GG:MM.", "time", [], [],
   "Wycinanie skończy się o {cutdone}, ale piec zwolni się dopiero o {ob}. Pieczenie do {bakedt}, stygnięcie do {ready}. Kurier czeka do {crmax}, więc zdążymy.",
   "Księżyce są gotowe o {ready}, kurier na nie zaczeka. Pudełko znów jest pełne, a Wiera od tego dnia czyta listy przewozowe przed podpisem.", "Przekaż zamówienie na jarmark",
   ["Wycinać można, kiedy piec jest zajęty gwiazdkami.", "Piec zwolni się dopiero o {ob}, wcześniej pieczenie się nie zacznie.", "Po pieczeniu jest jeszcze stygnięcie."], 3)
 ]}
L['en'] = {
 "title": "The Moon Cookie Bakery",
 "intro": "{baked} moon-shaped cookies were ordered for the fair. The box is on the counter, but there is a visible empty space in it, and Vera the baker was at the oven all day and noticed nothing. In the morning the bakery was visited by tasters, Petya the courier and Masha the helper. Help work out how many moons are missing, where they went, whether there is enough dough, and when the box can be handed over.",
 "ending": "{missing} moons were missing: {baked} were baked, {inbox} are in the box, and {bk} broken ones lay separately. The tasters got stars, and {missing} moons were taken to the fair stand by Petya the courier under a delivery note Vera had not read. The {dg} g of dough gave {cnt} moons: {missing} for the box and {spare} spare. The oven was busy with stars until {ob}, so the moons had cooled by {ready}, and the courier waited for them.",
 "question": "The tasters received exactly {samples} cookies, and {missing} were missing. Why was it immediately clear that they were not the cause?",
 "steps": [
  step("How many moons are missing?", "At the counter, Vera shows two photos: full trays before packing and the open box. Beside the box is a plate with broken moons: they were set aside because broken ones are no good for the fair.",
   ["{tr} full trays of {tp} moons each were baked.", "The box holds {br} full rows of {bp} moons.", "{bk} broken moons lie separately on a plate and did not go into the box."],
   "How many moons are missing, not counting the broken ones? Enter a number.", "number", [], [],
   "Baked: {tr} × {tp} = {baked}. In the box: {br} × {bp} = {inbox}. The broken ones did not vanish, they are on the plate: {baked} - {inbox} - {bk} = {missing} moons are unaccounted for.",
   "{missing} moons disappeared between the tray and the box. Vera opens the morning log: the tasting, the courier, the helper.", "Check the morning log",
   ["Count the baked ones and count the ones in the box.", "The broken ones did not vanish; they lie separately.", "Subtract both the box and the broken ones from the baked ones."], 0),
  step("Where did the moons go?", "The log records everything that left the bakery this morning, and there are photos to go with the entries. Check each theory by both the number and the shape of the cookies.",
   ["09:20: {tn} tasters received {te} cookies each. The tasting photo shows {samples} stars.", "09:40: Vera set {bk} broken moons aside on a plate.", "09:50: Petya the courier took a bag under a delivery note reading “{missing} pcs, samples for the fair stand”. The stand photo shows {missing} moons.", "Masha the helper came in at 10:00, but only for her apron, and did not go near the cookies.", "The tray photo was taken at 09:10: it shows {baked} moons."],
   "Where are the missing moons?", "choice", ["The tasters ate them", "They never existed: only {fake} moons were baked", "Petya took them to the fair stand under the delivery note", "They are the broken moons"],
   ["The tasters received {samples} cookies, not {missing}, and in the photo they have stars.", "The tray photo at 09:10 shows exactly {baked} moons.", "", "There are {bk} broken ones, and {missing} are missing. Besides, the broken ones are on the plate; they went nowhere."],
   "The tasters have {samples} stars: wrong number and wrong shape. The trays were full. Only {bk} are broken. But Petya’s delivery note says exactly {missing} samples, and the stand photo shows {missing} moons. The moons did not vanish; they are at the fair.",
   "Vera remembers: she signed the delivery note without looking. The stand needs its moons, so {missing} more must be baked for the box. Let’s check the dough.", "Check the remaining dough",
   ["For each theory check the number of cookies and the shape in the photo.", "The broken moons went nowhere, and there are {bk} of them.", "Compare the number on Petya’s delivery note with the shortfall."], 1),
  step("Is there enough dough?", "At the table, Vera weighs the remaining dough. The box needs {missing} moons, but she wants a few spare ones too, if the dough allows.",
   ["{dg} g of dough is left.", "One moon takes {pm} g of dough.", "No moon is made from a leftover that is not enough for a whole one."],
   "How many moons in total can be cut from the remaining dough? Enter a number.", "number", [], [],
   "{dg} ÷ {pm} = {cnt} with {rest} g left over. {cnt} moons: {missing} for the box and {spare} spare, with {rest} g of dough remaining.",
   "There is enough dough for {cnt} moons: {missing} for the box and {spare} spare. Now we need to know when the moons will be ready: the oven is busy right now.", "Work out the handover time",
   ["Divide the dough supply by the amount for one moon.", "A leftover that is not enough for a whole moon does not count.", "The number of moons will be a whole number."], 2),
  step("When can the order be collected?", "At the oven, Vera looks at the clock. The oven currently holds stars for another order, and they cannot come out early. The fair’s courier is already on the way.",
   ["It is {now} now. Vera starts cutting the moons right away; it takes {cut} minutes.", "The oven is busy with stars until {ob}. The moons can go in only after that.", "Baking the moons takes {bake} minutes, then they cool for {cool} minutes. Only cooled moons are handed to the courier.", "The courier arrives at {cr} and can wait no more than {wait} minutes."],
   "What time will the moons be ready to hand over? Enter the time as HH:MM.", "time", [], [],
   "Cutting finishes at {cutdone}, but the oven is free only at {ob}. Baking until {bakedt}, cooling until {ready}. The courier waits until {crmax}, so we make it.",
   "The moons are ready at {ready}, and the courier waits for them. The box is full again, and from today Vera reads delivery notes before signing.", "Send the order to the fair",
   ["Cutting can be done while the oven is busy with stars.", "The oven is free only at {ob}; baking cannot start before that.", "After baking there is still the cooling."], 3)
 ]}
L['uk'] = {
 "title": "Пекарня місячних пряників",
 "intro": "Для ярмарку замовили {baked} пряників у формі місяця. Коробка стоїть на прилавку, але в ній помітне порожнє місце, а сама пекарка Віра була весь день біля печі й нічого не помітила. Уранці в пекарні були дегустатори, кур’єр Петя і помічниця Маша. Допоможи з’ясувати, скількох місяців бракує, куди вони поділися, чи вистачить тіста і коли коробку можна віддавати.",
 "ending": "Бракувало {missing|місяця|місяців|місяців}: {baked} спекли, {inbox} в коробці, {bk|розбитий лежав|розбиті лежали|розбитих лежали} окремо. Дегустатори отримали зірки, а {missing|місяць|місяці|місяців} відвіз на стенд ярмарку кур’єр Петя за накладною, якої Віра не прочитала. Із {dg} г тіста вийшло {cnt|місяць|місяці|місяців}: {missing} в коробку і {spare} про запас. Піч була зайнята зірками до {ob}, тому місяці охололи до {ready}, і кур’єр їх дочекався.",
 "question": "Дегустатори отримали рівно {samples|пряник|пряники|пряників}, а бракувало {missing}. Чому одразу було видно, що річ не в них?",
 "steps": [
  step("Скількох місяців бракує?", "Біля прилавка Віра показує два знімки: повні дека перед пакуванням і відкриту коробку. Поруч із коробкою тарілка з розбитими місяцями: їх відклали, бо на ярмарок такі не годяться.",
   ["Спекли {tr} повні дека по {tp} місяців.", "У коробці {br} повних рядів по {bp} місяців.", "{bk|розбитий місяць лежить|розбиті місяці лежать|розбитих місяців лежать} окремо на тарілці й у коробку не потрапили."],
   "Скількох місяців бракує, не рахуючи розбитих? Введи число.", "number", [], [],
   "Спекли {tr} × {tp} = {baked}. У коробці {br} × {bp} = {inbox}. Розбиті не зникли, вони на тарілці: {baked} - {inbox} - {bk} = {missing|місяць|місяці|місяців} невідомо де.",
   "{missing|місяць зник|місяці зникли|місяців зникли} між деком і коробкою. Віра відкриває журнал ранку: дегустація, кур’єр, помічниця.", "Перевірити журнал ранку",
   ["Порахуй спечені й порахуй у коробці.", "Розбиті не зникли, вони лежать окремо.", "Відніми від спечених і коробку, і розбиті."], 0),
  step("Куди поділися місяці?", "У журналі записано все, що виносили з пекарні вранці, а до записів є фотографії. Перевір кожну версію і за кількістю, і за формою пряників.",
   ["09:20: {tn} дегустатори отримали по {te} пряники. На фото дегустації {samples|зірка|зірки|зірок}.", "09:40: Віра відклала {bk|розбитий місяць|розбиті місяці|розбитих місяців} на тарілку.", "09:50: кур’єр Петя взяв пакет за накладною «{missing} шт., зразки для стенда ярмарку». На фото стенда {missing|місяць|місяці|місяців}.", "Помічниця Маша приходила о 10:00, але лише по фартух, і до пряників не підходила.", "Фото дек зроблено о 09:10: на них {baked} місяців."],
   "Де місяці, яких бракує?", "choice", ["Їх з’їли дегустатори", "Їх не було: спекли лише {fake|місяць|місяці|місяців}", "Їх відвіз Петя на стенд ярмарку за накладною", "Це і є розбиті місяці"],
   ["Дегустатори отримали {samples|пряник|пряники|пряників}, а не {missing}, і на фото в них зірки.", "На фото дек о 09:10 рівно {baked} місяців.", "", "Розбитих {bk}, а бракує {missing}. До того ж розбиті лежать на тарілці, вони нікуди не поділися."],
   "У дегустаторів {samples|зірка|зірки|зірок}: не та кількість і не та форма. Дека повні. Розбитих лише {bk}. А накладна Петі говорить рівно про {missing} зразків, і на фото стенда {missing|місяць|місяці|місяців}. Місяці не зникли, вони на ярмарку.",
   "Віра згадує: вона підписала накладну не дивлячись. Стенду місяці потрібні, отже для коробки треба допекти {missing}. Ідемо перевіряти тісто.", "Перевірити тісто, що залишилося",
   ["У кожної версії перевір кількість пряників і форму на фотографії.", "Розбиті місяці нікуди не поділися, їх {bk}.", "Порівняй число в накладній Петі з нестачею."], 1),
  step("Чи вистачить тіста?", "На столі Віра зважує тісто, що залишилося. Для коробки потрібно {missing|місяць|місяці|місяців}, але вона хоче ще кілька про запас, якщо тісто дозволить.",
   ["Залишилося {dg} г тіста.", "На один місяць іде {pm} г тіста.", "Із залишку тіста, якого не вистачає на цілий місяць, місяця не роблять."],
   "Скільки всього місяців можна вирізати з тіста, що залишилося? Введи число.", "number", [], [],
   "{dg} : {pm} = {cnt} і {rest} г у залишку. {cnt|місяць|місяці|місяців}: {missing} в коробку і {spare} про запас, {rest} г тіста залишиться.",
   "Тіста вистачає на {cnt|місяць|місяці|місяців}: {missing} для коробки і {spare} запасні. Залишилося дізнатися, коли місяці будуть готові: піч зараз зайнята.", "Розрахувати час видачі",
   ["Поділи запас тіста на витрату одного місяця.", "Залишок, якого не вистачає на цілий місяць, не рахується.", "Місяців вийде ціле число."], 2),
  step("Коли забирати замовлення?", "Біля печі Віра дивиться на годинник. У печі зараз зірки для іншого замовлення, і дістати їх раніше не можна. Кур’єр ярмарку вже в дорозі.",
   ["Зараз {now}. Віра починає вирізати місяці просто зараз, це займає {cut|хвилину|хвилини|хвилин}.", "Піч зайнята зірками до {ob}. Місяці можна поставити в піч лише після цього.", "Випікання місяців займає {bake|хвилину|хвилини|хвилин}, потім вони охолоджуються {cool|хвилину|хвилини|хвилин}. Кур’єрові віддають лише охололі.", "Кур’єр приїде о {cr} і може почекати не більше ніж {wait|хвилину|хвилини|хвилин}."],
   "О котрій місяці будуть готові до видачі? Введи час ГГ:ХХ.", "time", [], [],
   "Вирізання закінчиться о {cutdone}, але піч звільниться лише о {ob}. Випікання до {bakedt}, охолодження до {ready}. Кур’єр чекає до {crmax}, отже встигаємо.",
   "Місяці готові о {ready}, кур’єр їх дочекається. Коробка знову повна, а Віра відтепер читає накладні перед підписом.", "Передати замовлення на ярмарок",
   ["Вирізати можна, поки піч зайнята зірками.", "Піч звільниться лише о {ob}, раніше випікання не почнеться.", "Після випікання ще охолодження."], 3)
 ]}
if __name__ == '__main__':
    write_case('bakery', '008', L, variants())
