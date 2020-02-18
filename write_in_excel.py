import xlwings as xw
#open excel file
wb = xw.Book(r"yourExcelfile.xlsx")
# select your excel sheet
data_sheet = wb.sheets["sheet name"]
#clean the existing data
data_sheet.range("A1:G10").clear()

#import 40 data from data.json
for data_num in range(0, 40):
    
    #call for function
    data=web_crawler (data_num)
   
    # find the last row of data in excel sheet
    last_row = data_sheet.range("A1").end("down").row
    
    #convert timestamp format to year/day/month/hour
    localTimestamp=data["localTimestamp"]
    localtime=datetime.fromtimestamp(localTimestamp)

    #write data in excel
    data_sheet.range(f"A{last_row+1}").value = localtime.strftime("%Y/%m/%d")
    data_sheet.range(f"B{last_row+1}").value = localtime.strftime("%H")  
    data_sheet.range(f"C{last_row+1}").value = data["rating"]
    data_sheet.range(f"D{last_row+1}").value = data["max_swell"]
    data_sheet.range(f"E{last_row+1}").value = data["min_swell"]
    data_sheet.range(f"F{last_row+1}").value = data["period"]
    data_sheet.range(f"G{last_row+1}").value = data["temperature"]