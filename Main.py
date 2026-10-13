#The following program will  analyze Amazon data for different products within specific categories, utilizing key parameters
#STUDENT ID:24217516
def read_csv_file(CSVfile):
    data = []
    try:
        with open(CSVfile, 'r') as file:
            lines = file.readlines()
            if not lines:
                return data 
            
            #data within csv
            headers = lines[0].strip().lower().split(',')
            required_headers =['product_id','product_name','category','discounted_price $','actual_price $','discount_percentage %','rating','rating_count']
            #check for missing values in csv
            if not all(header in headers for header in required_headers):
                return data
            #indices of columns
            column_product_id = headers.index('product_id')
            name_of_product = headers.index('product_name')
            category_of_product = headers.index('category')
            discount_price_column = headers.index('discounted_price $')
            actual_price_column = headers.index('actual_price $')
            percentage_discount_column = headers.index('discount_percentage %')
            rating_column = headers.index('rating')
            rating_count_column = headers.index('rating_count')
            

            #process each data row
            for line in lines[1:]: #skip the header
                if not line.strip():
                    continue #if empty lines are present, it skips
                
                data_in_csv = line.strip().split(',')
                if len(data_in_csv) != len(headers):
                    continue
                try:
                    row = {
                        'product_id': data_in_csv[column_product_id],
                        'product_name': data_in_csv[name_of_product],
                        'category': data_in_csv[category_of_product],
                        'discounted_price': float(data_in_csv[discount_price_column]),
                        'actual_price': float(data_in_csv[actual_price_column]),
                        'discount_percentage': float(data_in_csv[percentage_discount_column]),
                        'rating': float(data_in_csv[rating_column]),
                        'rating_count':int(data_in_csv[rating_count_column])
                    }
                    data.append(row)
                except ValueError:
                    continue #rows with non-numeric data in numeric fields are skipped
                
    except FileNotFoundError:
        return data
    except Exception as e:
        return data
    return data
#Reading TXT
def read_TXT_data(TXTfile):
    sales_data = [] #initlise empty list
    with open(TXTfile, 'r') as file: #read file
        for line in file: #going through each line
            if line.startswith("Year:"):
                year_data = line.strip().lower().split(", ") #case-sensitivity
                sales_data.append(year_data)
    return sales_data
#OP1: [low discounted product, high discounted product]
def extreme_discount_price(data, category):
    filtered_low_discount_price = None  # Initialize to None
    filtered_high_discount_price = None
    
    # Iterate through data and filter case-insensitive condition
    for row in data:
        if row['category'].lower() == category.lower():
            discounted_price = row['discounted_price']
            
            if filtered_low_discount_price is None or discounted_price < filtered_low_discount_price['discounted_price']:
                filtered_low_discount_price = row
            
            if filtered_high_discount_price is None or discounted_price > filtered_high_discount_price['discounted_price']:
                filtered_high_discount_price = row

 
    # Check if any products were found in the specified category
    if filtered_low_discount_price is None or filtered_high_discount_price is None:
        return None, None

    
    # Return product IDs of the lowest and highest discounted products
    return filtered_high_discount_price['product_id'].lower(),filtered_low_discount_price['product_id'].lower()
#OP2: [mean, median, mean absolute deviation]
def statistical_measure_mean_deviation(data,category):
    #making sure the data is numeric
    def check_num(values):
        try:
            float(values)
            return True
        except ValueError:
            return False
    
    filter_product = [ row for row in data if row['category'].lower()==category.lower()] #filter category
    filter_rating_product = [row for row in filter_product if row['rating_count']>1000] #filter price
    if not filter_rating_product:
        return [0.0,0.0,0.0]
    filter_price = map(lambda row: row['actual_price'],filter_rating_product)
    price_list = [price for price in filter_price if check_num(price)]
    if not price_list:
        return [0.0,0.0,0.0]
    
    #mean calculation
    #initialise
    mean = 0 
    mean_actual_price = sum(price_list)/len(price_list)
    #mean absolute calculation
    numerator = 0 #initialise
    for price in price_list:
        numerator +=abs(price - mean_actual_price)
        denominator = len(price_list)
        mean_absolute_deviation = numerator/denominator 
    
    return mean_actual_price, mean_absolute_deviation

