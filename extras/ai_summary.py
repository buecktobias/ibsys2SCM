import os

from auto_codebase_documenter.AutoCodebaseDocumenter import AutoCodebaseDocumenter

if __name__ == '__main__':
    openai_api_key = os.getenv("OPENAI_KEY")  # get OPENAI_KEY value from .env file{}
    documenter = AutoCodebaseDocumenter(openai_api_key)
    documenter.process_all_files()
