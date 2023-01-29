<img src="https://github.com/TechLabGH/BlueBook_dla_opornych/blob/main/pic/4145.p2.gif">

ATmega32 używa AVR USART - mający kilka dodatkowych funkcji w stosunku do AVR UART

 - Dodany drugi rejestr bufora; dzięki temu pracują jako bufor FIFO (first-in-first-out)
  - Odbiorczy rejestr przesuwający który może pełnić rolę trzeciego poziomu buforowania. Dzięki temu USART jest bardziej odporny na błędy przekroczenia limitu danych

USART obsługuje cztery tryby pracy zegara:
 - Asynchroniczny normalny
 - Asynchroniczny podwójnej szybkości
 - Synchroniczny Master
 - Synchroniczny Slave

Rejestr szybkości transmisji USART - **UBRR** (USART Baud Rate Refister).

Licznik wsteczny - pracuje w częstotliwością zegara systemowego , jest ładowany wartością UBRR po osiągnięciu wartości 0, lub gdy nastąpi zapis do rejestru UBRRL. Za każdym razem, gdy licznik osiągnie 0, generowany jest takt zegarowy

Wzory

###### Tryb asynchroniczny
_szybkość transmisji_

$$ f_T=\frac{f_{osc}}{16*(UBBR + 1)}$$

_wartość UBRR_

$$ UBRR = \frac{f_{osc}}{16*f_T}-1$$

###### Tryb asynchroniczny podwójnej szybkości (U2X = 1)
_szybkość transmisji_

$$ f_T=\frac{f_{osc}}{8*(UBBR + 1)}$$

_wartość UBRR_

$$ UBRR = \frac{f_{osc}}{8*f_T}-1$$

###### Tryb synchroniczny Master
_szybkość transmisji_

$$ f_T=\frac{f_{osc}}{2*(UBBR + 1)}$$

_wartość UBRR_

$$ UBRR = \frac{f_{osc}}{2*f_T}-1$$

$ f_{T}$ - szybkość transmisji w bitach na sekundę

$f_{osc}$ – częstotliwość zegarowa oscylatora systemowego

UBRR – zawartość rejestrów UBRRH i UBRRL (0...4095)

#### Praca z podwójną szybkością

Szybkość można podwoić przez ustawienie bitu U2X w rejestrze UCSRA - działa tylko w trybie pracy asynchronicznej. Przy pracy synchronicznej, powinien on być ustawiony na 0. 

#### Ramka szeregowej transmisji

Parametry ramki:
 - 1 bit startu
 - 5, 6, 7, 8 lub 9 bitów danych
 - brak, bit parzystości lub bit nieparzystości
 - 1 lub 2 bity stopu

 Format ramki ustawia się za pomocą bitów UCSZ[2:0], UPM[1:0] i USBS w rejestrach UCSRB i UCSRC.

## Rejestry USART

#### UDR – Rejestr danych we/wy USART

<table class="tg"><thead><tr><th class="tg-0pky"></th><th class="tg-c3ow">7</th><th class="tg-c3ow">6</th><th class="tg-c3ow">5</th><th class="tg-c3ow">4</th><th class="tg-c3ow">3</th><th class="tg-c3ow">2</th><th class="tg-c3ow">1</th><th class="tg-c3ow">0</th><th class="tg-0pky"></th></tr></thead><tbody><tr><td class="tg-9wq8" rowspan="2">0x0C (0x2C)</td><td class="tg-c3ow" colspan="8">RXB[7:0]</td><td class="tg-0pky">UDR (Odczyt)</td></tr><tr><td class="tg-c3ow" colspan="8">TXB[7:0]</td><td class="tg-0pky">UDR (Zapis)</td></tr><tr><td class="tg-0pky">Zapis/Odczyt</td><td class="tg-0pky">Z/O</td><td class="tg-0pky">Z/O</td><td class="tg-0pky">Z/O</td><td class="tg-0pky">Z/O</td><td class="tg-0pky">Z/O</td><td class="tg-0pky">Z/O</td><td class="tg-0pky">Z/O</td><td class="tg-0pky">Z/O</td><td class="tg-0pky"></td></tr></tbody></table>

