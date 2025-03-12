root:
	scripts/root.sh $(filter-out $@, $(MAKECMDGOALS))

env:
	scripts/env.sh $(filter-out $@, $(MAKECMDGOALS))
