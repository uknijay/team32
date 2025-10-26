import math
import flet as ft

if not hasattr(ft, "Colors"):
    ft.Colors = ft.colors

def to_xy(pairs):
    xs, ys = [], []
    for m, g in sorted(pairs, key=lambda t: t[1]):
        xs.append(float(g))
        ys.append(float(m))
    return xs, ys

def lttb(pairs, threshold):
    n = len(pairs)
    if threshold >= n or threshold < 3:
        return pairs
    sampled = [pairs[0]]
    bucket_size = (n - 2) / (threshold - 2)
    a = 0
    for i in range(0, threshold - 2):
        start = int(round((i + 0) * bucket_size)) + 1
        end = int(round((i + 1) * bucket_size)) + 1
        if end >= n:
            end = n - 1
        avg_range_start = end
        avg_range_end = int(round((i + 2) * bucket_size)) + 1
        if avg_range_end >= n:
            avg_range_end = n
        avg_x = sum(p[0] for p in pairs[avg_range_start:avg_range_end]) / max(1, (avg_range_end - avg_range_start))
        avg_y = sum(p[1] for p in pairs[avg_range_start:avg_range_end]) / max(1, (avg_range_end - avg_range_start))
        max_area = -1
        max_area_point = None
        next_a = None
        for idx in range(start, end + 1):
            ax, ay = pairs[a]
            bx, by = pairs[idx]
            area = abs((ax - avg_x) * (by - ay) - (ax - bx) * (avg_y - ay)) * 0.5
            if area > max_area:
                max_area = area
                max_area_point = pairs[idx]
                next_a = idx
        sampled.append(max_area_point)
        a = next_a
    sampled.append(pairs[-1])
    return sampled

def nice_step(span, target_ticks):
    if span <= 0 or target_ticks < 2:
        return 1
    step = span / (target_ticks - 1)
    mag = 10 ** math.floor(math.log10(step))
    norm = step / mag
    if norm <= 1:
        nice = 1
    elif norm <= 2:
        nice = 2
    elif norm <= 5:
        nice = 5
    else:
        nice = 10
    return nice * mag

def nice_bounds(vmin, vmax, target_ticks=6):
    if vmin == vmax:
        return vmin - 1, vmax + 1, [vmin, vmax]
    step = nice_step(vmax - vmin, target_ticks)
    lo = math.floor(vmin / step) * step
    hi = math.ceil(vmax / step) * step
    ticks = []
    t = lo
    while t <= hi + 1e-9:
        ticks.append(round(t, 10))
        t += step
    return lo, hi, ticks

def nice_int_bounds(vmin, vmax, target_ticks=6):
    vmin = int(math.floor(vmin))
    vmax = int(math.ceil(vmax))
    span = max(1, vmax - vmin)
    step = max(1, math.ceil(span / (target_ticks - 1)))
    lo = (vmin // step) * step
    hi = ((vmax + step - 1) // step) * step
    ticks = list(range(lo, hi + 1, step))
    return lo, hi, ticks

def fmt_num(v):
    if abs(v - round(v)) < 1e-6:
        return str(int(round(v)))
    return f"{v:.2f}"

class MoneyLine(ft.Container):
    def __init__(self, title="Bankroll over Games", accentColor="#7C83FD", yAxisTitle="Money", max_points=2000):
        self.title = title
        self.accentColor = accentColor
        self.yAxisTitle = yAxisTitle
        self.max_points = max_points
        self._points = []
        content = self.buildChart()
        super().__init__(content=content, bgcolor=ft.Colors.GREY_900, padding=10, border_radius=12, expand=True)

    def set_data(self, pairs):
        xs, ys = to_xy(pairs)
        xy = list(zip(xs, ys))
        if len(xy) > self.max_points:
            xy = lttb(xy, self.max_points)
        self._points = [ft.LineChartDataPoint(x=p[0], y=p[1]) for p in xy]
        self.content = self.buildChart()

    def buildChart(self) -> ft.Column:
        if not self._points:
            self._points = [ft.LineChartDataPoint(x=0, y=0), ft.LineChartDataPoint(x=1, y=0)]
        xs = [p.x for p in self._points]
        ys = [p.y for p in self._points]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        y_lo, y_hi, y_ticks = nice_bounds(min_y, max_y, 7)
        x_lo, x_hi, x_ticks = nice_int_bounds(min_x, max_x, 7)
        series = ft.LineChartData(data_points=self._points, color=self.accentColor, curved=True, stroke_width=3)
        x_labels = [ft.ChartAxisLabel(value=t, label=ft.Container(ft.Text(fmt_num(t), color=ft.colors.WHITE), padding=2)) for t in x_ticks]
        y_labels = [ft.ChartAxisLabel(value=t, label=ft.Container(ft.Text(fmt_num(t), color=ft.colors.WHITE), padding=2)) for t in y_ticks]
        chart = ft.LineChart(
            data_series=[series],
            border=ft.border.all(1, ft.Colors.GREY_600),
            left_axis=ft.ChartAxis(labels=y_labels, labels_size=32, title=ft.Text(self.yAxisTitle, color=ft.colors.WHITE), title_size=16),
            bottom_axis=ft.ChartAxis(labels=x_labels, labels_size=22),
            horizontal_grid_lines=ft.ChartGridLines(color=ft.Colors.GREY_800, width=1, dash_pattern=[3, 3]),
            min_y=y_lo,
            max_y=y_hi,
            min_x=x_lo,
            max_x=x_hi,
            tooltip_bgcolor="#2E2E2E",
            interactive=True,
            expand=True,
            animate=True,
        )
        titleText = ft.Text(value=self.title, size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        return ft.Column(controls=[titleText, ft.Row([chart], expand=True)], spacing=10, expand=True)

def main(page: ft.Page):
    page.title = "Money vs Game"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.BLACK
    page.padding = 16
    money_chart = MoneyLine(max_points=2000)
    sample_pairs = [(100.0, 0), (98.0, 1), (105.0, 2), (110.0, 3), (103.0, 4), (120.0, 5)]
    money_chart.set_data(sample_pairs)
    page.add(money_chart)

if __name__ == "__main__":
    ft.app(target=main)