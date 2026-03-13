# ****************************************************
# IMPORT
import network
import socket
import time
import gc
import machine

from machine import WDT
from lineoa import LineOA_API
from JGSmod import JGSmodbus_API


# ****************************************************
# WATCHDOG (AUTO REBOOT IF SYSTEM FREEZE)

wdt = WDT(timeout=30000)   # 30 seconds


# ****************************************************
# WIFI SETTING

SSID = 'BESTstation'
PASSWORD = '0816592535'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

wifi_state = False
old_ip = ""


# ****************************************************
# LINE OA

bot = LineOA_API(
    channel_access_token='YOUR_CHANNEL_ACCESS_TOKEN',
    user_id='USER_ID'
)

def line_notify(msg):

    try:
        bot.sendMessage(msg)
    except:
        print("LINE ERROR")


# ****************************************************
# WIFI CONNECT

def connect_wifi():

    global wifi_state
    global old_ip

    if not sta_if.isconnected():

        print("Connecting WIFI...")

        sta_if.connect(SSID, PASSWORD)

        timeout = 20

        while not sta_if.isconnected() and timeout > 0:

            time.sleep(1)
            timeout -= 1

    if sta_if.isconnected():

        ip = sta_if.ifconfig()[0]

        print("Connected IP :", ip)

        if wifi_state == False:

            line_notify("✅ WIFI CONNECTED\nIP : " + ip)

        wifi_state = True
        old_ip = ip

    else:

        print("WiFi connect failed")


# ****************************************************
# NETWORK CHECK

def check_network():

    global wifi_state
    global old_ip

    if not sta_if.isconnected():

        if wifi_state == True:

            line_notify("⚠ WIFI DISCONNECTED")

        wifi_state = False

        connect_wifi()

    else:

        ip = sta_if.ifconfig()[0]

        if ip != old_ip:

            line_notify("📡 IP Address Changed\nNew IP : " + ip)

            old_ip = ip


# ****************************************************
# MEMORY CHECK

def check_memory():

    free_mem = gc.mem_free()

    if free_mem < 40000:

        print("Memory Low Reboot")

        line_notify("⚠ ESP32 Reboot\nReason: Memory Low")

        time.sleep(2)

        machine.reset()


# ****************************************************
# MODBUS

mb = JGSmodbus_API(1)

modbus_fail = 0


def safe_modbus_read(addr,scale,signed):

    global modbus_fail

    try:

        value = mb.read_sensor(addr,1,signed)[0]

        modbus_fail = 0

        return value/scale

    except:

        modbus_fail += 1

        print("Modbus fail:",modbus_fail)

        if modbus_fail > 10:

            line_notify("⚠ ESP32 Reboot\nReason: Modbus Timeout")

            time.sleep(2)

            machine.reset()

        return 0


# ****************************************************
# SENSOR READ

def read_sensor1():

    rd_speed_cmd = safe_modbus_read(8734,1,False)
    rd_speed_act = safe_modbus_read(8735,1,False)

    rd_disc_temp = safe_modbus_read(8704,10,True)
    rd_high_pres = safe_modbus_read(8705,100,True)
    rd_concoil_temp = safe_modbus_read(8706,10,True)

    rd_suc_temp = safe_modbus_read(8708,10,True)
    rd_suc_pres = safe_modbus_read(8709,100,True)

    rd_amb_temp = safe_modbus_read(8711,10,True)
    rd_evap_temp = safe_modbus_read(8712,10,True)

    rd_disc_sat_temp = safe_modbus_read(8714,10,True)
    rd_suc_sat_temp = safe_modbus_read(8715,10,True)

    return (
        rd_speed_cmd,rd_speed_act,rd_disc_temp,rd_high_pres,
        rd_concoil_temp,rd_suc_temp,rd_suc_pres,rd_amb_temp,
        rd_evap_temp,rd_disc_sat_temp,rd_suc_sat_temp
    )


def read_sensor2():

    rd_eev = safe_modbus_read(8736,1,False)
    rd_evi = safe_modbus_read(8737,1,False)

    rd_dc = safe_modbus_read(8758,1,False)
    rd_in_v = safe_modbus_read(8759,1,False)
    rd_in_a = safe_modbus_read(8760,1,False)
    rd_in_w = safe_modbus_read(8761,1,False)

    return rd_eev,rd_evi,rd_dc,rd_in_v,rd_in_a,rd_in_w


# ****************************************************
# WEB PAGE

chl_state = 0

def web_page():

    if sensor_readings1[0] > 0 or chl_state == 1:

        gpio_state = "ON"

    else:

        gpio_state = "OFF"

    html = """

<html>

<head>

<title>JGSEE Chiller Monitor</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<meta http-equiv="refresh" content="10">

</head>

<body>

<h2>JGSEE Chiller Monitor</h2>

<p>Speed command: """ + str(sensor_readings1[0]) + """ rpm</p>

<p>Speed actual: """ + str(sensor_readings1[1]) + """ rpm</p>

<p>Discharge temperature: """ + str(sensor_readings1[2]) + """ C</p>

<p>High pressure: """ + str(sensor_readings1[3]) + """ bar</p>

<p>Suction temperature: """ + str(sensor_readings1[5]) + """ C</p>

<p>Suction pressure: """ + str(sensor_readings1[6]) + """ bar</p>

<p>Ambient temperature: """ + str(sensor_readings1[7]) + """ C</p>

<p>Evaporator temperature: """ + str(sensor_readings1[8]) + """ C</p>

<p>EEV steps: """ + str(sensor_readings2[0]) + """</p>

<h3>Chiller State : """ + gpio_state + """</h3>

<a href="/ac/on"><button>ON</button></a>

<a href="/ac/off"><button>OFF</button></a>

</body>

</html>

"""

    return html


# ****************************************************
# START WIFI

connect_wifi()


# ****************************************************
# WEB SERVER

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

s.bind(('',80))

s.listen(5)

print("Web server running")


# ****************************************************
# MAIN LOOP

while True:

    try:

        wdt.feed()

        check_network()

        check_memory()

        if gc.mem_free() < 90000:

            gc.collect()

        conn, addr = s.accept()

        request = conn.recv(1024)

        request = str(request)

        ac_on = request.find('/ac/on')

        ac_off = request.find('/ac/off')


        if ac_off == 6:

            mb.cmd_order(8731,0,False)

            chl_state = 0

            print("Chiller OFF")

            line_notify("❌ Chiller OFF")


        if ac_on == 6:

            mb.cmd_order(8731,1,False)

            chl_state = 1

            print("Chiller ON")

            line_notify("✅ Chiller ON")


        sensor_readings1 = read_sensor1()

        sensor_readings2 = read_sensor2()


        response = web_page()

        conn.send('HTTP/1.1 200 OK\n')

        conn.send('Content-Type: text/html\n')

        conn.send('Connection: close\n\n')

        conn.sendall(response)

        conn.close()

    except Exception as e:

        print("System error:",e)

        try:

            conn.close()

        except:

            pass

        time.sleep(2)
