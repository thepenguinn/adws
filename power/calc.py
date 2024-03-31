#!/data/data/com.termux/files/usr/bin/python

import math

class WattSecTable:

    def __init__ (self, time, components):

        self.total_watt_sec = 0
        self.last_watt = 0
        self.time = time
        self._components = components

    def _watt(self, volt, amp):
        self.last_watt = volt * amp
        # return math.ceil(self.last_watt)
        return "{0:,g}".format(self.last_watt)

    def _wattsec(self, watt, secs):
        wattsec = watt * secs
        self.total_watt_sec += wattsec
        # return math.ceil(wattsec)
        return "{0:,g}".format(wattsec)

    def _get_total_wattsec(self):
        # return math.ceil(self.total_watt_sec)
        return "{0:,g}".format(self.total_watt_sec)

    def gen_table(self):
        print( "| | Active Components | Working Voltage (V) | Current Draw (A) | Power (W) | Time Duration (s) | Power x Time (W.s) |\n" +
            "|:- | :----- | :---: | :---: | :---: | :---: | :----: |")
        for comp in self._components:
            name, volt, amp = comp
            print("| | " + f"{name}" + " | " + f"{volt:,}" + " V | " + f"{amp:,}" " A | " +
                self._watt(volt, amp) + " W | " + f"{self.time:,}" + " s | " +
                self._wattsec(self.last_watt, self.time) + " W.s |")

        print("| Total | | | | | | " + self._get_total_wattsec() + " W.s |")

pump_worst_comp = []
pump_worst_comp.append(("Esp 32", 3.3, 0.24))
pump_worst_comp.append(("Relay Board", 12, 0.05))
pump_worst_comp.append(("Hydraulic Pump", 12, 0.7))
pump_worst = WattSecTable(2400, pump_worst_comp)

##  pump_worst.gen_table()

standby_worst_comp = []
standby_worst_comp.append(("Esp 32", 3.3, 0.02))
standby_worst_comp.append(("Relay Board I", 12, 0.002))
standby_worst_comp.append(("Relay Board II", 12, 0.002))
standby_worst_comp.append(("DHT 22 Sensor", 5, 0.0005))
standby_worst = WattSecTable(86400, standby_worst_comp)

sensing_worst_comp = []
sensing_worst_comp.append(("Esp 32", 3.3, 0.24))
sensing_worst_comp.append(("DHT 22 Sensor", 5, 0.002))
sensing_worst = WattSecTable(480, sensing_worst_comp)

watering_worst_comp = []
watering_worst_comp.append(("Esp 32", 3.3, 0.24))
watering_worst_comp.append(("Solenoid Valve", 12, 0.600))
watering_worst_comp.append(("Relay Board", 12, 0.05))
watering_worst = WattSecTable(160, watering_worst_comp)

# ideal

pump_ideal_comp = []
pump_ideal_comp.append(("Esp 32", 3.3, 0.16))
pump_ideal_comp.append(("Relay Board", 12, 0.05))
pump_ideal_comp.append(("Hydraulic Pump", 12, 0.7))
pump_ideal = WattSecTable(2400, pump_ideal_comp)

##  pump_ideal.gen_table()

standby_ideal_comp = []
standby_ideal_comp.append(("Esp 32", 3.3, 0.001))
standby_ideal_comp.append(("Relay Board I", 12, 0.002))
standby_ideal_comp.append(("Relay Board II", 12, 0.002))
standby_ideal_comp.append(("DHT 22 Sensor", 5, 0.0005))
standby_ideal = WattSecTable(86400, standby_ideal_comp)

sensing_ideal_comp = []
sensing_ideal_comp.append(("Esp 32", 3.3, 0.16))
sensing_ideal_comp.append(("DHT 22 Sensor", 5, 0.002))
sensing_ideal = WattSecTable(480, sensing_ideal_comp)

watering_ideal_comp = []
watering_ideal_comp.append(("Esp 32", 3.3, 0.16))
watering_ideal_comp.append(("Solenoid Valve", 12, 0.600))
watering_ideal_comp.append(("Relay Board", 12, 0.05))
watering_ideal = WattSecTable(160, watering_ideal_comp)

ONE_AH_WS = 43200
FIVE_AH_WS = 216000

def to_string(num):
    return "{0:,g}".format(num)

