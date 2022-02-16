#!/usr/bin/env/python3.8

import sqlite3                                                                                                          
import csv
import sys
import os
import time                                                                                                              


# Define the function to open source file, get headers and rows
def importFile(file):                                                                                                   
    rows = []                                                                                                           
    with open(file, encoding="utf-8-sig") as f:                                                                         
        reader = csv.reader(f)                                                                                          
        rows = [ row for row in reader ]                                                                                
        return rows[0], rows[1:]                                                                                        

#manually specify the source csv file
#csv_file = input('enter csv filename: ')

def clean(s):                                                                                                           
    return "".join([ c for c in s if c.isalpha() ])

# Work on every csv file in a specified dir
directory = input('enter path to dir with raw csv data: ')
# Count the csv file number in the dir starting from 0 for the first file
file_num = 0
for csv_file in os.listdir(directory):
    #f=os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(csv_file) and csv_file.startswith('result.'):
        continue
    elif os.path.isfile(csv_file) and csv_file.endswith('.csv') and csv_file.startswith('Report-'):
        print(f"Working on the file {csv_file}")
        if file_num == 0:
            #### > do the magic w/ the first file hdrs_0
            # populate headers and rows list                                                                                                                        
            hdrs, rows = importFile(csv_file)
            # populate headers for output csv
            csv_headers = []
            for i in hdrs:
                csv_headers.append(i)
            csv_headers.append('Report time')
            csv_headers.append('Latitude')
            csv_headers.append('Longitude')
            # define DB name derived from the source filename
            db_name = str(csv_file+'db.db')

            # check if DB exists and delete if yes
            if os.path.isfile(db_name):
                os.remove(db_name)
                
            # create and connect to the DB
            con = sqlite3.connect(db_name)
            cur = con.cursor()   

            columnText = ",".join(["%s text" % clean(f) for f in hdrs])                                                             
            cur.execute('CREATE TABLE IF NOT EXISTS Switches (%s)' % columnText)   
            
            for rowNum, row in enumerate(rows):                                                                                     
                #if len(row) != 23:                                                                                                  
                #    import pdb; pdb.set_trace()                                                                                     
                columnText = ",".join(["'%s'" % f.replace("'", r"") for f in row])                                                  
                #print("%d: %s" % (rowNum, columnText))                                                                              
                cur.execute("INSERT INTO Switches values (%s)" % columnText)
            
            # Define the value of the Date deployed value per each row
            date_depl_str=str(csv_file.strip('Report-.csv'))
            #print('date_depl_str ', date_depl_str)
            date_depl_tup=tuple([date_depl_str])
            #print('date_depl_tup ', date_depl_tup)

            # Get the list of A
            A_rows = []
            for row in cur.execute("select * from switches where `Hostname`like '*a%' and (Model like '%SUP%' or Model like '%7280%')"):
                #print(row)
                A_rows.append(row + date_depl_tup)
                #PA_rows.append(csv_file.strip('Report-.csv'))


            # Get the list of G
            G_rows = []
            for row in cur.execute("select * from switches where `Hostname`like '*g%' and (Model like '%SUP%' or Model like '%7280%')"):
                #print(row)
                G_rows.append(row+date_depl_tup)
              
            # Get the list of B
            B_rows = []
            for row in cur.execute("select * from switches where `Hostname`like '*b%' and (Model like '%SUP%' or Model like '%7280%')"):
                #print(row)
                B_rows.append(row + date_depl_tup)
            
            #Get the list of SW
            SW_rows = []
            for row in cur.execute("select * from switches where `Hostname` like '*sw%' and Model like 'DCS-7060CX-32S-R'"):
                SW_rows.append(row + date_depl_tup)
            
            #Get the list of 1SW
            1SW_rows = []
            for row in cur.execute("select * from switches where `Hostname` like '1sw%' and (Model like '%SUP%' or Model like '%7060CX%')"):
                PSW_rows.append(row + date_depl_tup)
            
            #Get the list of 2SW
            2SW_rows = []
            for row in cur.execute("select * from switches where `Hostname` like '2sw%' and Model like '%SUP%'"):
                2SW_rows.append(row + date_depl_tup)
                
            #Get the list of 3SW
            3SW_rows = []
            for row in cur.execute("select * from switches where `Hostname` like '3sw%' and Model like '%7060CX%'"):
                3SW_rows.append(row + date_depl_tup)

            # open file for writing the result to
            #check the existance of the output file, delete if exists and create a new empty one
            # Output for your network
            output = str('result.'+csv_file)
            if os.path.isfile(output):
                print(f"Found existing result file {output}, removing")
                os.remove(output)
                    # f=open(output,"w")
                    # f.close()
            with open(output, 'w') as fr:
                print(f"Creating a brand new result file {output} and writing results")
                writer = csv.writer(fr)  
                #write headers to the output file  
                writer.writerow(csv_headers)
                
                writer.writerows(A_rows)
                writer.writerows(G_rows)
                writer.writerows(B_rows)
            
            # Output for other part of the network
            _output = str('_result.'+csv_file)
            if os.path.isfile(_output):
                print(f"Found existing result file {_output}, removing")
                os.remove(output)
                    # f=open(output,"w")
                    # f.close()
            with open(_output, 'w') as fr:
                print(f"Creating a brand new result file {_output} and writing results")
                writer = csv.writer(fr)  
                #write headers to the output file  
                writer.writerow(csv_headers)
                
                writer.writerows(SW_rows)
                writer.writerows(1SW_rows)
                writer.writerows(2SW_rows)
                writer.writerows(3SW_rows)

            con.commit()                                                                                                            
            con.close()
            # clean up the DB for the existing file
            os.remove(db_name)

            print(f"File: {csv_file}, Number of As: {len(A_rows)}")
            print(f"File: {csv_file}, Number of Gs: {len(A_rows)}")
            print(f"File: {csv_file}, Number of Bs: {len(B_rows)}")

            print(f"File: {csv_file}, Number of SWs: {len(SW_rows)}")
            print(f"File: {csv_file}, Number of 1SWs: {len(1SW_rows)}")
            print(f"File: {csv_file}, Number of 2SWs: {len(2SW_rows)}")
            print(f"File: {csv_file}, Number of 3SWs: {len(3SW_rows)}")

            orig_csv_headers = []
            for i in hdrs:
                orig_csv_headers.append(i)


            file_num += 1
        else:
            #### > collect hdrs from current file and compare with hrds of file.0
            hdrs, rows = importFile(csv_file)
            # populate headers for output csv
            csv_headers = []
            for i in hdrs:
                csv_headers.append(i)
            csv_headers.append('Report time')
            csv_headers.append('Latitude')
            csv_headers.append('Longitude')
            #print('csv_headers2: \n', csv_headers)
            # Compare the headers of the this csv with headers of the result file
            for result_file in os.listdir(directory):
                if os.path.isfile(result_file) and result_file.startswith('result.Report-'):
                    with open(result_file, "a+") as f:
                        reader = csv.DictReader(f)
                        headers = reader.fieldnames
                        writer = csv.writer(f)  
                  
                        # define DB name derived from the source filename
                        db_name = str(csv_file+'db.db')

                        # check if DB exists and delete if yes
                        if os.path.isfile(db_name):
                            os.remove(db_name)
                            
                        # create and connect to the DB
                        con = sqlite3.connect(db_name)
                        cur = con.cursor()   

                        columnText = ",".join(["%s text" % clean(f) for f in hdrs])                                                             
                        cur.execute('CREATE TABLE IF NOT EXISTS Switches (%s)' % columnText)   
                        
                        for rowNum, row in enumerate(rows):                                                                                     
                            #if len(row) != 23:                                                                                                  
                            #    import pdb; pdb.set_trace()                                                                                     
                            columnText = ",".join(["'%s'" % f.replace("'", r"") for f in row])                                                  
                            #print("%d: %s" % (rowNum, columnText))                                                                              
                            cur.execute("INSERT INTO Switches values (%s)" % columnText)
                        
                        # Define the value of the Date deployed value per each row
                        date_depl_str=str(csv_file.strip('Report-.csv'))
                        #print('date_depl_str ', date_depl_str)
                        date_depl_tup=tuple([date_depl_str])
                        #print('date_depl_tup ', date_depl_tup)

                        # Get the list of A
                        A_rows = []
                        for row in cur.execute("select * from switches where `Hostname`like 'a%' and (Model like '%SUP%' or Model like '%7280%')"):
                            #print(row)
                            A_rows.append(row + date_depl_tup)
                            #PA_rows.append(csv_file.strip('Report-.csv'))


                        # Get the list of G
                        G_rows = []
                        for row in cur.execute("select * from switches where `Hostname`like 'g%' and (Model like '%SUP%' or Model like '%7280%')"):
                            #print(row)
                            G_rows.append(row+date_depl_tup)

                        # Get the list of B
                        B_rows = []
                        for row in cur.execute("select * from switches where `Hostname`like 'b%' and (Model like '%SUP%' or Model like '%7280%')"):
                            #print(row)
                            B_rows.append(row + date_depl_tup)
                          
                        writer.writerows(A_rows)
                        writer.writerows(G_rows)
                        writer.writerows(B_rows)

                        con.commit()                                                                                                            
                        con.close()
                        # Delete db off the current csv file
                        os.remove(db_name)

                        print(f"File: {csv_file}, Number of As: {len(A_rows)}")
                        print(f"File: {csv_file}, Number of Gs: {len(A_rows)}")
                        print(f"File: {csv_file}, Number of Bs: {len(B_rows)}")

                        file_num += 1
                ####<<<
                elif os.path.isfile(result_file) and result_file.startswith('result..Report-'):
                            #output = str('result.'+csv_file)
                    with open(result_file, "a+") as f:
                        reader = csv.DictReader(f)
                        headers = reader.fieldnames
                        writer = csv.writer(f)
                   
                        # define DB name derived from the source filename
                        db_name = str(csv_file+'db.db')

                        # check if DB exists and delete if yes
                        if os.path.isfile(db_name):
                            os.remove(db_name)
                            
                        # create and connect to the DB
                        con = sqlite3.connect(db_name)
                        cur = con.cursor()   

                        columnText = ",".join(["%s text" % clean(f) for f in hdrs])                                                             
                        cur.execute('CREATE TABLE IF NOT EXISTS Switches (%s)' % columnText)   
                        
                        for rowNum, row in enumerate(rows):                                                                                     
                            #if len(row) != 23:                                                                                                  
                            #    import pdb; pdb.set_trace()                                                                                     
                            columnText = ",".join(["'%s'" % f.replace("'", r"") for f in row])                                                  
                            #print("%d: %s" % (rowNum, columnText))                                                                              
                            cur.execute("INSERT INTO Switches values (%s)" % columnText)
                        
                        # Define the value of the Date deployed value per each row
                        date_depl_str=str(csv_file.strip('Report-.csv'))
                        #print('date_depl_str ', date_depl_str)
                        date_depl_tup=tuple([date_depl_str])
                        #print('date_depl_tup ', date_depl_tup)
                        ####>>>

                        #Get the list of SW
                        SW_rows = []
                        for row in cur.execute("select * from switches where `Hostname` like 'sw%' and Model like 'DCS-7060CX-32S-R'"):
                            SW_rows.append(row + date_depl_tup)
                        
                        #Get the list of 1SW
                        1SW_rows = []
                        for row in cur.execute("select * from switches where `Hostname` like '1sw%' and Model like '%SUP%' or Model like '%7060CX%'"):
                            1SW_rows.append(row + date_depl_tup)
                        
                        #Get the list of 2SW
                        2SW_rows = []
                        for row in cur.execute("select * from switches where `Hostname` like '2sw%' and Model like '%SUP%'"):
                            2SW_rows.append(row + date_depl_tup)
                            
                        #Get the list of 3SW
                        3SW_rows = []
                        for row in cur.execute("select * from switches where `Hostname` like '3sw%' and Model like '%7060CX%'"):
                            3SW_rows.append(row + date_depl_tup)                               
                        
                        
                        writer.writerows(SW_rows)
                        writer.writerows(1SW_rows)
                        writer.writerows(2SW_rows)
                        writer.writerows(3SW_rows)
                    

                        con.commit()                                                                                                            
                        con.close()
                        # Delete db off the current csv file
                        os.remove(db_name)

                        print(f"File: {csv_file}, Number of SWs: {len(SW_rows)}")
                        print(f"File: {csv_file}, Number of 1SWs: {len(1SW_rows)}")
                        print(f"File: {csv_file}, Number of 2SWs: {len(2SW_rows)}")
                        print(f"File: {csv_file}, Number of 3SWs: {len(3SW_rows)}")

                        file_num += 1

  

