# XML Validator

XML Validator is a Python tool for validating XML documents against predefined conditions using XSLT transformations. This tool allows you to define validation rules in a separate XML file and apply them to XML documents, generating validation results for each specified condition.

## Features:
- Dynamic Validation: Define validation conditions using XSLT templates, allowing for dynamic validation rules.
- Configurability: Easily configure validation conditions in a separate XML file.
- Result Reporting: Get validation results for each condition in a structured format.
- Cleanup: Automatically cleanup validation files after processing.

## Requirements:
- Python 3.x
- lxml library

## Usage:
- Installation: Install the required dependencies by running pip install lxml.
- Configuration: Define validation conditions in the validator.xml file. Each validation condition should be specified within an <xsl:when> element in the XSLT template.
- Execution: Run the script using Python, providing the paths to the XML document to be validated (document.xml) and the validation rules file (validator.xml).
```
python main.py
```

## Example:
```
from XMLValidator import XMLValidator

if __name__ == "__main__":
    validator = XMLValidator()
    results = validator.process(document_path="document.xml", validations_document_path="validator.xml")
    print(results)
```
