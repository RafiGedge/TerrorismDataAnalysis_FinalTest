from sqlalchemy import func, extract, desc
from database import session_maker, Event, Gname, Region, Targtype


def track_group_activity_over_time():
    with session_maker() as session:
        # Query to get the count of unique regions each group has been active in by year
        results = session.query(
            Gname.name.label('group_name'),
            extract('year', Event.date).label('year'),
            func.count(func.distinct(Event.region_id)).label('unique_regions')
        ).join(Gname.events).group_by(Gname.name, extract('year', Event.date)).order_by(Gname.name, extract('year',
                                                                                                            Event.date)).all()

    # Process the results to find groups that expanded to new regions over the years
    group_activity = {}
    for result in results:
        group_name = result.group_name
        year = result.year
        unique_regions = result.unique_regions

        if group_name not in group_activity:
            group_activity[group_name] = {}

        group_activity[group_name][year] = unique_regions

    # Find groups that expanded to new regions
    expanding_groups = {}
    for group_name, years in group_activity.items():
        previous_regions = 0
        for year in sorted(years):
            if years[year] > previous_regions:
                if group_name not in expanding_groups:
                    expanding_groups[group_name] = []
                expanding_groups[group_name].append(year)
            previous_regions = years[year]

    # Print the results
    for group_name, years in expanding_groups.items():
        print(f"Group '{group_name}' expanded to new regions in years: {years}")


# track_group_activity_over_time()


# Question 15
def find_top_target_types_per_group(group_name=None):
    with session_maker() as session:
        query = session.query(
            Gname.name.label('group_name'),
            Targtype.name.label('target_type'),
            func.count(Event.id).label('attack_count')) \
            .join(Event, Event.gname_id == Gname.id) \
            .join(Targtype, Event.targettype_id == Targtype.id) \
            .filter(Gname.name != 'Unknown')

        if group_name:
            query = query.filter(Gname.name == group_name)

        results = query \
            .group_by(Gname.name, Targtype.name) \
            .order_by(Gname.name, desc('attack_count')).all()

    group_targets = {}
    for result in results:

        if result.group_name not in group_targets:
            group_targets[result.group_name] = {}
        group_targets[result.group_name][result.target_type] = result.attack_count

    print(group_targets)


# find_top_target_types_per_group()
