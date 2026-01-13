import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import (
    DialogManager,
    ShowMode,
    StartMode,
)
from aiogram_dialog.api.entities.context import Context
from aiogram_dialog.widgets.kbd import (
    Button,
    Calendar,
    CalendarScope,
    ManagedCalendar,
)
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarScopeView,
    CalendarDaysView,
    CalendarMonthView,
    CalendarYearsView,
    CalendarUserConfig,
    DATE_TEXT,
    TODAY_TEXT,
)
from aiogram_dialog.widgets.text import Text, Format
from babel.dates import get_day_names, get_month_names
from datetime import date, datetime
from typing import TypedDict
from zoneinfo import ZoneInfo

from dialogs.states import StartSG, Mail


logger = logging.getLogger(__name__)


class CalendarData(TypedDict):
    current_scope: str
    current_offset: str


class WeekDay(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_day_names(
            width="short", context="stand-alone", locale=locale,
        )[selected_date.weekday()].title()


class MarkedDay(Text):
    def __init__(self, mark: str, other: Text):
        super().__init__()
        self.mark = mark
        self.other = other

    async def _render_text(self, data, manager: DialogManager) -> str:
        current_date: date = data["date"]
        serial_date = current_date.isoformat()
        selected = manager.dialog_data.get("selected_dates", [])
        if serial_date in selected:
            return self.mark
        return await self.other.render_text(data, manager)


class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: date = data["date"]
        locale = manager.event.from_user.language_code
        return get_month_names(
            "wide", context="stand-alone", locale=locale,
        )[selected_date.month].title()


class CustomCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                date_text=MarkedDay("🔴", DATE_TEXT),
                today_text=MarkedDay("⭕", TODAY_TEXT),
                header_text="~~~~~ " + Month() + " ~~~~~",
                weekday_text=WeekDay(),
                next_month_text=Month() + " >>",
                prev_month_text="<< " + Month(),
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                month_text=Month(),
                header_text="~~~~~ " + Format("{date:%Y}") + " ~~~~~",
                this_month_text="[" + Month() + "]",
            ),
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
            ),
        }

    async def _get_user_config(
            self,
            data: dict,
            manager: DialogManager,
    ) -> CalendarUserConfig:
        """
        User related config getter.

        Override this method to customize how user config is retrieved.

        :param data: data from window getter
        :param manager: dialog manager instance
        :return:
        """

        tz = ZoneInfo("Asia/Yekaterinburg")

        calendar_config = CalendarUserConfig(
            timezone=tz
        )

        return calendar_config

    def get_scope(self, manager: DialogManager) -> CalendarScope:
        return CalendarScope.MONTHS
        # calendar_data: CalendarData = self.get_widget_data(manager, {})
        # current_scope = calendar_data.get("current_scope")
        # if not current_scope:
        #     return CalendarScope.DAYS

        # try:
        #     return CalendarScope(current_scope)
        # except ValueError:
        #     # LOG
        #     return CalendarScope.DAYS


async def exit_mail(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.start(
        state=StartSG.main,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.EDIT,
    )


async def to_find_receipts(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager
) -> None:

    await dialog_manager.switch_to(
        state=Mail.calendar,
        show_mode=ShowMode.EDIT,
    )


async def on_date_select(
    callback: CallbackQuery,
    widget: ManagedCalendar,
    dialog_manager: DialogManager,
    clicked_date: date
) -> None:

    context: Context = dialog_manager.current_context()
    calendar_data: dict = context.widget_data.get("calendar")
    current_date_str: str = calendar_data.get("current_offset")
    current_date: date = datetime.fromisoformat(current_date_str).date()

    print(current_date, clicked_date)
