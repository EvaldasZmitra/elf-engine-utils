from argparse import ArgumentParser
from os import getcwd
from os.path import join


c_comp_template = """
#include <<name>.h>
#include <stdlib.h>

<name> *<name>_create()
{
    <name> *comp = malloc(sizeof(<name>));
    return comp;
}

void <name>_destroy(<name> *value)
{
    free(value);
}

"""

h_comp_template = """
#ifndef <name>_h
#define <name>_h

typedef struct {

} <name>;

<name> *<name>_create();
void <name>_destroy(<name> *value);

#endif
"""

c_template = """
#include <<name>.h>
#include <elf_sys_enum.h>
#include <<comp>.h>
#include <stdlib.h>

void <name>_advance(elf_entity *entity)
{
    <comp> *comp = entity->comps[<NAME>];
}

elf_system *<name>_create()
{
    elf_system *sys = malloc(sizeof(elf_system));
    unsigned int bitmask[] = {<NAME>};
    sys->is_parallel = 0;
    sys->advance = <name>_advance;
    sys->required_components = elf_bitmask_create(bitmask, sizeof(bitmask) / 4);
    return sys;
}
"""

h_template = """
#ifndef <name>_h
#define <name>_h

#include <elf_system.h>

elf_system *<name>_create();

#endif
"""


def main():
    parser = ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()
    c_path = join(getcwd(), "src", f"{args.name}_sys.c")
    h_path = join(getcwd(), "include", f"{args.name}_sys.h")
    c_comp_path = join(getcwd(), "src", f"{args.name}_comp.c")
    h_comp_path = join(getcwd(), "include", f"{args.name}_comp.h")
    with open(c_path, "w") as f:
        f.write(
            c_template
            .replace("<name>", f"{args.name}_sys")
            .replace("<NAME>", f"{args.name.upper()}_SYSTEM")
            .replace("<comp>", f"{args.name}_comp")
        )
    with open(h_path, "w") as f:
        f.write(h_template.replace("<name>", f"{args.name}_sys"))
    with open(c_comp_path, "w") as f:
        f.write(c_comp_template.replace("<name>", f"{args.name}_comp"))
    with open(h_comp_path, "w") as f:
        f.write(h_comp_template.replace("<name>", f"{args.name}_comp"))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
