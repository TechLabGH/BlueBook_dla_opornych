Jeśli ktoś nie miał okazji dłużej pobawić się z wyświetlaczami alfanumerycznymi LCD bazującymi na układzie 44780, albo obsługiwał je wyłącznie z arduino, 
o wielu funkcjach tego układu może nawet nie miec pojecia.

Na własne potrzeby przeczytałem pełną notę katalogową układu i zamieszczam swoje notatki

HD44780 posiada dwa 8-bitowe rejestry:
 - rejestr instrukcji - IR (instruction register)
 - rejestr danych - DR (data register)

Rejestr instrukcji może być zapisany tylko z zewnątrz (przez MPU). Do rego rejestru wpisywane są komendy, albo adresy rejestru danych do którego są wpisywane, 
albo z którego czytane dane.
Rejestr danych może być zapisany przez MPU (jako wejście danych) lub sam układ (jako wyjście danych odczytywanych z wyświetlacza).

Poniżej tabelka, która trochę lepiej wyjaśnia, jak działają linie RS i RW:
```
 RS  RW    Operacja
-------------------------------------------------------------------------------------
 0   0     Zapisanie do IR wewnętrznej oparacji (komendy) - np wyczyść ekran
 0   1     Odczyt flagi zajętości (DB7) i licznika adresów (AC) (DB0...DB6)
 1   0     Zapis do rejestru danych (DR)
 1   1     Odczyt z rejestru danych (DR)
```

Licznik adresów (Address counter AC) - Przechowuje adres pamięci DDRAM lub CGRAM do którego wpisujemy lub z którego czytamy dane. Po każdej takiej operacji 
jego wartość sama się inkrementuje (przy wpisywaniu) albo dekrementuje (przy odczycie). Dzięki temu można wysłać do wyświetlacza jakiś znak wyświetlony 
w konkretnym miejscu, a następny znak zostanie wyświetlony automatycznie obok. 

DDRAM (Display Data RAM) - ma pojemność 640 bitów / 80 bajtów (znaków). Najpopularniejsze modele mają 20x2 lub 16x2; mniej polularne 20x4 albo 40x2 więc 
teoretycznie nie każdy wymaga aż tak dużej pamięci. W pierwszych dwóch przypadkach wyświetlcz pokazuje tylko znaki zapisane we fragmencie pamięci. 
Pozostałe znaki znajdują się natomiast "na prawo" od tych wyświetlonych - jakby poza ekranem. Podczas inicjalizacji wyświetlacza, należy mu więc 
wysłać informację, ile linii tekstu bedzie wyświetlał.

## Standardowe adresowanie DDRAM w HR44780:
```
|1 |2 |3 |4 |5 |6 |7 |8 |9 |10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|32|33|34|35|36|37|38|39|40|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|00|01|02|03|04|05|06|07|08|09|0A|0B|0C|0D|0E|0F|10|11|12|13|14|15|16|17|18|19|1A|1B|1C|1D|1E|1F|20|21|22|23|24|25|26|27|
|40|41|42|43|44|45|46|47|48|49|4A|4B|4C|4D|4E|4F|50|51|52|53|54|55|56|57|58|59|5A|5B|5C|5D|5E|5F|60|61|62|63|64|65|66|67|
```
Zależnie od formatu wyświetlacza, pamięć ta jest różnie dzielona

###### 40x2 LCD - każdy adres pamięci DDRAM jest ściśle powiązany z jednym znakiem na wyświetlaczu
```
+---------------------------------------------------------+
|00                  <--- linia 1 --->                  27|
+---------------------------------------------------------+
|40                  <--- linia 2 --->                  67|
+---------------------------------------------------------+
```
###### 20x4 LCD
w tym przypadku pamięć zostaje dodatkowo podzielona tak:
```
|1 |2 |3 |4 |5 |6 |7 |8 |9 |10|11|12|13|14|15|16|17|18|19|20|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|00|01|02|03|04|05|06|07|08|09|0A|0B|0C|0D|0E|0F|10|11|12|13|
|40|41|42|43|44|45|46|47|48|49|4A|4B|4C|4D|4E|4F|50|51|52|53|
|14|15|16|17|18|19|1A|1B|1C|1D|1E|1F|20|21|22|23|24|25|26|27|
|54|55|56|57|58|59|5A|5B|5C|5D|5E|5F|60|61|62|63|64|65|66|67|
```
```
+-------------------------++-------------------------+
|00  <--- linia 1 --->  13||14  <--- linia 3 --->  27|
+-------------------------++-------------------------+
|40  <--- linia 2 --->  53||54  <--- linia 4 --->  67|
+-------------------------++-------------------------+
```
###### 20x2 LCD
W tym wypadku cała pamięć jest dostępna nadal, ale znaki są wyświetlane tylko z jej fragmentu.
```
+-------------------------++-------------------------+
|00  <--- linia 1 --->  13||14    linia 1 ukryta   27|
+-------------------------++-------------------------+
|40  <--- linia 2 --->  53||54    linia 2 ukryta   67|
+-------------------------++-------------------------+
```
Znaki zapisane w adresach 14-27 i 54-67 nie są tracone i mogą być wyświetlone po wydaniu instrukcji przesunięcia (Display shift)

Przesunięcie w lewo wyświetli więc znaki z rejestrów:
```
+-------------------------++-------------------------+
|01  <--- linia 1 --->  14||15 linia 1 ukryta   27|00|    <<
+-------------------------++-------------------------+
|41  <--- linia 2 --->  54||54 linia 2 ukryta   67|40|    <<
+-------------------------++-------------------------+
```
Przesunięcie w prawo natomiast pokaże znaki zapisane w ostatnich komórkach DDRAM
```
+---------------------------++-----------------------+
|27|00 <--- linia 1 --->  12||13  linia 1 ukryta   26|    >>
+---------------------------++-----------------------+
|67|40 <--- linia 2 --->  52||53  linia 2 ukryta   66|    >>
+---------------------------++-----------------------+
```
###### 16x1 LCD (typ 1)
Pomimo, że wyświetlacz ma tylko jedną linię, układ traktuje go jak dwuliniowy

Na początku wyświetlane są znaki z adresów:
```
|1 |2 |3 |4 |5 |6 |7 |8 |9 |10|11|12|13|14|15|16|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|00|01|02|03|04|05|06|07|40|41|42|43|44|45|46|47|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```
Nadal całe 80 bajtów jest programoiwalne, ale jeden zestaw jest używany do wyświetlania lewych, a drugi - prawych 8miu znaków
```
+----------------------------++-------------------------+
|00 <--- linia 1  LEWA---> 07||08     znaki ukryte    27|
+----------------------------++-------------------------+
|40 <--- linia 2 PRAWA---> 47||48     znaki ukryte    67|
+----------------------------++-------------------------+
```
Wyświetlanie na tych wyświetlaczach wymaga dodatkowych zabiegów (nie możemy wyświetlić 9 znaków na raz bez ustawiania nowego adresu dla ostatniego znaku). 
Dodatkowo przesuięcia stają się dużo bardziej skomplikowane.

