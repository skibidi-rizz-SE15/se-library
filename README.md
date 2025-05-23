
# SE-Library

SE-Library is a web-based platform that enables community members to register books they own and make them available for borrowing. Borrowers can request books, and owners have the ability to accept or decline these requests. The system ensures fair allocation of books by managing handovers through a Smart Locker.

## Features

- **Book Registration**: Owners can list books they are willing to lend.
- **Borrowing Requests**: Users can request to borrow available books.
- **Request Management**: Owners can approve or reject borrowing requests.
- **Smart Locker Integration**: Facilitates secure and fair book handovers.

## Technologies Used

- **Framework**: [Reflex](https://reflex.dev/) – A pure Python web framework for building full-stack applications.
- **Database**: PostgreSQL – A powerful, open-source relational database system.

## Getting Started

To set up the project locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/skibidi-rizz-SE15/se-library.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd se-library
   ```

3. **Set Up the Environment**:

   Ensure you have Python 3.10 or higher installed. It's recommended to use a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the Database**:

   Ensure PostgreSQL is installed and running. Create a new database:

   ```sql
   CREATE DATABASE se_library;
   ```

   Update the database connection settings in the project's configuration file as needed.

6. **Apply Migrations**:

   Please refer to the reflex [documentation](https://reflex.dev/docs/database/overview/).

7. **Run the Application**:

   ```bash
   reflex run
   ```

   Open your browser and go to `http://localhost:3000`.

## Contributing

We welcome contributions! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).
