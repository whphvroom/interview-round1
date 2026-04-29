"""
Test suite for Q1: Real-time Sensor Parsing

Run with:  pytest test_solution.py -v
"""
import random
import pytest
from typing import List
from solution_template import Solution


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_packet(sensor_type: int, distance: int, signal: int, seq: int) -> int:
    """Construct a well-formed packet with the correct parity nibble."""
    n_sensor  = sensor_type & 0xF
    n_dist_hi = (distance >> 8) & 0xF
    n_dist_md = (distance >> 4) & 0xF
    n_dist_lo =  distance       & 0xF
    n_sig_hi  = (signal >> 4)   & 0xF
    n_sig_lo  =  signal         & 0xF
    n_seq     = seq             & 0xF
    parity    = n_sensor ^ n_dist_hi ^ n_dist_md ^ n_dist_lo ^ n_sig_hi ^ n_sig_lo ^ n_seq
    return (sensor_type << 28) | (distance << 16) | (signal << 8) | (parity << 4) | seq


def corrupt_parity(packet: int) -> int:
    """Flip one bit in the parity nibble — guaranteed to break the parity check."""
    bad_parity = ((packet >> 4) & 0xF) ^ 0x1
    return (packet & 0xFFFFFF0F) | (bad_parity << 4)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestParseSensorPackets:

    def setup_method(self):
        self.sol = Solution()

    # --- Problem statement examples ------------------------------------------

    def test_example1_both_malformed(self):
        assert self.sol.parseSensorPackets([20971761, 285234434]) == []

    def test_example2_single_malformed(self):
        assert self.sol.parseSensorPackets([268697600]) == []

    # --- Single valid packet per sensor type ---------------------------------

    def test_single_lidar(self):
        p = build_packet(0, 320, 100, 1)
        assert self.sol.parseSensorPackets([p]) == [["LiDAR", 320, 100, 1]]

    def test_single_radar(self):
        p = build_packet(1, 500, 200, 7)
        assert self.sol.parseSensorPackets([p]) == [["Radar", 500, 200, 7]]

    def test_single_ultrasonic(self):
        p = build_packet(2, 1000, 150, 3)
        assert self.sol.parseSensorPackets([p]) == [["Ultrasonic", 1000, 150, 3]]

    def test_unknown_sensor_type_3(self):
        p = build_packet(3, 100, 50, 0)
        assert self.sol.parseSensorPackets([p]) == [["Unknown", 100, 50, 0]]

    def test_unknown_sensor_type_15(self):
        p = build_packet(15, 200, 255, 15)
        assert self.sol.parseSensorPackets([p]) == [["Unknown", 200, 255, 15]]

    # --- Sensor type boundary ------------------------------------------------

    def test_sensor_type_0_is_lidar(self):
        p = build_packet(0, 1, 1, 1)
        assert self.sol.parseSensorPackets([p])[0][0] == "LiDAR"

    def test_sensor_type_1_is_radar(self):
        p = build_packet(1, 1, 1, 1)
        assert self.sol.parseSensorPackets([p])[0][0] == "Radar"

    def test_sensor_type_2_is_ultrasonic(self):
        p = build_packet(2, 1, 1, 1)
        assert self.sol.parseSensorPackets([p])[0][0] == "Ultrasonic"

    def test_sensor_type_4_and_above_is_unknown(self):
        for t in [4, 5, 8, 14, 15]:
            p = build_packet(t, 1, 1, 1)
            assert self.sol.parseSensorPackets([p])[0][0] == "Unknown", f"type {t} should be Unknown"

    # --- Edge / boundary values ----------------------------------------------

    def test_all_zero_fields_is_valid(self):
        # All nibbles zero → parity = 0 → stored parity = 0 → valid
        p = build_packet(0, 0, 0, 0)
        assert self.sol.parseSensorPackets([p]) == [["LiDAR", 0, 0, 0]]

    def test_max_distance(self):
        # 12-bit max = 0xFFF = 4095
        p = build_packet(0, 4095, 0, 0)
        assert self.sol.parseSensorPackets([p]) == [["LiDAR", 4095, 0, 0]]

    def test_max_signal_strength(self):
        p = build_packet(1, 0, 255, 0)
        assert self.sol.parseSensorPackets([p]) == [["Radar", 0, 255, 0]]

    def test_max_sequence_number(self):
        p = build_packet(2, 0, 0, 15)
        assert self.sol.parseSensorPackets([p]) == [["Ultrasonic", 0, 0, 15]]

    def test_all_max_fields(self):
        p = build_packet(2, 4095, 255, 15)
        assert self.sol.parseSensorPackets([p]) == [["Ultrasonic", 4095, 255, 15]]

    # --- Malformed / corrupted packets ---------------------------------------

    def test_single_corrupted_parity_skipped(self):
        bad = corrupt_parity(build_packet(0, 100, 50, 2))
        assert self.sol.parseSensorPackets([bad]) == []

    def test_all_malformed_returns_empty(self):
        packets = [corrupt_parity(build_packet(i % 3, 100 * i, i * 10, i % 16))
                   for i in range(1, 11)]
        assert self.sol.parseSensorPackets(packets) == []

    # --- Mixed valid and malformed -------------------------------------------

    def test_mixed_valid_malformed_order_preserved(self):
        packets = [
            build_packet(0, 100, 50, 1),                       # valid   → LiDAR
            corrupt_parity(build_packet(1, 200, 100, 2)),       # malformed
            build_packet(1, 300, 150, 3),                       # valid   → Radar
            corrupt_parity(build_packet(2, 400, 200, 4)),       # malformed
            build_packet(2, 500, 250, 5),                       # valid   → Ultrasonic
        ]
        assert self.sol.parseSensorPackets(packets) == [
            ["LiDAR",       100,  50, 1],
            ["Radar",       300, 150, 3],
            ["Ultrasonic",  500, 250, 5],
        ]

    def test_valid_sandwiched_by_malformed(self):
        packets = [
            corrupt_parity(build_packet(0, 1, 1, 1)),
            build_packet(1, 42, 99, 5),
            corrupt_parity(build_packet(2, 1, 1, 1)),
        ]
        assert self.sol.parseSensorPackets(packets) == [["Radar", 42, 99, 5]]

    def test_all_valid_multiple_types(self):
        # sensor cycles 1→2→0→1→2, matching Radar/Ultrasonic/LiDAR/…
        packets = [build_packet(i % 3, 100 * i, i * 10, i % 16) for i in range(1, 6)]
        expected = [
            ["Radar",       100, 10, 1],
            ["Ultrasonic",  200, 20, 2],
            ["LiDAR",       300, 30, 3],
            ["Radar",       400, 40, 4],
            ["Ultrasonic",  500, 50, 5],
        ]
        assert self.sol.parseSensorPackets(packets) == expected

    # --- Output format -------------------------------------------------------

    def test_output_element_types(self):
        p = build_packet(0, 200, 128, 7)
        result = self.sol.parseSensorPackets([p])
        assert len(result) == 1
        row = result[0]
        assert len(row) == 4
        sensor, dist, sig, seq = row
        assert isinstance(sensor, str)
        assert isinstance(dist, int)
        assert isinstance(sig, int)
        assert isinstance(seq, int)

    # --- Performance ---------------------------------------------------------

    def test_large_all_valid(self):
        random.seed(42)
        packets = [
            build_packet(random.randint(0, 3), random.randint(0, 4095),
                         random.randint(0, 255), random.randint(0, 15))
            for _ in range(100_000)
        ]
        result = self.sol.parseSensorPackets(packets)
        assert len(result) == 100_000

    def test_large_all_malformed(self):
        random.seed(7)
        packets = [
            corrupt_parity(build_packet(random.randint(0, 3), random.randint(0, 4095),
                                        random.randint(0, 255), random.randint(0, 15)))
            for _ in range(100_000)
        ]
        assert self.sol.parseSensorPackets(packets) == []
