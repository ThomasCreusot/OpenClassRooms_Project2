# OpenClassRooms_Project2
Use Python basics for market analysis

# Project presentation
The present project is the second one of the training course *Python Application Developer*, offered by OpenClassRooms and aims to *Use Python basics for market analysis*.
The main goal is to develop a ‘scraper’ : a **program which extracts information from [a website related to books](http://books.toscrape.com/)**.
The website contains categories, and each category contains products (books).
**Products information** (product_page_url, universal_ product_code (upc), title, etc.) are extracted and then loaded in a CSV file (one CSV file per category). Each CSV file is recorded in the **folder ‘scraping_CSV_files’** which is created by the program **at the same location** than the python program. 
**Pictures of the product**s are also downloaded, and recorded in the **‘scraping_products_pictures’ folder**, which is created by the program **at the same location** than the python program.

# Project execution
To correctly execute the program, you need to activate the associated virtual environment. It has been recorded in the ‘requirements.txt’ file.
## To create and activate the virtual environment 
Please follow theses instructions:
1. Open your Shell (Windows : *windows + R* > *cmd* ; Mac : *Applications > Utilitaires > Terminal.app*)
2. Find the folder which contains the program (with *cd* command)
3. Create a virtual environment : write *python -m venv env* in the console
4. Activate this virtual environment : 
-Linux or Mac: write *source env/bin/activate* in the console
-windows: write *env\Scripts\activate.bat* in the console
5. Install the python packages recorded in the *requirements.txt* file : write *pip install -r requirements.txt* in the console 

## To execute the program
Please follow theses instructions
6. Execute the code : write *python main.py* in the console (Python must be installed on your computer).
