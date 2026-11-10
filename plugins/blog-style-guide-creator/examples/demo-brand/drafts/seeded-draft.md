---
title: Build your first team dashboard
content_type: how-to
---

# Build your first team dashboard

In today’s fast-paced world, data teams are asked to deliver more with less. Dashboards are how most companies leverage their data — and AcmeBoard makes building one seamless.

AcmeBoard unlocks powerful insights for every team. A recent survey found that most data leads lose a full day each week to reporting.

In our own usage data, 4k workspaces built a dashboard in their first week and 72% of them still used it a month later. Teams with one shared dashboard settle questions faster then teams that pass spreadsheets around.

## Before You Start

- **Data:** A table or CSV with at least 3 columns your team cares about.
- **Access.** An Acmeboard workspace where you can create dashboards.
- **Time.** About an hour.

## Steps.

1. Connect your data source. AcmeBoard reads from PostgreSQL, spreadsheets, and CSV files.
2. Choose the 3 numbers your team checks every Monday. These become your tiles.
3. Utilize the layout grid to put the most important number top left.
4. A filter for each team member, so each person sees their own work.
5. Share the dashboard in your team channel at 9am on a Monday.
6. Schedule a refresh. The 2nd refresh each day catches late data from the ETL job.

```sql
-- 3 tiles — one per region
select region, sum(revenue) from sales group by region;
```

## Pick numbers people already argue about

The best first tile is a number your team already debates in meetings. As one analyst told us, "if nobody argues about it, nobody will open it". Put the the revenue tile first and the rest below it.

> We rebuilt it in 3 days — and it stuck.

Dana Whitfield, who runs analytics at a 40-person startup, starts every dashboard with revenue. Whitfeld says the second tile is whatever the team asked about last week.

12 people opened our pilot dashboard in its first week. Acme Analytics put $2.5M into faster refreshes this year, and refreshes have been free on every plan since March 3rd.

## Keep it small

You will recieve a weekly email showing who opened the dashboard. If the count drops, ask why before adding tiles. For the full routine, [click here](https://acme.example/blog/retire-a-dashboard?utm_source=newsletter).
