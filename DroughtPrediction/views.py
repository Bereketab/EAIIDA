from django.shortcuts import render
from django.http import HttpResponse
import csv
from io import TextIOWrapper
from datetime import datetime
import pandas as pd

def index(request):
    return render(request,'main/index.html')

def about(request):
    return render(request,'about.html')

def Drought(request):
    return render(request,'Drought.html')

def SPI(request):
    return render(request,'main/SPI.html')

def data_loader(request):
    # Get the uploaded CSV file from the request.FILES
    csv_file = request.FILES.get("csv")#find this variable
    df = pd.read_csv(csv_file)
    print(df.head())# this will give you  panda stuff
    file_name =request.POST['fileName']
    if request.method=="POST":
        # Check if a file is selected
        if not csv_file:
            return HttpResponse("No file selected!")
        # Ensure the file is a CSV file
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Invalid file format. Please upload a CSV file.")

        # Parse the CSV file
        try:
            if(str(file_name).split('.')[0]=="spi"):
                expected_columns = ['date', 'ndvi', 'evi', 'ndwi']
                csv_reader = csv.reader(TextIOWrapper(csv_file.file, encoding='utf-8', delimiter='\t'))
                header_row = next(csv_reader)
                # Check if the header row matches the expected columns and order
                if header_row != expected_columns:
                    return HttpResponse(f"Invalid columns. Expected: {expected_columns}, Got: {header_row}")

                # Get the index of each expected column in the header
                column_indices = {column: header_row.index(column) for column in expected_columns}

                for row_number, row in enumerate(csv_reader, start=1):
                        # Check for missing values in the 'date' column
                        if 'date' not in row or not row['date']:
                            return HttpResponse(f"Missing 'date' value in row {row_number}")

                        # Validate the 'date' column format
                        try:
                            # Assuming date format is 'YYYY-MM-DD', adjust if needed
                            datetime.strptime(row['date'], '%Y-%m-%d')
                        except ValueError:
                            return HttpResponse(f"Invalid date format in row {row_number}, 'date' value: {row['date']}")

                        # Do something with each row, for example, print it
                        print(row)

        except Exception as e:
            # Handle exceptions (e.g., CSV parsing error)
            return HttpResponse(f"Error processing CSV file: {e}")

        # Return a simple HttpResponse indicating successful loading
        return HttpResponse("CSV file loaded successfully!!")
