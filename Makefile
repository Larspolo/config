install:
	@echo "This will overwrite your existing configuration files in your home directory. Press enter to continue"
	@read -r a
	@echo "Installing..."
	mv -f $(HOME)/.zshrc $(HOME)/.zshrc.bak
	mv -f $(HOME)/.zsh_aliases $(HOME)/.zsh_aliases.bak
	mv -f $(HOME)/.config/polybar $(HOME)/.config/polybar.bak
	mv -f $(HOME)/.config/i3 $(HOME)/.config/i3.bak
	mv -f $(HOME)/.scripts $(HOME)/.scripts.bak
	mv -f $(HOME)/.fonts $(HOME)/.fonts.bak

	ln -sf $(PWD)/.zshrc $(HOME)/.zshrc
	ln -sf $(PWD)/.zsh_aliases $(HOME)/.zsh_aliases
	ln -sf $(PWD)/polybar $(HOME)/.config/
	ln -sf $(PWD)/i3 $(HOME)/.config/
	ln -sf $(PWD)/.scripts $(HOME)/
	ln -sf $(PWD)/.fonts $(HOME)/
	@echo "Done!"

removeBackups:
	@echo "Are you sure you want to remove the backups? Press enter to continue"
	@read -r a
	@echo "Removing backups..."
	rm -rf $(HOME)/.zshrc.bak
	rm -rf $(HOME)/.zsh_aliases.bak
	rm -rf $(HOME)/.config/polybar.bak
	rm -rf $(HOME)/.config/i3.bak
	rm -rf $(HOME)/.scripts.bak
	rm -rf $(HOME)/.fonts.bak
	@echo "Done!"