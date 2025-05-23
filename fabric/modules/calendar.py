from imports import *


class CalendarPopUp(WaylandWindow):
    def __init__(self):
        self.current_time = datetime.now()
        self.shown_month = self.current_time.month
        self.shown_year = self.current_time.year

        self.calendar_label = Label(
            label=f"{month_name[self.shown_month]} {self.shown_year}",
            style_classes="calendar-label",
        )
        self.month_stack = Stack(
            transition_duration=Config.transition_duration,
            transition_type="slide-left-right",
            children=self.create_month_grid(
                self.current_time.year, self.current_time.month
            ),
        )

        super().__init__(
            title="big-popup",
            anchor="top center",
            visible=False,
            child=Box(
                orientation="v",
                children=[
                    Box(
                        children=[
                            Button(
                                h_expand=True,
                                label="←",
                                style_classes="cool-button",
                                on_clicked=lambda *args: self.cycle_handler("previous"),
                            ),
                            self.calendar_label,
                            Button(
                                h_expand=True,
                                label="→",
                                style_classes="cool-button",
                                on_clicked=lambda *args: self.cycle_handler("next"),
                            ),
                        ]
                    ),
                    Box(
                        children=[
                            Label(label=f"{day[:-1]}", name="week-days")
                            for day in day_abbr
                        ]
                    ),
                    self.month_stack,
                ],
            ),
        )

    def update_calendar(self, year_to_show, month_to_show, direction):
        self.shown_month = month_to_show
        self.shown_year = year_to_show
        self.calendar_label.set_label(
            f"{month_name[self.shown_month]} {self.shown_year}"
        )
        child = self.create_month_grid(year_to_show, month_to_show)
        stack_label = f"{year_to_show}/{month_to_show}"

        if not self.month_stack.get_child_by_name(stack_label):
            self.month_stack.add_named(child, name=stack_label)

            if direction == "previous":
                self.month_stack.child_set_property(child, "position", 0)

        self.month_stack.set_visible_child_name(stack_label)

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

        self.update_calendar(year_to_show, month_to_show, direction)  # type:ignore

    def create_month_grid(self, year, month):
        month = [day for day in Calendar().itermonthdays3(year, month)]

        # Pad month to 42 days so every grid is 7x6
        while True:
            if len(month) == 42:
                break

            # Get last date, increase the day until its smaller than it should be
            y, m, d = month[-1]
            if d >= monthrange(y, m)[-1]:
                d = 0
                m += 1
            month.append((y, m, d + 1))

        # Split padded month into weeks
        month = [month[i : i + 7] for i in range(0, len(month), 7)]

        month_grid = Gtk.Grid(visible=True)

        for week in month:
            for date in week:
                month_grid.attach(
                    Label(
                        label=f"{date[-1]}",
                        style_classes=self.check_if_current_day(date),
                    ),
                    week.index(date),
                    month.index(week),
                    1,
                    1,
                )

        return month_grid

    def check_if_current_day(self, shown_date):
        current_date = (
            self.current_time.year,
            self.current_time.month,
            self.current_time.day,
        )

        return (
            ["date", "current"]
            if shown_date == current_date
            else ["date", "passive"]
            if shown_date[1] != self.shown_month
            else ["date"]
        )


calendar_pop_up = CalendarPopUp()
