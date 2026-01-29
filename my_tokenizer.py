from my_utils import * 

class BasicTokenizer():
    def __init__(self):
        super().__init__()

    def encode(self, vocab, text):
        return list(text.encode("utf-8")) # returns a list of integers

    def decode(self, tokens, merges):
        while any(t > 255 for t in tokens):
            key = max(tokens)
            for i, t in enumerate(tokens):
                if t == key:
                    tokens[i] = merges[key]
            
            tokens = [x for t in tokens for x in (t if isinstance(t, tuple) else (t,))]
            

        return tokens 


    def train(self, tokens, vocab_size):
        
        num_merges = vocab_size - 256
        # Determine the number of merges by the maximum number of your vocab. Essentially vocab determines how many tokens
        # do you want to have.
        merges = {} 
        for i in range(1, num_merges):
            counts, top_pair = get_counts(tokens=tokens)
            if counts[top_pair] == 1:
                print(f"not enough tokens for vocabulary size: {vocab_size}")
                break

            merges[255+i] = top_pair
            tokens = merge(tokens=tokens, top_pair=top_pair, value=255+i)

        return tokens, merges

       
if __name__ =="__main__":
    vocab = {x: bytes([x]) for x in range(256)}

    with open("/home/miros/karpathy/GPT2/minbpe/tests/taylorswift.txt", "r", encoding="utf-8") as f:
        text = f.read()

    tokenizer = BasicTokenizer()
    tokens = tokenizer.encode(vocab=vocab, text=text)

    tokens, merges = tokenizer.train(tokens=tokens, vocab_size=500)

    # Write a karpathy-style vocab visualization
    write_vocab_file("/home/miros/karpathy/GPT2/minbpe/results.vocab", merges, vocab) # If you use + on bytes it is concatenation.

    # If you want to reconstruct the text, you can decode by expanding ids using vocab directly:
    # (Assuming your `tokens` after training are ids, including >255)
    message = b"".join(vocab[t] for t in tokens).decode("utf-8", errors="replace")
    print(message == text)
