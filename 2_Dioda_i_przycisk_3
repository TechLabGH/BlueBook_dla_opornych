#include <avr/io.h>      // Standard include for AVR
#include <util/delay.h>  // Delay functions

#define LED_PIN (1<<PC7)            //definicja pinu, do ktorego podlaczona jest dioda
#define LED_ON  PORTC &= ~LED_PIN   //makrodefinicja - wlaczenie diody
#define LED_OFF PORTC |=  LED_PIN   //makrodefinicja - wylaczenie diody
#define LED_TOG PORTC ^=  LED_PIN   //makrodefinicja - zmiana stanu pinu diody

#define KEY1_PIN (1<<PC6)           //definicja pinu, do ktorego podlaczony jest przycisk1
#define KEY2_PIN (1<<PC5)           //definicja pinu, do ktorego podlaczony jest przycisk2
#define KEY3_PIN (1<<PC2)           //definicja pinu, do ktorego podlaczony jest przycisk3

uint8_t klawisz_wcisniety(uint8_t klawisz);   //deklaracja funkcji

int main(void) {

	DDRC  |= LED_PIN;   //kierunek pinu - wyjscie
	PORTC |= LED_PIN;   //wylaczenie diody led

	DDRC  &= ~( KEY1_PIN | KEY2_PIN | KEY3_PIN );   //kierunek pinu - wejscie
	PORTC |=    KEY1_PIN | KEY2_PIN | KEY3_PIN  ;   //wewnetrzne podciogniecie pinu przyciskow

	while(1)
	{
		if ( klawisz_wcisniety( KEY1_PIN ) ) LED_ON;

		if ( klawisz_wcisniety( KEY2_PIN ) ) LED_OFF;

		if ( klawisz_wcisniety( KEY3_PIN ) ) LED_TOG;

	}

}

uint8_t klawisz_wcisniety(uint8_t klawisz) {      // kod funkcji
	if ( !(PINC & klawisz ) ) {
		_delay_ms(80);
		if ( !(PINC & klawisz ) ) return 1;
	}
	return 0;                          // funcja zwraca 0, jesli nie wykryla wcisnietego przycisku
}

Chyba jabardziej interesującym jest ten kod

	DDRC  &= ~( KEY1_PIN | KEY2_PIN | KEY3_PIN );
	PORTC |=    KEY1_PIN | KEY2_PIN | KEY3_PIN  ;

jeśli	
KEY1_PIN:        | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  |
KEY2_PIN:        | 0  | 0  | 1  | 0  | 0  | 0  | 0  | 0  |
KEY3_PIN:        | 0  | 0  | 0  | 0  | 0  | 1  | 0  | 0  |

to suma tych trzech bajtów da nam
                 | 0  | 1  | 1  | 0  | 0  | 1  | 0  | 0  |
				 
więc można będzie ustawić kierunek dla nich trzech na raz, zamiast w trzech osobnych liniach
	DDRC  &= ~KEY1_PIN;
	DDRC  &= ~KEY2_PIN;
	DDRC  &= ~KEY3_PIN;

Poodwnie w drugiej linii ustawiamy stan wysoku dla wszystkich trzech pinów razem