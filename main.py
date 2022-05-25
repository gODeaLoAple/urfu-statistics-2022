from one_dimensional_table import OneDimensionalTable
from report_builder import ReportBuilder, NormReportOptions
from table_builder import TableBuilder
from intervals import Intervals


def report(variances, intervals, name, options):
    frequencies = OneDimensionalTable(intervals).create_discrete_table(variances)
    builder = ReportBuilder(variances, frequencies, intervals, name, options)
    builder.print_table()
    builder.create_hist()
    builder.print_stat()
    builder.report_norm()


def main():
    pairs = [
        (50, 411),
        (57, 491),
        (61, 508),
        (58, 491),
        (51, 454),
        (70, 552),
        (43, 377),
        (71, 567),
        (64, 496),
        (67, 580),
        (63, 502),
        (58, 458),
        (60, 516),
        (47, 374),
        (54, 405),
        (60, 485),
        (67, 554),
        (58, 512),
        (68, 610),
        (56, 421),
        (74, 613),
        (72, 578),
        (59, 524),
        (60, 511),
        (52, 422),
        (47, 367),
        (57, 507),
        (57, 449),
        (67, 567),
        (45, 381),
        (62, 507),
        (56, 478),
        (51, 444),
        (66, 529),
        (51, 427),
        (54, 404),
        (53, 450),
        (41, 358),
        (65, 530),
        (54, 404),
        (52, 417),
        (59, 486),
        (55, 437),
        (70, 572),
        (62, 500),
        (58, 464),
        (46, 373),
        (50, 423),
        (63, 539),
        (64, 554),
        (47, 413),
        (59, 450),
        (76, 620),
        (60, 531),
        (61, 511),
        (65, 551),
        (66, 518),
        (60, 483),
        (63, 506),
        (45, 392),
        (62, 494),
        (54, 445),
        (67, 566),
        (48, 391),
        (60, 456),
        (55, 416),
        (62, 513),
        (57, 510),
        (49, 406),
        (63, 476),
        (72, 602),
        (64, 538),
        (53, 467),
        (65, 507),
        (45, 362),
        (61, 513),
        (45, 384),
        (57, 488),
        (43, 358),
        (74, 601),
        (57, 511),
        (54, 425),
        (57, 506),
        (65, 652),
        (79, 485),
        (56, 508),
        (66, 557),
        (67, 500),
    ]
    x_variances, y_variances = list(map(list, map(sorted, zip(*pairs))))
    x_intervals, y_intervals = Intervals(38, max(x_variances), 7), Intervals(333, max(y_variances), 50)

    table = TableBuilder(x_intervals, y_intervals).build(pairs)
    table.draw()

    report(x_variances, x_intervals, "X", NormReportOptions(0.05, 6, 1.67))

    report(y_variances, y_intervals, "Y", NormReportOptions(0.05, 7.8, 1.67))


main()
