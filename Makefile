# To prevent make from assuming "root" and "env" are already built because of the same-named directories
.PHONY: root
.PHONY: env

install:
	chmod +x scripts/*.sh
	scripts/install.sh

fmt:
	tf fmt -recursive

root:
	scripts/root.sh

env:
	scripts/env.sh $(filter-out $@, $(MAKECMDGOALS))
