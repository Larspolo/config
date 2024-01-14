configFolders = zsh polybar i3 gtk-3.0 gtk-4.0
homeConfigFolders = .scripts .fonts
homeFiles = .zshrc .Xresources

install:
	@echo "This will overwrite your existing configuration files in your home directory. Press enter to continue"
	@read -r a
	@echo "Installing..."
	@for folder in $(configFolders); do \
		ln -sfn $(PWD)/$$folder $(HOME)/.config/; \
	done
	@for folder in $(homeConfigFolders); do \
		ln -sfn $(PWD)/$$folder $(HOME)/; \
	done
	@for file in $(homeFiles); do \
		ln -sfn $(PWD)/$$file $(HOME)/$$file; \
	done

	# Install rofi theme
	@sudo ln -sfn $(PWD)/others/theme.rasi /usr/share/rofi/themes/theme.rasi

	# Allow ddccontrol to run without sudo for current user (used in brightspace change)
	@sudo ln -sfn $(PWD)/others/30-i2c-tools.rules /etc/udev/rules.d/30-i2c-tools.rules
	@sudo getent group i2cdev || sudo groupadd i2cdev
	@sudo usermod -aG i2cdev $(USER)

	@echo "Done!"
