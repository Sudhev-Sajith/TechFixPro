import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables (Create a .env file locally with these)
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_anon_key
load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Admin Credentials (Set these in .env for production)
# REPLACED BY SUPABASE AUTH

# Initialize Supabase
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Graceful fallback if keys aren't set (for demo purposes)
supabase: Client = None
if url and key:
    supabase = create_client(url, key)
else:
    print("WARNING: Supabase URL or Key not found. App will error on database calls.")

# --- Authentication Decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("Please log in to access the dashboard.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    """Customer-facing ticket tracking (Now the Homepage)."""
    ticket = None
    if request.method == 'POST':
        ticket_id = request.form.get('ticket_id')
        if ticket_id:
            try:
                # Assuming ID is an integer. Handle generic search if needed.
                response = supabase.table('repairs').select("*").eq('id', ticket_id).execute()
                if response.data:
                    ticket = response.data[0]
                else:
                    flash("Ticket not found. Please check the ID.", "error")
            except Exception as e:
                flash(f"Error tracking ticket: {e}", "error")
    
    return render_template('tracking.html', ticket=ticket)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Staff login page using Supabase Auth."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            response = supabase.auth.sign_in_with_password({ "email": email, "password": password })
            if response.user:
                # Store minimal user info in session
                session['user'] = {
                    'id': response.user.id,
                    'email': response.user.email
                }
                flash("Welcome back!", "success")
                return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f"Login failed: {str(e)}", "error")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    try:
        supabase.auth.sign_out()
    except:
        pass
    session.pop('user', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Fetches all repair tickets and displays the backend dashboard."""
    try:
        response = supabase.table('repairs').select("*").order('id', desc=True).execute()
        tickets = response.data
    except Exception as e:
        print(f"Error fetching data: {e}")
        tickets = []
        flash("Error connecting to database. Check credentials.", "error")
    
    return render_template('dashboard.html', tickets=tickets)

@app.route('/add', methods=['POST'])
@login_required
def add_ticket():
    """Creates a new repair ticket."""
    try:
        data = {
            'customer_name': request.form['customer_name'],
            'customer_email': request.form['customer_email'],
            'device_model': request.form['device_model'],
            'serial_number': request.form['serial_number'],
            'issue_description': request.form['issue_description'],
            'status': 'Received',
            'estimated_cost': 0.00
        }
        supabase.table('repairs').insert(data).execute()
        flash("Ticket created successfully!", "success")
    except Exception as e:
        flash(f"Error creating ticket: {e}", "error")
    
    return redirect(url_for('dashboard'))

@app.route('/update/<int:id>', methods=['POST'])
@login_required
def update_ticket(id):
    """Updates the status and cost of a ticket."""
    try:
        data = {
            'status': request.form['status'],
            'estimated_cost': request.form['estimated_cost']
        }
        supabase.table('repairs').update(data).eq('id', id).execute()
        flash("Ticket updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating ticket: {e}", "error")

    return redirect(url_for('dashboard'))

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_ticket(id):
    """Deletes a ticket."""
    try:
        supabase.table('repairs').delete().eq('id', id).execute()
        flash("Ticket deleted.", "success")
    except Exception as e:
        flash(f"Error deleting ticket: {e}", "error")
        
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)