import re


class Db:
    @classmethod
    def fetchall_dict(cls, cursor):
        """
        Convert fetchall result into a dictionary(column: row_value) instead of list of tuples.
        """
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

    @classmethod
    def fetchall(cls, cursor, query, default_value):
        if not cursor or not query:
            return default_value

        try:
            cursor.execute(query)
            return cursor.fetchall()
        except:
            return default_value

    @classmethod
    def group_count(cls, cursor, query):
        """
        Count the number of groups when the statement contains "Group By"
            ie. row count instead of the count of the sub-group

        :param cursor:
        :param query:
        :return:
        """
        query = query.strip()

        exp = re.compile(r'^SELECT (.+) FROM', re.IGNORECASE | re.DOTALL)
        query = exp.sub('SELECT 1 FROM', query)

        query = """SELECT COUNT(*) FROM (
                    %s
                ) grp_tbl""" % query

        try:
            cursor.execute(query)
            row = cursor.fetchone()
            if row:
                return int(row[0])
        except:
            return -1


