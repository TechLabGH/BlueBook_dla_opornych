#### Przedruk: Elektronika dla Wszystkich - Listopad 2015

Jedno z bardziej rzeczowych wyjaśnień

Czym jest wskaźnik? Ogólnie mówiąc, jest to adres zmiennej, czyli liczba wskazująca, w którym miejscu pamięci operacyjnej znajduje się dana zmienna.

W pierwszej chwili adres zmiennej może się wydać czymś niezbyt potrzebnym w pisaniu programu, jednak w C jest to bardzo często wykorzystywana dana. Jednym z zastosowań wskaźników jest dostęp do elementów zmiennych tablicowych. Za pomocą zmiennej wskaźnikowej możemy przemieszczać się po elementach tablicy. 

Zadeklarujmy więc zmienną tablicową:
```c
char napis[] = "Elektronika";
```
a następnie zmienną wskaźnikową:
```c
char * w;
```
Nie, nie odbywa się tutaj mnożenie. Gwiazdka oznacza tu, że deklarujemy zmienną wskaźnikową (wskaźnik), która będzie zawierała adres danej typu char. Której zmiennej? Tego jeszcze nie wiadomo, gdyż nowo zadeklarowana zmienna nie została jeszcze zainicjalizowana i jest w tej chwili bezużyteczna.

Zainicjalizujmy więc wskaźnik:
```c
w = napis;
```
Tak prosto? Tak, w języku C nazwa zmiennej tablicowej jest wskaźnikiem na jej pierwszy element. Co więcej, w tej chwili możemy używać zamiennie zmiennych w
oraz napisu:
```c
printf("%s\n", napis);
printf("%s\n", w);
```
Możemy traktować zmienną w jak tablicę:
```c
printf("%c\n", w[2]);
```
Zostanie wyświetlona litera e. OK, jest to ciekawe, ale nadal nie wiemy, co nam taka zmienna wskaźnikowa daje. Skoro jest to zmienna, to zmodyfikujmy ją, np. zwiększając o 1:
```c
w++;
```
Wykonajmy ponownie linijki:
```c
printf("%s\n", w);
printf("%c\n", w[2]);
```
Pojawił się napis "lektronika" oraz litera k. Przesunęliśmy bowiem wskaźnik o jeden bajt do przodu. Wiemy już, że do danych wskazywanych
przez wskaźnik możemy odwoływać się za pomocą notacji tablicowej. Zazwyczaj jednak robi się to za pomocą operatora wyłuskania. Tym operatorem znów jest gwiazdka:
```c
char z = *w;
printf("%c\n", z);
printf("%c\n", *w);
printf("%c\n", *(w+1));
```
W powyższym przykładzie deklarowana jest nowa zmienna, której przypisywana jest wartość wskazywana przez zmienną w. Kolejne wywołanie funkcji printf wyświetla tę samą daną, ale już bez pośrednictwa zmiennej z. W trzecim wywołaniu wyświetlana jest zawartość bajtu, który znajduje się za bajtem wskazywanym przez w. Dzięki wskaźnikom można swobodnie „jeździć” po pamięci. Jest to potężne narzędzie w języku C, ale jednocześnie niebezpieczne. Łatwo bowiem strzelić sobie
w stopę, odwołując się przez przypadek do niewłaściwego miejsca w pamięci. Jeśli za pomocą wskaźnika odwołujemy się do tablicy, nie ma sprawdzania, czy nie wyszliśmy poza jej obszar. Można więc nie tylko odczytać nie te dane, które się chciało, ale też przypadkowo zmodyfikować inne zmienne. Jeśli odwołamy się do obszaru pamięci poza przestrzenią naszego procesu, system operacyjny zamknie nasz program i zostanie wyświetlony komunikat o wykonaniu nieprawidłowej operacji. Jeśli jednak będzie to obszar wewnątrz naszego procesu, najprawdopodobniej nie będzie żadnego komunikatu, a jedynie nieprawidłowość w działaniu naszego programu, niekoniecznie widoczna od razu. Rozważmy przykład: 
```c
char napis[] = "Elektronika";
int a = 10;
char * w;
w = napis;
w -= 12;
*w = 100;
printf("%d\n", a);
```
Jeśli kod ten zostanie skompilowany pod Visual C++ 2010, zauważymy, że za pomocą wskaźnika w zmodyfikowaliśmy zmienną a i jej wartość wynosi 100, a nie 10. W przypadku kompilatora GCC zmienna a jest w pamięci za zmienną napis i trzeba do wskaźnika w dodać wartość 12, a nie odjąć. Jeśli to samo zrobimy w Visual C++ (w += 12;), przy wychodzeniu z funkcji włączy się ochrona stosu i program zostanie zamknięty. Zainteresowani mogą wygooglować hasło „stack cookies” oraz opis działania przełącznika /GS w Visual C++. 

#### Przekazywanie argumentów funkcji przez wskaźniki. 

W języku C używamy często wskaźników do przekazywania danych do funkcji. Parametry bowiem są przekazywane przez wartość. Jeśli chcemy przekazać do funkcji zmienną tak, aby funkcja mogła tę zmienną zmodyfikować, używamy wkaźnika. Popatrzmy na przykład:
```c
#include <stdio.h>
void dodaj(int a);
int main() {
int a = 3;
dodaj(a);
printf("%d\n",a);
return 0;
}
void dodaj(int a) {
a += 5;
printf("%d\n",a);
}
```
W wyniku dostaniemy liczby 8 oraz 3. Wartość 3 została przekazana do funkcji i tam zwiększona, wyświetlone zostało 8. Jednak zmienna w funkcji main nadal miała wartość 3, co zostało potem wyświetlone. Problem możemy rozwiązać przez zwracanie wartości:
```c
#include <stdio.h>
int dodaj(int a);
int main() {
int a = 3;
a = dodaj(a);
printf("%d\n",a);
return 0;
}
int dodaj(int a) {
a += 5;
printf("%d\n",a);
return a;
}
```
Zmieniliśmy zwracany typ z void na int, a zwracana wartość przypisywana jest do zmiennej. Problem jednak w tym, że nie zawsze możemy skorzystać z tego sposobu.
Często potrzebujemy zwracać kilka wartości. Tutaj z pomocą przychodzą wskaźniki:
```c
#include <stdio.h>
void dodaj(int * a);
int main() {
int a = 3;
dodaj(&a);
printf("%d\n",a);
return 0;
}
void dodaj(int * a) {
*a += 5;
printf("%d\n", *a);
}
```
Deklarujemy funkcję dodaj jako przyjmującą jako argument wskaźnik na zmienną typu int. Aby taki wskaźnik uzyskać, stosujemy operator &.

autor: Grzegorz Niemirowski
grzegorz@grzegorz.net