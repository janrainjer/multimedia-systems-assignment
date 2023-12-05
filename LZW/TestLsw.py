class LZW:
    def __init__(self, bits=12):
        self.bits = bits
        self.max_code = 2**bits
        self.reset()

    def reset(self):
        self.dictionary = {chr(i): i for i in range(256)}
        self.next_code = 256

    def compress(self, data):
        compressed = []
        prefix = ""

        for c in data:
            if isinstance(prefix, int):
                prefix = str(prefix)

            wc = prefix + str(c)

            if wc in self.dictionary:
                prefix = wc
            else:
                if prefix:
                    compressed.append(self.dictionary[prefix])

                if len(self.dictionary) < self.max_code:
                    self.dictionary[wc] = self.next_code
                    self.next_code += 1

                prefix = c

        if prefix:
            compressed.append(self.dictionary[prefix])

        return compressed

    def decompress(self, compressed):
        decompressed = ""
        prefix = ""

        for code in compressed:
            if code in self.dictionary:
                entry = self.dictionary[code]
            else:
                entry = prefix + prefix[0]

            decompressed += entry

            if len(self.dictionary) < self.max_code:
                self.dictionary[self.next_code] = prefix + entry[0]
                self.next_code += 1

            prefix = entry

        return decompressed


def test_lzw_compression_2(extensions):
    for ext in extensions:
        with open(f"res/file{ext}", "rb") as file:
            data = file.read()
        lzw = LZW()
        compressed = lzw.compress(data)
        with open(f"com2/compressed{ext}.lzw", "wb") as compressed_file:
            compressed_file.write(bytes(compressed))

        decompressed = lzw.decompress(compressed)
        with open(f"decom2/file_decompressed{ext}", "wb") as decompressed_file:
            decompressed_file.write(decompressed)
