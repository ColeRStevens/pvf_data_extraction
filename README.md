# PVF Volleyball Extraction

This program uses the [selenium](https://selenium-python.readthedocs.io/installation.html), [pandas](https://pandas.pydata.org/docs/getting_started/install.html), and [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/#installing-beautiful-soup) python libraries to extract the html and data from the Omaha Supernovas and other teams from the [Pro Volleyball Federation](https://provolleyball.com/) team websites.

### Installation and Usage

You can install these libraries with the following command

```
pip install -r requirements.txt
```

After installation, navigate to a place in your file system that you want the files in and run the following ...

```
cd ./<YourFolder>/
```

Then clone the repo with the following ...

```
git clone "https://github.com/ColeRStevens/pvf_data_extraction/"
```

Finally run this last command ...

```
python main.py
```

All that's left is to check your data.csv file in the ./data folder!

### Sorting

The program can sort the data according to the columns. Check the comments on [sort_data()](https://github.com/ColeRStevens/pvf_data_extraction/blob/main/main.py#L102) for details.

### Lessons Learned

This project taught me how to use powerful data extraction and automation libraries such as selenium, pandas and BeautifulSoup4. I had to learn how to get around dynamic tables, which is why I use selenium instead of [requests](https://requests.readthedocs.io/en/latest/user/install/) or BeautifulSoup. Not only did I learn valuable skills, I got to use them on data that relates to something I support.
