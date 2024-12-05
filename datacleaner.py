import os
from datetime import datetime
import json

def extract_year(date_str, debug=False):
    if debug:
        print(f"Attempting to extract year from: {date_str}")
    try:
        date = datetime.strptime(date_str.strip(), '%b %d, %Y')
        if debug:
            print(f"Successfully extracted year: {date.year}")
        return date.year
    except ValueError as e:
        if debug:
            print(f"Failed to parse date: {date_str}. Error: {e}")
        return None

def count_posts_by_year(filepath, debug=False):
    if debug:
        print(f"\nProcessing file: {filepath}")
    year_counts = {}
    
    try:
        with open(filepath, 'r') as f:
            line_count = 0
            valid_dates = 0
            for line in f:
                line_count += 1
                if '|' in line:  # Skip any header/footer lines without dates
                    date_str = line.split('|')[1].strip()
                    year = extract_year(date_str, debug)
                    if year:
                        year_counts[year] = year_counts.get(year, 0) + 1
                        valid_dates += 1
                else:
                    year = extract_year(line.strip(), debug)
                    if year:
                        year_counts[year] = year_counts.get(year, 0) + 1
                        valid_dates += 1
            
            if debug:
                print(f"Processed {line_count} lines, found {valid_dates} valid dates")
                print(f"Year distribution: {year_counts}")
            
    except Exception as e:
        if debug:
            print(f"Error processing file {filepath}: {e}")
        
    return year_counts

def process_data_folder(debug=False):
    if debug:
        print("\n=== Starting data processing ===")
    # Create dictionary to store results
    results = {}
    
    # Process each category folder
    data_path = 'data'
    if debug:
        print(f"Looking for category folders in: {data_path}")
    
    # Get all folders that end with 'Keywords'
    category_folders = [f for f in os.listdir(data_path) 
                       if os.path.isdir(os.path.join(data_path, f)) 
                       and f.endswith('Keywords')]
    
    if not category_folders:
        if debug:
            print(f"Warning: No category folders found in {data_path}")
        return results
        
    if debug:
        print(f"Found categories: {category_folders}")
    
    for category_folder in category_folders:
        if debug:
            print(f"\nProcessing category: {category_folder}")
        # Extract category name without "Keywords" suffix
        category_type = category_folder.replace('Keywords', '')
        results[category_type] = {}
        
        folder_path = os.path.join(data_path, category_folder)
        
        # Get all files in category folder
        files = [f for f in os.listdir(folder_path) if not f.startswith('.')]
        if debug:
            print(f"Found {len(files)} files in {category_folder}")
        
        # Process each file
        for filename in files:
            if debug:
                print(f"\nProcessing keyword file: {filename}")
            filepath = os.path.join(folder_path, filename)
            # Use filename without extension as keyword name
            keyword = os.path.splitext(filename)[0]
            year_counts = count_posts_by_year(filepath, debug)
            results[category_type][keyword] = year_counts
            if debug:
                print(f"Completed processing {keyword}: {len(year_counts)} years found")
    
    # Create cleanedData directory if it doesn't exist
    if debug:
        print("\nSaving results...")
    os.makedirs('cleanedData', exist_ok=True)
    
    # Save results to JSON file
    output_path = 'cleanedData/post_counts.json'
    try:
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        if debug:
            print(f"Successfully saved results to {output_path}")
            print(f"Final results structure: {json.dumps(results, indent=2)}")
    except Exception as e:
        if debug:
            print(f"Error saving results: {e}")

    if debug:
        print("\n=== Data processing complete ===")

if __name__ == '__main__':
    process_data_folder(debug=False)

