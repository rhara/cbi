default:
	@echo Please specify target
	@for f in $$(cat Makefile | grep -E '^\w.*:' | cut -d: -f1) ; do echo '-' $$f ; done

clean:
	find data -type f -name '*.pdb.gz'
