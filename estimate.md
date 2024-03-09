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
| Active Mode | Basically everything is active including Wifi and Bluetooth. | ~ 240 | mA |
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
& = 2400 \: seconds
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
&= 86400 \: seconds
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

- Esp 32 is in **Active Mode**, while we are doing something, and in **Modem Sleep Mode**, while during Standby.

### Pumping Water

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Duration (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.24 A | 0.8 W | 2400 s | 1920 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 2400 s | 1440 W.s |
| | Hydraulic Pump | 12 V | 0.7 A | 8.4 W | 2400 s | 20160 W.s |
| Total | | | | | | 23520 W.s |

Table: Total Consumption during Pumping Water to the Tank. {#tbl:worstPumpingWatt}

NOTE: Power Consumed by the **Sensor** and the other **Relay Board** during their standby mode
is not included in this table.

### Per Day Consumption

#### Standby

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Duration (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.02 A | 0.07 W | 86400 s | 5702.5 W.s |
| | Relay Board I | 12 V | 0.01 A | 0.12 W | 86400 s | 10368 W.s |
| | Relay Board II | 12 V | 0.01 A | 0.12 W | 86400 s | 10368 W.s |
| | DHT 22 Sensor | 5 V | 0.0005 A | 0.0025 W | 86400 s | 216 W.s |
| Total | | | | | | 26654 W.s |

Table: Total Consumption during the Standby Time for a day. {#tbl:worstStandbyWatt}

#### Sensing

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Duration (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.24 A | 0.8 W | 480 s | 380 W.s |
| | DHT 22 Sensor | 5 V | 0.002 A | 0.01 W | 480 s | 4.8 W.s |
| Total | | | | | | 385 W.s |

Table: Total Consumption during the Sensing Time for a day. {#tbl:worstSensingWatt}

#### Watering

| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Duration (W.s) |
|:- | :----- | :---: | :---: | :---: | :---: | :----: |
| | Esp 32 | 3.3 V | 0.24 A | 0.8 W | 160 s | 130 W.s |
| | Solenoid Valve | 12 V | 0.600 A | 7.2 W | 160 s | 1152 W.s |
| | Relay Board | 12 V | 0.05 A | 0.6 W | 160 s | 100 W.s |
| Total | | | | | | 1252 W.s |

Table: Total Consumption during the Watering Time for a day. {#tbl:worstWateringWatt}

#### Final Per Day Consumption

| |
