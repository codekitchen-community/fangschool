from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/construction_site')
def construction_site():
    return render_template('construction_site.html')


from random import randrange, choice


@app.route('/playground')
def playground():
    students = []
    names = ['Grey', 'Good', 'Peter', 'cook24', 'fi22', 'molly', 'jackss', '彩蛋', '旺福', '赵杰', '李辉']
    for i in range(50):
        rand_color = (randrange(255), randrange(255), randrange(255))

        students.append({
            'width': randrange(50, 200),
            'height': randrange(50, 200),
            'name': choice(names),
            'color': f'rgb{rand_color}',
        })
    print(students)
    return render_template('playground.html', students=students)
