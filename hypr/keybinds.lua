require("variables")

hl.bind(mod .. " + return", hl.dsp.exec_cmd(terminal))
hl.bind(mod .. " + kp_enter", hl.dsp.exec_cmd(terminal))
hl.bind(mod .. " + SHIFT + q", hl.dsp.window.close())
hl.bind(mod .. " + v", hl.dsp.window.float({ action = "toggle" }))
hl.bind(mod .. " + p", hl.dsp.window.pseudo())
hl.bind(mod .. " + t", hl.dsp.layout("togglesplit"))
hl.bind(
	mod .. " + d",
	hl.dsp.exec_cmd("fabriccc/bin/python -m fabric execute default 'app_launcher.slide(); calendar.hide()'")
)
hl.bind(
	"escape",
	hl.dsp.exec_cmd(
		"fabriccc/bin/python -m fabric execute default 'app_launcher.unslide(); calendar.hide(); remove_device.hide()'"), { non_consuming = true }
)

hl.bind(mod .. " + left", hl.dsp.focus({ direction = "left" }))
hl.bind(mod .. " + right", hl.dsp.focus({ direction = "right" }))
hl.bind(mod .. " + up", hl.dsp.focus({ direction = "up" }))
hl.bind(mod .. " + down", hl.dsp.focus({ direction = "down" }))

hl.bind(mod .. " + h", hl.dsp.focus({ direction = "left" }))
hl.bind(mod .. " + l", hl.dsp.focus({ direction = "right" }))
hl.bind(mod .. " + k", hl.dsp.focus({ direction = "up" }))
hl.bind(mod .. " + j", hl.dsp.focus({ direction = "down" }))

hl.bind(mod .. " + SHIFT + left", hl.dsp.window.move({ direction = "left" }))
hl.bind(mod .. " + SHIFT + right", hl.dsp.window.move({ direction = "right" }))
hl.bind(mod .. " + SHIFT + up", hl.dsp.window.move({ direction = "up" }))
hl.bind(mod .. " + SHIFT + down", hl.dsp.window.move({ direction = "down" }))

hl.bind(mod .. " + SHIFT + h", hl.dsp.window.swap({ direction = "left" }))
hl.bind(mod .. " + SHIFT + l", hl.dsp.window.swap({ direction = "right" }))
hl.bind(mod .. " + SHIFT + k", hl.dsp.window.swap({ direction = "up" }))
hl.bind(mod .. " + SHIFT + j", hl.dsp.window.swap({ direction = "down" }))

hl.bind(mod .. " + 1", hl.dsp.focus({ workspace = 1 }))
hl.bind(mod .. " + 2", hl.dsp.focus({ workspace = 2 }))
hl.bind(mod .. " + 3", hl.dsp.focus({ workspace = 3 }))
hl.bind(mod .. " + 4", hl.dsp.focus({ workspace = 4 }))
hl.bind(mod .. " + 5", hl.dsp.focus({ workspace = 5 }))
hl.bind(mod .. " + 6", hl.dsp.focus({ workspace = 6 }))
hl.bind(mod .. " + 7", hl.dsp.focus({ workspace = 7 }))
hl.bind(mod .. " + 8", hl.dsp.focus({ workspace = 8 }))
hl.bind(mod .. " + 9", hl.dsp.focus({ workspace = 9 }))
hl.bind(mod .. " + 0", hl.dsp.focus({ workspace = 10 }))

hl.bind(mod .. " + SHIFT + 1", hl.dsp.window.move({ workspace = 1, follow = false }))
hl.bind(mod .. " + SHIFT + 2", hl.dsp.window.move({ workspace = 2, follow = false }))
hl.bind(mod .. " + SHIFT + 3", hl.dsp.window.move({ workspace = 3, follow = false }))
hl.bind(mod .. " + SHIFT + 4", hl.dsp.window.move({ workspace = 4, follow = false }))
hl.bind(mod .. " + SHIFT + 5", hl.dsp.window.move({ workspace = 5, follow = false }))
hl.bind(mod .. " + SHIFT + 6", hl.dsp.window.move({ workspace = 6, follow = false }))
hl.bind(mod .. " + SHIFT + 7", hl.dsp.window.move({ workspace = 7, follow = false }))
hl.bind(mod .. " + SHIFT + 8", hl.dsp.window.move({ workspace = 8, follow = false }))
hl.bind(mod .. " + SHIFT + 9", hl.dsp.window.move({ workspace = 9, follow = false }))
hl.bind(mod .. " + SHIFT + 0", hl.dsp.window.move({ workspace = 10, follow = false }))

hl.bind(mod .. " + mouse:272", hl.dsp.window.drag(), { mouse = true })
hl.bind(mod .. " + mouse:273", hl.dsp.window.resize(), { mouse = true })

hl.bind(mod .. " + f", hl.dsp.window.fullscreen({ mode = "maximized" }))
hl.bind(mod .. " + SHIFT + f", hl.dsp.window.fullscreen_state({ action = "toggle", internal = 0, client = 2 }))
hl.bind(
	mod .. " + s",
	hl.dsp.exec_cmd('grim -g "$(slurp -b 00000080 -w 0)" - | swappy -f -')
)
