import pandas
import pandas as pd
from highcharts_core import highcharts
from highcharts_core.chart import Chart
from highcharts_core.options import HighchartsOptions
from highcharts_core.options.series.area import LineSeries, StreamGraphSeries
from highcharts_core.options.series.bar import BarSeries
from highcharts_core.options.series.scatter import ScatterSeries
from highcharts_core.options.series.spline import SplineSeries

df = pd.DataFrame()
df = pandas.read_csv("./TechSpider/gpu-data.csv", parse_dates=True)
df = df.dropna(subset=['shading_units'])
template_options = HighchartsOptions.from_js_literal(
    'template.js'
)
my_chart = Chart.from_options(template_options,
                              chart_kwargs={
                                  'container': 'chart',
                                  'variable_name': 'myChart'
                              })

my_chart.add_series(BarSeries.from_pandas(df,
                                             property_map={
                                                 'x': 'release_date',
                                                 'y': 'shading_units',
                                                 'id': 'card_name'
                                             },
                                             series_kwargs={
                                                 "turboThreshold": 0
                                             }
                                             ))

as_js_literal = my_chart.to_js_literal()

with open('my_target_file.js', 'w') as file:
    file.write(as_js_literal)
