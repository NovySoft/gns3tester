# BGP IPv6 tesztelési jegyzőkönyv

## BGP router hiba (IPv6)

**Dátum:** 2026. 02. 10.

**A dokumentum célja:** A Yapper, Magentus és ICANN közötti BGP Peering kapcsolatok stabilitásának és redundanciájának tesztelése. A dokumentáció bemutatja, hogy specifikus hibaesetekben hogyan biztosított az internet és másik AS elérése a tartalék útvonalakon keresztül.

A tesztelés a `traceroute` parancs segítségével történt, a célcímek a következőek:
- Yapper és Magentus közötti kapcsolat tesztelése: Management hálózatok
	- Magentus esetén: `2001:470:2171:BBBB:BBBB::14`
	-  Yapper esetén: `2001:470:216F:AAAA::66`
- Internet kapcsolat teszteléséhez: `2001:4860:4860::8888`
- ICANN kapcsolat teszteléséhez a 'távolabbi' cím:
	- Magentus esetén: `172:30:30::30`
	- Yapper esetén: `172:29:29::30`

**Jelmagyarázat:** A tesztábrákon a szimulált hiba helyét vagy a megszakadt kapcsolatot <span style="color:red;font-weight:bold">piros vonal</span>, míg a hibatűrés miatt létrejött alternatív útvonalat <span style="color:orange;font-weight:bold">sárga szaggatott vonal</span> jelöli.

<div style="page-break-after: always;"></div>

### Hiba szimuláció: ICANN-R1 - IPv6 Ping

<img src="images/ipv6/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 500px">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:1:0:4 28ms 48ms 20ms</p>
    <img src="./images/ipv6/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:1:0:4 40ms 44ms 16ms</p>
    <img src="./images/ipv6/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:2:0:4 40ms 24ms 32ms</p>
    <img src="./images/ipv6/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:2:0:4 32ms 32ms 56ms</p>
    <img src="./images/ipv6/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 52ms 44ms 48ms</p>
    <img src="./images/ipv6/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 40ms 60ms 68ms</p>
    <img src="./images/ipv6/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 44ms 52ms 40ms</p>
    <img src="./images/ipv6/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 52ms 48ms 56ms</p>
    <img src="./images/ipv6/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: ICANN-R2 - IPv6 Ping

<img src="images/ipv6/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 500px">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:1:0:4 8ms 36ms 32ms</p>
    <img src="./images/ipv6/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:1:0:4 32ms 40ms 28ms</p>
    <img src="./images/ipv6/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:2:0:4 36ms 20ms 20ms</p>
    <img src="./images/ipv6/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:2:0:4 24ms 28ms 32ms</p>
    <img src="./images/ipv6/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 44ms 44ms 48ms</p>
    <img src="./images/ipv6/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 36ms 40ms 20ms</p>
    <img src="./images/ipv6/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 44ms 60ms 56ms</p>
    <img src="./images/ipv6/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 44ms 32ms 36ms</p>
    <img src="./images/ipv6/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: MAGENTUS-EDGE-R1 - IPv6 Ping

<img src="images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 500px">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:1:0:4 36ms 24ms 24ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:1:0:4 32ms 48ms 48ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:2:0:4 36ms 24ms 20ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:2:0:4 56ms 48ms 24ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 32ms 48ms 44ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 40ms 40ms 48ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 32ms 28ms 56ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 32ms 44ms 32ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: MAGENTUS-EDGE-R2 - IPv6 Ping

<img src="images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 500px">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:2:0:4 16ms 28ms 28ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:1:0:4 48ms 28ms 56ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:2:0:4 36ms 32ms 44ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:2:0:4 32ms 12ms 56ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 44ms 44ms 32ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 44ms 44ms 52ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 36ms 60ms 36ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 48ms 48ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: YAPPER-EDGE-R1 - IPv6 Ping

<img src="images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 500px">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:1:0:4 12ms 24ms 24ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:1:0:4 44ms 32ms 56ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:2:0:4 4ms 44ms 4ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:2:0:4 40ms 44ms 40ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 44ms 48ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 36ms 40ms 32ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 56ms 72ms 32ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 44ms 48ms 44ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: YAPPER-EDGE-R2 - IPv6 Ping

<img src="images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 500px">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:1:0:4 24ms 16ms 20ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:2:0:4 36ms 56ms 36ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 4 2001:470:2171:AAAA:AAAA:2:0:4 28ms 52ms 16ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 5 2001:470:2171:AAAA:AAAA:2:0:4 56ms 40ms 52ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 40ms 36ms 24ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 52ms 48ms 44ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 40ms 44ms 44ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:216F:AAAA::62 44ms 60ms 60ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Magentus-Yapper interconnect hiba (IPv6)

Yapper és Magentus BGP peer linkjei nem működik, kapcsolat ICANN-en keresztül

