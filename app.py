# -*- coding: utf-8 -*-
"""
Created on Fri May 10 00:26:52 2024

@author: rishe
"""
# app.py
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Read data from Excel
    df = pd.read_excel('data.xlsx')

    # Get column names (excluding the first column which contains dates)
    columns = df.columns[1:]

    # Create a list to store chart URLs and column names together
    chart_data = []

    # Create line plots for each column
    for column in columns:
        # Process data
        labels = df.iloc[:, 0].tolist()
        values = df[column].tolist()

        # Create line plot
        plt.figure(figsize=(8, 6))
        plt.plot(labels, values, marker='o', linestyle='-')
        plt.xlabel('Date and Time')
        plt.ylabel(column)
        plt.title(f'{column} over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save chart to a BytesIO object
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        chart_url = base64.b64encode(img.getvalue()).decode()

        # Append chart URL and column name to the list
        chart_data.append((chart_url, column))
        plt.close()

    # Convert DataFrame to HTML table
    table_html = df.to_html(index=False)

    return render_template('index.html', table_html=table_html, chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
