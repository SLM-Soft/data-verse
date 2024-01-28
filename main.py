# -*- coding: utf-8 -*-
import json
import requests

def read_and_parse_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")
    except PermissionError:
        print(f"Permission denied to read the file {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None


def send_to_dataverse(entry):
    timestamp = entry.get("Timestamp")
    source_type = entry.get("5. Вид джерела / Type of the source")
    language = entry.get("6. Мова джерела / Source language")
    content = entry.get("18. Conten of post")
    keywords = entry.get("14. Ключові слова / Key words")
    web_link = entry.get("9. Інтернет посилання (для онлайн джерела) / Web link (for online source)", "")
    date_of_source_submission = entry.get("15. Дата подання джерела / Date of source submission",  "")

    title = ' '.join(content.split()[:6])
    print(f"title: {title}")
    print(f"Timestamp: {timestamp}")
    print(f"Source Type: {source_type}")
    print(f"Language: {language}")
    print("Content:")
    print(content)
    print(f"Keywords: {keywords}")
    print(f"Web Link: {web_link}")
    print(f"Date of source submission: {date_of_source_submission}")
    print("\n" + "-" * 50 + "\n")

    url = 'https://dataverse.netzwerk-erinnerung.de/api/dataverses/discourses_of_war/datasets'
    api_key = ''

    headers = {
        'X-Dataverse-key': api_key,
        'Content-type': 'application/json'
    }

    data = {
      "datasetVersion": {
        "license": {
          "name": "CC0 1.0",
          "uri": "http://creativecommons.org/publicdomain/zero/1.0"
        },
        "protocol":"doi",
        "authority":"10.502",
        "identifier":"ZZ7/MOSEISLEYDB94",
        "metadataBlocks": {
          "citation": {
              "fields": [
                            {
                                "typeName": "title",
                                "multiple": False,
                                "typeClass": "primitive",
                                "value": title
                            },
                            {
                                "typeName": "author",
                                "multiple": True,
                                "typeClass": "compound",
                                "value": [
                                    {
                                        "authorName": {
                                            "typeName": "authorName",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": "Unknown"
                                        },
                                        "authorAffiliation": {
                                            "typeName": "authorAffiliation",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": "Dataverse.org"
                                        }
                                    }
                                ]
                            },
                            {
                                "typeName": "datasetContact",
                                "multiple": True,
                                "typeClass": "compound",
                                "value": [
                                    {
                                        "datasetContactName": {
                                            "typeName": "datasetContactName",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": "Unknown"
                                        },
                                        "datasetContactAffiliation": {
                                            "typeName": "datasetContactAffiliation",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": "Dataverse.org"
                                        },
                                        "datasetContactEmail": {
                                            "typeName": "datasetContactEmail",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": "dataverse@mailinator.com"
                                        }
                                    }
                                ]
                            },
                            {
                                "typeName": "dsDescription",
                                "multiple": True,
                                "typeClass": "compound",
                                "value": [
                                    {
                                        "dsDescriptionValue": {
                                            "typeName": "dsDescriptionValue",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": content
                                        },
                                        "dsDescriptionDate": {
                                            "typeName": "dsDescriptionDate",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": date_of_source_submission
                                        }
                                    }
                                ]
                            },
                            {
                                "typeName": "subject",
                                "multiple": True,
                                "typeClass": "controlledVocabulary",
                                "value": [
                                    "Law",
                                    "Social Sciences",
                                    "Other"
                                ]
                            },
                            {
                                "typeName": "keyword",
                                "multiple": True,
                                "typeClass": "compound",
                                "value": [
                                    {
                                        "keywordValue": {
                                            "typeName": "keywordValue",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": keywords
                                        }
                                    }
                                ]
                            },
                            {
                                "typeName": "publication",
                                "multiple": True,
                                "typeClass": "compound",
                                "value": [
                                    {
                                        "publicationURL": {
                                            "typeName": "publicationURL",
                                            "multiple": False,
                                            "typeClass": "primitive",
                                            "value": web_link
                                        }
                                    }
                                ]
                            },
                            {
                                "typeName": "depositor",
                                "multiple": False,
                                "typeClass": "primitive",
                                "value": "Admin, Dataverse"
                            },
                            {
                                "typeName": "dateOfDeposit",
                                "multiple": False,
                                "typeClass": "primitive",
                                "value": timestamp.split()[0]
                            }
                        ],
            "displayName": "Citation Metadata"
          }
        }
      }
    }

    # Convert the dictionary to JSON format
    data_json = json.dumps(data)

    # response = requests.post(url, headers=headers, json=data)
    response = requests.post(url, headers=headers, data=data_json)
    if response.status_code == 201:
        print("Successfully sent to API:", response.json())
    else:
        print("Error sending to API:", response.status_code, response.text)

def extract_data(parsed_json):
    for entry in parsed_json[:10]:
        send_to_dataverse(entry)


# Example usage
file_path = './files/database_part_10.json'
parsed_data = read_and_parse_json(file_path)

if parsed_data is not None:
    extract_data(parsed_data)
