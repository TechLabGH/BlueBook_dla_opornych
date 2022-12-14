Przykład - dla mikroprocesora ATmega32 z 20MHz kwarcem

## Rejestry timera 0

#### Rejestr TCCR0

|         |`    7    `|`    6    `|`    5    `|`    4    `|`    3    `|`    2    `|`    1    `|`    0    `|
|:---     | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|TCCR0    |FOC0|WGM00|COM01|COM00|WGM01|CS02|CS01|CS00|
|                                                                         |
|INIT     |   0   |   0   |   0   |   0   |   0   |   0   |   0   |   0   |

Nas interesują:

Bity 6 i 3 - tryb pracy timera (WGMxx)
* `0 0` -  Normal
* `0 1` -  PWM
* `1 0` -  CTC
* `1 1` -  Fast PWM
			 
Bity 2, 1 i 0 -  ustawienia preskalera (CSxx)
* `0 0 0`  - Timer zatrzymany
* `0 0 1`  - Brak preskalera - praca w częstotliwością zegara
* `0 1 0`  - CLK / 8
* `0 1 1`  - CLK / 64
* `1 0 0`  - CLK / 256
* `1 0 1`  - CLK / 1024
* `1 1 0`  - Zewn zegar na pinie T0 - wykrywanie zbocza opadającego
* `1 1 1`  - Zewn zegar na pinie T0 - wykrywanie zbocza narastającego

#### Rejestr TCNT0

|         |`    7    `|`    6    `|`    5    `|`    4    `|`    3    `|`    2    `|`    1    `|`    0    `|
|:---     | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|TCNT0    |       |       |       |       |       |       |       |       |
|                                                                         |
|INIT     |   0   |   0   |   0   |   0   |   0   |   0   |   0   |   0   |

W tym rejestrze znajduje się aktualny stan licznika

#### Rejestr OCR0

|         |`    7    `|`    6    `|`    5    `|`    4    `|`    3    `|`    2    `|`    1    `|`    0    `|
|:---     | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|OCR0     |       |       |       |       |       |       |       |       |
|                                                                         |
|INIT     |   0   |   0   |   0   |   0   |   0   |   0   |   0   |   0   |

W tym rejestrze ustawiamy wartość, z którą będzie porównywany licznik z rejestru TCNT0. W momencie, gdy będą identyczne, wygenerowane zostanie przerwanie.

#### Rejestr TIMSK


|         |`    7    `|`    6    `|`    5    `|`    4    `|`    3    `|`    2    `|`    1    `|`    0    `|
|:---     | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|TIMSK    |OCIE2|TOIE2|TICIE1C|OCIE1A|OCIE1B|TOIE1|***OCIE0***|***TOIE0***|
|                                                                         |
|INIT     |   0   |   0   |   0   |   0   |   0   |   0   |   0   |   0   |

* Bit 1  - gdy jest ustawiony na 1, przerwanie jest generowane gdy rejestry TCNT0 i OCR0 są identyczne.
* Bit 0  - gdy jest udtawiony na 1, przerwanie jest generowanie przy przepełnieniu timera.

#### Rejestr TIFR

|         |`    7    `|`    6    `|`    5    `|`    4    `|`    3    `|`    2    `|`    1    `|`    0    `|
|:---     | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
|TIFR     |OCIF2|TOV2|ICF1|OCF1A|OCF1B|TOV1|***OCF0***|***TOVO0***|
|                                                                         |
|INIT     |   0   |   0   |   0   |   0   |   0   |   0   |   0   |   0   |
	
To jest rejest flag, gdzie:
* Bit 1  - jest ustawiany na 1, gdy generowane jest przerwanie związane z porównywaniem licznika z rejestrem OCR0
* Bit 0  - jest ustawiany na 1, gdy generowane jest przerwanie spowodowane przepełnieniem licznika

### W kodzie będziemy ustawiać:
1. bity WGM 10 (WGM00 = 1, WGM01 = 0) aby timer pracował w trybie CTC
2. bity preskalera CS 101 (CS02 = 1, CS01 = 0, CS00 = 1) aby ustawić częstotliwość timera na CPU / 1024
3. bajt "porównawczy" OCR0 = 98 (0x62), ponieważ 20000000 / 1024 / 200 = 97.7

	Dlaczego tak? Tłumaczenie łopatologiczne:
	* Kwarc "tyka" 20mln razy na sek
	* My dzielimy to przez 1024, więc licznik będzie tykał ok 19531 na sekundę (19531Hz)
	* My potrzebujemy 200 tyknięć (200Hz), więc interesuje nas tylko co 98-my cykl timera.
	* Gdyby wartość ta wyszła większa, niż 255 (bo tyle max możemy zapisać w rejestrze OCR0) to musielibyśmy posłużyć się 16bitowym timerem, albo szukać innego rozwiązania (np dodatkowa zmienna)


