import json
import math

from correlation import Correlation
from intervals_range import IntervalsRange
from report_builder import ReportBuilder, NormReportOptions
from table_builder import TableBuilder
from variance_collection import VarianceCollection


def report(intervals, name, options):
    builder = ReportBuilder(intervals, name, options)
    builder.print_table()
    builder.create_hist()
    builder.print_stat()
    builder.report_norm()
    return builder.stat


def main():
    with open("data.json", "r", encoding="utf8") as f:
        data = json.load(f)
    pairs = data["pairs"]
    n = len(pairs)
    x_variances, y_variances = list(map(list, map(sorted, zip(*pairs))))
    x_intervals = VarianceCollection(x_variances, IntervalsRange(data["start_x"], max(x_variances), data["step_x"]))
    y_intervals = VarianceCollection(y_variances, IntervalsRange(data["start_y"], max(y_variances), data["step_y"]))

    table = TableBuilder(x_intervals, y_intervals).build(pairs)
    table.draw()

    alpha = data["alpha"]
    x_stat = report(x_intervals, "X", NormReportOptions(alpha, data["xi_expected_x"], data["q_x"]))
    y_stat = report(y_intervals, "Y", NormReportOptions(alpha, data["xi_expected_y"], data["q_y"]))

    correlation = Correlation(table, x_stat, y_stat)
    rxy = correlation.coefficient()
    T = rxy * math.sqrt((n - 2) / (1 - rxy ** 2))


main()

