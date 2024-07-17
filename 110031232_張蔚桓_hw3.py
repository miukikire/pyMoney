import sys

class Record:
    def __init__(self, category,description,amount):
        self._category=category
        self._description=description
        self._amount=int(amount)
    
    @property
    def cate(self):
        return self._category
    @property
    def des(self):
        return self._description
    @property
    def amo(self):
        return self._amount
    
class Records:

    def __init__(self):
        
        try:

            with open('record.txt','r') as fh:
                self._initial_balance=int(fh.readline())
                self._current_balance=int(fh.readline())
                self._temporary_expense=fh.readlines()
                self._expense_or_income=[]
                
                for i in self._temporary_expense:
                    self._expense_or_income.append(i.strip())
                check_value=self._initial_balance
                
                for i in self._expense_or_income:
                    check_value+=int(i.split()[2])
            
                assert check_value==self._current_balance
            
            for i,v in enumerate(self._expense_or_income):
                c,d,a=v.split()
                r=Record(c,d,int(a))
                self._expense_or_income[i]=r

        except:
            sys.stderr.write('Invalid format in records.txt, or unavle to find it. Deleting the contents.\n')
            
            try:
                self._initial_balance=int(input("How much money do you have?"))
                self._current_balance=self._initial_balance
                self._expense_or_income=[]
            
            except ValueError:
                sys.stderr.write('Invalid value for money. Set to 0 by default\n')
                self._initial_balance=0
                self._current_balance=0
                self._expense_or_income=[]

    def add(self):
        new_expense_or_income=input("Add an expense or income record with a category, a description, and amount:").split(', ')
        

        for i in new_expense_or_income:
            try:
                c,d,a=i.split()
                r=Record(c,d,int(a))
                self._expense_or_income.append(r)    
                cates=Categories()
                
                if cates.is_category_valid(r._category)==True:
                    try:
                        self._current_balance+=r._amount
                
                    except IndexError:
                        sys.stderr.write('The format of a record should be like this:food breakfast -50, meal lunch -100\nFail to add one of the records.\n')
                        self._expense_or_income.pop(-1)
                
                    except ValueError:
                        sys.stderr.write('Invalid value for money\nFail to add a record.\n')
                        self._expense_or_income.pop(-1)
                
                else:
                    print('The specified category is not in the category list.\nYou can check the category list by command "view categories".\nFail to add a record.\n')
                    self._expense_or_income.pop(-1)
            except:
                sys.stderr.write('Invalid format, the format of a record should be like this:food breakfast -50, meal lunch -100\nFail to add a record.\n')
                
        return self._current_balance, self._expense_or_income
    
    def view(self):
    
        if self._expense_or_income==[]:
            print('No records have been found')

        else:
            print("Here's your expense and income records:\n")
            for i, v in enumerate(self._expense_or_income):
                print(f'{i} {v.cate} {v.des} {v.amo}')
        
            print('')
            print(f'Now you have {self._current_balance} dollars')

    def delete(self):
        print("Here's your expense and income records:\n")
            
        for i, v in enumerate(self._expense_or_income):
            print(f'{i} {v.cate} {v.des} {v.amo}')
            
        print('')
            
        try:
            delete_record=int(input('Which record would you like to delete? Please insert the number:'))
            self._current_balance-=self._expense_or_income[delete_record]._amount
            self._expense_or_income.pop(delete_record)
            print("Here's your expense and income records after the deletion:\n")
            
            for i, v in enumerate(self._expense_or_income):
                print(f'{i} {v.cate} {v.des} {v.amo}')
            
            print('')
            print(f'Now you have {self._current_balance} dollars')
            
        except:
            sys.stderr.write('Invalid value. Fail to delete the record\n')

        return self._current_balance,self._expense_or_income
    
    def find(self):
        cates=Categories()
        object_category=input('Please enter the object you would like to find:')
        finded_result=[x for x in self._expense_or_income if x._category in cates.find_subcategories(object_category)]
        total_amount=0

        if finded_result==[]:
            print('No results have been found.\n')

        else:

            for i in finded_result:
                total_amount += i._amount
            print(f'Here is your expense and income records under category "{object_category}"\n')
            for i,v in enumerate(finded_result):
                print(f'{i} {v.cate} {v.des} {v.amo}')
            print('')
            print(f'The total amount above is {total_amount}')

    def save(self):
        with open('record.txt','w') as fh:
            fh.write(f'{self._initial_balance}\n')
            fh.write(f'{self._current_balance}\n')
            
            for i in self._expense_or_income:
                fh.writelines(f'{i.cate} {i.des} {i.amo}\n')

class Categories:
    def __init__(self):
        self._categories=['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
    
    def view(self,L, level=0):
        if L== None:
            return
        if type(L) in {list, tuple}:
            for child in L:
                self.view(child, level+1)
        else:
            print(f'{" "*2*level}-{L}')

    def is_category_valid(self,addition):

        """ To check whether the category exist when adding records. """

        if type(self._categories) in {list}:
            for i in self._categories:
                self._categories=i
                p=self.is_category_valid(addition)
                if p == True:
                    return True
                if p != False:
                    return p
        return self._categories == addition
        
    
    def find_subcategories(self,category):

        """ Make a list of the appointed category and all of its subcategories. """

        def find_subcategories_gen(category,categories,found=False):
            if type(categories)==list:
                for index,child in enumerate(categories):
                    yield from find_subcategories_gen(category,child,found)
                    if child==category and index+1<len(categories) and type(categories[index+1])==list:
                        yield from find_subcategories_gen(category,categories[index+1],found=True)
            else:
                if categories==category or found==True:
                    yield categories
        return [x for x in find_subcategories_gen(category,self._categories,found=False)]

def flatten(L):
    if type(L)==list:
        result=[]
        for child in L:
            result.extend(flatten(child))
        return result
    else:
        return [L]


records=Records()
cates=Categories()
    
while True:
    command=input(r'What would you like to do (add/view/delete/view categories/find/exit)?')
    
    if command=='add':
        records.add()
    
    elif command=='view':
        records.view()
    
    elif command=='delete':
        records.delete()

    elif command=='view categories':
        cates.view(cates._categories)

    elif command=='find':
        records.find()
        
    elif command=='exit':
        records.save()
        break
        
    else:
        sys.stderr.write('Invalid command. Try again\n')