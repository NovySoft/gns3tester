# BGP IPv6 tesztelési jegyzőkönyv

## BGP router hiba (IPv6)

<div style="page-break-after: always;"></div>

## Egyetlen útvonal ICANN-en keresztül (IPv6)

Minden közvetlen kapcsolat megszakítva, ICANN kapcsolatok redundanciája megszüntetve (1-1 link aktív)

<img src="images/ipv6/icann-single-path/icann-single-path.svg" style="display: block; margin: 10px auto; width: 400px;">

### Útvonal: Mag-R1 - ICANN - Yap-R1

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:2:0:4 28ms 52ms 20ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:1:0:4 48ms 68ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:2:0:4 40ms 48ms 52ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:2:0:4 36ms 56ms 40ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 68ms 72ms 60ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 64ms 60ms 52ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 56ms 52ms 72ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 52ms 60ms 48ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-YAPPER-USER4.svg" width="100%">
  </div>
</div>

### Útvonal: Mag-R1 - ICANN - Yap-R2

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:1:0:4 56ms 80ms 28ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:1:0:4 60ms 76ms 60ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:2:0:4 44ms 60ms 44ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:2:0:4 60ms 72ms 52ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 60ms 56ms 68ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 76ms 56ms 68ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 96ms 76ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 76ms 48ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-YAPPER-USER4.svg" width="100%">
  </div>
</div>

### Útvonal: Mag-R2 - ICANN - Yap-R1

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 56ms 60ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:2171:AAAA:AAAA:1:0:4 56ms 64ms 40ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 68ms 56ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:2171:AAAA:AAAA:2:0:4 56ms 40ms 52ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 88ms 80ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 72ms 60ms 64ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 64ms 48ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 92ms 48ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-YAPPER-USER4.svg" width="100%">
  </div>
</div>

### Útvonal: Mag-R2 - ICANN - Yap-R2

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:1:0:4 36ms 60ms 36ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:2171:AAAA:AAAA:1:0:4 44ms 40ms 48ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 40ms 48ms 40ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:2171:AAAA:AAAA:2:0:4 84ms 40ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 56ms 40ms 80ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 64ms 84ms 60ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 60ms 64ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 72ms 60ms 72ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

