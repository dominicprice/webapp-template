.PHONY: debug
debug:
	scripts/debug.sh

.PHONY: docker
docker:
	$(MAKE) -C api docker
	$(MAKE) -C frontend docker
