# projectLLM

projectLLM is a Django-based project that processes property data from another Django project (Datashift), rewrites property titles and descriptions using the Gemma 2B language model, generates summaries, and stores the results.

## Project Overview

This project consists of a custom CLI command that:

1. Fetches property data from the Datashift project's database.
2. Rewrites the title and description for each property using the Gemma 2B model.
3. Updates the Datashift database with the rewritten content.
4. Generates a summary for each property using the updated information and amenities.
5. Stores the property ID and summary in the projectLLM database.

## Prerequisites

- Python 3.8+
- Django 3.2+
- PostgreSQL 12+
- Ollama (with the Gemma 2B model installed)

## Setup Instructions

1. Clone the repository:

   ```
   git clone https://github.com/Oyshik-ICT/Assignment_LLM.git
   cd Assignment_LLM
   ```

2. Create a virtual environment and activate it:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL databases:

   - Ensure you have two PostgreSQL databases set up: one for projectLLM and one for Datashift.
   - Create or update the `.pg_service.conf` file in your home directory with the following structure:

     ```
     [my_service]
     host=
     user=
     dbname=
     port=
     password=

     [my_llm_service]
     host=
     user=
     dbname=
     port=
     password=
     ```

   - Fill in the appropriate details for each service:
     - `[my_service]` should contain the connection details for the Datashift project database.
     - `[my_llm_service]` should contain the connection details for the projectLLM database.

5. Apply migrations:

   ```
   python manage.py migrate
   ```

6. Ensure Ollama is installed and the Gemma 2B model is available:
   ```
   ollama pull gemma2:2b
   ```

## Running the Project

1. Start the Ollama server:

   ```
   ollama serve
   ```

2. In a new terminal, navigate to the project directory and activate the virtual environment.

3. Run the custom management command:
   ```
   python manage.py process_properties
   ```

This command will process the properties from the Datashift database, rewrite titles and descriptions, generate summaries, and store the results in the projectLLM database.

## Project Structure

- `summarizer/models.py`: Contains the `PropertySummary` model definition.
- `summarizer/management/commands/process_properties.py`: Custom management command for processing properties.
- `projectLLM/settings.py`: Project settings, including database configurations.

## Notes

- Ensure that the Datashift project database is accessible and contains the required `MyApp_property` and `MyApp_amenity` tables.
- The project uses the `gemma2:2b` model through Ollama. Make sure Ollama is installed and the model is available.
- You'll need to configure the `.pg_service.conf` file with the appropriate database details for both the Datashift and projectLLM databases.
- If you encounter any issues with database connections, double-check the PostgreSQL service configurations and ensure the databases are created and accessible.

## Troubleshooting

If you encounter any issues:

1. Ensure all dependencies are installed correctly.
2. Check that the PostgreSQL services are properly configured and running.
3. Verify that Ollama is running and the Gemma 2B model is available.
4. Review the console output for any error messages during the execution of the `process_properties` command.
