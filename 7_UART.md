<img source="/pic/4145.p2.gif">

ATmega32 używa AVR USART - mający kilka dodatkowych funkcji w stosunku do AVR UART

 - Dodany drugi rejestr bufora; dzięki temu pracują jako bufor FIFO (first-in-first-out)
  - Odbiorczy rejestr przesuwający który może pełnić rolę trzeciego poziomu buforowania. Dzięki temu USART jest bardziej odporny na błędy przekroczenia limitu danych

