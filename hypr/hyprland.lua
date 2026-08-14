require("keybinds")
require("variables")
require("workspaces_and_monitors")
require("window_rules")
require("autostarts")
hl.config({
	general = {
		gaps_in = 1,
		gaps_out = 2,

		border_size = 1,

		col = {
			active_border = { colors = { "rgba(33ccffee)", "rgba(00ff99ee)" }, angle = 45 },
			inactive_border = "rgba(595959aa)",
		},

		layout = "dwindle",
	},

	decoration = {

		-- Change transparency of focused and unfocused windows
		active_opacity = 1.0,
		inactive_opacity = 1.0,

		shadow = {
			enabled = true,
			range = 4,
			render_power = 3,
			color = 0xee1a1a1a,
		},

		blur = {
			enabled = true,
			size = 3,
			passes = 1,
			vibrancy = 0.1696,
		},
	},

	animations = {
		enabled = true,
	},
	input = {
		kb_layout = "tr",
		follow_mouse = 1,
		numlock_by_default = true,
	},
	dwindle = {
		preserve_split = true,
		force_split = 2,
	},
	misc = {
		disable_splash_rendering = true,
		disable_hyprland_logo = true,
	},
	ecosystem = {
		no_update_news = false,
		no_donation_nag = true
	}
})
