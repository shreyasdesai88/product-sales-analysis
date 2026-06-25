"""
Quick Demo - Show flexible system with IPL Teams
"""

from generic_data_loader import GenericDataLoader
from flexible_analytics_engine import FlexibleAnalyticsEngine


print("\n" + "="*80)
print("🏏 IPL TEAMS COMPARISON - FLEXIBLE SYSTEM DEMO")
print("="*80)

# Load IPL data
print("\n📥 Loading IPL dataset...")
loader = GenericDataLoader('ipl_dataset_10000.csv')

# Show what was auto-detected
print("\n✓ Auto-Detected Structure:")
print(f"  Entity Column: {loader.entity_column}")
print(f"  Teams: {', '.join(loader.get_all_entities())}")
print(f"  Metrics: {', '.join(loader.numeric_columns)}")
print(f"  Categories: {', '.join(loader.categorical_columns)}")
print(f"  Date Range: {loader.get_date_range()['min_date'].date()} to {loader.get_date_range()['max_date'].date()}")

# Initialize analytics
print("\n🔧 Initializing analytics engine...")
analytics = FlexibleAnalyticsEngine(loader)

# Get teams
teams = loader.get_all_entities()
team1, team2 = teams[0], teams[1]

print(f"\n⚡ Comparing: {team1} vs {team2}")
print("="*80)

# Get comparison
comparison = analytics.compare_entities(team1, team2)

# Print formatted results
print(f"\n📊 MATCH STATISTICS:")
print(f"\n{team1}:")
print(f"  Total Matches: {comparison['records'][team1]}")
print(f"  Total Runs: {comparison['metrics']['runs_scored'][team1]['sum']:,.0f}")
print(f"  Average Runs: {comparison['metrics']['runs_scored'][team1]['mean']:,.0f}")
print(f"  Wickets Lost: {comparison['metrics']['wickets_lost'][team1]['sum']:,.0f}")
print(f"  Average Wickets Lost: {comparison['metrics']['wickets_lost'][team1]['mean']:,.0f}")

print(f"\n{team2}:")
print(f"  Total Matches: {comparison['records'][team2]}")
print(f"  Total Runs: {comparison['metrics']['runs_scored'][team2]['sum']:,.0f}")
print(f"  Average Runs: {comparison['metrics']['runs_scored'][team2]['mean']:,.0f}")
print(f"  Wickets Lost: {comparison['metrics']['wickets_lost'][team2]['sum']:,.0f}")
print(f"  Average Wickets Lost: {comparison['metrics']['wickets_lost'][team2]['mean']:,.0f}")

# Show differences
print(f"\n📈 DIFFERENCES:")
print(f"  Run Difference: {comparison['metrics']['runs_scored']['difference']:,.0f} runs")
print(f"  Wickets Difference: {comparison['metrics']['wickets_lost']['difference']:,.0f} wickets")

# Show categorical data
print(f"\n🎯 CATEGORICAL ANALYSIS:")
if 'result' in comparison['categorical']:
    results = comparison['categorical']['result']
    print(f"\n  {team1} Results:")
    for result, count in results[team1].items():
        print(f"    • {result}: {count}")
    print(f"\n  {team2} Results:")
    for result, count in results[team2].items():
        print(f"    • {result}: {count}")

# Generate insights
print(f"\n💡 KEY INSIGHTS:")
insights = analytics.generate_insights(team1, team2)
if insights:
    for insight in insights:
        print(f"  ✓ {insight}")
else:
    print("  (No significant differences detected)")

# Show player of match
print(f"\n⭐ PLAYER OF THE MATCH AWARDS:")
if 'player_of_match' in comparison['categorical']:
    players = comparison['categorical']['player_of_match']
    print(f"\n  {team1}:")
    top_players_1 = sorted(players[team1].items(), key=lambda x: x[1], reverse=True)[:3]
    for player, count in top_players_1:
        print(f"    • {player}: {count} awards")
    print(f"\n  {team2}:")
    top_players_2 = sorted(players[team2].items(), key=lambda x: x[1], reverse=True)[:3]
    for player, count in top_players_2:
        print(f"    • {player}: {count} awards")

# Venues
print(f"\n🏟️  VENUES:")
if 'venue' in comparison['categorical']:
    venues = comparison['categorical']['venue']
    print(f"\n  {team1}:")
    for venue, count in venues[team1].items():
        print(f"    • {venue}: {count} matches")
    print(f"\n  {team2}:")
    for venue, count in venues[team2].items():
        print(f"    • {venue}: {count} matches")

print("\n" + "="*80)
print("✓ ANALYSIS COMPLETE")
print("="*80)

print("\n📊 To visualize this data:")
print("  1. Run: streamlit run dynamic_dashboard.py")
print("  2. Select 'ipl_dataset_10000.csv' from dropdown")
print("  3. Compare teams in interactive dashboard")

print("\n🔄 To use with your own dataset:")
print("  1. Place CSV file in project directory")
print("  2. Run: streamlit run dynamic_dashboard.py")
print("  3. Select your dataset - it works automatically!")

print("\n" + "="*80)
