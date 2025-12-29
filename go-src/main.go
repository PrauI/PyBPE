package main

import (
	"fmt"
	"os"
	"bufio"
	"C"
)
type Node struct {
	index uint16
	prev* Node
	next* Node
}

type Tuple struct {
	a uint16
	b uint16
}

//export GenerateTokens
func GenerateTokens(input_file *C.char, output_file *C.char, max_n_tokens_ C.int, delimiter *C.char) C.int{
	path := C.GoString(input_file)
	dat, err := os.ReadFile(path)
	if err != nil {
		return C.int(-1)
	}

	max_n_tokens := uint16(max_n_tokens_)
	tokens := make([]string, max_n_tokens)
	token_index := uint16(0)
	token_appearance := make(map[string]uint16)

	// Initialize tokens
	startnode := Node{
		index: token_appearance[string(dat[0])],
		prev: nil,
		next: nil,
	}

	lastnode := &startnode

	for i, c := range dat {
		if token_index == max_n_tokens {
			break
		}
		_, ok := token_appearance[string(c)]
		if !ok {
			token_appearance[string(c)] = uint16(token_index)
			tokens[token_index] = string(c)
			token_index++
		}
		if i == 0 {
			continue
		}

		n := new(Node)
		n.index = token_appearance[string(c)]
		n.prev = lastnode
		lastnode.next = n
		lastnode = n
	}



	// successive Token analysis

	pairs := make(map[Tuple]uint16)
	for {

		if token_index == max_n_tokens {
			break
		}

		// loop thorugh tokens 
		current := &startnode
		for current != nil && current.next != nil{

			p := Tuple {
				a: current.index,
				b: current.next.index,
			}

			pairs[p]++

			current = current.next
		}

		// find pair with highest pair
		var maxKey Tuple
		var maxValue uint16
		first := true

		for k, v := range pairs {
			if first || v > maxValue {
				maxKey = k
				maxValue = v
				first = false
			}
		}

		// create new token
		tokens[token_index] = tokens[maxKey.a] + tokens[maxKey.b]
		fmt.Printf(" %d / % d New Token %s\n", token_index, max_n_tokens, tokens[token_index])

		// replace all appearances in the linked list by this new token
		current = &startnode
		for true {


			if current.index == maxKey.a && current.next.index == maxKey.b {
				next := current.next
				current.index = token_index
				current.next = next.next
				next.prev = nil
				next.next = nil
				next = nil
			}
			
			if current.next == nil {
				break
			}
			current = current.next
		}
		token_index++

		// set map back to zero
		
		pairs = make(map[Tuple]uint16)
	}


	// write tokens to file
	output, _ := os.Create(C.GoString(output_file))
	defer output.Close()

	output.Sync()
	w := bufio.NewWriter(output)
	for _, token := range(tokens){
		_, _ = w.WriteString(token + C.GoString(delimiter))
	}
	w.Flush()
	return C.int(0)
}

func main(){}
