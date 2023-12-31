configFolders = zsh polybar i3
homeConfigFolders = .scripts .fonts

install:
	@echo "This will overwrite your existing configuration files in your home directory. Press enter to continue"
	@read -r a
	@echo "Installing..."
	for folder in $(configFolders); do \
		mv -f $(HOME)/.config/$$folder $(HOME)/.config/$$folder.bak; \
		ln -sf $(PWD)/$$folder $(HOME)/.config/; \
	done
	for folder in $(homeConfigFolders); do \
		mv -f $(HOME)/$$folder $(HOME)/$$folder.bak; \
		ln -sf $(PWD)/$$folder $(HOME)/; \
	done
	ln -sf $(PWD)/.zshrc $(HOME)/.zshrc
	@echo "Done!"

removeBackups:
	@echo "Are you sure you want to remove the backups? Press enter to continue"
	@read -r a
	@echo "Removing backups..."
	for folder in $(configFolders); do \
		rm -rf $(HOME)/.config/$$folder.bak; \
	done
	for folder in $(homeConfigFolders); do \
		rm -rf $(HOME)/$$folder.bak; \
	done
	rm -rf $(HOME)/.zshrc.bak
	@echo "Done!"