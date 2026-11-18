CC      ?= gcc
CFLAGS  ?= -Wall -Wextra -g -Iengine/include
BUILD   := build

.PHONY: all engine lib test test-py test-c clean

all: engine lib

engine: $(BUILD)/smartsignal_cli

$(BUILD)/smartsignal_cli: engine/src/green_time.c engine/src/cli.c
	@mkdir -p $(BUILD)
	$(CC) $(CFLAGS) $^ -o $@

lib: $(BUILD)/libgreen_time.so

$(BUILD)/libgreen_time.so: engine/src/green_time.c
	@mkdir -p $(BUILD)
	$(CC) $(CFLAGS) -shared -fPIC $< -o $@

$(BUILD)/test_green_time: engine/src/green_time.c engine/tests/test_green_time.c
	@mkdir -p $(BUILD)
	$(CC) $(CFLAGS) $^ -o $@

test: test-py test-c

test-py:
	python3 -m pytest

test-c: $(BUILD)/test_green_time
	./$(BUILD)/test_green_time

clean:
	rm -rf $(BUILD)
