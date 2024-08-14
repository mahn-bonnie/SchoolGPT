import pandas as pd

# Load student database
readatabase = pd.read_excel('school.xlsx', sheet_name='Student Database')

Adno = readatabase['Adm No'].tolist()
Adno = Adno[len(Adno) - 1] - 1
Name = readatabase['Name'].tolist()
Class = readatabase['Class'].tolist()
Section = readatabase['Section'].tolist()
House = readatabase['House'].tolist()
Mname = readatabase['Mother Name'].tolist()
Fname = readatabase['Father Name'].tolist()
Contact = readatabase['Contact No'].tolist()
Mainsub = readatabase['Main Sub'].tolist()
Faddsub = readatabase['1st Add Sub'].tolist()
Saddsub = readatabase['2nd Add Sub'].tolist()
Transport = readatabase['Transport'].tolist()
Fees = readatabase['Fees'].tolist()
Message = readatabase['Messages'].tolist()
Assignment = readatabase['Assignments Pending'].tolist()
Progressreport = readatabase['Progress Report'].tolist()

def showdetails(num):
    if num > 0 and num < Adno + 2:
        num -= 1
        details = {
            "Name": Name[num],
            "Class": Class[num],
            "Section": Section[num],
            "House": House[num],
            "Mother Name": Mname[num],
            "Father Name": Fname[num],
            "Contact Number": Contact[num],
            "Main Subjects": Mainsub[num].split(' '),
            "First Additional Subject": Faddsub[num],
            "Second Additional Subject": Saddsub[num],
            "Transport availed": Transport[num],
            "Fees": Fees[num],
            "New Messages": Message[num],
            "New Assignments": Assignment[num],
            "Progress Report": dict(zip(
                Mainsub[num].split(' ') + [Faddsub[num], Saddsub[num]],
                Progressreport[num].split(' ')
            ))
        }
        return details
    else:
        return {"error": "Wrong admission number. Please enter again"}
