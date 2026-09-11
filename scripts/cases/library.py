from common import step, write_case
def variants():
    out = []
    data = [
        dict(a=121, b=160, nth=19, ni=0, L=8, W=5, sp=2),
        dict(a=201, b=240, nth=24, ni=1, L=10, W=6, sp=2),
        dict(a=81, b=130, nth=33, ni=2, L=9, W=6, sp=2),
        dict(a=151, b=190, nth=12, ni=3, L=12, W=7, sp=2),
    ]
    for d in data:
        a, b = d['a'], d['b']; page = a + d['nth'] - 1; back = b - page; assert a < page < b and back > 0
        P = 2 * (d['L'] + d['W']); assert P % d['sp'] == 0; posts = P // d['sp']
        v = dict(a=a, b=b, a2=a + 1, aA=a - 40, bA=a - 1, aC=b + 1, bC=b + 40, bD=b + 4, nth=d['nth'], ni=d['ni'], nm1=d['nth'] - 1, page=page, back=back,
                 L=d['L'], W=d['W'], W1=d['W'] + 1, g=2, P=P, sp=d['sp'], posts=posts)
        out.append({'values': v, 'answers': [1, str(page), 1, str(posts)]})
    return out
ORD = {
 'ru': ("девятнадцатой|двадцать четвёртой|тридцать третьей|двенадцатой", "Девятнадцатая|Двадцать четвёртая|Тридцать третья|Двенадцатая"),
 'pl': ("dziewiętnastej|dwudziestej czwartej|trzydziestej trzeciej|dwunastej", "Dziewiętnasta|Dwudziesta czwarta|Trzydziesta trzecia|Dwunasta"),
 'en': ("nineteenth|twenty-fourth|thirty-third|twelfth", "The nineteenth|The twenty-fourth|The thirty-third|The twelfth"),
 'uk': ("дев’ятнадцятій|двадцять четвертій|тридцять третій|дванадцятій", "Дев’ятнадцята|Двадцять четверта|Тридцять третя|Дванадцята"),
}
L = {}
o, O = ORD['ru']
L['ru'] = {
 "title": "Две закладки и одна страница",
 "intro": "Книжный клуб собирается обсудить задачу про сад из сборника загадок. Две читательницы отмечали её закладками, но при ремонте книги закладки вынули, а угол страницы с рисунком повредился. Остались две заметки читательниц и папка с копиями рисунков. Помоги библиотекарю найти издание, страницу и верную копию, а потом решить задачу, ради которой всё затевалось.",
 "ending": "Издание Б единственное совпало по обеим границам раздела: {a} и {b}. Обе заметки указали на страницу {page}, хотя считали по-разному: одна с {ni#" + o + "} страницы раздела, другая на {back} назад от последней. Копия Б единственная совпала по всем четырём признакам рисунка. Для сада {L} на {W} метров с воротами нужно {posts|столб|столба|столбов}: столько же, сколько промежутков по {sp} метра на всей границе.",
 "question": "Первая заметка говорит «{ni#" + o.replace('|', ' страница раздела|').replace('девятнадцатой', 'девятнадцатая').replace('двадцать четвёртой', 'двадцать четвёртая').replace('тридцать третьей', 'тридцать третья').replace('двенадцатой', 'двенадцатая') + " страница раздела}», а вторая «на {back} меньше последней». Почему обе дают {page}, хотя {a} + {nth} не равно {page}?",
 "steps": [
  step("Какое издание открыть?", "У полок библиотекарь показывает четыре издания одного сборника. В каждом раздел загадок начинается и заканчивается на своих страницах. Одна из читательниц записала границы раздела в своей книге.",
   ["Запись читательницы: раздел загадок начинается на странице {a} и заканчивается на странице {b}.", "Издание А: загадки на страницах {aA}-{bA}.", "Издание Б: загадки на страницах {a}-{b}.", "Издание В: загадки на страницах {aC}-{bC}.", "Издание Г: загадки на страницах {a}-{bD}."],
   "Какое издание совпадает с записью?", "choice", ["Издание А", "Издание Б", "Издание В", "Издание Г"],
   ["В издании А раздел кончается на {bA}, там, где в записи он только начинается.", "", "В издании В раздел начинается на {aC}, сразу после конца раздела в записи.", "Начало совпадает, но раздел здесь заканчивается на {bD}, а в записи на {b}."],
   "Совпасть должны обе границы. Издание Г начинается на {a}, как в записи, но заканчивается на {bD} вместо {b}. Только издание Б даёт {a} и {b}.",
   "Библиотекарь открывает издание Б. Теперь нужно найти саму страницу по двум заметкам, которые считали по-разному.", "Найти страницу",
   ["Сравни и начало, и конец раздела.", "Одна граница может совпасть случайно. Проверь вторую.", "Только у одного издания совпадают обе границы."], 0),
  step("Какая это страница?", "За столом библиотекарь раскладывает две заметки. Одна читательница считала страницы раздела по порядку, другая отсчитывала назад от последней страницы. Обе имели в виду одну и ту же напечатанную страницу.",
   ["Раздел загадок занимает страницы с {a} по {b}.", "Первая заметка: «Задача про сад на {ni#" + o + "} странице раздела».", "Вторая заметка: «Номер страницы с задачей на {back} меньше номера последней страницы раздела».", "Первая страница раздела это страница {a}."],
   "Какой номер напечатан на нужной странице? Введи число.", "number", [], [],
   "Первая страница раздела {a}, вторая {a2}, значит {ni#" + O.lower() + "} это {a} + {nm1} = {page}. Проверка по второй заметке: {b} - {back} = {page}. Обе заметки указывают на {page}.",
   "Страница {page} найдена: там задача про сад. Но угол с рисунком повреждён. Библиотекарь достаёт папку ремонта с копиями.", "Подобрать копию рисунка",
   ["{ni#" + O + "} страница раздела: первая это {a}, вторая {a2}. Сколько прибавить к {a}?", "Вторая заметка: от последней страницы отними {back}.", "Обе заметки должны дать одно и то же число."], 1),
  step("Какая копия верная?", "В папке ремонта четыре копии рисунков к задачам про сады. Текст задачи на странице {page} сохранился, и по нему можно проверить каждую копию.",
   ["Текст: прямоугольный сад длиной {L} м и шириной {W} м.", "В ограде оставлен проём ворот шириной {g} м.", "Вдоль длинной стороны сада внутри ограды идёт дорожка шириной 1 м.", "Копия А: сад {L} × {W} м, ворота {g} м, дорожки нет.", "Копия Б: сад {L} × {W} м, ворота {g} м, дорожка вдоль длинной стороны.", "Копия В: сад {L} × {W1} м, ворота {g} м, дорожка вдоль длинной стороны.", "Копия Г: сад {L} × {W} м, ворота {g} м, дорожка вдоль короткой стороны."],
   "Какая копия соответствует тексту?", "choice", ["Копия А", "Копия Б", "Копия В", "Копия Г"],
   ["Размеры и ворота совпадают, но в тексте есть дорожка, а на копии А её нет.", "", "На копии В ширина сада {W1} м, а в тексте {W} м.", "Дорожка есть, но она идёт вдоль короткой стороны, а в тексте вдоль длинной."],
   "Нужно совпадение всех четырёх признаков: длина, ширина, ворота и дорожка вдоль длинной стороны. У А нет дорожки, у В другая ширина, у Г дорожка не там. Подходит только копия Б.",
   "Рисунок восстановлен по копии Б. Теперь можно прочитать задачу целиком и решить её к встрече клуба.", "Решить найденную задачу",
   ["Проверь каждую копию по всем четырём признакам, а не по первым двум.", "Дорожка это тоже признак: где она проходит?", "Копии могут совпадать в трёх признаках из четырёх. Нужна та, где совпадают все."], 2),
  step("Сколько нужно столбов?", "В комнате клуба читают задачу с восстановленной страницы. Ограда идёт по границе сада, столбы стоят через равные промежутки, а для ворот столбы нужны тем более.",
   ["Сад прямоугольный: длина {L} м, ширина {W} м.", "Столбы ставят по всей границе сада через каждые {sp} м, начиная от угла.", "Проём ворот шириной {g} м приходится ровно между двумя соседними столбами. Эти два столба остаются: на них вешают ворота.", "Дорожка внутри сада на ограду не влияет."],
   "Сколько столбов нужно для ограды? Введи число.", "number", [], [],
   "Граница сада: {L} + {W} + {L} + {W} = {P} м. На замкнутой границе столбов столько же, сколько промежутков по {sp} м: {P} : {sp} = {posts}. Ворота занимают один из промежутков, но столбы по его краям нужны, поэтому их по-прежнему {posts}.",
   "Задача решена: {posts|столб|столба|столбов}. Страница найдена, рисунок восстановлен, обе закладки возвращаются на страницу {page}.", "Передать книгу клубу",
   ["Сначала найди длину всей границы сада.", "На замкнутой границе столбов столько же, сколько промежутков по {sp} м.", "Ворота занимают один промежуток, но столбы по его краям остаются."], 3)
 ]}