###### 16x1 LCD (typ 2)
To niestety mniej popularna wersja tego wyświetlacza, natomiast dużo prostrza do kontrolowania, bo wykorzystuje tylko pierwszą linię pamięci, ale nie 
dzieli jej dodatkowo.
```
|1 |2 |3 |4 |5 |6 |7 |8 |9 |10|11|12|13|14|15|16|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|00|01|02|03|04|05|06|07|08|09|0A|0B|0C|0D|0E|0F|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```
```
+-------------------------++-------------------------+
|00 <---  linia 1 --->  0F||10     znaki ukryte    4F|
+-------------------------++-------------------------+
```

###### 16x2 LCD
Tutaj mala uwaga. Sprawdzilem dwa z posiadanych wyswietlaczy 16x2 i oba maja inne rodzaje adresowania. W kodzie ponizej uzylem rozwiadania, ktore dziala 
dla mnie, ale jesli dziala ci tylko polowa wyswietlacza, to nalezy 
zmienic ustawienia

Moj wyswietlacz:
```
|1 |2 |3 |4 |5 |6 |7 |8 |9 |10|11|12|13|14|15|16|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|00|01|02|03|04|05|06|07|08|09|0A|0B|0C|0D|0E|0F|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|40|41|42|43|44|45|46|47|48|49|4A|4B|4C|4D|4E|4F|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```
```
+-------------------------++-------------------------+
|00  <--- linia 1 --->  0F||10    linia 1 ukryta   27|
+-------------------------++-------------------------+
|40  <--- linia 2 --->  4F||50    linia 2 ukryta   67|
+-------------------------++-------------------------+
```
Drugi wyswietlacz - konfiguracja nie sprawdzona
```
|1 |2 |3 |4 |5 |6 |7 |8 |9 |10|11|12|13|14|15|16|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|00|01|02|03|04|05|06|07|14|15|16|17|18|19|1A|1B|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--'
|48|49|4A|4B|4C|4D|4E|4F|54|55|56|57|58|59|5A|5B|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```
```
+-------------------------++-------------------------++-------------------------++-------------------------+
|00 <--- linia 1 L ---> 0F||10   linia 1 L ukryta  13||14 <--- linia 1 R ---> 1B||1C   linia 1 R ukryta  27|
+-------------------------++-------------------------++-------------------------++-------------------------+
|40 <--- linia 2 L ---> 4F||50   linia 2 L ukryta  53||54 <--- linia 2 R ---> 5B||5C   linia 2 R ukryta  67|
+-------------------------++-------------------------++-------------------------++-------------------------+
```
Takie rozlozenie DDRAM dosc bardzo komplikuje sprawe i nie chcialo mi sie tego testowac. Chyba najlatwiej byloby traktowac go jak wyswietlacz 20x4 pokazany 
wyzej na ktorym widoczne jest tylko 8 lewych znakow, linia 3 jest
kontynuacja pierwszej, a czwarta - drugiej.

###### 16x4 LCD
```
|1 |2 |3 |4 |5 |6 |7 |8 |9 |10|11|12|13|14|15|16|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|00|01|02|03|04|05|06|07|08|09|0A|0B|0C|0D|0E|0F|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|40|41|42|43|44|45|46|47|48|49|4A|4B|4C|4D|4E|4F|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|10|11|12|13|14|15|16|17|18|19|1A|1B|1C|1D|1E|1F|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
|50|51|52|53|54|55|56|57|58|59|5A|5B|5C|5D|5E|5F|
+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
```
```
+-----------------------+-----------------------+--------------------+
|00 <--- linia 1 ---> 0F|10 <--- linia 3 ---> 1F|20  znaki ukryte  27|
+-----------------------+-----------------------+--------------------+
|40 <--- linia 2 ---> 4F|50 <--- linia 4 ---> 5F|60  znaki ukryte  67|
+-----------------------+-----------------------+--------------------+
```
Tu wprawdzie wpisuje się tekst łatwiej, ale przy przesunięciu, zawsze przesuwają się dwie linie.

###### 40x4 LCD
W tych wyświetlaczach montowane są dwa układy HD44780. Każdy z nich kontroluje dwie linie, więc pierwsza i trzecia linia będą mieć identyczne adresowanie, 
ale zapisywane osobno w każdym z dwóch układów. 


## Dodatkowe znaki

Tablica ASCI zawiera 127 "znaków" - w cudzysłowie - bo pierwsze 32 (0x00-0x1F 0-31) nie są drukowalne. Dopiero znak (0x20 - 32) oznacza spację, 33 to ! ... 
do 127 (0x7F), gdzie znajduje się DEL (wyjścietlany jako <- przez 44780).
```
0b        0x ASCI  0b        0x ASCI  0b        0x ASCI   
00100000  20  SP   01000000  40  @    01100000  60  `
00100001  21  !    01000001  41  A    01100001  61  a
00100010  22  “    01000010  42  B    01100010  62  b
00100011  23  #    01000011  43  C    01100011  63  c
00100100  24  $    01000100  44  D    01100100  64  d
00100101  25  %    01000101  45  E    01100101  65  e
00100110  26  &    01000110  46  F    01100110  66  f
00100111  27  ‘    01000111  47  G    01100111  67  g
00101000  28  (    01001000  48  H    01101000  68  h
00101001  29  )    01001001  49  I    01101001  69  i
00101010  2A  *    01001010  4A  J    01101010  6A  j
00101011  2B  +    01001011  4B  K    01101011  6B  k
00101100  2C  ,    01001100  4C  L    01101100  6C  l
00101101  2D  -    01001101  4D  M    01101101  6D  m
00101110  2E  .    01001110  4E  N    01101110  6E  n
00101111  2F  /    01001111  4F  O    01101111  6F  o
00110000  30  0    01010000  50  P    01110000  70  p
00110001  31  1    01010001  51  Q    01110001  71  q
00110010  32  2    01010010  52  R    01110010  72  r
00110011  33  3    01010011  53  S    01110011  73  s
00110100  34  4    01010100  54  T    01110100  74  t
00110101  35  5    01010101  55  U    01110101  75  u
00110110  36  6    01010110  56  V    01110110  76  v
00110111  37  7    01010111  57  W    01110111  77  w
00111000  38  8    01011000  58  X    01111000  78  x
00111001  39  9    01011001  59  Y    01111001  79  y
00111010  3A  :    01011010  5A  Z    01111010  7A  z
00111011  3B  ;    01011011  5B  [    01111011  7B  {
00111100  3C  <    01011100  5C  \    01111100  7C  |
00111101  3D  =    01011101  5D  ]    01111101  7D  }
00111110  3E  >    01011110  5E  ^    01111110  7E  ->
00111111  3F  ?    01011111  5F  _    01111111  7F  <-
```

!!! Jeśli trafisz na HD44780 z wewnętrznym romem oznaczonym A02, to do dyspozycji jest aż 240 wbudowanych znaków + 8 własnych - opcja raczej nie spotykana 
z tanich chińskich wyświetlaczach, ale może być dostępna w jakiś z demobilu.

Dodatkowo HD44780 ma wbudowane kolejne 96 znaków, z których większość to chińskie krzaczki ale jest tam też omega (0xF4), pi (0xF7) i kilka innych. 
Oczywiście istnieje też możliwość dodania własnych znaków - w dwóch rozdzielczościach:
- 5x8 (do ośmiu znaków) - w tym przypadku otrzymują one adresy 0x00-0x07 i lustrzane 0x08-0x0F
- 5x10 (do czterech znaków) - otrzymają adresy 0x00, 0x02, 0x04, 0x06 i lustrzane 0x08, 0x0A, 0x0C i 0x0E

Samo zdefiniowanie własnego znaku jest bardzo proste - przykład otwarta kłódka
```
    ***        0b01110 - 0x0E
   *           0b10000 - 0x10
   *           0b10000 - 0x10
   *****       0b11111 - 0x1F
   ** **       0b11011 - 0x18
   ** **       0b11011 - 0x18
   *****       0b11111 - 0x1F
