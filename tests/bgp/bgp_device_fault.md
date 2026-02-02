# BGP tesztelési jegyzőkönyv

## BGP router hiba

<div style="page-break-after: always;"></div>

## Magentus-Yapper interconnect hiba - Magentus Ping

Yapper és Magentus BGP peer linkjei nem működik, kapcsolat ICANN-en keresztül

<img src="images/yapper-magentus-bgpfail/yapper-internet.svg" style="display: block; margin: 0 auto; width: 400px;">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 20ms 68ms 56ms</p>
    <img src="./images/yapper-magentus-bgpfail/MAGENTUS-Customer1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.2.4 48ms 48ms 48ms</p>
    <img src="./images/yapper-magentus-bgpfail/MAGENTUS-Customer2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.2.4 44ms 40ms 32ms</p>
    <img src="./images/yapper-magentus-bgpfail/MAGENTUS-Customer3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>MAGENTUS-Customer4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.17.1.4 68ms 40ms 48ms</p>
    <img src="./images/yapper-magentus-bgpfail/MAGENTUS-Customer4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

## Magentus-Yapper interconnect hiba - Yapper Ping

<img src="images/yapper-magentus-bgpfail/yapper-magentus-bgpfail.svg" style="display: block; margin-left: auto; margin-right: auto; margin-top: 10px; margin-bottom: 10px; width: 400px">

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER1 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 52ms 68ms 80ms</p>
    <img src="./images/yapper-magentus-bgpfail/YAPPER-CUSTOMER1.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER2 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 56ms 48ms 68ms</p>
    <img src="./images/yapper-magentus-bgpfail/YAPPER-CUSTOMER2.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER3 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 44ms 60ms 52ms</p>
    <img src="./images/yapper-magentus-bgpfail/YAPPER-CUSTOMER3.svg" width="100%">
  </div>
  <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px;">
    <h4>YAPPER-CUSTOMER4 ✅</h4>
    <p><strong>Sikeres ping!</strong> 172.16.0.61 56ms 40ms 72ms</p>
    <img src="./images/yapper-magentus-bgpfail/YAPPER-CUSTOMER4.svg" width="100%">
  </div>
</div>

<div style="page-break-after: always;"></div>

