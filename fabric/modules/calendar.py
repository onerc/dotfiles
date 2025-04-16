from imports import *
from config import Config


class theCalendar(Box):
    def __init__(self):
        self.current_time = datetime.now()
        self.shown_year = self.current_time.year
        self.shown_month = self.current_time.month

        self.calendar_label = Label(self.current_time.strftime("%A | %d.%m.%Y"))
        self.month_stack = Stack(
            transition_duration=Config.transition_duration,
            transition_type="slide-left-right",
            children=self.create_grid(self.current_time.year, self.current_time.month),
        )

        super().__init__(
            children=[
                Button(
                    label="<",
                    style_classes="cool-button",
                    on_clicked=lambda *args: self.cycle_handler("previous"),
                ),
                Box(
                    orientation="v",
                    children=[
                        self.calendar_label,
                        Box(
                            children=[
                                Label(label=f"{day[:-1]}", name="week_days")
                                for day in day_abbr
                            ]
                        ),
                        self.month_stack,
                    ],
                ),
                Button(
                    label=">",
                    style_classes="cool-button",
                    on_clicked=lambda *args: self.cycle_handler("next"),
                ),
            ]
        )

    def update_calendar(self, year_to_show, month_to_show, direction):
        self.calendar_label.set_label(f"Shown date: {year_to_show}/{month_to_show}")

        child = self.create_grid(year_to_show, month_to_show)
        stack_label = f"{year_to_show}/{month_to_show}"

        if not self.month_stack.get_child_by_name(stack_label):
            self.month_stack.add_named(child, name=stack_label)

            if direction == "previous":
                self.month_stack.child_set_property(child, "position", 0)

        self.month_stack.set_visible_child_name(stack_label)

        self.shown_month = month_to_show
        self.shown_year = year_to_show

    def cycle_handler(self, direction):
        match direction:
            case "previous":
                if self.shown_month == 1:
                    month_to_show = 12
                    year_to_show = self.shown_year - 1
                else:
                    month_to_show = self.shown_month - 1
                    year_to_show = self.shown_year
            case "next":
                if self.shown_month == 12:
                    month_to_show = 1
                    year_to_show = self.shown_year + 1
                else:
                    month_to_show = self.shown_month + 1
                    year_to_show = self.shown_year

        self.update_calendar(year_to_show, month_to_show, direction)  # type: ignore

    def create_grid(self, year_to_show, month_to_show):
        month_grid = Gtk.Grid(visible=True)

        month_to_show = [
            day for day in Calendar().itermonthdays(year_to_show, month_to_show)
        ]
        self.add_padding(month_to_show)
        month_to_show = [
            month_to_show[i : i + 7] for i in range(0, len(month_to_show), 7)
        ]
        column = 0
        row = 0
        for week in month_to_show:
            for day in week:
                month_grid.attach(self.check_if_valid_day(day), column, row, 1, 1)
                column += 1
            column = 0
            row += 1

        return month_grid

    @staticmethod
    def check_if_valid_day(day):
        return (
            Label(label=f"{day}", name="date")
            if day
            else Label(label="x", name="invalid_date")
        )

    @staticmethod
    def add_padding(list_to_pad):
        """
        Pads every month to 42 days so every grid is 7x6
        """
        while True:
            if len(list_to_pad) == 42:
                break
            list_to_pad.append(0)
