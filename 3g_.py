import serial
import time
import os
import sys
import subprocess

class ATcommands:
	def connect(self, driver):
		self.ser 				= serial.Serial()
		self.ser.port 			= driver
		self.ser.baudrate 		= 9600
		self.ser.bytesize 		= serial.EIGHTBITS 		#number of bits per bytes
		self.ser.parity 		= serial.PARITY_NONE 		#set parity check: no parity
		self.ser.stopbits 		= serial.STOPBITS_ONE 	#number of stop bits
		# self.ser.timeout 		= None 		#block read
		# self.ser.timeout 		= 0 			#non-block read
		self.ser.timeout 		= 8 			#timeout block read
		self.ser.xonxoff 		= False 		#disable software flow control
		self.ser.rtscts 		= False 		#disable hardware (RTS/CTS) flow control
		self.ser.dsrdtr 		= False 		#disable hardware (DSR/DTR) flow control
		self.ser.writeTimeout 	= 2 		#timeout for write

		if self.ser.isOpen():
			print("[+] connected to: " + self.ser.portstr)
			self.ser.flushInput()
			self.ser.flushOutput()
		else:
			self.ser.open()	
		# time.sleep(1)

	def get2G(self):
		# self.write("ATZ\r") ## ATZ : Restore profile ##
		return self.write("AT+ZSNT=1,0,0")

	def get3G(self):
		# self.write("ATZ\r") ## ATZ : Restore profile ##
		return self.write("AT+ZSNT=2,0,0")
	
	def write(self, msg):
		print("<< "+ msg)
		self.ser.write(msg+"\r")
		self.ser.flush()
		# time.sleep(1)
		return self.read()
	
	def startNetwork(self):
		os.system('sudo nmcli con up id "%s"' % self.network)

	def read(self):
		try:
			data = ""
			while True:
				line = self.ser.readline()
				data += line
				print(">> " + line)
				timeout = time.time() + 0.1
				while not self.ser.inWaiting() and timeout > time.time():
					pass
				if not self.ser.inWaiting():
					break
			return data
		except Exception as e:
			print(e)

	def disconnect(self):
		self.ser.close()
def run(cmd):
	# if type(cmd) == str:
	# 	cmd = cmd.split(' ')
	sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return sp.communicate()

if __name__ == '__main__':
	driver 	= '/dev/ttyUSB2'
	os.setuid(os.geteuid())
	os.system("whoami")
	# stop 3G
	print("[+] disconnect network")
	os.system('sudo nmcli con down id "Viettel 3G"')
	time.sleep(1)


	# kill device driver
	print("[+] kill process %s" % driver)
	output, error = run('sudo fuser %s -k' % driver)
	print('[!] %s --- %s' % (output, error))
	
	time.sleep(1)


	# change to 2G
	print("[+] change to 2G")
	at = ATcommands()
	at.connect(driver)
	while True:
		result = at.get2G()
		if result and not 'ERROR' in result:
			break
		time.sleep(0.5)
	at.disconnect()
	
	time.sleep(3)

	print("[+] connect 2G")
	run('sudo nmcli con up id "Viettel 3G"&')

	time.sleep(1)
	# kill device driver
	print("[+] kill process %s" % driver)
	output, error = run('sudo fuser %s -k' % driver)
	print('[!] %s --- %s' % (output, error))

	time.sleep(1)
	# # connect 2G
	# print("[+] connect 2G")
	# os.system('sudo nmcli con up id "Viettel 2G"')
	
	# # ping
	# print("[+] ping")
	# os.system('ping -c 1 google.com')
	# #####
	# print("[+] disconnect 2G")
	# os.system('sudo nmcli con down id "Viettel 2G"')
	# time.sleep(1)

	# change to 3G
	print("[+] change to 3G")
	at = ATcommands()
	at.connect(driver)
	while True:
		result = at.get3G()
		if result and not 'ERROR' in result:
			break
		time.sleep(0.5)
	at.disconnect()

	time.sleep(3)
	
	# connect 3G
	while True:
		print("[+] connect 3G")
		output, error = run('sudo nmcli con up id "Viettel 3G"')
		print('[!] %s --- %s' % (output, error))
		if not 'Error:' in error:
			break
		time.sleep(0.5)