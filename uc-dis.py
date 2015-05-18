#!/usr/bin/python2
import collections
import string

# From US patent 4,325,120 "Data Processing System" section 11, pp. 106 ff.

Uinst_Descr = collections.namedtuple('Uinst_Descr', ['bits_str', 'cycles_str', 'descr'])
Uinst_Info = collections.namedtuple('Uinst_info', ['const_mask', 'const_bits', 'dont_care_mask', 'fields'])

uinst_descr = [
    Uinst_Descr('000M PJJQ WVVV BBBB', 'var', 'Access Memory'),
    Uinst_Descr('0010 0010 W001 XXXX', 'var', 'Local Access'),
    Uinst_Descr('0010 1JJQ WVVV MXXX', 'var', 'Access List Access'),
    Uinst_Descr('0011 0XX0 0110 1010', 'var', 'Instruction Segment Read'),
    Uinst_Descr('0011 1JJ0 WVVV 1011', 'var', 'Operand Stack Access'),
    Uinst_Descr('0100 0SSD DTTT 0110', '2-3', 'Add'),
    Uinst_Descr('0100 0SSD DTTT 1001', '2-3', 'Subtract'),
    Uinst_Descr('0100 1SSD DTTT 0110', '2-3', 'Decrement'),
    Uinst_Descr('0100 1SSD DTTT 1001', '2-3', 'Increment'),
    Uinst_Descr('0101 0SSD DTTT XXX0', '2-3', 'Absolute Value'),
    Uinst_Descr('0101 0SSD DTTT 1001', '2-3', 'Negate'),
    Uinst_Descr('0101 1SSX X001 0110', '2',   'Add to Displacement Stack'),
    Uinst_Descr('0101 1SSX X010 0110', '2',   'Add to IP Stack'),
    Uinst_Descr('0101 1SSX X100 0110', '2',   'Add to Exponent Stack'),
    Uinst_Descr('0110 0SSD DRJT AABB', '1',   'Extract'),
    Uinst_Descr('0110 1SSD DTTT LLLL', '1-2', 'Logical Operation'),
    Uinst_Descr('0111 0SSD DXXX XXXX', '2',   'Significant Bit'),
    Uinst_Descr('0111 1SSD DVVV 0100', '2',   'Scale Displacement'),
    Uinst_Descr('1000 0SS0 RRRR LLLL', '1',   'DEQ OP DEQ to Register'),
    Uinst_Descr('1000 0DD1 RRRR LLLL', '1',   'OP DEQ to DEQ'),
    Uinst_Descr('1000 1DDA AAAA LLLL', '1',   'ROM OP DEQ to DEQ'),
    Uinst_Descr('1001 0SSF FFFI XXXX', '2',   'Return Flag to Instruction Unit Branch Condition'),
    Uinst_Descr('1001 1DDF FFFI 0101', '2',   'Convert Flag to Boolean'),
    Uinst_Descr('1010 0SS0 000K KKKK', '1',   'Move Constant to Displacement Stack'),
    Uinst_Descr('1010 0SS0 001K KKKK', '1',   'Move Constant to Extractor Shift Count'),
    Uinst_Descr('1010 0SS0 0110 XXXX', '1',   'Reset Execution Unit Fault State'),
    Uinst_Descr('1010 0SS0 0111 XXXX', '1',   'Test Write Rights'),
    Uinst_Descr('1010 0SS0 1000 XXXX', '1',   'Clear Operand Sign Bits'),
    Uinst_Descr('1010 0SS0 1001 XXXX', '1',   'Exchange Flags'),
    Uinst_Descr('1010 0SS0 1010 XXXX', '1',   'Invert SA'),
    Uinst_Descr('1010 0SS0 1100 XXXX', '1',   'No Operation'),
    Uinst_Descr('1010 0SS1 0000 XXXX', '1',   'Invalidate Data Segment Cache Register'),
    Uinst_Descr('1010 0SS1 0001 XXXX', '1',   'Invalidate Data Segment Cache Register Set'),
    Uinst_Descr('1010 0SS1 0010 XXXX', '1',   'Invalidate Data Segment Cache'),
    Uinst_Descr('1010 0SS1 0011 XXXX', '1',   'Invalidate Segment Table Cache'),
    Uinst_Descr('1010 0SS1 010X XXXX', '1',   'Stop Process Timer'),
    Uinst_Descr('1010 0SS1 011X XXXX', '1',   'Start Process Timer'),
    Uinst_Descr('1010 0SS1 1000 BBBB', '1',   'Load Rights'),
    Uinst_Descr('1010 0SS1 1001 BBBB', '1',   'Load Physical Address Lower'),
    Uinst_Descr('1010 0SS1 1010 BBBB', '1',   'Load Physical Address Upper'),
    Uinst_Descr('1010 0SS1 1011 BBBB', '1',   'Load Segment Length'),
    Uinst_Descr('1010 0001 110C LLLL', '1',   'Conditionally Shift by Sixteen'),
    Uinst_Descr('1010 0SS1 111U LLLL', '1',   'Move to Extractor Shift Count'),
    Uinst_Descr('1010 1XXX XXXX CCCC', 'var', 'Perform Operation'),
    Uinst_Descr('1011 0SSZ KKKK KKKK', '2',   'Test Segment Type'),
    Uinst_Descr('1100 AAAA AAAA AAAA', '1',   'Branch (one delay slot)'),
    Uinst_Descr('1101 AAAA AAAA AAAA', '1',   'Conditional Branch (one delay slot)'),
    Uinst_Descr('1110 AAAA AAAA AAAA', '1',   'Call Microsubroutine (one delay slot)'),
    Uinst_Descr('1111 0XX0 0000 XXXX', '1',   'Stop Instruction Decoder and Flush Composer'),
    Uinst_Descr('1111 0XX0 0001 XXXX', '1',   'Start Instruction Decoder'),
    Uinst_Descr('1111 0XX0 0010 XXXX', '1',   'Pop Bit Pointer Stack'),
    Uinst_Descr('1111 0XX0 0011 XXXX', '1',   'Move TBIP to BIP'),
    Uinst_Descr('1111 0XX0 0100 XXXX', '1',   'Move Bit Pointer Stack to XBUF'),
    Uinst_Descr('1111 0XX0 0101 XXXX', '1',   'Set Invalid Class Fault'),
    Uinst_Descr('1111 0XX0 0110 XXXX', '1',   'Issue IPC Function'),
    Uinst_Descr('1111 0XX0 0111 XXXX', '1',   'Set Processor Fatal Condition Pin'),
    Uinst_Descr('1111 0XX0 1000 XXXX', '1',   'Restart Current Access Microinstruction'),
    Uinst_Descr('1111 0XX0 1001 XXCC', '1',   'Move Condition to Branch Flag'),
    Uinst_Descr('1111 0XX0 1010 XXXX', '1',   'Return From Microsubroutine (one delay slot)'),
    Uinst_Descr('1111 0XX0 1011 XXXX', '1',   'Set Trace Fault'), # encoding in patent conflicts with Access Destination

#    Uinst_Descr('1111 0JJ0 1011 WVVV', '1',   'Access Destination'), # inst unit translates to Access Memory or Operand Stack Access
                                                          # encoding in patent conflicts with Set Trace Fault
    Uinst_Descr('1111 1SS0 0000 XXXX', '3',   'Transfer Operator Fault Encoding'),
    Uinst_Descr('1111 1SS0 0001 0000', '3',   'Transfer Logical Address'),
    Uinst_Descr('1111 1SS0 0010 RRRR', '2',   'Transfer Data to Register'),
    Uinst_Descr('1111 1SS0 0011 XXXX', '1',   'Set Lookahead Mode'),
    Uinst_Descr('1111 1SS0 0100 XXXX', '1',   'Reset Processor'),
    Uinst_Descr('1111 1SS0 0110 XXXX', '1',   'End of Branch Macro Instruction'),
    Uinst_Descr('1111 1SS0 0111 XXXX', '1',   'End of Macro Instruction'),
    Uinst_Descr('1111 1SS0 1001 XXXX', '1',   'Reset IP and Stack to Instruction Start'),
    Uinst_Descr('1111 1SS0 1010 LLLL', '1',   'Transfer DEQ to BIP')
]