```   

Po dodaniu naszej kłódki, dostaje ona adres 0x00 i taki kod ASCI trzeba by wysłać do wyświetlacza, aby dostała ona wyświetlona. 
Więc aby wyświetlić "Nacisnij @ aby otworzyc" (@ to miejsce naszej klodki), musimy napisać kod:
```c
   char txt[] = "Nacisnij ";
   lcd_str(tab);
   lcd_write_data(0);
   txt[] = " aby otworzyc";
   lcd_str(tab);
```
Trochę to kłopotliwe - dobrze by było móc wpleść własny znak w jakiś string bez takich zabiegów. Nie możemy też użyć
char txt[] = "Nacisnij ""\x0"" aby otworzyc"; bo kod asci 0 jest niedrukowalny. 

Dlatego sprytny (ale kocio opisany) pomysł Mirka polega na znalezieniu ciągu 8 znaków w tych zapisanych w wyświetlaczu, ale zupełnie dla nas zbędnych -
na przykład 0x80-0x87. Zazwyczaj znajdują się tam jakieś krzaczki albo nic (jeśli to oryginalny układ HITACHI). Teraz tylko trzeba sprawić, aby nasz kod, 
po napotkaniu znaku ASCI 128 (0x80), zamiast wysłać ten numer, wysłał 0. 
analogicznie 0x81->0x01, 0x82->0x02 itd

właśnie temu służy tak sprytnie zapisana instrukcja if: (znak>=0x80 && znak<=87) ? (znak & 0x07) : znak - możemy ją wpleść w wywołanie funkcji lcd_write_data, 
zamiast tworzyc osobną zmienną ustawianą w tradycyjnej instrukcji if-else.


## UWAGA

Po kompilacji i zaprogramowaniu, odczyt z pamieci EEPROM moze nie dzialac. 
Jak to poznac?
tekst EEPROM, ktory powinien byc odczytany z pamieci i wyswietlony nie jast, a mapa bajtow, ktora odczytana z EEPROMa powinna stworzyc znak z emotka, jest 
cala "czarna".
Oznacza to, ze zawartosc EEPROMu nie zostala wgrana. Podczas kompilacji w katalogu Release tworzony jest plik .eep, ktory powinien byc zaladowany tak 
samo jak .hex jest
programowany w pamieci FLASH. W tym wypadku zaznaczamy projekt; Menu Project - Properties - AVR - AVRDude - zakladka Flash/EEPROM - i zaznaczamy opcje 
Upload EEPROM image: From build.


# main.c

```c
#include <avr/io.h>
#include <avr/pgmspace.h>             // Modul z funkcjami umozliwiajacymi dostep do danych zapisanych w pamieci FLASH
#include <avr/eeprom.h>               // Podobny modul ale dajacy obsluge danych przechowywanych w pamieci EEPROM
#include <util/delay.h>

#include "LCD/lcd44780.h"             // Plik naglowkowy dolaczjacy dodatkowe funkcje do obslugi wyswietlacza

// Przydatne rozwiazanie od Mirka - bez ponizszej linijki eclipse traktuje zmienne przechowywane w pamieci EEPROM jako bledne
#define EEMEM __attribute__((section(".eeprom")))

const char PROGMEM tab1[] = {"FLASH"};   // zapisanie stringa w pamieci FLASH
      char EEMEM   tab2[] = {"EEPROM"};  // zapisanie stringa w pamieci EEPROM

      uint8_t znak_a[]         = {14,14,4,14,21,4,10,10};   // definicja znaku w pamieci RAM - ludek
      uint8_t znak_b[] EEMEM   = {0,0,10,4,4,17,14,0};      // definicja znaku w pamieci EEPROM - emotka
const uint8_t znak_c[] PROGMEM = {14,16,16,31,27,27,31,0};  // definicja znaku w pamieci FLASH - klodka otw
const uint8_t znak_d[] PROGMEM = {14,17,17,31,27,27,31,0};  // definicja znaku w pamieci FLASH - klodka zam

