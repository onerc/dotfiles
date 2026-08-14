hl.on("hyprland.start", function()
	hl.exec_cmd(
		"librewolf jellyfin.home.arpa/web/#/music?topParentId=5df466c316ba8de2b02fbbff466365b0 youtube.com mail.google.com/mail/u/0 mail.google.com/mail/u/1 tureng.com sozluk.gov.tr qbittorrent.home.arpa prowlarr.home.arpa",
		{ workspace = "2 silent" }
	)
	hl.exec_cmd(
		"firefox-developer-edition discord.com/app web.whatsapp.com",
		{ workspace = "3 silent" }
	)
	hl.exec_cmd(
		"signal-desktop",
		{ workspace = "3 silent" }
	)
	hl.exec_cmd("rustdesk", { workspace = "4 silent" })
	hl.exec_cmd("bitwarden-desktop", { workspace = "5 silent" })
	hl.exec_cmd("obs --disable-shutdown-check", { workspace = "6 silent" })
	hl.exec_cmd("alacritty -e sh -c 'fabriccc/bin/python .config/fabric/main.py'", { workspace = "10 silent" })
	hl.exec_cmd("hyprctl setcursor macOS 24")
	hl.exec_cmd("wl-clip-persist --clipboard both")
end)
