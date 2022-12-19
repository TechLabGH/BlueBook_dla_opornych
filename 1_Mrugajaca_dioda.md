```C
#include <avr/io.h>      // Standard include for AVR
#include <util/delay.h>  // Delay functions

#define LED_PIN (1<<PC7)           //definicja pinu, do ktorego podlaczona jest dioda
#define LED_ON PORTC &= ~LED_PIN   //makrodefinicja - wlaczenie diody
#define LED_OFF PORTC |= LED_PIN   //makrodefinicja - wylaczenie diody

int main(void) {

	DDRC |= LED_PIN;    //kierunek pinu - wyjscie

	while(1)
	{
			LED_ON;          //zapal diode
			_delay_ms(1000); //czekaj
			LED_OFF;         //zgas diode
			_delay_ms(1000); //czekaj
	}


}
```
Omowienie poszczegolnych opeacji w nastepnym przykladzie z przyciskiem
