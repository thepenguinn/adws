---
title: Power Consumption Estimate
subtitle: Automated Drip based Watering System
geometry: a4paper, margin=1in
numbersections: true
---

# Power Dissipating Components

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
| Idle | 2 | mA | If we dettach the Relay module from the circuit using a MFET, we can decrease the current draw to 0mA |
| Triggerd | 30 - 50 | mA | - |

Table: Current Draw of 2 Channel Relay Board in different Modes. {#tbl:relayCurrent}

NOTE: This is for a single Relay Board.

# Power Consumption during a Single Duty Cycle

Power Consumption during a single Duty Cycle can be split into two parts:

- Power Consumed during **Pumping the Water into the 40L Tank**.
- Power Consumed during **Doing everything else Daily for the 10 Days**.

![Power Consumption Block Diagram](./tikzpics/epicpowerconsumptionblock.pdf)

## Duration of Pumping Water into the 40L Tank

This is need to be done once during a Duty Cycle.

Let the minimum pump flow be **1 L/m** and $T$ be the time taken to fill the Tank,

\begin{align*}
\therefore \: T &= \dfrac{40}{1} \times 60 \\
& = 2,400 \: seconds
\end{align*}

## Per Day Power Consumption

Per Day Power Consumption can be furthur divided into these three:

- Power Consumed during **Standby**.
- Power Consumed while **Sensing the Temperature and Humidity**.
- Power Consumed during **Actually watering the plants**.

### Duration of Standby

During standby, for one day, the total Time Duration will be:

\begin{align*}
T_{Standby} &= 24 \times 60 \times 60 \\
&= 86,400 \: seconds
\end{align*}

### Duration of Sensing

For a day, we will be sensing the temperature and humidity for **10 seconds**,
during every **30 minute** interval.

The total duration of Sensing will be:

\begin{align*}
T_{Sensing} &= 24 \times 2 \times 10 \\
&= 480 \: seconds
\end{align*}

### Duration of Watering Plants

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

- Esp 32 is in **Active Mode I**, while we are doing something, and in **Modem Sleep Mode**, while Standby.

### Pumping Water

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.24 A | 0.792 W | 2,400 s | 1,900.8 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 2,400 s | 1,440 W.s |
| | Hydraulic Pump | 12 V | 0.7 A | 8.4 W | 2,400 s | 20,160 W.s |
| Total | | | | | | 23,500.8 W.s |

Table: Total Consumption during Pumping Water to the Tank. {#tbl:worstPumpingWatt}

NOTE: Power Consumed by the **Sensor** and the other **Relay Board** during their standby mode
is not included in this table.

### Per Day Consumption

#### Standby

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.02 A | 0.066 W | 86,400 s | 5,702.4 W.s |
| | Relay Board I | 12 V | 0.002 A | 0.024 W | 86,400 s | 2,073.6 W.s |
| | Relay Board II | 12 V | 0.002 A | 0.024 W | 86,400 s | 2,073.6 W.s |
| | DHT 22 Sensor | 5 V | 0.0005 A | 0.0025 W | 86,400 s | 216 W.s |
| Total | | | | | | 10,065.6 W.s |

Table: Total Consumption during the Standby Time for a day. {#tbl:worstStandbyWatt}

#### Sensing

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.24 A | 0.792 W | 480 s | 380.16 W.s |
| | DHT 22 Sensor | 5 V | 0.002 A | 0.01 W | 480 s | 4.8 W.s |
| Total | | | | | | 384.96 W.s |

Table: Total Consumption during the Sensing Time for a day. {#tbl:worstSensingWatt}

#### Watering

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.24 A | 0.792 W | 160 s | 126.72 W.s |
| | Solenoid Valve | 12 V | 0.6 A | 7.2 W | 160 s | 1,152 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 160 s | 96 W.s |
| Total | | | | | | 1,374.72 W.s |

Table: Total Consumption during the Watering Time for a day. {#tbl:worstWateringWatt}

#### Final Worst Case Per Day Consumption

\begin{align*}
\mbox{Final Worst Case Per Day Consumption} &= \mbox{Standby} + \mbox{Sensing} + \mbox{Watering} \\
&= 10,065.6 + 384.96 + 1,374.72 \\
&= 11,825.3 \: \mbox{W} \cdot \mbox{s}
\end{align*}

### Final Worst Case Per Cycle Consumption

\begin{align*}
\mbox{Final Worst Case Per Cycle Consumption} &= \mbox{Pumping} + (10 \times \mbox{Per Day}) \\
&= 23,500.8 + (10 \times 11,825.3) \\
&= 23,500.8 + 118,253 \\
&= 141,754 \: \mbox{W} \cdot \mbox{s}
\end{align*}

### Backup available from a 12 V 1 AH Battery

\begin{align*}
\mbox{Total Watt Hours, battery can output} &= 12 \times 1 \\
&= 12 \: \mbox{W} \cdot \mbox{H} \\ \\
\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \times 60 \times 60 \\
&= 12 \times 60 \times 60 \\
&= 43,200 \: \mbox{W} \cdot \mbox{s}
\end{align*}

Clearly the per cycle demand, **141,754** $\mbox{W} \cdot \mbox{s}$ is much **larger** than
what this battery can provide, **43,200** $\mbox{W} \cdot \mbox{s}$.

An approximate amount of backup will be,

\begin{align*}
\mbox{Pumping water is inevitable in a single Duty Cycle.} \\
\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\
&= 43,200 - 23,500.8 \\
&= 19,699.2 \: \mbox{W} \cdot \mbox{s}
\end{align*}

\begin{align*}
\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\
&= \dfrac{19,699.2}{11,825.3} \\
&= 1.67 \: \mbox{Days} \: (\approx 1 \: \mbox{Days and} \: 16 \: \mbox{Hours})
\end{align*}

### Backup available from a 12 V 5 AH Battery

\begin{align*}
\mbox{Total Watt Hours, battery can output} &= 12 \times 5 \\
&= 60 \: \mbox{W} \cdot \mbox{H} \\ \\
\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \times 60 \times 60 \\
&= 60 \times 60 \times 60 \\
&= 216,000 \: \mbox{W} \cdot \mbox{s}
\end{align*}

As we can see the per cycle demand, **141,754** $\mbox{W} \cdot \mbox{s}$ is **lesser** than
what this battery can provide, **216,000** $\mbox{W} \cdot \mbox{s}$.

An approximate amount of backup will be,

\begin{align*}
\mbox{Pumping water is inevitable in a single Duty Cycle.} \\
\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\
&= 216,000 - 23,500.8 \\
&= 192,499 \: \mbox{W} \cdot \mbox{s}
\end{align*}

\begin{align*}
\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\
&= \dfrac{192,499}{11,825.3} \\
&= 16.28 \: \mbox{Days} \: (\approx 16 \: \mbox{Days and} \: 6 \: \mbox{Hours})
\end{align*}

## Ideal Case Scenario

### Assumptions

In the ideal case scenario, we are assuming these things to be true:

- Esp 32 is in **Active Mode II**, while we are doing something, and in **Sleep Mode**, while Standby.

### Pumping Water

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.16 A | 0.528 W | 2,400 s | 1,267.2 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 2,400 s | 1,440 W.s |
| | Hydraulic Pump | 12 V | 0.7 A | 8.4 W | 2,400 s | 20,160 W.s |
| Total | | | | | | 22,867.2 W.s |

Table: Total Consumption during Pumping Water to the Tank. {#tbl:idealPumpingWatt}

NOTE: Power Consumed by the **Sensor** and the other **Relay Board** during their standby mode
is not included in this table.

### Per Day Consumption

#### Standby

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.001 A | 0.0033 W | 86,400 s | 285.12 W.s |
| | Relay Board I | 12 V | 0.002 A | 0.024 W | 86,400 s | 2,073.6 W.s |
| | Relay Board II | 12 V | 0.002 A | 0.024 W | 86,400 s | 2,073.6 W.s |
| | DHT 22 Sensor | 5 V | 0.0005 A | 0.0025 W | 86,400 s | 216 W.s |
| Total | | | | | | 4,648.32 W.s |

Table: Total Consumption during the Standby Time for a day. {#tbl:idealStandbyWatt}

#### Sensing

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.16 A | 0.528 W | 480 s | 253.44 W.s |
| | DHT 22 Sensor | 5 V | 0.002 A | 0.01 W | 480 s | 4.8 W.s |
| Total | | | | | | 258.24 W.s |

Table: Total Consumption during the Sensing Time for a day. {#tbl:idealSensingWatt}

#### Watering

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.16 A | 0.528 W | 160 s | 84.48 W.s |
| | Solenoid Valve | 12 V | 0.6 A | 7.2 W | 160 s | 1,152 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 160 s | 96 W.s |
| Total | | | | | | 1,332.48 W.s |

Table: Total Consumption during the Watering Time for a day. {#tbl:idealWateringWatt}

#### Final Ideal Case Per Day Consumption

\begin{align*}
\mbox{Final Ideal Case Per Day Consumption} &= \mbox{Standby} + \mbox{Sensing} + \mbox{Watering} \\
&= 4,648.32 + 258.24 + 1,332.48 \\
&= 6,239.04 \: \mbox{W} \cdot \mbox{s}
\end{align*}

### Final Ideal Case Per Cycle Consumption

\begin{align*}
\mbox{Final Ideal Case Per Cycle Consumption} &= \mbox{Pumping} + (10 \times \mbox{Per Day}) \\
&= 22,867.2 + (10 \times 6,239.04) \\
&= 22,867.2 + 62,390.4 \\
&= 85,257.6 \: \mbox{W} \cdot \mbox{s}
\end{align*}

### Backup available from a 12 V 1 AH Battery

\begin{align*}
\mbox{Total Watt Hours, battery can output} &= 12 \times 1 \\
&= 12 \: \mbox{W} \cdot \mbox{H} \\ \\
\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \times 60 \times 60 \\
&= 12 \times 60 \times 60 \\
&= 43,200 \: \mbox{W} \cdot \mbox{s}
\end{align*}

The per cycle demand, **85,257.6** $\mbox{W} \cdot \mbox{s}$ is **double** than that of
the battery can provide, **43,200** $\mbox{W} \cdot \mbox{s}$.

An approximate amount of backup will be,

\begin{align*}
\mbox{Pumping water is inevitable in a single Duty Cycle.} \\
\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\
&= 43,200 - 22,867.2 \\
&= 20,332.8 \: \mbox{W} \cdot \mbox{s}
\end{align*}

\begin{align*}
\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\
&= \dfrac{20,332.8}{6,239.04} \\
&= 3.25 \: \mbox{Days} \: (\approx 3 \: \mbox{Days and} \: 6 \: \mbox{Hours})
\end{align*}

### Backup available from a 12 V 5 AH Battery

\begin{align*}
\mbox{Total Watt Hours, battery can output} &= 12 \times 5 \\
&= 60 \: \mbox{W} \cdot \mbox{H} \\ \\
\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \times 60 \times 60 \\
&= 60 \times 60 \times 60 \\
&= 216,000 \: \mbox{W} \cdot \mbox{s}
\end{align*}

Clearly the per cycle demand, **85,257.6** $\mbox{W} \cdot \mbox{s}$ is much **less** than
what this battery can provide, **216,000** $\mbox{W} \cdot \mbox{s}$.

An approximate amount of backup will be,

\begin{align*}
\mbox{Pumping water is inevitable in a single Duty Cycle.} \\
\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\
&= 216,000 - 22,867.2 \\
&= 193,133 \: \mbox{W} \cdot \mbox{s}
\end{align*}

\begin{align*}
\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\
&= \dfrac{193,133}{6,239.04} \\
&= 30.9 \: \mbox{Days} \: (\approx 30 \: \mbox{Days and} \: 21 \: \mbox{Hours})
\end{align*}
