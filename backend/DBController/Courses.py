from datetime import datetime

from Schedulizer.constants import OUTDATED_COURSE_METADATA_TIMEDELTA
from DBController.MysqlConnection import get_connection
from Schedulizer.CourseClass import Course


def __check_add_course_table(course_table: str):
    """Check that the course table exists, if it doesn't exist make a new courses table

    Args:
        course_table: course_table: SQL course_table name.
    """
    connection = get_connection()
    cur = connection.cursor(prepared=True)

    if not isinstance(course_table, str):
        raise TypeError("course_table must be a string")

    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='%s'" % course_table)

    if cur.fetchone()[0] != 1:  # fac table does not exist yet, add new fac table
        # ^^^ cur.fetchone()[0] == 1  # means a table exists
        cur.execute("CREATE TABLE %s ("
                    "crn INT(10) NOT NULL, "
                    "fac VARCHAR(5) NOT NULL, "
                    "uid VARCHAR(5) NOT NULL, "
                    "class_type VARCHAR(25) NOT NULL, "
                    "title VARCHAR(25) NOT NULL, "
                    "section VARCHAR(5) NOT NULL, "
                    "class_time JSON NOT NULL, "
                    "is_linked BOOL NOT NULL, "
                    "link_tag VARCHAR(5), "
                    "seats_filled INT(3) NOT NULL, "
                    "max_capacity INT(3) NOT NULL, "
                    "instructors VARCHAR(100), "
                    "is_virtual BOOL NOT NULL, "
                    "metadata TIMESTAMP NOT NULL, "
                    "PRIMARY KEY(crn))" % course_table)
        connection.commit()

    cur.close()
    connection.close()


def is_up_to_date(course_table: str, fac: str, uid: bool):
    """

    Args:
        course_table: SQL course_table name.
        fac: FAC of the course (Ex: MATH, PHY, CHEM).
        uid: UID of the course (Ex: 1010U, 1020U, 1800U).

    Returns:
        Boolean, True if the course record is up-to-date, False if the course record does not exist or isn't up-to-date.
    """
    __check_add_course_table(course_table=course_table)

    connection = get_connection()
    cur = connection.cursor(prepared=True)

    cur.execute("SELECT metadata FROM %s WHERE fac='%s' AND uid='%s' LIMIT 1" % (course_table, fac, uid))

    metadata = cur.fetchone()

    cur.close()
    connection.close()

    # Note: The server and MySQL DBController should be running on UTC
    if metadata is None:
        return False
    elif (datetime.utcnow() - metadata[0]) < OUTDATED_COURSE_METADATA_TIMEDELTA:  # Data is not stale
        # Note: metadata is now needed to search index 0 since the fetchone result is (datetime.datetime(),)
        # If there is no record, fetchone returns None.
        return True
    else:
        return False


def update_course_record(course_table: str, c: Course):
    """Update record of a course record on the courses table

    Args:
        course_table: SQL course_table name.
        c: Course to update record for
    """

    if not isinstance(c, Course):
        raise TypeError("Expected type Course")

    __check_add_course_table(course_table=course_table)  # Ensure table exists

    connection = get_connection()
    cur = connection.cursor(prepared=True)

    cur.execute("SELECT COUNT(*) FROM %s WHERE crn=%s" % (course_table, c.crn))
    # Select a pre-existing record with matching crn key

    if cur.fetchone()[0] == 0:  # Course does not have a pre-existing record, create new record
        cur.execute("INSERT INTO %s "
                    "(crn, fac, uid, class_type, title, section, class_time, is_linked, link_tag, seats_filled, "
                    "max_capacity, instructors, is_virtual, metadata) "
                    "VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', %r, '%s', %d, %d, '%s', %r, NOW())" % (
                        course_table, c.crn, c.fac, c.uid, c.class_type[:25], c.title[:25], c.section,
                        c.get_serialized_self_class_time(), c.is_linked, c.link_tag, c.seats_filled, c.max_capacity,
                        c.instructors[:100], c.is_virtual)
                    )

    else:  # Course has a pre-existing record, update record
        cur.execute("UPDATE %s SET "
                    "class_time='%s', is_linked=%r, link_tag='%s', seats_filled=%d, instructors='%s', is_virtual=%r, "
                    "metadata=NOW() "
                    "WHERE crn=%d" % (
                        course_table, c.get_serialized_self_class_time(), c.is_linked, c.link_tag, c.seats_filled,
                        c.instructors[:100], c.is_virtual, c.crn)
                    )

    connection.commit()
    cur.close()
    connection.close()


def __sql_to_course_decode(sql_result: list) -> Course:
    """

    Args:
        sql_result: MySQL cursor results of a single course element

    Returns:
        Decoded course object
    """
    return Course(crn=sql_result[0],
                  fac=sql_result[1],
                  uid=sql_result[2],
                  class_type=sql_result[3],
                  title=sql_result[4],
                  section=sql_result[5],
                  class_time=Course.deserialize_to_class_time(sql_result[6]),
                  is_linked=sql_result[7],
                  link_tag=sql_result[8],
                  seats_filled=sql_result[9],
                  max_capacity=sql_result[10],
                  instructors=sql_result[11],
                  is_virtual=sql_result[12])


def get_course_via_crn(course_table: str, crn: int) -> Course | None:
    """Get Course object of a course according to CRN from DBController

    Args:
        course_table: SQL course_table name.
        crn: CRN code to pull Course by.

    Returns:
        Course object of the matching crn. If a record does not exist, returns None.
    """
    if isinstance(crn, int):
        crn = str(crn)
    elif not isinstance(crn, str):
        raise TypeError("Expected type str or int")

    __check_add_course_table(course_table)

    connection = get_connection()
    cur = connection.cursor(prepared=True)

    cur.execute("SELECT * FROM %s WHERE crn=%s" % (course_table, crn))
    # Select a pre-existing record with matching crn key

    sql_result = cur.fetchone()

    connection.commit()
    cur.close()
    connection.close()

    if sql_result is None:
        return None
    else:
        return __sql_to_course_decode(sql_result)


def get_courses_via_fac_uid(course_table: str, fac: str, uid: str) -> list[Course] | None:
    """

    Args:
        course_table: SQL course_table name.
        fac: FAC of the course (Ex: MATH, PHY, CHEM)
        uid: UID of the course (Ex: 1010U, 1020U, 1800U)

    Returns:
        List of course objects of the matching FAC and UID. If no records exist, returns None.
    """
    if not isinstance(fac, str) or not isinstance(uid, str):
        raise TypeError("Expected type str")

    __check_add_course_table(course_table)

    connection = get_connection()
    cur = connection.cursor(prepared=True)

    cur.execute("SELECT * FROM %s WHERE fac='%s' AND uid='%s'" % (course_table, fac, uid))

    sql_result = cur.fetchall()

    connection.commit()
    cur.close()
    connection.close()

    if sql_result is None or sql_result == []:
        return None
    else:
        return [__sql_to_course_decode(course_element) for course_element in sql_result]
