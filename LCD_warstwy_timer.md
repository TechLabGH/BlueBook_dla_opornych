Inspiracja: http://mirekk36.blogspot.com/2012/02/lcd-hd44870-warstwy-efekty.html

Rzeczywiście - ludzie z Elektrody, wypowiadający się w wątku, który podlinkowany jest na końcu wpisu, powalają swoją ignorancją. 

Poniżej moja wariacja na temat wyświetlania różnych, czasem całkiem niezależnych informacji na wyświetlaczu LCD.

Założenia
 - informacje można umieścić na jednej z 5 warstw (gdzie 0 jest najniższa, 4 - najwyższa)
 - każdą warstwę można pozycjonować względem miejsca 0x0 na wyświetlaczu
 - każda warstwa może mieć inny rozmiar i może wychodzić "poza" wyświetlacz
 - Każda warstwa niezależnie może mieć "przezroczystość" - czyli spacje umieszczone na niej mogą zasłaniać warstwy poniżej, lub nie
 - Rozmiar i położenie warstwy może być zmieniane podczas działania programu

Do wyświetlania użyłem biblioteki z przykładu #4, ale w sasadzie wykorzystuję tylko funkcję `lcd_str()` i te, które są przez nią wywoływane.

```c
#include <avr/io.h>                    // standard
#include <avr/pgmspace.h>              // można pominąć, jeśli nie składuje się zmiennych FLASH
#include <avr/eeprom.h>                // można pominąć, jeśli nie składuje się zmiennych EEPROM
#include <util/delay.h>                // jest tu, bo wysyłąnie danych do wyświetlacza używa _delay_ms()
#include <avr/interrupt.h>             // obsługa przerwań
#include <string.h>                    // dodatkowe funkcje do pracy na ciągach znaków
#include "LCD/lcd44780.h"              // biblioteka wyświetlacza

#define LED_PIN (1<<PC0)               // pin C0 ustawiony jako wyjście - używany do debugowania, ustawiania czasów z pomocą oscyloskopu itp
#define LED_TOG PORTC ^=  LED_PIN

char row0[] = "                    ";  // tutaj zdefiniowane są 4 tablice znaków wyświetlane jako kolejne wiersze na wyświetlaczu
char row1[] = "                    ";  // to na nie "nakładane" są kolejne warstwy, które po połączeniu wysyłane są do wyświetlacza
char row2[] = "                    ";  
char row3[] = "                    ";
uint8_t icnt = 0;                      // licznik - maxymalnie zwolniony timer0 (preskaler 1024) przy 20MHz kwarcu nadal jest za szybki, aby sam robił za 
                                       // podstawę czasu w programie - nie chciałem też zaczynać od wolniejszego kwarcu, bo spowolniłoby to też inne operacje
                                       // zamiast tego icnt jest zwiększany o 1 z każdym taktem timera (/1024) i resetowany, gdy osiągnie wartość 250 (co 1 sek)
                                       // dodatkowo używany jest do ustawiania flag ping and pong, które w głównej pętli wywołują obliczenia

int lx[]  = {0,  3, 12,  0,  0};       // pozycja x warstwy względem ekranu: lx[0]=0 - warstwa 0, lx[1]=3 - warstwa 1 ...
int ly[]  = {0,  1,  0,  0,  0};       // pozycja y warstwy - j.w.
int lsx[] = {20, 9,  8,  1, 10};       // rozmiar poziomy warstwy
int lsy[] = {4,  3,  1,  1,  3};       // rozmiar pionowy warstwy

int ltr[] = {0,  0,  0,  0,  0};       // przezroczysztosc warstwy: 0 - spacje nie przezroczyste
                                       //                           1 - spacje nie przesłaniają znaku poniżej

char ltxt[5][LCD_ROWS][LCD_COLS+1];    // tablica ciągów znaków - każda warstwa ma do 4 (zależnie od ilości wierszy) ciągów znaków o długości zależnej
                                       // od wybranego wyświetlacza

uint8_t sek = 13;                      // zmienna sekundy - używana do wyświetlania czasu (symulacja z dużym błędem bez użycia RTC)
uint8_t ping = 0;                      // flaga ping - iest ustawiana (=1) 4 razy na ok sek - przesuwanie gwiazdki
uint8_t pong = 0;                      // flaga pong - jest ustawiana (=1) co sekundę - przeliczenie zegara i przesuwanie napisu
uint8_t gwx = 1;                       // kierunek poziomy gwiazdki (9: w lewo / 1: w prawo)
uint8_t gwy = 1;                       // kierunek pionowy gwiazdki (0: do góry / 1: w dół)

void timer_init(void);                 // deklaracje funkcji użytych w kodzie
void sendstr(void);
void merge(void);


/* === MAIN === */
int main(void)
{

	DDRA  |= (1<<PA7);                 // ustawienie portu A7 - kontrola podświetlenia
	PORTA |= (1<<PA7);                 // włączenie podświetlenia

	DDRC |= LED_PIN;                   // ustawienie poru C0 - dioda / oscyloskop do debugowania kodu i ustawiania czasu
	PORTC |= LED_PIN;

	char godz[] = "--:--:--";          // deklaracja ciągu godz - do wyświetlania symulacji zegarka w prawym górnym rogu

	strcpy(ltxt[1][0], "+-------+");   // napis w ramce, który będzie przesuwał się po dolnych trzech wierszach
	strcpy(ltxt[1][1], "| JACIE |");   // (WARSTWA 2)
	strcpy(ltxt[1][2], "+-------+");

	strcpy(ltxt[3][0], "*");           // gwiadka odbijająca się od brzegów ekranu (WARSTWA 4)


	uint8_t h = 13;                    // wstępne ustawienie godziny do symulacji zegarka
	uint8_t min = 13;                  // wstępne ustawienie minuty do symulacji zegarka

	lcd_init();                        // zainicjowanie wyświetlacza
	timer_init();                      // zainicjowanie timera 0
	sei();                             // włączenie przerwań

	while(1)                           // wszystkie obliczenia znajdują się w nieskończonej pętli while(1), ale nie są wykonywane w sposób ciągły
	{                                  // a dopiero, gdy timer ustawi flagę ping i/lub pong
		if (pong == 1){                // flaga pong wymusza zaktualizowanie zegara i przesunięcie napisu
			if (sek == 60){
				sek = 0;
				min++;
				}
			if (min == 60){
				min = 0;
				h++;
				}
			if (h == 24){
				h = 0;
				}
			godz[0]=((h/10)+48);              // | Jest kilka różnych metod, aby ta część wyglądała bardziej elegancko, ale ta zdawała się
			godz[1]=((h-(h/10)*10)+48);       // | działać najszybciej. 
			godz[2]=':';                      // |
			godz[3]=((min/10)+48);            // |
			godz[4]=((min-(min/10)*10)+48);   // |
			godz[5]=':';                      // |
			godz[6]=((sek/10)+48);            // |
			godz[7]=((sek-(sek/10)*10)+48);   // |

			strcpy(ltxt[2][0], godz);         // po skonstuowaniu ciągu godz, jest on wklejany do zmiennej ltxt pierwszego (0) wiersza trzeciej (2) warstwy
			
            if (sek > 30) lx[1] = 20 - sek/3; else lx[1] = sek/3;  // tutaj auktualniana jest pozycja x warstwy 2 powodując przesuwanie się napisu w ramce
			
            pong = 0;                         // zerowanie flagi pong
		}


		if (ping == 1){                                              // flaga ping jest ustawiana co 1/4 sek, wiec gwiardka przesuwa sie o 4 pola na sek
			if (gwx == 1) lx[3] = lx[3] +1; else lx[3] = lx[3] -1;   // ustawianie nowej pozycji warstwy 4 przechowującej gwiazdkę na podstawie
			if (gwy == 1) ly[3] = ly[3] +1; else ly[3] = ly[3] -1;   // zmiennych gwx i gwy

			if (lx[3] == 0) gwx = 1;                                 // zmiana kierunku przy dojściu do brzegu ekranu
			if (lx[3] == 19) gwx = 0;
			if (ly[3] == 0) gwy = 1;
			if (ly[3] == 3) gwy = 0;
			ping = 0;                                                // zerowanie flagi ping
		}
	}
}

void timer_init(void)                                                // funkcja inicjująca timer 0
{
	TCCR0 |= (1<<WGM01);
	TCCR0 |= (1<<CS02)|(1<<CS00);
	OCR0 = 250;                                                      // wartość dobrana eksperymentalnie - zależnie od potrzeb - ile razy na 1 sek mamy zamiar 
	TIMSK |= (1<<OCIE0);                                             // aktualizować różne obliczenia
}

ISR(TIMER0_COMP_vect)                                                // obsługa przerwania
{
	icnt++;
	if (icnt == 15 || icnt == 30 || icnt == 45 || icnt ==60){        // 4 razy na sekundę:
		ping = 1;                                                    // - ustawiana jest flaga ping
		merge();                                                     // - następuje złączenie warstw
		sendstr();                                                   // - złączone warstwy są wysyłane do wyświetlacza
	}
	if (icnt > 60){                                                  // Co sekundę inkrementowana jest liczba sekund i ustawiana jest flaga pong 
	icnt = 0;                                                        // uaktualniająca zegar i pozycję napisu
	pong = 1;
	sek++;
	}
	LED_TOG;                                                         // zmiana stanu na pinie C0 - pozwala po podłączeniu oscyloskopu sprawdzić, czy przerwania są
}                                                                    // generowane i z jaką dokładnie częstotliwością

void merge(void){                                                    // funkcja łącząca warstwy

	for (int x = 0; x < LCD_COLS; x++){                              // łączenie po kolumnach - od lewej (x=0) do prawej (x=20)
		row0[x] = ' ';                                               // łączenie odbywa się dla czterech wierszy (0-3) na raz
		row1[x] = ' ';                                               //   |
		row2[x] = ' ';                                               //   |
		row3[x] = ' ';                                               //   |

		for (int l = 0; l < 5; l++){                                 // analizowanie znaków na warstwach od najniższej (0) do najwyższej (4)

			// ltxt [l] [y] [x]                                                  <- zmienna char przechowująca znak - pozycja x-y na warstwie l
			// top-left corner        : ly[l] x lx[1]                            <- lewy górny róg warstwy - pozycja względem ekranu>
			// bottom - right corner  : ly[l] + lsx[l] - 1 x ly[l] + lsy[l] - 1  <- prawy dolny róg warstwy - pozycja względem ekranu

                                                                         // analiza znaków z wiersza 0 i kolumny x
			if (       ly[l] <= 0                                        // górna krawędź warstwy powyżej lub w wierszu 0
					&& lx[l] <= x                                        // lewa krawedź warstwy na lewo od albo w kolumnie x
					&& (ly[l] + lsy[l] - 1) >= 0                         // dolna krawędź warstwy poniżej albo w wierszu 0
					&& (lx[l] + lsx[l] - 1) >= x                         // prawa krawędź warstwy na prawo od albo w kolumne x
					&& ltxt [l] [0 - ly[l]] [x - lx[l]] > 31 + ltr[l])   // znak do analizy jest drukowalny + pomijanie spacji przy przezroczystości
				row0[x] = ltxt [l] [0 - ly[l]] [x - lx[l]];              // jeśli wszystkie powyższe warunki spełnione - "kładziemy znak z warstwy na wyświetlacz"

			if (       ly[l] <= 1
					&& lx[l] <= x
					&& (ly[l] + lsy[l] - 1) >= 1
					&& (lx[l] + lsx[l] - 1) >= x
					&& ltxt [l] [1 - ly[l]] [x - lx[l]] > 31 + ltr[l])
				row1[x] = ltxt [l] [1 - ly[l]] [x - lx[l]];

			if (       ly[l] <= 2
					&& lx[l] <= x
					&& (ly[l] + lsy[l] - 1) >= 2
					&& (lx[l] + lsx[l] - 1) >= x
					&& ltxt [l] [2 - ly[l]] [x - lx[l]] > 31 + ltr[l])
				row2[x] = ltxt [l] [2 - ly[l]] [x - lx[l]];

			if (       ly[l] <= 3
					&& lx[l] <= x
					&& (ly[l] + lsy[l] - 1) >= 3
					&& (lx[l] + lsx[l] - 1) >= x
					&& ltxt [l] [3 - ly[l]] [x - lx[l]] > 31 + ltr[l])
				row3[x] = ltxt [l] [3 - ly[l]] [x - lx[l]];

		}
	}
}

void sendstr(void){                           // funkcja wysyłająca kolejne wiersze do wyświetlacza
	lcd_locate(0, 0);
	lcd_str(row0);
	lcd_locate(1, 0);
	lcd_str(row1);
	if ( LCD_ROWS>2 ) lcd_locate(2, 0);
	if ( LCD_ROWS>2 ) lcd_str(row2);
	if ( LCD_ROWS>3 ) lcd_locate(3, 0);
	if ( LCD_ROWS>3 ) lcd_str(row3);
}
```

Częstotliwości 
```
16000000 - kwarc
    |
    |    : 1024 - preskaler
    |
   \ /
    15625
       |
       |    : 250 - rejest porównawczy wywołujący przerwanie
       |
      \ /
       62.5   - zaokrąglone do 60
                     ----------------------------
                        |                    |
                        | : 4                |
                        |                    |
                       \ /                  \ /
                   flaga ping           flaga pong
```


Warstwy
```

                                 ----------------------
                                /     A              /       warstwa 4
                               /             X      / 
                               ---------------------
                                      |      |
                                 ----------------------
                                /            |       /       warstwa 3
                               /                    / 
                               ---------------------
                                      |      |
                                 ----------------------
                                /            |       /        warstwa 2
                               /                    / 
                               ---------------------
                                      |      |
                                 ----------------------
                                /            |       /        warstwa 1
                               /             Y      / 
                               ---------------------
                                      |      |
                                 ----------------------
                                /            |       /        warstwa 0
                               /                    / 
                               ---------------------
                                      |      |
                         ========================================
                        /             |      |                 /
                       /              A      |                /
                      /                      X                /
                     /                                      /
                    ========================================
```
