import pandas as pd
from datetime import datetime as dt, timedelta

class CsvMerger:
    def __init__(self, antara_dir='../../hasil_scrapping_antara', serambi_dir='../../hasil_scrapping_serambi', output_dir='../data'):
        self.antara_dir = antara_dir
        self.serambi_dir = serambi_dir
        self.output_dir = output_dir

    def merge_csv(self, start_date, end_date):
        # Format tanggal untuk file paths
        start_date_str = start_date.strftime("%Y%m%d")
        end_date_str = end_date.strftime("%Y%m%d")

        # Paths to input files
        antara_file = f'{self.antara_dir}/Antara_{start_date_str}_to_{end_date_str}.csv'
        serambi_file = f'{self.serambi_dir}/Serambi_{start_date_str}_to_{end_date_str}.csv'

        try:
            # Read the CSV files
            df1 = pd.read_csv(antara_file)
            df2 = pd.read_csv(serambi_file)
            
            # Concatenate the DataFrames
            merged_df = pd.concat([df1, df2])

            # Output file path
            output_file = f'{self.output_dir}/Merged_{start_date_str}_to_{end_date_str}.csv'
            
            # Save the merged DataFrame to CSV
            merged_df.to_csv(output_file, index=False)

            print(f"Files merged and saved to {output_file}")

        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# Usage example
# if __name__ == "__main__":
#     # Example usage
#     merger = CsvMerger()
#     yesterday = dt.now() - timedelta(days=1)
#     start_date = yesterday
#     end_date = yesterday
#     merger.merge_csv(start_date, end_date)
