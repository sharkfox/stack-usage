
CFLAGS := -O1 -fno-inline -fstack-usage -fdump-ipa-cgraph

example: example.c makefile stack-usage.py
	# compile the code
	$(CC) $(CFLAGS) -o $@ $<

	# collect stack and call-graph information
	find . -name '*.cgraph' | grep -v stack-usage-log | xargs cat > stack-usage-log.cgraph
	find . -name '*.su'     | grep -v stack-usage-log | xargs cat > stack-usage-log.su

	# analyse the data
	python stack-usage.py --csv stack-usage.csv --json stack-usage.json

clean:
	# delete intermediate files
	-$(RM) -v *.cgraph *.su *.json *.csv example.exe example
