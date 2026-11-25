"""
ADT proxy for Enhancement Spots commands
"""

import sap.adt
import sap.adt.whereused
import sap.cli.core


class CommandGroup(sap.cli.core.CommandGroup):
    """Commands for Enhancement Spots"""

    def __init__(self):
        super().__init__('enhs')

    def install_parser(self, arg_parser):
        super().install_parser(arg_parser)

        arg_parser.add_argument('enhancement_spot', help='Enhancement Spot Name')


@CommandGroup.command('list-implementations')
def list_implementations(connection, args):
    """List Enhancement Implementations of the given Enhancement Spot
    """

    console = args.console_factory()

    enhs = sap.adt.EnhancementSpot(connection, args.enhancement_spot)
    impls = enhs.get_implementations()
    for impl in impls:
        console.printout(f'{impl}')


@CommandGroup.command('whereused')
def whereused(connection, args):
    """Find objects that reference the given Enhancement Spot (BAdI definition)

    enhancement_spot is declared at the group level (install_parser), consistent
    with list-implementations. Usage: sapcli enhs SPOT_NAME whereused
    """

    console = args.console_factory()

    obj = sap.adt.EnhancementSpot(connection, args.enhancement_spot)
    result = sap.adt.whereused.where_used(connection, obj.full_adt_uri)

    for ref_obj in result.referenced_objects:
        adt_obj = ref_obj.adt_object
        typ = adt_obj.typ or ''
        console.printout(f'  {typ} {adt_obj.name}')
