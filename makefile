
example: example.c makefile stack-usage.py
	# compile the code
	$(CC) -fstack-usage -fdump-ipa-cgraph -o $@ $<

	# collect stack and call-graph information
	find . -name '*.cgraph' | grep -v stack-usage-log | xargs cat > stack-usage-log.cgraph
	find . -name '*.su'     | grep -v stack-usage-log | xargs cat > stack-usage-log.su

	# analyse the data
	python stack-usage.py

clean:
	# delete intermediate files
	-$(RM) -v *.cgraph *.su example.exe example