## main.c

```c
#include <avr/io.h>           // standard - plik naglowkowy AVR
#include <avr/interrupt.h>    // plik naglowkowy do obslugi przerwan
#include <util/delay.h>       // plik naglowkowy do obslugi _delay_

#include "d_led.h"            // plik naglowkowy projektu - do obslugi wyswietlacza

void czekaj(uint8_t ts);      // delkaracja funkcji do opoznienia opartego na zmiennym czasie - wykorzystanej do 
                              // przyspieszania animacji

int main(void)
{

        d_led_init();                     // wywolanie funkcji inicjujacej wyswietlacz z d_led.c

        sei();			          // uruchomienie przerwan - funkcja wywolywana z interrupt.h

        cy1=2;                            // przynajmniej na poczatku warto sobie poustawiac kilka roznych cyfr, zeby sprawdzic
        cy2=0;                            // czy wszystko jest dobrze podlaczone
        cy3=2;
        cy4=3;
        _delay_ms(3000);

        uint16_t licznik=0;               // licznik do wykorzystania w kodzie ponizej - 16 bitow bedzie potrzebne do 
	                                  // wyswietlania malejacej liczby

        cy1=8;                            // wyswietla 8888 i czeka 3sek
        cy2=8;
        cy3=8;
        cy4=8;
        _delay_ms(3000);

        cy1=NIC;                          // czysci wyswietlacz i czeka 3 sek
        cy2=NIC;
        cy3=NIC;
        cy4=NIC;
        _delay_ms(3000);

        licznik=1;                       // liczenie 1-9999 wydaje mi sie troche lepsza logika, niz propozycja z ksiazki
        while(licznik<10000)             // nie wymaga 4 dodatkowych zmiennych; trudno mi powiedziec, ktore operacje
        {                                // sa bardziej wymagajace
                cy4 = licznik % 10;
                if (licznik>9)   cy3 = (licznik / 10) % 10; else cy3 = NIC;     // ...%10 zwraca jednosci z zadanej liczby
		if (licznik>99)  cy2 = (licznik / 100) % 10; else cy2 = NIC;
		if (licznik>999) cy1 = (licznik / 1000) % 10; else cy1 = NIC;

		_delay_ms(10);
		licznik++;
	}

	cy1=NIC;                         // czysci wyswietlacz i czeka 3 sek
	cy2=NIC;
	cy3=NIC;
	cy4=NIC;
	_delay_ms(3000);

         // po zdefiniowaniu dodatkowych kombinacji wyswietlanych segmentow, mozemy zmienne cy... ustawiac jako kolejne liczby >10
         // aby wykorzystac wyswietlacz do wyswietlania czegos poza cyframi (nawet bardzo "umownych" liter)

	licznik = 100;

	while (licznik) {
		cy1 = 11;
		czekaj(licznik);
		cy1 = NIC;
		cy2 = 11;
		czekaj(licznik);
		cy2 = NIC;
		cy3 = 11;
		czekaj(licznik);
		cy3 = NIC;
		cy4 = 11;
		czekaj(licznik);
		cy4 = 12;
		czekaj(licznik);
		cy4 = 13;
		czekaj(licznik);
		cy4 = 14;
		czekaj(licznik);
		cy4 = NIC;
		cy3 = 14;
		czekaj(licznik);
		cy3 = NIC;
		cy2 = 14;
		czekaj(licznik);
		cy2 = NIC;
		cy1 = 14;
		czekaj(licznik);
		cy1 = 15;
		czekaj(licznik);
		cy1 = 16;
		czekaj(licznik);
		licznik--;
	}

	// Przyklad z ksiazki

	licznik=6000;
	uint8_t  d1,d2,d3,d4;

	while(1)
		{
			licznik--;

			d1=licznik/1000;
			if(d1) cy1=d1; else cy1=NIC;
			d2=(licznik-(d1*1000))/100;
			if(d2) cy2=d2; else cy2=(licznik>999)?0:NIC;
			d3=(licznik-(d1*1000)-(d2*100))/10;
			if(d3) cy3=d3; else cy3=(licznik>99)?0:NIC;
			d4=(licznik-(d1*1000)-(d2*100)-(d3*10));
			cy4=d4;
			_delay_ms(10);
			if(!licznik) licznik=6000;
		}
}

void czekaj(uint8_t ts) {
	while(ts){
		_delay_ms(1);
		ts--;
	}
}
```

## d_led.c

