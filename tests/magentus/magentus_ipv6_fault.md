# Magentus "IPv6" tesztelési jegyzőkönyv

**Dátum:** 2026. 02. 08.

**A dokumentum célja:** A Magentus ISP hálózatban fellépő "single router fault" (egy router hiba) esemény hatásainak bemutatása és tesztelése IPv6-on. A vizsgálat során az Ügyfél (Customer) routerén futtatott `traceroute 2001:4860:4860::8888` paranccsal ellenőrizzük az útvonalválasztást.

**Jelmagyarázat:** Az ábrákon a meghibásodott linket <span style="color:red;font-weight:bold">piros vonal</span>, míg a traceroute által felderített aktív útvonalat <span style="color:orange;font-weight:bold">sárga szaggatott vonal</span> jelöli.

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-CORE-R4

<img src="images/ipv6/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25.svg" style="display: block; margin: 0 auto; width: 450px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms</p>
    <img src="./images/ipv6/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms 52ms 56ms</p>
    <img src="./images/ipv6/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms 56ms 60ms</p>
    <img src="./images/ipv6/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 64ms</p>
    <img src="./images/ipv6/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-CORE-R3

<img src="images/ipv6/610f5e4b-042e-4f75-b0cb-1a4267529a00/610f5e4b-042e-4f75-b0cb-1a4267529a00.svg" style="display: block; margin: 0 auto; width: 450px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 52ms</p>
    <img src="./images/ipv6/610f5e4b-042e-4f75-b0cb-1a4267529a00/610f5e4b-042e-4f75-b0cb-1a4267529a00-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 52ms 60ms 56ms</p>
    <img src="./images/ipv6/610f5e4b-042e-4f75-b0cb-1a4267529a00/610f5e4b-042e-4f75-b0cb-1a4267529a00-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms</p>
    <img src="./images/ipv6/610f5e4b-042e-4f75-b0cb-1a4267529a00/610f5e4b-042e-4f75-b0cb-1a4267529a00-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ❌</h4>
    <p><strong>Sikertelen ping!</strong></p>
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-CORE-R2

<img src="images/ipv6/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff.svg" style="display: block; margin: 0 auto; width: 450px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 84ms</p>
    <img src="./images/ipv6/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 44ms 60ms 60ms</p>
    <img src="./images/ipv6/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 32ms</p>
    <img src="./images/ipv6/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 64ms</p>
    <img src="./images/ipv6/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-CORE-R1

<img src="images/ipv6/d2c3d54b-a190-447b-bd61-c997441ce923/d2c3d54b-a190-447b-bd61-c997441ce923.svg" style="display: block; margin: 0 auto; width: 450px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 64ms</p>
    <img src="./images/ipv6/d2c3d54b-a190-447b-bd61-c997441ce923/d2c3d54b-a190-447b-bd61-c997441ce923-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ❌</h4>
    <p><strong>Sikertelen ping!</strong></p>
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 64ms</p>
    <img src="./images/ipv6/d2c3d54b-a190-447b-bd61-c997441ce923/d2c3d54b-a190-447b-bd61-c997441ce923-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms 56ms</p>
    <img src="./images/ipv6/d2c3d54b-a190-447b-bd61-c997441ce923/d2c3d54b-a190-447b-bd61-c997441ce923-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-EDGE-R3

<img src="images/ipv6/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09.svg" style="display: block; margin: 0 auto; width: 450px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms 56ms 44ms</p>
    <img src="./images/ipv6/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms 52ms 68ms</p>
    <img src="./images/ipv6/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms 60ms 64ms</p>
    <img src="./images/ipv6/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 36ms 56ms</p>
    <img src="./images/ipv6/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-EDGE-R4

<img src="images/ipv6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6.svg" style="display: block; margin: 0 auto; width: 450px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 64ms 108ms</p>
    <img src="./images/ipv6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 40ms</p>
    <img src="./images/ipv6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 52ms 56ms 88ms</p>
    <img src="./images/ipv6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms</p>
    <img src="./images/ipv6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-EDGE-R1

<img src="images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180.svg" style="display: block; margin: 0 auto; width: 450px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 64ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 120ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms 56ms 64ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms 76ms</p>
    <img src="./images/ipv6/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-EDGE-R2

<img src="images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce.svg" style="display: block; margin: 0 auto; width: 450px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 112ms 28ms 52ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms 84ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms 56ms 76ms</p>
    <img src="./images/ipv6/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

