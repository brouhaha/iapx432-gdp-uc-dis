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
    Uinst_Descr('1100 AAAA AAAA AAAA', '1',   'Branch'), # one delay slot
    Uinst_Descr('1101 AAAA AAAA AAAA', '1',   'Conditional Branch'), # one delay slot
    Uinst_Descr('1110 AAAA AAAA AAAA', '1',   'Call Microsubroutine'), # one delay slot
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
    Uinst_Descr('1111 0XX0 1010 XXXX', '1',   'Return From Microsubroutine'), # one delay slot
    Uinst_Descr('1111 0XX0 1011 XXXX', '1',   'Set Trace Fault'), # encoding in patent conflicts with Access Destination

    Uinst_Descr('1111 0JJ0 1111 WVVV', '1',   'Access Destination'), # inst unit translates to Access Memory or Operand Stack Access
                                                          # encoding in patent conflicts with Set Trace Fault
                                                          # this encoding is a guess

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



ui_decode = [None] * 65536

uinst_info = [None] * len(uinst_descr)

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


def dis_field_generic(s, fields, fc):
    field = '%c=0x%x' % (fc, fields[fc])
    return field

def dis_field_b(s, fields, fc):
    return 'seg=' + ['entry-access-list',
                     'public-access-list',
                     'context',
                     'private-access-list',
                     'segment-table-dir',
                     'processor',
                     'disp-port',
                     'process',
                     'process-control',
                     'context-control',
                     'instruction',
                     'operand-stack',
                     'work-reg-A',
                     'work-reg-B',
                     'data-seg-cache',
                     'seg-table-cache'][fields[fc]]

def dis_field_c(s, fields, fc):
    if s == 'Perform Operation':
        return 'op=' + ['short-ord-mult',
                        'short-int-mult',
                        'ord-mult',
                        'int-mult',
                        'short-ord-div',
                        'short-ord-rem',
                        'short-int-div',
                        'short-int-rem',
                        'ord-div',
                        'ord-rem',
                        'int-div',
                        'int-rem',
                        '64-ord-div',
                        '64-mod',
                        '64-ord-mult',
                        '64-square-root'][fields[fc]]
    elif s == 'Move Condition to Branch Flag':
        return 'cond=' + ['destination_stack_flag',
                          'lookahead_mode',
                          'ipc',
                          'unk3'][fields[fc]]
    else: # Conditionally Shift by Sixteen
        return 'src=' + ['DEQA', 'DEQB'][fields[fc]]

def dis_field_f(s, fields, fc):
    if s == 'Convert Flag to Boolean':
        return 'flag=' + ['zero',
                          'sign',
                          'carry',
                          'opaz',
                          'sa',
                          'nsign-and-nzero',
                          'sign-and-nzero',
                          'round',
                          'guard',
                          'greater-than-ordinal',
                          'greater-than-integer',
                          'greater-than-or-equal-integer',
                          'equal-real',
                          'greater-than-real',
                          'greater-than-or-equal-real',
                          'unkF'][fields[fc]]
    else:  # Return Flag to Instruction Unit Branch Condition
        return 'flag=' + ['zero',
                          'sign',
                          'carry',
                          'opaz',
                          'sa',
                          'sa-xnor-sb',
                          'opbz',
                          'opaz-or-opbz',
                          'prec-ctrl-24-or-53',
                          'prec-ctrl-24',
                          'sub-mag-zero-result',
                          'lsb',
                          'unnb-or-sign',
                          'trace',
                          'unkE',
                          'unkF'][fields[fc]]

def dis_field_l(s, fields, fc):
    return 'op=' + ['zero',
                    'not-a-and-not-b',
                    'not-a-and-b',
                    'not-a',
                    'a-and-not-b',
                    'not-b',
                    'a-xor-b',
                    'not-a-or-not-b',
                    'a-and-b',
                    'a-xnor-b',
                    'b',
                    'not-a-or-b',
                    'a',
                    'a-or-not-b',
                    'a-or-b',
                    'ones'][fields[fc]]

def dis_field_r(s, fields, fc):
    return 'reg=' + ['seg-sel-stack',
                     'disp-stack',
                     'ip-stack',
                     'sp-stack',
                     'exponent-stack',
                     'fifo',
                     'fault-encoding',
                     'unknown7',
                     'process-timer',
                     'system-timer',
                     'tempB',
                     'on-chip-stack-count',
                     'context-status',
                     'processor-status',
                     'process-status',
                     'inst-seg-sel'][fields[fc]]

