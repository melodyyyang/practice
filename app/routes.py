from flask import render_template, request, redirect, url_for, abort
from server import app, system
from datetime import datetime
from src.system import System
from src.order import *
from src.food import *

'''
Dedicated page for "page not found"
'''
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404


@app.route('/', methods=["GET", "POST"])
def index():
    ''' Welcome screen for customers
    Create a burger
    '''
    
    next_link = request.args.get('food')
    if next_link != 'Burger' and next_link != 'Wrap':
        next_link = "/"
    return render_template('index.html', next_link=next_link)

@app.route('/Burger', methods=["GET", "POST"])
def burger():
    ''' Bun selection
    '''
    
    bun_type = request.args.get('bun')
    if bun_type != 'Sesame' and bun_type != 'Muffin':
        bun_type = ""

    bun_count = request.args.get('count')
    if bun_count == '' or bun_count == None:
        bun_count = 2 # set default
    else:
        bun_count = int(request.args.get('count'))


    bun_count_action= request.args.get('count_action')

    if bun_count_action == '1':
        if bun_count >= 2:
            print("error")
        else:
            bun_count += 1

    if bun_count_action == '2':
        if bun_count <= 0:
            print("error")
        else:
            bun_count -= 1
                    
    return render_template('bun.html', bun_type=bun_type, count=bun_count)

def update_patty_count(type, count, action):
    if count:
        patty = Topping("Vegetarian Patty")
        set_count = int(count)
        if action:
            action = int(action)
            if action + set_count != 3:
                set_count += 2-action
        new_patty_cost = patty.price * set_count
        if new_patty_cost != 0:
            return set_count, new_patty_cost
        return (set_count, 99)

@app.route('/patty', methods=["GET", "POST"])
@app.route('/Wrap', methods=["GET", "POST"])
def patty():
    ''' Bun selection
    '''
    main = {
        "type": "Main"
    }
    prices_main = {}
    prices = {
        "main": prices_main, 
        "sides": {}
    }
    patty_count = {
        "vc": 0, # Vegetarian Count
        "bc": 0, # Beef Count
        "cc": 0 # Chicken Count
    }

    burger_properties = {}
    if request.args.get('bun'):
        # The user has chosen a Burger
        bun_type = request.args.get('bun')
        bun_count = request.args.get('count')
        burger_properties['bun'] = bun_type
        burger_properties['count'] = bun_count
        main['name'] = 'Burger'
        burger = Burger()
        prices["main"]["Burger"] = burger.price
        prices["main"][bun_type + ' Bun'] = 0
    else:
        # The user has chosen a Wrap
        #w = Wrap()
        main['name'] = 'Wrap'
        wrap = Wrap()
        prices["main"]["Wrap"] = wrap.price

    if request.args.get('vc'):
        patty = Topping("Vegetarian Patty")
        patty_count['vc'] = int(request.args.get('vc'))
        action = request.args.get('va')
        if action:
            action = int(action)
            if action + patty_count['vc'] != 3:
                patty_count['vc'] += 2-int(request.args.get('va'))
        new_patty_cost = patty.price * patty_count['vc']
        if new_patty_cost != 0:
            prices["main"][patty.name] = new_patty_cost
    '''print(update_patty_count('vc', request.args.get('vc'), request.args.get('va')))
    a, cost = update_patty_count('vc', request.args.get('vc'), request.args.get('va'))
    patty_count['vc'] = a
    if cost is not None:
        prices["main"]['Vegetarian Patty'] = cost'''


    if request.args.get('cc'):
        patty = Topping("Chicken Patty")
        patty_count['cc'] = int(request.args.get('cc'))
        action = request.args.get('ca')
        if action:
            action = int(action)
            if action + patty_count['cc'] != 3:
                patty_count['cc'] += 2-int(request.args.get('ca'))
        new_patty_cost = patty.price * patty_count['cc']
        if new_patty_cost != 0:
            prices["main"][patty.name] = new_patty_cost
    if request.args.get('bc'):
        patty = Topping("Beef Patty")
        patty_count['bc'] = int(request.args.get('bc'))
        action = request.args.get('ba')
        if action:
            action = int(action)
            if action + patty_count['bc'] != 3:
                patty_count['bc'] += 2-int(request.args.get('ba'))
        new_patty_cost = patty.price * patty_count['bc']
        if new_patty_cost != 0:
            prices["main"][patty.name] = new_patty_cost


    
    return render_template('patty.html', prices=prices, patty_count=patty_count, **burger_properties)

