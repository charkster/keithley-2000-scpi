import pyvisa
import time

rm = pyvisa.ResourceManager('@py') # Linux pyvisa-py backend
#rm = pyvisa.ResourceManager()     # Windows NIVISA

class ke2000:
	
	# Constructor
	def __init__(self):
		self.instr = rm.open_resource('ASRL/dev/ttyUSB0::INSTR', baud_rate=9600, read_termination  = '\r', write_termination = '\r', timeout=4000) # Linux USB<->rs232
		#self.instr = rm.open_resource('ASRL6::INSTR', baud_rate=9600, read_termination  = '\r', write_termination = '\r', timeout=4000) # Windows COM6 USB<->rs232
		#self.instr = rm.open_resource('GPIB::15::INSTR') # GPIB

	def read_v(self, samples=1, avg_mode='REP', filt='ON', nplc=1):
		if samples < 100:
			operation_loops = 1
		else:
			operation_loops = int(samples / 100)
			samples = 100
		self.instr.write("\n".join([
		"*CLS",
		":INIT:CONT OFF;:ABORT",
		":TRIG:COUN 1;SOUR TIM",
		":SAMP:COUN {:d}".format(operation_loops),
		":FUNC 'VOLT:DC';:VOLT:DC:NPLC {:f};AVER:TCON {:s};COUN {:d};STAT {:s}".format(nplc,avg_mode, samples, filt),
		":FORMAT:ELEMENTS READ",
		":INIT"]))
		self.instr.query('*OPC?')
		voltage = self.instr.query(':SENSE:DATA?')
		self.instr.write(':SAMP:COUN 1;:INIT:CONT ON')
		return float(voltage)

	def read_i(self, samples=1, avg_mode='MOV', filt='ON', nplc=1):
		if samples < 100:
			operation_loops = 1
		else:
			operation_loops = int(samples/100)
			samples = 100
		self.instr.write("\n".join([
		"*CLS",
		":INIT:CONT OFF;:ABORT",
		":TRIG:COUN 1;SOUR TIM",
		":SAMP:COUN {:d}".format(operation_loops),
		":FUNC 'CURR:DC';:CURR:DC:NPLC {:f};AVER:TCON {:s};COUN {:d};STAT {:s}".format(nplc,avg_mode, samples, filt),
		":FORMAT:ELEMENTS READ",
		":INIT"]))
		self.instr.query('*OPC?')
		current = self.instr.query(':SENSE:DATA?')
		self.instr.write(':SAMP:COUN 1;:INIT:CONT ON')
		return float(current)

	def read_freq(self, samples=1):
		self.instr.write("\n".join([
		"*CLS",
		":INIT:CONT OFF;:ABORT",
		":TRIG:COUN 1;SOUR TIM",
		":SAMP:COUN {:d}".format(samples),
		":FUNC 'FREQ';:FREQ:THR:VOLT:RANG 10",
		":FORMAT:ELEMENTS READ",
		":INIT"]))
		self.instr.query('*OPC?')
		frequency = self.instr.query(':SENSE:DATA?')
		self.instr.write(':TRIG:COUN INF;:INIT')
		return float(frequency)

	def beep_on(self):
		self.instr.write(":SYST:BEEP:STAT 'ON'")

	def display_text(self, text='Message',time_duration=3):
		self.instr.write("DISPLAY:TEXT:DATA '{:s}'".format(text))
		self.instr.write("DISPLAY:TEXT:STATE 1")
		time.sleep(time_duration)
		self.instr.write("DISPLAY:TEXT:STATE 0")

