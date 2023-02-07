import csv

from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


CSV_DATA = {Category: 'category.csv',
            Comment: 'comment.csv',
            GenreTitle: 'genre_title.csv',
            Genre: 'genre.csv',
            Review: 'review.csv',
            Title: 'titles.csv',
            User: 'users.csv'}


class Command(BaseCommand):
    help = "Loads data from csv files"

    def handle(self, *args, **kwargs):
        for model, csv_file in CSV_DATA:
            if model.objects.exists():
                print('data already loaded...exiting.')
                print(ALREDY_LOADED_ERROR_MESSAGE)
                return

        with open('category.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                category = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                category.save()

        with open('comments.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                comment = Comment(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=row['author'],
                    pub_date=row['pub_date'],
                )
                comment.save()

        with open('genre_title.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                genretitle = GenreTitle(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id'],
                )
                genretitle.save()

        with open('genre.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                genre = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )
                genre.save()

        with open('review.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                review = Review(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date'],
                )
                review.save()

        with open('titles.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                title = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=row['category'],
                )
                title.save()

        with open('users.csv', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                user = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
                user.save()