o, O = ORD['pl']
L['pl'] = {
 "title": "Dwie zakładki i jedna strona",
 "intro": "Klub książki zbiera się, żeby omówić zadanie o ogrodzie ze zbioru zagadek. Dwie czytelniczki zaznaczały je zakładkami, ale podczas naprawy książki zakładki wyjęto, a róg strony z rysunkiem został uszkodzony. Zostały dwie notatki czytelniczek i teczka z kopiami rysunków. Pomóż bibliotekarce znaleźć wydanie, stronę i właściwą kopię, a potem rozwiązać zadanie, o które w tym wszystkim chodziło.",
 "ending": "Wydanie B jako jedyne zgadzało się z obiema granicami rozdziału: {a} i {b}. Obie notatki wskazały stronę {page}, choć liczyły inaczej: jedna od {ni#" + o + "} strony rozdziału, druga o {back} wstecz od ostatniej. Kopia B jako jedyna zgadzała się we wszystkich czterech cechach rysunku. Do ogrodu {L} na {W} metrów z furtką potrzeba {posts|słupka|słupki|słupków}: tyle samo, ile odcinków po {sp} metry na całej granicy.",
 "question": "Pierwsza notatka mówi „{ni#" + O.lower() + "} strona rozdziału”, a druga „o {back} mniej niż ostatnia”. Dlaczego obie dają {page}, skoro {a} + {nth} to nie {page}?",
 "steps": [
  step("Które wydanie otworzyć?", "Przy półkach bibliotekarka pokazuje cztery wydania tego samego zbioru. W każdym rozdział z zagadkami zaczyna się i kończy na innych stronach. Jedna z czytelniczek zapisała granice rozdziału w swojej książce.",
   ["Notatka czytelniczki: rozdział z zagadkami zaczyna się na stronie {a} i kończy na stronie {b}.", "Wydanie A: zagadki na stronach {aA}-{bA}.", "Wydanie B: zagadki na stronach {a}-{b}.", "Wydanie C: zagadki na stronach {aC}-{bC}.", "Wydanie D: zagadki na stronach {a}-{bD}."],
   "Które wydanie zgadza się z notatką?", "choice", ["Wydanie A", "Wydanie B", "Wydanie C", "Wydanie D"],
   ["W wydaniu A rozdział kończy się na {bA}, tam gdzie w notatce dopiero się zaczyna.", "", "W wydaniu C rozdział zaczyna się na {aC}, zaraz po końcu rozdziału z notatki.", "Początek się zgadza, ale rozdział kończy się tu na {bD}, a w notatce na {b}."],
   "Zgadzać się muszą obie granice. Wydanie D zaczyna się na {a}, jak w notatce, ale kończy na {bD} zamiast {b}. Tylko wydanie B daje {a} i {b}.",
   "Bibliotekarka otwiera wydanie B. Teraz trzeba znaleźć samą stronę według dwóch notatek, które liczyły inaczej.", "Znajdź stronę",
   ["Porównaj i początek, i koniec rozdziału.", "Jedna granica może zgadzać się przypadkiem. Sprawdź drugą.", "Tylko w jednym wydaniu zgadzają się obie granice."], 0),
  step("Która to strona?", "Przy stole bibliotekarka rozkłada dwie notatki. Jedna czytelniczka liczyła strony rozdziału po kolei, druga odliczała wstecz od ostatniej strony. Obie miały na myśli tę samą wydrukowaną stronę.",
   ["Rozdział z zagadkami zajmuje strony od {a} do {b}.", "Pierwsza notatka: „Zadanie o ogrodzie jest na {ni#" + o + "} stronie rozdziału”.", "Druga notatka: „Numer strony z zadaniem jest o {back} mniejszy niż numer ostatniej strony rozdziału”.", "Pierwsza strona rozdziału to strona {a}."],
   "Jaki numer jest wydrukowany na szukanej stronie? Wpisz liczbę.", "number", [], [],
   "Pierwsza strona rozdziału to {a}, druga {a2}, więc {ni#" + O.lower() + "} to {a} + {nm1} = {page}. Sprawdzenie z drugiej notatki: {b} - {back} = {page}. Obie notatki wskazują {page}.",
   "Strona {page} znaleziona: tam jest zadanie o ogrodzie. Ale róg z rysunkiem jest uszkodzony. Bibliotekarka wyjmuje teczkę naprawy z kopiami.", "Dobierz kopię rysunku",
   ["{ni#" + O + "} strona rozdziału: pierwsza to {a}, druga {a2}. Ile dodać do {a}?", "Druga notatka: od ostatniej strony odejmij {back}.", "Obie notatki muszą dać tę samą liczbę."], 1),
  step("Która kopia jest właściwa?", "W teczce naprawy są cztery kopie rysunków do zadań o ogrodach. Tekst zadania na stronie {page} się zachował i można według niego sprawdzić każdą kopię.",
   ["Tekst: prostokątny ogród o długości {L} m i szerokości {W} m.", "W ogrodzeniu zostawiono otwór na furtkę o szerokości {g} m.", "Wzdłuż dłuższego boku ogrodu, po wewnętrznej stronie ogrodzenia, biegnie ścieżka o szerokości 1 m.", "Kopia A: ogród {L} × {W} m, furtka {g} m, bez ścieżki.", "Kopia B: ogród {L} × {W} m, furtka {g} m, ścieżka wzdłuż dłuższego boku.", "Kopia C: ogród {L} × {W1} m, furtka {g} m, ścieżka wzdłuż dłuższego boku.", "Kopia D: ogród {L} × {W} m, furtka {g} m, ścieżka wzdłuż krótszego boku."],
   "Która kopia odpowiada tekstowi?", "choice", ["Kopia A", "Kopia B", "Kopia C", "Kopia D"],
   ["Wymiary i furtka się zgadzają, ale w tekście jest ścieżka, a na kopii A jej nie ma.", "", "Na kopii C szerokość ogrodu to {W1} m, a w tekście {W} m.", "Ścieżka jest, ale biegnie wzdłuż krótszego boku, a w tekście wzdłuż dłuższego."],
   "Potrzebna jest zgodność wszystkich czterech cech: długość, szerokość, furtka i ścieżka wzdłuż dłuższego boku. A nie ma ścieżki, C ma inną szerokość, D ma ścieżkę nie tam. Pasuje tylko kopia B.",
   "Rysunek odtworzono według kopii B. Teraz można przeczytać zadanie w całości i rozwiązać je na spotkanie klubu.", "Rozwiąż znalezione zadanie",
   ["Sprawdź każdą kopię według wszystkich czterech cech, a nie tylko dwóch pierwszych.", "Ścieżka to też cecha: gdzie biegnie?", "Kopie mogą zgadzać się w trzech cechach z czterech. Potrzebna jest ta, w której zgadzają się wszystkie."], 2),
  step("Ile potrzeba słupków?", "W sali klubu czytają zadanie z odtworzonej strony. Ogrodzenie biegnie wzdłuż granicy ogrodu, słupki stoją w równych odstępach, a przy furtce słupki są potrzebne tym bardziej.",
   ["Ogród jest prostokątny: długość {L} m, szerokość {W} m.", "Słupki stawia się wzdłuż całej granicy ogrodu co {sp} m, zaczynając od narożnika.", "Otwór na furtkę o szerokości {g} m wypada dokładnie między dwoma sąsiednimi słupkami. Te dwa słupki zostają: na nich wiesza się furtkę.", "Ścieżka wewnątrz ogrodu nie wpływa na ogrodzenie."],
   "Ile słupków potrzeba do ogrodzenia? Wpisz liczbę.", "number", [], [],
   "Granica ogrodu: {L} + {W} + {L} + {W} = {P} m. Na zamkniętej granicy słupków jest tyle samo, ile odcinków po {sp} m: {P} : {sp} = {posts}. Furtka zajmuje jeden z odcinków, ale słupki na jego końcach są potrzebne, więc nadal jest ich {posts}.",
   "Zadanie rozwiązane: {posts|słupek|słupki|słupków}. Strona znaleziona, rysunek odtworzony, obie zakładki wracają na stronę {page}.", "Przekaż książkę klubowi",
   ["Najpierw znajdź długość całej granicy ogrodu.", "Na zamkniętej granicy słupków jest tyle samo, ile odcinków po {sp} m.", "Furtka zajmuje jeden odcinek, ale słupki na jego końcach zostają."], 3)
 ]}
