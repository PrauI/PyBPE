
library:
	mkdir -p bin
	go build -o bin/bpe.so -buildmode=c-shared cmd/main.go
