
BAJT a           | 1  | 1  | 1  | 1  | 0  | 0  | 0  | 0  |
NAJT b           | 1  | 0  | 1  | 0  | 1  | 0  | 1  | 0  |


Mnożenie bitowe
===================================
zapis a & b

Bit wynikowy jest równy 1 tylko, jeśli oba bity są równe 1

BAJT a           | 1  | 1  | 1  | 1  | 0  | 0  | 0  | 0  |
NAJT b           | 1  | 0  | 1  | 0  | 1  | 0  | 1  | 0  |
                 -----------------------------------------
a & b            | 1  | 0  | 1  | 0  | 0  | 0  | 0  | 0  |

Do czego się przydaje - do wymuszenia 0 na określonym bicie bez zmiany pozostałych - ustawienia stanu niskiego na pinie wyjściowym

BAJT b           | b7 | b6 | b5 | b4 | b3 | b2 | b1 | b0 |
BAJT a           | 1  | 1  | 0  | 1  | 1  | 1  | 0  | 1  |
                 -----------------------------------------
a & b            | b7 | b6 | 0  | b4 | b3 | b2 | 0  | b0 |
                            ----                ----


Sumowanie bitowe
===================================
zapis a | b

Bit wynikawy jest równy 1 jeśli co najmniej jeden z bitów a lub b jest równy 1

BAJT a           | 1  | 1  | 1  | 1  | 0  | 0  | 0  | 0  |
NAJT b           | 1  | 0  | 1  | 0  | 1  | 0  | 1  | 0  |
                 -----------------------------------------
a | b            | 1  | 1  | 1  | 1  | 1  | 0  | 1  | 0  |

Do czego się przydaje - do wymuszenia 1 na określonym bicie bez zmiany pozostałych - ustawienia stanu wysokiego na pinie wyjściowym

BAJT b           | b7 | b6 | b5 | b4 | b3 | b2 | b1 | b0 |
BAJT a           | 0  | 0  | 1  | 0  | 0  | 0  | 1  | 0  |
                 -----------------------------------------
a & b            | b7 | b6 | 1  | b4 | b3 | b2 | 1  | b0 |
                            ----                ----


Sumowanie bitowe modulo 2
===================================
zapis a ^ b

Bit wynikowy jest równy 1, kiedy odpowiadające sobie bity w a i b są różne

BAJT a           | 1  | 1  | 1  | 1  | 0  | 0  | 0  | 0  |
NAJT b           | 1  | 0  | 1  | 0  | 1  | 0  | 1  | 0  |
                 -----------------------------------------
a ^ b            | 0  | 1  | 0  | 1  | 1  | 0  | 1  | 0  |

Do czego się przydaje - do zmiany określonego bitu na przeciwny bez zmiany pozostałych - przęłączania pinu wyjściowego ON<>OFF

BAJT b           | b7 | b6 | b5 | b4 | b3 | b2 | b1 | b0 |
BAJT a           | 0  | 0  | 1  | 0  | 0  | 0  | 1  | 0  |
                 -----------------------------------------
a ^ b            | b7 | b6 |~b5 | b4 | b3 | b2 |~b1 | b0 |
                            ----                ----


Negacja bitowa
===================================
zapis ~a

BAJT a           | 1  | 1  | 1  | 1  | 0  | 0  | 0  | 0  |
                 -----------------------------------------
~a               | 0  | 0  | 0  | 0  | 1  | 1  | 1  | 1  |

Do czego się przydaje - do bardziej zaawansowanych operacji bitowych lub zmiany wszyskich pinów wyjściowych ON<>OFF

