0. Before running any script, make sure you have virtual environment prepared and activated (see [Python Virtual Environment](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)) and required packages installed (use `python3 -m pip install -r requirements.txt` command)
1. To run the application, run this `python src\run.py` in your terminal. (replace `\` with `/` if you're not using Windows)
2. Application config variables has to be defined in `src\inz\config.py.example` and file itself has to be renamed to `config.py`.
3. For now: `/ocr/{file-name}` endpoint runs ocr_service using photo from `{root_repository_folder}\static\receipts` directory (tested with *.jpg and *.png formats).
4. To run ocr_service directly, use `python src\run_ocr.py` command