#### UCSRA – Rejestr **A** sterowania i stanu USART

| 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|______|______|______|______|______|______|______|______|
|RXC  |TXC  |UDRE |FE   |DOR  |UPE  |U2X  |MPCM |

 - Bit 7 – RXC: Znacznik zakończenia odbioru USART - znacznik ustawiany, gdy w buforze odbiorczym znajdują się nieodczytane dane.

 - Bit 6 – TXC: Znacznik zakończenia nadawania USART - ustawiany, gdy cała ramka w nadawczym rejestrze przesuwającym została wysłana i nie ma nowych danych.

 - Bit 5 – UDRE: Znacznik pustego rejestru danych USART - znacznik wskazuje, że bufor nadawczy jest gotowy na przyjęcie nowych danych. Znacznik ten może generować przerwanie przy pustym rejestrze danych.

 - Bit 4 – FE: Znacznik błędu ramki - bit ustawiany, gdy dane w buforze odbiorczym miały błąd ramki przy odbiorze. Zawsze należy ustawić ten bit na zero przy zapisie do rejestru UCSRA.

 - Bit 3 – DOR: Znacznik przekroczenia ilości danych - bit zostaje ustawiony po wykryciu przekroczenia ilości danych. Zawsze należy ustawić ten bit na zero przy zapisie do rejestru UCSRA.

 - Bit 2 - UPE: Znacznik błędu parzystości USART - Bit ustawiany na 1, gdy następny ciąg bitów danych w buforze odbiorczym miał przy odbiorze błąd parzystości, a sprawdzanie parzystości w tym punkcie zostało włączone (UPM1 = 1)

 - Bit 1 – U2X: Podwojenie szybkości transmisji USART - bit ma znaczenie tylko przy pracy w trybie asynchronicznej. Powinien być ustawiony na 0 przy pracy synchronicznej.

 - Bit 0 – MPCM: Tryb komunikacji wieloprocesorowej

#### UCSRB –  Rejestr **B** sterowania i stanu USART

| 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|______|______|______|______|______|______|______|______|
|RXCIE|TXCIE|UDRIE|RXEN|TXEN|UCSZ2|RXB8|TXB8|

 - Bit 7 – RXCIE: Włączenie przerwań przy zakończeniu odbioru - uaktywnia przerwanie przy ustawieniu znacznik RXC. Przerwanie przy zakończeniu odczytu USART zostanie wygenerowane tylko wtedy, gdy ustawione na jeden są bity:
    - RXCIE, I w rejestrze stanu SREG
    - RXC w rejestrze UCSRA.

 - Bit 6 – TXCIE: Włączenie przerwań przy zakończeniu nadawania - włącza przerwania przy ustawieniu znacznika TXC. Przerwanie przy zakończeniu nadawania USART zostanie wygenerowane tylko wtedy, gdy ustawione na jeden są bity:
    - TXCIE, I w rejestrze stanu SREG
    - TXC w rejestrze UCSRA.

 - Bit 5 – UDRIE: USART Data Register Empty Interrupt Enable – Włączenie przerwań przy pustym rejestrze danych USART - włącza przerwania przy ustawieniu znacznika UDRE. Przerwanie przy pustym rejestrze danych USART zostanie wygenerowane tylko wtedy, gdy ustawione na jeden są bity:
    - UDRIE, I w rejestrze stanu SREG
    - UDRE w rejestrze UCSRA.

 - Bit 4 – RXEN: Włączenie odbiornika

 - Bit 3 – TXEN: Włączenie nadajnika

 - Bit 2 – UCSZ2: Długość ciągu bitów danych. Bit UCSZ2 w połączeniu z bitami UCSZ1:0 w rejestrze UCSRC ustawia liczbę bitów danych w ramce używanej przez odbiornik i nadajnik.

 - Bit 1 – RXB8: Odbiorczy bit danych nr 8. RXB8 jest dziewiątym bitem danych odebranego ciągu bitów, gdy odbiornik został ustawiony do pracy z ramkami szeregowymi zawierającymi dziewięć bitów danych. Należy go odczytać przed odczytem młodszych bitów z rejestru UDR.

 - Bit 0 – TXB8: Nadawczy bit danych nr 8

 #### UCSRC – Rejestr **C** sterowania i stanu USART

 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|______|______|______|______|______|______|______|______|