int main(void)
{

	// kontrola podswietlenia wyswietlacza, jesli nie jest wlaczone/wylaczone na stale
	DDRA  |= (1<<PA7);                     // kontrola podswietlenia ustawiona na pinie A7 - ustaw pin jako wyjscie
	PORTA |= (1<<PA7);                     // podanie stanu wysokiego na pin, aby wlaczyc podswietlenie

	lcd_init();                            // inicjalizacja wyswietlacza - wywolymawa z LCD/lcd44780.c

	// TEST: kontrola migania podswietleniem
	int i=10;
	while(i) {
		PORTA |= (1<<PA7);
		lcd_cls();
		lcd_locate(0,0);
		lcd_int(i);
		_delay_ms(1000);
		PORTA &= ~(1<<PA7);
		_delay_ms(1000);
		i--;
	}

	PORTA |= (1<<PA7);

    // TEST: wyswietlenie stringa zdefiniowanego w pamieci FLASH
	lcd_cls();
	lcd_locate(0,0);
	lcd_str_P(tab1);                       // wyswietla napis z pamieci FLASH
	_delay_ms(2500);

	// TEST: wyswietlenie stringa zdefiniowanego w pamieci EEPROM
	lcd_locate(1,0);
	lcd_str_E(tab2);                       // wyswietla napis z pamieci EEPROM
	_delay_ms(2500);

	// TEST: wyswietlenie stringa zdfioniowanego w pamieci RAM
	lcd_locate(1,10);
	lcd_str("RAM");                     // wyswietla napis z pamieci RAM
	_delay_ms(2500);

	// TEST: wyswietlenie liczby dziesietnej
	lcd_cls();
	i = 2023;
	lcd_locate(0,0);
	lcd_str("ROK (int)");
	lcd_locate(0,10);
	lcd_int(i);
	_delay_ms(2500);

	// TEST: wyswietlenie liczby szestnastkowej
	lcd_cls();
	i = 123;
	lcd_locate(0,0);
	lcd_str("123 (hex)");
	lcd_locate(0,10);
	lcd_hex(i);
	_delay_ms(2500);

	//TEST: zaladowanie tablic definiujacych dodatkowe znaki do roznych obszarow pamieci
	lcd_cls();
	lcd_locate(0,0);
	lcd_str("Programowanie znakow");
	lcd_locate(1,0);
	lcd_str("z RAM, FLASH i EEPROM");
		// wywolanie funkcji programujacych pamiec CGRAM w wyswietlaczu. Pozwala na dodanie do 8 roznych znakow 5x8 pixeli
		lcd_defchar(0x80, znak_a);             // programuje znak z pamieci RAM
		lcd_defchar_E(0x81, znak_b);           // programuje znak z pamieci EEPROM
		lcd_defchar_P(0x82, znak_c);           // progarmuje znak z pamieci FLASH
		lcd_defchar_P(0x83, znak_d);           // programuje znak z pamieci FLASH
	_delay_ms(2500);

	// TEST: wyswietlenie dodatkowych znakow

	// wyswietlanie znakow zaprogramowanych w pamieci CGRAM
    lcd_cls();
    lcd_locate(0,0);
	lcd_str("\x80"" ""\x81");
	lcd_str(" ");
	lcd_str("\x82");
	lcd_str(" ");
	lcd_str("\x83");
	_delay_ms(2500);

	// TEST: wyswietlanie kursora
	lcd_cls();
    lcd_locate(0,0);
	lcd_str("Kursor wlaczony");
	lcd_locate(1,0);
	lcd_cursor_on();
	_delay_ms(2500);

    lcd_locate(0,0);
	lcd_str("Kursor wylaczony");
	lcd_locate(1,0);
	lcd_cursor_off();
	_delay_ms(2500);

    lcd_locate(0,0);
	lcd_str("Kursor mrugajacy  ");
	lcd_locate(1,0);
	lcd_cursor_on();
	lcd_blink_on();
	_delay_ms(10000);
	lcd_cursor_off();

	while(1) {

	// Matrix has you
	// kod jest zupełnie jalowy i napisany tylko i wylacznie aby moc porownac sobie kilka wyswietlaczy
	// i tego, czy maja roznice w czasie odswierzania
	lcd_cls();
	lcd_locate(0,0);
	lcd_str("The Matrix has");
	lcd_locate(1,6);
	lcd_str("you");
	_delay_ms(2000);
	lcd_locate(1,13);
	lcd_str(".");
	_delay_ms(2000);
	lcd_locate(1,14);
	lcd_str(".");
	_delay_ms(2000);
	lcd_locate(1,14);
	lcd_str(".");
	_delay_ms(5000);
	lcd_cls();
	lcd_locate(0,0);
	lcd_str("FOLLOW THE WHITE");
	lcd_locate(1,6);
	lcd_str("RABBIT");
	_delay_ms(5000);
	PORTA &= ~(1<<PA7);
	lcd_cls();
	lcd_locate(0,0);
	_delay_ms(2000);
	lcd_str("KNOCK!");
	PORTA |= (1<<PA7);
	_delay_ms(300);
	PORTA &= ~(1<<PA7);
	lcd_locate(1,7);
	_delay_ms(400);
	lcd_str("KNOCK!");
	PORTA |= (1<<PA7);
	_delay_ms(400);
	PORTA &= ~(1<<PA7);
	lcd_cls();
	_delay_ms(30000);
	PORTA |= (1<<PA7);


	// TEST: Wyswietlenie dostepnych znakow
	i=0;
	while(i<256){
		lcd_cls();
		lcd_locate(0,0);
		lcd_int(i);
		lcd_str(": ");
		lcd_write_data(i);
		_delay_ms(500);
		i++;
	}
	}
}
```

# lcd44780.c
```c
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/eeprom.h>
#include <avr/pgmspace.h>
#include <stdlib.h>              // Jedna ze standardowych bibliotek C z funkcjami do obslugi alokacji pamieci, kontrole procesow,
                                 // czy konwersji np. atoi() - string to integer, int rand(void) - generowanie liczb pseudolosowych
                                 // opis: https://en.wikibooks.org/wiki/C_Programming/stdlib.h
#include <util/delay.h>

#include "lcd44780.h"

// makrodefinicje uzywane do kontroli sygnalow sterujacych

// linia RS kontroluje, jakiego rodzaju transmisja jest wykonywana miedzy mikrokontrolerem, a wyswietlaczem
// mikrokontroler moze wysylac do wyswietlacza komendy; wysylac lub odczytywac dane
#define SET_RS 	PORT(LCD_RSPORT) |= (1<<LCD_RS)			// Stan wysoki - kontrola danych (przesyl znakow)
#define CLR_RS 	PORT(LCD_RSPORT) &= ~(1<<LCD_RS)		// Stan niski -  komendy wyswietlacza

// Linia RW przez wiekszosc czasu ma ustawiony stan niski, czyli komunikacja odbywa sie DO wyswietlacza.
// Ustawienie na niej stanu wysokiego pozwala odczytac zapisanych znakow, albo flagi zajetosci
// Wyswietlacz mozna kontrolowac zupelnie jednostronnie, bez potrzeby odczytu zadnych danych, wiec czesto podlacza sie ja to GND na stale
#define SET_RW 	PORT(LCD_RWPORT) |= (1<<LCD_RW)			// stan wysoki - LCD > kontroler
#define CLR_RW 	PORT(LCD_RWPORT) &= ~(1<<LCD_RW)		// stan niski - kontroler > LCD


