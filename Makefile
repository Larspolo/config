configFolders = zsh polybar i3 gtk-3.0 gtk-4.0
homeConfigFolders = .scripts .fonts

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
	@ln -sfn $(PWD)/.zshrc $(HOME)/.zshrc
	@echo "Done!"
