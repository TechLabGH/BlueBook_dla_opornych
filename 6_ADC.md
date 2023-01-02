#### Przykładowa charakterystyka przetwornika ADC w ATmega32:
 - Rozdzielczość 10-bitów
 - Nieliniowość całkowa na poziomie 0,5 LSB
 - Całkowita dokładność ± 2 najmłodsze bity
 - Czas przetwarzania 13 - 260 μs.
 - 15 tysięcy próbek na sekundę przy pełnej rozdzielczości
 - 8 multipleksowanych nieróżnicowych kanałów wejściowych
 - 7 multipleksowanych różnicowych kanałów wejściowych
 - 2 różnicowe kanały wejściowe z opcjonalnym wzmocnieniem 10x i 200x
 - Opcjonalna korekcja lewostronna dla odczytu wyniku przetwarzania
 - Zakres napięcia wejściowego: 0 – VCC
 - Wybieralne napięcie odniesienia 2,56 V
 - Tryb przetwarzania ciągłego lub pojedynczego
 - Rozpoczynanie przetwarzania przez samowyzwalanie ze źródeł przerwań
 - Przerwanie przy zakończeniu przetwarzania
 - Układ zmniejszania szumu w trybie uśpienia

<img src="https://eduinf.waw.pl/inf/prg/009_kurs_avr/images_u2/4349.p3.gif">

Mikrokontroler ATmega32 udostępnia 10-bitowy kompensacyjny przetwornik analogowo/cyfrowy. Przetwornik połączony jest do 8-kanałowego multipleksera analogowego, który pozwala na wprowadzenie ośmiu nieróżnicowych napięć pobieranych z końcówek portu A. Wejścia napięć nieróżnicowych odnoszą się do 0V **(GND)**.

Mikrokontroler wspiera również 16 kombinacji napięć różnicowych. Dwa z wejść różnicowych **(ADC1, ADC0 i ADC3, ADC2)** jest wyposażone w programowany stopień wzmacniający, który dostarcza stopnie wzmocnienia 0dB **(1x)**, 20 dB **(10x)** i 46dB **(200x)** wejściowego napięcia różnicowego przed konwersją analogowo/cyfrową. Siedem różnicowych wejść analogowych współdzieli wspólne wejście odwracające **(ADC1)**, a każde inne wejście przetwornika można wybrać na wejście nieodwracające. Jeśli używane jest wzmocnienie 1x lub 10x, to można oczekiwać rozdzielczości 8 bitów. Jeśli używane jest wzmocnienie 200x, to można oczekiwać rozdzielczości 7 bitów.

Przetwornik A/C posiada oddzielną końcówkę analogowego napięcia zasilania, AVCC. Napięcie to nie powinno się różnić więcej niż ±0.3V od VCC. 

Wewnętrznie dostępne jest napięcie odniesienia o wartości znamionowej 2,56V lub AVCC.

Przetwornik analogowo/cyfrowy zamienia analogowe napięcie wejściowe na 10-bitową wartość za pomocą kolejnych przybliżeń. Wartość minimalna reprezentuje **GND**, a wartość maksymalna reprezentuje napięcie na końcówce **AREF** minus 1 LSB (najmłodszy bit). Opcjonalnie do końcówki AREF można podłączyć AVCC lub wewnętrzne napięcie odniesienia 2,56V przez zapis bitów **REFSn** w rejestrze **ADMUX**. W ten sposób wewnętrzne napięcie odniesienia można odsprzęgnąć zewnętrznym kondensatorem podłączonym do końcówki AREF, co polepszy odporność na zakłócenia.

<img src="https://eduinf.waw.pl/inf/prg/009_kurs_avr/images_u2/4379.p1.gif">

