import os.path
def file_exists(file_name):
    """Verify that the file exists.

    Args:
        file_name (str): name of the file

    Returns:
        boolean: returns True if the file exists and False otherwise.
    """
    # Remove pass and fill in your code here
    return os.path.isfile(file_name)
        
def main():
    print(file_exists("sfadsf"))

if __name__ == '__main__':
    main()