#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# ormerodl, 2020-Aug-18, Update file title
# ormerodl, 2020-Aug-18, Add/Move processing code into DataProcesser class
# ormerodl, 2020-Aug-18, Add write_file capability
# ormerodl, 2020-Aug-18, Add/Move I/O functions from presentation into IO class
# ormerodl, 2020-Aug-19, Troubleshoot for delete loop running but not deleting
# ormerodl, 2020-Aug-19, Troubleshoot for save loop running but not saving to file
# ormerodl, 2020-Aug-19, Update Docstring and comments
# ormerodl, 2020-Aug-26, Add descriptive variable names
# ormerodl, 2020-Aug-26, Add DataProcessing remove_cd_from_inventory function
# ormerodl, 2020-Aug-26, Removed dependence on global variables
# ormerodl, 2020-Aug-26, Update read_file to load from binary file rather than text
# ormerodl, 2020-Aug-26, Update write_file to save to binary file rather than text
# ormerodl, 2020-Aug-26, Add Error Exception handling
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat' # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    @staticmethod
    def get_dicRow(cd_id, cd_name, cd_artist, table):
        """Function to add row to a list of dictionaries

        Appends data input by a user to the 2D list lstTbl

        Args:
            cd_id: user input ID
            cd_name: user input Title
            cd_artist: user input Artist

        Returns:
            None.
        """
        dicRow = {'ID': int(cd_id), 'Title': cd_name, 'Artist': cd_artist}
        table.append(dicRow)

    def remove_cd_from_inventory(table, intIDDel):
        """ Function to remove data from in memory inventory table

        Args:
            intIDDel (int): integer indicating the ID of entry to remove

        Returns:
            table (list of dicts): list of dictionaries with the specified entry removed.
        """

        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row["ID"] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print("The CD was removed")
        else:
            print("Could not find this CD!")


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'rb') as objFile:
            table = pickle.load(objFile) #load one line of data
        return table

    @staticmethod
    def write_file(file_name, table):
        """Function to save data from a list of dictionaries to text file

        Writes the data from a 2D table (list of dicts) to a text file identified by file_name
         one dictionary row in table represents one line in the file.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        with open(file_name, 'wb') as objFile:
            pickle.dump(table,objFile)
        print('CD Inventory has been saved to "CDInventory.dat"\n')

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

        """
        choice = ''
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================\n')

    @staticmethod
    def user_input():
        """Gets user input for CD Inventory

        Args:
            None.

        Returns:
            strID (string): A numeric string from user input
            strTitle (string): alphanumeric string for CD Title
            StrArtist (string): alphnumeric string for CD Artist

        """
        strID = int(input('Enter ID: ').strip())
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, strArtist

    @staticmethod
    def del_Row():
        """Function to remove row from a list of dictionaries

        Deletes data input by a user from the 2D list lstTbl
        
        Args:
            intIDDel (int): user input ID for deletion
        
        Returns:
            None.
        """
        intIDDel = int(input('Enter the ID you would like to delete: '))
        return intIDDel


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break

    # 3.2 process load inventory
    if strChoice == 'l':
        try:
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory loaded from file.')
            strYesNo = input('Would you like to continue and load from file? [y/n] ')
            if strYesNo.lower() == 'y':
                lstTbl = FileProcessor.read_file(strFileName, lstTbl)
                IO.show_inventory(lstTbl)
            else:
                input('canceling... Inventory data NOT loaded. Press [ENTER] to continue to the menu.')
                IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        except EOFError:
            print('File exists, but there is no data. Please add data using menu option "a"\n')
        except FileNotFoundError:
            createFile = input('File does not exist, would you like to create it now? [y/n] ')
            if createFile.lower() == 'y':
                with open(strFileName, 'w'):
                    pass
                print('File has been created, get down whichya bad self adding data!')
            else:
                pass

    # 3.3 process add a CD
    elif strChoice == 'a':
        try:
            strID, strTitle, strArtist = IO.user_input()
            DataProcessor.get_dicRow(strID, strTitle, strArtist, lstTbl)
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        except ValueError:
            print('ID must be a positive integer. Please try again.\n')

    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.5 process delete a CD
    elif strChoice == 'd':
        try:
            intIDDel = IO.del_Row()
            DataProcessor.remove_cd_from_inventory(lstTbl, intIDDel)
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        except ValueError:
            print('Sorry, ID must be a positive integer. Please try again.\n')

    # 3.6 process save inventory to file
    elif strChoice == 's':
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        if strYesNo == 'y':
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.

    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




