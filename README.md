# NYC Traffic Crashes Dashboard

## Project Overview

This project is a comprehensive data analytics dashboard for analyzing traffic crash data in New York City. The dashboard provides interactive visualizations and filtering capabilities to explore patterns, trends, and insights from NYC traffic collision records.

## Features

### Interactive Dashboard
- Real-time data filtering and visualization
- Dynamic chart updates based on user selections
- Responsive design with dark theme interface
- Search functionality across multiple data columns
- CSV data export capability

### Data Filtering Options
- **Borough Selection**: Filter crashes by NYC borough
- **Contributing Factor**: Analyze crashes by primary contributing factors
- **Demographic Filter**: Filter by most common gender involved
- **Year Slider**: Select data from 2009 to 2023
- **Search Bar**: Free-text search across multiple columns

### Visualizations

The dashboard includes five primary visualization types:

1. **Bar Chart**: Total injuries aggregated by borough
2. **Pie Chart**: Top 10 contributing factors to crashes
3. **Line Chart**: Temporal trends showing crash patterns over time (daily, monthly, or yearly)
4. **Heatmap**: Correlation analysis or time-based crash frequency patterns
5. **Geographic Map**: Interactive scatter map showing crash locations with up to 2000 sampled points

### Summary Statistics

Four key metrics displayed at the top of the dashboard:
- Total Crashes
- Total Injuries
- Total Fatalities
- Average Persons Involved per crash

## Technical Stack

### Core Technologies
- **Python 3.x**
- **Dash**: Web application framework
- **Plotly**: Interactive visualization library
- **Pandas**: Data manipulation and analysis
- **Dash Bootstrap Components**: UI components and styling

### Key Libraries
```python
dash
dash-bootstrap-components
plotly
pandas
```

## Project Structure
```
Visuals/
│
├── app.py                      # Main dashboard application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── components/
│   ├── __init__.py
│   ├── DataLoader.py          # Data loading and filtering functions
│   └── charts.py              # Visualization creation functions
│
├── assets/
│   └── styles.css             # Custom CSS styling
│
├── data/
│   ├── raw/                   # Raw data files
│   └── processed/             # Cleaned data files
│
└── notebooks/
    └── data_cleaning.ipynb    # Data preprocessing notebooks
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Visuals.git
cd Visuals
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure your data file is placed in the `data/processed/` directory and update the path in `components/DataLoader.py`

## Usage

### Running the Dashboard

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8050
```

### Dashboard Controls

**Filters Section**:
- Use dropdown menus to select borough, contributing factor, and demographic filters
- Adjust the year slider to focus on specific time periods
- Enter search terms in the search bar for custom filtering

**Action Buttons**:
- **Generate Report**: Apply selected filters and update all visualizations
- **Reset**: Clear all filters and return to default view
- **Download Data**: Export filtered dataset as CSV file

**Interactive Features**:
- Hover over charts for detailed information
- Click and drag on maps to pan
- Zoom in/out on geographic visualizations

## Data Processing

### Data Cleaning
The project includes comprehensive data cleaning procedures:
- Handling missing values
- Standardizing column names
- Converting data types
- Aggregating person-level data to crash-level
- Creating derived columns for analysis
- Removing duplicates and invalid records

### Filter Logic
- Multiple filters work with AND logic (all conditions must be met)
- Search functionality uses OR logic across columns
- Empty/null values are handled gracefully
- Case-insensitive search implementation

## Chart Functions

### create_bar(df)
Creates a bar chart showing total injuries by borough.

**Parameters:**
- `df`: Pandas DataFrame with crash data

**Returns:**
- Plotly figure object or empty figure if no data

### create_pie(df)
Generates a pie chart of the top 10 contributing factors.

**Parameters:**
- `df`: Pandas DataFrame with crash data

**Returns:**
- Plotly figure object or empty figure if no data

### create_line(df)
Produces a time-series line chart with automatic granularity detection:
- Daily view for data spanning less than 1 month
- Monthly view for data spanning less than 1 year
- Yearly view for multi-year datasets

**Parameters:**
- `df`: Pandas DataFrame with crash data

**Returns:**
- Plotly figure object or empty figure if no date data

### create_heatmap(df)
Creates a heatmap visualization showing either:
- Crash frequency by hour and borough (if time data available)
- Correlation matrix of numeric variables (fallback)

**Parameters:**
- `df`: Pandas DataFrame with crash data

**Returns:**
- Plotly figure object or empty figure if insufficient data

### create_map(df)
Displays an interactive geographic scatter map of crash locations using OpenStreetMap.

**Parameters:**
- `df`: Pandas DataFrame with crash data including LATITUDE and LONGITUDE

**Returns:**
- Plotly figure object or empty figure if no location data

### get_stats(df)
Calculates summary statistics for the filtered dataset.

**Parameters:**
- `df`: Pandas DataFrame with crash data

**Returns:**
- Tuple of formatted strings: (crashes, injuries, fatalities, avg_people)

## Research Questions Addressed

