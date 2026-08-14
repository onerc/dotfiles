hl.curve("linear", { type = "bezier", points = { { 0, 0 }, { 0, 0 } } })
hl.animation({ leaf = "layers", enabled = true, speed = 3, bezier = "linear" })

hl.layer_rule({
	match = { namespace = "calendar" },
	no_anim = true,
})

hl.layer_rule({
	match = { namespace = "app-launcher" },
	no_anim = true,
})

hl.layer_rule({
	match = { namespace = "remove-device" },
	no_anim = true,
})

hl.curve("myBezier", { type = "bezier", points = { { 0.05, 0.9 }, { 0.1, 1.05 } } })

hl.animation({ leaf = "windows", enabled = true, speed = 7, bezier = "myBezier" })
hl.animation({ leaf = "windowsOut", enabled = true, speed = 7, bezier = "default", style = "popin 80%" })
hl.animation({ leaf = "border", enabled = true, speed = 10, bezier = "default" })
hl.animation({ leaf = "borderangle", enabled = true, speed = 8, bezier = "default" })
hl.animation({ leaf = "fade", enabled = true, speed = 7, bezier = "default" })
hl.animation({ leaf = "workspaces", enabled = true, speed = 6, bezier = "default" })
