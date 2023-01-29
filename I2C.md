## PCF8583 - Real time clock

Nota katalogowa: https://www.mouser.com/datasheet/2/302/PCF8583-1127587.pdf

#### Najwazniejsze informacje:

PCF8583 posiada 
* 256 bajtow pamieci RAM
* 8 bitowy rejestr adresu
* 32.768 kHz oscylator
* dzielnik czestotliwosci
* magistrale I2C

Pierwsze 16 bajtow pamieci RAM (00h do 0Fh) wykorzystywane jest jako 8-bitowe rejestry specjalne:
* 00h - rejestr konfigurayjny i przechowujacy statusy
* 01h do 07h - liczniki uzywane przez funkcje zegara
* 08h do 0Fh - moga byc skonfigurowane do ustawienia alarmow albo wykorzystane jak normalna pamiec RAM (jesli alarmy sa wylaczone)

#### Rejestry

###### komorka pamieci 00h
 MSB ---------------------------------- LSB 

|  7  |  6  |  5  |  4  |  3  |  2  |  1  |  0  | 
|-----|-----|-----|-----|-----|-----|-----|-----|

* BIT 7 - flaga licznika
  *  0 - zlicza pulsy
  *  1 - zatrzymuje zliczanie, resetuje dzielnik
* BIT6 - flaga przechowywania stanu licznika
  *  0 - zliczj
  *  1 - przechowuj ostatni stan licznika
* BIT 5-4 - function mode
  *  00 - tryb 32.768 kHz
  *  01 - tryb 50 Hz
  *  10 - tryb zliczania "eventow"
  *  11 - tryb testowy
* BIT 3 - flaga maski
  *  0 - odczytuje rejestry 05h do 06h niemaskowwane
  *  1 - bezposrednio odczytuje licznik dni i miesięcy
* BIT 2 - kotrola alarmu
  *  0 - alarm wylaczony 
  *  1 - alarm wlaczony
* BIT 1 = alarm flag: 50 % duty factor minutes flag if alarm enable bit is logic 0
* BIT 0 - timer flag: 50 % duty factor seconds flag if alarm enable bit is logic 0

###### rejestry licznikow

**Komorka pamieci 04h (licznik godzin)**
Bit7: 0 - formar 24h / 1 - format 12h
Bit6: 0 - AM / 1 - PM
Bit5-4: miejsca dziesietne (0-2)
Bit3-0: hodziny w formacie BCD

**Komorka pamieci 05h (licznik roku i daty)**
Bit7-6: rok
Bit5-4: miejsca dziesietne (0-3)
Bit3-0: dniy w formacie BCD

**Komorka pamieci 06h (licznik dnia tygodnia i miesiaca)**
Bit7-5: dzien tygodnia (0-6)
Bit4: miejsca dziesietne 
Bit3-0: miesiac w formacie BCD

... i to tylko mały ułamek tego, co zostało udokumentowane w nocie katalogowej.

