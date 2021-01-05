from app.main.model.job_domain_model import JobDomainModel


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


def format_skill(resume):
    tech = resume.technical_skills.split("|")
    soft = resume.soft_skills.split("|")

    return ", ".join(tech + soft) 


def format_domains(domains):
    if domains:
        domains = domains.split(",") 
        domains = [ int(domain) for domain in domains ]
    else:
        domains = []
        
    return domains

def format_provinces(provinces):
    return provinces.split(",") if provinces else []

def format_experience(exp):
    year = int(exp / 12)
    month = exp % 12

    return "{} năm {} tháng".format(year, month) if year > 0 else "{} tháng".format(month)


def format_education(post):
    if post.education_level == 0:
        return "Không yêu cầu bằng cấp"
    elif post.education_level:
        return "Bằng {}".format(format_education_level(post.education_level))

def format_education_level(level):
    if level == 1:
        return "đại học/ cao đẳng"
    elif level == 2:
        return "thạc sĩ"
    elif level == 3:
        return "tiến sĩ"