```c
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/pgmspace.h>   // plik naglowkowy dodajacy mozliwosc odczytu danych z panieci flash

#include "d_led.h"          // dolacza plik naglowkowy

volatile uint8_t cy1;       // definicja czterech zmiennych, ktore beda przechowywaly cyfry do wyswietlenia
volatile uint8_t cy2;       // po ich zmianie, nowa cyfra ZACZNIE wyswietlac sie przy najblizszym wygenerowanym
volatile uint8_t cy3;       // przerwaniu z timera i bedzie trwalo 4 cykle tego timera (ok 20 milisekund)
volatile uint8_t cy4;       // bardzo szybka zmiana tych zmiennych moze spowodowac zmniejszenie czytelnosci

const uint8_t cyfry[20] PROGMEM = {                               // segment          GFEDCBA
		~(SEG_A|SEG_B|SEG_C|SEG_D|SEG_E|SEG_F),	          // 0   cyfry[0]  0b11000000        A
		~(SEG_B|SEG_C),                                   // 1   cyfry[1]  0b11111001     +-----+
		~(SEG_A|SEG_B|SEG_D|SEG_E|SEG_G),                 // 2   cyfry[2]  0b10100100   F |     | B
		~(SEG_A|SEG_B|SEG_C|SEG_D|SEG_G),                 // 3   cyfry[3]  0b10110000     |  G  |
		~(SEG_B|SEG_C|SEG_F|SEG_G),                       // 4   cyfry[4]  0b10011001     +-----+
		~(SEG_A|SEG_C|SEG_D|SEG_F|SEG_G),                 // 5   cyfry[5]  0b10010010   E |     | C
		~(SEG_A|SEG_C|SEG_D|SEG_E|SEG_F|SEG_G),	          // 6   cyfry[6]  0b10000010     |     |
		~(SEG_A|SEG_B|SEG_C|SEG_F),                       // 7   cyfry[7]  0b11011000     +-----+
		~(SEG_A|SEG_B|SEG_C|SEG_D|SEG_E|SEG_F|SEG_G),     // 8   cyfry[8]  0b10000000        D
		~(SEG_A|SEG_B|SEG_C|SEG_D|SEG_F|SEG_G),	          // 9   cyfry[9]  0b10010000
		0xFF,                                             // NIC cyfry[10] 0b11111111
		~SEG_A,                                           // segment A wyswietlony gdy jako zmienna cy... ustawimy 11
		~SEG_B,                                           // segment B wyswietlony gdy jako zmienna cy... ustawimy 12
		~SEG_C,                                           // segment C wyswietlony gdy jako zmienna cy... ustawimy 13
		~SEG_D,                                           // segment D wyswietlony gdy jako zmienna cy... ustawimy 14
		~SEG_E,                                           // segment E wyswietlony gdy jako zmienna cy... ustawimy 15
		~SEG_F                                            // segment F wyswietlony gdy jako zmienna cy... ustawimy 16
};
        // Podczas definiowania kolejnych elementow tablicy uzywamy negacji (~) poniewaz potrzebujemy ustawic stan niski (0)
        // dla tych elementow, ktore powinny byc zaswiecone. Do tego mylacy jest fakt, ze bity ofpowiadajace kolejnym segmentom
        // sa ulozone od najmlodzego (czyli "od prawej do lewej")

void d_led_init(void)                       // FUNKCJA INICJUJACE WYSWIETLACZ
{
	LED_DATA_DIR = 0xFF;                // ustawia wszystkie piny jako wyjscia
	LED_DATA = 0xFF;                    // ustawia wszystkie piny w stan wysoki (gasi)
	ANODY_DIR |= MASKA_ANODY;           // ustawia 4 piny jako wyjscia
	ANODY_PORT |= MASKA_ANODY;          // ustawia 4 piny w stan wysoki (gasi)

	// ustawienie TIMER0
	TCCR0 |= (1<<WGM01);                // wymusza tryb CTC dla timera 0
	TCCR0 |= (1<<CS02)|(1<<CS00);       // ustawia preskaler = 1024 dla timera 0
	OCR0 = 98;                          // wpisuje 98 do rejestu porownawczego (zeby osiagnac czest przerwania 200Hz)
	TIMSK |= (1<<OCIE0);                // ustawia przerwanie w momencie CompareMatch
}


ISR(TIMER0_COMP_vect)                       // FUNKCJA OBSLUGI PRZERWANIA
{
	static uint8_t licznik=1;           // tylko jedna cyfra jest wyswietlana na raz - co 5ms kolejnal zmienna licznik 
	                                    // kontroluje ktora to cyfra

	ANODY_PORT = (ANODY_PORT | MASKA_ANODY);                     // wygaszenie wszystkich wyswietlaczy

	if(licznik==1)      LED_DATA = pgm_read_byte( &cyfry[cy1] ); // Zaleznie od zmiennej licznik, z tablicy 
	else if(licznik==2) LED_DATA = pgm_read_byte( &cyfry[cy2] ); // zdefiniowanej powyzej pobieramy bajt odpowiadajacy 
	else if(licznik==4) LED_DATA = pgm_read_byte( &cyfry[cy3] ); // cyfrze ustawionej zmiennymi cy1 - cy4
	else if(licznik==8) LED_DATA = pgm_read_byte( &cyfry[cy4] );

	ANODY_PORT = (ANODY_PORT & ~MASKA_ANODY) | (~licznik & MASKA_ANODY); // Zaleznie od zmiennej licznik ustawiamy 
	                                                                     // stan niski na odpowiednim wyjsciu podlaczonym 
                                                                             // do jednej ze wspolnych anodwyswietlacza - 
                                                                             // CA1, CA2, CA3 lub CA4

        // dzieki temu rozwiazaniu te sama zmienna uzywamy do kontroli wyswietlanej cyfry 1-2-3-4-1-2... jak i do logiki 
        // odpowiedzialnej za ustawianie stanow na pinach wyjsciowych bez zadnego dodatkowgo przeliczania

	licznik <<= 1;                 // zamiast stosowac inkrementacje, lub w tym przypadku mnozenie *2, po prostu 
                                       // przesuwamy bit w zmiennej licznik o jeden w lewo
	if(licznik>8) licznik = 1;     // ustawiamy zmienna licznik = 0b00000001 po tym, jak po przesunieciu wartosc 
                                       // binarna tej zmiennej >8 - w naszym przypadku bedzie to 16, bo 0x00010000
}
```