The dashboard visualizations are designed to support analysis of complex research questions including:

1. **Spatial Correlation**: Examining the relationship between crash density per borough and average injury severity
2. **Temporal Analysis**: Tracking how primary contributing factors for fatal crashes have shifted over five years (2020-2025)
3. **Vulnerable Populations**: Analyzing disproportionate involvement of specific vehicle types in pedestrian crashes during peak hours
4. **Time-of-Day Impact**: Identifying combinations of time and location that lead to highest injury rates
5. **Vehicle Type Risk**: Calculating injury risk rates for top vehicle types across boroughs
6. **Fatality Trends**: Computing compound annual growth rate (CAGR) for fatalities by contributing factor
7. **Demographic Impact**: Analyzing injury severity trends based on gender demographics
8. **Hotspot Identification**: Detecting high-frequency crash clusters associated with specific contributing factors
9. **Seasonality Analysis**: Time series decomposition showing weekly or monthly patterns in crash rates
10. **Factor-Person Correlation**: Examining relationships between contributing factors and injury severity for different person types

## Deployment

The application is configured for deployment with:
- Environment-based port configuration
- Production-ready server setup
- Host binding for external access

Default deployment configuration:
```python
port = int(os.environ.get("PORT", 8050))
app.run_server(host="0.0.0.0", port=port, debug=False)
```

### Deploying to Heroku

1. Create a `Procfile`:
```
web: gunicorn app:server
```

2. Add gunicorn to requirements.txt:
```bash
echo "gunicorn" >> requirements.txt
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Customization

### Styling
- Modify `assets/styles.css` for custom styling
- Dashboard uses DARKLY Bootstrap theme
- All charts use transparent backgrounds with light text for dark mode

### Adding New Visualizations
1. Create chart function in `components/charts.py`
2. Add Output in app.py callback
3. Include dcc.Graph component in layout
4. Return chart from update_dashboard callback

### Extending Filters
1. Add dropdown in layout using make_dropdown helper
2. Include new State parameter in callback
3. Update filter_dataframe function in `components/DataLoader.py`

## Performance Considerations

- Map visualization limited to 2000 points for performance optimization
- Efficient pandas operations for filtering large datasets
- Lazy loading of visualizations
- Debounced search input to reduce unnecessary updates
- Caching mechanisms for frequently accessed data

## Known Limitations

- Geographic visualization requires LATITUDE and LONGITUDE columns
- Time-series analysis depends on date column availability
- Some visualizations may show empty state if filtered dataset is too small
- Search functionality limited to predefined column list
- Maximum 2000 points displayed on map for performance reasons

## Data Requirements

### Required Columns
- `BOROUGH`: NYC borough name
- `CRASH DATE` or `CRASH_DATE`: Date of crash
- `CRASH_YEAR`: Year of crash
- `NUMBER OF PERSONS INJURED`: Count of injured persons
- `NUMBER OF PEDESTRIANS KILLED`: Pedestrian fatalities
- `NUMBER OF CYCLIST KILLED`: Cyclist fatalities
- `NUMBER OF MOTORIST KILLED`: Motorist fatalities
- `CONTRIBUTING FACTOR VEHICLE 1`: Primary contributing factor
- `VEHICLE TYPE CODE 1`: Primary vehicle type
- `LATITUDE`: Geographic latitude
- `LONGITUDE`: Geographic longitude
- `MOST_COMMON_SEX`: Demographic information
- `PERSONS_INVOLVED_COUNT`: Total persons involved

## Future Enhancements

Potential improvements for future versions:
- Additional chart types (box plots, scatter plots, grouped bars, stacked bars)
- Advanced statistical analysis features
- Clustering algorithms for hotspot detection
- Machine learning predictions for crash risk
- Multi-page dashboard with dedicated analysis sections
- User authentication and saved filter presets
- Real-time data updates via API integration
- Export functionality for charts and reports
- Mobile-responsive design improvements
- Advanced search with regular expressions

## Troubleshooting

### Common Issues

**Dashboard won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that port 8050 is not already in use
- Verify data file path in DataLoader.py

**Charts not displaying:**
- Check browser console for JavaScript errors
- Ensure data file is properly formatted
- Verify required columns exist in dataset

**Slow performance:**
- Reduce dataset size for testing
- Check map point limit (default 2000)
- Ensure sufficient system memory

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes with clear commit messages
4. Test thoroughly
5. Update documentation as needed
6. Submit a pull request with description of changes

### Code Style
- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Include docstrings for all functions
- Comment complex logic

## License

This project is provided for educational and analytical purposes. Please check the repository for specific license information.

## Contact

For questions, issues, or suggestions, please open an issue in the repository.

## Acknowledgments

- Data source: NYC Open Data Portal
- Built with Dash by Plotly
- Bootstrap components for UI design
- OpenStreetMap for geographic visualizations

## Version History

- **v1.0.0** - Initial release with core dashboard functionality
- Basic filtering and visualization capabilities
- Five primary chart types
- CSV export functionality

---

**Last Updated:** November 2025