// Linia E jest podpieta przez rezystor do GND (domyslny stan niski). Podaje sie na nia krotki impuls wysoki gdy wszystkie pozostale linie
// sa ustawione, aby wymusic na wyswietlaczu ich pobranie (taki ENTER)
#define SET_E 	PORT(LCD_EPORT) |= (1<<LCD_E)			// stan wysoki na linii E - ENTER
#define CLR_E 	PORT(LCD_EPORT) &= ~(1<<LCD_E)			// stan niski na linii E



uint8_t check_BF(void);  // deklaracja funkcji sprawdzajacej stan "Busy Flag" - Flaga jest ustawiana, kiedy wyswietlcz jest gotowy
                         // do przyjecia dalszej transkmisji - pozwala to przyspieszyc komunikacje, ktora nie musi bazowac na
                         // z gory zalozonych timingach - ktore wymakaja uzycia timera, albo wrecz "zawieszenia" mikrokontrolera wieloma
                         // komendami czekania.


// ...:::funkcje kontroli pinow sygnalowych mikrokontrolera:::...

// data_dir_out wymusza ustawienie linii danych (piny D4-D7 na wyswietlaczu) jako wyjsc - wysylanie danych/komend do wyswietlacza
static inline void data_dir_out(void)
{
	DDR(LCD_D7PORT)	|= (1<<LCD_D7);
	DDR(LCD_D6PORT)	|= (1<<LCD_D6);
	DDR(LCD_D5PORT)	|= (1<<LCD_D5);
	DDR(LCD_D4PORT)	|= (1<<LCD_D4);
}

// data_dir_in ustawia linie danych jako wejscia - aby mikrokontroler mogl odczytac dane z wyswietlacza
static inline void data_dir_in(void)
{
	DDR(LCD_D7PORT)	&= ~(1<<LCD_D7);
	DDR(LCD_D6PORT)	&= ~(1<<LCD_D6);
	DDR(LCD_D5PORT)	&= ~(1<<LCD_D5);
	DDR(LCD_D4PORT)	&= ~(1<<LCD_D4);
}

// wyslanie 4 mlodszych bitow z bajdu data. Poniewaz uzywamy tylko 4 linii rownoleglej transmisji, a potrzebujemy wyslac pelen, bajt
// dlatego wysylamy go na "raty" - najpierw cztery najstarsze bity (4-8), nastepnie 4 mlodsze (1-4). Ta funkcja wysyla na raz
// cztery najmlodsze bity, wiec trzeba ja wywolac dwa razy - pierwszy raz z bajtem przesunietym o 4 pozycje w prawo, aby starsze
// bity znalazly sie na miejscu mldszych
// Przyklad
// Bajt do wyslania bajt = 0b1101 1011
// lcd_sendhalf(bajt>>4) - funkcja na wejsciu otrzyma 0b0000 1101 i wysle 1101 <- 4 starsze bity
// lcd_sendhalf(bajt)    - funkcja na wejsciu otrzyma 0b1101 1011 i wysle 1011 <- 4 mlodsze bity
// zobacz kod funkcji _lcd_write_byte

static inline void lcd_sendHalf(uint8_t data)
{
	if (data&(1<<0)) PORT(LCD_D4PORT) |= (1<<LCD_D4); else PORT(LCD_D4PORT) &= ~(1<<LCD_D4);
	if (data&(1<<1)) PORT(LCD_D5PORT) |= (1<<LCD_D5); else PORT(LCD_D5PORT) &= ~(1<<LCD_D5);
	if (data&(1<<2)) PORT(LCD_D6PORT) |= (1<<LCD_D6); else PORT(LCD_D6PORT) &= ~(1<<LCD_D6);
	if (data&(1<<3)) PORT(LCD_D7PORT) |= (1<<LCD_D7); else PORT(LCD_D7PORT) &= ~(1<<LCD_D7);
}

#if USE_RW == 1
// ta funkcja dziala jesli pin RW jest podlaczony do mikrokontrolera (musimy recznie ustawic USE_RW = 1)
// zasada jest udentyczna (choc dziala w przeciwna strone) jak powyzej. Aby odczytac pelny bajt z wyswietlacza, trzeba ja wywolac dwa
// razy, a potem polaczyc zwrocone przez nia dwie polowki 4-ro bitowe. Zobacz kod funkcji _lcd_read_byte
static inline uint8_t lcd_readHalf(void)
{
	uint8_t result=0;

	if(PIN(LCD_D4PORT)&(1<<LCD_D4)) result |= (1<<0);
	if(PIN(LCD_D5PORT)&(1<<LCD_D5)) result |= (1<<1);
	if(PIN(LCD_D6PORT)&(1<<LCD_D6)) result |= (1<<2);
	if(PIN(LCD_D7PORT)&(1<<LCD_D7)) result |= (1<<3);

	return result;
}
#endif

// dzialanie funkcji do wysylania danych do wyswietlacza omowione wyzej w kodzie
void _lcd_write_byte(unsigned char _data)
{
	// Wywolanie funkcji ustawiajacej piny danych jako wyjscia
	data_dir_out();

#if USE_RW == 1
	CLR_RW;
#endif

	SET_E;                              // podanie stanu wysokiego na linii E
	lcd_sendHalf(_data >> 4);			// wyslanie czterech starszych bitow
	CLR_E;                              // podanie stanu niskiego na linii E

	SET_E;
	lcd_sendHalf(_data);				// wyslanie czterech mlodszych bitow
	CLR_E;


// Petla ponizej dziala jesli chcemy uzyc linii RW do sprawdzania Busy Flag. Pozwala to na wysylanie nastepnego polecenia/nastepnej
// paczki bitow tak szybko, jak szybko wyswietlacz jest gotowy ro odczytu zamiast czekac z gory zalozony czas.

// !!! Zamiast uzywac standardowej komendy if, ktora baylaby sprawdzana za kazdym razem podczas pracy, wykorzystujemy delkaracje #if
// preprocesor, przed kompilacja na podstawie zadeklarowanej zmiennej USE_RWwybierze z ponizszego kodu ALBO petle ALBO opoznienie
// 120 ms i tylko jedna mozliwosc zostanie skompilowana do kodu wynikowego.
#if USE_RW == 1
	while( (check_BF() & (1<<7)) );
#else
	_delay_us(120);
#endif

}


