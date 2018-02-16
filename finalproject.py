from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# Create session and connect to DB ##
app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenus.db') #create instance engine for create_engine database
Base.metadata.bind = engine	# call Base Class
DBSession = sessionmaker(bind=engine)	# bind engine with sessionmaker
session = DBSession() # isntance session with DBSession()

@app.route('/')
@app.route('/restaurants')
def listRestaurant():
	rest = session.query(Restaurant).all()
	list_ = session.query(Restaurant).all()
	rest_name = []

	for name in list_:
		rest_name.append(str(name))

	output = ""
	output += "<html><head><style><link rel=stylesheet type=text/css href='{{ url_for('static', filename='style.css') }}'></style></head><body>"
	output += "<div style='text-align:center;color:black;'><h1>Restaurant List</h1></div>"
	output += "<h2><a href='/restaurants/1/menu'style='color:black;'>1. %s</a>" % rest_name[0]
	output += "<h2><a href='/restaurants/2/menu'style='color:black;'>2. %s</a>" % rest_name[1]
	output += "<h2><a href='/restaurants/3/menu'style='color:black;'>3. %s</a>" % rest_name[2]
	output += "<h2><a href='/restaurants/4/menu'style='color:black;'>4. %s</a>" % rest_name[3]
	output += "<h2><a href='/restaurants/5/menu'style='color:black;'>5. %s</a>" % rest_name[4]
	output += "<h2><a href='/restaurants/6/menu'style='color:black;'>6. %s</a>" % rest_name[5]
	output += "<h2><a href='/restaurants/7/menu'style='color:black;'>7. %s</a>" % rest_name[6]
	output += "<h2><a href='/restaurants/8/menu'style='color:black;'>8. %s</a>" % rest_name[7]
	output += "<h2><a href='/restaurants/9/menu'style='color:black;'>9. %s</a>" % rest_name[8]
	output += "</body></html>"
	return output

@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return render_template('home.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(
			name=request.form['name'],restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash("New menu item created!!")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('new.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id,menu_id):
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('edit.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id,menu_id):
	deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template('delete.html', restaurant_id=restaurant_id, menu_id=menu_id, item=deleteItem)

@app.route('/restaurants/<int:restaurant_id>/menu/json')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem=menuItem.serialize)

@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0',port = 5000)