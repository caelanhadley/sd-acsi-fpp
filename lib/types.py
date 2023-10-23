class Num:
    F32 = 'F32'
    F64 = 'F64'
    I16 = 'I16'
    I32 = 'I32'
    I64 = 'I64'
    I8 = 'I8'
    U16 = 'U16'
    U32 = 'U32'
    U64 = 'U64'
    U8 = 'U8'
    NUM_TYPES = [F32, F64, I16, I32, I64, I8, U16, U32, U64, U8]

    @staticmethod
    def contains(value):
        return value in Num.NUM_TYPES

class Port:
    # Regular ports
    SYNC_INPUT =    'sync input'
    ASYNC_INPUT =   'async input'
    GUARDED_INPUT = 'guarded input'
    OUTPUT =        'output'

    # Special ports
    COMMAND_RECV =  'command recv'
    COMMAND_REG =   'command reg'
    COMMAND_RESP =  'command resp'
    EVENT =         'event'
    PARAM_GET =     'param get'
    PARAM_SET =     'param set'
    TELEMETRY =     'telemetry'
    TEXT_EVENT =    'text event'
    TIME_GET =      'time get'

    STANDARD_PORTS = [ASYNC_INPUT, SYNC_INPUT, GUARDED_INPUT, OUTPUT]
    SPECIAL_PORTS = [COMMAND_RECV,COMMAND_REG,COMMAND_RESP,
                    EVENT,PARAM_GET,PARAM_SET,TELEMETRY,
                    TEXT_EVENT,TIME_GET]
    
    @staticmethod
    def contains(value):
        return (value in Port.STANDARD_PORTS or value in Port.SPECIAL_PORTS)

class Command:
    KIND_SYNC = 20
    KIND_ASYNC = 21
    KIND_GUARDED = 22
    KINDS = [KIND_SYNC, KIND_ASYNC, KIND_GUARDED]

class Event:
    pass

class Telemetry:
    pass

class QueueFullBehavior:
    pass