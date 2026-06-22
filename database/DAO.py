

from database.DB_connect import DBConnect
from model.circuit import Circuit
from model.position import Position


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuit(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct `year` 
                    from races r 
                    order by r.`year` desc """
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAllPositions(startY, endY):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select c.circuitId , r.raceId, r.`year` , r2.driverId , r2.`position` 
                    from races r, results r2 , circuits c 
                    where r.raceId = r2.raceId 
                    and c.circuitId = r.circuitId 
                    and r.`year` between %s and %s"""

        cursor.execute(query, (startY, endY,))

        res = []
        for row in cursor:
            res.append(Position(**row))

        cursor.close()
        cnx.close()
        return res

