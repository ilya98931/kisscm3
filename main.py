import json
import argparse
import sys
#
def mask(n: int) -> int:
    return 2**n - 1
def load_const(const: int) -> bytes:
    cmd = 6 | ((const & mask(16)) << 4)
    return cmd.to_bytes(length=4, byteorder="little")
def read(adress: int) -> bytes:
    cmd = 12 | ((adress & mask(21)) << 4)
    return cmd.to_bytes(length=4, byteorder="little")
def write(adress: int) -> bytes:
    cmd = 13 | ((adress & mask(21)) << 4)
    return cmd.to_bytes(length=4, byteorder="little")
def bitwise_and(adress: int) -> bytes:
    cmd = 2 | ((adress & mask(21)) << 4)
    return cmd.to_bytes(length=4, byteorder='little')

# (только для 1-ого этапа) 1.5
# assert list(load_const(479)) == [0xF6,0x1D,0x00,0x00]
# assert list(read(662)) == [0x6C ,0x29,0x00,0x00]
# assert list(write(807)) == [0x7D,0x32,0x00,0x00]
# assert list(bitwise_and(564)) == [0x42,0x23,0x00,0x00]

opcode_map = {
    "LOAD_CONST": load_const,
    "READ_MEM": read,
    "WRITE_MEM": write,
    "BITWISE_AND": bitwise_and,
}
#1.1
parser = argparse.ArgumentParser(description='Ассемблер УВМ')
parser.add_argument('input_file', help='Исходный файл json')
parser.add_argument('output_file', help='Выходной бинарный файл')
parser.add_argument('--test', action='store_true', help='Режим тестирования')
args = parser.parse_args()

with open(args.input_file, 'r') as f:
        program_data = json.load(f)
#1.4 внутренее представление 2.1
binary_data = b''
internal_represantation = []
for i, instr in enumerate(program_data.get('program', [])):
    opcode_name = instr.get('opcode')
    operand = instr.get('operand')

    if opcode_name not in opcode_map:
        raise ValueError(f"Неизвестная команда на строке {i}: {opcode_name}")
    func = opcode_map[opcode_name]

    binary = func(operand)
    internal_represantation.append({
        'opcode': opcode_name,
        'operand': operand,
        'bytes': binary
    })
    binary_data += binary
#1.6 тесты
if args.test:
    print("Режим тестирования")
    print("=" * 50)
    for i, instr in enumerate(internal_represantation):
        bytes_hex = [f'0x{b:02x}' for b in instr['bytes']]
        print(f"Команда {i} : {instr['opcode']} \nOperand: {instr['operand']}")
        print(f"Байты: {bytes_hex}")
        print()
#запись в файл
with open(args.output_file, 'wb') as f:
    f.write(binary_data)




