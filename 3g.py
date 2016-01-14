import time
import os
import subprocess

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
	output, error = run('sudo nmcli con down id "Viettel 3G"')
	print('[!] %s --- %s' % (output, error))

	# kill device driver
	print("[+] kill process %s" % driver)
	output, error = run('sudo fuser %s -k' % driver)
	print('[!] %s --- %s' % (output, error))
	
	time.sleep(1)
	
	# change to 2G
	while True:
		print("[+] change to 2G")
		output, error = run('whoami;sudo echo -e "AT+ZSNT=1,0,0\r" >> %s' % driver)
		print('[!] %s --- %s' % (output, error))
		if not 'busy' in error:
			break
		time.sleep(0.5)
	
	time.sleep(5)
	
	# change to 3G
	while True:
		print("[+] change to 3G")
		output, error = run('sudo echo -e "AT+ZSNT=2,0,0\r" >> %s' % driver)
		print('[!] %s --- %s' % (output, error))
		if not 'busy' in error:
			break
		time.sleep(0.5)

	time.sleep(3)
	
	# connect 3G
	while True:
		print("[+] connect 3G")
		output, error = run('sudo nmcli con up id "Viettel 3G"')
		print('[!] %s --- %s' % (output, error))
		if not 'Error:' in error:
			break
		time.sleep(0.5)