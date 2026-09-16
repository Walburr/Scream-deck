Hey, welcome here!

I have to admit I wanted to do this project a while ago, but I was busy and a bit lazy, so I finally decided to build it.

This isn't perfect, especially on the code side, but it works for the most part.

This project currently only works with end-4 (https://github.com/end-4/dots-hyprland/blob/main/dots), but I'd like it to work with most distros and OSes, including Windows — not macOS, because capitalism doesn't deserve this kind of help, so that would need a lot more work.

I might actually pause this project for now and come back to it later, because I'm currently working on an AI for my phone, something between Bixby and Claude, but for the moment I'm keeping it private.

So I hope you guys like this repo and enjoy!

I'll also explain how I built this.

I used:

- 2 USB-C female ports (optional)
- 2 Wemos D1 Mini boards (with Wi-Fi, but you don't need it)
- 2 potentiometers
- 1 button, ref: Omron B3F 4-pin
- 1 addressable LED, but you can add more (be careful, since too many can cause issues)

## Electronics

### USB

I soldered the female USB-C ports to the 5V and GND of each Wemos, since mine were old, but you can keep the regular USB port — I just prefer USB-C.

### LED

For the LED, I soldered the DIN to the D4 pin of the main board (let's call it "mc").

### Button

For the button I used, the two top pins are the data pins, connected to D1, and the two bottom pins go to the mc's GND.

### Potentiometers

The 1st potentiometer's GND is soldered to the mc, but the VCC is plugged into 3V3 (not the mc's 5V, since it won't work), and the SIG goes to A0.

The 2nd one is plugged into the 2nd Wemos ("baby"), but nothing else changes, except I wanted to wire the mc's GND to it as well.
