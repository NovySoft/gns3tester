# Yapper "IPv6" tesztelési jegyzőkönyv

**Dátum:** 2026. 02. 08.

**A dokumentum célja:** A Yapper ISP hálózatban fellépő "single component fault" (egy komponens meghibásodása) esemény hatásainak bemutatása és tesztelése IPv6-on. A többi vizsgálattól eltérően, itt most a végfelhasználói (DEMARC utáni) routeren futtatott `traceroute 2001:4860:4860::8888` paranccsal ellenőrizzük az útvonalválasztást. Ez a változtatás azért szükséges, mert a NATv6 szabályaink csak az ügyfelek ip címével működnek (2001:470:2171:Xff0::/60).

**Jelmagyarázat:** Az ábrákon a meghibásodott linket <span style="color:red;font-weight:bold">piros vonal</span>, míg a traceroute által felderített aktív útvonalat <span style="color:orange;font-weight:bold">sárga szaggatott vonal</span> jelöli.

<div style="page-break-after: always;"></div>

## Hiba szimuláció: Mesh Routers (YAPPER-MESH1, YAPPER-MESH2)

<img src="images/ipv6_mesh/mesh.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 84ms 120ms</p>
    <img src="./images/ipv6_mesh/YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 92ms 92ms</p>
    <img src="./images/ipv6_mesh/YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms 60ms</p>
    <img src="./images/ipv6_mesh/YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 104ms 120ms 100ms</p>
    <img src="./images/ipv6_mesh/YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-R1

<img src="images/ipv6/3b03c953-0c05-480c-8ff7-d6138b4b4fda/3b03c953-0c05-480c-8ff7-d6138b4b4fda.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 112ms</p>
    <img src="./images/ipv6/3b03c953-0c05-480c-8ff7-d6138b4b4fda/3b03c953-0c05-480c-8ff7-d6138b4b4fda-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms 88ms</p>
    <img src="./images/ipv6/3b03c953-0c05-480c-8ff7-d6138b4b4fda/3b03c953-0c05-480c-8ff7-d6138b4b4fda-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms 64ms 76ms</p>
    <img src="./images/ipv6/3b03c953-0c05-480c-8ff7-d6138b4b4fda/3b03c953-0c05-480c-8ff7-d6138b4b4fda-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 96ms</p>
    <img src="./images/ipv6/3b03c953-0c05-480c-8ff7-d6138b4b4fda/3b03c953-0c05-480c-8ff7-d6138b4b4fda-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-R2

<img src="images/ipv6/fd513749-3a21-43be-977f-04596bd65653/fd513749-3a21-43be-977f-04596bd65653.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 124ms</p>
    <img src="./images/ipv6/fd513749-3a21-43be-977f-04596bd65653/fd513749-3a21-43be-977f-04596bd65653-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms</p>
    <img src="./images/ipv6/fd513749-3a21-43be-977f-04596bd65653/fd513749-3a21-43be-977f-04596bd65653-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms</p>
    <img src="./images/ipv6/fd513749-3a21-43be-977f-04596bd65653/fd513749-3a21-43be-977f-04596bd65653-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms</p>
    <img src="./images/ipv6/fd513749-3a21-43be-977f-04596bd65653/fd513749-3a21-43be-977f-04596bd65653-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-R3

<img src="images/ipv6/964969f1-37bb-4638-8ca7-b46164976e31/964969f1-37bb-4638-8ca7-b46164976e31.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 84ms</p>
    <img src="./images/ipv6/964969f1-37bb-4638-8ca7-b46164976e31/964969f1-37bb-4638-8ca7-b46164976e31-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> Tracing the route to 2001:4860:4860::8888</p>
    <img src="./images/ipv6/964969f1-37bb-4638-8ca7-b46164976e31/964969f1-37bb-4638-8ca7-b46164976e31-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms</p>
    <img src="./images/ipv6/964969f1-37bb-4638-8ca7-b46164976e31/964969f1-37bb-4638-8ca7-b46164976e31-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms 76ms</p>
    <img src="./images/ipv6/964969f1-37bb-4638-8ca7-b46164976e31/964969f1-37bb-4638-8ca7-b46164976e31-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-R4

