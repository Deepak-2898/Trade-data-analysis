# Trade Analysis Project

This project automates the process of analyzing trade data, including imports and exports, and visualizing key insights. It is designed to be a complete data engineering pipeline that is reusable and efficient.

## Project Structure

```
├── data
│   ├── Export_Data.csv             # Raw export data
│   ├── Import_Data.csv             # Raw import data
│   ├── combined_trade_data.csv     # Cleaned and combined dataset
├── output
│   ├── top_export_destinations.png # Visualization of top export destinations
├── trade_pipeline.py               # Main pipeline script
├── README.md                       # Project documentation
```

## Features

1. **Data Ingestion**: Reads raw import and export datasets.
2. **Data Cleaning**: Handles missing values and standardizes columns.
3. **Data Integration**: Merges datasets to create a unified view.
4. **Database Storage**: Stores cleaned data in a SQLite database.
5. **Visualization**: Generates plots for insights.

## How to Use

1. **Setup Environment**:
   - Ensure Python 3.7+ is installed.
   - Install dependencies:
     ```bash
     pip install pandas sqlalchemy matplotlib
     ```

2. **Place Data**:
   - Save the raw data files (`Export_Data.csv` and `Import_Data.csv`) in the `data/` folder.

3. **Run the Pipeline**:
   - Execute the script:
     ```bash
     python trade_pipeline.py
     ```

4. **View Outputs**:
   - Cleaned data: `data/combined_trade_data.csv`
   - SQLite database: `data/trade_analysis.db`
   - Visualization: `output/top_export_destinations.png`

## Customization

- **Database Backend**: Modify the database engine in `trade_pipeline.py` to use PostgreSQL or MySQL.
- **Additional Analysis**: Extend the script to analyze other metrics (e.g., commodity trends).

## Next Steps

- Automate using a workflow orchestrator (e.g., Prefect or Airflow).
- Push to GitHub.

## Contributing

Feel free to fork this project and submit pull requests to improve its functionality or expand features.
