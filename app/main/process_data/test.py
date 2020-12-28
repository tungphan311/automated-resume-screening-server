import sys
sys.path.append("/Users/vinhpham/Desktop/automated-resume-screening-server")

from app.main.process_data.classify_wrapper.classify_manager import ClassifyManager

mn = ClassifyManager()

jd = """
Job Description
The Senior Backend Engineer (SBE) designs complex backend technology solutions, develops code, and tests and maintains new and existing systems. As part of Floware’s Infrastructure & Security team, he partners closely with development teams to define scope and requirements for reusable services with integration services and APIs, and to use appropriate technology solutions for the business. The BE is a key member of the team responsible for delivering robust solutions while defining backend standards for all development teams at Floware VN. 

Your Skills and Experience
WHO YOU ARE

3+ years of experience designing, developing, and managing RESTful APIs
3+ years of experience developing in any of following core language: NodeJS/Ruby on Rails/JS or experience with relevant frameworks
Demonstrated design and programming skills using NodeJS, JSON, Web Services, XML, XSLT, etc...
Excellent experience in designing and implementing database systems with integrity, scalability, performance, reliability, security in mind
HUGE PLUS IF YOU ARE/HAVE

Excellent fullstack developer
Excellent understanding of backend development best practices and standards
Impeccable leadership skills and able to drive solutions
Excellent understanding of CI/CD/CD
Excellent experience designing and developing backend microservices
Why You'll Love Working Here
We challenge ourselves every day to find better solutions and better ways to do things. We ask difficult questions and work together to solve them. We believe in doing the right things as well as doing things right. We value honesty, hard work, integrity, and transparency. We are committed to transforming people’s lives, will you join us today?

COMPENSATION & BENEFITS

Friendly, flexible, and fun working environment
Very attractive salary based on skills and experience
Free office lunch
Coffee, tea, snack bar everyday
Full income tax, insurance paid by company (Net Salary)
13th month of salary
Great opportunity for career development
Company trip, team building, monthly party, etc.
"""

result = mn.run_classifier("backend", jd, explanation=True)