|URSEL|UMSEL|UPM1|UPM0|USBS|UCSZ1|UCSZ0|UCPOL|

 - Bit 7 – URSEL: Wybór rejestru - wybiera przy zapisie dostęp do rejestru UCSRC lub UBRRH. Przy odczycie bit ten daje stan jeden. Bit URSEL musi mieć wartość jeden przy zapisie do UCSRC.

 - Bit 6 – UMSEL: Wybór trybu USART - wybór pomiędzy asynchronicznym lub synchronicznym trybem pracy:
    - 0	Praca asynchroniczna
    - 1	Praca synchroniczna

 - Bity 5:4 – Tryb parzystości

|UPM1|UPM0|  |
|----|----|------------------|
|0   |0   |Wyłączony         |
|0   |1   |Zarezerwowane     |
|1   |0   |Parzystość        |
|1   |1   |Nieparzystość     |

 - Bit 3 – USBS: Wybór bitów stopu
    - 0: 1 bit stopu
    - 1: 2 bity stopu

 - Bit 2:1 – Liczba bitów danych w ramce

|UCSZ2|UCSZ1|UCSZ0|Liczba bitów danych w ramce|
|:---:|:---:|:---:|---------------------------|
|0    |0    |0    |5 bitów                    |
|0    |0    |1    |6 bitów                    |
|0    |1    |0    |7 bitów                    |
|0    |1    |1    |8 bitów                    |
|1    |0    |0    |Zarezerwowane              |
|1    |0    |1    |Zarezerwowane              |
|1    |1    |0    |Zarezerwowane              |
|1    |1    |1    |9 bitów                    |

 - Bit 0 – UCPOL: Polaryzacja zegara

|UCPOL|Zmiana danych wysyłanych|Próbkowanie danych odbieranych|
|-----|------------------------|------------------------------|
|0    |Narastające zbocze XCK  |Opadające zbocze XCK          |
|1    |Opadające zbocze XCK    |Narastające zbocze XCK        |

#### UBRRL i UBRRH – Rejestry szybkości transmisji USART

<table class="tg"><thead><tr><th class="tg-c3ow">15</th>
    <th class="tg-c3ow">14</th><th class="tg-c3ow">13</th><th class="tg-c3ow">12</th><th class="tg-c3ow">11</th><th class="tg-c3ow">10</th><th class="tg-c3ow">9</th><th class="tg-baqh">8</th><th class="tg-0lax"></th></tr></thead><tbody><tr><td class="tg-c3ow">URSEL</td><td class="tg-c3ow">-</td><td class="tg-c3ow">-</td>
    <td class="tg-c3ow">-</td><td class="tg-c3ow" colspan="4">UBRR[11:8]</td><td class="tg-0lax">UBRRH</td></tr><tr><td class="tg-c3ow" colspan="8">UBRR[7:0]</td><td class="tg-0lax">UBRRL</td></tr></tbody></table>

 - Bit 15 – URSEL: Wybór rejestru UBRRH lub UCSRC. Przy odczycie rejestru UBRRH bit ten ma wartość zero. Bit URSEL musi być wyzerowany podczas zapisu do UBRRH.

 - Bit 11:0 – UBRR11:0: Rejestr szybkości transmisji USART

## Ustawienia szybkości transmisji

