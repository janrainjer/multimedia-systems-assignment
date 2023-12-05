import os
from Timer import Timer


def lzw_compress(data):
    dictionary = {bytes([i]): i for i in range(256)}
    code_width = 9  # Initial code width
    max_code = 2 ** code_width
    result = []
    current_code = 256
    buffer = b''

    for byte in data:
        next_buffer = buffer + bytes([byte])
        if next_buffer in dictionary:
            buffer = next_buffer
        else:
            result.append(dictionary[buffer])
            if current_code < max_code:
                dictionary[next_buffer] = current_code
                current_code += 1
            if current_code >= max_code and code_width < 12:
                code_width += 1
                max_code = 2 ** code_width
            buffer = bytes([byte])

    result.append(dictionary[buffer])

    return result


def lzw_decompress(compressed_data):
    dictionary = {i: bytes([i]) for i in range(256)}
    code_width = 9  # Initial code width
    max_code = 2 ** code_width
    current_code = 256
    result = [compressed_data[0]]
    buffer = dictionary[compressed_data[0]]

    for code in compressed_data[1:]:
        if code in dictionary:
            entry = dictionary[code]
        else:
            entry = buffer + buffer[0:1]
        result.extend(entry)
        if current_code < max_code:
            dictionary[current_code] = buffer + entry[:1]
            current_code += 1
        if current_code >= max_code and code_width < 12:
            code_width += 1
            max_code = 2 ** code_width
        buffer = entry

    return bytes(result)


def calculate_compression_ratio(original_size, compressed_size):
    return compressed_size / original_size


def calculate_compression_speed(original_size, compression_time):
    return original_size / compression_time


def calculate_decompression_speed(decompressed_size, decompression_time):
    return decompressed_size / decompression_time


def test_lzw_compression_1(extensions):
    timer = Timer()
    for extension in extensions:
        input_filename = f'res/file{extension}'
        with open(input_filename, 'rb') as file:
            data = file.read()

        print('**************************************************')
        timer.start()
        compressed = lzw_compress(data)
        compressed_filename = f'compressed/file_compressed{extension}.lzw'
        with open(compressed_filename, 'wb') as compressed_file:
            for code in compressed:
                compressed_file.write(code.to_bytes(2, byteorder='big'))
        print(f'Compressed \t{extension} \t in {timer.stop():.5f} seconds')

        # Calculate compression ratio
        original_size = os.path.getsize(input_filename)
        compressed_size = os.path.getsize(compressed_filename)
        compression_ratio = calculate_compression_ratio(
            original_size, compressed_size)

        compression_speed = calculate_compression_speed(
            original_size, timer.elapsed_time)

        timer.start()
        decompressed = lzw_decompress(compressed)
        decompressed_filename = f'decompressed/file_decompressed{extension}'
        with open(decompressed_filename, 'wb') as decompressed_file:
            decompressed_file.write(decompressed)
        print(f'Decompressed \t{extension} \t in {timer.stop():.5f} seconds')

        decompressed_size = os.path.getsize(decompressed_filename)
        decompression_speed = calculate_decompression_speed(
            decompressed_size, timer.elapsed_time)
        print('--------------------------------------------------')
        print(f'File: {input_filename}')
        print(f'Original Size: \t\t{original_size:,} \t bytes')
        print(f'Compressed Size: \t{compressed_size:,} \t bytes')

        print(f'Compression Ratio: \t{compression_ratio:.4f}')
        print(f'Compression Speed: \t{compression_speed:,.4f} \t bytes/second')
        print(
            f'Decompression Speed: \t{decompression_speed:,.4f} \t bytes/second')
        print('--------------------------------------------------\n')


extensions = ['.doc', '.docx', '.pdf', '.png',
              '.jpg', '.gif', '.bmp', '.mp3', '.wav']
test_lzw_compression_1(extensions)
