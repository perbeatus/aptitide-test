"""Module with MoviesAudit class"""
import os
import psycopg2
import consts
import exceptions as exc


class MoviesAudit():
    """Simple class for auditing movies DB"""

    def __init__(self):
        self.con_params = self.__get_con_params()
        self.movies_tb = 'movies'
        self.links_tb = 'links'
        self.ratings_tb = 'ratings'
        self.tags_tb = 'tags'
        self.results = {}
        self.result_file = '/movies-audit-result/audit-result.md'

    def __get_con_params(self):
        res = {
            'user': consts.DB_USER,
            'dbname': consts.DB_NAME,
            'password': os.environ.get(consts.DB_PASSWORD_ENV)
        }
        if res['password'] is None:
            raise exc.NoPassException('PostgreSQL DB password not provided. '
                                      f'Please pass it in {consts.DB_PASSWORD_ENV} environment variable.')

        return res

    def __exec_sql(self, con, sql):
        with con.cursor() as cur:
            cur.execute(sql)
            res = cur.fetchall()
            if len(res) <= 0:
                raise exc.NoDataException('Failed with no data.')
            return res

    def connection(self):
        return psycopg2.connect(host='movies-db', **self.con_params)

    def count_movies(self, con):
        """
        Counts movies in DB
        Args:
            con (object): DB connection
        Returns:
            count (int): movies count
        Side effect:
            self.result is filled with return vaule
        """
        sql = f'SELECT count(*) from {self.movies_tb}'
        res = self.__exec_sql(con, sql)
        self.results['movies_count'] = res[0][0]
        return res[0][0]

    def most_common_genre(self, con):
        """
        Selects and returns most common genres
        Args:
            con (object): DB connection
        Returns:
            genres (List[tuple]): List of tuples (genre_name, occurence_count)
        Side effect:
            self.result is filled with return vaule
        """
        sql = f"""
        with genres as (
            select
                unnest(regexp_split_to_array(genres, E'\\\\|')) as genre,
                count(*) as cnt
            from {self.movies_tb}
            group by 1 order by 1
        ),
        max_cnt as (
            select
                max(cnt) as max
                from genres
        )
        select genres.genre, genres.cnt 
        from genres
        left join max_cnt on 1=1
        where cnt=max_cnt.max
        """
        res = self.__exec_sql(con, sql)
        self.results['most_common_genre'] = res
        return res

    def top_movies(self, con, count=10):
        """
        Selects and returns top <count> movies with highest rates
        Args:
            con (object): DB connection
            count (int): How many movies
        Returns:
            genres (List[tuple]): List of tuples (movie_id, title, avg_rate, rates_count)
        Side effect:
            self.result is filled with return vaule
        """
        sql = f"""
        with rats as (
            select movieId, avg(rating), count(*) cnt
            from {self.ratings_tb}
            group by 1
        ),
        count_perc as (
            select (percentile_cont(0.99) WITHIN GROUP (ORDER BY rats.cnt)::int) as p99
            from rats
        ),
        top_m as (
            select movieId, avg, cnt
            from rats
            cross join count_perc
            where rats.cnt >= count_perc.p99
            order by rats.avg desc
            limit {count}
        )
        select m.movieId, m.title, t.avg, t.cnt
        from {self.movies_tb} m
        right join top_m t on t.movieId=m.movieId
        """
        res = self.__exec_sql(con, sql)
        self.results[f'top_{count}'] = res
        return res

    def most_active_users(self, con, count=5):
        """
        Selects and returns top <count> actively rating users
        Args:
            con (object): DB connection
            count (int): How many users
        Returns:
            genres (List[tuple]): List of tuples (user_id, ratings_count)
        Side effect:
            self.result is filled with return vaule
        """
        sql = f"""
        select userId, count(*) from {self.ratings_tb} group by 1 order by 2 desc limit {count}
        """
        res = self.__exec_sql(con, sql)
        self.results['most_active_users'] = res
        return res

    def first_and_last_ratings(self, con):
        """
        Selects and returns fisrt and last ratings in dataset
        Args:
            con (object): DB connection
        Returns:
            genres (List[tuple]): List of tuples (movie, user_id, rating, timestamp)
        Side effect:
            self.result is filled with return vaule
        """
        sql = f"""
        with min_max as (
            select min(timestamp), max(timestamp)
            from {self.ratings_tb}
        ),
        first_last as (
            select userId, movieId, rating, timestamp
            from {self.ratings_tb} r
            cross join min_max mm
            where mm.min=r.timestamp or mm.max=r.timestamp
        )
        select m.title, fl.userId, fl.rating, fl.timestamp 
        from first_last fl 
        left join {self.movies_tb} m on m.movieId=fl.movieId
        order by fl.timestamp
        """
        res = self.__exec_sql(con, sql)
        self.results['first_last_ratings'] = res
        return res

    def movies_from_year(self, con, year=1990):
        """
        Selects and returns all movies from 1990
        Args:
            con (object): DB connection
        Returns:
            genres (List[tuple]): List of tuples (movieId, title)
        Side effect:
            self.result is filled with return vaule
        """
        sql = f"select movieId, title from {self.movies_tb} where title ~ ' \({year}\)'"
        res = self.__exec_sql(con, sql)
        self.results[f'movies_from_{year}'] = res
        return res

    def audit(self):
        with self.connection() as con:
            self.count_movies(con)
            self.most_common_genre(con)
            self.top_movies(con)
            self.most_active_users(con)
            self.first_and_last_ratings(con)
            self.movies_from_year(con)

    def save_result(self):
        with open(self.result_file, 'w') as f:
            for what, result in self.results.items():
                if isinstance(result, list):
                    f.write(f'{what}: \n')
                    for it in result:
                        f.write(f'  - {it}\n')
                    f.write('\n')
                else:
                    f.write(f'{what}: {result}\n\n')
            f.flush()
            f.close()