<table class="tg">
<thead>
  <tr>
    <th class="tg-wa1i" rowspan="3">Szybkość<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;transmisji</th>
    <th class="tg-nrix" colspan="4">fosc = 1,0000 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 1,8432 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 2,0000 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 3,6864 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 4,0000 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 7,3728 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 8,0000 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 11,0592 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 14,7456 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 16,0000 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 18,4320 MHz</th>
    <th class="tg-nrix" colspan="4">fosc = 20.0000 MHz</th>
  </tr>
  <tr>
    <th class="tg-wa1i" colspan="2">UX2&nbsp;&nbsp;&nbsp;= 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
    <th class="tg-wa1i" colspan="2">UX2 = 0</th>
    <th class="tg-wa1i" colspan="2">UX2 = 1</th>
  </tr>
  <tr>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
    <th class="tg-wa1i">UBRR</th>
    <th class="tg-wa1i">Błąd</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-7zrl">2400</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">51</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">95</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">51</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">103</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">95</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">191</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">103</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">207</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">191</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">383</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">207</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">416</td>
    <td class="tg-7zrl">-0,1%</td>
    <td class="tg-7zrl">287</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">575</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">383</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">767</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">416</td>
    <td class="tg-7zrl">-0,1%</td>
    <td class="tg-7zrl">832</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">479</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">959</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">520</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1041</td>
    <td class="tg-7zrl">0,0%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">4800</td>
    <td class="tg-7zrl"> 12</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">51</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">95</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">51</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">103</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">95</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">191</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">103</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">207</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">143</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">287</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">191</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">383</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">207</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">416</td>
    <td class="tg-7zrl">-0,1%</td>
    <td class="tg-7zrl">239</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">479</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">259</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">520</td>
    <td class="tg-7zrl">0,0%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">9600</td>
    <td class="tg-7zrl">6</td>
    <td class="tg-7zrl">-7,0%</td>
    <td class="tg-7zrl">12</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">11</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">12</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">51</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">95</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">51</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">103</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">71</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">143</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">95</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">191</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">103</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">207</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">119</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">239</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">129</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">259</td>
    <td class="tg-7zrl">0,2%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">14,4k</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">-3,5%</td>
    <td class="tg-7zrl">7</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">15</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">-3,5%</td>
    <td class="tg-7zrl">16</td>
    <td class="tg-7zrl">2,1%</td>
    <td class="tg-7zrl">15</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">31</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">16</td>
    <td class="tg-7zrl">2,1%</td>
    <td class="tg-7zrl">34</td>
    <td class="tg-7zrl">-0,8%</td>
    <td class="tg-7zrl">31</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">63</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">34</td>
    <td class="tg-7zrl">-0,8%</td>
    <td class="tg-7zrl">68</td>
    <td class="tg-7zrl">0,6%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">95</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">63</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">127</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">68</td>
    <td class="tg-7zrl">0,6%</td>
    <td class="tg-7zrl">138</td>
    <td class="tg-7zrl">-0,1%</td>
    <td class="tg-7zrl">79</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">159</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">86</td>
    <td class="tg-7zrl">-0,2%</td>
    <td class="tg-7zrl">173</td>
    <td class="tg-7zrl">-0,2%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">19,2k</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">6</td>
    <td class="tg-7zrl">-7,0%</td>
    <td class="tg-7zrl">5</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">11</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">6</td>
    <td class="tg-7zrl">-7,0%</td>
    <td class="tg-7zrl">12</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">11</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">12</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">51</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">35</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">71</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">95</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl"> 51</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">103</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">59</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">119</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">64</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">129</td>
    <td class="tg-7zrl">0,2%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">28,8k</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">7</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">-3,5%</td>
    <td class="tg-7zrl">7</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">15</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">-3,5%</td>
    <td class="tg-7zrl">16</td>
    <td class="tg-7zrl">2,1%</td>
    <td class="tg-7zrl">15</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">31</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">16</td>
    <td class="tg-7zrl">2,1%</td>
    <td class="tg-7zrl">34</td>
    <td class="tg-7zrl">-0,8%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">31</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">63</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl"> 34</td>
    <td class="tg-7zrl">-0,8%</td>
    <td class="tg-7zrl">68</td>
    <td class="tg-7zrl">0,6%</td>
    <td class="tg-7zrl">39</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">79</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">42</td>
    <td class="tg-7zrl">0,9%</td>
    <td class="tg-7zrl">86</td>
    <td class="tg-7zrl">-0,2%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">38,4k</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">-18,6%</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">5</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">6</td>
    <td class="tg-7zrl">-7,0%</td>
    <td class="tg-7zrl">5</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">11</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">6</td>
    <td class="tg-7zrl">-7,0%</td>
    <td class="tg-7zrl">12</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">11</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">12</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">17</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">35</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">47</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl"> 0,2%</td>
    <td class="tg-7zrl">51</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">29</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">59</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">32</td>
    <td class="tg-7zrl">-1,4%</td>
    <td class="tg-7zrl">64</td>
    <td class="tg-7zrl">0,2%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">57,6k</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">7</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">-3,5%</td>
    <td class="tg-7zrl">7</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">15</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">-3,5%</td>
    <td class="tg-7zrl">16</td>
    <td class="tg-7zrl">2,1%</td>
    <td class="tg-7zrl">11</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">15</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">31</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl"> 16</td>
    <td class="tg-7zrl">2,1%</td>
    <td class="tg-7zrl">34</td>
    <td class="tg-7zrl">-0,8%</td>
    <td class="tg-7zrl">19</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">39</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">21</td>
    <td class="tg-7zrl">-1,4%</td>
    <td class="tg-7zrl">42</td>
    <td class="tg-7zrl">0,9%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">76,8k</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">-18,6%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">-25,0%</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">-18,6%</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">5</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">6</td>
    <td class="tg-7zrl">-7,0%</td>
    <td class="tg-7zrl">5</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">11</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">6</td>
    <td class="tg-7zrl">-7,0%</td>
    <td class="tg-7zrl">12</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">17</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">11</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">23</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">12</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">25</td>
    <td class="tg-7zrl">0,2%</td>
    <td class="tg-7zrl">14</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">29</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">15</td>
    <td class="tg-7zrl">1,7%</td>
    <td class="tg-7zrl">32</td>
    <td class="tg-7zrl">-1,4%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">115,2k</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0.085</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">7</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">-3,5%</td>
    <td class="tg-7zrl">5</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">11</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">7</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">15</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">-3,5%</td>
    <td class="tg-7zrl">16</td>
    <td class="tg-7zrl">2,1%</td>
    <td class="tg-7zrl">9</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">19</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">10</td>
    <td class="tg-7zrl">-1,4%</td>
    <td class="tg-7zrl">21</td>
    <td class="tg-7zrl">-1,4%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">230,4k</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">5</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">7</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">-3,5%</td>
    <td class="tg-7zrl">4</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl"> 9</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">4</td>
    <td class="tg-7zrl">8,5%</td>
    <td class="tg-7zrl">10</td>
    <td class="tg-7zrl">-1,4%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">250k</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">5</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">6</td>
    <td class="tg-7zrl">5,3%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">7</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">4</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">8</td>
    <td class="tg-7zrl">2,4%</td>
    <td class="tg-7zrl">4</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">9</td>
    <td class="tg-7zrl">0,0%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">0,5M</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">2</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">3</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl"> –</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">4</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">4</td>
    <td class="tg-7zrl">0,0%</td>
  </tr>
  <tr>
    <td class="tg-7zrl">1M</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">-7,8%</td>
    <td class="tg-7zrl">0</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">1</td>
    <td class="tg-7zrl">0,0%</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl"> –</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
    <td class="tg-7zrl">–</td>
  </tr>
  <tr>
    <td class="tg-4168">MAX</td>
    <td class="tg-4168" colspan="2">62,5 kbps</td>
    <td class="tg-4168" colspan="2">125 kbps</td>
    <td class="tg-4168" colspan="2">115,2 kbps</td>
    <td class="tg-4168" colspan="2">230,4 kbps</td>
    <td class="tg-4168" colspan="2">125 kbps</td>
    <td class="tg-4168" colspan="2">250 kbps</td>
    <td class="tg-4168" colspan="2">230,4 kbps</td>
    <td class="tg-4168" colspan="2">460,8 kbps</td>
    <td class="tg-4168" colspan="2">250 kbps</td>
    <td class="tg-4168" colspan="2">0,5 Mbps</td>
    <td class="tg-4168" colspan="2">460,8 kbps</td>
    <td class="tg-4168" colspan="2">921,6 kbps</td>
    <td class="tg-4168" colspan="2">0,5 Mbps</td>
    <td class="tg-4168" colspan="2">1 Mbps</td>
    <td class="tg-4168" colspan="2">691,2 kbps</td>
    <td class="tg-4168" colspan="2">1,3824 Mbps</td>
    <td class="tg-4168" colspan="2">921,6 kbps</td>
    <td class="tg-4168" colspan="2">1,8432 Mbps</td>
    <td class="tg-4168" colspan="2">1 Mbps</td>
    <td class="tg-4168" colspan="2">2 Mbps</td>
    <td class="tg-4168" colspan="2">1,152 Mbps</td>
    <td class="tg-4168" colspan="2">12,304 Mbps</td>
    <td class="tg-4168" colspan="2">1,25 Mbps</td>
    <td class="tg-4168" colspan="2">2,5 Mbps</td>
  </tr>
