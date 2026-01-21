# TechFixPro

TechFixPro is a comprehensive repair ticket tracking system built with **Flask** and **Supabase**. It allows customers to track their device repair status and provides a secure dashboard for staff to manage repair tickets.

## Features

-   **Customer Tracking**: Customers can check the status of their repair using their Ticket ID.
-   **Admin Dashboard**: Secure login for staff to view, add, update, and delete tickets.
-   **Supabase Integration**: robust backend for database (PostgreSQL) and authentication.
-   **Responsive Design**: Built with Flask templates for a clean user interface.

## Tech Stack

-   **Backend**: Python, Flask
-   **Database & Auth**: Supabase
-   **Frontend**: HTML, CSS (via Templates)
-   **Deployment**: Ready for Vercel

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Sudhev-Sajith/TechFixPro.git
    cd TechFixPro
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your Supabase credentials:
    ```env
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_anon_key
    ```

4.  **Run the application:**
    ```bash
    python app.py
    ```
    Visit `http://127.0.0.1:5000` in your browser.

## Deployment

### Vercel
This project includes a `vercel.json` for easy deployment.
1.  Import the repo into Vercel.
2.  Add `SUPABASE_URL` and `SUPABASE_KEY` to the **Environment Variables** in Vercel settings.
3.  Deploy!

## License
MIT