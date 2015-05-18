#!/usr/bin/python2
import string

# From US patent 4,325,120 "Data Processing System" section 11, pp. 106 ff.

uinst_list = [
    ['000M PJJQ WVVV BBBB', 'var', 'Access Memory'],
    ['0010 0010 W001 XXXX', 'var', 'Local Access'],
    ['0010 1JJQ WVVV MXXX', 'var', 'Access List Access'],
    ['0011 0XX0 0110 1010', 'var', 'Instruction Segment Read'],
    ['0011 1JJ0 WVVV 1011', 'var', 'Operand Stack Access'],
    ['0100 0SSD DTTT 0110', '2-3', 'Add'],
    ['0100 0SSD DTTT 1001', '2-3', 'Subtract'],
    ['0100 1SSD DTTT 0110', '2-3', 'Decrement'],
    ['0100 1SSD DTTT 1001', '2-3', 'Increment'],
    ['0101 0SSD DTTT XXX0', '2-3', 'Absolute Value'],
    ['0101 0SSD DTTT 1001', '2-3', 'Negate'],
    ['0101 1SSX X001 0110', '2',   'Add to Displacement Stack'],
    ['0101 1SSX X010 0110', '2',   'Add to IP Stack'],
    ['0101 1SSX X100 0110', '2',   'Add to Exponent Stack'],
    ['0110 0SSD DRJT AABB', '1',   'Extract'],
    ['0110 1SSD DTTT LLLL', '1-2', 'Logical Operation'],
    ['0111 0SSD DXXX XXXX', '2',   'Significant Bit'],
    ['0111 1SSD DVVV 0100', '2',   'Scale Displacement'],
    ['1000 0SS0 RRRR LLLL', '1',   'DEQ OP DEQ to Register'],
    ['1000 0DD1 RRRR LLLL', '1',   'OP DEQ to DEQ'],
    ['1000 1DDA AAAA LLLL', '1',   'ROM OP DEQ to DEQ'],
    ['1001 0SSF FFFI XXXX', '2',   'Return Flag to Instruction Unit Branch Condition'],
    ['1001 1DDF FFFI 0101', '2',   'Convert Flag to Boolean'],
    ['1010 0SS0 000K KKKK', '1',   'Move Constant to Displacement Stack'],
    ['1010 0SS0 001K KKKK', '1',   'Move Constant to Extractor Shift Count'],
    ['1010 0SS0 0110 XXXX', '1',   'Reset Execution Unit Fault State'],
    ['1010 0SS0 0111 XXXX', '1',   'Test Write Rights'],
    ['1010 0SS0 1000 XXXX', '1',   'Clear Operand Sign Bits'],
    ['1010 0SS0 1001 XXXX', '1',   'Exchange Flags'],
    ['1010 0SS0 1010 XXXX', '1',   'Invert SA'],
    ['1010 0SS0 1100 XXXX', '1',   'No Operation'],
    ['1010 0SS1 0000 XXXX', '1',   'Invalidate Data Segment Cache Register'],
    ['1010 0SS1 0001 XXXX', '1',   'Invalidate Data Segment Cache Register Set'],
    ['1010 0SS1 0010 XXXX', '1',   'Invalidate Data Segment Cache'],
    ['1010 0SS1 0011 XXXX', '1',   'Invalidate Segment Table Cache'],
    ['1010 0SS1 010X XXXX', '1',   'Stop Process Timer'],
    ['1010 0SS1 011X XXXX', '1',   'Start Process Timer'],
    ['1010 0SS1 1000 BBBB', '1',   'Load Rights'],
    ['1010 0SS1 1001 BBBB', '1',   'Load Physical Address Lower'],
    ['1010 0SS1 1010 BBBB', '1',   'Load Physical Address Upper'],
    ['1010 0SS1 1011 BBBB', '1',   'Load Segment Length'],
    ['1010 0001 110C LLLL', '1',   'Conditionally Shift by Sixteen'],
    ['1010 0SS1 111U LLLL', '1',   'Move to Extractor Shift Count'],
    ['1010 1XXX XXXX CCCC', 'var', 'Perform Operation'],
    ['1011 0SSZ KKKK KKKK', '2',   'Test Segment Type'],
    ['1100 AAAA AAAA AAAA', '1',   'Branch (one delay slot)'],
    ['1101 AAAA AAAA AAAA', '1',   'Conditional Branch (one delay slot)'],
    ['1110 AAAA AAAA AAAA', '1',   'Call Microsubroutine (one delay slot)'],
    ['1111 0XX0 0000 XXXX', '1',   'Stop Instruction Decoder and Flush Composer'],
    ['1111 0XX0 0001 XXXX', '1',   'Start Instruction Decoder'],
    ['1111 0XX0 0010 XXXX', '1',   'Pop Bit Pointer Stack'],
    ['1111 0XX0 0011 XXXX', '1',   'Move TBIP to BIP'],
    ['1111 0XX0 0100 XXXX', '1',   'Move Bit Pointer Stack to XBUF'],
    ['1111 0XX0 0101 XXXX', '1',   'Set Invalid Class Fault'],
    ['1111 0XX0 0110 XXXX', '1',   'Issue IPC Function'],
    ['1111 0XX0 0111 XXXX', '1',   'Set Processor Fatal Condition Pin'],
    ['1111 0XX0 1000 XXXX', '1',   'Restart Current Access Microinstruction'],
    ['1111 0XX0 1001 XXCC', '1',   'Move Condition to Branch Flag'],
    ['1111 0XX0 1010 XXXX', '1',   'Return From Microsubroutine (one delay slot)'],
    ['1111 0XX0 1011 XXXX', '1',   'Set Trace Fault'], # encoding in patent conflicts with Access Destination

    ['1111 0JJ0 1011 WVVV', '1',   'Access Destination'], # inst unit translates to Access Memory or Operand Stack Access
                                                          # encoding in patent conflicts with Set Trace Fault
    ['1111 1SS0 0000 XXXX', '3',   'Transfer Operator Fault Encoding'],
    ['1111 1SS0 0001 0000', '3',   'Transfer Logical Address'],
    ['1111 1SS0 0010 RRRR', '2',   'Transfer Data to Register'],
    ['1111 1SS0 0011 XXXX', '1',   'Set Lookahead Mode'],
    ['1111 1SS0 0100 XXXX', '1',   'Reset Processor'],
    ['1111 1SS0 0110 XXXX', '1',   'End of Branch Macro Instruction'],
    ['1111 1SS0 0111 XXXX', '1',   'End of Macro Instruction'],
    ['1111 1SS0 1001 XXXX', '1',   'Reset IP and Stack to Instruction Start'],
    ['1111 1SS0 1010 LLLL', '1',   'Transfer DEQ to BIP']
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
    return (const_mask, const_bits, dc_mask, fields)


decode = [None] * 65536

for i in range(len(uinst_list)):
    uinst_info = uinst_list[i]
    (const_mask, const_bits, dc_mask, fields) = parse_bits(uinst_info[0])
    print uinst_info[0], "%04x" % const_mask, "%04x" % const_bits, fields


    
    
