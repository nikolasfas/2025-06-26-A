import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._circuits = []
        self._positions = []
        self._graph = nx.Graph()
        self._maxC = None


    def handleCampionato(self, K, M):

        self._bestObj = []
        parziale = []
        self._bestI = 0

        self._ricorsione(parziale, K, M, 0, 0)

        return self._bestObj, self._bestI

    def _ricorsione(self, parziale, K, M, imprevedibilità, startIndex):
        print(parziale, imprevedibilità)

        if len(parziale) == K:
            if imprevedibilità > self._bestI:
                self._bestObj = copy.deepcopy(parziale)
                self._bestI = imprevedibilità
                return

        for i in range(startIndex, len(self._maxC)):
            c = self._maxC[i]

            if len(c.positions) >= M:
                nP = 0
                nPT = 0
                for lista_pos in c.positions.values():
                    for pos in lista_pos:
                        if pos.position is not None:
                            nP += 1
                        nPT += 1
                    I = 1-nP/nPT
                    parziale.append(c)
                    self._ricorsione(parziale, K, M, imprevedibilità + I, i+1)
                    parziale.pop()

    def _maxIncidentEdgeWeight(self, node):
        maxPeso = 0

        for u, v, data in self._graph.edges(node, data=True):
            peso = data["weight"]

            if peso > maxPeso:
                maxPeso = peso

        return maxPeso

    def getCompConn(self):
        self._maxC = list(max(nx.connected_components(self._graph), key=len))

        result = []

        for node in self._maxC:
            pesoMax = self._maxIncidentEdgeWeight(node)
            result.append((node, pesoMax))


        result.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return result

    def buildGraph(self, startY, endY):
        self._graph.clear()

        self._circuits = DAO.getAllCircuits()
        self._positions = DAO.getAllPositions(startY, endY)

        self.createVariables()

        self._graph.add_nodes_from(self._circuits)

        for i in range(len(self._circuits)):
            c1 = self._circuits[i]

            for j in range(i + 1, len(self._circuits)):
                c2 = self._circuits[j]

                if len(c1.positions) != 0 and len(c2.positions) != 0:
                    totPilotiC1 = self._countFinishedDrivers(c1)
                    totPilotiC2 = self._countFinishedDrivers(c2)

                    peso = totPilotiC1 + totPilotiC2

                    self._graph.add_edge(c1, c2, weight=peso)

    def createVariables(self):
        for circuit in self._circuits:
            circuit.positions.clear()

        for position in self._positions:
            for circuit in self._circuits:
                if position.circuitId == circuit.circuitId:

                    if position.year not in circuit.positions:
                        circuit.positions[position.year] = []

                    circuit.positions[position.year].append(position)

    def _countFinishedDrivers(self, circuit):
        count = 0

        for lista_posizioni in circuit.positions.values():
            for position in lista_posizioni:
                if position.position is not None:
                    count += 1

        return count

    def getGraphDetails(self):
        nodes = self._graph.nodes()
        edges = self._graph.edges(data=True)
        return nodes, edges

    def getAllYears(self):
        return DAO.getAllYears()

    def gettAllCircuits(self):
        self._circuits = DAO.getAllCircuits()
        return self._circuits

    def getAllPositions(self, startY, endY):
        self._positions = DAO.getAllPositions(startY, endY)
        return self._positions