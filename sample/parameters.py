import argparse
import platform
import sys


def retrieve():
    py_cmd = ('python3', 'python.exe')[platform.system() == 'Windows'] + ' run.py'
    # spaces = ' ' * (17 - len(py_cmd))
    cmd_description = ('             ╔══════════════════════════════════════════════════╗             \n'
                       '             ║   Loops a snowy tree much like a gif wallpaper   ║             \n'
                       '             ╚══════════════════════════════════════════════════╝             \n'
                       '                                                                              \n'
                       # 'If you are unsure about what value to set an optional argument to, watch the  \n'
                       # '    demonstration by typing --config after any one of the optional arguments. \n'
                       # '- I recommend that everyone starts with configuring the width which can be    \n'
                       # '    executed with the command:                                                \n'
                       # '                                                                              \n'
                       # '$ ' + py_cmd + ' -w --demo                 ' + spaces + '                                \n'
                       # '                                                                              \n'
                       '------------------------------------------------------------------------------')

    parser = argparse.ArgumentParser(usage=py_cmd + ' [options]',
                                     description=cmd_description,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-w', '--width',
                        type=int,
                        metavar='',
                        default=271,
                        help=('WIDTH of the terminal window: (default = 271)               '
                              '271 => characters printed on a single line on a 32-inch     '
                              '          monitor in landscape orientation (23.5 inches)    '
                              '151 => characters printed on a single line on a 32-inch     '
                              '          monitor in portrait orientation (13.37 inches)'))

    parser.add_argument('-s', '--speed',
                        type=str,
                        default='slow',
                        metavar='',
                        choices=['ultra', 'fast', 'average', 'slow'],
                        help=('valid choices=[ultra, fast, average, slow]                  '
                              'SPEED of the refresh: (default = slow)                      '
                              '   slow => the snow falling will print every second'))

    parser.add_argument('-d', '--density',
                        type=str,
                        default='average',
                        metavar='',
                        choices=['ultra', 'heavy', 'average', 'thin'],
                        help=('valid choices=[ultra, fast, average, slow] which equates    '
                              'to percent of [ 75.0, 51.2,    12.8,  3.6] chance of snow.  '
                              'DENSITY of the snow: (default = average)                    '
                              '   average => 12.8 percent chance of snow'))

    parser.add_argument('-t', '--tiers',
                        type=int,
                        default=4,
                        metavar='',
                        choices=range(1, 14),
                        help=('valid range of [1, 13] inclusive                            '
                              'TIERS of tree: (default = 4)                                '
                              '   4 => Tree has 4 triangular tiers'))
    ornaments = parser.add_mutually_exclusive_group(required=False)
    ornaments.add_argument('-y', '--yes',
                           action='store_true',
                           help='YES, display the ornaments on the tree')

    ornaments.add_argument('-n', '--no',
                           action='store_false',
                           help='NO ornaments. Ornaments will not be displayed on the tree')

    vrs_description = ('                                                    \n'
                       '              *   snowy-trees v0.0   *              \n'
                       'Check out if there are any new releases for this at:\n'
                       '\thttps://github.com/Mas9311/snowy-trees/releases')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=vrs_description)

    # if no arguments were provided, print the welcome screen
    if len(sys.argv) == 1:
        print_welcome(parser)

    known_args, unknown_args = parser.parse_known_args()

    if unknown_args:
        # user added unknown args, so print the --help screen
        parser.print_help()
        print()
        if len(unknown_args) is 1:
            unrecognized = ' \'' + unknown_args[0] + '\' is'
        else:
            unrecognized = 's ' + str(unknown_args) + ' are'
        input('\nThe argument' + unrecognized + ' not valid.\n\nPress [Enter] to quit\n>')
        parser.parse_args()  # prints error message and stops execution
        raise Exception('Unknown arguments')  # redundantly raised an Exception to ensure failure

    return known_args


def print_welcome(parser):
    py_cmd = ('python3', 'python.exe')[platform.system() == 'Windows'] + ' run.py'
    h_option = ' --help'
    # d_option = ' -w --demo'
    help_flags = h_option + ' ' * (27 - len(py_cmd + h_option))
    # demo_flags = d_option + ' ' * (27 - len(py_cmd + d_option))

    print('╭┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┲━━━━━━┱┈┈┈╮\n'
          '┊                     ╔═════════════════════════════╗             ┃ v0.0 ┃   ┊\n'
          '┊                     ║   Welcome to snowy-trees!   ║             ┗━━━━━━┛   ┊\n'
          '┊                     ╚═════════════════════════════╝                        ┊\n'
          '┊                                                                            ┊\n'
          '┊0.  In case you have not read any instructions prior, I wanted to tell you  ┊\n'
          '┊        how to access the configurable options.                             ┊\n'
          '┊                                                                            ┊\n'
          '┊1.  If you ever need help, just type -h or --help such as:                  ┊\n'
          '┊    $ ' + py_cmd + help_flags + '                                           ┊\n'
          '┊    It will be printed soon because you are using the defaults.             ┊\n'
          '┊                                                                            ┊\n'
          # '┊2.  When configuring an option, i.e. --width, you can always                ┊\n'
          # '┊       type --demo after any argument such as:                              ┊\n'
          # '┊    $ ' + py_cmd + demo_flags + '                                           ┊\n'
          # '┊    This will give you a short demonstration to better prepare              ┊\n'
          # '┊       you for the given argument.                                          ┊\n'
          # '┊                                                                            ┊\n'
          '╰┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈╯')
    input('\n\nPress [Enter] to print --help:\n>')

    parser.print_help()
    d = ('\n\twidth=' + str(parser.parse_args().width) +
         ',\n\tspeed=' + str(parser.parse_args().speed) +
         ',\n\tdensity=' + str(parser.parse_args().density) +
         ',\n\ttiers=' + str(parser.parse_args().tiers) +
         ',\n\tornaments=' + str(parser.parse_args().yes))
    input(f'\n\n\nPress [Enter] to run with the options set to: {d}\n>')
    print()
