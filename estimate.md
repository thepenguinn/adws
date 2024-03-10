---
title: Power Consumption Estimate
geometry: a4paper, margin=1in
numbersections: true
---

# Components

- Four Solenoid Valves
- One Esp 32
- One DHT 22 sensor
- One 12V pump
- Two 2-channel 12V Relay

# A Duty Cycle

## Assumptions

There will be a total of **20 plants**, and each plant needs **200 mL** a day.

$\therefore$ total of **200 mL x 20 = 4000 mL**, of water is needed each day.

$\therefore$ **40 L** will last for **Approx. 10 days**.

## Duty Cycle

A single Duty Cycle consist of:

- Filling the Tank to **Full**.
- Watering the Plants Daily for **10 Days**.

# Voltage and Current Rating for Components

## Esp 32

- Working Voltage = $3.3$ V

| Mode | Description | Current Draw | Unit |
| :----- | :---------- | ---: | ---: |
| Active Mode I | Basically everything is active including Wifi and Bluetooth. Esp is acting as a WiFi Hotspot | ~ 240 | mA |
| Active Mode II | Basically everything is active including Wifi and Bluetooth. Esp is acting as a WiFi Reciver | ~ 160 | mA |
| Modem Sleep Mode | Wifi and Bluetooth are inactive and everything else is active. | ~ 20 | mA |
| Sleep Mode | Esp Core Processor is inactive, RAM is active and ULP is active. | ~ 1 | mA |

