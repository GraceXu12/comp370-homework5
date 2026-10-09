import pandas as pd
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure, curdoc

# Load data
df = pd.read_csv("preprocessed_311_monthly.csv")
df["Incident Zip"] = df["Incident Zip"].astype(str).str.strip()

zips = sorted(z for z in df["Incident Zip"].unique() if z != "ALL")
zip1 = zips[0]
zip2 = zips[1] if len(zips) > 1 else zip1

months = list(range(1, 13))

# get monthly averages given zipcode
def get_monthly_averages(zipcode):
    subset = df[df["Incident Zip"] == zipcode]
    month_data = dict(zip(subset["closed_month"],
                          subset["response_time_hours"]))
    return [month_data.get(m, None) for m in months]

# create data source
source = ColumnDataSource(
    data={
    "month": months,
    "all": get_monthly_averages("ALL"),
    "zip1": get_monthly_averages(zip1),
    "zip2": get_monthly_averages(zip2)})


p = figure(
    title="Monthly Average 311 Response Time in 2020",
    x_axis_label="Month",
    y_axis_label="Average Response Time (Hours)",
    width=800,
    height=450)

p.line("month", "all", source=source, legend_label="All Zipcodes", line_width=3, color="black")
p.line("month", "zip1", source=source, legend_label=f"Zipcode {zip1}", line_width=2, color="blue")
p.line("month", "zip2", source=source, legend_label=f"Zipcode {zip2}", line_width=2, color="orange")

p.xaxis.ticker = months
p.legend.location = "top_left"

# dropdowns
select1 = Select(title="Select Zipcode 1", value=zip1, options=zips)
select2 = Select(title="Select Zipcode 2", value=zip2, options=zips)

# update plot when change in dropdown 
def update(attr, old, new):
    source.data = {
        "month": months,
        "all": get_monthly_averages("ALL"),
        "zip1": get_monthly_averages(select1.value),
        "zip2": get_monthly_averages(select2.value)}

    p.legend.items[1].label = {"value": f"Zipcode {select1.value}"}
    p.legend.items[2].label = {"value": f"Zipcode {select2.value}"}

select1.on_change("value", update)
select2.on_change("value", update)

# display dashboard
curdoc().add_root(column(select1, select2, p))
curdoc().title = "311 Response Time Dashboard"
