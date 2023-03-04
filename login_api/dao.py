import logging
import pymysql


logger = logging.getLogger(__name__)


def _get_mysql_connection(conf: dict):
    logger.debug("Initializing database connection.")
    try:
        return pymysql.connect(host=conf["HOST"],
                               user=conf["USER"],
                               password=conf["PASSWORD"],
                               db=conf["DB"])
    except Exception as ex:
        logger.exception(ex)


async def execute_no_result_query(query: str, conf: dict):
    db = _get_mysql_connection(conf=conf)
    with db.cursor() as cursor:
        cursor.execute(query)
    db.commit()


async def execute_results_query(query: str, conf: dict):
    results = None
    mysql_db = _get_mysql_connection(conf=conf)
    with mysql_db.cursor() as cursor:
        cursor.execute(query)
        columns = cursor.description
        results = [{columns[index][0]: column_value for index, column_value in enumerate(row)}
                   for row in cursor.fetchall()]

    mysql_db.close()

    return results


async def execute_single_result_query(query: str, conf: dict):
    result = None
    mysql_db = _get_mysql_connection(conf=conf)
    with mysql_db.cursor() as cursor:
        cursor.execute(query)
        columns = cursor.description
        result = cursor.fetchone()
        result = result if not result else \
            {columns[index][0]: column_value for index, column_value in enumerate(result)}

    mysql_db.close()

    return result
