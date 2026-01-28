# Magentus "Single Router Fault" tesztelési jegyzőkönyv

**Dátum:** 2026. 01. 28.

**A dokumentum célja:** A Magentus ISP hálózatban fellépő "single router fault" (egy router hiba) esemény hatásainak bemutatása és tesztelése. A vizsgálat során az Ügyfél (Customer) routerén futtatott `traceroute 1.1.1.1` paranccsal ellenőrizzük az útvonalválasztást.

**Jelmagyarázat:** Az ábrákon a meghibásodott linket <span style="color:red;font-weight:bold">piros vonal</span>, míg a traceroute által felderített aktív útvonalat <span style="color:orange;font-weight:bold">sárga szaggatott vonal</span> jelöli.
<div style="page-break-after: always;"></div>

## Hiba szimuláció: Szomszédos Internetszolgáltató meghibásodása

<img src="images/fault1_router/internet/internet.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 68 msec</p>
    <img src="./images/fault1_router/internet/internet-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 68 msec 64 msec</p>
    <img src="./images/fault1_router/internet/internet-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 40 msec 56 msec 56 msec</p>
    <img src="./images/fault1_router/internet/internet-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 96 msec 76 msec 92 msec</p>
    <img src="./images/fault1_router/internet/internet-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>


## Hiba szimuláció: MAGENTUS-CORE-R4

<img src="images/fault1_router/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 20 msec 40 msec 24 msec</p>
    <img src="./images/fault1_router/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 40 msec</p>
    <img src="./images/fault1_router/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 24 msec</p>
    <img src="./images/fault1_router/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 24 msec</p>
    <img src="./images/fault1_router/ba37e357-1fed-4a94-b80f-96dbdedb8a25/ba37e357-1fed-4a94-b80f-96dbdedb8a25-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-CORE-R3

<img src="images/fault1_router/610f5e4b-042e-4f75-b0cb-1a4267529a00/610f5e4b-042e-4f75-b0cb-1a4267529a00.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 12 msec</p>
    <img src="./images/fault1_router/610f5e4b-042e-4f75-b0cb-1a4267529a00/610f5e4b-042e-4f75-b0cb-1a4267529a00-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 12 msec</p>
    <img src="./images/fault1_router/610f5e4b-042e-4f75-b0cb-1a4267529a00/610f5e4b-042e-4f75-b0cb-1a4267529a00-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 28 msec 32 msec</p>
    <img src="./images/fault1_router/610f5e4b-042e-4f75-b0cb-1a4267529a00/610f5e4b-042e-4f75-b0cb-1a4267529a00-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ❌</h4>
    <p><strong>Sikertelen ping!</strong></p>
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-CORE-R2

<img src="images/fault1_router/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 12 msec</p>
    <img src="./images/fault1_router/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 40 msec 36 msec 40 msec</p>
    <img src="./images/fault1_router/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 36 msec 32 msec 28 msec</p>
    <img src="./images/fault1_router/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 48 msec</p>
    <img src="./images/fault1_router/cd01053b-56ce-46d6-a15a-3a26ded99eff/cd01053b-56ce-46d6-a15a-3a26ded99eff-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-CORE-R1

<img src="images/fault1_router/d2c3d54b-a190-447b-bd61-c997441ce923/d2c3d54b-a190-447b-bd61-c997441ce923.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 4 msec 28 msec 32 msec</p>
    <img src="./images/fault1_router/d2c3d54b-a190-447b-bd61-c997441ce923/d2c3d54b-a190-447b-bd61-c997441ce923-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ❌</h4>
    <p><strong>Sikertelen ping!</strong></p>
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 16 msec</p>
    <img src="./images/fault1_router/d2c3d54b-a190-447b-bd61-c997441ce923/d2c3d54b-a190-447b-bd61-c997441ce923-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 12 msec</p>
    <img src="./images/fault1_router/d2c3d54b-a190-447b-bd61-c997441ce923/d2c3d54b-a190-447b-bd61-c997441ce923-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-EDGE-R3

<img src="images/fault1_router/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 24 msec 44 msec 12 msec</p>
    <img src="./images/fault1_router/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 32 msec 24 msec 20 msec</p>
    <img src="./images/fault1_router/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 28 msec 16 msec</p>
    <img src="./images/fault1_router/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 28 msec</p>
    <img src="./images/fault1_router/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09/c4b1dcad-0a7a-4462-bd2e-0f2ed56e0f09-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-EDGE-R4

<img src="images/fault1_router/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 16 msec 24 msec</p>
    <img src="./images/fault1_router/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 16 msec 28 msec</p>
    <img src="./images/fault1_router/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 24 msec 64 msec 12 msec</p>
    <img src="./images/fault1_router/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 16 msec 20 msec</p>
    <img src="./images/fault1_router/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6/fc4d42a0-3d17-4b4f-b35e-500fb14f3ef6-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-EDGE-R1

<img src="images/fault1_router/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 28 msec</p>
    <img src="./images/fault1_router/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 20 msec</p>
    <img src="./images/fault1_router/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 28 msec 32 msec</p>
    <img src="./images/fault1_router/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 28 msec 28 msec 24 msec</p>
    <img src="./images/fault1_router/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180/1d6fc7fa-f5cf-48b2-bcc8-cc5418eb2180-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-EDGE-R2

<img src="images/fault1_router/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 12 msec 44 msec 8 msec</p>
    <img src="./images/fault1_router/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 40 msec</p>
    <img src="./images/fault1_router/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 40 msec</p>
    <img src="./images/fault1_router/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 4 msec 28 msec 28 msec</p>
    <img src="./images/fault1_router/dc9bc350-2888-4232-8c7c-591f9c3899ce/dc9bc350-2888-4232-8c7c-591f9c3899ce-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: MAGENTUS-EDGE-IP6Broker

<img src="images/fault1_router/c2deaeff-b7e2-4b13-9286-a097d4ee3112/c2deaeff-b7e2-4b13-9286-a097d4ee3112.svg" style="display: block; margin: 0 auto; width: 500px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 16 msec</p>
    <img src="./images/fault1_router/c2deaeff-b7e2-4b13-9286-a097d4ee3112/c2deaeff-b7e2-4b13-9286-a097d4ee3112-MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 32 msec 28 msec</p>
    <img src="./images/fault1_router/c2deaeff-b7e2-4b13-9286-a097d4ee3112/c2deaeff-b7e2-4b13-9286-a097d4ee3112-MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 68 msec</p>
    <img src="./images/fault1_router/c2deaeff-b7e2-4b13-9286-a097d4ee3112/c2deaeff-b7e2-4b13-9286-a097d4ee3112-MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 1.1.1.1 40 msec</p>
    <img src="./images/fault1_router/c2deaeff-b7e2-4b13-9286-a097d4ee3112/c2deaeff-b7e2-4b13-9286-a097d4ee3112-MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

