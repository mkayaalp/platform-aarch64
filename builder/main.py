"""
    Builder for AArch64 platform
"""

from os.path import join

from SCons.Script import AlwaysBuild, Default, DefaultEnvironment

env = DefaultEnvironment()

env.Replace(
    AR="aarch64-none-elf-ar",
    AS="aarch64-none-elf-as",
    CC="aarch64-none-elf-gcc",
    LD="aarch64-none-elf-ld",
    GDB="aarch64-none-elf-gdb",
    OBJCOPY="aarch64-none-elf-objcopy",
    RANLIB="aarch64-none-elf-ranlib",
    SIZETOOL="aarch64-none-elf-size",

    SIZEPRINTCMD='$SIZETOOL $SOURCES'
)

env.Append(
    ASFLAGS=[
        "-g"
    ],

    LINKFLAGS=[
        "-nostdlib",
        "-nostartfiles",
        "-Ttext=0x80000"
    ]
)

env.Append(
    BUILDERS=dict(
        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".ihex"
        )
    )
)

target_elf = env.BuildProgram()
target_hex = env.ElfToHex(join("$BUILD_DIR", "${PROGNAME}"), target_elf)

#
# Target: Print binary size
#

target_size = env.Alias("size", target_elf, env.VerboseAction(
    "$SIZEPRINTCMD", "Calculating size $SOURCE"))
AlwaysBuild(target_size)

#
# Default targets
#

Default([target_hex])
