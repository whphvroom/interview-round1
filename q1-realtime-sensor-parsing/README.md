# Q1: Real-time Sensor Parsing

**Difficulty:** Mid

---

## Problem

You are given a list of raw sensor data packets, where each packet is represented as a 32-bit unsigned integer. Each packet encodes the following fields using specific bit ranges:

| Bits  | Width | Field              | Notes                                          |
|-------|-------|--------------------|------------------------------------------------|
| 31–28 | 4     | Sensor type        | 0=LiDAR, 1=Radar, 2=Ultrasonic, others=Unknown |
| 27–16 | 12    | Distance (cm)      | Unsigned                                       |
| 15–8  | 8     | Signal strength    | Unsigned, 0–255                                |
| 7–4   | 4     | Parity nibble      | See below                                      |
| 3–0   | 4     | Sequence number    | 0–15                                           |

### Parity Check

A packet is **malformed** if the parity nibble does not match the expected value.

The expected parity is the XOR of all non-parity nibbles:
- Sensor type nibble (bits 31–28)
- Three nibbles of the distance field (bits 27–16)
- Two nibbles of the signal strength field (bits 15–8)
- Sequence number nibble (bits 3–0)

### Output

For each **valid** (non-malformed) packet, produce a result entry:

```
[sensor_type_string, distance, signal_strength, sequence_number]
```

Malformed packets are skipped. Return results for all valid packets in the order they appear.

---

## Examples

### Example 1

**Input:** `packets = [20971761, 285234434]`  
**Output:** `[]`

```
Packet 1: 0x01400071 = 20971761
  Sensor: 0 (LiDAR), Distance: 320, Signal: 0, Parity stored: 7, Seq: 1
  Expected parity: 0^0^1^4^0^0^1 = 4  →  4 != 7  →  malformed, skipped

Packet 2: 0x10FF5502 = 285234434
  Sensor: 1 (Radar), Distance: 255, Signal: 85, Parity stored: 0, Seq: 2
  Expected parity: 1^0^F^F^5^5^2 = 3  →  3 != 0  →  malformed, skipped
```

Both packets are malformed → result is empty.

### Example 2

**Input:** `packets = [268697600]`  
**Output:** `[]`

```
Packet: 0x10040800 = 268697600
  Sensor: 1 (Radar), Distance: 4, Signal: 8, Parity stored: 0, Seq: 0
  Expected parity: 1^0^0^4^0^8^0 = 0xD  →  0xD != 0  →  malformed, skipped
```

---

## Constraints

- `1 <= packets.length <= 10^5`
- `0 <= packets[i] <= 2^32 - 1`
- Sensor type mapping: `0 → "LiDAR"`, `1 → "Radar"`, `2 → "Ultrasonic"`, others → `"Unknown"`
- Malformed packets (parity mismatch) are excluded from output