## Printing Tables
print(
    "## Worst Case Scenario\n" +
        "\n" +
        "### Assumptions\n" +
        "\n" +
        "In the worst case scenario, we are assuming these things to be true:\n" +
        "\n" +
        "- Esp 32 is in **Active Mode I**, while we are doing something, and in **Modem Sleep Mode**, while Standby.\n" +
        "\n" +
        "### Pumping Water\n" +
        "\n")
pump_worst.gen_table()
print(
    "\n" +
        "Table: Total Consumption during Pumping Water to the Tank. {#tbl:worstPumpingWatt}\n" +
        "\n" +
        "NOTE: Power Consumed by the **Sensor** and the other **Relay Board** during their standby mode\n" +
        "is not included in this table.\n" +
        "\n" +
        "### Per Day Consumption\n" +
        "\n" +
        "#### Standby\n" +
        "\n")
standby_worst.gen_table()
print(
    "\n" +
        "Table: Total Consumption during the Standby Time for a day. {#tbl:worstStandbyWatt}\n" +
        "\n" +
        "#### Sensing\n" +
        "\n")
sensing_worst.gen_table()
print(
    "\n" +
        "Table: Total Consumption during the Sensing Time for a day. {#tbl:worstSensingWatt}\n" +
        "\n" +
        "#### Watering\n" +
        "\n")
watering_worst.gen_table()
print(
    "\n" +
        "Table: Total Consumption during the Watering Time for a day. {#tbl:worstWateringWatt}\n" +
        "\n")


WORST_PER_DAY = standby_worst.total_watt_sec + sensing_worst.total_watt_sec + watering_worst.total_watt_sec
WORST_TOTAL_DAYS = 10 * WORST_PER_DAY
WORST_TOTAL_CYCLE = pump_worst.total_watt_sec + WORST_TOTAL_DAYS
WORST_ONE_EXP_PUMP = ONE_AH_WS - pump_worst.total_watt_sec
WORST_FIVE_EXP_PUMP = FIVE_AH_WS - pump_worst.total_watt_sec

##  Printing conclutions

print(
        "#### Final Worst Case Per Day Consumption\n" +
        "\n"
"\\begin{align*}\n" +
    "\mbox{Final Worst Case Per Day Consumption} &= \mbox{Standby} + \mbox{Sensing} + \mbox{Watering} \\\\\n" +
    "&= " + standby_worst._get_total_wattsec() +
        " + " + sensing_worst._get_total_wattsec() +
        " + " + watering_worst._get_total_wattsec() + " \\\\\n" +
    "&= " + to_string(WORST_PER_DAY) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "\n" +
    "### Final Worst Case Per Cycle Consumption\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Final Worst Case Per Cycle Consumption} &= \mbox{Pumping} + (10 \\times \mbox{Per Day}) \\\\\n" +
    "&= " + to_string(pump_worst.total_watt_sec) + " + (10 \\times " + to_string(WORST_PER_DAY) + ") \\\\\n" +
    "&= " + to_string(pump_worst.total_watt_sec) + " + " + to_string(WORST_TOTAL_DAYS) + " \\\\\n" +
    "&= " + to_string(WORST_TOTAL_CYCLE) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "\n" +
    "### Backup available from a 12 V 1 AH Battery\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Total Watt Hours, battery can output} &= 12 \\times 1 \\\\\n" +
    "&= 12 \: \mbox{W} \cdot \mbox{H} \\\\ \\\\\n" +
    "\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \\times 60 \\times 60 \\\\\n" +
    "&= 12 \\times 60 \\times 60 \\\\\n" +
    "&= " + to_string(ONE_AH_WS) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "<++>\n" +
    "Clearly the per cycle demand, **" + to_string(WORST_TOTAL_CYCLE) + "** $\mbox{W} \cdot \mbox{s}$ is much **larger** than\n" +
    "what this battery can provide, **" + to_string(ONE_AH_WS) + "** $\mbox{W} \cdot \mbox{s}$.\n" +
    "\n" +
    "An approximate amount of backup will be,\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Pumping water is inevitable in a single Duty Cycle.} \\\\\n" +
    "\\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\\\\n" +
    "&= " + to_string(ONE_AH_WS) + " - " + to_string(pump_worst.total_watt_sec) + " \\\\\n" +
    "&= " + to_string(WORST_ONE_EXP_PUMP) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\\\\n" +
    "&= \dfrac{" + to_string(WORST_ONE_EXP_PUMP) + "}{" + to_string(WORST_PER_DAY) + "} \\\\\n" +
    "&= " + to_string(WORST_ONE_EXP_PUMP / WORST_PER_DAY) + " \: \mbox{Days} \: (\\approx <++> \: \mbox{Days and} \: <++> \: \mbox{Hours})\n" +
    "\end{align*}\n" +
    "\n" +
    "### Backup available from a 12 V 5 AH Battery\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Total Watt Hours, battery can output} &= 12 \\times 5 \\\\\n" +
    "&= 60 \: \mbox{W} \cdot \mbox{H} \\\\ \\\\\n" +
    "\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \\times 60 \\times 60 \\\\\n" +
    "&= 60 \\times 60 \\times 60 \\\\\n" +
    "&= " + to_string(FIVE_AH_WS) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "<++>\n" +
    "Clearly the per cycle demand, **" + to_string(WORST_TOTAL_CYCLE) + "** $\mbox{W} \cdot \mbox{s}$ is much **larger** than\n" +
    "what this battery can provide, **" + to_string(FIVE_AH_WS) + "** $\mbox{W} \cdot \mbox{s}$.\n" +
    "\n" +
    "An approximate amount of backup will be,\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Pumping water is inevitable in a single Duty Cycle.} \\\\\n" +
    "\\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\\\\n" +
    "&= " + to_string(FIVE_AH_WS) + " - " + to_string(pump_worst.total_watt_sec) + " \\\\\n" +
    "&= " + to_string(WORST_FIVE_EXP_PUMP) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\\\\n" +
    "&= \dfrac{" + to_string(WORST_FIVE_EXP_PUMP) + "}{" + to_string(WORST_PER_DAY) + "} \\\\\n" +
    "&= " + to_string(WORST_FIVE_EXP_PUMP / WORST_PER_DAY) + " \: \mbox{Days} \: (\\approx <++> \: \mbox{Days and} \: <++> \: \mbox{Hours})\n" +
    "\end{align*}\n")

