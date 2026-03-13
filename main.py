# ****************************
# ****************************
# WIFI CONNECTION
import network

ssid = 'BESTstation'
password = '0816592535'

sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
	print('connecting to network...')
	sta_if.active(True)
	sta_if.connect(ssid,password)
	while not sta_if.isconnected():
		pass

print('network config:', sta_if.ifconfig())   

# ****************************
# ****************************
# LINE OFFICAIL IF IP ADDRESS CHANGE OR ONLINE
from lineoa import LineOA_API

bot = LineOA_API(channel_access_token='YOUR_CHANNEL_ACCESS_TOKEN', user_id='USER_ID')
bot.sendMessage(sta_if.ifconfig())


# ****************************
# ****************************
# MODBUS API READ AND WRITE 
from  JGSmod import JGSmodbus_API

mb= JGSmodbus_API(1) #slave_addr

def read_sensor1():
	#temp = mb.read_temphum(1,2,True)[0]/10
	#hum = mb.read_temphum(1,2,True)[1]/10
	rd_speed_cmd = mb.read_sensor(8734,1,False)[0]
	rd_speed_act = mb.read_sensor(8735,1,False)[0]	
	rd_disc_temp =mb.read_sensor(8704,1,True)[0]/10
	rd_high_pres =mb.read_sensor(8705,1,True)[0]/100
	rd_concoil_temp =mb.read_sensor(8706,1,True)[0]/10
	rd_suc_temp = mb.read_sensor(8708,1,True)[0]/10
	rd_suc_pres =mb.read_sensor(8709,1,True)[0]/100
	rd_amb_temp = mb.read_sensor(8711,1,True)[0]/10
	rd_evap_temp = mb.read_sensor(8712,1,True)[0]/10
	rd_disc_sat_temp = mb.read_sensor(8714,1,True)[0]/10
	rd_suc_sat_temp = mb.read_sensor(8715,1,True)[0]/10	
	return rd_speed_cmd,rd_speed_act,rd_disc_temp,rd_high_pres,rd_concoil_temp,rd_suc_temp,rd_suc_pres,rd_amb_temp,rd_evap_temp,rd_disc_sat_temp,rd_suc_sat_temp

def read_sensor2():
	rd_eev= mb.read_sensor(8736,1,False)[0]
	rd_evi= mb.read_sensor(8737,1,False)[0]
	rd_dc=mb.read_sensor(8758,1,False)[0]
	rd_in_v=mb.read_sensor(8759,1,False)[0]
	rd_in_a=mb.read_sensor(8760,1,False)[0]
	rd_in_w=mb.read_sensor(8761,1,False)[0]
	return rd_eev,rd_evi,rd_dc,rd_in_v,rd_in_a,rd_in_w


# ****************************
# ****************************
#  OPTIMIZATION AND MEMORY MANAGEMENT
import gc
gc.collect()


# ****************************
# ****************************
# WEB SERVER AND INTERFACE MODBUS
import socket

chl_state = 0

def web_page():	
  if sensor_readings1[0] > 0 or chl_state == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html = """
<html><head> <title>JGSEE Chiller Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="10">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>JGSEE Chiller Web Server</h1>
   <div id='content'>   
    <p>Speed command: <strong><span>""" + str(sensor_readings1[0]) + """</span></strong> rpm</p>  
    <p>Speed actual: <strong><span>""" + str(sensor_readings1[1]) + """</span></strong> rpm</p>
    <p>Discharge temperature: <strong><span>""" + str(sensor_readings1[2]) + """</span></strong> Degree C</p>
    <p>High pressure : <strong><span>""" + str(sensor_readings1[3]) + """</span></strong> bar</p>
    <p>Suction temperature : <strong><span>""" + str(sensor_readings1[5]) + """</span></strong> Degree C</p>
    <p>Suction pressure : <strong><span>""" + str(sensor_readings1[6]) + """</span></strong> bar</p>
    <p>Ambinet temperature : <strong><span>""" + str(sensor_readings1[7]) + """</span></strong> Degree C</p>
    <p>Evaporator temperature : <strong><span>""" + str(sensor_readings1[8]) + """</span></strong> Degree C</p>
    <p>Discharge saturated temperature : <strong><span>""" + str(sensor_readings1[9]) + """</span></strong> Degree C</p>
    <p>Suction saturated temperature : <strong><span>""" + str(sensor_readings1[10]) + """</span></strong> Degree C</p>
   </div>
    <div id='content'>
    <p>EEV open steps: <strong><span>""" + str(sensor_readings2[0]) + """</span></strong></p>   
    </div>
  <p>Chiller state: <strong>""" + gpio_state + """</strong></p>
<p><a href="/ac/on"><button class="button">ON</button></a><a href="/ac/off"><button class="button button2">OFF</button></a></p></body></html>
"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

while True:
	try:
		if gc.mem_free() < 102000:
			gc.collect()
		conn, addr = s.accept()
		print('Got a connection from %s' % str(addr))
		request = conn.recv(1024)
		request = str(request)
		print('Content = %s' % request)		
		ac_on = request.find('/ac/on')
		ac_off = request.find('/ac/off')
		
		if ac_off == 6:
			try:
				mb.cmd_order(8731,0 ,False)
				chl_state = 0
				print("Chiller is off")
			except:
				print("Error : Can't read a modbus address.")
				
		if ac_on == 6:
			try:
				mb.cmd_order(8731,1 ,False)
				chl_state = 1
				print("Chiller is on")
			except:
				print("Error : Can't read a modbus address.")
				
		sensor_readings1 = read_sensor1()
		sensor_readings2 = read_sensor2()
		response = web_page()
		conn.send('HTTP/1.1 200 OK\n')
		conn.send('Content-Type: text/html\n')
		conn.send('Connection: close\n\n')
		conn.sendall(response)
		conn.close()
	except OSError as e:
		conn.close()
		print('Connection closed')
  