<img src="images/ipv6/c4c7691c-dc07-4509-bffb-ae1454c15ee5/c4c7691c-dc07-4509-bffb-ae1454c15ee5.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 68ms 68ms</p>
    <img src="./images/ipv6/c4c7691c-dc07-4509-bffb-ae1454c15ee5/c4c7691c-dc07-4509-bffb-ae1454c15ee5-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 96ms 100ms 96ms</p>
    <img src="./images/ipv6/c4c7691c-dc07-4509-bffb-ae1454c15ee5/c4c7691c-dc07-4509-bffb-ae1454c15ee5-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms 76ms 92ms</p>
    <img src="./images/ipv6/c4c7691c-dc07-4509-bffb-ae1454c15ee5/c4c7691c-dc07-4509-bffb-ae1454c15ee5-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 116ms</p>
    <img src="./images/ipv6/c4c7691c-dc07-4509-bffb-ae1454c15ee5/c4c7691c-dc07-4509-bffb-ae1454c15ee5-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-R5

<img src="images/ipv6/334511d2-83aa-4de4-b2ba-d2188be29e57/334511d2-83aa-4de4-b2ba-d2188be29e57.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms</p>
    <img src="./images/ipv6/334511d2-83aa-4de4-b2ba-d2188be29e57/334511d2-83aa-4de4-b2ba-d2188be29e57-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 68ms 76ms 76ms</p>
    <img src="./images/ipv6/334511d2-83aa-4de4-b2ba-d2188be29e57/334511d2-83aa-4de4-b2ba-d2188be29e57-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 72ms</p>
    <img src="./images/ipv6/334511d2-83aa-4de4-b2ba-d2188be29e57/334511d2-83aa-4de4-b2ba-d2188be29e57-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms 92ms 76ms</p>
    <img src="./images/ipv6/334511d2-83aa-4de4-b2ba-d2188be29e57/334511d2-83aa-4de4-b2ba-d2188be29e57-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-R6

<img src="images/ipv6/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms</p>
    <img src="./images/ipv6/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 68ms 76ms</p>
    <img src="./images/ipv6/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 100ms</p>
    <img src="./images/ipv6/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 72ms</p>
    <img src="./images/ipv6/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2/faf0c8e1-f69b-43d4-b7aa-6f71dca203e2-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-R7

<img src="images/ipv6/60592e82-9a43-42c2-a0d4-b37bd27abcf2/60592e82-9a43-42c2-a0d4-b37bd27abcf2.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms</p>
    <img src="./images/ipv6/60592e82-9a43-42c2-a0d4-b37bd27abcf2/60592e82-9a43-42c2-a0d4-b37bd27abcf2-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms</p>
    <img src="./images/ipv6/60592e82-9a43-42c2-a0d4-b37bd27abcf2/60592e82-9a43-42c2-a0d4-b37bd27abcf2-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms 72ms 76ms</p>
    <img src="./images/ipv6/60592e82-9a43-42c2-a0d4-b37bd27abcf2/60592e82-9a43-42c2-a0d4-b37bd27abcf2-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms</p>
    <img src="./images/ipv6/60592e82-9a43-42c2-a0d4-b37bd27abcf2/60592e82-9a43-42c2-a0d4-b37bd27abcf2-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-R8

<img src="images/ipv6/f4c401f1-bb9b-4afb-865d-06f04913aa6c/f4c401f1-bb9b-4afb-865d-06f04913aa6c.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 84ms 80ms</p>
    <img src="./images/ipv6/f4c401f1-bb9b-4afb-865d-06f04913aa6c/f4c401f1-bb9b-4afb-865d-06f04913aa6c-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms</p>
    <img src="./images/ipv6/f4c401f1-bb9b-4afb-865d-06f04913aa6c/f4c401f1-bb9b-4afb-865d-06f04913aa6c-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms 72ms 64ms</p>
    <img src="./images/ipv6/f4c401f1-bb9b-4afb-865d-06f04913aa6c/f4c401f1-bb9b-4afb-865d-06f04913aa6c-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms 52ms</p>
    <img src="./images/ipv6/f4c401f1-bb9b-4afb-865d-06f04913aa6c/f4c401f1-bb9b-4afb-865d-06f04913aa6c-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-EDGE-R3

