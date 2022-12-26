Fast PWM – szybki (i mniej dokładny od pozostałych) tryb generowania fali o zmiennym wypełnieniu. Licznik liczy do wartości OCR0 i zostaje wyzerowany. W tym momencie następuje zmiana poziomu logicznego sygnału na pinie OC0 mikrokontrolera.

Dla mikrokontrolera ATmega32 dostępne są trzy timery:
 - 8-bitowy Timer0, 
 - 16-bitowy Timer1,
 - 8-bitowy Timer2

Timer 0 wykorzystuje następujące rejestry:
 - TCCR0 służący do konfiguracji timera
 - TCNT0 to licznik timera, przechowuje jego aktualną wartość
 - OCR0 wykorzystywany przez funkcję Output Compare
 - TIMSK służy do włączania/wyłączania poszczególnych przerwań dla wszystkich timerów
 - TIFR przechowuje flagi powiązane z przerwaniami timerów
 
W trybach Normal i CTC - timer zmienia automatycznie stan pinu w momencie osiągnięcia przez licznik określonej wartości, albo przy jego przepełnieniu. 

Wykorzystanie obu tych funkcji - zmiany stanu pinu przy określonej wartości **I** przepełnieniu licznika pozwala na generowanie sygnału PWM.

W szybkin trybie PWM (fast PWM), licznik timera liczy od 0 do 255, a następnie przepełnia się i zaczyna liczyć od nowa. Przełączenie stanu pinu wyjściowego następuje po osiągnięciu przez licznik wartości wpisanej w rejestrze OCR0.

W trybie nieodwracającym, na początku dyklu pin wyjściowy jest ustawiony w stan wysoki, a po osiągnięciu licznika OCR0, zostaje na nim ustalony stan niski. W trybie odwracającym działą to po prostu odwrotnie (stan niski na początku cyklu).

Dokładny opis rejestrów:

TCCR0:
|7       |6       |5       |4       |3       |2       |1       |0       |
| :---:  | :---:  | :---:  | :---:  | :---:  | :---:  | :---:  | :---:  |
|________|________|________|________|________|________|________|________|
| FOC0   |WGM00   |COM01   |COM00   |WGM01   |CS02    |CS01    |CS00    |


WGM0[1:0]
| Mode | WGM01 CTC0 | WGM00 PWM0 | Timer/Counter Mode of Operation | TOP  | Update of OCR0 | TOV0 Flag Set-on |
|------|------------|------------|---------------------------------|------|----------------|------------------|
|   0  |      0     |      0     |              Normal             | 0xFF |    Immediate   |        MAX       |
|   1  |      0     |      0     |        PWM, Phase Correct       | 0xFF |       TOP      |      BOTTOM      |
|   2  |      1     |      0     |               CTC               | OCR0 |    Immediate   |        MAX       |
|   3  |      1     |      1     |             Fast PWM            | 0xFF |     BOTTOM     |        MAX       |

Tryb NORMAL i CTC Timera0

|COM01 |COM00 |Description                               |
|------|------|------------------------------------------|
|  0   |  0   |Normal port operation, OC0 disconnected.  |
|  0   |  1   |Toggle OC0 on compare match               |
|  1   |  0   |Clear OC0 on compare match                |
|  1   |  1   |Set OC0 on compare match                  |

Tryb PWM Timera0

|COM01 |COM00 |Description                                     |
|------|------|------------------------------------------------|
|  0   |  0   |Normal port operation, OC0 disconnected.        |
|  0   |  1   |Reserved                                        |
|  1   |  0   |Clear OC0 on compare match, set OC0 at BOTTOM,  |
|      |      |(non-inverting mode)                            |
|  1   |  1   |Set OC0 on compare match                        |
|      |      |(inverting mode)                                |

Ustawienie 1:0 - Podanie stanu wysokiego na OC0 na początku cyklu i stanu niskiego, kiedy TCNT0 = OCR0
                 Przy niskiej wartości OCR, średnie wyjściowe napięcie na pinie będzie niskie


Ustawienie 1:1 - Podanie stanu niskiego na OC0 na początku cyklu i stanu wysokiego, kiedy TCNT0 = OCR0
                 Przy niskiej wartości OCR, średnie wyjściowe napięcie na pinie będzie wysokie

                         /|     /|     /|     /|     /|     /|       <- TCNT = 255
                        / |    / |    / |    / |    / |    / |
                       -  |   -  |   -  |   -  |   -  |   -  |      <-  warość OCR     
                      /   |  /   |  /   |  /   |  /   |  /   |
                     /    | /    | /    | /    | /    | /    |
                    /     |/     |/     |/     |/     |/     |       <- TCNT = 0

                    ---    ---    ---    ---    ---    ---    ---
                   |   |  |   |  |   |  |   |  |   |  |   |  |   |     <- Wyjście na pinie OC przy trzybie nieodwracającym 
                   |   |  |   |  |   |  |   |  |   |  |   |  |   |
                  -     --     --     --     --     --     --     -

                  -     --     --     --     --     --     --     -
                   |   |  |   |  |   |  |   |  |   |  |   |  |   |     <- Wyjście na pinie OC przy trzybie odwracającym 
                   |   |  |   |  |   |  |   |  |   |  |   |  |   |
                    ---    ---    ---    ---    ---    ---    ---

