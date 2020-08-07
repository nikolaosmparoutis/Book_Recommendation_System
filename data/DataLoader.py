# data: 278,858 users |  1,149,780 ratings | 271,379 books.
# http://www2.informatik.uni-freiburg.de/~cziegler/BX/
import os
import pandas as pd
from data.DataClean import DataClean


class DataLoader:
    path_to_file = None
    directory_to_extract_to = None

    def __init__(self):
        self.data = pd.DataFrame()

    @staticmethod
    def read_paths(absolute_path):
        import yaml
        with open(absolute_path, 'r') as yml_file:
            cfg = yaml.load(yml_file, Loader=yaml.FullLoader)
            DataLoader.path_to_file = cfg["path_to_file"]
            DataLoader.directory_to_extract_to = cfg["directory_to_extract_to"]

    @staticmethod
    def unzip_dataset():
        import zipfile
        with zipfile.ZipFile(DataLoader.path_to_file, 'r') as zip_ref:
            zip_ref.extractall(DataLoader.directory_to_extract_to)
        print("The folder unzipped.")
        return

    @staticmethod
    def check_zip_and_csv():
        zip_extension = os.path.splitext(DataLoader.path_to_file)[1]
        if zip_extension != ".zip":
            print("A .zip file does not exist in the given path.")
            return FileNotFoundError
        else:
            DataLoader.unzip_dataset()
            for files in os.listdir(DataLoader.directory_to_extract_to):
                if os.path.splitext(files)[1] != ".csv":
                    print("The file " + files + " is not .csv. This directory accept only .csv datasets")
                    return FileNotFoundError
                else:
                    break
            DataLoader.remove_zip_folder()
            print("The check passed, all datasets are .csv")
            return

    @staticmethod
    def remove_zip_folder():
        os.remove(DataLoader.path_to_file)
        print("The redundant folder .zip removed.")

    def read_data(self, filename):
        try:
            self.data = pd.read_csv(DataLoader.directory_to_extract_to + filename,
                                    sep=";", encoding='latin-1', error_bad_lines=False, warn_bad_lines=False,
                                    low_memory=False, memory_map=True, nrows=50
                                    )
        except:
            raise TypeError("Wrong file name.")
        return self.data


paths = "/home/nikoscf/PycharmProjects/BookRecommendation/configurations/paths.yml"
load_begin = DataLoader()
load_begin.read_paths(paths)

# execute one time to get the zip if is .zip, unzip, check for .csv and remove the redundant zip folder
# load_begin.check_zip_and_csv()


books = load_begin.read_data("BX-Books.csv")
users = load_begin.read_data("BX-Users.csv")
ratings = load_begin.read_data("BX-Book-Ratings.csv")


to_drop_columns = ['Image-URL-S', 'Image-URL-M', 'Image-URL-L']
numeric_col_to_nan = ["Year-Of-Publication"]
data_books = DataClean(books)
data_books.execute_pipeline_cleaning(to_drop_columns, numeric_col_to_nan)


to_drop_columns = []
numeric_col_to_nan = ["User-ID", "ISBN", "Book-Rating"]
data_ratings = DataClean(ratings)
data_ratings.execute_pipeline_cleaning(to_drop_columns, numeric_col_to_nan)


to_drop_columns = []
numeric_col_to_nan = ["User-ID", "Age"]
data_users = DataClean(users)
data_users.execute_pipeline_cleaning(to_drop_columns, numeric_col_to_nan)