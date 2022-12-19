
#include <avr/io.h>      // Standard include for AVR
#include <util/delay.h>  // Delay functions

#define LED_PIN (1<<PC7)           //definicja pinu, do ktorego podlaczona jest dioda
#define LED_TOG PORTC ^=  LED_PIN  //makrodefinicja - zmiana stanu pinu diody

#define KEY_PIN (1<<PC6)           //definicja pinu, do ktorego podlaczony jest przycisk
#define KEY_DOWN !(PINC & KEY_PIN) //makro spardzajace czy przycisk jest wcisniery (stan wysoki na pinie)

int main(void) {

	DDRC |= LED_PIN;    //kierunek pinu - wyjscie
	PORTC |= LED_PIN;   //wylaczenie diody led
	DDRC &= ~KEY_PIN;   //kierunek pinu - wejscie
	PORTC |= KEY_PIN;   //wewnetrzne podciogniecie pinu przycisku

	while(1)
	{
		if ( KEY_DOWN ) {
			_delay_ms(80);
			if ( KEY_DOWN ) {
				LED_TOG;
				_delay_ms(200);
			}
		}
	}


}


                                                  --- o ---
						  
PC7 jest zdefiniowane w <avr/io.h> i dla ATmegi32 oznacza tak naprawdę... 7. Więc LEDPIN = (1<<PC7) = 0b10000000

                                                  --- o ---
						  
PORTC - bajt zawierający stany każdego pinu Portu_C mikrokontrolera. 
Zmieniające je programowo można ustawiać stan na pinach wyjściowych; odczytując, można sprawdzić stana na pinach wejściowych.

PORTC ^= LED_PIN to skrócony zapis PORTC = PORTC ^ LED_PIN (sumowanie bitowe modulo 2)
Po polsku - tam, gdzie bajt LED_PIN ma "1", tam odpowiadający bit w PORTC jest zmieniany na przeciwny, a pozostałe pozostają niezmienione


PORTC:           | b7 | b6 | b5 | b4 | b3 | b2 | b1 | b0 |
LED_PIN:         | 1  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |

PORTC^LED_PIN:   |~b7 | b6 | b5 | b4 | b3 | b2 | b1 | b0 |


Czyli przy każdym wywołaniu, zmieniamy stan na pinie wyjściowym C7 na przeciwny.

                                                  --- o ---
						  
!(PINC & KEY_PIN) można zapisać jako 

NOT (PINC & KEY_PIN)

PORTC:           | b7 | b6 | b5 | b4 | b3 | b2 | b1 | b0 |
KEY_PIN:         | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  |

PINC & KEY_PIN:  | 0  | b6  | 0  | 0  | 0  | 0  | 0  | 0  |

Można zauważyć, że wartość tego co wyjdze z mnożenia bitowego (&) PINC i KEY_PIN, zależy od bitu b6.
Przy wciśniętym przycisku, bit ten = 0 (przycisk pogłączony do GND), przy puszczonym = 1 (przycisk podciągnięcy do VCC przez rezystor)

(PINC & KEY_PIN) będzie "TRUE" (to znaczy >0) gdy przycisk jest zwolniony.
"!" odwraca tę logikę czyli !(PINC & KEY_PIN) = TRUE kiedy przycisk jest wciśnięty

dlatego dioda mruga dopiero po naciśnięciu przycisku, gdyż 

if ( KEY_DOWN )       <- warunek jest spełniony kiedy !(PINC & KEY_PIN) == TRUE (>0)

                                                  --- o ---
						  
PORTC |= LED_PIN  ==>  PORTC = PORTC | LED_PIN

ustawia na samym początku wyjściowy bit pinu PC7 = 1 (do niego jest podłączona anoda diody, więc pin musi mieć stan niski, aby dioda świeciła)

PORTC:           | b7 | b6 | b5 | b4 | b3 | b2 | b1 | b0 |
LED_PIN:         | 1  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |

PORTC|LED_PIN:   | 1  | b6 | b5 | b4 | b3 | b2 | b1 | b0 |

                                                  --- o ---
									
DDRC |= LED_PIN     <- ustawia pin C7 jako wyjście
DDRC &= ~KEY_PIN    <- ustawia pin c6 jako wejście

Oba operatory mają podobny cel, pomimo zupełnie przeciwnego działania
Mają one za zadanie ustawienie określonych bitów rejestru DDRC tak, aby nie zmieniać innych.

DDRC |= LED_PIN  => DDRC = DDRC | LED_PIN
Tutaj mamy identyczną logikę, jak powyżej, czyli wymuszamy stan wysoki (1) na 7 bicie rejestru DDRC
Oznaczamy w ten sposób pin PC7 jako wyjście

DDRC &= ~KEY_PIN => DDRC = DDRC & ~KEY_PIN
Tym poleceniem ustawiamy stan niski (0) na 6 bicie rejestru DDRC oznaczając go jako wejście.

KEY_PIN:         | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  |
~KEY_PIN:        | 1  | 0  | 1  | 1  | 1  | 1  | 1  | 1  |
DDRC:            | b7 | b6 | b5 | b4 | b3 | b2 | b1 | b0 |

DDRC&~KEY_PIN:   | b7 } 0  | b5 | b4 | b3 | b2 | b1 | b0 |