// Podobnie jak powyzej - funkcja _lcd_read_byte zostanie dolaczona do kompilacji tylko jesli zmienna USE_BF == 1. Inaczej zostanie
// zupelnie pominieta.
#if USE_RW == 1
uint8_t _lcd_read_byte(void)
{
	uint8_t result=0;
	data_dir_in();

	SET_RW;                          // ustawienie stanu wysokiego na linii RW oznaczajace odczyt z wyswietlacza

	SET_E;
	result = (lcd_readHalf() << 4);  // odczyt starszej czesci bajtu i wpisanie jej jako bitow 5-8 zmiennej result
	CLR_E;
                    // tu nastepuje krotki sygnal 0 na linii E, co oznacza dla wyswietlacza, zeby na piny danych podac nastepne (mlodsze)
	                // 4 bity
	SET_E;
	result |= lcd_readHalf();       // odczyt mlodszej czesci bajtu i dodanie jej jako bity 1-4 zmiennej result
	CLR_E;

	return result;
}
#endif

// Funkcja sprawdzajaca, czy wyswietlacz ustawil Busy Flag oznaczjaca gotowosc do dalszej komunikacji
// Scisle cytujac note katalogowa HD44780U - Kiedy linia RS ma ustawiony stan niski, a linia RW stan wysoki, pin DB7
// wyswietlacza (najstarszy) jest uzywany przez wyswietlacz to komunikacji przyjecia nastepnej instrukcji. Moze ona zostac wyslana
// dopiero, kiedy pin ten bedzie mial stan niski.
#if USE_RW == 1
uint8_t check_BF(void)
{
	CLR_RS;                         // ustawienie stanu niskiego na linii RS oznaczajace przychodzaca komende dla wyswietlacza
	return _lcd_read_byte();
}
#endif


// funkcja wysylajaca komende - wykorzystuje zdefiniowana wczesniej funkcje wysylania danych ale dodatkowo usawia stan niski
// na linii RS oznaczajacy wysylana komende
void lcd_write_cmd(uint8_t cmd)
{
	CLR_RS;
	_lcd_write_byte(cmd);
}

// identyczna funkcja jak ponizej ale na linii RS ustawiany jest stan wysoki oznaczajacy przychodzace dane
void lcd_write_data(uint8_t data)
{
	SET_RS;
	_lcd_write_byte(data);
}


// _____________________________________________________________________________________________________
// ponizej dodatkowe funkcje, ktore beda wykorzystywane "na zewnatrz" tego modulu (np. w funkcji main())

// Opis ponizszej funcji (berdziej jej idei, niz kodu) w ksiazce jest dla mnie "koci", jakies malowanie znakow... nie wazne
// Opis dzialania znajduje sie powyzej z czesci informacyjmej na temat HD44780
#if USE_LCD_CHAR == 1
void lcd_char(char c)
{
	lcd_write_data( ( c>=0x80 && c<=0x87 ) ? (c & 0x07) : c);
}
#endif

// ta funkcja wysyla string wczesniej zapisany w pamieci RAM - normalna zmienna
void lcd_str(char * str)
{
	register char znak;
	while ( (znak=*(str++)) ) lcd_char( znak );
}

// ta funkcja umozliwia wyslanie stringa wczesniej zapisanego w pamieci FLASH - czyli moze byc uzyta do dluzszych tekstow, ktore
// nie sa zmieniane
#if USE_LCD_STR_P == 1
void lcd_str_P(const char * str)
{
	register char znak;
	while ( (znak=pgm_read_byte(str++)) ) lcd_char( znak );
}
#endif

// ta funkcja umozliwia wyslanie stringa zapisanego wczesniej w pamieci EEPROM - na przyklad Imienia, ktore nie zostanie ustracone
// w momencie wylaczenia zasilania.
#if USE_LCD_STR_E == 1
void lcd_str_E(char * str)
{
	register char znak;
	while(1)
	{
		znak=eeprom_read_byte( (uint8_t *)(str++) );
		if(!znak || znak==0xFF) break;
		else lcd_char( znak );
	}
}
#endif

// funkcja sluzaca do wyswieltania liczb dziesietnych na podstawie zmiennej int
#if USE_LCD_INT == 1
void lcd_int(int val)
{
	char bufor[17];
	lcd_str( itoa(val, bufor, 10) );
}
#endif

// funkcja sluzaca do wyswietlania liczb szestnastkowych
#if USE_LCD_HEX == 1
void lcd_hex(uint32_t val)
{
	char bufor[17];
	lcd_str( ltoa(val, bufor, 16) );
}
#endif

// ta funkcja definiue wlasny znak z pamieci RAM
// nr - to kod znaku ktory definiujemy (0-7)
// def_znak - wskaznik tablicy zawierajacej siedem bajtow definiujacych znak
#if USE_LCD_DEFCHAR == 1
void lcd_defchar(uint8_t nr, uint8_t *def_znak)
{
	register uint8_t i,c;
	lcd_write_cmd( 64+((nr&0x07)*8) );
	for(i=0;i<8;i++)
	{
		c = *(def_znak++);
		lcd_write_data(c);
	}
}
#endif

// funkcja podobna do lcd_defchar, ale tablica zawierajaca definisje znaku znajduje sie w pamieci FLASH
// moze byc uzyta do wgrania znakow, ktore zawsze beda programowane w wyswietlaczu po starcie, a nie beda zmieniane
#if USE_LCD_DEFCHAR_P == 1
void lcd_defchar_P(uint8_t nr, const uint8_t *def_znak)
{
	register uint8_t i,c;
	lcd_write_cmd( 64+((nr&0x07)*8) );
	for(i=0;i<8;i++)
	{
		c = pgm_read_byte(def_znak++);
		lcd_write_data(c);
	}
}
#endif

// trzecia analogiczna funkcja do definicji wlasnych znakow ale z tablicy w pamieci EEPROM - daje to mozliwosc
// podmiany predefiniowanych znakow bez koniecznosci rekompilacji i programowania calego ukladu.
// bardzo pomocne przy obsludze wyswietlaczy graficznych umozliwic np wgranie loga producenta
#if USE_LCD_DEFCHAR_E == 1
void lcd_defchar_E(uint8_t nr, uint8_t *def_znak)
{
	register uint8_t i,c;

	lcd_write_cmd( 64+((nr&0x07)*8) );
	for(i=0;i<8;i++)
	{
		c = eeprom_read_byte(def_znak++);
		lcd_write_data(c);
	}
}
#endif

// funkcja ustawia kursor w zadanej pozycji Y (wiersz), X (kolumna)
#if USE_LCD_LOCATE == 1
void lcd_locate(uint8_t y, uint8_t x)
{
	switch(y)
	{
		case 0: y = LCD_LINE1; break;

#if (LCD_ROWS>1)
	    case 1: y = LCD_LINE2; break; // przeliczenie adresow dla wyswietlczy dwu wierszowych
#endif
#if (LCD_ROWS>2)
    	case 2: y = LCD_LINE3; break; // przeliczenie adresow dla wyswietlczy trzy wierszowych
#endif
#if (LCD_ROWS>3)
    	case 3: y = LCD_LINE4; break; // przeliczenie adresow dla wyswietlczy cztero wierszowych
#endif
	}

	lcd_write_cmd( (0x80 + y + x) );
}
#endif


