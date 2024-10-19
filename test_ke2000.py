import ke2000

dmm1 = ke2000.ke2000()
print("DC Voltage is {:.7e}".format(dmm1.read_v()))
print("DC Current is {:.7e}".format(dmm1.read_i()))
print("Frequency is {:.4f}".format(dmm1.read_freq()))
dmm1.beep_on()
dmm1.display_text(text='HELLO')

