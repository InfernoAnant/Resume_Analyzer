import csv
import os

skills_file = 'dataset/skills.csv'
out_file = 'dataset/skill_resources.csv'

curated_skills = {
    'python': ('Programming', 'Intermediate', '', 20, 'Python Official Tutorial', 'https://docs.python.org/3/tutorial/index.html'),
    'sql': ('Data Analyst', 'Beginner', '', 15, 'SQL Tutorial by W3Schools', 'https://www.w3schools.com/sql/'),
    'java': ('Programming', 'Intermediate', '', 25, 'Java Programming - Mooc.fi', 'https://java-programming.mooc.fi/'),
    'javascript': ('Programming', 'Intermediate', '', 20, 'MDN JavaScript Guide', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide'),
    'react': ('Frontend', 'Intermediate', 'javascript', 25, 'React Official Docs', 'https://react.dev/learn'),
    'angular': ('Frontend', 'Intermediate', 'javascript', 25, 'Angular Official Docs', 'https://angular.io/docs'),
    'docker': ('DevOps', 'Intermediate', 'linux', 15, 'Docker Curriculum', 'https://docker-curriculum.com/'),
    'kubernetes': ('DevOps', 'Advanced', 'docker', 30, 'Kubernetes Basics', 'https://kubernetes.io/docs/tutorials/kubernetes-basics/'),
    'aws': ('Cloud', 'Intermediate', '', 30, 'AWS Skill Builder', 'https://explore.skillbuilder.aws/'),
    'git': ('DevOps', 'Beginner', '', 10, 'Pro Git Book', 'https://git-scm.com/book/en/v2'),
    'html': ('Frontend', 'Beginner', '', 10, 'MDN HTML Basics', 'https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics'),
    'css': ('Frontend', 'Beginner', 'html', 15, 'MDN CSS Basics', 'https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/CSS_basics'),
    'node.js': ('Backend', 'Intermediate', 'javascript', 20, 'Node.js Official Docs', 'https://nodejs.org/en/docs/'),
    'django': ('Backend', 'Intermediate', 'python', 25, 'Django Official Tutorial', 'https://docs.djangoproject.com/en/stable/intro/tutorial01/'),
    'flask': ('Backend', 'Intermediate', 'python', 15, 'Flask Quickstart', 'https://flask.palletsprojects.com/en/2.3.x/quickstart/'),
    'mongodb': ('Database', 'Intermediate', '', 15, 'MongoDB University', 'https://learn.mongodb.com/'),
    'postgresql': ('Database', 'Intermediate', 'sql', 15, 'PostgreSQL Tutorial', 'https://www.postgresqltutorial.com/'),
    'machine learning': ('Machine Learning', 'Advanced', 'python', 40, 'Machine Learning Crash Course', 'https://developers.google.com/machine-learning/crash-course'),
    'tensorflow': ('AI Engineer', 'Advanced', 'machine learning', 30, 'TensorFlow Tutorials', 'https://www.tensorflow.org/tutorials'),
    'pytorch': ('AI Engineer', 'Advanced', 'machine learning', 30, 'PyTorch Tutorials', 'https://pytorch.org/tutorials/'),
    'rest api': ('Backend', 'Intermediate', '', 15, 'RESTful API Tutorial', 'https://restfulapi.net/'),
    'linux': ('DevOps', 'Beginner', '', 15, 'Linux Journey', 'https://linuxjourney.com/'),
    'ci/cd': ('DevOps', 'Intermediate', 'git', 20, 'CI/CD Guide - GitLab', 'https://about.gitlab.com/topics/ci-cd/'),
    'redis': ('Backend', 'Intermediate', '', 10, 'Redis Official Tutorial', 'https://redis.io/docs/getting-started/'),
    'typescript': ('Programming', 'Intermediate', 'javascript', 20, 'TypeScript Handbook', 'https://www.typescriptlang.org/docs/handbook/intro.html'),
    'nextjs': ('Frontend', 'Intermediate', 'react', 25, 'Next.js Foundations', 'https://nextjs.org/learn/foundations/about-nextjs'),
    'azure vm': ('Cloud', 'Intermediate', '', 20, 'Azure Fundamentals', 'https://learn.microsoft.com/en-us/training/azure/'),
    'google cloud': ('Cloud', 'Intermediate', '', 20, 'Google Cloud Training', 'https://cloud.google.com/training'),
    'tableau': ('Data Analyst', 'Intermediate', '', 20, 'Tableau Free Training', 'https://www.tableau.com/learn/training/20234'),
    'power bi': ('Data Analyst', 'Intermediate', '', 20, 'Power BI Documentation', 'https://learn.microsoft.com/en-us/power-bi/')
}

with open(skills_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    all_skills = [row for row in reader if row and len(row) >= 2]

out_rows = []
out_rows.append(['skill', 'category', 'difficulty', 'prerequisite', 'est_hours', 'resource_title', 'resource_url'])

for row in all_skills:
    skill = row[0].strip().lower()
    category = row[1].strip()
    if skill in curated_skills:
        cat, diff, prereq, hrs, title, url = curated_skills[skill]
        out_rows.append([skill, category, diff, prereq, hrs, title, url])
    else:
        out_rows.append([skill, category, 'Intermediate', '', 15, 'Search official documentation', f'https://www.google.com/search?q={skill.replace(" ", "+")}+tutorial'])

with open(out_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(out_rows)

print("Created skill_resources.csv with", len(out_rows)-1, "skills.")
