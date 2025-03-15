print_h1 = @printf '\n\033[1m${1}\033[0m\n\n'

init:
	$(call print_h1, Enable git hooks...)
	git config core.hooksPath .githooks
	chmod +x .githooks/pre-commit

	$(call print_h1, Install linters...)
	chmod +x ./scripts/**/*.sh
	./scripts/shellcheck/install.sh