def statistical_measure_median(data, category):
    #making sure the data is numeric
    def check_num(values):
        try:
            float(values)
            return True
        except ValueError:
            return False
    filter_product = [ row for row in data if row['category'].lower()==category.lower()] #filter category
    filter_rating_product = [row for row in filter_product if row['rating_count']>1000] #filter price
    if not filter_rating_product:
        return 0.0
    filter_price = map(lambda row: row['actual_price'],filter_rating_product)
    price_list = [price for price in filter_price if check_num(price)]
    if not price_list:
        return 0.0
    #order in ascending manner
    sort_price_list = sorted(price_list)
    # X = ordered list of values in data list
    # n = number of values
    #handle empty list case
    n = len(sort_price_list)
    if n == 0:
        return 0.0 
    if n%2 ==1: #odd value
        #numerator
        median = sort_price_list[n//2] #middle number
    else: #when even
        median = (sort_price_list[n//2-1]+sort_price_list[n//2])/2
    
    return float(median)
#OP3:  [STD1, STD2, ..., STDN]
def standard_deviation_percentage(data):
    # Create a dictionary for category+discount percentage
    category_dic = {}
    filter_rating = []  # Validate values
    for row in data:
        try:
            rating = float(row['rating'])
            discount_percentage = float(row['discount_percentage'])
            if 3.3 <= rating <= 4.3:
                filter_rating.append(row)
        except ValueError:
            # Skip invalid data
            continue
    # Discount percentage based on category
    for row in filter_rating:
        category = row['category'].lower()
        if category not in category_dic:
            category_dic[category] = []
        try:
            discount_percentage = float(row['discount_percentage'])
            category_dic[category].append(discount_percentage)
        except ValueError:
            # Skip invalid data
                    continue
    # Calculating standard deviation
    std_deviation_lst = []
    for category in category_dic:
        discount_percentages = category_dic[category]
        N = len(discount_percentages)
        if N > 1:
            # Mean/variance of discount
            #let x be discount price
            mean_discount = sum(discount_percentages) / N
            variance_discount = sum((x - mean_discount) ** 2 for x in discount_percentages) / (N - 1)
            std_deviation = variance_discount ** 0.5
            # Add to the list
            std_deviation_lst.append(std_deviation)
        elif N == 1:
            # If only one discount percentage = not defined
            std_deviation_lst.append(0.0)
    # Sorted in the descending order
    std_deviation_lst = [round(sd, 4) for sd in std_deviation_lst]
    std_deviation_lst.sort(reverse=True)
    return std_deviation_lst
#OP4 Calculation
def correlation_value(TXTfile, lowest_discounted_id, highest_discounted_id):
    sales_data = read_TXT_data(TXTfile)
    if not sales_data:
        return 0.0 #read and process data and return 0 if empty
    
    low_sale_price = [] #Store sale count
    high_sale_price = []
    
    for year in sales_data:
        year_dic = {}
        for item in year[1:]:  # Skip the "Year: XXXX" part
            key, value_str = item.split(": ")
            key = key.strip().lower()
            try:
                value = int(value_str)
                year_dic[key] = value
            except ValueError:
                continue  # Skip invalid data
        
        low_sales_count = year_dic.get(lowest_discounted_id, 0)
        high_sales_count = year_dic.get(highest_discounted_id, 0)
        
        low_sale_price.append(low_sales_count)
        high_sale_price.append(high_sales_count)
    
    if len(low_sale_price) != len(high_sale_price) or len(low_sale_price) == 0:
        return 0.0
    #breaking the formula down to numerator and denominator 
    mean_low = sum(low_sale_price) / len(low_sale_price)
    mean_high = sum(high_sale_price) / len(high_sale_price)   
    numerator = sum((low_sale_price[i] - mean_low) * (high_sale_price[i] - mean_high) for i in range(len(low_sale_price)))
    sum_sq_low = sum((low_sale_price[i] - mean_low) ** 2 for i in range(len(low_sale_price)))
    sum_sq_high = sum((high_sale_price[i] - mean_high) ** 2 for i in range(len(high_sale_price)))    
    denominator = (sum_sq_low * sum_sq_high) ** 0.5 
    if denominator == 0:
        return 0.0
    
    correlation = numerator / denominator
    return round(correlation, 4)


def main(CSVfile, TXTfile, category):
    data = read_csv_file(CSVfile)
    lowest_discounted_id,highest_discounted_id = extreme_discount_price(data, category)
    OP1 =[lowest_discounted_id,highest_discounted_id] 
    mean, mean_absolute_deviation = statistical_measure_mean_deviation(data,category)
    median = statistical_measure_median(data, category)
    OP2 = [round(mean,4), round(median,4), round(mean_absolute_deviation,4)]
    OP3 = standard_deviation_percentage(data)
    OP4 = correlation_value (TXTfile,lowest_discounted_id, highest_discounted_id)
    return OP1,OP2,OP3,OP4


