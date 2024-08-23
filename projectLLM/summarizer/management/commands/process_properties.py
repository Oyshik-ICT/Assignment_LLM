import requests
from django.core.management.base import BaseCommand
from django.db import connections
from summarizer.models import PropertySummary
from requests.exceptions import RequestException


import json


def get_ollama_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma2:2b", "prompt": prompt},
            stream=True,
        )

        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                try:
                    # Attempt to parse each line as JSON
                    json_line = line.decode("utf-8").strip()
                    json_data = json.loads(json_line)

                    # Check if the response is complete
                    if json_data.get("done", False):
                        full_response += json_data.get("response", "")
                        break
                    else:
                        full_response += json_data.get("response", "")
                except ValueError as e:
                    print(f"Error decoding JSON: {e}")
                    continue

        print(full_response)
        return full_response if full_response else None

    except RequestException as e:
        print(f"Error connecting to Ollama API: {e}")
        return None


class Command(BaseCommand):
    help = "Process properties from datashift and update summaries"

    def handle(self, *args, **options):
        # Connect to the datashift database
        with connections["datashift"].cursor() as cursor:
            cursor.execute(
                'SELECT property_id, title, description FROM "MyApp_property"'
            )
            properties = cursor.fetchall()

            for property_id, title, description in properties:
                # Prepare prompt for rewriting
                rewrite_prompt = (
                    f"Rewrite the following property details:\n"
                    f"Title: {title}\n"
                    f"Description: {description}"
                )
                # Call Ollama API to rewrite title and description
                rewritten_text = get_ollama_response(rewrite_prompt)
                if rewritten_text is None:
                    print(f"Skipping property {property_id} due to API error")
                    continue

                new_title, new_description = rewritten_text.split(
                    "\n", 1
                )  # Adjust based on response format

                # Update the datashift database
                cursor.execute(
                    """
                    UPDATE "MyApp_property"
                    SET title = %s, description = %s
                    WHERE property_id = %s
                """,
                    [new_title, new_description, property_id],
                )

                # Prepare prompt for generating summary
                cursor.execute(
                    """
                    SELECT title, description,
                        (
                            SELECT STRING_AGG(name, ', ')
                            FROM "MyApp_amenity"
                            WHERE id IN (
                                SELECT amenity_id
                                FROM "MyApp_property_amenities"
                                WHERE property_id = %s
                            )
                        ) AS amenities
                    FROM "MyApp_property"
                    WHERE property_id = %s
                    """,
                    [property_id, property_id],
                )

                row = cursor.fetchone()
                title, description, amenities = row
                summary_prompt = (
                    f"Generate a summary using the following details:\n"
                    f"Title: {title}\n"
                    f"Description: {description}\n"
                    f"Amenities: {amenities}"
                )
                # Call Ollama API to generate summary
                summary_text = get_ollama_response(summary_prompt)
                if summary_text is None:
                    print(
                        f"Skipping summary for property {property_id} "
                        "due to API error"
                    )
                    continue

                # Save summary to new database
                PropertySummary.objects.create(
                    property_id=property_id, summary=summary_text
                )

        print("Processing completed.")
