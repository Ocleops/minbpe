def get_counts(
    tokens: list
):
    counts = {}
    for char1, char2 in zip(tokens, tokens[1:]):
        counts[(char1, char2)] = counts.get((char1, char2), 0) + 1
    
    top_pair = max(counts, key=counts.get)

    return counts, top_pair

def merge(
     tokens: list,
     top_pair: tuple,
     value: int   
):
    i = 0
    new_tokens = []
    while i<len(tokens):
        if i<len(tokens)-1 and (tokens[i]==top_pair[0]) and (tokens[i+1]==top_pair[1]):
            new_tokens.append(value)
            i+=2
        else:
            new_tokens.append(tokens[i])
            i+=1 
    
    return new_tokens

def write_vocab_file(path: str, merges: dict[int, tuple[int, int]], vocab: dict[int, bytes]):
    # IMPORTANT: ensure vocab contains merged token bytes
    # Build in id order so dependencies exist
    for new_id in sorted(merges):
        a, b = merges[new_id]
        vocab[new_id] = vocab[a] + vocab[b]

    with open(path, "w", encoding="utf-8") as f:
        for new_id in sorted(merges):
            a, b = merges[new_id]
            left  = vocab[a].decode("utf-8", errors="replace") #render_bytes_token(vocab[a])
            right = vocab[b].decode("utf-8", errors="replace") #render_bytes_token(vocab[b])
            merged = vocab[new_id].decode("utf-8", errors="replace") #render_bytes_token(vocab[new_id])
            f.write(f"[{left}][{right}] -> [{merged}] {new_id}\n")

def render_bytes_token(b: bytes) -> str:
    out = []
    for byte in b:
        ch = chr(byte)
        if ch == "\n":
            out.append("\\n")
        elif ch == "\t":
            out.append("\\t")
        elif ch == "\r":
            out.append("\\r")
        elif 32 <= byte <= 126:  # printable ASCII
            out.append(ch)
        else:
            out.append(f"\\x{byte:02x}")
    return "".join(out)


    