Ustawienie 0:0 (domyślne) - sygnał nie jest wysyłany na pin PB3. 

Ustawienia zegara ia preskalera

|CS02    |CS01    |CS00    |Description                                              |
|--------|--------|--------|---------------------------------------------------------|
|  0     |  0     |  0     |No clock source (Timer/Counter stopped).                 |
|  0     |  0     |  1     |clkI/O/(No prescaling)                                   |
|  0     |  1     |  0     |clkI/O/8 (From prescaler)                                |
|  0     |  1     |  1     |clkI/O/64 (From prescaler)                               |
|  1     |  0     |  0     |clkI/O/256 (From prescaler)                              |
|  1     |  0     |  1     |clkI/O/1024 (From prescaler)                             |
|  1     |  1     |  0     |External clock source on T0 pin. Clock on falling edge.  |
|  1     |  1     |  1     |External clock source on T0 pin. Clock on rising edge.   |

Częstotliwość PWM:

Fpwm  = F_CPU / preskaler / 256 (dla 8 bit timera)
```
F_CPU = 20000000 (20MHz)
Presc = 1        Fpwm = 78125     Hz (78    kHz)
Presc = 8        Fpwm =  9765.63  Hz ( 9    kHz)
Presc = 64       Fpwm =  1220.7   Hz ( 1.2  kHz)
Presc = 256      Fpwm =   305.176 Hz ( 0.3  kHz) 
Presc = 1024     Fpwm =    76.3   Hz ( 0.08 kHz)
```


## Wykorzystanie sprzętowego PWM

```c
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

volatile uint8_t pwm1, pwm2, pwm3;

// ********************* MAIN() *********************
int main(void)
{

	DDRB |= (1<<PB3);                   // Pin, naktorym wyprowadzony jest timer
	                                    // (dla OC0 w ATmega32 - PB3), musi byc ustawiony jako
	                                    // wyjscie

                                        //    | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |  <- rejestr TCCR0
	                                    //    +---+---+---+---+---+---+---+---+
	TCCR0 |= (1<<WGM01)|(1<<WGM00);		//    |   | 1 |   |   | 1 |   |   |   |  <- tryb Fast PWM
	TCCR0 |= (1<<COM01);				//    |   |   | 1 |(0)|   |   |   |   |  <- clear at TOP
	TCCR0 |= (1<<CS02)|(1<<CS00);		//    |   |   |   |   |   | 1 |(0)| 1 |  <- preskaler = 1024
	                                    //    +---+---+---+---+---+---+---+---+

	                                    // OCR0 – Output Compare Register:
	OCR0=1;							    // Ustawienie stanu niskiego w cyklu pracy PWM


	uint8_t i = 0;                      // zmienna do wypełnienia (0-255)
	while(1)
	{
		for (i = 0; i<255; i++) {       // pętla zwiększająca wypełnienie co 25ms
		OCR0 = i;                       // rozjaśnianie diody
		_delay_ms(10);
		}
		for (i = 255; i>0; i--) {       // pętla zmniejszająca wypełnienie do 25ms
		OCR0 = i;                       // ściemnianie diody
		_delay_ms(10);
		}
	}
}
```

## Programowy PWM

Wygodnie jest użyć timera w trybie Normal. Ponieważ jest to dmyślny tryb, nie trzeba nawet go specjalnie ustawiać przez wywołanie:

```c
TCCR2 &= ~((1<<WGM21)|(1<<WGM20));
```
Należy natomiast ustawić wywoływanie przerwania przy przepełnieniu licznika:
```
TIMSK |= (1<<TOIE2);
```
oraz
```
TCNT2 = 246;           <- do jakiej wartości ma być ustawiony licznik po przepełnieniu
TCCR2 |= (1<<CS20)|(1<<CS21);   <- preskaler 64
```
Obliczanie częstotliwości przcy generatora PWM:

- częstotliwość taktowania zegara F_CPU = 20MHz = 20000000
- Preskaler = 64

