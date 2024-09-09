import struct
import sys

def getCRC16(frame):
    crc = 0xFFFF
    polynomial = 0xA001

    for byte in frame:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ polynomial
            else:
                crc >>= 1

    return crc

def calculate_crc(addr, cmd):
    # Pack the frame with addr and cmd
    frame = struct.pack(">BB", addr, cmd)
    crc16 = getCRC16(frame)

    # Extract crc_h and crc_l
    crc_h = (crc16 >> 8) & 0xFF
    crc_l = crc16 & 0xFF
    
    return crc_h, crc_l

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <address> <command>")
        sys.exit(1)
    
    try:
        addr = int(sys.argv[1], 16)  # Parse address as hex
        cmd = int(sys.argv[2], 16)   # Parse command as hex
    except ValueError:
        print("Invalid address or command. Please provide them in hex format.")
        sys.exit(1)

    crc_h, crc_l = calculate_crc(addr, cmd)
    
    print(f"Address: 0x{addr:02X}, Command: 0x{cmd:02X}")
    print(f"CRC High Byte (crc_h): 0x{crc_h:02X}")
    print(f"CRC Low Byte (crc_l): 0x{crc_l:02X}")