o, O = ORD['en']
L['en'] = {
 "title": "Two Bookmarks and One Page",
 "intro": "The book club is meeting to discuss a garden puzzle from a riddle collection. Two readers had marked it with bookmarks, but the bookmarks were removed when the book was repaired, and the corner of the page with the drawing got damaged. What remains are the two readers’ notes and a folder of drawing copies. Help the librarian find the edition, the page and the right copy, and then solve the puzzle this was all about.",
 "ending": "Edition B was the only one that matched both section boundaries: {a} and {b}. Both notes pointed to page {page}, although they counted differently: one from the {ni#" + o + "} page of the section, the other {back} back from the last. Copy B was the only one that matched all four features of the drawing. The {L} by {W} metre garden with a gate needs {posts} posts: as many as there are {sp}-metre gaps around the whole boundary.",
 "question": "The first note says “the {ni#" + o + "} page of the section” and the second “{back} less than the last”. Why do both give {page}, when {a} + {nth} is not {page}?",
 "steps": [
  step("Which edition to open?", "At the shelves, the librarian shows four editions of the same collection. In each, the riddle section starts and ends on different pages. One of the readers wrote down the section boundaries in her copy.",
   ["The reader’s note: the riddle section begins on page {a} and ends on page {b}.", "Edition A: riddles on pages {aA}-{bA}.", "Edition B: riddles on pages {a}-{b}.", "Edition C: riddles on pages {aC}-{bC}.", "Edition D: riddles on pages {a}-{bD}."],
   "Which edition matches the note?", "choice", ["Edition A", "Edition B", "Edition C", "Edition D"],
   ["In edition A the section ends on {bA}, where in the note it only begins.", "", "In edition C the section begins on {aC}, right after the end of the section in the note.", "The start matches, but here the section ends on {bD}, and in the note on {b}."],
   "Both boundaries have to match. Edition D starts on {a} like the note but ends on {bD} instead of {b}. Only edition B gives {a} and {b}.",
   "The librarian opens edition B. Now the page itself has to be found from two notes that counted in different ways.", "Find the page",
   ["Compare both the start and the end of the section.", "One boundary can match by chance. Check the other.", "Only one edition matches both boundaries."], 0),
  step("Which page is it?", "At the desk, the librarian lays out the two notes. One reader counted the pages of the section in order; the other counted back from the last page. Both meant the same printed page.",
   ["The riddle section occupies pages {a} to {b}.", "First note: “The garden puzzle is on the {ni#" + o + "} page of the section.”", "Second note: “The number of the puzzle page is {back} less than the number of the last page of the section.”", "The first page of the section is page {a}."],
   "What number is printed on the page we need? Enter a number.", "number", [], [],
   "The first page of the section is {a}, the second is {a2}, so the {ni#" + o + "} is {a} + {nm1} = {page}. Check with the second note: {b} - {back} = {page}. Both notes point to {page}.",
   "Page {page} is found: the garden puzzle is there. But the corner with the drawing is damaged. The librarian takes out the repair folder with the copies.", "Pick the drawing copy",
   ["{ni#" + O + "} page of the section: the first is {a}, the second is {a2}. How much do you add to {a}?", "Second note: subtract {back} from the last page.", "Both notes must give the same number."], 1),
  step("Which copy is right?", "The repair folder holds four copies of drawings for garden puzzles. The text of the puzzle on page {page} has survived, so each copy can be checked against it.",
   ["Text: a rectangular garden {L} m long and {W} m wide.", "A {g} m wide gate opening is left in the fence.", "Along the long side of the garden, inside the fence, runs a path 1 m wide.", "Copy A: garden {L} × {W} m, gate {g} m, no path.", "Copy B: garden {L} × {W} m, gate {g} m, path along the long side.", "Copy C: garden {L} × {W1} m, gate {g} m, path along the long side.", "Copy D: garden {L} × {W} m, gate {g} m, path along the short side."],
   "Which copy matches the text?", "choice", ["Copy A", "Copy B", "Copy C", "Copy D"],
   ["The dimensions and gate match, but the text has a path and copy A has none.", "", "In copy C the garden is {W1} m wide, and in the text it is {W} m.", "There is a path, but it runs along the short side, and in the text along the long side."],
   "All four features must match: length, width, gate and a path along the long side. A has no path, C has a different width, D has the path in the wrong place. Only copy B fits.",
   "The drawing is restored from copy B. Now the puzzle can be read in full and solved for the club meeting.", "Solve the puzzle you found",
   ["Check each copy against all four features, not just the first two.", "The path is a feature too: where does it run?", "Copies can match three features out of four. You need the one that matches all of them."], 2),
  step("How many posts are needed?", "In the club room, they read the puzzle from the restored page. The fence runs along the garden boundary, the posts stand at equal intervals, and the gate needs posts more than anything.",
   ["The garden is rectangular: {L} m long and {W} m wide.", "Posts are placed along the whole boundary of the garden every {sp} m, starting from a corner.", "The {g} m gate opening falls exactly between two neighbouring posts. Those two posts stay: the gate hangs on them.", "The path inside the garden does not affect the fence."],
   "How many posts are needed for the fence? Enter a number.", "number", [], [],
   "The garden boundary: {L} + {W} + {L} + {W} = {P} m. On a closed boundary there are as many posts as {sp} m gaps: {P} ÷ {sp} = {posts}. The gate takes up one of the gaps, but the posts at its edges are needed, so there are still {posts}.",
   "The puzzle is solved: {posts} posts. The page is found, the drawing is restored, and both bookmarks go back to page {page}.", "Hand the book to the club",
   ["First find the length of the whole garden boundary.", "On a closed boundary there are as many posts as {sp} m gaps.", "The gate takes up one gap, but the posts at its edges stay."], 3)
 ]}