<img src="images/ipv6/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg" style="display: block; margin: 10px auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 76ms 48ms 56ms</p>
    <img src="./images/ipv6/yapper-magentus-bgpfail/MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:2:0:4 52ms 56ms 64ms</p>
    <img src="./images/ipv6/yapper-magentus-bgpfail/MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 44ms 64ms 60ms</p>
    <img src="./images/ipv6/yapper-magentus-bgpfail/MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:1:0:4 56ms 52ms 60ms</p>
    <img src="./images/ipv6/yapper-magentus-bgpfail/MAGENTUS-Customer4.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 80ms 68ms 60ms</p>
    <img src="./images/ipv6/yapper-magentus-bgpfail/YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 60ms 60ms 44ms</p>
    <img src="./images/ipv6/yapper-magentus-bgpfail/YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 88ms 56ms 60ms</p>
    <img src="./images/ipv6/yapper-magentus-bgpfail/YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 76ms 60ms 84ms</p>
    <img src="./images/ipv6/yapper-magentus-bgpfail/YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## ICANN R1 közvetlen kapcsolat hiba (IPv6)

ICANN R1 közvetlen összekötetése Magentus részéről megszakítva, kapcsolat Yapper-en keresztül

<img src="images/ipv6/icann-r1-fail/icann-r1-fail.svg" style="display: block; margin: 10px auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 172:29:29::30 44ms 56ms 36ms</p>
    <img src="./images/ipv6/icann-r1-fail/MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:29:29::30 48ms 56ms 56ms</p>
    <img src="./images/ipv6/icann-r1-fail/MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 172:29:29::30 36ms 44ms 44ms</p>
    <img src="./images/ipv6/icann-r1-fail/MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:29:29::30 48ms 48ms 68ms</p>
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
    <p><strong>Sikeres ping!</strong> 7 172:30:30::30 36ms 80ms 76ms</p>
    <img src="./images/ipv6/icann-r2-fail/YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:30:30::30 60ms 60ms 56ms</p>
    <img src="./images/ipv6/icann-r2-fail/YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:30:30::30 52ms 40ms 60ms</p>
    <img src="./images/ipv6/icann-r2-fail/YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 172:30:30::30 24ms 60ms 52ms</p>
    <img src="./images/ipv6/icann-r2-fail/YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Egyetlen útvonal ICANN-en keresztül (IPv6)

Minden közvetlen kapcsolat megszakítva, ICANN kapcsolatok redundanciája megszüntetve (1-1 link aktív)

<img src="images/ipv6/icann-single-path/icann-single-path.svg" style="display: block; margin: 10px auto; width: 400px;">

Ezen tesztnek a célja, hogy ellenőrizze, hogy megfelelően választódik ki az egyetlen lehetséges útvonal, nem jön létre routing loop az eBGP, iBGP és OSPF útvonalak között.

<div style="page-break-after: always;"></div>

### Útvonal: Mag-R1 - ICANN - Yap-R1

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:1:0:4 48ms 48ms 44ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:2:0:4 52ms 56ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 52ms 56ms 60ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:2:0:4 76ms 80ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 76ms 72ms 60ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 84ms 72ms 60ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 72ms 76ms 60ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 56ms 56ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R1-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Útvonal: Mag-R1 - ICANN - Yap-R2

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 68ms 56ms 64ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:1:0:4 84ms 52ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 44ms 52ms 60ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 7 2001:470:2171:AAAA:AAAA:1:0:4 60ms 60ms 72ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 40ms 64ms 80ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 56ms 76ms 64ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 60ms 56ms 84ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 48ms 76ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R1-Yap-R2-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Útvonal: Mag-R2 - ICANN - Yap-R1

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:1:0:4 64ms 64ms 40ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:2171:AAAA:AAAA:2:0:4 52ms 56ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 60ms 88ms 36ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:2171:AAAA:AAAA:2:0:4 48ms 56ms 52ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 104ms 76ms 84ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 60ms 56ms 44ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 52ms 72ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 76ms 84ms 72ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R1-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Útvonal: Mag-R2 - ICANN - Yap-R2

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 24ms 56ms 76ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:2171:AAAA:AAAA:1:0:4 60ms 64ms 80ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 6 2001:470:2171:AAAA:AAAA:2:0:4 44ms 60ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:2171:AAAA:AAAA:1:0:4 76ms 72ms 48ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 10px">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 72ms 72ms 80ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 76ms 76ms 56ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 8 2001:470:216F:AAAA::62 76ms 76ms 60ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 9 2001:470:216F:AAAA::62 72ms 52ms 72ms</p>
    <img src="./images/ipv6/icann-single-path/Mag-R2-Yap-R2-YAPPER-USER4.svg" width="100%">
  </div>
</div>