Częstotliwość pracy Timera
```
20000000 / 64 = 312500 = 312.5 kHz
```
Częstotliwość generowanego przerwania (przy przepełnieniu licznika - 256 dla 8 bit)
```
312500 / 256 = 4.8 kHz
```
Powiedzmy, że chcemy, aby częstotliwość ta wynosiła ok 30 kHz - wtedy
```
312500 / 30000 = 10.4.
```
Potrzebujemy więc, aby licznik nie pracował pełnych 256 razy między przerwaniami, ale tylko 10. Więc nakazujemy, any resetował się do wartości 246 zamiast do 0 po przepełnieiu.

Jeśli zamierzamy, aby programowe porty PWM miały rozdzielczość 8-bitową, to będzemy potrzebowali 256 przerwań w celu wygenerowania jednego cyklu sygnału PWM. Będzie miał więc on częstotliwość

```
30000 / 256 = 117 Hz - wystarczającą do sterowania diodami LED, ale potencjalnie za niską do innych celów.
```

Generowanie przerwania z częstotliwością 30kHz odnacza, że każde będzie następowało co
```
1/30000 = 0.000033 - 33 us
```
Jeden cykl taktowania zegara to natomiast
```
1/20000000 = 0.000000005 - 50 ns
```
Oznacza to, że między przerwaniami możemy wykonać ok 666 instrukcji. W momencie, gdy program główny jest bardzo rozbudowany, może spowodować to, że będzie on wykonywany dużo wolniej. Trzeba brać to pod uwagę przy używaniu wolniejszego taktowania mikrokontrolera i zależnie od warunków dobierać odpoweidnio preskaler i częstotliwośc przerwań. Natomiast w tym przypadku, jeśli nie potrzebujemy tak dużej rozdzielczości, możemy zrealidować sterowanie 7 bitowe dające nam już częstotlwość 234 Hz.

_Po przetestowaniu kodu, okazało się, że taka częstotliwość jest za mała, i mruganie diody było bardzo widoczne, więc zmieniłem preskaler do 8_ 

Do rozpoczęcia pracy potrzebna jest jeszcze nazwa przerwania, którą dla ATmego32 można znaleźć w ...\AVR Toolchain\avr\include\avr\IOM32.h
```c
/* Timer/Counter2 Overflow */
#define TIMER2_OVF_vect_num		5
#define TIMER2_OVF_vect			_VECTOR(5)
#define SIG_OVERFLOW2			_VECTOR(5)
```

```c
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

volatile uint8_t pwmR, pwmG, pwmB;          // deklaracja zmiennych trzech kanalow RGB diody LED
volatile uint8_t cnt = 0;

int main(void)
{

	DDRC |= (1<<PC0)|(1<<PC1)|(1<<PC2);     // ustawienie wyjsc na trzech pinach portu C


	TIMSK |= (1<<TOIE2); // przepelnienie licznika bedzie wywolywalo przerwanie
	TCNT2 = 246;                    // reset licznika do 246 po przepelnieniu
	//TCCR2 |= (1<<CS20)|(1<<CS21);   // <- preskaler 64
	TCCR2 |= (1<<CS21);   // <- preskaler 8


	sei();				        // odblokowanie globalne przerwañ
	uint8_t iR, iG, iB;			// definicja zmiennej i na potrzeby petli for()
	uint8_t xR, xG, xB;			// definicja zmiennej i na potrzeby petli for()

	iR = 0;
	iG = 200;
	iB = 0;
	xR = 0;
	xG = 0;
	xB = 0;

	while(1)
	{
		pwmR = iR;
		pwmG = iG;
		pwmB = iB;

		if (xR == 0) iR++; else iR--;
		if (xG == 0) iG=iG+2; else iG=iG-2;
		if (xB == 0) iB=iB+3; else iB=iB-3;
		if ( iR <=0 ) xR = 0;
		if ( iR >=128 ) xR = 1;
		if ( iG <=0 ) xG = 0;
		if ( iG >=128 ) xG = 1;
		if ( iB <=0 ) xB = 0;
		if ( iB >=128 ) xB = 1;
		_delay_ms(10);

	}

}

// funkcja obslugi przerwania - liczaca 0 - 128 i porownujaca aktualny licznik z zadanymi watrosciami pwnR/G/B
ISR( TIMER2_OVF_vect )
{
	if (cnt == 128) cnt=0; else cnt++;
	if(cnt<=pwmR) PORTC |= (1<<PC0); else PORTC &= ~(1<<PC0); // jesli licznik w przerwaniu jest nizszy, niz zadana wartosc pwn
	if(cnt<=pwmG) PORTC |= (1<<PC1); else PORTC &= ~(1<<PC1); // to na odpowietni pin zostanie podany stan wysoki
	if(cnt<=pwmB) PORTC |= (1<<PC2); else PORTC &= ~(1<<PC2); // jesli jest wyzszy, bedzie tam ustawiony stan niski
}
```

