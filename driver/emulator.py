from serial import Serial

arduino = Serial("COM5", 115200)

init = False

color = []
colors = []

while True:
	data = arduino.read()
	if len(data) > 0:
		data = data[0]
		if data == 0xff:
			print("Show")
			print(colors)
			colors = []
			color = []
		else:
			color.append(data)
			if len(color) == 3:
				colors.append(color)
				color = []
	elif not init:
		arduino.write(b"Bob\n")
		arduino.write(b"0\n0\n0\n0\n")
		init = True