## Printing Ideal

## Printing Tables

print(
    "## Ideal Case Scenario\n" +
        "\n" +
        "### Assumptions\n" +
        "\n" +
        "In the ideal case scenario, we are assuming these things to be true:\n" +
        "\n" +
        "- Esp 32 is in **Active Mode II**, while we are doing something, and in **Sleep Mode**, while Standby.\n" +
        "\n" +
        "### Pumping Water\n" +
        "\n")
pump_ideal.gen_table()
print(
    "\n" +
        "Table: Total Consumption during Pumping Water to the Tank. {#tbl:idealPumpingWatt}\n" +
        "\n" +
        "NOTE: Power Consumed by the **Sensor** and the other **Relay Board** during their standby mode\n" +
        "is not included in this table.\n" +
        "\n" +
        "### Per Day Consumption\n" +
        "\n" +
        "#### Standby\n" +
        "\n")
standby_ideal.gen_table()
print(
    "\n" +
        "Table: Total Consumption during the Standby Time for a day. {#tbl:idealStandbyWatt}\n" +
        "\n" +
        "#### Sensing\n" +
        "\n")
sensing_ideal.gen_table()
print(
    "\n" +
        "Table: Total Consumption during the Sensing Time for a day. {#tbl:idealSensingWatt}\n" +
        "\n" +
        "#### Watering\n" +
        "\n")
watering_ideal.gen_table()
print(
    "\n" +
        "Table: Total Consumption during the Watering Time for a day. {#tbl:idealWateringWatt}\n" +
        "\n")

IDEAL_PER_DAY = standby_ideal.total_watt_sec + sensing_ideal.total_watt_sec + watering_ideal.total_watt_sec
IDEAL_TOTAL_DAYS = 10 * IDEAL_PER_DAY
IDEAL_TOTAL_CYCLE = pump_ideal.total_watt_sec + IDEAL_TOTAL_DAYS
IDEAL_ONE_EXP_PUMP = ONE_AH_WS - pump_ideal.total_watt_sec
IDEAL_FIVE_EXP_PUMP = FIVE_AH_WS - pump_ideal.total_watt_sec

##  Printing conclutions