o, O = ORD['uk']
L['uk'] = {
 "title": "Дві закладки й одна сторінка",
 "intro": "Книжковий клуб збирається обговорити задачу про сад зі збірки загадок. Дві читачки позначали її закладками, але під час ремонту книжки закладки вийняли, а кут сторінки з малюнком пошкодився. Залишилися дві нотатки читачок і тека з копіями малюнків. Допоможи бібліотекарці знайти видання, сторінку і правильну копію, а потім розв’язати задачу, заради якої все затівалося.",
 "ending": "Видання Б єдине збіглося за обома межами розділу: {a} і {b}. Обидві нотатки вказали на сторінку {page}, хоча рахували по-різному: одна з {ni#" + o.replace('дев’ятнадцятій', 'дев’ятнадцятої').replace('двадцять четвертій', 'двадцять четвертої').replace('тридцять третій', 'тридцять третьої').replace('дванадцятій', 'дванадцятої') + "} сторінки розділу, друга на {back} назад від останньої. Копія Б єдина збіглася за всіма чотирма ознаками малюнка. Для саду {L} на {W} метрів із хвірткою потрібно {posts|стовп|стовпи|стовпів}: стільки ж, скільки проміжків по {sp} метри на всій межі.",
 "question": "Перша нотатка каже «{ni#" + O.lower() + "} сторінка розділу», а друга «на {back} менше за останню». Чому обидві дають {page}, хоча {a} + {nth} не дорівнює {page}?",
 "steps": [
  step("Яке видання відкрити?", "Біля полиць бібліотекарка показує чотири видання однієї збірки. У кожному розділ загадок починається і закінчується на своїх сторінках. Одна з читачок записала межі розділу у своїй книжці.",
   ["Запис читачки: розділ загадок починається на сторінці {a} і закінчується на сторінці {b}.", "Видання А: загадки на сторінках {aA}-{bA}.", "Видання Б: загадки на сторінках {a}-{b}.", "Видання В: загадки на сторінках {aC}-{bC}.", "Видання Г: загадки на сторінках {a}-{bD}."],
   "Яке видання збігається із записом?", "choice", ["Видання А", "Видання Б", "Видання В", "Видання Г"],
   ["У виданні А розділ закінчується на {bA}, там, де в записі він лише починається.", "", "У виданні В розділ починається на {aC}, одразу після кінця розділу в записі.", "Початок збігається, але розділ тут закінчується на {bD}, а в записі на {b}."],
   "Збігтися мають обидві межі. Видання Г починається на {a}, як у записі, але закінчується на {bD} замість {b}. Лише видання Б дає {a} і {b}.",
   "Бібліотекарка відкриває видання Б. Тепер треба знайти саму сторінку за двома нотатками, які рахували по-різному.", "Знайти сторінку",
   ["Порівняй і початок, і кінець розділу.", "Одна межа може збігтися випадково. Перевір другу.", "Лише в одного видання збігаються обидві межі."], 0),
  step("Яка це сторінка?", "За столом бібліотекарка розкладає дві нотатки. Одна читачка рахувала сторінки розділу по порядку, друга відлічувала назад від останньої сторінки. Обидві мали на увазі ту саму надруковану сторінку.",
   ["Розділ загадок займає сторінки з {a} по {b}.", "Перша нотатка: «Задача про сад на {ni#" + o + "} сторінці розділу».", "Друга нотатка: «Номер сторінки із задачею на {back} менший за номер останньої сторінки розділу».", "Перша сторінка розділу це сторінка {a}."],
   "Який номер надруковано на потрібній сторінці? Введи число.", "number", [], [],
   "Перша сторінка розділу {a}, друга {a2}, отже {ni#" + O.lower() + "} це {a} + {nm1} = {page}. Перевірка за другою нотаткою: {b} - {back} = {page}. Обидві нотатки вказують на {page}.",
   "Сторінку {page} знайдено: там задача про сад. Але кут із малюнком пошкоджено. Бібліотекарка дістає теку ремонту з копіями.", "Дібрати копію малюнка",
   ["{ni#" + O + "} сторінка розділу: перша це {a}, друга {a2}. Скільки додати до {a}?", "Друга нотатка: від останньої сторінки відніми {back}.", "Обидві нотатки мають дати те саме число."], 1),
  step("Яка копія правильна?", "У теці ремонту чотири копії малюнків до задач про сади. Текст задачі на сторінці {page} зберігся, і за ним можна перевірити кожну копію.",
   ["Текст: прямокутний сад завдовжки {L} м і завширшки {W} м.", "В огорожі залишено проріз хвіртки завширшки {g} м.", "Уздовж довгої сторони саду всередині огорожі йде доріжка завширшки 1 м.", "Копія А: сад {L} × {W} м, хвіртка {g} м, доріжки немає.", "Копія Б: сад {L} × {W} м, хвіртка {g} м, доріжка вздовж довгої сторони.", "Копія В: сад {L} × {W1} м, хвіртка {g} м, доріжка вздовж довгої сторони.", "Копія Г: сад {L} × {W} м, хвіртка {g} м, доріжка вздовж короткої сторони."],
   "Яка копія відповідає тексту?", "choice", ["Копія А", "Копія Б", "Копія В", "Копія Г"],
   ["Розміри і хвіртка збігаються, але в тексті є доріжка, а на копії А її немає.", "", "На копії В ширина саду {W1} м, а в тексті {W} м.", "Доріжка є, але вона йде вздовж короткої сторони, а в тексті вздовж довгої."],
   "Потрібен збіг усіх чотирьох ознак: довжина, ширина, хвіртка і доріжка вздовж довгої сторони. В А немає доріжки, у В інша ширина, у Г доріжка не там. Підходить лише копія Б.",
   "Малюнок відновлено за копією Б. Тепер можна прочитати задачу цілком і розв’язати її до зустрічі клубу.", "Розв’язати знайдену задачу",
   ["Перевір кожну копію за всіма чотирма ознаками, а не за першими двома.", "Доріжка це теж ознака: де вона проходить?", "Копії можуть збігатися у трьох ознаках із чотирьох. Потрібна та, де збігаються всі."], 2),
  step("Скільки потрібно стовпів?", "У кімнаті клубу читають задачу з відновленої сторінки. Огорожа йде по межі саду, стовпи стоять через рівні проміжки, а для хвіртки стовпи потрібні тим паче.",
   ["Сад прямокутний: довжина {L} м, ширина {W} м.", "Стовпи ставлять по всій межі саду через кожні {sp} м, починаючи від кута.", "Проріз хвіртки завширшки {g} м припадає рівно між двома сусідніми стовпами. Ці два стовпи залишаються: на них вішають хвіртку.", "Доріжка всередині саду на огорожу не впливає."],
   "Скільки стовпів потрібно для огорожі? Введи число.", "number", [], [],
   "Межа саду: {L} + {W} + {L} + {W} = {P} м. На замкненій межі стовпів стільки ж, скільки проміжків по {sp} м: {P} : {sp} = {posts}. Хвіртка займає один із проміжків, але стовпи по його краях потрібні, тому їх так само {posts}.",
   "Задачу розв’язано: {posts|стовп|стовпи|стовпів}. Сторінку знайдено, малюнок відновлено, обидві закладки повертаються на сторінку {page}.", "Передати книжку клубу",
   ["Спершу знайди довжину всієї межі саду.", "На замкненій межі стовпів стільки ж, скільки проміжків по {sp} м.", "Хвіртка займає один проміжок, але стовпи по його краях залишаються."], 3)
 ]}
if __name__ == '__main__':
    write_case('library', '010', L, variants())
