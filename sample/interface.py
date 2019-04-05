import time
from tkinter import *
from screeninfo import get_monitors
import pyautogui

from sample.file_helper import make_sure_dir_exists, file_exists, export_file_as, get_filepath, import_from_file
from sample.format import print_change, Notification
from sample.frame.Textbox import Textbox
from sample.frame.Toolbar import ToolbarFrame
from sample.frame.WindowManager import WindowManagerFrame
from sample.image import Tree
from sample.parameters import retrieve_parameters, default_configurations


def run_interface():
    my_tree = Tree(retrieve_parameters())

    if my_tree.arg_dict['interface']:
        root = Tk()
        GUI(root, my_tree)
        root.mainloop()
    else:
        app = CLI(my_tree)
        app.print_indefinitely()


class CLI:
    def __init__(self, my_tree):
        self.tree = my_tree

    def print_indefinitely(self):
        # immediately prints all trees too fill the CLI window with snowy trees
        for _ in range(min(self.tree.length, 50)):
            print(self.tree.list[self.tree.increment_index()])

        # continuous loop that iterates through the list of trees
        while True:
            print(self.tree.list[self.tree.increment_index()])
            # pause execution for the time specified in the --speed argument provided.
            time.sleep(self.tree.sleep_time)


class GUI(Frame):
    def __init__(self, parent, my_tree):
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=True)
        self.root = parent
        self.root.configure(background='black')
        # self.root.image = PhotoImage(file='./assets/icons/transparent.png')  # ToolbarFrame bg will be transparent
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file='./assets/icons/tree_icon.png'))

        # creates the template of the Tree to print; snow & ornaments are unique upon printing.
        self.tree = my_tree

        print(self.tree.arg_dict)
        self.monitors = []

        self.textbox = None
        self.window_manager_frame = None
        self.toolbar_frame = None

        self.update_idletasks()
        self._defined = ['w_dim', 'h_dim', 'x_dim', 'y_dim']
        self.configurations = {}
        self.offsets_are_set = False
        self._create()

        self.set_root()

        self.textbox.print_trees_now()  # immediately fills the current GUI window with trees
        self.textbox.run_gui()  # continue execution

    def _create(self):
        self._create_monitors()
        self._create_configurations()
        self._create_dimensions()

        self.textbox = Textbox(self)
        self.window_manager_frame = WindowManagerFrame(self)
        self.toolbar_frame = ToolbarFrame(self)

    def _create_default_file(self):
        make_sure_dir_exists()
        if not file_exists(get_filepath('default')):
            revert = self.tree
            mouse_x, mouse_y = pyautogui.position()
            pyautogui.moveTo(30, 30)

            re_maximize = retrieve_parameters()['maximized']
            if re_maximize:
                self.set_arg('maximized', True)
                self.window_manager_frame.maximize()

            self.tree = Tree(default_configurations())
            self.tree.update_parameters()
            self.set_arg('x_dim', self.winfo_rootx())  # 3  or  4
            self.set_arg('y_dim', self.winfo_rooty())  # 29 or 54

            export_file_as('default', self.tree.arg_dict, False)
            pyautogui.moveTo(mouse_x, mouse_y)
            self.tree = revert
            if re_maximize:
                self.set_arg('maximized', False)
                self.window_manager_frame.maximize()

        defaults = import_from_file('default', False)
        self.configurations['x_dim']['offset'] = defaults['x_dim']
        self.configurations['y_dim']['offset'] = defaults['y_dim']
        if self.get_arg('verbose'):
            print(f"Offsets set to: x={self.configurations['x_dim']['offset']} "
                  f"y={self.configurations['y_dim']['offset']}")

    def _create_monitors(self):
        screen_info = get_monitors()
        for index, m in enumerate(screen_info[::-1]):  # for me, the monitors are right-to-left.
            print(f'monitor {index}: {m.width}x{m.height}+{m.x}+{m.y}')
            self.monitors.append({
                'w_dim': m.width,
                'h_dim': m.height,
                'x_dim': m.x,
                'y_dim': m.y
            })

    def _create_configurations(self):
        self.configurations['w_dim'] = {'assign': self.assign_width_dim, 'offset': 0}
        self.configurations['h_dim'] = {'assign': self.assign_height_dim, 'offset': 0}
        self.configurations['x_dim'] = {'assign': self.assign_x_dim, 'offset': 0}  # 0 => 3 or 4
        self.configurations['y_dim'] = {'assign': self.assign_y_dim, 'offset': 0}  # 0 => 29 or 54

    def _create_dimensions(self):
        if not self.get_arg('maximized'):
            for curr_dim in self._defined:
                if self.get_arg(curr_dim) is default_configurations()[curr_dim]:  # 0
                    if self.get_arg('verbose'):
                        print(curr_dim, 'is assigned to', self.get_arg(curr_dim))
                    self.configurations[curr_dim]['assign']()
                else:
                    if self.get_arg(curr_dim) is self.configurations[curr_dim]['offset']:
                        if self.get_arg('verbose'):
                            print(curr_dim, 'is default. Subtracting offset')
                        self.set_arg(curr_dim, self.get_arg(curr_dim) - self.configurations[curr_dim]['offset'])
                    else:
                        if self.get_arg('verbose'):
                            print(curr_dim, 'is custom. Leaving it alone')
            # self.correct_height()
        else:
            self.manually_set_dimensions()
    
    def get_arg(self, key):
        return self.tree.arg_dict[key]

    def set_arg(self, key, value):
        self.tree.arg_dict[key] = value

    def get_monitor(self, mouse_x=None, mouse_y=None, message=''):
        if mouse_x is None:
            mouse_x, _ = pyautogui.position()
        if mouse_y is None:
            _, mouse_y = pyautogui.position()
        for index, m in enumerate(self.monitors):
            if m['x_dim'] <= mouse_x <= m['w_dim'] + m['x_dim']:
                if self.get_arg('verbose'):
                    print(f"{message + ' ' if message else ''}mouse on monitor {index}")
                return m

    def get_dimensions(self, type_of_window='gui'):
        if type_of_window == 'gui':
            w = self.get_arg('w_dim')
            h = self.get_arg('h_dim')
            x = self.get_arg('x_dim')
            y = self.get_arg('y_dim')
        else:
            w = self.winfo_width()
            h = self.winfo_height()
            x = self.winfo_rootx()
            y = self.winfo_rooty()

        return f"{w}x{h}+{x}+{y}"

    def set_dimensions(self):
        self.set_arg('w_dim', self.winfo_width())
        self.set_arg('width', self.convert_w_dim())
        self.set_arg('h_dim', self.winfo_height())
        self.set_arg('x_dim', self.winfo_rootx())
        self.set_arg('y_dim', self.winfo_rooty())

        return self.get_dimensions()

    def assign_width_dim(self):
        """Converts width (in characters) to pixels"""
        self.set_arg('w_dim', (self.tree.screen_width + self.tree.make_even) * 6)

    def convert_w_dim(self):
        """Converts pixels to width (in characters)"""
        return self.get_arg('w_dim') // 6 - self.tree.make_even

    def assign_height_dim(self):
        num_trees = 2
        if self.get_arg('textbox') == 'small':
            self.set_arg('h_dim', ((48 * self.tree.tree_tiers) + 53) * num_trees)
        elif self.get_arg('textbox') == 'medium':
            self.set_arg('h_dim', self.tree.screen_height * 13 * num_trees)
        else:
            Notification(['Height unknown', 'Just going to assign 500 pixels?'])
            self.set_arg('h_dim', 500)
        # self.correct_height()

    # def correct_height(self):
    #     current_monitor = self.get_monitor()
    #     max_h = current_monitor['h_dim']
    #
    #     if self.get_arg('h_dim') + self.get_arg('y_dim') > max_h:
    #         self.set_dim('h_dim', self.get_arg('h_dim') - (self.get_arg('h_dim') + self.get_arg('y_dim')) - max_h)
    #         print('correcting h_dim:', self.get_arg('h_dim'))
    #         self.root.geometry('{}x{}+{}+{}'.format(
    #             self.get_arg('w_dim'), self.get_arg('h_dim'), self.get_arg('x_dim'), self.get_arg('y_dim')))

    def assign_x_dim(self):
        self.set_arg('x_dim', self.winfo_x())

    def assign_y_dim(self):
        self.set_arg('y_dim', self.winfo_y())

    def set_root(self):
        self.root.bind('<Configure>', self.window_change)
        self.root.title('Snowy Trees')
        # self.root.overrideredirect(True)
        self.root.resizable(width=True, height=True)

        self.root.geometry('{}x{}+{}+{}'.format(
            self.get_arg('w_dim'), self.get_arg('h_dim'), self.get_arg('x_dim'), self.get_arg('y_dim')))

    def set_screen_width(self):
        before = self.tree.screen_width
        self.reset_tree('width', self.convert_w_dim())
        print_change('Window Width', before, self.tree.screen_width)

    def reset_tree(self, key=None, value=None):
        if key is not None and value is not None:
            self.set_arg(key, value)
        self.tree.update_parameters()
        if key == 'new file':
            if self.get_arg('verbose'):
                print('manually setting the dimensions')
            self.manually_set_dimensions()
        self.textbox.print_trees_now()

    def manually_set_dimensions(self):
        if not self.get_arg('maximized'):
            if self.get_arg('verbose'):
                print('manually set not maximized.')

            before = self.get_dimensions()
            # self.correct_height()
            self.root.geometry('{}x{}+{}+{}'.format(
                self.get_arg('w_dim'), self.get_arg('h_dim'), self.get_arg('x_dim'), self.get_arg('y_dim')))
            self.tree.update_parameters()
            after = self.get_dimensions()

            if before != after:
                if self.get_arg('verbose'):
                    print('manually setting:', before, after)
        else:
            if self.get_arg('verbose'):
                print('manually set maximized.')
            self.tree.update_parameters()

    def have_root_dimensions_changed(self):
        w = self.winfo_width() == self.get_arg('w_dim')
        h = self.winfo_height() == self.get_arg('h_dim')
        x = self.winfo_rootx() == self.get_arg('x_dim')
        y = self.winfo_rooty() == self.get_arg('y_dim')

        return w or h or x or y

    def textbox_change(self):
        if not self.get_arg('maximized'):
            if self.get_arg('verbose'):
                print('textbox not maximized.')
            before = self.get_dimensions('window')
            self.set_dimensions()

            if abs(self.get_arg('y_dim') - self.winfo_rooty()) == (2 * self.configurations['y_dim']['offset']):
                self.set_arg('y_dim', self.get_arg('y_dim') - (2 * self.configurations['y_dim']['offset']))

            # self.correct_height()

            after = (f"{self.get_arg('w_dim')}x{self.get_arg('h_dim')}+"
                     f"{self.get_arg('x_dim')}+{self.get_arg('y_dim')}")

            self.tree.update_parameters()
            self.textbox.print_trees_now()
            if before != after:
                if self.get_arg('verbose'):
                    print('textbox setting:', before, '=>', after)

                self.root.geometry('{}x{}+{}+{}'.format(
                    self.get_arg('w_dim'), self.get_arg('h_dim'), self.get_arg('x_dim'), self.get_arg('y_dim')))
        else:
            if self.get_arg('verbose'):
                print('textbox maximized.')
            curr_monitor = self.get_monitor(message='current  :')
            requested_monitor = self.get_monitor(self.get_arg('x_dim'), self.get_arg('y_dim'), 'requested:')

            if curr_monitor != requested_monitor:
                mouse_x, mouse_y = pyautogui.position()
                delta_x = (requested_monitor['x_dim'] - mouse_x)  # x distance to top-left corner
                delta_y = (requested_monitor['y_dim'] - mouse_y)  # y distance to top-left corner
                delta_x += (requested_monitor['w_dim'] // 2)  # centered horizontally on requested screen
                delta_y += (requested_monitor['h_dim'] // 2)  # centered  vertically  on requested screen
                pyautogui.move(delta_x, delta_y)  # move mouse to th center of the other screen to prevent the 0 error

            l_border = b_border = r_border = self.configurations['x_dim']['offset']  # { left, bottom, right } borders
            t_border = self.configurations['y_dim']['offset']  # { top } border

            self.set_arg('w_dim', requested_monitor['w_dim'] - (l_border + r_border))
            self.set_arg('h_dim', requested_monitor['h_dim'] - (t_border + b_border))
            self.set_arg('x_dim', requested_monitor['x_dim'])
            self.set_arg('y_dim', requested_monitor['y_dim'])

            self.tree.update_parameters()
            self.textbox.print_trees_now()

            self.set_arg('maximized', False)
            self.window_manager_frame.maximize()

            self.root.geometry('{}x{}+{}+{}'.format(
                self.get_arg('w_dim'), self.get_arg('h_dim'), self.get_arg('x_dim'), self.get_arg('y_dim')))

            if curr_monitor != requested_monitor:
                pyautogui.moveTo(mouse_x, mouse_y)  # move mouse back to its original position

    def wmf_maximize_button_change(self):
        if self.get_arg('maximized'):
            if self.get_arg('verbose'):
                print('WMF changed. maximized =', self.get_arg('maximized'))
            loc_of_gui_monitor = self.get_monitor(self.get_arg('x_dim') + 1, self.get_arg('y_dim') + 1)

            if self.winfo_width() == loc_of_gui_monitor['w_dim']:
                self.set_arg('width', self.convert_w_dim())
                self.tree.update_parameters()
                self.textbox.print_trees_now()

    def root_change(self):
        if self.have_root_dimensions_changed():
            if not self.get_arg('maximized'):
                if self.get_arg('verbose'):
                    print('root not maximized.')
                before = self.get_dimensions('monitor')
                before_w_h, *_ = before.split('+')

                after = self.set_dimensions()
                after_w_h, *_ = after.split('+')

                if before != after:
                    if self.get_arg('verbose'):
                        print('root: setting', before, '=>', after)
                if self.get_arg('maximized'):
                    print('updating the tree parameters')
                    self.tree.update_parameters()
                if before_w_h == after_w_h:
                    if self.get_arg('verbose'):
                        print(f"{self.get_arg('w_dim')}x{self.get_arg('h_dim')}+"
                              f"{self.winfo_rootx() - self.configurations['x_dim']['offset']}+"
                              f"{self.winfo_rooty() - self.configurations['y_dim']['offset']}")
                    self.root.geometry('{}x{}+{}+{}'.format(
                        self.get_arg('w_dim'),
                        self.get_arg('h_dim'),
                        self.winfo_rootx() - self.configurations['x_dim']['offset'],
                        self.winfo_rooty() - self.configurations['y_dim']['offset']
                    ))
            else:
                if self.get_arg('verbose'):
                    print('root maximized.')
                    self.set_arg('width', self.convert_w_dim())

    def window_change(self, event=None):
        if self.winfo_width() is not 1:
            before_w = self.get_arg('w_dim')
            before_h = self.get_arg('h_dim')
            before_x = self.get_arg('x_dim')
            before_y = self.get_arg('y_dim')

            if not self.offsets_are_set:
                self.offsets_are_set = True
                self._create_default_file()

            if event.widget.winfo_id() == self.textbox.winfo_id():
                self.textbox_change()
            elif event.widget.winfo_id() == self.window_manager_frame.winfo_id():
                self.wmf_maximize_button_change()
            elif event.widget.winfo_id() == self.root.winfo_id():
                self.root_change()

            if self.get_arg('verbose'):
                print_change('\t   gui width', before_w, self.get_arg('w_dim'))
                print_change('\t  gui height', before_h, self.get_arg('h_dim'))
                print_change('\tgui x offset', before_x, self.get_arg('x_dim'))
                print_change('\tgui y offset', before_y, self.get_arg('y_dim'))