print(
        "#### Final Ideal Case Per Day Consumption\n" +
        "\n"
"\\begin{align*}\n" +
    "\mbox{Final Ideal Case Per Day Consumption} &= \mbox{Standby} + \mbox{Sensing} + \mbox{Watering} \\\\\n" +
    "&= " + standby_ideal._get_total_wattsec() +
        " + " + sensing_ideal._get_total_wattsec() +
        " + " + watering_ideal._get_total_wattsec() + " \\\\\n" +
    "&= " + to_string(IDEAL_PER_DAY) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "\n" +
    "### Final Ideal Case Per Cycle Consumption\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Final Ideal Case Per Cycle Consumption} &= \mbox{Pumping} + (10 \\times \mbox{Per Day}) \\\\\n" +
    "&= " + to_string(pump_ideal.total_watt_sec) + " + (10 \\times " + to_string(IDEAL_PER_DAY) + ") \\\\\n" +
    "&= " + to_string(pump_ideal.total_watt_sec) + " + " + to_string(IDEAL_TOTAL_DAYS) + " \\\\\n" +
    "&= " + to_string(IDEAL_TOTAL_CYCLE) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "\n" +
    "### Backup available from a 12 V 1 AH Battery\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Total Watt Hours, battery can output} &= 12 \\times 1 \\\\\n" +
    "&= 12 \: \mbox{W} \cdot \mbox{H} \\\\ \\\\\n" +
    "\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \\times 60 \\times 60 \\\\\n" +
    "&= 12 \\times 60 \\times 60 \\\\\n" +
    "&= " + to_string(ONE_AH_WS) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "<++>\n" +
    "Clearly the per cycle demand, **" + to_string(IDEAL_TOTAL_CYCLE) + "** $\mbox{W} \cdot \mbox{s}$ is much **larger** than\n" +
    "what this battery can provide, **" + to_string(ONE_AH_WS) + "** $\mbox{W} \cdot \mbox{s}$.\n" +
    "\n" +
    "An approximate amount of backup will be,\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Pumping water is inevitable in a single Duty Cycle.} \\\\\n" +
    "\\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\\\\n" +
    "&= " + to_string(ONE_AH_WS) + " - " + to_string(pump_ideal.total_watt_sec) + " \\\\\n" +
    "&= " + to_string(IDEAL_ONE_EXP_PUMP) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\\\\n" +
    "&= \dfrac{" + to_string(IDEAL_ONE_EXP_PUMP) + "}{" + to_string(IDEAL_PER_DAY) + "} \\\\\n" +
    "&= " + to_string(IDEAL_ONE_EXP_PUMP / IDEAL_PER_DAY) + " \: \mbox{Days} \: (\\approx <++> \: \mbox{Days and} \: <++> \: \mbox{Hours})\n" +
    "\end{align*}\n" +
    "\n" +
    "### Backup available from a 12 V 5 AH Battery\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Total Watt Hours, battery can output} &= 12 \\times 5 \\\\\n" +
    "&= 60 \: \mbox{W} \cdot \mbox{H} \\\\ \\\\\n" +
    "\mbox{Total Watt seconds, battery can output} &= \mbox{Total Watt Hours} \\times 60 \\times 60 \\\\\n" +
    "&= 60 \\times 60 \\times 60 \\\\\n" +
    "&= " + to_string(FIVE_AH_WS) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "<++>\n" +
    "Clearly the per cycle demand, **" + to_string(IDEAL_TOTAL_CYCLE) + "** $\mbox{W} \cdot \mbox{s}$ is much **larger** than\n" +
    "what this battery can provide, **" + to_string(FIVE_AH_WS) + "** $\mbox{W} \cdot \mbox{s}$.\n" +
    "\n" +
    "An approximate amount of backup will be,\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Pumping water is inevitable in a single Duty Cycle.} \\\\\n" +
    "\\therefore \mbox{Watt seconds available for the rest of the Cycle} &= \mbox{Total Output} - \mbox{Pumping Water} \\\\\n" +
    "&= " + to_string(FIVE_AH_WS) + " - " + to_string(pump_ideal.total_watt_sec) + " \\\\\n" +
    "&= " + to_string(IDEAL_FIVE_EXP_PUMP) + " \: \mbox{W} \cdot \mbox{s}\n" +
    "\end{align*}\n" +
    "\n" +
    "\\begin{align*}\n" +
    "\mbox{Total days this battery can last} &= \dfrac{\mbox{Rest of the Energy Available}}{\mbox{Per Day Consumption}} \\\\\n" +
    "&= \dfrac{" + to_string(IDEAL_FIVE_EXP_PUMP) + "}{" + to_string(IDEAL_PER_DAY) + "} \\\\\n" +
    "&= " + to_string(IDEAL_FIVE_EXP_PUMP / IDEAL_PER_DAY) + " \: \mbox{Days} \: (\\approx <++> \: \mbox{Days and} \: <++> \: \mbox{Hours})\n" +
    "\end{align*}\n")
