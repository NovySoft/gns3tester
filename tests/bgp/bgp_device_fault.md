# BGP tesztelési jegyzőkönyv

## BGP router hiba

**Dátum:** 2026. 02. 02.

**A dokumentum célja:** A Yapper, Magentus és ICANN közötti BGP Peering kapcsolatok stabilitásának és redundanciájának tesztelése. A dokumentáció bemutatja, hogy specifikus hibaesetekben hogyan biztosított az internet és másik AS elérése a tartalék útvonalakon keresztül.

A tesztelés a `traceroute` parancs segítségével történt, a célcímek a következőek:
- Yapper és Magentus közötti kapcsolat tesztelése: Management hálózatok
	- Magentus esetén: `172.16.255.1`
	-  Yapper esetén: `172.17.255.1`
- Internet kapcsolat teszteléséhez: `1.1.1.1`
- ICANN kapcsolat teszteléséhez a 'távolabbi' cím:
	- Magentus esetén: `172.30.30.30`
	- Yapper esetén: `172.29.29.30`

**Jelmagyarázat:** A tesztábrákon a szimulált hiba helyét vagy a megszakadt kapcsolatot <span style="color:red;font-weight:bold">piros vonal</span>, míg a hibatűrés miatt létrejött alternatív útvonalat <span style="color:orange;font-weight:bold">sárga szaggatott vonal</span> jelöli.

<div style="page-break-after: always;"></div>

### Hiba szimuláció: ICANN-R1 - Magentus ping

<img src="images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 12ms 28ms 20ms</p>
    <img src="./images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 24ms 48ms 16ms</p>
    <img src="./images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 24ms 24ms 16ms</p>
    <img src="./images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 56ms 60ms 36ms</p>
    <img src="./images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: ICANN-R1 - Yapper ping

<img src="images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 40ms 8ms 28ms</p>
    <img src="./images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 16ms 64ms 4ms</p>
    <img src="./images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 16ms 36ms 32ms</p>
    <img src="./images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 36ms 32ms 28ms</p>
    <img src="./images/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5/fbdafd2a-7d1b-467f-83ea-4746f9d2c9b5-YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: ICANN-R2 - Magentus ping

<img src="images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 12ms 24ms 20ms</p>
    <img src="./images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 32ms 32ms 40ms</p>
    <img src="./images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 24ms 16ms 28ms</p>
    <img src="./images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 40ms 52ms 52ms</p>
    <img src="./images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: ICANN-R2 - Yapper ping

<img src="images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 48ms 20ms 100ms</p>
    <img src="./images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 52ms 8ms 40ms</p>
    <img src="./images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 16ms 40ms 36ms</p>
    <img src="./images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 32ms 60ms 88ms</p>
    <img src="./images/404488b7-3784-45f8-a03d-0b0b16504da6/404488b7-3784-45f8-a03d-0b0b16504da6-YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: MAGENTUS-EDGE-R1 - Magentus ping

<img src="images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 48ms 32ms 20ms</p>
    <img src="./images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 68ms 40ms 24ms</p>
    <img src="./images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 20ms 48ms 12ms</p>
    <img src="./images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 40ms 44ms 36ms</p>
    <img src="./images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: MAGENTUS-EDGE-R1 - Yapper ping

<img src="images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 52ms 8ms 64ms</p>
    <img src="./images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 72ms 44ms 56ms</p>
    <img src="./images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 32ms 68ms 16ms</p>
    <img src="./images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 48ms 16ms 44ms</p>
    <img src="./images/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: MAGENTUS-EDGE-R2 - Magentus ping

<img src="images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 32ms 36ms 4ms</p>
    <img src="./images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 24ms 28ms 52ms</p>
    <img src="./images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.2.4 12ms 28ms 36ms</p>
    <img src="./images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 40ms 40ms 40ms</p>
    <img src="./images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: MAGENTUS-EDGE-R2 - Yapper ping

<img src="images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 24ms 24ms 32ms</p>
    <img src="./images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 52ms 20ms 44ms</p>
    <img src="./images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 52ms 24ms 20ms</p>
    <img src="./images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 24ms 40ms 56ms</p>
    <img src="./images/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: YAPPER-EDGE-R1 - Magentus ping

<img src="images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 52ms 12ms 44ms</p>
    <img src="./images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 32ms 36ms 56ms</p>
    <img src="./images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.2.4 36ms 28ms 36ms</p>
    <img src="./images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 36ms 36ms 76ms</p>
    <img src="./images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: YAPPER-EDGE-R1 - Yapper ping