Table: Esp 32 Modes and respective current consumption. {#tbl:espModes}

NOTE: There are **Deep Sleep Mode** and **Hibernation Mode**. We might not be needing them.

## DHT 22 Sensor

- Working Voltage = $3.3 - 6$ V


| Mode | Current Draw | Unit | Remark |
| :--- | :--- | :--- | :------------ |
| Idle | 0.5 | mA | If we dettach the sensor from the circuit using a MFET, we can decrease the current draw to 0mA |
| Active | 1 - 2 | mA | - |

Table: Current Draw of DHT 22 Sensor in different Modes. {#tbl:dhtCurrent}

## Solenoid Valve

- Working Voltage = $12$ V

| Mode | Current Draw | Unit | Remark |
| :--- | :--- | :--- | :------------ |
| Idle | 0 | mA | Solenoid will be dettached from the circuit using the Relay while we are not using it. |
| Active | 320 - 600 | mA | - |

Table: Current Draw of Solenoid Valve in different Modes. {#tbl:solenoidCurrent}

## Hydraulic Pump (R365)

- Working Voltage = $8 - 12$ V
- Maximum Flow = $2 - 3$ L/m
- Maximum Outlet Pressure = $1 - 2.5$ kg

| Mode | Current Draw | Unit | Remark |
| :--- | :--- | :--- | :------------ |
| Idle | 0 | mA | Pump will be dettached from the circuit using the Relay while we are not using it. |
| No Load | 230 | mA | - |
| On Load | 500 - 700 | mA | If we were using a brushless one, this would have been ~320mA, but it costs more, almost 500/-. |

Table: Current Draw of Hydraulic pump in different Modes. {#tbl:pumpCurrent}

## 2 Channel Relay Board

- Trigger Voltage = $12$ V

| Mode | Current Draw | Unit | Remark |
| :--- | :--- | :--- | :------------ |
| Idle | 10 | mA | If we dettach the Relay module from the circuit using a MFET, we can decrease the current draw to 0mA |
| Triggerd | 30 - 50 | mA | - |

Table: Current Draw of 2 Channel Relay Board in different Modes. {#tbl:relayCurrent}

NOTE: This is for a single Relay Board.

# Power Consumption for a Single Duty Cycle

![Power Consumption Block Diagram](./tikzpics/epicpowerconsumptionblock.pdf)

Power Consumption for a single Duty Cycle can be split into two parts:

- Power Consumed during **Pumping the Water into the 40L Tank**.
- Power Consumed during **Doing everything else Daily for the 10 Days**.

## Pumping Water into the 40L Tank

This is need to be done once during a Duty Cycle.

Let minimum pump flow be **1 L/m** and $T$ be the time taken to fill the Tank,

\begin{align*}
\therefore \: T &= \dfrac{40}{1} \times 60 \\
& = 2,400 \: seconds
\end{align*}

For the simplicity of calculations, let's assume the pump needs to be active for
**Approx. 30 Minutes**, for every Duty Cycle, ie for every 10 Days.

## Per Day Power Consumption

Per Day Power Consumption can be furthur divided into these three:

- Power Consumed during **Standby**.
- Power Consumed while **Sensing the Temperature and Humidity**.
- Power Consumed during **Actually watering the plants**.

### Standby

During standby, for one day, the total Time Duration will be:

\begin{align*}
T_{Standby} &= 24 \times 60 \times 60 \\
&= 86,400 \: seconds
\end{align*}

### Sensing

For a day, we will be sensing the temperature and humidity for **10 seconds**,
during every **30 minute** interval.

The total duration of Sensing will be:

\begin{align*}
T_{Sensing} &= 24 \times 2 \times 10 \\
&= 480 \: seconds
\end{align*}

### Watering Plants

Only one of the total 4 Solenoids will be open at a time. We will be watering
each row for a period of **10 seconds** and all the rows will be watered for
**4 times** a day.

The total duration of Watering will be:

\begin{align*}
T_{Watering} &= 4 \times 4 \times 10 \\
&= 160 \: seconds
\end{align*}

## Worst Case Scenario

### Assumptions

In the worst case scenario, we are assuming these things to be true:

- Esp 32 is in **Active Mode I**, while we are doing something, and in **Modem Sleep Mode**, while during Standby.

### Pumping Water

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.24 A | 0.8 W | 2,400 s | 1,920 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 2,400 s | 1,440 W.s |
| | Hydraulic Pump | 12 V | 0.7 A | 8.4 W | 2,400 s | 20,160 W.s |
| Total | | | | | | 23,520 W.s |

Table: Total Consumption during Pumping Water to the Tank. {#tbl:worstPumpingWatt}

NOTE: Power Consumed by the **Sensor** and the other **Relay Board** during their standby mode
is not included in this table.

### Per Day Consumption

#### Standby

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.02 A | 0.07 W | 86,400 s | 5,702.5 W.s |
| | Relay Board I | 12 V | 0.01 A | 0.12 W | 86,400 s | 10,368 W.s |
| | Relay Board II | 12 V | 0.01 A | 0.12 W | 86,400 s | 10,368 W.s |
| | DHT 22 Sensor | 5 V | 0.0005 A | 0.0025 W | 86,400 s | 216 W.s |
| Total | | | | | | 26,654 W.s |

Table: Total Consumption during the Standby Time for a day. {#tbl:worstStandbyWatt}

#### Sensing

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.24 A | 0.8 W | 480 s | 380 W.s |
| | DHT 22 Sensor | 5 V | 0.002 A | 0.01 W | 480 s | 4.8 W.s |
| Total | | | | | | 385 W.s |

Table: Total Consumption during the Sensing Time for a day. {#tbl:worstSensingWatt}

#### Watering

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.24 A | 0.8 W | 160 s | 130 W.s |
| | Solenoid Valve | 12 V | 0.600 A | 7.2 W | 160 s | 1,152 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 160 s | 100 W.s |
| Total | | | | | | 1,382 W.s |

Table: Total Consumption during the Watering Time for a day. {#tbl:worstWateringWatt}

#### Final Per Day Consumption

\begin{align*}
\mbox{Final Worst Case Per Day Consumption} &= \mbox{Standby} + \mbox{Sensing} + \mbox{Watering} \\
&= 26,654 + 385 + 1,382 \\
&= 28,421 \: \mbox{W} \cdot \mbox{s}
\end{align*}

### Final Per Cycle Consumption

\begin{align*}
\mbox{Final Worst Case Per Cycle Consumption} &= \mbox{Pumping} + (10 \times \mbox{Per Day}) \\
&= 23,520 + (10 \times 28,421) \\
&= 23,520 + 284,910 \\
&= 306,430 \: \mbox{W} \cdot \mbox{s}
\end{align*}

### Power Output of a 12 V 1 AH Battery

\begin{align*}
\mbox{Total Watt Hours, battery can output} &= 12 \times 1 \\
&= 12 \: \mbox{W} \cdot \mbox{H} \\ \\
\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \times 60 \times 60 \\
&= 12 \times 60 \times 60 \\
&= 43,200 \: \mbox{W} \cdot \mbox{s}
\end{align*}

Clearly the per cycle demand, $306,430 \: \mbox{W} \cdot \mbox{s}$ is much **larger** than
what this battery can provide, $43,200 \: \mbox{W} \cdot \mbox{s}$.

Let's see how long this battery will be able to hold,

\begin{align*}
\mbox{Pumping water is inevitable in a single Duty Cycle.} \\
\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\
&= 43,200 - 23,520 \\
&= 19,680 \: \mbox{W} \cdot \mbox{s}
\end{align*}

\begin{align*}
\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\
&= \dfrac{19,680}{28,291} \\
&= 0.7 \: \mbox{Days} \: (\approx 16.8 \: \mbox{Hours})
\end{align*}

### Power Output of a 12 V 5 AH Battery

\begin{align*}
\mbox{Total Watt Hours, battery can output} &= 12 \times 5 \\
&= 60 \: \mbox{W} \cdot \mbox{H} \\ \\
\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \times 60 \times 60 \\
&= 60 \times 60 \times 60 \\
&= 216,000 \: \mbox{W} \cdot \mbox{s}
\end{align*}

Clearly the per cycle demand, $306,430 \: \mbox{W} \cdot \mbox{s}$ is much **larger** than
what this battery can provide, $216,000 \: \mbox{W} \cdot \mbox{s}$.

Let's see how long this battery will be able to hold,

\begin{align*}
\mbox{Pumping water is inevitable in a single Duty Cycle.} \\
\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\
&= 216,000 - 23,520 \\
&= 192,480 \: \mbox{W} \cdot \mbox{s}
\end{align*}

\begin{align*}
\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\
&= \dfrac{192,480}{28,291} \\
&= 6.8 \: \mbox{Days} \: (\approx 6 \: \mbox{Days and} \: 19.2 \: \mbox{Hours})
\end{align*}

## Ideal Case Scenario

### Assumptions

In the ideal case scenario, we are assuming these things to be true:

- Esp 32 is in **Active Mode II**, while we are doing something, and in **Sleep Mode**, while during Standby.

### Pumping Water

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.16 A | 0.528 W | 2,400 s | 1,267 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 2,400 s | 1,440 W.s |
| | Hydraulic Pump | 12 V | 0.7 A | 8.4 W | 2,400 s | 20,160 W.s |
| Total | | | | | | 22,867 W.s |

Table: Total Consumption during Pumping Water to the Tank. {#tbl:idealPumpingWatt}

NOTE: Power Consumed by the **Sensor** and the other **Relay Board** during their standby mode
is not included in this table.

### Per Day Consumption

#### Standby

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.001 A | 0.0033 W | 86,400 s | 285 W.s |
| | Relay Board I | 12 V | 0.01 A | 0.12 W | 86,400 s | 10,368 W.s |
| | Relay Board II | 12 V | 0.01 A | 0.12 W | 86,400 s | 10,368 W.s |
| | DHT 22 Sensor | 5 V | 0.0005 A | 0.0025 W | 86,400 s | 216 W.s |
| Total | | | | | | 21,237 W.s |

Table: Total Consumption during the Standby Time for a day. {#tbl:idealStandbyWatt}

#### Sensing

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.16 A | 0.528 W | 480 s | 254 W.s |
| | DHT 22 Sensor | 5 V | 0.002 A | 0.01 W | 480 s | 4.8 W.s |
| Total | | | | | | 258.8 W.s |

Table: Total Consumption during the Sensing Time for a day. {#tbl:idealSensingWatt}

#### Watering

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.16 A | 0.528 W | 160 s | 85 W.s |
| | Solenoid Valve | 12 V | 0.600 A | 7.2 W | 160 s | 1,152 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 160 s | 100 W.s |
| Total | | | | | | 1,337 W.s |

Table: Total Consumption during the Watering Time for a day. {#tbl:idealWateringWatt}

#### Final Per Day Consumption

\begin{align*}
\mbox{Final Worst Case Per Day Consumption} &= \mbox{Standby} + \mbox{Sensing} + \mbox{Watering} \\
&= 26,654 + 385 + 1,252 \\
&= 28,291 \: \mbox{W} \cdot \mbox{s}
\end{align*}

### Final Per Cycle Consumption

\begin{align*}
\mbox{Final Worst Case Per Cycle Consumption} &= \mbox{Pumping} + (10 \times \mbox{Per Day}) \\
&= 23,520 + (10 \times 28,291) \\
&= 23,520 + 282,910 \\
&= 306,430 \: \mbox{W} \cdot \mbox{s}
\end{align*}

### Power Output of a 12 V 1 AH Battery

\begin{align*}
\mbox{Total Watt Hours, battery can output} &= 12 \times 1 \\
&= 12 \: \mbox{W} \cdot \mbox{H} \\ \\
\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \times 60 \times 60 \\
&= 12 \times 60 \times 60 \\
&= 43,200 \: \mbox{W} \cdot \mbox{s}
\end{align*}

Clearly the per cycle demand, $306,430 \: \mbox{W} \cdot \mbox{s}$ is much **larger** than
what this battery can provide, $43,200 \: \mbox{W} \cdot \mbox{s}$.

Let's see how long this battery will be able to hold,

\begin{align*}
\mbox{Pumping water is inevitable in a single Duty Cycle.} \\
\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\
&= 43,200 - 23,520 \\
&= 19,680 \: \mbox{W} \cdot \mbox{s}
\end{align*}

\begin{align*}
\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\
&= \dfrac{19,680}{28,291} \\
&= 0.7 \: \mbox{Days} \: (\approx 16.8 \: \mbox{Hours})
\end{align*}

### Power Output of a 12 V 5 AH Battery

\begin{align*}
\mbox{Total Watt Hours, battery can output} &= 12 \times 5 \\
&= 60 \: \mbox{W} \cdot \mbox{H} \\ \\
\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \times 60 \times 60 \\
&= 60 \times 60 \times 60 \\
&= 216,000 \: \mbox{W} \cdot \mbox{s}
\end{align*}

Clearly the per cycle demand, $306,430 \: \mbox{W} \cdot \mbox{s}$ is much **larger** than
what this battery can provide, $216,000 \: \mbox{W} \cdot \mbox{s}$.

Let's see how long this battery will be able to hold,

\begin{align*}
\mbox{Pumping water is inevitable in a single Duty Cycle.} \\
\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\
&= 216,000 - 23,520 \\
&= 192,480 \: \mbox{W} \cdot \mbox{s}
\end{align*}

\begin{align*}
\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\
&= \dfrac{192,480}{28,291} \\
&= 6.8 \: \mbox{Days} \: (\approx 6 \: \mbox{Days and} \: 19.2 \: \mbox{Hours})
\end{align*}
