from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__, template_folder='.')
app.secret_key = 'your_secret_key'

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="@Cactus90#",  # Change if needed
        database="library_db"
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        contact = request.form['contact']
        book_name = request.form['book_name']
        author = request.form['author']
        loan_date = request.form['loan_date']
        return_date = request.form.get('return_date', 'N/A')  # Default to 'N/A' if not provided

        connection = connect_db()
        cursor = connection.cursor()

        # Insert new record without unique constraint on student_id or book_name
        cursor.execute("""
            INSERT INTO libraryrecords (student_id, name, contact, book_name, author, loan_date, return_date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (student_id, name, contact, book_name, author, loan_date, return_date))

        connection.commit()
        cursor.close()
        connection.close()

        flash("Record added successfully!", "success")
        return redirect(url_for('index'))

    return render_template('id.html')


@app.route('/history', methods=['GET', 'POST'])
def history():
    results = None
    if request.method == 'POST':
        search_query = request.form['search_query']

        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT student_id, name, contact, book_name, loan_date, 
                   IF(return_date IS NULL, 'N/A', return_date) AS return_date
            FROM libraryrecords
            WHERE student_id = %s OR name = %s OR contact = %s
        """, (search_query, search_query, search_query))
        
        results = cursor.fetchall()
        cursor.close()
        connection.close()

    return render_template('history.html', results=results)


@app.route('/update_return_date', methods=['POST'])
def update_return_date():
    student_id = request.form['student_id']
    book_name = request.form['book_name']
    return_date = request.form['return_date']

    connection = connect_db()
    cursor = connection.cursor()
    
    cursor.execute("""
        UPDATE libraryrecords 
        SET return_date = %s 
        WHERE student_id = %s AND book_name = %s
    """, (return_date, student_id, book_name))

    connection.commit()
    cursor.close()
    connection.close()

    flash("Return date updated successfully!", "success")
    return redirect(url_for('history'))


if __name__ == "__main__":
    app.run(debug=True)