<img src="images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 64ms 52ms 40ms</p>
    <img src="./images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 56ms 40ms 8ms</p>
    <img src="./images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 60ms 44ms 24ms</p>
    <img src="./images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 52ms 16ms 28ms</p>
    <img src="./images/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: YAPPER-EDGE-R2 - Magentus ping

<img src="images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 20ms 20ms 24ms</p>
    <img src="./images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.2.4 56ms 12ms 56ms</p>
    <img src="./images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 8ms 32ms 16ms</p>
    <img src="./images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.2.4 60ms 12ms 56ms</p>
    <img src="./images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

### Hiba szimuláció: YAPPER-EDGE-R2 - Yapper ping

<img src="images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 100%">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 40ms 60ms 20ms</p>
    <img src="./images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 60ms 36ms 44ms</p>
    <img src="./images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 24ms 64ms 28ms</p>
    <img src="./images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 36ms 56ms 44ms</p>
    <img src="./images/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Magentus internet hiba

Magentus közvetlen összekötetése az internet felé megszakítva, internet elérés Yapper-en keresztül

<img src="images/magentus-internet/magentus-internet.svg" style="display: block; margin: 10px auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 60ms 112ms</p>
    <img src="./images/magentus-internet/MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 84ms</p>
    <img src="./images/magentus-internet/MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 40ms</p>
    <img src="./images/magentus-internet/MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 76ms</p>
    <img src="./images/magentus-internet/MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Yapper internet hiba

Yapper közvetlen összekötetése az internet felé megszakítva, internet elérés Magentus-on keresztül

<img src="images/yapper-internet/yapper-internet.svg" style="display: block; margin: 10px auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 60ms</p>
    <img src="./images/yapper-internet/YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 40ms 48ms 68ms</p>
    <img src="./images/yapper-internet/YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 48ms</p>
    <img src="./images/yapper-internet/YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 60ms 56ms 44ms</p>
    <img src="./images/yapper-internet/YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Magentus-Yapper interconnect hiba - Magentus Ping

Yapper és Magentus BGP peer linkjei nem működik, kapcsolat ICANN-en keresztül

<img src="images/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg" style="display: block; margin: 10px auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 40ms 48ms 40ms</p>
    <img src="./images/yapper-magentus-bgpfail/MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.2.4 52ms 68ms 56ms</p>
    <img src="./images/yapper-magentus-bgpfail/MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.2.4 88ms 16ms 48ms</p>
    <img src="./images/yapper-magentus-bgpfail/MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.2.4 68ms 52ms 48ms</p>
    <img src="./images/yapper-magentus-bgpfail/MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Magentus-Yapper interconnect hiba - Yapper Ping

<img src="images/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 400px">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 56ms 44ms 104ms</p>
    <img src="./images/yapper-magentus-bgpfail/YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 60ms 64ms 72ms</p>
    <img src="./images/yapper-magentus-bgpfail/YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 48ms 64ms 60ms</p>
    <img src="./images/yapper-magentus-bgpfail/YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 60ms 60ms 56ms</p>
    <img src="./images/yapper-magentus-bgpfail/YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## ICANN R1 közvetlen kapcsolat hiba

ICANN R1 közvetlen összekötetése Magentus részéről megszakítva, kapcsolat Yapper-en keresztül

<img src="images/icann-r1-fail/icann-r1-fail.svg" style="display: block; margin: 10px auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.29.29.30 68ms 52ms 48ms</p>
    <img src="./images/icann-r1-fail/MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.29.29.30 88ms 52ms 56ms</p>
    <img src="./images/icann-r1-fail/MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.29.29.30 40ms 44ms 44ms</p>
    <img src="./images/icann-r1-fail/MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.29.29.30 56ms 68ms 64ms</p>
    <img src="./images/icann-r1-fail/MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## ICANN R2 közvetlen kapcsolat hiba

ICANN R2 közvetlen összekötetése Yapper részéről megszakítva, kapcsolat Magentus-on keresztül

<img src="images/icann-r2-fail/icann-r2-fail.svg" style="display: block; margin: 10px auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.30.30.30 40ms 36ms 64ms</p>
    <img src="./images/icann-r2-fail/YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.30.30.30 64ms 44ms 44ms</p>
    <img src="./images/icann-r2-fail/YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.30.30.30 60ms 32ms 60ms</p>
    <img src="./images/icann-r2-fail/YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.30.30.30 56ms 48ms 40ms</p>
    <img src="./images/icann-r2-fail/YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

