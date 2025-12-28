
ifeq ($(OS), Windows_NT)
	EXT := .dll
	RM := del
else
	EXT := .so
	RM := rm -f
endif

library:
	mkdir -p bin
	go build -o bin/bpe$(EXT) -buildmode=c-shared go-src/main.go

install: library
	pip install -e .

clean:
	$(RM) bin/bpe.so bin/bpe.dll bin/bpe.h
