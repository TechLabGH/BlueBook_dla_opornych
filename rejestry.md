## ATmega32 - rejestry

<table class="tg">
<thead>
  <tr>
    <th class="tg-1wig">Address</th>
    <th class="tg-1wig">Name</th>
    <th class="tg-1wig">Bit 7</th>
    <th class="tg-1wig">Bit 6</th>
    <th class="tg-1wig">Bit 5</th>
    <th class="tg-1wig">Bit 4</th>
    <th class="tg-1wig">Bit 3</th>
    <th class="tg-1wig">Bit 2</th>
    <th class="tg-1wig">Bit 1</th>
    <th class="tg-1wig">Bit 0</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0lax">$3F($5F)</td>
    <td class="tg-0lax">SREG</td>
    <td class="tg-baqh">I</td>
    <td class="tg-baqh">T</td>
    <td class="tg-baqh">H</td>
    <td class="tg-baqh">S</td>
    <td class="tg-baqh">V</td>
    <td class="tg-baqh">N</td>
    <td class="tg-baqh">Z</td>
    <td class="tg-baqh">C</td>
  </tr>
  <tr>
    <td class="tg-0lax">$3E($5E)</td>
    <td class="tg-0lax">SPH</td>
    <td class="tg-6qw1">-</td>
    <td class="tg-6qw1">-</td>
    <td class="tg-6qw1">-</td>
    <td class="tg-6qw1">-</td>
    <td class="tg-baqh">SP11</td>
    <td class="tg-baqh">SP10</td>
    <td class="tg-baqh">SP9</td>
    <td class="tg-baqh">SP8</td>
  </tr>
  <tr>
    <td class="tg-0lax">$3D($5D)</td>
    <td class="tg-0lax">SPL</td>
    <td class="tg-baqh">SP7</td>
    <td class="tg-baqh">SP6</td>
    <td class="tg-baqh">SP5</td>
    <td class="tg-baqh">SP4</td>
    <td class="tg-baqh">SP3</td>
    <td class="tg-baqh">SP2</td>
    <td class="tg-baqh">SP1</td>
    <td class="tg-baqh">SP0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$3C($5C)</td>
    <td class="tg-0lax">OCR0</td>
    <td class="tg-0lax" colspan="8">Timer/Counter0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$3B($5B)</td>
    <td class="tg-0lax">GICR</td>
    <td class="tg-baqh">INT1</td>
    <td class="tg-baqh">INT0</td>
    <td class="tg-baqh">INT2</td>
    <td class="tg-6qw1">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">IVSEL</td>
    <td class="tg-baqh">IVCE</td>
  </tr>
  <tr>
    <td class="tg-0lax">$3A($5A)</td>
    <td class="tg-0lax">GIFR</td>
    <td class="tg-baqh">INTF1</td>
    <td class="tg-baqh">INTF0</td>
    <td class="tg-baqh">INTF2</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
  </tr>
  <tr>
    <td class="tg-0lax">$39($59)</td>
    <td class="tg-0lax">TIMSK</td>
    <td class="tg-baqh">OCIE2</td>
    <td class="tg-baqh">TOIE2</td>
    <td class="tg-baqh">TICIE1</td>
    <td class="tg-baqh">OCIE1A</td>
    <td class="tg-baqh">OCIE1B</td>
    <td class="tg-baqh">TOIE1</td>
    <td class="tg-baqh">OCIE0</td>
    <td class="tg-baqh">TOIE0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$38($58)</td>
    <td class="tg-0lax">TIFR</td>
    <td class="tg-baqh">OCF2</td>
    <td class="tg-baqh">TOV2</td>
    <td class="tg-baqh">ICF1</td>
    <td class="tg-baqh">OCF1A</td>
    <td class="tg-baqh">OCF1B</td>
    <td class="tg-baqh">TOV1</td>
    <td class="tg-baqh">OCF0</td>
    <td class="tg-baqh">TOV0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$37($57)</td>
    <td class="tg-0lax">SPMCR</td>
    <td class="tg-baqh">SPMIE</td>
    <td class="tg-baqh">RWWSB</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">RWWSRE</td>
    <td class="tg-baqh">BLBSET</td>
    <td class="tg-baqh">PGWRT</td>
    <td class="tg-baqh">PGERS</td>
    <td class="tg-baqh">SPMEN</td>
  </tr>
  <tr>
    <td class="tg-0lax">$36($56)</td>
    <td class="tg-0lax">TWCR</td>
    <td class="tg-baqh">TWINT</td>
    <td class="tg-baqh">TWEA</td>
    <td class="tg-baqh">TWSTA</td>
    <td class="tg-baqh">TWSTO</td>
    <td class="tg-baqh">TWWC</td>
    <td class="tg-baqh">TWEN</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">TWIE</td>
  </tr>
  <tr>
    <td class="tg-0lax">$35($55)</td>
    <td class="tg-0lax">MCUCR</td>
    <td class="tg-baqh">SE</td>
    <td class="tg-baqh">SM2</td>
    <td class="tg-baqh">SM1</td>
    <td class="tg-baqh">SM0</td>
    <td class="tg-baqh">ISC11</td>
    <td class="tg-baqh">ISC10</td>
    <td class="tg-baqh">ISC01</td>
    <td class="tg-baqh">ISC00</td>
  </tr>
  <tr>
    <td class="tg-0lax">$34($54)</td>
    <td class="tg-0lax">MCUCSR</td>
    <td class="tg-baqh">JTD</td>
    <td class="tg-baqh">ISC2</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">JTRF</td>
    <td class="tg-baqh">WDRF</td>
    <td class="tg-baqh">BORF</td>
    <td class="tg-baqh">EXTRF</td>
    <td class="tg-baqh">PORF</td>
  </tr>
  <tr>
    <td class="tg-0lax">$33($53)</td>
    <td class="tg-0lax">TCCR0</td>
    <td class="tg-baqh">FOC0</td>
    <td class="tg-baqh">WGM00</td>
    <td class="tg-baqh">COM01</td>
    <td class="tg-baqh">COM00</td>
    <td class="tg-baqh">WGM01</td>
    <td class="tg-baqh">CS02</td>
    <td class="tg-baqh">CS01</td>
    <td class="tg-baqh">CS00</td>
  </tr>
  <tr>
    <td class="tg-0lax">$32($52)</td>
    <td class="tg-0lax">TCNT0</td>
    <td class="tg-0lax" colspan="8">Timer/Counter0 (8 Bits)</td>
  </tr>
  <tr>
    <td class="tg-0lax" rowspan="2">$31($51)</td>
    <td class="tg-0lax">OSCCAL</td>
    <td class="tg-0lax" colspan="8">Oscillator Calibration Register</td>
  </tr>
  <tr>
    <td class="tg-0lax">OCDR</td>
    <td class="tg-0lax" colspan="8">On-Chip Debug Register</td>
  </tr>
  <tr>
    <td class="tg-0lax">$30($50)</td>
    <td class="tg-0lax">SFIOR</td>
    <td class="tg-baqh">ADTS2</td>
    <td class="tg-baqh">ADTS1</td>
    <td class="tg-baqh">ADTS0</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">ACME</td>
    <td class="tg-baqh">PUD</td>
    <td class="tg-baqh">PSR2</td>
    <td class="tg-baqh">PSR10</td>
  </tr>
  <tr>
    <td class="tg-0lax">$2F($4F)</td>
    <td class="tg-0lax">TCCR1A</td>
    <td class="tg-baqh">COM1A1</td>
    <td class="tg-baqh">COM1A0</td>
    <td class="tg-baqh">COM1B1</td>
    <td class="tg-baqh">COM1B0</td>
    <td class="tg-baqh">FOC1A</td>
    <td class="tg-baqh">FOC1B</td>
    <td class="tg-baqh">WGM11</td>
    <td class="tg-baqh">WGM10</td>
  </tr>
  <tr>
    <td class="tg-0lax">$2E($4E)</td>
    <td class="tg-0lax">TCCR1B</td>
    <td class="tg-baqh">ICNC1</td>
    <td class="tg-baqh">ICES1</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">WGM13</td>
    <td class="tg-baqh">WGM12</td>
    <td class="tg-baqh">CS12</td>
    <td class="tg-baqh">CS11</td>
    <td class="tg-baqh">CS10</td>
  </tr>
  <tr>
    <td class="tg-0lax">$2D($4D)</td>
    <td class="tg-0lax">TCNT1H</td>
    <td class="tg-0lax" colspan="8">Timer/Counter1 ? Counter Register High Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$2C($4C)</td>
    <td class="tg-0lax">TCNT1L</td>
    <td class="tg-0lax" colspan="8">Timer/Counter1 ? Counter Register Low Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$2B($4B)</td>
    <td class="tg-0lax">OCR1AH</td>
    <td class="tg-0lax" colspan="8">Timer/Counter1 ? Output Compare Register A High Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$2A($4A)</td>
    <td class="tg-0lax">OCR1AL</td>
    <td class="tg-0lax" colspan="8">Timer/Counter1 ? Output Compare Register A Low Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$29($49)</td>
    <td class="tg-0lax">OCR1BH</td>
    <td class="tg-0lax" colspan="8">Timer/Counter1 ? Output Compare Register B High Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$28($48)</td>
    <td class="tg-0lax">OCR1BL</td>
    <td class="tg-0lax" colspan="8">Timer/Counter1 ? Output Compare Register B Low Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$27($47)</td>
    <td class="tg-0lax">ICR1H</td>
    <td class="tg-0lax" colspan="8">Timer/Counter1 ? Input Capture Register High Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$26($46)</td>
    <td class="tg-0lax">ICR1L</td>
    <td class="tg-0lax" colspan="8">Timer/Counter1 ? Input Capture Register Low Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$25($45)</td>
    <td class="tg-0lax">TCCR2</td>
    <td class="tg-baqh">FOC2</td>
    <td class="tg-baqh">WGM20</td>
    <td class="tg-baqh">COM21</td>
    <td class="tg-baqh">COM20</td>
    <td class="tg-baqh">WGM21</td>
    <td class="tg-baqh">CS22</td>
    <td class="tg-baqh">CS21</td>
    <td class="tg-baqh">CS20</td>
  </tr>
  <tr>
    <td class="tg-0lax">$24($44)</td>
    <td class="tg-0lax">TCNT2</td>
    <td class="tg-0lax" colspan="8">Timer/Counter2 (8 Bits)</td>
  </tr>
  <tr>
    <td class="tg-0lax">$23($43)</td>
    <td class="tg-0lax">OCR2</td>
    <td class="tg-0lax" colspan="8">Timer/Counter2 Output Compare Register</td>
  </tr>
  <tr>
    <td class="tg-0lax">$22($42)</td>
    <td class="tg-0lax">ASSR</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">AS2</td>
    <td class="tg-baqh">TCN2UB</td>
    <td class="tg-baqh">OCR2UB</td>
    <td class="tg-baqh">TCR2UB</td>
  </tr>
  <tr>
    <td class="tg-0lax">$21($41)</td>
    <td class="tg-0lax">WDTCR</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">WDTOE</td>
    <td class="tg-baqh">WDE</td>
    <td class="tg-baqh">WDP2</td>
    <td class="tg-baqh">WDP1</td>
    <td class="tg-baqh">WDP0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$20($40)</td>
    <td class="tg-0lax">UBRRH</td>
    <td class="tg-baqh">URSEL</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-0lax" colspan="4">UBRR[11:8]</td>
  </tr>
  <tr>
    <td class="tg-0lax"></td>
    <td class="tg-0lax">UCSRC</td>
    <td class="tg-baqh">URSEL</td>
    <td class="tg-baqh">UMSEL</td>
    <td class="tg-baqh">UPM1</td>
    <td class="tg-baqh">UPM0</td>
    <td class="tg-baqh">USBS</td>
    <td class="tg-baqh">UCSZ1</td>
    <td class="tg-baqh">UCSZ0</td>
    <td class="tg-baqh">UCPOL</td>
  </tr>
  <tr>
    <td class="tg-0lax">$1F($3F)</td>
    <td class="tg-0lax">EEARH</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">EEAR9</td>
    <td class="tg-baqh">EEAR8</td>
  </tr>
  <tr>
    <td class="tg-0lax">$1E($3E)</td>
    <td class="tg-0lax">EEARL</td>
    <td class="tg-0lax" colspan="8">EEPROM Address Register Low Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$1D($3D)</td>
    <td class="tg-0lax">EEDR</td>
    <td class="tg-0lax" colspan="8">EEPROM Data Register</td>
  </tr>
  <tr>
    <td class="tg-0lax">$1C($3C)</td>
    <td class="tg-0lax">EECR</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">EERIE</td>
    <td class="tg-baqh">EEMWE</td>
    <td class="tg-baqh">EEWE</td>
    <td class="tg-baqh">EERE</td>
  </tr>
  <tr>
    <td class="tg-0lax">$1B($3B)</td>
    <td class="tg-0lax">PORTA</td>
    <td class="tg-baqh">PORTA7</td>
    <td class="tg-baqh">PORTA6</td>
    <td class="tg-baqh">PORTA5</td>
    <td class="tg-baqh">PORTA4</td>
    <td class="tg-baqh">PORTA3</td>
    <td class="tg-baqh">PORTA2</td>
    <td class="tg-baqh">PORTA1</td>
    <td class="tg-baqh">PORTA0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$1A($3A)</td>
    <td class="tg-0lax">DDRA</td>
    <td class="tg-baqh">DDA7</td>
    <td class="tg-baqh">DDA6</td>
    <td class="tg-baqh">DDA5</td>
    <td class="tg-baqh">DDA4</td>
    <td class="tg-baqh">DDA3</td>
    <td class="tg-baqh">DDA2</td>
    <td class="tg-baqh">DDA1</td>
    <td class="tg-baqh">DDA0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$19($39)</td>
    <td class="tg-0lax">PINA</td>
    <td class="tg-baqh">PINA7</td>
    <td class="tg-baqh">PINA6</td>
    <td class="tg-baqh">PINA5</td>
    <td class="tg-baqh">PINA4</td>
    <td class="tg-baqh">PINA3</td>
    <td class="tg-baqh">PINA2</td>
    <td class="tg-baqh">PINA1</td>
    <td class="tg-baqh">PINA0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$18($38)</td>
    <td class="tg-0lax">PORTB</td>
    <td class="tg-baqh">PORTB7</td>
    <td class="tg-baqh">PORTB6</td>
    <td class="tg-baqh">PORTB5</td>
    <td class="tg-baqh">PORTB4</td>
    <td class="tg-baqh">PORTB3</td>
    <td class="tg-baqh">PORTB2</td>
    <td class="tg-baqh">PORTB1</td>
    <td class="tg-baqh">PORTB0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$17($37)</td>
    <td class="tg-0lax">DDRB</td>
    <td class="tg-baqh">DDB7</td>
    <td class="tg-baqh">DDB6</td>
    <td class="tg-baqh">DDB5</td>
    <td class="tg-baqh">DDB4</td>
    <td class="tg-baqh">DDB3</td>
    <td class="tg-baqh">DDB2</td>
    <td class="tg-baqh">DDB1</td>
    <td class="tg-baqh">DDB0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$16($36)</td>
    <td class="tg-0lax">PINB</td>
    <td class="tg-baqh">PINB7</td>
    <td class="tg-baqh">PINB6</td>
    <td class="tg-baqh">PINB5</td>
    <td class="tg-baqh">PINB4</td>
    <td class="tg-baqh">PINB3</td>
    <td class="tg-baqh">PINB2</td>
    <td class="tg-baqh">PINB1</td>
    <td class="tg-baqh">PINB0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$15($35)</td>
    <td class="tg-0lax">PORTC</td>
    <td class="tg-baqh">PORTC7</td>
    <td class="tg-baqh">PORTC6</td>
    <td class="tg-baqh">PORTC5</td>
    <td class="tg-baqh">PORTC4</td>
    <td class="tg-baqh">PORTC3</td>
    <td class="tg-baqh">PORTC2</td>
    <td class="tg-baqh">PORTC1</td>
    <td class="tg-baqh">PORTC0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$14($34)</td>
    <td class="tg-0lax">DDRC</td>
    <td class="tg-baqh">DDC7</td>
    <td class="tg-baqh">DDC6</td>
    <td class="tg-baqh">DDC5</td>
    <td class="tg-baqh">DDC4</td>
    <td class="tg-baqh">DDC3</td>
    <td class="tg-baqh">DDC2</td>
    <td class="tg-baqh">DDC1</td>
    <td class="tg-baqh">DDC0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$13($33)</td>
    <td class="tg-0lax">PINC</td>
    <td class="tg-baqh">PINC7</td>
    <td class="tg-baqh">PINC6</td>
    <td class="tg-baqh">PINC5</td>
    <td class="tg-baqh">PINC4</td>
    <td class="tg-baqh">PINC3</td>
    <td class="tg-baqh">PINC2</td>
    <td class="tg-baqh">PINC1</td>
    <td class="tg-baqh">PINC0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$12($32)</td>
    <td class="tg-0lax">PORTD</td>
    <td class="tg-baqh">PORTD7</td>
    <td class="tg-baqh">PORTD6</td>
    <td class="tg-baqh">PORTD5</td>
    <td class="tg-baqh">PORTD4</td>
    <td class="tg-baqh">PORTD3</td>
    <td class="tg-baqh">PORTD2</td>
    <td class="tg-baqh">PORTD1</td>
    <td class="tg-baqh">PORTD0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$11($31)</td>
    <td class="tg-0lax">DDRD</td>
    <td class="tg-baqh">DDD7</td>
    <td class="tg-baqh">DDD6</td>
    <td class="tg-baqh">DDD5</td>
    <td class="tg-baqh">DDD4</td>
    <td class="tg-baqh">DDD3</td>
    <td class="tg-baqh">DDD2</td>
    <td class="tg-baqh">DDD1</td>
    <td class="tg-baqh">DDD0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$10($30)</td>
    <td class="tg-0lax">PIND</td>
    <td class="tg-baqh">PIND7</td>
    <td class="tg-baqh">PIND6</td>
    <td class="tg-baqh">PIND5</td>
    <td class="tg-baqh">PIND4</td>
    <td class="tg-baqh">PIND3</td>
    <td class="tg-baqh">PIND2</td>
    <td class="tg-baqh">PIND1</td>
    <td class="tg-baqh">PIND0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$0F($2F)</td>
    <td class="tg-0lax">SPDR</td>
    <td class="tg-0lax" colspan="8">SPI Data Register</td>
  </tr>
  <tr>
    <td class="tg-0lax">$0E($2E)</td>
    <td class="tg-0lax">SPSR</td>
    <td class="tg-baqh">SPIF</td>
    <td class="tg-baqh">WCOL</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">SPI2X</td>
  </tr>
  <tr>
    <td class="tg-0lax">$0D($2D)</td>
    <td class="tg-0lax">SPCR</td>
    <td class="tg-baqh">SPIE</td>
    <td class="tg-baqh">SPE</td>
    <td class="tg-baqh">DORD</td>
    <td class="tg-baqh">MSTR</td>
    <td class="tg-baqh">CPOL</td>
    <td class="tg-baqh">CPHA</td>
    <td class="tg-baqh">SPR1</td>
    <td class="tg-baqh">SPR0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$0C($2C)</td>
    <td class="tg-0lax">UDR</td>
    <td class="tg-0lax" colspan="8">USART I/O Data Register</td>
  </tr>
  <tr>
    <td class="tg-0lax">$0B($2B)</td>
    <td class="tg-0lax">UCSRA</td>
    <td class="tg-baqh">RXC</td>
    <td class="tg-baqh">TXC</td>
    <td class="tg-baqh">UDRE</td>
    <td class="tg-baqh">FE</td>
    <td class="tg-baqh">DOR</td>
    <td class="tg-baqh">PE</td>
    <td class="tg-baqh">U2X</td>
    <td class="tg-baqh">MPCM</td>
  </tr>
  <tr>
    <td class="tg-0lax">$0A($2A)</td>
    <td class="tg-0lax">UCSRB</td>
    <td class="tg-baqh">RXCIE</td>
    <td class="tg-baqh">TXCIE</td>
    <td class="tg-baqh">UDRIE</td>
    <td class="tg-baqh">RXEN</td>
    <td class="tg-baqh">TXEN</td>
    <td class="tg-baqh">UCSZ2</td>
    <td class="tg-baqh">RXB8</td>
    <td class="tg-baqh">TXB8</td>
  </tr>
  <tr>
    <td class="tg-0lax">$9($29)</td>
    <td class="tg-0lax">UBRRL</td>
    <td class="tg-0lax" colspan="8">USART Baud Rate Register Low Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$8($28)</td>
    <td class="tg-0lax">ACSR</td>
    <td class="tg-baqh">ACD</td>
    <td class="tg-baqh">ACBG</td>
    <td class="tg-baqh">ACO</td>
    <td class="tg-baqh">ACI</td>
    <td class="tg-baqh">ACIE</td>
    <td class="tg-baqh">ACIC</td>
    <td class="tg-baqh">ACIS1</td>
    <td class="tg-baqh">ACIS0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$7($27)</td>
    <td class="tg-0lax">ADMUX</td>
    <td class="tg-baqh">REFS1</td>
    <td class="tg-baqh">REFS0</td>
    <td class="tg-baqh">ADLAR</td>
    <td class="tg-baqh">MUX4</td>
    <td class="tg-baqh">MUX3</td>
    <td class="tg-baqh">MUX2</td>
    <td class="tg-baqh">MUX1</td>
    <td class="tg-baqh">MUX0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$6($26)</td>
    <td class="tg-0lax">ADCSRA</td>
    <td class="tg-baqh">ADEN</td>
    <td class="tg-baqh">ADSC</td>
    <td class="tg-baqh">ADATE</td>
    <td class="tg-baqh">ADIF</td>
    <td class="tg-baqh">ADIE</td>
    <td class="tg-baqh">ADPS2</td>
    <td class="tg-baqh">ADPS1</td>
    <td class="tg-baqh">ADPS0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$5($25)</td>
    <td class="tg-0lax">ADCH</td>
    <td class="tg-0lax" colspan="8">ADC Data Register High Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$4($24)</td>
    <td class="tg-0lax">ADCL</td>
    <td class="tg-0lax" colspan="8">ADC Data Register Low Byte</td>
  </tr>
  <tr>
    <td class="tg-0lax">$3($23)</td>
    <td class="tg-0lax">TWDR</td>
    <td class="tg-0lax" colspan="8">Two-wire Serial Interface Data Register</td>
  </tr>
  <tr>
    <td class="tg-0lax">$2($22)</td>
    <td class="tg-0lax">TWAR</td>
    <td class="tg-baqh">TWA6</td>
    <td class="tg-baqh">TWA5</td>
    <td class="tg-baqh">TWA4</td>
    <td class="tg-baqh">TWA3</td>
    <td class="tg-baqh">TWA2</td>
    <td class="tg-baqh">TWA1</td>
    <td class="tg-baqh">TWA0</td>
    <td class="tg-baqh">TWGCE</td>
  </tr>
  <tr>
    <td class="tg-0lax">$01($21)</td>
    <td class="tg-0lax">TWSR</td>
    <td class="tg-baqh">TWS7</td>
    <td class="tg-baqh">TWS6</td>
    <td class="tg-baqh">TWS5</td>
    <td class="tg-baqh">TWS4</td>
    <td class="tg-baqh">TWS3</td>
    <td class="tg-c7wh">-</td>
    <td class="tg-baqh">TWPS1</td>
    <td class="tg-baqh">TWPS0</td>
  </tr>
  <tr>
    <td class="tg-0lax">$00($20)</td>
    <td class="tg-0lax">TWBR</td>
    <td class="tg-0lax" colspan="8">Two-wire Serial Interface Bit Rate Register</td>
  </tr>
</tbody>
</table>
