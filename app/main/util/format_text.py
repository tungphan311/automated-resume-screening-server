

def format_contract(id):
    if id == 0:
        return "Toàn thời gian"
    elif id == 1:
        return "Bán thời gian"
    else:
        return "Thực tập"

def format_salary(min_salary, max_salary):
    if not min_salary:
        if not max_salary:
            return "Thoả thuận"
        else: 
            return "Lên đến {} triệu đồng".format(max_salary)
    else:
        if not max_salary:
            return "Từ {} triệu đồng".format(min_salary)
        else:
            return "{} - {} triệu đồng".format(min_salary, max_salary)