// funkcja czyszczaca ekran wyswietlacza
void lcd_cls(void)
{
	lcd_write_cmd( LCDC_CLS );

	#if USE_RW == 0
		_delay_ms(4.9);
	#endif
}


// funkcja ustawiajaca kursor w pozycji 0,0
#if USE_LCD_CURSOR_HOME == 1
void lcd_home(void)
{
	lcd_write_cmd( LCDC_CLS|LCDC_HOME );

	#if USE_RW == 0
		_delay_ms(4.9);
	#endif
}
#endif


// funkcje wlaczajace i wylaczajace widocznosc kursora
#if USE_LCD_CURSOR_ON == 1
void lcd_cursor_on(void)
{
	lcd_write_cmd( LCDC_ONOFF|LCDC_DISPLAYON|LCDC_CURSORON);
}

void lcd_cursor_off(void)
{
	lcd_write_cmd( LCDC_ONOFF|LCDC_DISPLAYON);
}
#endif


// funkcje wlaczajace i wylaczajace miganie kursora
#if USE_LCD_CURSOR_BLINK == 1
void lcd_blink_on(void)
{
	lcd_write_cmd( LCDC_ONOFF|LCDC_DISPLAYON|LCDC_CURSORON|LCDC_BLINKON);
}

void lcd_blink_off(void)
{
	lcd_write_cmd( LCDC_ONOFF|LCDC_DISPLAYON);
}
#endif



// *** funkcja inicjucaca wyswietlacz po wlaczeniu zasilania ***
void lcd_init(void)
{
	// inicjowanie pinow portow ustalonych do podlaczenia z wyswietlaczem LCD
	// ustawienie wszystkich jako wyjscia
	data_dir_out();                       // ustawienie pinow danych jako wyjscia
	DDR(LCD_RSPORT) |= (1<<LCD_RS);       // ustawienie pinu RS jako wyjscia
	DDR(LCD_EPORT) |= (1<<LCD_E);         // ustawienie pinu E jako wyjscia
	#if USE_RW == 1
		DDR(LCD_RWPORT) |= (1<<LCD_RW);   // usatwienie pinu RW jako wyjscia (jesli jest uzywany)
	#endif

	PORT(LCD_RSPORT) |= (1<<LCD_RS);      // Stan wysoki na pinie RS
	PORT(LCD_EPORT) |= (1<<LCD_E);        // Stan wysoki na pinie E
	#if USE_RW == 1
		PORT(LCD_RWPORT) |= (1<<LCD_RW);  // Stan wysoki na pinie RW (jesli jest uzywany)
	#endif

	_delay_ms(15);                        // Ustawia stany niskie na pinach kontrolnych
	PORT(LCD_EPORT) &= ~(1<<LCD_E);
	PORT(LCD_RSPORT) &= ~(1<<LCD_RS);
	#if USE_RW == 1
    	PORT(LCD_RWPORT) &= ~(1<<LCD_RW);
	#endif

    	// Zgodnie z nota ukladu HD44780, po jego wlaczeniu, wymaga on inicjalizacji - wyslania serii danych, ktore ustawia go
    	// w tryb 4-ro bitowy. Wyslanie pierwszych czterech polowek bajtu wydaje sie strasznie amatorskie. Poniewaz w czasie ich
    	// wysylania nie mozna odczytac BusyFlag, nie mozna tez uzyc duzo lepszych funkcji zdefiniowanych wyzej.

    	// POWER ON
    	// wait >15ms
    	// send           RS  RW  DB7  DB6  DB5  DB4
    	//                0   0    0    0    1    1
        // wait >4.1ms
    	// send           0   0    0    0    1    1
    	// wait 100us
    	// send           0   0    0    0    1    1
    	// send           0   0    0    0    1    0
    	//                                               dopiero teraz mozna zaczac sprawdzac BF
    	// send           0   0    0    0    1    0
    	// send           0   0    N    F    *    *      N:1 - dwa wiersze; 0 - jeden wiersz  F: 1 - 5x10; 0 - 5x8
    	// send           0   0    0    0    0    0
    	// send           0   0    1    0    0    0
    	// send           0   0    0    0    0    0
    	// send           0   0    0    0    0    1
    	// send           0   0    0    0    0    0
    	// send           0   0    0    1   I/D   S
    	// Koniec inicjalizacji

	                                       // To jest procedura ustawiajaca 44780 w tryb 4ro bitowy
	SET_E;
	lcd_sendHalf(0x03);	                   // tryb 8-bitowy
	CLR_E;
	_delay_ms(4.1);

	SET_E;
	lcd_sendHalf(0x03);	                   // tryb 8-bitowy
	CLR_E;
	_delay_us(100);

	SET_E;
	lcd_sendHalf(0x03);	                   // tryb 8-bitowy
	CLR_E;
	_delay_us(100);

	SET_E;
	lcd_sendHalf(0x02);                    // tryb 4-bitowy
	CLR_E;
	_delay_us(100);

	// juz mozna uzywac Busy Flag
	// tryb 4-bitowy, 2 wiersze, znak 5x7
	lcd_write_cmd( LCDC_FUNC|LCDC_FUNC4B|LCDC_FUNC2L|LCDC_FUNC5x7 );
	// wylaczenie kursora
	lcd_write_cmd( LCDC_ONOFF|LCDC_CURSOROFF );
	// wlaczenie wyswietlacza
	lcd_write_cmd( LCDC_ONOFF|LCDC_DISPLAYON );
	// przesuwanie kursora w prawo bez przesuwania zawartosci ekranu
	lcd_write_cmd( LCDC_ENTRY|LCDC_ENTRYR );

	// kasowanie ekranu
	lcd_cls();
}
```

# lcd44780.h
```c
#ifndef LCD_H_
#define LCD_H_


// Ponizej nalezy zdefiniowac parametry i sposob pracy podlaczonego wyswietlacza:

#define LCD_ROWS 2        // Ilosc wierszy
#define LCD_COLS 16       // Ilosc kolumn

#define USE_RW 1           // 0: brak kontroli pinu RW; wylaczenie sprawdzania Busy Flag; pin na stale sciagniety do GND
                           // 1: linia RW jest kontrolowana przez mikrokontroler

