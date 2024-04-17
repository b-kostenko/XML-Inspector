import re
import os
from typing import List

from lxml import etree


class XMLValidator:

    def __init__(self):
        self.folder_name = "validators"
        self.create_folder()
        self.results = {}

    def create_folder(self):
        if not os.path.exists(self.folder_name):
            try:
                os.makedirs(self.folder_name)
                print(f"Folder '{self.folder_name}' created successfully.")
            except OSError as e:
                print(f"Failed to create folder '{self.folder_name}'. Error: {e}")
        else:
            print(f"Folder '{self.folder_name}' already exists.")

    def cleanup_folder(self):
        files = os.listdir(self.folder_name)
        for file in files:
            os.remove(os.path.join(self.folder_name, file))
        print(f"Contents of folder '{self.folder_name}' have been cleaned up.")

    def create_new_validator_file(self, body: tuple):
        payload = f"""
        <?xml version='1.0'?>
            <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
                <xsl:template match="/">
                    <xsl:choose>
                        <xsl:when test="{body[1]}">
                        <result>true</result>
                        </xsl:when>
                        <xsl:otherwise>
                            <result>false</result>
                        </xsl:otherwise>
                    </xsl:choose>
                </xsl:template>
            </xsl:stylesheet>
        """
        with open(f"{self.folder_name}/validator_{body[0]}.xml", "w", encoding='utf-8') as f:
            f.write(payload.strip())

    @staticmethod
    def get_field_name(field):
        regex_pattern = r"field\[@name='([^']+)'\]"
        match = re.search(regex_pattern, field)
        if match:
            return match.group(1)
        else:
            raise ValueError("Failed to extract field name.")

    @staticmethod
    def extract_boolean_result(input_string: str):
        regex_pattern = r'<result>(true|false)</result>'
        match = re.search(regex_pattern, input_string)
        if match:
            return match.group(1)
        else:
            raise ValueError("Failed to extract boolean result.")

    def extract_validation_cases(self, validations_document) -> List[tuple]:
        tree = self.parse_xml(validations_document)
        root = tree.getroot()
        validation_cases = []
        for index, case in enumerate(root.findall('.//xsl:when', namespaces={'xsl': 'http://www.w3.org/1999/XSL/Transform'}), start=1):
            test_condition = case.get('test')
            field_name = self.get_field_name(test_condition)
            validation_cases.append((index, test_condition, field_name))
        return validation_cases

    @staticmethod
    def parse_xml(file):
        return etree.parse(file)

    def process(self, document_path: str, validations_document_path: str):
        document = self.parse_xml(document_path)

        validation_cases = self.extract_validation_cases(validations_document=validations_document_path)

        for index, test_condition, field_name in validation_cases:
            self.create_new_validator_file(body=(index, test_condition))

            transform = etree.XSLT(self.parse_xml(f"{self.folder_name}/validator_{index}.xml"))
            result = transform(document)

            self.results[field_name] = self.extract_boolean_result(str(result))
        self.cleanup_folder()
        return self.results


if __name__ == "__main__":
    vl = XMLValidator()
    vl.process(document_path="document.xml", validations_document_path="validator.xml")