def parse_bits(bits_str):
    assert len(bits_str) == 19 and bits_str[4] == ' ' and bits_str[9] == ' ' and bits_str[14] == ' '
    bits_str = bits_str[0:4] + bits_str[5:9] + bits_str[10:14] + bits_str[15:19]
    fields = { }
    const_bits = 0
    const_mask = 0
    dc_mask = 0
    for i in range(16):
        c = bits_str[15-i] 
        if c in '01':
            const_bits += int(c) << i
            const_mask += 1 << i
        elif c == 'X':
            dc_mask += 1 << i
        else:
            assert c in string.ascii_uppercase
            if c not in fields:
                fields[c] = [i, 1]
            else:
                assert i == fields[c][0] + fields[c][1]
                fields[c][1] += 1
    return Uinst_Info(const_mask, const_bits, dc_mask, fields)


ui_decode = [None] * 65536

uinst_info = [None] * len(uinst_descr)

for i in range(len(uinst_descr)):
    uinst_info[i] = parse_bits(uinst_descr[i].bits_str)
    #print uinst_descr[i].descr, "%04x" % uinst_info[i].const_mask, "%04x" % uinst_info[i].const_bits, uinst_info[i].fields
    min = uinst_info[i].const_bits
    max = uinst_info[i].const_bits + (uinst_info[i].const_mask ^ 0xffff)
    for j in range(min, max+1):
        if j & uinst_info[i].const_mask == uinst_info[i].const_bits:
            assert ui_decode[j] is None
            ui_decode[j] = i