#define LCD_D7PORT  A      // ustawienie portow danych
#define LCD_D7 6           //  |
#define LCD_D6PORT  A      //  |
#define LCD_D6 5           //  |
#define LCD_D5PORT  A      //  |
#define LCD_D5 4           //  |
#define LCD_D4PORT  A      //  |
#define LCD_D4 3           //  |

#define LCD_RSPORT  A      // ustawienie linii kontrolnych
#define LCD_RS 0           //  |
#define LCD_RWPORT  A      //  |  Linia RW moze byc pominieta, jesli jej kontrola zostala wylaczona powyzej
#define LCD_RW 1           //  |
#define LCD_EPORT   A      //  |
#define LCD_E  2           //  |

// _____________________________________________________________________________________________________________________________
// Tutaj istnieje mozliwosc wlaczenia lub wylaczenia poszczegolnych funkcji. Pozwala to zmniejszyc rozmiar wyjsciowy, jesli nie
// wszystkie sa koneczne do projektowanego rozwiazania

// 1: wlacza funkcjie  | 0: wylacza funkcje

#define USE_LCD_LOCATE          1   // ustawia kursor na wybranej pozycji Y,X (Y=0-3, X=0-n)
#define USE_LCD_CHAR            1   // wysyla pojedynczy znak jako argument funkcji
#define USE_LCD_STR_P           1   // wysyla string umieszczony w pamieci FLASH
#define USE_LCD_STR_E           1   // wysyla string umieszczony w pamieci FLASH
#define USE_LCD_INT             1   // wyswietla liczbe dziesietna (int) na LCD
#define USE_LCD_HEX             1   // wyswietla liczbe szesnastkowa na LCD
#define USE_LCD_DEFCHAR         1   // wysyla zdefiniowany znak z pamieci RAM
#define USE_LCD_DEFCHAR_P       1   // wysyla zdefiniowany znak z pamieci FLASH
#define USE_LCD_DEFCHAR_E       1   // wysyla zdefiniowany znak z pamieci EEPROM
#define USE_LCD_CURSOR_ON       1   // obsluga wlaczania/wylaczania kursora
#define USE_LCD_CURSOR_BLINK 	1   // obsluga wlaczania/wylaczania migania kursora
#define USE_LCD_CURSOR_HOME 	1   // ustawia kursor na pozycji poczatkowej
// _____________________________________________________________________________________________________________________________
// Definicje adresow DDRAM zaleznie od rozmiaru wyswietlacza:

#if ( (LCD_ROWS == 2) && (LCD_COLS == 40) )
#define LCD_LINE1 0x00
#define LCD_LINE2 0x40
#endif

#if ( (LCD_ROWS == 4) && (LCD_COLS == 20) )
#define LCD_LINE1 0x00
#define LCD_LINE2 0x40
#define LCD_LINE3 0x14
#define LCD_LINE4 0x54
#endif

#if ( (LCD_ROWS == 2) && (LCD_COLS == 20) )
#define LCD_LINE1 0x00
#define LCD_LINE2 0x40
#endif

#if ( (LCD_ROWS == 2) && (LCD_COLS == 16) )
#define LCD_LINE1 0x00
#define LCD_LINE2 0x40
#endif

#if ( (LCD_ROWS == 4) && (LCD_COLS == 16) )
#define LCD_LINE1 0x00
#define LCD_LINE2 0x40
#define LCD_LINE3 0x10
#define LCD_LINE4 0x50
#endif


// Makra upraszczajace
#define PORT(x) SPORT(x)
#define SPORT(x) (PORT##x)
#define PIN(x) SPIN(x)
#define SPIN(x) (PIN##x)
#define DDR(x) SDDR(x)
#define SDDR(x) (DDR##x)


// Predefiniowane komendy sterujace wyswietlaczem
#define LCDC_CLS                        0x01
#define LCDC_HOME                       0x02
#define LCDC_ENTRY                      0x04
	#define LCDC_ENTRYR             0x02
	#define LCDC_ENTRYL             0
	#define LCDC_MOVE               0x01
#define LCDC_ONOFF                      0x08
	#define LCDC_DISPLAYON          0x04
	#define LCDC_CURSORON           0x02
	#define LCDC_CURSOROFF          0
	#define LCDC_BLINKON            0x01
#define LCDC_SHIFT                      0x10
	#define LCDC_SHIFTDISP          0x08
	#define LCDC_SHIFTR             0x04
	#define LCDC_SHIFTL             0
#define LCDC_FUNC                       0x20
	#define LCDC_FUNC8B             0x10
	#define LCDC_FUNC4B             0
	#define LCDC_FUNC2L             0x08
	#define LCDC_FUNC1L             0
	#define LCDC_FUNC5x10           0x04
	#define LCDC_FUNC5x7            0
#define LCDC_SET_CGRAM                  0x40
#define LCDC_SET_DDRAM                  0x80

// Deklaracje funkcji, ktore beda dostepne w innych modulach
void lcd_init(void);                                       // inicjalizacja wyswietlacza        - zawsze wlaczona
void lcd_cls(void);                                        // wyczyszczenie wyswietlacza        - zawsze wlaczona
void lcd_str(char * str);                                  // wyswietlenie stringa              - zawsze wlaczona
void lcd_locate(uint8_t y, uint8_t x);                     // ustawienie kursora na poz y,x     - zawsze wlaczona
void lcd_char(char c);                                     // wyswietlenie pojedyn znaku        - zawsze wlaczona
void lcd_write_data(uint8_t data);                         // wyswietla znak z komorki CGROM    - zawsze wlaczona
void lcd_str_P(const char * str);                          // wyswietlenie znaku z FLASH        - ON/OFF
void lcd_str_E(char * str);                                // wyswietlenie znaku z EEPROM       - ON/OFF
void lcd_int(int val);                                     // wyswietlenie liczby ze zm init    - ON/OFF
void lcd_hex(uint32_t val);                                // wyswietlenie liczby hex           - ON/OFF
void lcd_defchar(uint8_t nr, uint8_t *def_znak);           // definicja wlasnego znaku          - ON/OFF
void lcd_defchar_P(uint8_t nr, const uint8_t *def_znak);   // definicja wlaznego znaku z FLASH  - ON/OFF
void lcd_defchar_E(uint8_t nr, uint8_t *def_znak);         // definicja wlasnego znaku z EEPROM - ON/OFF
void lcd_home(void);                                       // ust kursora na poz 0,0            - ON/OFF
void lcd_cursor_on(void);                                  // wyswietlenie kursora              - ON/OFF
void lcd_cursor_off(void);                                 // ukrycie kursora                   - ON/OFF
void lcd_blink_on(void);                                   // wlaczenie migania kursora         - ON/OFF
void lcd_blink_off(void);                                  // wylaczenie migania kursora        - ON/OFF
#endif 
```
