import time
from typing import Optional, Tuple

from PIL import ImageGrab
from PIL.Image import Resampling
from serial import Serial


def handshake(seek: bytes, respond: Optional[bytes] = None) -> bytes:
	before = b""
	handshakeBytes = b""
	while True:
		handshakeByte = arduino.read()
		handshakeBytes += handshakeByte
		if len(handshakeBytes) > len(seek):
			handshakeBytes = handshakeBytes[-2:]
		if handshakeBytes == seek:
			if respond is not None:
				arduino.write(respond)
			return before
		before += handshakeByte


def sendUpdates(data: bytes):
	arduino.write(data)

	response = handshake(b"\xff\xff")
	print(data, "->", response)


def getColorData(index: int, color: Tuple[int, int, int]) -> bytes:
	r, g, b = color
	diff = (abs(r - g) + abs(g - b) + abs(r - b)) // 3 / 255
	mean = (r + g + b) // 3 / 255
	z = diff * -(mean - 1)
	r = int(r * z)
	g = int(g * z)
	b = int(b * z)
	return bytes([index, r, g, b])


if __name__ == '__main__':

	arduino = Serial("COM15", 115200, timeout=0.1)

	handshake(b"\xfe\xfa", b"\xff")

	j = 0
	lastColors = None
	maxDiff = 10

	while True:
		screen = ImageGrab.grab()
		screen.thumbnail((60, 60), Resampling.LANCZOS)

		colors = []
		for x in range(screen.width):
			if x == 0:
				for y in reversed(range(screen.height)):
					colors.append(screen.getpixel((x, y)))
			elif x == screen.width - 1:
				for y in range(screen.height):
					colors.append(screen.getpixel((x, y)))
			else:
				colors.append(screen.getpixel((x, 0)))

		colors = list(reversed(colors))

		if lastColors is None:
			lastColors = colors
			data = b""
			i = 0
			for color in colors:
				data += getColorData(i, color)
				i += 1
			sendUpdates(data)
			continue

		updates = []
		for i in range(len(colors)):
			if abs(colors[i][0] - lastColors[i][0]) >= maxDiff and abs(colors[i][1] - lastColors[i][1]) >= maxDiff and abs(colors[i][2] - lastColors[i][2]) >= maxDiff:
				updates.append((i, colors[i]))
				print(i, colors[i])

		if len(updates) > 0:
			data = b""
			for update in updates:
				data += getColorData(update[0], update[1])
			sendUpdates(data)

		time.sleep(0.3)

		lastColors = colors