### d_led.h

```c
#ifndef _d_led_h
#define _d_led_h

// Definicje poszczegolnych portow i pinow, ktore uzywamy do kontroli wyswietlacza
#define 	LED_DATA      PORTA	// Do portu A podlaczamy 8 pinow wyswietlacza odpowiedzialnych za segmenty
#define		LED_DATA_DIR  DDRA	// Ustawiamy wszystkie wyjscia wybranego portu jako wyjscia
#define 	ANODY_PORT    PORTC	// Do portu C podlaczamy 4 piny wyswietlacza kontrolujace poszczegolne cyfry
#define 	ANODY_DIR     DDRC	// Ustawiamy te 4 wybrane piny jako wyjscia

// Piny uzyte w kodzie sa przestawione w stosunku do opisu z ksiazki!!!
// ====================================================================

#define 	CA1 	(1<<PC0)		// pin CA1 wyswietlacza podlaczamy do pinu 0 portu C
#define 	CA2 	(1<<PC1)		// pin CA2 wyswietlacza podlaczamy do pinu 1 portu C
#define 	CA3 	(1<<PC2)		// pin CA3 wyswietlacza podlaczamy do pinu 2 portu C
#define 	CA4 	(1<<PC3)		// pin CA4 wyswietlacza podlaczamy do pinu 3 portu C

#define MASKA_ANODY (CA1|CA2|CA3|CA4)  // Zdefinowana MASKA_ANODY bedzie uzywana do kontroli czterech pinow wspolnych anod
                                       // np inicjalizacja i gaszenie wyswietlacza

#define SEG_A (1<<0)                // Definiujemy, do ktorych wyjsc sa podlaczone poszczegolne piny wyswietlacza
#define SEG_B (1<<1)                // odpowiedzialne za wyswietlanie segmentow
#define SEG_C (1<<2)
#define SEG_D (1<<3)
#define SEG_E (1<<4)
#define SEG_F (1<<5)
#define SEG_G (1<<6)
#define SEG_DP (1<<7)

#define NIC 10                      // "wirtualny" segment, ktory jest uzywany do nie wyswietlania niczego (kiedy nie 
                                    // chcemy) wyswietlac zera. Jesli to pomoze, to mozna przyjac ze znajduje sie na 
                                    // wyswietlaczu, ale nie jest podlaczony.

// zmienne uzywane do ustalania, jakie cyfry powinny byc wyswietlone na poszczegolnych pozycjach
// ustawione sa jako extern, aby bylo mozna z nich korzystac we wszystkich funkcjach plikow z tym plikiem dolaczonym

extern volatile uint8_t cy1;
extern volatile uint8_t cy2;
extern volatile uint8_t cy3;
extern volatile uint8_t cy4;

void d_led_init(void);              // deklaracja funkcji inicjujacej wyswietlacz, aby byla ona wywolywalna z main.c
                                    // funcji ISR(TIMER0_COMP_vect) nie trzeba tutaj dodawac, bo dziala ona tylko w pliku d_led.c

#endif	// koniec _d_led_h
```
