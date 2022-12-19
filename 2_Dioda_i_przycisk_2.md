#include <avr/io.h>      // Standard include for AVR
#include <util/delay.h>  // Delay functions

#define LED_PIN (1<<PC7)           //definicja pinu, do ktorego podlaczona jest dioda
#define LED_TOG PORTC ^=  LED_PIN  //makrodefinicja - zmiana stanu pinu diody

#define KEY_PIN (1<<PC6)           //definicja pinu, do ktorego podlaczony jest przycisk
#define KEY_DOWN !(PINC & KEY_PIN) //makro spardzajace czy przycisk jest wcisniery (stan niski na pinie)

uint8_t klawisz_wcisniety(void);   //deklaracja funkcji                                      (*)

int main(void) {

	DDRC |= LED_PIN;    //kierunek pinu - wyjscie
	PORTC |= LED_PIN;   //wylaczenie diody led
	DDRC &= ~KEY_PIN;   //kierunek pinu - wejscie
	PORTC |= KEY_PIN;   //wewnetrzne podciogniecie pinu przycisku

	while(1)
	{
		if (klawisz_wcisniety() ) {   // wywolanie funkcji sprawdzajacej wcisniecie przycisku (**)

				LED_TOG;              // zmien stan diody na przeciwny
				_delay_ms(200);

		}
	}

}

uint8_t klawisz_wcisniety(void) {      // kod funkcji
	if ( KEY_DOWN ) {
		_delay_ms(80);

		if ( KEY_DOWN ) return 1;      // funkcja zwraca 1, jesli wykryla wcisniety przycisk (***)
	}

	return 0;                          // funcja zwraca 0, jesli nie wykryla wcisnietego przycisku
}

O ile idea jest prosta - wyrzucenie kodu sprawdzającego wciśnięcie przycisku poza main(), to warto zwrócić uwagę na dwie rzeczy:

(*) deklaracja funkcji powyżej main() - aby kompilator wiedział, że taka funcja znajduje się gdzieś i nie wyrzucił błędu
kiedy jest ona wołana w miejscu (**)

(***) return 1 powoduje opuszczenie funkcji i jej dalszy kod jest pomijany