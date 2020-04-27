from flask import Flask, render_template, flash, redirect, url_for, request, json
from app import app, mysql

#Global Variables
countMatch=-1
artistName=''
userData = []
userRow=[]


@app.route('/')
def main():
    return "Welcome!"

@app.route('/meet')
def artistPick():
    curr=mysql.connection.cursor()
    curr.execute("select * from artists order by artists.artist_id")
    data = curr.fetchall()
    return render_template("artist.html", info=data)

@app.route('/match', methods=['GET', 'POST'])
def match():
    global countMatch
    global userData
    global userRow
    global artistName
    if request.method == 'POST':
        artistName = request.form.get('comp_select')

        # Find Artist Details
        curr=mysql.connection.cursor()
        sql_select_query = """select * from artists a where a.name = %s"""
        curr.execute(sql_select_query, (artistName,))
        data = curr.fetchall()
    
        #Finding Users with the same interest
        sql_select_query = """select * from fav_artists f where f.artist_id = %s"""
        curr.execute(sql_select_query, (data[0][0],))
        data=curr.fetchall()
        list_of_user=[]
        for i in data:
            list_of_user.append(i[0])
        print(list_of_user)

        # Find Matching User Id's
        sql_select_query = """ select * from users u where u.user_id in %s"""
        curr.execute(sql_select_query, (list_of_user, ))
        data=curr.fetchall()
        userData=data
        countMatch=-1

    countMatch+=1
    if countMatch==len(userData):
        countMatch=0   
    userRow=userData[countMatch]
    print(countMatch)

    return render_template("meet.html", info=userRow)


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    global artistName
    userId = request.form.get('userid')
    userName = request.form.get('userName')

    # Find Artist Details
    curr=mysql.connection.cursor()
    sql_select_query = """select * from artists a where a.name = %s"""
    curr.execute(sql_select_query, (artistName,))
    data = curr.fetchall()

    #Adding to User connections
    tup=(userId, data[0])
    # sql_select_query = """ insert into  %s"""
    # curr.execute(sql_select_query, tup)
    # data = curr.fetchall()

    print(userId)
    return render_template('connected.html', info=userName)