</tbody>
</table>

## Opis dzialania buforow w kodzie przykladowym

<img src="https://github.com/TechLabGH/BlueBook_dla_opornych/blob/main/pic/bufory.jpg">

#### main.c
```c
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "uart/uart.h"


int main(void) {

	USART_Init( __UBRR );                           // Wlaczenie UARTa
	sei();                                          // Wlaczenie przerwan

	uint8_t licznik,  pm = licznik = OSCCAL-20;	    // wskaznik kalibracyjny
	                                                // OSCCAL - jest rejestrem, gdzie przechowywane są dane
	                                                // kalibracyjne mikrokontrolera używane do precyzyjnego ustawienia
	                                                // wewnętrznego rezonatora. Jego rozkalibrowanie może spowodować zbyt
	                                                // dużą ilość błędów w komunikacji UART ale np. także błędy przy zapisie do EEPROM

	// petla
	while(1) {

		uart_puts("Test UART, wartosc OSCCAL = ");  // wysyla string
		uart_putint(licznik, 10);                   // wysyla liczbe
		uart_putc('\r');                            // wysyla CR (enter)
		uart_putc('\n');                            // wysyla LF (nowa linia)
		_delay_ms(500);
		OSCCAL = licznik++;                         // powieksz wskaznik kalibracyjny

		if(licznik > pm+40) licznik=pm;             // sprawdza kalibracje +/- 20
	}

}
```

