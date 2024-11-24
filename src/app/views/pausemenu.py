import arcade
import arcade.gui
from app.constants.ui import BUTTON_WIDTH

class PauseMenu(arcade.View):
    def __init__(self, previous_view: arcade.View):
        super().__init__()

        self.previous_view = previous_view
        self.manager = arcade.gui.UIManager()
        self._root_dir = None

    def setup(self, root_dir):
        self._root_dir = root_dir
        self.window.set_mouse_visible(True)
        self.manager = arcade.gui.UIManager()
        btn_continue = arcade.gui.UIFlatButton(
            text = _('Continue'),
            width=BUTTON_WIDTH,
        )

        @btn_continue.event("on_click")
        def on_click_btn_continue(event):
            self.on_continue()

        btn_exit = arcade.gui.UIFlatButton(
            text=_('Back to Menu'),
            width=BUTTON_WIDTH
        )

        @btn_exit.event("on_click")
        def on_click_btn_exit(event):
            self.on_exit()


        grid = arcade.gui.UIGridLayout(column_count=2, row_count=2, vertical_spacing=20)
        grid.add(btn_continue, row=0)
        grid.add(btn_exit, row=1)


        # Passing the main view into menu view as an argument.
        anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=grid,
        )

        self.manager.add(anchor)
        self.manager.enable()

    def on_hide_view(self) -> None:

        self.manager.disable()
        self.manager.clear()
        self.window.set_mouse_visible(False)
        self.manager = None

    def on_draw(self) -> None:
        """ On draw menu """
        self.clear()
        self.manager.draw()


    def on_update(self, delta_time: float) -> None:
        """ On update menu """

        self.manager.on_update(delta_time)

    def on_continue(self) -> None:
        """ On continue game """

        self.window.show_view(self.previous_view)

    def on_exit(self) -> None:
        """ On exit to menu """

        from .startscreen import StartScreen
        start_screen = StartScreen()
        start_screen.setup(self._root_dir)
        self.window.show_view(start_screen)
