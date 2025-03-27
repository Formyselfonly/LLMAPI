def get_full_name(first_name:str,last_name:str):
    full_name=first_name.title()+" "+last_name.title()
    return full_name
name=get_full_name("Zheng","Shijie")
print(name)

def get_name_with_age(name:str,age:int):
    name_with_age=name+" is the old: "+str(age)
    return name_with_age

name_with_age=get_name_with_age("ShijieZheng",25)
print(name_with_age)

def get_items(item_a:str,item_b:int,item_c:float):
    return item_a,item_b,item_c

def print_capitalize_items(items:list[str]):
    for item in items:
        print(item.capitalize())

test=["as","b","c","d"]
print_capitalize_items(test)

# items_t: tuple[int, int, str] vs items_t= tuple[int, int, str]
# One is for hint,one is for regular and can't be different
def process_items(items_t: tuple[int, int, str], items_s: set[float]):
    return items_t, items_s

test=process_items((1,1,"1"),{1.1,2.2})
print(test)

my_dict={"A":"1","B":"2","c":3}
my_dict_change=list(my_dict.items())
print("\n")
print(my_dict_change)

def dict_items_processing(price:dict[str,float]):
    for item_name,item_price in price.items():
        print(item_name)
        print(item_price)

def process_item(item:int|str):
    print(item)

class Person:
    def __init__(self,name:str):
        self.name=name
    def get_name(self):
        return self.name
def get_person_name(person:Person):
    return person.get_name()

person=Person("Shijie Zheng")
person_name=get_person_name(person)
print(person_name)