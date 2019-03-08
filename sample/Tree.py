import numpy as np


def set_speed(speed_arg):
    """assigns a number to the variable, Tree.sleep_time which is used to measure
    how fast the screen refreshes (in seconds)"""
    speeds = {'ultra': 0.1, 'fast': 0.465000, 'average': 0.7265000, 'slow': 0.9810000}
    return speeds[speed_arg]


def set_density(density_arg):
    """Assigns a number (max 999) to the variable, Tree.max_snow, which is used
    to gauge the probability of printing the snow character.
    ultra= 733=73.3%.  heavy= 512=51.2%.  average= 128=12.8%.  thin= 36=3.6%"""
    densities = {'ultra': 733, 'heavy': 512, 'average': 128, 'thin': 36}
    return densities[density_arg]


class Tree:
    def __init__(self, arg_dict):
        self.tree_tiers = arg_dict['tiers']
        self.screen_width = arg_dict['width']
        self.sleep_time = set_speed(arg_dict['speed'])
        self.max_snow = set_density(arg_dict['density'])
        self.ornaments = ([], ['⍟', 'x', '♦'])[arg_dict['ornaments']]
        # Additional ornaments  ● x ♦ ○ * ★ ⍟ ❤

        self.tree_width = [t_width for t_width in range(13, 68, 4)][self.tree_tiers]
        self.make_even = (1, 0)[(self.screen_width - self.tree_width) % 2 is 0]
        self.star_char = '★'
        self.leaf_char = '❇'  # ❇ #
        self.snow_char = '*'  # * ❇
        self.base_char = '┆'  # │ ║ ┃ ┆ ┇ ┊ ┋

    def _gen_snow(self, snow_len):
        output = ''
        for _ in range(snow_len):
            rand_snow = int(np.random.random_sample() * 1000)
            output += (' ', self.snow_char)[0 <= rand_snow <= 0 + self.max_snow]
        return output

    def _tree_topper(self):
        output = self._star_line()
        for leaves_width in range(1, 10, 2):  # 1, 3, 5, 7, 9
            output += self._tree_line(leaves_width)
        return self._gen_snow(self.screen_width) + '\n' + output + self._tree_line(13)

    def _tree_shape(self):
        output = ''
        neck = 7
        for _ in range(self.tree_tiers - 1):
            for curr in range(4):
                w = neck + (curr * 4)
                if curr is 0:
                    output += self._tree_line(w, 8)
                elif curr is 1:
                    output += self._tree_line(w, 4)
                else:
                    output += self._tree_line(w)
            neck += 4
        return output

    def _tree_base(self):
        output = ''
        base_width = 1 + ((self.tree_tiers // 2) * 2)
        base_width = (base_width, 9)[base_width > 9]
        base_height = (self.tree_tiers - 1, 1)[self.tree_tiers is 1]
        base_height = (base_height, 6)[base_height > 6]
        for _ in range(base_height):
            output += self._make_base(base_width)
        return output + self._gen_snow(self.screen_width)

    def _star_line(self):
        spaces = ((self.screen_width - 3) // 2)
        return self._gen_snow(spaces) + ' ' + self.star_char + ' ' + self._gen_snow(spaces + self.make_even) + '\n'

    def _tree_line(self, leaves, buffer_len=2):
        buffer = ' ' * (buffer_len // 2)
        leaves_str = self._gen_leaf(leaves)
        spaces = (self.screen_width - (buffer_len + leaves)) // 2
        return self._gen_snow(spaces) + buffer + leaves_str + buffer + self._gen_snow(spaces + self.make_even) + '\n'

    def _gen_leaf(self, leaves):
        output = ''
        for _ in range(leaves):
            r = int(np.random.random_sample() * 1000)
            if 500 <= r < 550 and len(self.ornaments) >= 1:     # 5.0% chance of first ornament
                output += self.ornaments[0]
            elif 600 <= r < 635 and len(self.ornaments) >= 2:   # 3.5% chance of second ornament
                output += self.ornaments[1]
            elif 700 <= r < 725 and len(self.ornaments) >= 3:   # 2.5% chance of third ornament
                output += self.ornaments[2]
            elif 800 <= r < 820 and len(self.ornaments) >= 4:   # 2.0% chance of fourth ornament
                output += self.ornaments[3]
            elif 900 <= r < 915 and len(self.ornaments) >= 5:   # 1.5% chance of fifth ornament
                output += self.ornaments[4]
            else:
                output += self.leaf_char
        return output

    def _make_base(self, width):
        buffer = ' ' * ((self.tree_width - width - 2) // 2)
        base_str = self.base_char * width
        spaces = (self.screen_width - self.tree_width + 2) // 2
        return self._gen_snow(spaces) + buffer + base_str + buffer + self._gen_snow(spaces + self.make_even) + '\n'

    def build_list(self, max_len=25):
        """Returns a list of generated snow and ornament arrangements to be used to print."""
        tree_list = [str(self) for _ in range(max_len)]
        return tree_list

    def __str__(self):
        return (f'{self._tree_topper()}'
                f'{self._tree_shape()}'
                f'{self._tree_base()}')