#### uart.c
```c
#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>

#include "uart.h"

volatile char UART_RxBuf[UART_RX_BUF_SIZE];            // definicja zmiennej bufora wejsciowego
volatile uint8_t UART_RxHead;                          // indeks początku danych
volatile uint8_t UART_RxTail;                          // indeks konca danych

volatile char UART_TxBuf[UART_TX_BUF_SIZE];            // definicja zmiennej bufora wyjsciowego
volatile uint8_t UART_TxHead;                          // indeks poczatku danych
volatile uint8_t UART_TxTail;                          // indeks konca danych

void USART_Init( uint16_t baud ) {                     // ustaweinie predkosci
	UBRRH = (uint8_t)(baud>>8);                        // wpisanie bitów 8-11 do rejestru UBRRH
	UBRRL = (uint8_t)baud;                             // wpisanie bitów 0-7 do rejestru UBRRL
	UCSRB = (1<<RXEN)|(1<<TXEN);                       // wlaczenie Rx i Tx

	UCSRC = (1<<URSEL)|(3<<UCSZ0);                     // ustawienia transmisji
	                                                   // Ustawia 1 w bicie URSEL rejestru UCSRC - oznacza zmianę zapisywaną
	                                                   // w rejestrze UCSRC
	                                                   // Ustawia 2 w bicie UCSZ0 rejestru UCSRC - 6 bitowa ramka

	#ifdef UART_DE_PORT                                // konfiguracja pinu dla linii DE interefejsu RS485
		UART_DE_DIR |= UART_DE_BIT;                    // kierunek linii DE konwertera RS485
		UART_DE_ODBIERANIE;                            // usatwienie trybu odbierania jako domyślnego
	#endif

	#ifdef UART_DE_PORT                                // interefejs RS485
		UCSRB |= (1<<RXEN)|(1<<TXEN)|(1<<RXCIE)|(1<<TXCIE);  // ustawienie dodatkowego bitu TXCIE dla interfejsu RS485
		                                                     // bit ten wyzwala przerwanie przy zakończeniu nadawania
	#else
		UCSRB |= (1<<RXEN)|(1<<TXEN)|(1<<RXCIE);       // brak interfejsu RS485
	#endif
}

#ifdef UART_DE_PORT                                    // ustawienie przerwania po zakończeniu nadawania
ISR( USART_TXC_vect ) {                                // używane tylko do komunikacji po RS485
  UART_DE_PORT &= ~UART_DE_BIT;	                       // blokuje nadawanie RS485
}
#endif

void uart_putc( char data ) {                          // funkcja dodaje jeden bajt do bufora cyklicznego
	uint8_t tmp_head;                                  // delkaracja tymczasowego indeksu początku danych

    tmp_head  = (UART_TxHead + 1) & UART_TX_BUF_MASK;  // Przy pustym buforze: UART_TxHead = 0
                                                       // UART_TX_BUF_MASK = 15 (0b1111)
                                                       // czyli tpm_head = (1) & (15) = 1
                                                       // Przy trzech bajtach w buforze: UART_TxHead = 3
                                                       // czyli tmp_head = (4) & (15) = 4

    while ( tmp_head == UART_TxTail ){}                // Petla oczekuje w momencie wypełnionego całkowicie bufora

    UART_TxBuf[tmp_head] = data;                       // Dodanie otrzymanego w funkcji bajtu na poz tmp_head ciągu UART_TxBuf
    UART_TxHead = tmp_head;                            // Ustawienie nowego indeksu poczatku danych

    UCSRB |= (1<<UDRIE);                               // Włączamy generowanie przerwania przy pustym buforze. Przerwanie to będzie
                                                       // powodowało wyzwolenie procedury odpowiedzialnej za
                                                       // pobranie kolejnych bajtów z ciągu UART_TxBuf i ich wysłanie.
}


void uart_puts(char *s)		                           // Funkcja wysyłająca string
{
  register char c;
while ((c = *s++)) uart_putc(c);			           // Funcja po prostu wywołuje uart_putc() dla kolejnych znaków do czasu
                                                       // napotkania zera
}

void uart_putint(int value, int radix)                 // Funkcja wysyła zmienną INTIGER
{
	char string[17];			                       // bufor dla funkcji itoa
	itoa(value, string, radix);		                   // konwertuje liczbę ze zmiennej INT na STRING
	uart_puts(string);			                       // wysyła wynikowy string używając wcześniej zdefiniowanej funkcji
}

ISR( USART_UDRE_vect)  {                               // funkcja wysyłająca dane z bufora cyklicznego wywoływana przerwaniem

    if ( UART_TxHead != UART_TxTail ) {                // funkcja pracuje tak długo, jak gługo indeks poczatku i końca danych są
    	                                               // różne, co oznacza, że w UART_TxBuf[] znajdują się znaki do wysłania
    	UART_TxTail = (UART_TxTail + 1) & UART_TX_BUF_MASK;  // Przesuwa indeks końca danych o jedną pozycję
    	UDR = UART_TxBuf[UART_TxTail];                       // Wysyłamy ostatni znak do bufora UDR
    } else {
	UCSRB &= ~(1<<UDRIE);                              // po wysłaniu wszystkich znaków z UART_TxBuf[] wywoływanie przerwania
	                                                   // pustego bufora zostaje wyłączone
    }
}

char uart_getc(void) {                                 // funkcja pobierajaca 1 bajt z bufora wejsciowego

    if ( UART_RxHead == UART_RxTail ) return 0;        // jesli indeksy sa identyczne, zwracanay jest pousty znak oznaczajacy
                                                       // ze caly bufor zostal odczytany

    UART_RxTail = (UART_RxTail + 1) & UART_RX_BUF_MASK;      // Przesuwa indeks konca danych o jedna pozycje
    return UART_RxBuf[UART_RxTail];                          // Zwraca bajt znajdujacy sie na uaktualnionej pozycji
}

ISR( USART_RXC_vect ) {                                // obsluga przerwania odbiorczego - zapisuje dane do bufora wejsciosego
    uint8_t tmp_head;                                  // zdefiniowanie tymczasowego indeksu poczatkowego danych
    char data;                                         // zdefiniowanie bajtu pamieci na odebrane dane

    data = UDR;                                        // pobranie danych z bufora sprzetowego i zapisanie do pamieci

    tmp_head = ( UART_RxHead + 1) & UART_RX_BUF_MASK;  // obliczamy wartosc przesunietego indeksu poczatku danych i zapisujemy go
                                                       // do tymczasowej zmiennej

    if ( tmp_head == UART_RxTail ) {                   // porownujemy tymczasowy indeks konca danych z indeksem poczatku danych
    	                                               // w przypadku, kiedy sa one identyczne - oznacza to, ze bufor zostal
    	                                               // wypelniony i wpisywanie do niego kolejnych bajtow nadpisaloby juz
    	                                               // istniejace w nim dane
    } else {                                           // jesli nadal mamy miejsce w buforze to

	UART_RxHead = tmp_head; 		                   // ustawiamy uaktualniony idenks poczatku danych
	UART_RxBuf[tmp_head] = data; 	                   // wpisujemy odebrany bajt do bufora odbiorczego
    }
}


```