<img src="images/ipv6/8b9773c3-2668-492c-a863-35edfda95203/8b9773c3-2668-492c-a863-35edfda95203.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms</p>
    <img src="./images/ipv6/8b9773c3-2668-492c-a863-35edfda95203/8b9773c3-2668-492c-a863-35edfda95203-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms</p>
    <img src="./images/ipv6/8b9773c3-2668-492c-a863-35edfda95203/8b9773c3-2668-492c-a863-35edfda95203-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms</p>
    <img src="./images/ipv6/8b9773c3-2668-492c-a863-35edfda95203/8b9773c3-2668-492c-a863-35edfda95203-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms 76ms</p>
    <img src="./images/ipv6/8b9773c3-2668-492c-a863-35edfda95203/8b9773c3-2668-492c-a863-35edfda95203-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-EDGE-R4

<img src="images/ipv6/d131c68c-866a-4939-b3ae-2646d97b2be0/d131c68c-866a-4939-b3ae-2646d97b2be0.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms 72ms</p>
    <img src="./images/ipv6/d131c68c-866a-4939-b3ae-2646d97b2be0/d131c68c-866a-4939-b3ae-2646d97b2be0-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms</p>
    <img src="./images/ipv6/d131c68c-866a-4939-b3ae-2646d97b2be0/d131c68c-866a-4939-b3ae-2646d97b2be0-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms 72ms</p>
    <img src="./images/ipv6/d131c68c-866a-4939-b3ae-2646d97b2be0/d131c68c-866a-4939-b3ae-2646d97b2be0-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms 112ms</p>
    <img src="./images/ipv6/d131c68c-866a-4939-b3ae-2646d97b2be0/d131c68c-866a-4939-b3ae-2646d97b2be0-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-MESH1

<img src="images/ipv6/d200ad58-745d-444a-8300-c83f91cc885a/d200ad58-745d-444a-8300-c83f91cc885a.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 112ms 96ms</p>
    <img src="./images/ipv6/d200ad58-745d-444a-8300-c83f91cc885a/d200ad58-745d-444a-8300-c83f91cc885a-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms</p>
    <img src="./images/ipv6/d200ad58-745d-444a-8300-c83f91cc885a/d200ad58-745d-444a-8300-c83f91cc885a-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms</p>
    <img src="./images/ipv6/d200ad58-745d-444a-8300-c83f91cc885a/d200ad58-745d-444a-8300-c83f91cc885a-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms</p>
    <img src="./images/ipv6/d200ad58-745d-444a-8300-c83f91cc885a/d200ad58-745d-444a-8300-c83f91cc885a-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-MESH2

<img src="images/ipv6/54105fa1-a439-44d0-8d5e-ef26ee5103b2/54105fa1-a439-44d0-8d5e-ef26ee5103b2.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 96ms</p>
    <img src="./images/ipv6/54105fa1-a439-44d0-8d5e-ef26ee5103b2/54105fa1-a439-44d0-8d5e-ef26ee5103b2-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms 40ms 60ms</p>
    <img src="./images/ipv6/54105fa1-a439-44d0-8d5e-ef26ee5103b2/54105fa1-a439-44d0-8d5e-ef26ee5103b2-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 56ms</p>
    <img src="./images/ipv6/54105fa1-a439-44d0-8d5e-ef26ee5103b2/54105fa1-a439-44d0-8d5e-ef26ee5103b2-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 72ms</p>
    <img src="./images/ipv6/54105fa1-a439-44d0-8d5e-ef26ee5103b2/54105fa1-a439-44d0-8d5e-ef26ee5103b2-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-EDGE-R1

<img src="images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 96ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 80ms 80ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 60ms</p>
    <img src="./images/ipv6/69d26c3c-6537-4edf-a7c2-01a4ae898594/69d26c3c-6537-4edf-a7c2-01a4ae898594-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Hiba szimuláció: YAPPER-EDGE-R2

<img src="images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms 80ms 60ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-USER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 72ms 64ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-USER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 76ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-USER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-USER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 2001:4860:4860::8888 124ms</p>
    <img src="./images/ipv6/15e34721-e0e2-4186-acab-d99028afe878/15e34721-e0e2-4186-acab-d99028afe878-YAPPER-USER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

