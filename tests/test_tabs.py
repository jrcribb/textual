from textual.app import App, ComposeResult
from textual.widgets import Tab, Tabs


async def test_compose_empty_tabs():
    """It should be possible to create an empty Tabs."""

    class TabsApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Tabs()

    async with TabsApp().run_test() as pilot:
        assert pilot.app.query_one(Tabs).tab_count == 0
        assert pilot.app.query_one(Tabs).active_tab is None


async def test_compose_tabs_from_strings():
    """It should be possible to create a Tabs from some strings."""

    class TabsApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Tabs("John", "Aeryn", "Moya", "Pilot")

    async with TabsApp().run_test() as pilot:
        tabs = pilot.app.query_one(Tabs)
        assert tabs.tab_count == 4
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-1"


async def test_compose_tabs_from_tabs():
    """It should be possible to create a Tabs from some Tabs."""

    class TabsApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Tabs(
                Tab("John"),
                Tab("Aeryn"),
                Tab("Moya"),
                Tab("Pilot"),
            )

    async with TabsApp().run_test() as pilot:
        tabs = pilot.app.query_one(Tabs)
        assert tabs.tab_count == 4
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-1"


async def test_add_tabs_after():
    """It should be possible to add tabs later on in the app's cycle."""

    class TabsApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Tabs()

    async with TabsApp().run_test() as pilot:
        tabs = pilot.app.query_one(Tabs)
        assert tabs.tab_count == 0
        assert tabs.active_tab is None
        await tabs.add_tab("John")
        assert tabs.tab_count == 1
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-1"
        await tabs.add_tab("Aeryn")
        assert tabs.tab_count == 2
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-1"


async def test_remove_tabs():
    """It should be possible to remove tabs."""

    class TabsApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Tabs("John", "Aeryn", "Moya", "Pilot")

    async with TabsApp().run_test() as pilot:
        tabs = pilot.app.query_one(Tabs)
        assert tabs.tab_count == 4
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-1"

        await tabs.remove_tab("tab-1")
        await pilot.pause()
        assert tabs.tab_count == 3
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-2"

        await tabs.remove_tab(tabs.query_one("#tab-2", Tab))
        await pilot.pause()
        assert tabs.tab_count == 2
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-3"

        await tabs.remove_tab("tab-does-not-exist")
        await pilot.pause()
        assert tabs.tab_count == 2
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-3"

        await tabs.remove_tab(None)
        await pilot.pause()
        assert tabs.tab_count == 2
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-3"

        await tabs.remove_tab("tab-3")
        await tabs.remove_tab("tab-4")
        assert tabs.tab_count == 0
        assert tabs.active_tab is None


async def test_clear_tabs():
    """It should be possible to clear all tabs."""

    class TabsApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Tabs("John", "Aeryn", "Moya", "Pilot")

    async with TabsApp().run_test() as pilot:
        tabs = pilot.app.query_one(Tabs)
        assert tabs.tab_count == 4
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-1"
        await tabs.clear()
        assert tabs.tab_count == 0
        assert tabs.active_tab is None


async def test_change_active_from_code():
    """It should be possible to change the active tab from code.."""

    class TabsApp(App[None]):
        def compose(self) -> ComposeResult:
            yield Tabs("John", "Aeryn", "Moya", "Pilot")

    async with TabsApp().run_test() as pilot:
        tabs = pilot.app.query_one(Tabs)
        assert tabs.tab_count == 4
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-1"
        assert tabs.active == tabs.active_tab.id

        tabs.active = "tab-2"
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-2"
        assert tabs.active == tabs.active_tab.id

        # TODO: This one is questionable. It seems Tabs has been designed so
        # that you can set the active tab to an empty string, and it remains
        # so, and just removes the underline; no other changes. So active
        # will be an empty string while active_tab will be a tab. This feels
        # like an oversight. Need to investigate and possibly modify this
        # behaviour unless there's a good reason for this.
        tabs.active = ""
        assert tabs.active_tab is not None
        assert tabs.active_tab.id == "tab-2"
