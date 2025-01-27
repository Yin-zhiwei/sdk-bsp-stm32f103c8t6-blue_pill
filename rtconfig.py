import os

# toolchains options
ARCH='arm'
CPU='cortex-m3'
CROSS_TOOL='gcc'

# bsp lib config
BSP_LIBRARY_TYPE = None

# system comes with a compiler toggle switch
USE_DEFAULT_TOOLCHAIN = None

if USE_DEFAULT_TOOLCHAIN:
    if os.getenv('RTT_CC'):
        CROSS_TOOL = os.getenv('RTT_CC')
print('using CROSS_TOOL: {}'.format(CROSS_TOOL)) 

# cross_tool provides the cross compiler
# EXEC_PATH is the compiler execute path, for example, CodeSourcery, Keil MDK, IAR
if  CROSS_TOOL == 'gcc':
    PLATFORM    = 'gcc'
    EXEC_PATH   = r'D:/gcc-arm-none-eabi-10.3-2021.10/bin'
elif CROSS_TOOL == 'keil':
     PLATFORM    = 'armcc'
     EXEC_PATH   = r'D:/Keil_v5'
elif CROSS_TOOL == 'iar':
     PLATFORM    = 'iccarm'
     EXEC_PATH   = r'C:/Program Files (x86)/IAR Systems/Embedded Workbench 8.3'
   

if USE_DEFAULT_TOOLCHAIN:
    if os.getenv('RTT_EXEC_PATH'):
        EXEC_PATH = os.getenv('RTT_EXEC_PATH')
print('CROSS_TOOL path: {}'.format(EXEC_PATH)) 

BUILD = 'debug'

if PLATFORM == 'gcc':
    # toolchains
    PREFIX = 'arm-none-eabi-'
    CC = PREFIX + 'gcc'
    AS = PREFIX + 'gcc'
    AR = PREFIX + 'ar'
    CXX = PREFIX + 'g++'
    LINK = PREFIX + 'gcc'
    TARGET_EXT = 'axf'
    SIZE = PREFIX + 'size'
    OBJDUMP = PREFIX + 'objdump'
    OBJCPY = PREFIX + 'objcopy'

    DEVICE = ' -mcpu=cortex-m3 -mthumb -ffunction-sections -fdata-sections'
    CFLAGS = DEVICE + ' -Dgcc'
    AFLAGS = ' -c' + DEVICE + ' -x assembler-with-cpp -Wa,-mimplicit-it=thumb '
    LFLAGS = DEVICE + ' -Wl,--gc-sections,-Map=out/rt-thread.map,-cref,-u,Reset_Handler -T board/linker_scripts/link.lds'

    CPATH = ''
    LPATH = ''

    if BUILD == 'debug':
        CFLAGS += ' -O2 -gdwarf-2 -g'
        AFLAGS += ' -gdwarf-2'
    else:
        CFLAGS += ' -O2'

    CXXFLAGS = CFLAGS 

    POST_ACTION = OBJCPY + ' -O binary $TARGET out/rtthread.bin\n' + SIZE + ' $TARGET \n'
    POST_ACTION += 'cp out/rtthread.axf out/rtthread.elf\n'

elif PLATFORM == 'armcc':
    # toolchains
    CC = 'armcc'
    CXX = 'armcc'
    AS = 'armasm'
    AR = 'armar'
    LINK = 'armlink'
    TARGET_EXT = 'axf'

    DEVICE = ' --cpu Cortex-M3 '
    CFLAGS = '-c ' + DEVICE + ' --apcs=interwork --c99'
    AFLAGS = DEVICE + ' --apcs=interwork '
    LFLAGS = DEVICE + ' --scatter "board\linker_scripts\link.sct" --info sizes --info totals --info unused --info veneers --list rt-thread.map --strict'
    CFLAGS += ' -I' + EXEC_PATH + '/ARM/ARMCompiler5/include'
    LFLAGS += ' --libpath=' + EXEC_PATH + '/ARM/ARMCompiler5/lib'

    CFLAGS += ' -D__MICROLIB '
    AFLAGS += ' --pd "__MICROLIB SETA 1" '
    LFLAGS += ' --library_type=microlib '
    EXEC_PATH += '/ARM/ARMCompiler5/bin/'

    if BUILD == 'debug':
        CFLAGS += ' -g -O2'
        AFLAGS += ' -g'
    else:
        CFLAGS += ' -O2'


    CXXFLAGS = CFLAGS 
    CFLAGS += ' -std=c99'

    POST_ACTION = 'fromelf --bin $TARGET --output rtthread.bin \nfromelf -z $TARGET'

