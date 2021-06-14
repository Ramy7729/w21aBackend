# Collaborated with Liz for this assignment.

import dbconnect
from flask import Flask, request, Response
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# This decorator handles the get request.
@app.get("/candy")
def get_candy():
    # Creating a db connection and cursor.
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # Initiaize variable to None. Will be used in a conditional check.
    candy_rows = None
    
    try:
        # Executing the select statement to fetch data from a table with the specified columns.
        cursor.execute("SELECT name, description, price, image_url, id FROM candy")
        candy_rows = cursor.fetchall()

    except:
        # Handling error when a connection to the db can't be made.
        print("Error in running db query")
        return Response("Error in running db query", mimetype="plain/text", status=500)
    # Closing the cursor and db connection.
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # Conditional statement to ensure that data was fetched without any errors.
    # If error occurs a response is sent back to the user.
    if(candy_rows == None):
        return Response("Failed to get candy from DB", mimetype="test/plain, status=500")
    
    response_body = json.dumps(candy_rows, default=str)
    return Response(response_body, mimetype="application/json", status=200)

# This decorater handles the post request.
@app.post("/candy")
def add_candy():
    try:  
        # Requested data sent from the user.
        candy_name = request.json['name']
        candy_description = request.json['description']
        candy_price = int(request.json['price'])
        candy_image = request.json['image']
    except:
        print("Data Error")
        return Response("Data Error", mimetype="plain/text", status=400)
    # Conditionals to check for required fields.
    # If at leat one required field is None, an error occurs.
    if(candy_name == None or candy_description == None or candy_image == None or candy_price == None):
        return Response("Data Error", mimetype="plain/text", status=400)
    # Creating a db connection and cursor.
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # Initializing variable for item id.
    new_id = -1
    
    try:
        # Executes an insert statement to add a new candy into table.
        cursor.execute("INSERT INTO candy (name, description, price, image_url) VALUES (?,?,?,?)", [candy_name, candy_description, candy_price, candy_image])
        conn.commit()
        new_id = cursor.lastrowid
      
    except:
        print("Error in running db query")
        return Response("Error in running db query", mimetype="plain/text", status=500)
    # Closing the cursor and db connection.
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # Conditional that checks for a valid item id, if there isn't one an error occurs.
    if(new_id == -1):
       return Response("Insert into DB failed", mimetype="text/plain", status=500)
    else:
        response_body = json.dumps([candy_name, candy_description, candy_price, candy_image, new_id], default=str)
        return Response(response_body, mimetype="application/json", status=201)

# This decorater handles a delete request.
@app.delete("/candy")
def delete_candy():
    try:   
        # Requested data sent from the user.
        candy_id = int(request.json['id'])
        
    except:
        print("Data error")
        return Response("Data error", mimetype="plain/text", status=500)
       
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    row_count = 0
    
    try:
        # Executes a delete statment to delete a candy based on its id.
        cursor.execute("DELETE FROM candy WHERE id=?", [candy_id,])
         # Using the rowcount property to determine the number of rows.
        row_count = cursor.rowcount
        conn.commit()
    
    except:
        print("Error in running db query")
        return Response("Error in running db query", mimetype="text/plain", status=400)
    
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # Conditional to check for a failed delete request.
    if(row_count == 0):
        return Response("Failed to delete candy!", mimetype="text/plain", status=400)
    
    return Response("Candy deleted!", mimetype="text/plain", status=200)

# This decorater handles a delete request.
@app.patch("/candy")
def update_candy():
    try:
        # Requested data sent from the user.
        candy_name = request.json['name']
        candy_description = request.json['description']
        candy_price = int(request.json['price'])
        candy_image = request.json['image']
        candy_id = int(request.json['id'])
    # Handling error for user input.  
    except:
        print("Data error")
        return Response("Data error", mimetype="text/plain", status=400)
    
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    row_count = 0
    updated_candy = None
    
    try:
        # Executes the update statement to edit candy information based on the specified columns.
        cursor.execute("UPDATE candy SET name =?, description =?, price =?, image_url =? WHERE id=?", [candy_name, candy_description, candy_price, candy_image, candy_id])
        conn.commit()
        # Using the rowcount property to determine the number of rows.
        row_count = cursor.rowcount
        # Executes the select statement that fetches candy data after the update is done.
        cursor.execute("SELECT name, description, price, image_url, id FROM candy WHERE id=?", [candy_id,])
        updated_candy = cursor.fetchall()

    except:
        print("Error in running db query")
        return Response("Error in running db query", mimetype="text/plain", status=400)
    
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # Conditional that checks for a success in the update request.
    if(row_count ==1 and updated_candy !=None):
        response_body = json.dumps(updated_candy, default=str)
        return Response(response_body, mimetype="application/json", status=200)
    else:
        return Response("Failed to update candy", mimetype="text/plain", status=400)

# Starts the application flask server. 
# An argument is passed that enables debugging mode to be turned on.
app.run(debug=True)