def dis_field_t(s, fields, fc):
    return 'type='+['char',
                    'shortordinal',
                    'ordinal',
                    '16nonfaulting',
                    '16flagsunchanged',
                    'shortinteger',
                    'integer',
                    '16nonfaulting-carry'][fields[fc]]

def dis_field_v(s, fields, fc):
    return 'size='+str([8, 16, 32, 48, 64, 80, 'inst', 'segsel'][fields[fc]])

def dis_field_w(s, fields, fc):
    return ['read', 'write'][fields[fc]]

dis_field_dispatch = { 'B' : dis_field_b,
                       'C' : dis_field_c,
                       'F' : dis_field_f,
                       'L' : dis_field_l,
                       'R' : dis_field_r,
                       'T' : dis_field_t,
                       'V' : dis_field_v,
                       'W' : dis_field_w }

def dis_field(s, fields, fc):
    return dis_field_dispatch.get(fc, dis_field_generic)(s, fields, fc)

def disassemble(opcode):
    i = ui_decode[opcode]
    fields = {}
    fdis = []
    if i is None:
        s = "unknown"
    else:
        s = uinst_descr[i].descr
        for fc in uinst_info[i].fields:
            pos, cnt = uinst_info[i].fields[fc]
            val = (opcode >> pos) & ((1 << cnt) - 1)
            fields[fc] = val
        for fc in uinst_info[i].fields:
            fdis += [dis_field(s, fields, fc)]
    return s,fdis



for i in range(len(uinst_descr)):
    uinst_info[i] = parse_bits(uinst_descr[i].bits_str)
    #print uinst_descr[i].descr, "%04x" % uinst_info[i].const_mask, "%04x" % uinst_info[i].const_bits, uinst_info[i].fields
    min = uinst_info[i].const_bits
    max = uinst_info[i].const_bits + (uinst_info[i].const_mask ^ 0xffff)
    for j in range(min, max+1):
        if j & uinst_info[i].const_mask == uinst_info[i].const_bits:
            assert ui_decode[j] is None
            ui_decode[j] = i

fn = 'ucode-dump.txt'
with open(fn, 'r') as f:
    ucode = [int(l.strip(),16) for l in f.readlines()]

assert len(ucode) == 4096

if False:
    unk = { }
    for i in range(len(ucode)):
        ui = ucode[i]
        di,fields = disassemble(ui)
        if di == 'unknown':
            if ui not in unk:
                unk[ui] = 0
            unk[ui] += 1

    for o in sorted(unk.keys()):
        print "%04x: %d" % (o, unk[o])

space_after = [0] * 4096

call_target_ref = {}
branch_target_ref = {}
cond_branch_target_ref = {}

def add_target_ref(d, t, i):
    if t not in d:
        d[t] = set()
    d[t].add(i)

for i in range(len(ucode)):
    di,fields = disassemble(ucode[i])
    t = ucode[i] & 0xfff
    if di == 'Call Microsubroutine':
        add_target_ref(call_target_ref, t, i)
    elif di == 'Branch':
        add_target_ref(branch_target_ref, t, i)
        space_after[i+1] += 1
    elif di == 'Conditional Branch':
        add_target_ref(cond_branch_target_ref, t, i)
    elif di == 'Return From Microsubroutine':
        space_after[i+1] += 1
    elif di == 'End of Macro Instruction':
        space_after[i] += 1

for i in range(len(ucode)):
    di,fields = disassemble(ucode[i])
    tflags = ''
    if i in call_target_ref:
        tflags += 'S'
        print '; called from: ' + ','.join(['%04x' % a for a in sorted(call_target_ref[i])])
    if i in branch_target_ref:
        tflags += 'B'
        print '; branched from: ' + ','.join(['%04x' % a for a in sorted(branch_target_ref[i])])
    if i in cond_branch_target_ref:
        tflags += 'C'
        print '; cond branched from: ' + ','.join(['%04x' % a for a in sorted(cond_branch_target_ref[i])])
    print "%3s %04x: %04x %s %s" % (tflags, i, ucode[i], di, ', '.join(fields))
    if space_after[i] > 0:
        print


