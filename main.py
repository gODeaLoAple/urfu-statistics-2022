import json

from correlation import Correlation
from correlation_options import CorrelationOptions
from intervals_range import IntervalsRange
from report_builder import ReportBuilder, NormReportOptions
from statistics_calculator import StatisticsCalculator
from table_builder import TableBuilder
from variance_collection import VarianceCollection


def report(collection, stat, name, options):
    builder = ReportBuilder(collection, stat, name, options)
    builder.print_table()
    builder.create_hist()
    builder.print_stat()
    builder.report_norm()


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

    x_stat = StatisticsCalculator(x_intervals).calculate()
    #report(x_intervals, x_stat, "X", NormReportOptions(alpha, data.get("xi_expected_x", None), data.get("q_x", None)))

    y_stat = StatisticsCalculator(y_intervals).calculate()
    #report(y_intervals, y_stat, "Y", NormReportOptions(alpha, data.get("xi_expected_y", None), data.get("q_y", None)))

    correlation = Correlation(table, x_stat, y_stat, CorrelationOptions(alpha, data.get("critical_t", None)))
    rxy = correlation.coefficient()
    correlation.regression_lines()
    print(correlation.significance())


main()