elif PLATFORM == 'armclang':
    # toolchains
    CC = 'armclang'
    CXX = 'armclang'
    AS = 'armasm'
    AR = 'armar'
    LINK = 'armlink'
    TARGET_EXT = 'axf'

    DEVICE = ' --cpu Cortex-M3 '
    CFLAGS = ' --target=arm-arm-none-eabi -mcpu=cortex-m3 '
    CFLAGS += ' -mcpu=cortex-m3 '
    CFLAGS += ' -c -fno-rtti -funsigned-char -fshort-enums -fshort-wchar '
    CFLAGS += ' -gdwarf-3 -ffunction-sections '
    AFLAGS = DEVICE + ' --apcs=interwork '
    LFLAGS = DEVICE + ' --info sizes --info totals --info unused --info veneers '
    LFLAGS += ' --list rt-thread.map '
    LFLAGS += r' --strict --scatter "board\linker_scripts\link.sct" '
    CFLAGS += ' -I' + EXEC_PATH + '/ARM/ARMCLANG/include'
    LFLAGS += ' --libpath=' + EXEC_PATH + '/ARM/ARMCLANG/lib'

    EXEC_PATH += '/ARM/ARMCLANG/bin/'

    if BUILD == 'debug':
        CFLAGS += ' -g -O1' # armclang recommend
        AFLAGS += ' -g'
    else:
        CFLAGS += ' -O2'
        
    CXXFLAGS = CFLAGS
    CFLAGS += ' -std=c99'

    POST_ACTION = 'fromelf --bin $TARGET --output rtthread.bin \nfromelf -z $TARGET'

elif PLATFORM == 'iccarm':
    # toolchains
    CC = 'iccarm'
    CXX = 'iccarm'
    AS = 'iasmarm'
    AR = 'iarchive'
    LINK = 'ilinkarm'
    TARGET_EXT = 'out'

    DEVICE = '-Dewarm'

    CFLAGS = DEVICE
    CFLAGS += ' --diag_suppress Pa050'
    CFLAGS += ' --no_cse'
    CFLAGS += ' --no_unroll'
    CFLAGS += ' --no_inline'
    CFLAGS += ' --no_code_motion'
    CFLAGS += ' --no_tbaa'
    CFLAGS += ' --no_clustering'
    CFLAGS += ' --no_scheduling'
    CFLAGS += ' --endian=little'
    CFLAGS += ' --cpu=Cortex-M3'
    CFLAGS += ' -e'
    CFLAGS += ' --fpu=None'
    CFLAGS += ' --dlib_config "' + EXEC_PATH + '/arm/INC/c/DLib_Config_Normal.h"'
    CFLAGS += ' --silent'

    AFLAGS = DEVICE
    AFLAGS += ' -s+'
    AFLAGS += ' -w+'
    AFLAGS += ' -r'
    AFLAGS += ' --cpu Cortex-M3'
    AFLAGS += ' --fpu None'
    AFLAGS += ' -S'

    if BUILD == 'debug':
        CFLAGS += ' --debug'
        CFLAGS += ' -Oh'
    else:
        CFLAGS += ' -Oh'

    LFLAGS = ' --config "board/linker_scripts/link.icf"'
    LFLAGS += ' --entry __iar_program_start'

    CXXFLAGS = CFLAGS
    
    EXEC_PATH = EXEC_PATH + '/arm/bin/'
    POST_ACTION = 'ielftool --bin $TARGET rtthread.bin'

