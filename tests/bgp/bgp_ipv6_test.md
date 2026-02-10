# BGP IPv6 tesztelési jegyzőkönyv

## BGP router hiba (IPv6)

<div style="page-break-after: always;"></div>

## ICANN R1 közvetlen kapcsolat hiba (IPv6)

ICANN R1 közvetlen összekötetése Magentus részéről megszakítva, kapcsolat Yapper-en keresztül

<img src="images/ipv6/icann-r1-fail/icann-r1-fail.svg" style="display: block; margin: 10px auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 172:29:29::30 36ms 56ms 52ms</p>
    <img src="./images/ipv6/icann-r1-fail/MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:29:29::30 52ms 60ms 32ms</p>
    <img src="./images/ipv6/icann-r1-fail/MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 172:29:29::30 68ms 20ms 56ms</p>
    <img src="./images/ipv6/icann-r1-fail/MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:29:29::30 36ms 44ms 48ms</p>
    <img src="./images/ipv6/icann-r1-fail/MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## ICANN R2 közvetlen kapcsolat hiba (IPv6)

ICANN R2 közvetlen összekötetése Yapper részéről megszakítva, kapcsolat Magentus-on keresztül

<img src="images/ipv6/icann-r2-fail/icann-r2-fail.svg" style="display: block; margin: 10px auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:30:30::30 60ms 56ms 60ms</p>
    <img src="./images/ipv6/icann-r2-fail/YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:30:30::30 40ms 40ms 60ms</p>
    <img src="./images/ipv6/icann-r2-fail/YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:30:30::30 44ms 52ms 48ms</p>
    <img src="./images/ipv6/icann-r2-fail/YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:30:30::30 56ms 56ms 40ms</p>
    <img src="./images/ipv6/icann-r2-fail/YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