Całą przetłumaczoną notę katalogową można znaleźć [tutaj](https://eduinf.waw.pl/inf/prg/009_kurs_avr/4379.php).

## Ops rejestrów

#### ADMUX – ADC Rejest wyboru multipleksera
  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0
:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- 
REFS1|REFS0|ADLAR|MUX4 |MUX3 |MUX2 |MUX1 |MUX0
 R/W | R/W | R/W | R/W | R/W | R/W | R/W | R/W 

* Bit 7:6 - wybór napięcia referencyjnego

|REFS1 | REFS0 |                                |
|------|-------|--------------------------------|
|0     |0      |AREF, Wewnętrzny Vref wyłączony |
|0     |1      |AVCC                            |
|1     |0      | ---                            |
|1     |1      |Wewnętrzny 2,56V                |

* Bit 5 - ADLAR - Wyrównanie wyniku zapisanego w rejestrze danych:
    * 1: wyrównanie do lewej
    * 2: wyrównanie do prawej

* Bity 4:0 - wybór kanału i wzmocnienia

| MUX4:0 | Wejście | Wejście nieodwracające | Wejście odwracające | Wzmocnienie|
|--------|---------|------------------------|---------------------|------------|
|00000   |ADC0     |---                     |---                  |---         |
|00001   |ADC1     |---                     |---                  |---         |
|00010   |ADC2     |---                     |---                  |---         |
|00011   |ADC3     |---                     |---                  |---         |
|00100   |ADC4     |---                     |---                  |---         |
|00101   |ADC5     |---                     |---                  |---         |
|00110   |ADC6     |---                     |---                  |---         |
|00111   |ADC7     |---                     |---                  |---         |
|01000   |---      |ADC0                    |ADC0                 |10x         |
|01001   |---      |ADC1                    |ADC0                 |10x         |
|01010   |---      |ADC0                    |ADC0                 |200x        |
|01011   |---      |ADC1                    |ADC0                 |200x        |
|01100   |---      |ADC2                    |ADC0                 |10x         |
|01101   |---      |ADC3                    |ADC0                 |10x         |
|01110   |---      |ADC1                    |ADC0                 |200x        |
|01111   |---      |ADC3                    |ADC0                 |200x        |
|10000   |---      |ADC0                    |ADC0                 |1x          |
|10001   |---      |ADC1                    |ADC0                 |1x          |
|10010   |---      |ADC2                    |ADC0                 |1x          |
|10011   |---      |ADC3                    |ADC0                 |1x          |
|10100   |---      |ADC4                    |ADC0                 |1x          |
|10101   |---      |ADC5                    |ADC0                 |1x          |
|10110   |---      |ADC6                    |ADC0                 |1x          |
|10111   |---      |ADC7                    |ADC0                 |1x          |
|11000   |---      |ADC0                    |ADC0                 |1x          |
|11001   |---      |ADC1                    |ADC0                 |1x          |
|11010   |---      |ADC2                    |ADC0                 |1x          |
|11011   |---      |ADC3                    |ADC0                 |1x          |
|11100   |---      |ADC4                    |ADC0                 |200x        |
|11101   |---      |ADC5                    |ADC0                 |200x        |
|11110   |1.22V    |---                     |---                  |---         |
|11111   |0V GND   |---                     |---                  |---         |

#### ADCSRA – ADC Rejestr A kontroli i statusu
  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0
:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- 
ADEN |ADSC |ADATE|ADIF |ADIE |ADPS2|ADPS1|ADPS0
 R/W | R/W | R/W | R/W | R/W | R/W | R/W | R/W 

* Bit 7 - ADEN - (ADC Enable) Ustawienie tego bitu na jeden włącza przetwornik ADC mikrokontrolera. Ustawienie tego bitu na zero wyłącza przetwornik ADC mikrokontrolera. Jeśli konwersja jest w trakcie zostaje ona przerwana.

* Bit 6 - ADSC - (ADC Start Conversion) W trybie pojedynczego pomiaru ustawienie tego bitu na jeden startuje pojedyncze przetwarzanie ADC mikrokontrolera. W trybie ciągłego przetwarzania (Free Runing mode) ustawienie tego bitu na jeden startuje pierwsze przetwarzanie po tym jak zostanie włączony bitem ADEN. Pierwsze przetwarzanie przetwornika z inicjalizacją trwa 25 cykli kolejne trwają 13 cykli. Bit ten jest równy jeden tak długo jak trwa konwersja. Po skończonej konwersji przez mikrokontroler bit ten zostaje wyzerowany. Wpisanie w ten bit zera nic nie powoduje.

* Bit 5 - ADATE - (ADC Auto Trigger Enable) Jeśli bit ten zostanie ustawiony na jedynkę zostanie włączone automatyczne wyzwalanie przetwornika ADC mikrokontrolera. Źródło sygnału taktującego przetwornik ADC mikrokontrolera można wybrać za pomocą bitów ADTS w rejestrze ADCSRB mikrokontrolera.

* Bit 4 - ADIF - (ADC Interrupt Flag) Jest to flaga przerwania od przetwornika ADC mikrokontrolera. Gdy zakończone zostanie przetwarzanie przez przetwornik ADC mikrokontrolera flaga ta zostaje ustawiona na jedynkę jednocześnie wyzwalając przerwanie obsługi przetwornika ADC mikrokontrolera. Flaga jest zerowana sprzętowo po wykonaniu przerwania obsługi przetwornika ADC mikrokontrolera.

* Bit 3 - ADIE - (ADC Interrupt Enable) Gdy bit ten jest ustawiony na jedynkę aktywuje możliwość generowania przerwania obsługi przetwornika ADC mikrokontrolera.

* Bity 2:0 - ADPSx - Preskaler przetwornika ADC

| ADPS2 | ADPS1 | ADPS0 | Preskaler |
| :---: | :---: | :---: | :---: |
|   0   |   0   |   0   |   2   |
|   0   |   0   |   1   |   2   |
|   0   |   1   |   0   |   4   |
|   0   |   1   |   1   |   8   |
|   1   |   0   |   0   |   16  |
|   1   |   0   |   1   |   32  |
|   1   |   1   |   0   |   64  |
|   1   |   1   |   1   |   128 |

#### ADCL - ADCH – Rejestry danych przetwornika

###### ADLAR = 0

  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0
:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- 
| |     |     |     |     |     |ADC9 |ADC8
ADC7 |ADC6 |ADC5 |ADC4 |ADC3 |ADC2 |ADC1 |ADC0

###### ADLAR = 1

  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0
:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- 
ADC9 |ADC8 |ADC7 |ADC6 |ADC5 |ADC4 |ADC3 |ADC2
ADC1 |ADC0 |  |  |  |  |  | 

#### SFIOR - Rejestr funkcji specjalnych

  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0
:--- |:--- |:--- |:--- |:--- |:--- |:--- |:--- 
ADTS2|ADTS1|ADTS0| - |ACME|PUD|PSR2|PSR10
 R/W | R/W | R/W | R/W | R/W | R/W | R/W | R/W 

* Bit 7:5 - Źródło autowyzwalania

* Bit 3 - ACME - jeśli ten bit jest ustawiony na jeden i przetwornik ADC jest wyłączony (ADEN i ADCSRA jest zerem) multiplexer wejść ADC przyłączony jest do wejścia odwracającego komparatora analogowego. Jeśli bit ten jest równy zero nóżka AIN1 jest bezwarunkowo podpięta do wejścia odwracającego komparatora analogowego.

| ADTS2 | ADTS1 | ADTS0 | Wyzwalanie przez |
| :---: | :---: | :---: | :---: |
|   0   |   0   |   0   |Pomiar ciągły|
|   0   |   0   |   1   |Analog Comparator|
|   0   |   1   |   0   |External Interrupt Request 0|
|   0   |   1   |   1   |Timer/Counter0 Compare Match|
|   1   |   0   |   0   |Timer/Counter0 Overflow|
|   1   |   0   |   1   |Timer/Counter1 Compare Match B|
|   1   |   1   |   0   |Timer/Counter1 Overflow|
|   1   |   1   |   1   |Timer/Counter1 Capture Event|

## Przykład 0

_UWAGA Kod zamieszczony w książce nie działa._

```c
#include <avr/io.h>
#include <avr/delay.h>

#include "LCD/lcd44780.h"              // do wyświetlania wyniku używam LCD (kod bibliotrki w przykładach z wyświtlaczem)

uint16_t pomiar(uint8_t kanal);        // deklaracja funkcji uruchamiającej i odczytującej pomiar z ADC

int main (void){

	lcd_init();
//	ADMUX  |= ( 1<<REFS0 );                            // podłączenie wewnętrznego napięcia referencyjnego VCC
    ADMUX  |= ( 1<<REFS0 )|( 1<<REFS1 );               // podłączenie wewnętrznego napięcia referencyjnego 2.56V
	ADCSRA |= ( 1<<ADEN  )|                            // Włączenie przetwornika
              ( 1<<ADPS2 )|( 1<<ADPS1 )|( 1<<ADPS0 );  // Ustawienie preskalera 128 (Atmega z 20MHz kwarcem)

	while(1){                          // pętla programu
		lcd_cls();                     // czyszczenie ekranu
		lcd_int( pomiar(7) );          // wywołanie funkcji pomiarowej, która będzie badać pin 7 wyświetlenie zwróconej z niej wartości odczytanej z ADC
		_delay_ms( 1000 );             // pomiar wykonywany so 1 sek

	}
}

uint16_t pomiar( uint8_t kanal ){      // funkcja dokonująca pomiaru
	ADMUX |= ( ADMUX & 0xE0 ) | kanal; // Ustawia rejestr ADMUX:
                                       // 0xE0 -> 11100000: 
                                       // Bit 7:6 (REFS1:0) = 11 <- ustawienie wewnętrznego napięcia referencyjnego 2.56V
                                       // Bit 5 - ADLAR = 1 <- wyrównanie do lewej
                                       // "| kanal" dodatkowo ustawia Bity 4:0 (MUX4:0) wskazując, że pomiar ma być wykonany na pinie 7
//  ADMUX |= ( ADMUX & 0x60 ) | kanal; // Ustawi napięcie referencyjne VCC

    ADCSRA |= ( 1<<ADSC );             // rozpoczęcie pomiaru
	while( (ADCSRA & (1<<ADSC)) );     // Oczekiwanie na zakończenie pomiaru (ustawienie pinu ADSC = 0)
	return ADCW;                       // funkcja zwraca wartość int orczytaną z rejestrów ADCL i ADCH
}
```
Niezależnie od wybranego napięcia referencyjnego, podłączenie piny PA7 do AREF powinno dać wynik 1023, a pogłączenie go do GNW, wynik 0.
## Trochę matematyki
Warto teraz wykonać pomiary rzeczywistego napięcia na pinie AREF dla obu napięć referencyjnych:
 - AVCC - 4.912
 - 2.56 - 2.589

Dla każdego "stopnia" 10-cio bitowego wyniku otrzymanego z ADC, napięcie będzie wynosić
 - AVCC - 4.895 / 1024 = 0.00478V
 - 2.56 - 2,589 / 1024 = 0.00253V

Pierwszą rzeczą, jaką należy uwzględnić, jest maksymalne napięcie, jakie potrzebujemy zmierzyć - powiedzmy, że będzie to 14V (Jakiś akumulator uwzględniając jego wyższe napięcie ładowania).

Podłączenie 14v do mikrokontrolera spowoduje jego uszkodzenie, więc należy je przepuścić przez dzielnik napięcia. Zobacz skrypt [dzielnik.py] pomagający w dobraniu rezystorów do zadanych napięć wejściowych i wyjściowych. Daje on dodatkowo możliwość wyboru szeregu rezystancji i wymuszenia jednego z rezystorów.

Poniżej przykład działania skryptu
```
Skrypt oblicza najlepsza pare rezystorow ktore mozna wybrac z zadanego szeregu, aby napiecie wyjsciowe dzielnika bylo jak najbardziej zblizone do zadanego

   ------------               
   |          |               
   |         ---              
   |         | | R1           
   |         | |              
   |         ---              
   |          |               
   Vin        *---------      
   |          |        |      
   |         ---       |      
   |         | | R2    Vout   
   |         | |       |      
   |         ---       |      
   |          |        |      
   -----------*---------      

podaj napiecie WEJsciowe Vin: 14
podaj napiecie WYJsiowe Vout: 4.5
Wybierz szereg E3/E6/E12/E24/E48/E96   
wciśnij ENTER aby wybrac domyslny E24: E12
Podaj opor R1 (1-999) aby go wymusic
w obliczeniach (ENTER - pomin):     

Najblizsza para rezystorow z szeregu  E12  :
  Rezystor R1:              82
  Rezystor R2:              39
  Obliczone napięcie wyj:
        39
  --------------- x  14.0   =   4.512  V
  ( 82  +  39 )

```
Dlaczego zadana jest wartość Vout 4.5V? Aby zabezpieczyć się, gdyby napięcie wejściowe przekroczyło 14V albo napięcie zasilania mikrokontrolera spadło. 

Wyliczone rezystancje mnożymy x100 aby ograniczyć prąd przepływający przez dzielnik czyli potrzebujemy rezystorów 8k2 i 3k9 OHM.

Kolejny przypatny wzór to:
```
       Vin x 1024
ADC = ------------
          Vref
```
Czyli, jeśli zamierzam użyć AVCC jako napięcia adniesienia, to dla jego rzeczywistej wartości i 14 V na wejściu dzielnika, otrzymam 

(4.512 * 1024) / 4.912 = 940.6 ~~ 940

To oznacza, że po podłączeniu 14V do dzielnika napięcia, a następnie jego wyjścia do mikrokontrolera, ADC powinien zwrócić 940. 

A wracając do omówienia 'Mirkowej" metodyki - bo przecież taki mamy cel.

## Zróbmy to po Mirkowemu

Przekształcając wzory podane wyżej:

400 * (5 / 1024) * 1 = 1.95V

gdzie: 
 - 400 - odczyt z ADC
 - 5 - napięcie odniesienia ustawione w ADC
 - 1 - współczynnik podziału dzielnika napięcia - 1 oznacza bezpośrednie podpięcie napięcia do mikroprocesora
 
Jeśli natomiast mamy najprostrzy dzielnik z dwoma identycznymi rezystorami:

400 * (5 / 1024) * 2 = 3.90V

Przy dzielniku, gdzie R1=120k R2=10k, współczynnik podziału = 13. Jeśli wybraliśmy napięcie odniesienia 2.56V

670 * (2.56 / 1024) * 13 = 21.77V

Problem polega na tym, że napięcie odniesienia, współczynnik podziału i wyliczone napięcie najczęściej są liczbami zmiennoprzecinkowymi, których ATmegi nie lubią (obsługa tych zmiennych nie jest sprzętowo zaimplementowana). Trzeba więc tak napisać program, aby obliczenia wykonywał na liczbach całkowitych.

230 * (2.56 / 1024) * 13 = 7.47V

230 * 0.025         * 13 = 7.47V    | *10000

230 * 25            * 13 = 74750

Teraz należy liczbę 74750 rozbić na dwie, gdzie:
 - cz_d będze częścią całkowitą
 - cz_u będzie częścią ułamkową
```c
uint32_t wynik;
uint16_t pm;
uint8_t cz_d, cz_u;

pm = pomiar(5);    //zobacz kod pierwszego przykładu
wynik = pm * 23 * 13;          // dla 850 = 276250
dz_d = wynik / 10000;          // 27
cz_u = (wynik/100) % 100;      // 62
lcd_int(cz_d);
lcd_char('.');
lcd_int(cz_u);
lcd_str("W");
```
Jeśli zakładamy, że cz_d albo cz_u będzie miała trzy miejsca, to należy zdefiniować ją jako uint_16_t.

## Kalibracja i rozwiązania układowe
Testując cały zmontowany układ, często otrzymywałem wartości, których zupełnie się nie spodziewałem - niestety wynikające z problemów sprzętowych:
 - mało precyzyjne rezystory
 - wyrobiona płytka stykowa
 - słabej jakości kabelki

Jeśli wbudowany w ATmegę ADC miałby służyć choćby do monitorowania stanu baterii zasilania awaryjnego, pokusiłbym się o kilka dodatkowych elementów w projekcie:
 - precyzyjne rezystory 0.01%
 - zewnętrzne źródło napięcia odniesienia
 - kondensator szeregowo włączony w układ dzielnika (przy zastosowaniu punktów powyżej - raczej do kompensacji długości przewodu, który byłby podłączony z monitorowaną baterią)
 - wbudowana funkcja kalibrująca - np podłączamy zamiast baterii zasilacz z dość precyzyjnym napięciem 12V na wyjściu, przy mikrokontrolerze mamy dodatkowy przycisk, który zainicjuje pomiar, zczyta wartość z ADC i obliczy:

 230 * 25 * 13 = 74750

 X = (ADC*13)/120000, gdzie 13 to współczynnik podziału, a 120000 = 12V * 10000 (patrz przykład wyżej)

 Tak wyliczony X zapamięta w EEPROM i będzie używał do kolejnych pomiarów.

## Przykład 1


```c
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#include "LCD/lcd44780.h"

#define VREF_VCC (1<<REFS0)               // Deklaracja: Bity REFS1:0 - 01 <- wybór AVCC jako napięcie referencyjne
                                          // Zmierzone napięcie na AREF 4.723V

#define VREF_256 (1<<REFS1)|(1<<REFS0)    // Deklaracja: Bity REFS1:0 - 11 <- wybór wewnętrznego nap 2.56V
                                          // Zmierzone napięcie na AREF 2.588V

#define VREF_VCC_MUL 49                   // Współczynnik dla napięcia 4.83V (uint16_t)((4.83*1000000)/1024)
#define VREF_256_MUL 25                   // Współczynnik dla napięcia 2.56V (uint16_t)((2.56*10000)/1024)

                                          // 230 * (2.56 / 1024) * 13 = 7.47V
                                          // 230 * 0.025         * 13 = 7.47V | *10000
                                          // 230 * 25            * 13 = 74750
                                          //       |
                                          // VREF_256_MUL

volatile uint32_t value;                  // Deklaracja zmiennej wartości - udczytanej z ADC

//#define buf_cnt 15
//volatile uint32_t buf[buf_cnt];

uint8_t init=0;


char liczba[10];                          // zmienna 'liczba' otrzymywana z konwersji wartości


char *int_to_str(int val, char *str, int8_t fw, char znak_wiodacy) {
	char *strp = str;
	uint8_t subzero = 0;

	if(val<0) {                           // jeśli liczba jest ujemna
		val = ~val+1;                     // zaneguj i koryguj
		subzero=1;                        // ustaw znacznik na 1
		fw--;
	}

   do{
      div_t divmod = div(val, 10);        // opracja dzielenia oraz modulo - wynik do struktury ldiv_t
      //*strp++ = divmod.rem + '0';       // wstawianie cyfr od najmniej znaczącej do łańcucha

      if((val == 0) && (strp != str)) {
         *strp++ = znak_wiodacy;
      } else {
         *strp++ = divmod.rem + '0';
      }

      val = divmod.quot;            	// wartość zmniejsza się o jednostki, dziesiątki, setki itd
      fw--;                     		// zmniejszenie licznika szerokości formatowanego pola
      // wykonuj pętlę do momentu sprawdzenia ostatniej cyfry znaczącej lub zajętości całego pola
   } while ( (fw>0));

   if(subzero) *strp++ = '-';			// jeśli była to liczba ujemna, wstaw znak minus
   *strp = 0;                     		// zakończ łańcuch zerem

   strrev(str); // w związku z tym, że w łańcuchu jest odwrócona kolejność cyfr
                // wykonaj ich zamianę

   return str;  // zwróć wskaźnik do początku łańucha z liczbą
}

int main(void)
{

	lcd_init();         // Standardowo, podświetlenie LCD mam sterowane z portu PA7,
	                    // więc do testów odłączyłem je, a port na stałe podłączyłem do VCC

	ADMUX = 7;          // ADMUX to rejestr wyboru multipleksera, gdzie 5 dolnych bitów odpowiada za wybór pinu, do którego
	                    // podłączamy mierzony sygnał (MUX4:0) - ustawienie wartości 7 ustawi 00111 na tych bitach - w ten sposób
	                    // wybierając port PA7(ADC7) jako wejście

	ADMUX |= VREF_256;  // usatwia bity REFS1:0 rejestru ADMUX jako 11 wybierając wewnętrzne napięcie referencyjne 2.56V

    // Poniższe ustawienia powodują cykliczne wyzwalanie pomiaru za pomocą przerwania
	//ADCSRA = (1<<ADEN)|(1<<ADIE)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);  // ADEN=1    - Włącza ADC
	//ADCSRA |= (1<<ADSC)|(1<<ADATE);                                 // ADIE=1    - Włącza przerwania
	                                                                  // ADPSx=111 - Preskaler 128
	                                                                  // ADSC=1    - Rozpoczyna konwersję
	                                                                  // ADATE=1   - Aktywacja automatycznego włącznika ADC

	// Przy poniższych ustawieniach rozpoczęcie pomiaru będzie wyzwalane przez ustawienie 1 na bicie ADCS rejestru ADCSRA
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);              // ADEN=1    - Włącza ADC
	                                                                  // ADPSx=111 - Preskaler 128

	sei();                   // globalne włączenie przerwań

	lcd_cls();               // czyść ekran
	lcd_str("start...");     // wyświetl informację początkową
	_delay_ms(1000);


	uint32_t v, sr=0;        //

	uint8_t czas=5;          //

	uint16_t v1=0, v2=0;     // Obliczone napięcie rozbite na część całkowitą i dziesiętną, aby wyeliminować konieczność
	                         // programowania mikrokontrolera do pracy ze zmiennymi float

	while(1)
	{
                                                       // To jest właśnie przykład "kociego" kodu, który dodatkowo nie został
		                                               // skomentowany, przez co jest zupełnie niezrozumiały
		uint8_t kfil=4;                                // Co robi ta zmienna? Nie mam pojęcia, skoro nigdzie w kodzie nie
		                                               // jest zmieniana.

		ADCSRA |= (1<<ADSC);                           // rozpocznij pomiar
		while( (ADCSRA & (1<<ADSC)) );                 // oczekuje na zakończenie pomiaru - sprawdza flagę ADSC (=0 na końcu pomiaru)
		value = ADCW;                                  // 16bit wartość odczytana z rejestrów ADCH i ADCL

		sr=kfil*sr;
		sr=sr+value*VREF_256_MUL*100;                  // 1194 wzięło się ze współczynnika podziału wynoszącego 11.94
                                                       // Zakładam, że współczynnik ten został wyliczony po dokładnym zmierzeniu
		                                               // rezystancji użytych oporników, ale autor SLOWEM nie wspomniał o tym
		                                               // ani w książce, ani w samym przykładzie.

		sr=sr/(kfil+1);

		v=sr;

		if(!czas) {                                    // wygląda to mi wprost na to, że zutor skopiował cudzy kod i tylko go
			lcd_locate(0,0);                           // trochę "spolonizował" - zmieniając prawdopodobnie oryginalny "time"
			if(v1 || v2)	lcd_str("+");              // na "czas" jako zmienną, która miała wyświetlać wynik tylko co ileś "razy"
			else lcd_str(" ");
			v1 = v/1000000;
			lcd_int( v1 );
			lcd_str(".");

			div_t divmod = div(v/1000, 1000);

			v2 = divmod.rem;

			lcd_str(int_to_str(v2, liczba, 3, '0'));

	//		v2 = (v/100000)%10UL;      // Wyświetlanie innej liczby miejsc po przecinku
	//		lcd_int( v2 );             // |
	//		v3 = (v/10000UL)%10UL;     // |
	//		lcd_int( v3 );             // |
	//		v4 = (v/1000UL)%10UL;      // |
	//		lcd_int( v4 );             // |

			lcd_str(" V   ");

			lcd_locate(1,0);
			//lcd_str(long_int_to_str(v, liczba, 9, ' '));
			czas=7;
		} else czas--;

		//lcd_locate(1,0);
		//lcd_int( value );
		//lcd_str("   ");
		_delay_ms(100);


		PORTD |= (1<<PD4);
		_delay_ms(1);
		PORTD &= ~(1<<PD4);
	}
}

ISR(ADC_vect)
{
	//value = ADCW;
}

```