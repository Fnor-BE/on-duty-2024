# On Duty 2024

This project aims to study the presence of workers in several workshops. While the worksheets provided is full of data, it not formatted in a computer-friendly way, which rends its exploitation difficult.

This project will thus consist of two parts:
1. An **ETL** (Extract, Transform, Load): transforming the data into a form that's easily processable.
2. A **data visualization** part to explore this data.

## Objective
The objective of this project is to study the presence of workers through the workshops, and count their use of sick days and time-off days. This data should be able to be aggregated by month and by workshop.

The project should answer these questions:
- How many sick days were taken?
- How many days-off did people take?
- How do workshops compare to each other in presence rate of their workers?

A problem to be solved is that sick leaves and time-off are encoded, from first day to last day, across weekends and holidays. The later days should be not be counted and need to be processed out. More advanced case like part-time workers should also be handled.

In addition, as a personal interest I will also study how these sick/off days are taken across the week and year, to answer these questions:
- Are sick and off-days more easily taken closer to the weekend?
- Are they more easily taken close to a holiday?

## Source data
The project has two source files:

 - `data/on-duty-2024.xslx`: an excel file containing the presence data, spread into 12 sheets repesenting each month.
    - The file contains the worker information, followed by their presence data for each day (accounted for both am and pm), encoded in the form of keywords explained at the top of each sheet, and followed by crude calculations.
    - The file also contains a reference sheet displaying most workers and their expected retirement date.
- `data/holidays.csv`: a list of holidays the workshops aren't working.

It is to be noted that the workshops also don't work over the weekends.

While the source file may initially appear well-made, it becomes quickly apparent that it has severe flaws:
- Some of the rows use lookups to find worker names based on their ID, but others don't. It seems a person with some excel knowledge set the file up using lookups, but the person later maintaining it didn't know how to use them and entered raw data.
- Weekends and holidays are manually handled: cells are greyed and kept mostly empty, but there is no programmatic way to handle them. It will have to be remedied to correctly count sick and time-off days.
- Most of the conditional formatting is done by hand.

This project aims to fix all this issues.

## Technologies
Python
