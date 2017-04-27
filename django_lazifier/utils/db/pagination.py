import math
from django_lazifier.utils.builtin_types.str import Str
from django_lazifier.utils.db.db_helper import Db
from django_lazifier.utils.db.db_normalization import DbNorm


class Pagination:
    """
    Break a query into multiple pages.
    """
    row_count = -1
    page_count = -1

    def __init__(self, cursor, query: str, rows_per_page=10, current_page=1):
        """
        :param cursor: connection.cursor()
        :param query: the query without the limit command
        :param rows_per_page:
        :param current_page: 1-index (first page is 1)
        :return:
        """
        self.backend = DbNorm.get_backend_engine()

        self.cursor = cursor
        self.query = query
        self.rows_per_page = Str.int_val(rows_per_page, 10)
        self.current_page = Str.int_val(current_page, 1)

        self.count()

        if self.row_count > 0:
            self.page_count = math.ceil(self.row_count / rows_per_page)

    def count(self):
        if self.row_count == -1:
            # if not Str.contains(self.query, 'GROUP BY'):
            #     query = self.query.strip()
            #     exp = re.compile(r'^SELECT (.+) FROM', re.IGNORECASE | re.DOTALL)
            #     query = exp.sub('SELECT COUNT(*) FROM', query)
            #     try:
            #         self.cursor.execute(query)
            #         row = self.cursor.fetchone()
            #         self.row_count = int(row[0])
            #     except:
            #         return -1
            # else:
            self.row_count = Db.group_count(self.cursor, self.query)

        return self.row_count

    def get_current_page_query(self):
        """
        Get the mysql query for the current page.
        :return {str}:
        """
        return self.get_page_query(self.current_page)

    def get_page_query(self, page_number):
        """
        Get the mysql query for the specified page.
        :param page_number: 1-index (first page is 1)
        :return:
        """
        # [LIMIT {[offset,] row_count | row_count OFFSET offset}]

        page_number = Str.int_val(page_number, 1)

        if page_number <= 0:
            page_number = 1
        elif self.row_count > 0 and page_number > self.page_count:
            page_number = self.page_count

        offset = (page_number - 1) * self.rows_per_page
        row_count = self.rows_per_page

        db_norm = DbNorm.get_db_normalizer()
        limit_query = db_norm.limit(offset, row_count)
        query = '%s %s' % (self.query, limit_query)
        return query

    def get_current_page(self):
        return self.get_page(self.current_page)

    def get_page(self, page_number):
        query = self.get_page_query(page_number)
        self.cursor.execute(query)
        return self.cursor.fetchall()