#### uart.h
```c
#ifndef UART_H_
#define UART_H_


#define UART_BAUD 115200		                            // definicja predkosci
#define __UBRR ((F_CPU+UART_BAUD*8UL) / (16UL*UART_BAUD)-1) // blicz UBBR

#define UART_DE_PORT PORTD                                  // ustawienie pinu DE dla konwertera RS 484
#define UART_DE_DIR  DDRD                                   // ustawienie pinu DE dla konwertera RS 484
#define UART_DE_BIT  (1<<PD2)                               // ustawienie pinu DE dla konwertera RS 484

#define UART_DE_ODBIERANIE UART_DE_PORT &= ~UART_DE_BIT     // ustawienie stanu na pinie DE dla konwertera RS 484
#define UART_DE_NADAWANIE  UART_DE_PORT |=  UART_DE_BIT     // ustawienie stanu na pinie DE dla konwertera RS 484
                                                            // powyższe ustawienia są niepoprawne w książce, na płycie DVD, ale także
                                                            // w przykładach wysyłanych elektronicznie nikomu nie chciało się ich
                                                            // poprawić

#define UART_RX_BUF_SIZE 32                                 // bufor wejsciowy
#define UART_RX_BUF_MASK ( UART_RX_BUF_SIZE - 1)            // maska bufora

#define UART_TX_BUF_SIZE 16                                 // bufor wyjsciowy
#define UART_TX_BUF_MASK ( UART_TX_BUF_SIZE - 1)            // maska bufora

void USART_Init( uint16_t baud );                           // definicje funkcji dostepnych przy wywolaniu biblioteki
char uart_getc( void );                                     //
void uart_putc( char data );                                // funkcja wysyla zmienna char
void uart_puts( char *s );                                  // funkcja wysyla string
void uart_putint( int value, int radix );                   // funkcja wysyla zmienną intiger

#endif

```
