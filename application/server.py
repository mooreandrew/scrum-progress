from application.models import projects
from application import app, db
from application.forms import projectSettings

from flask import request, render_template, request, redirect, url_for, session, flash
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from dateutil import parser

from trello import TrelloClient
from datetime import datetime, date, timedelta
import json
import time
import math

import os


@app.route('/')
def login():
    return 'ok'

@app.route('/<project_url>/setup', methods=['GET', 'POST'])
def setup(project_url):
    form = projectSettings()
    form.collaboration_project_name.choices = get_trello_projects()

    res = projects.query.filter(projects.project_name.ilike(project_url)).order_by(projects.id).all()
    if (len(res) == 1):
        form.project_name.data = res[0].project_name
        form.collaboration_tool.data = res[0].collaboration_tool
        form.collaboration_project_name.data = res[0].collaboration_project_name
        form.start_sprint.data = res[0].start_sprint
        form.start_day.data = res[0].start_day
        form.start_month.data = res[0].start_month
        form.start_year.data = res[0].start_year



    if request.method == 'POST':
        if form.validate_on_submit():
            db.session.query(projects).filter(projects.project_url == project_url).delete()
            db.session.commit()

            project_settings = projects(project_url, request.form['project_name'], request.form['collaboration_tool'], request.form['collaboration_project_name'], request.form['start_sprint'], request.form['start_day'], request.form['start_month'], request.form['start_year'])
            db.session.add(project_settings)
            db.session.commit()
            return redirect("/" + project_url, code=302)

    return render_template(
        'setup.html',
        asset_path='/static/',
        form=form,
        project_url=project_url)

@app.route('/<project_url>')
def dashboard(project_url):
    project_settings = projects.query.filter(projects.project_name.ilike(project_url)).order_by(projects.id).all()
    if (len(project_settings) == 0):
        return redirect("/" + project_url + "/setup", code=302)

    project_name = project_settings[0].project_name

    sprint_start_date = date(project_settings[0].start_year, project_settings[0].start_month, project_settings[0].start_day)
    sprint_start = project_settings[0].start_sprint
    current_date = date.today()

    sprint_start_date_epoch = time.mktime(sprint_start_date.timetuple())
    current_date_epoch = time.mktime(current_date.timetuple())
    sprint_date_sub = (current_date_epoch - sprint_start_date_epoch)
    sprint_diff = math.floor((int(sprint_date_sub / 86400)) / 14)

    sprint = str(int(sprint_start) + sprint_diff)
    sprint_start_date = sprint_start_date + timedelta(days=(14 * sprint_diff))
    sprint_finish_date = sprint_start_date + timedelta(days=(14 * sprint_diff))

    client = TrelloClient(
        api_key=os.environ.get('trello_api_key'),
        api_secret=os.environ.get('trello_api_secret'),
        token=os.environ.get('trello_token')
    )

    board = client.get_board(project_settings[0].collaboration_project_name)

    list = board.all_lists()
    for l in board.all_lists():
        if (l.name.decode("utf-8") == 'Sprint ' + sprint + ' - Backlog'):
            backlog_list = l.id
        if (l.name.decode("utf-8") == 'Sprint ' + sprint + ' - Doing'):
            doing_list = l.id
        if (l.name.decode("utf-8") == 'Sprint ' + sprint + ' - Done'):
            done_list = l.id

    if 'backlog_list' not in locals():
        return 'Error: No Sprint ' + sprint + ' - Backlog list found in Trello'

    if 'backlog_list' not in locals():
        return 'Error: No Sprint ' + sprint + ' - Doing list found in Trello'

    if 'backlog_list' not in locals():
        return 'Error: No Sprint ' + sprint + ' - Done list found in Trello'

    done_days = []
    for x in range(0, 14):
        done_days.append(0)

    done_cards = []
    done_count = 0
    done_points = 0

    list = board.get_list(done_list)

    for c in list.list_cards():
        if (len(c.listCardMove_date()) > 0):
            card_date = parser.parse(str(c.latestCardMove_date))
        else:
            card_date = c.create_date()

        start_epoch = time.mktime(sprint_start_date.timetuple())
        card_date_epoch = time.mktime(card_date.date().timetuple())
        date_sub = (card_date_epoch - start_epoch)
        day_of_sprint = int(date_sub / 86400)

        card_info = get_points(c.name)
        done_cards.append([card_info[0], card_info[1], c.id])
        done_count = done_count + 1
        done_points = done_points + int(card_info[1])
        done_days[day_of_sprint] = done_days[day_of_sprint] + int(card_info[1])

    doing_cards = []
    doing_count = 0
    doing_points = 0

    list = board.get_list(doing_list)

    for c in list.list_cards():
        card_info = get_points(c.name)
        doing_cards.append([card_info[0], card_info[1], c.id])
        doing_count = doing_count + 1
        doing_points = doing_points + int(card_info[1])


    backlog_cards = []
    backlog_count = 0
    backlog_points = 0

    list = board.get_list(backlog_list)

    for c in list.list_cards():
        card_info = get_points(c.name)
        backlog_cards.append([card_info[0], card_info[1], c.id])
        backlog_count = backlog_count + 1
        backlog_points = backlog_points + int(card_info[1])


    total_points = backlog_points + doing_points + done_points

    planned_days = []
    for x in range(0, 14):
        planned_days.append(int(total_points/14 * (14 - x)))


    running_total = total_points
    actual_days = []
    for x in range(0, 14):
        running_total = running_total - done_days[x]
        actual_days.append(running_total)



    burnupdata = []
    burnupkey = []

    for x in range(0, int(sprint) - int(sprint_start)):
        burnupdata.append(0)

    burnupkey = []
    for x in range(int(sprint_start), int(sprint)):
        burnupkey.append(x)



    list = board.all_lists()
    for l in board.all_lists():
        for x in range(int(sprint_start), int(sprint)):
            if (l.name.decode("utf-8") == 'Sprint ' + str(x) + ' - Done'):
                for c in l.list_cards():
                    card_info = get_points(c.name)
                    burnupdata[int(sprint) - x - 1] = burnupdata[int(sprint) - x - 1]  + int(card_info[1])
    burnupdata.reverse()

    #card = board.get_cards('55c0be1c385f787cf2c6b371')

    #print(dir(card.latestCardMove_date()))
    return render_template('dashboard.html',
        backlog_cards=backlog_cards,
        backlog_count=backlog_count,
        backlog_points=backlog_points,
        doing_cards=doing_cards,
        doing_count=doing_count,
        doing_points=doing_points,
        done_cards=done_cards,
        done_count=done_count,
        done_points=done_points,
        json_planned=json.dumps(planned_days),
        json_actual=json.dumps(actual_days),
        sprint=sprint,
        sprint_start_date=sprint_start_date,
        sprint_finish_date=sprint_finish_date,
        project_name=project_name,
        burnupdata=json.dumps(burnupdata),
        burnupkey=json.dumps(burnupkey),
        asset_path='/static/'
    )

def get_points(name):
    split = name.decode("utf-8").split('(')
    points = split[len(split) - 1].replace(')', '')
    return split[0].strip(), points.strip()



def get_trello_projects():
    client = TrelloClient(
        api_key=os.environ.get('trello_api_key'),
        api_secret=os.environ.get('trello_api_secret'),
        token=os.environ.get('trello_token')
    )

    form_projects = []
    for b in client.list_boards():
        form_projects.append([b.id, b.name.decode("utf-8")])

    return form_projects
