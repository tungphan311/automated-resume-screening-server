import sys
sys.path.append("/Users/vinhpham/Desktop/automated-resume-screening-server")

from app.main.process_data.classify_wrapper.classify_manager import ClassifyManager

mn = ClassifyManager()
print("Load done.")

jd = """
<ul><li>University degree in Computer Sciences, or equivalent</li><li>3+ year experience in FE competence</li><li>Experienced in <strong>HTML/CSS, JavaScript/TypeScript </strong>and pre-processing languages such as LESS/SASS/SCSS</li><li>Experienced in layout techniques and frameworks such as Bootstrap, Material</li><li>Experienced in one of modern JS frameworks/libraries such as <strong>React, Angular, Vue,…</strong></li><li>Experienced in working with Vanilla JS, customer's libraries and frameworks</li><li>Experienced in CLI, setup project environment, running automated test using libraries such as Jest, Mocha, Chai</li><li>Experienced in web service development (SOAP, REST)</li><li>Good awareness about security and performance in web development</li><li>Proficient in code review, code refactoring, Unit Testing</li><li>Experience working in an Agile Software Development environment</li><li>Can perform the backends’ work (NodeJS, Python, Ruby, PHP) is a plus</li><li>Good communication in English</li></ul>
"""

result = mn.run_classifier("frontend", jd, explanation=True)

print(result.get_dict())